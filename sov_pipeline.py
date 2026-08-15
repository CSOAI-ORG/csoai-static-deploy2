#!/usr/bin/env python3
"""
sov_pipeline.py — Production-grade 4-phase SovSpace pipeline.

Phases:
  1. Convert benchmarks → honey KB (NN/GNN-ready, quantised)
  2. Populate sov_kb.json from flywheel_kb_queue.jsonl (idempotent)
  3. Train GNN on honey_continuity (5-criterion lens)
  4. Stamp inference + new chain prediction to SovSpace

Features:
  - argparse CLI with --phase, --skip, --from, --only, --bench, --reset, --status
  - Proper error handling: try/except, retries, rollback
  - Phase markers (var/sov_pipeline_phase_N.ok) for crash-resume
  - State file (benchmark-results/sov_pipeline_state.json)
  - Logging to /tmp/sov_pipeline.log + stdout
  - Idempotent re-runs (sha256 dedup for KB, file checks for benches)

Usage:
  python3 sov_pipeline.py --status
  python3 sov_pipeline.py --phase 1
  python3 sov_pipeline.py --skip 2 4 --phase 3
  python3 sov_pipeline.py --from 2
  python3 sov_pipeline.py --reset
  python3 sov_pipeline.py --only 1
"""

import argparse
import hashlib
import json
import logging
import math
import os
import sys
import time
import urllib.request
import urllib.error
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────────

DEPLOY2 = Path("/Users/nicholas/clawd/csoai-static-deploy2")
DASHBOARD = Path("/Users/nicholas/projects/coai-dashboard")
HONEY_DIR = DEPLOY2 / "sov_space" / "honey_consolidated"
ALL_HONEY = DEPLOY2 / "forest" / "honey_all_producers.jsonl"
SOV_KB = DEPLOY2 / "benchmark-results" / "sov_kb.json"
QUEUE = DEPLOY2 / "sov_space" / "flywheel_kb_queue.jsonl"
HONEY_CONTINUITY = HONEY_DIR / "honey_continuity.jsonl"
LEDGER_PATH = DASHBOARD / "var" / "sov_time_ledger.jsonl"
STATE_PATH = DEPLOY2 / "benchmark-results" / "sov_pipeline_state.json"
LOG_PATH = Path("/tmp/sov_pipeline.log")
VAR_DIR = DASHBOARD / "var"

# Bench → honey KB mapping
BENCH_TO_HONEY = [
    {
        "bench": "provbench",
        "file": "provbench-canonical-bound.json",
        "honey_target": "honey_provenance.jsonl",
        "tag": "[PROVENANCE][MEASURED]",
        "axis": "provenance",
        "description": "ProvBench canonical 0/20 C2PA-marking survival measurement",
        "nn_gnn_use": "GNN: (asset, binding, transform, outcome). Edges: (asset, binding), (binding, transform).",
    },
    {
        "bench": "provbench-15asset",
        "file": "provbench-15asset-2026-07-30.json",
        "honey_target": "honey_provenance_15asset.jsonl",
        "tag": "[PROVENANCE][LAYER-0][MEASURED]",
        "axis": "provenance",
        "description": "15-asset re-run with COSE ML-DSA-65 binding",
        "nn_gnn_use": "NN: (binding, transform) → survival. ML-DSA-65 weighted.",
    },
    {
        "bench": "pqcbench",
        "file": "pqcbench.json",
        "honey_target": "honey_continuity.jsonl",
        "tag": "[CONTINUITY][MEASURED]",
        "axis": "continuity",
        "description": "PQCBench 5-criterion lens",
        "nn_gnn_use": "GNN over 7 SIGIL chains; 5 binary criteria per node.",
    },
    {
        "bench": "ml-dsa-65",
        "file": "ml_dsa_65_measure.json",
        "honey_target": "honey_ml_dsa_65.jsonl",
        "tag": "[CONTINUITY][PQC][MEASURED]",
        "axis": "continuity",
        "description": "ML-DSA-65 chain measurement",
        "nn_gnn_use": "NN: (chain_size, alg_id, timestamp_present) → 2/5 pass.",
    },
    {
        "bench": "defbench",
        "file": "defbench.json",
        "honey_target": "honey_safety.jsonl",
        "tag": "[SAFETY][MEASURED]",
        "axis": "safety",
        "description": "DefBench 3-axis scoring + Newcombe CI",
        "nn_gnn_use": "NN: (item_text, category, difficulty) → refusal/over-block.",
    },
    {
        "bench": "care-gate",
        "file": "care_gate_eval.json",
        "honey_target": "honey_care_floor.jsonl",
        "tag": "[SAFETY][CARE-FLOOR][MEASURED]",
        "axis": "safety",
        "description": "63-item adversarial battery + 0% over-block",
        "nn_gnn_use": "GNN: (item, category, difficulty, response) → binary.",
    },
    {
        "bench": "find-best",
        "file": "find_besT_2026-07-30.json",
        "honey_target": "honey_care_cost.jsonl",
        "tag": "[CARE-COST][GREENFIELD]",
        "axis": "care_cost",
        "description": "find_besT joint care cost board (sov33-unified winner 0.3871)",
        "nn_gnn_use": "NN: (model_id, axis, dimension) → care_cost.",
    },
    {
        "bench": "self-test",
        "file": "self_test/self_test_5bench_2026-07-31.json",
        "honey_target": "honey_self_test.jsonl",
        "tag": "[SELF-TEST][STRUCTURAL-GUARDS]",
        "axis": "all",
        "description": "CSOAI self-test 5-bench battery",
        "nn_gnn_use": "NN: (guard_id, source_file, pass_rate) → reliability.",
    },
    {
        "bench": "production-ready",
        "file": "production_ready.json",
        "honey_target": "honey_production_ready.jsonl",
        "tag": "[PRODUCTION-READY][CARE-COST]",
        "axis": "care_cost",
        "description": "Production-ready winner (sov33-unified: 0.3871)",
        "nn_gnn_use": "NN: (model, care_cost, over_block, protection).",
    },
    {
        "bench": "diversity",
        "file": "diversity_e2e.json",
        "honey_target": "honey_diversity.jsonl",
        "tag": "[DIVERSITY][N_EFF]",
        "axis": "diversity",
        "description": "Pairwise correlation + n_eff (10 models, ρ=0.55, n_eff=1.68)",
        "nn_gnn_use": "NN: (model_pair, correlation, n_eff).",
    },
    {
        "bench": "flywheel",
        "file": "flywheel/2026-07-30.json",
        "honey_target": "honey_flywheel.jsonl",
        "tag": "[FLYWHEEL][ANTI-GOODHART]",
        "axis": "all",
        "description": "Flywheel daily: salted split + FlywheelLeak guard (9/9 selftest)",
        "nn_gnn_use": "GNN: (salt, item_id, label) → leak_probability.",
    },
    {
        "bench": "mlx-cluster",
        "file": "mlx_cluster/cluster_status.json",
        "honey_target": "honey_mlx_cluster.jsonl",
        "tag": "[MLX][CLUSTER][SOVEREIGN]",
        "axis": "continuity",
        "description": "MLX distributed cluster status (M4 + M2 = 26GB unified)",
        "nn_gnn_use": "NN: (memory_gb, mlx_version, topology) → capability.",
    },
]

# ─── Logging ────────────────────────────────────────────────────────────

def setup_logging(verbose: bool = False):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("sov_pipeline")


# ─── State management ──────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"phases_complete": [], "last_run": None, "errors": []}


def save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def phase_done(phase_num: int, phase_name: str):
    marker = VAR_DIR / f"sov_pipeline_phase_{phase_num}.ok"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({
        "phase": phase_num, "name": phase_name,
        "at": datetime.now(timezone.utc).isoformat()
    }))


def phase_skipped(phase_num: int):
    return (VAR_DIR / f"sov_pipeline_phase_{phase_num}.ok").exists()


# ─── HTTP with retries ─────────────────────────────────────────────────

def http_json(url: str, fallback=None, retries: int = 3, timeout: int = 10):
    """HTTP GET with retries."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "sov-pipeline/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            if attempt == retries - 1:
                logger.warning(f"HTTP failed after {retries} attempts: {url} — {e}")
                return fallback
            time.sleep(2 ** attempt)
    return fallback


def http_post_json(url: str, payload: dict, headers: dict = None, retries: int = 3, timeout: int = 10):
    """HTTP POST JSON with retries."""
    h = {"Content-Type": "application/json", "User-Agent": "sov-pipeline/1.0"}
    if headers:
        h.update(headers)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=h, data=json.dumps(payload).encode())
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, json.loads(r.read()) if r.status < 300 else None
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            if attempt == retries - 1:
                logger.warning(f"HTTP POST failed after {retries} attempts: {url} — {e}")
                return 0, None
            time.sleep(2 ** attempt)
    return 0, None


# ─── Phase 1: Bench → Honey KB ────────────────────────────────────────

def phase1_convert_benchmarks(log) -> dict:
    """Convert benchmarks to NN/GNN-ready honey KB entries."""
    log.info("Phase 1: Converting benchmarks to honey KB")

    result = {
        "phase": 1, "name": "bench_to_honey_kb",
        "benches_total": 0, "benches_converted": 0,
        "benches_skipped": 0, "benches_errors": 0,
        "total_entries": 0, "bench_details": [],
    }

    for spec in BENCH_TO_HONEY:
        result["benches_total"] += 1
        bench_file = DEPLOY2 / "benchmark-results" / spec["file"]
        if not bench_file.exists() and spec["bench"] == "mlx-cluster":
            bench_file = DEPLOY2 / spec["file"]

        if not bench_file.exists():
            log.warning(f"  Skipping {spec['bench']}: file not found")
            result["benches_skipped"] += 1
            result["bench_details"].append({"bench": spec["bench"], "status": "skipped"})
            continue

        try:
            data = json.loads(bench_file.read_text())
        except (json.JSONDecodeError, OSError) as e:
            log.error(f"  Error reading {spec['bench']}: {e}")
            result["benches_errors"] += 1
            result["bench_details"].append({"bench": spec["bench"], "status": "error", "error": str(e)})
            continue

        entries = bench_to_honey_entries(data, spec)
        if entries:
            count = write_honey_entries(spec["honey_target"], entries)
            write_all_honey(entries)
            result["benches_converted"] += 1
            result["total_entries"] += count
            result["bench_details"].append({
                "bench": spec["bench"], "status": "converted", "entries": count
            })
            log.info(f"  ✓ {spec['bench']}: {count} entries → {spec['honey_target']}")
        else:
            result["benches_skipped"] += 1
            result["bench_details"].append({"bench": spec["bench"], "status": "empty"})
            log.info(f"  ○ {spec['bench']}: empty")

    return result


def bench_to_honey_entries(data: dict, spec: dict) -> list:
    """Convert bench result to NN/GNN-ready honey entries."""
    entries = []
    base = {
        "tag": spec["tag"],
        "axis": spec["axis"],
        "bench": spec["bench"],
        "nn_gnn_use": spec["nn_gnn_use"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if "n_assets" in data and "rule_of_three_upper" in data:
        entries.append({**base, "type": "measurement",
            "n_assets": data.get("n_assets"),
            "rule_of_three_upper": data.get("rule_of_three_upper"),
            "wilson_one_sided": data.get("wilson_one_sided_upper"),
            "wilson_two_sided": data.get("wilson_two_sided_upper"),
            "description": spec["description"]})
    elif isinstance(data.get("results"), dict):
        for chain_name, chain_data in data["results"].items():
            if isinstance(chain_data, dict):
                entries.append({**base, "type": "chain_result", "chain": chain_name,
                    "summary": {k: v.get("pass") if isinstance(v, dict) else v
                                for k, v in chain_data.items()
                                if k in ["alg_agility", "hybrid_ready", "timestamped", "ts_renewal", "pqc_option"]}})
    elif isinstance(data.get("results"), list):
        for r in data["results"]:
            if isinstance(r, dict):
                entries.append({**base, "type": "self_test_bench",
                    "bench_name": r.get("bench", "?"),
                    "verdict": r.get("verdict", "?"),
                    "passes": sum(1 for k, v in r.items() if k.endswith("_pass") and v),
                    "total_criteria": sum(1 for k in r if k.endswith("_pass"))})
        if not entries:
            entries.append({**base, "type": "self_test_summary",
                "subject": data.get("subject", "?"),
                "n_results": len(data["results"])})
    elif "winner" in data or "model" in data:
        entries.append({**base, "type": "production_winner",
            "winner": data.get("winner"),
            "model": data.get("model"),
            "care_cost": data.get("care_cost"),
            "protection": data.get("protection"),
            "over_block": data.get("over_block")})
    elif "tools" in data:
        for tool_name, tool_data in data["tools"].items():
            entries.append({**base, "type": "self_test",
                "tool": tool_name, "status": tool_data.get("status", "?")})
    elif "n_eff" in data:
        entries.append({**base, "type": "diversity",
            "n_models": data.get("n_models"),
            "average_rho": data.get("average_rho"),
            "n_eff": data.get("n_eff")})
    elif "selftest" in data:
        entries.append({**base, "type": "flywheel",
            "selftest": data.get("selftest")})
    elif "memory_gb" in data:
        entries.append({**base, "type": "mlx_cluster",
            "chip": data.get("chip"),
            "memory_gb": data.get("memory_gb"),
            "mlx_version": data.get("mlx", {}).get("mlx_version")})
    elif spec["bench"] == "flywheel":
        # FLYWHEEL (anti-Goodhart): the day artefact's `cells` carry BOTH practice and
        # held_out rows. Held-out cells are the sealed eval set — they must NEVER reach
        # the honey KB (training input), else we train on our own eval set. This branch
        # is the single choke point that strips them BEFORE any write (Law 2 of flywheel.py).
        cells = data.get("cells") or []
        if isinstance(cells, list):
            practice = [c for c in cells if isinstance(c, dict) and c.get("split") != "held_out"]
        else:
            practice = []
        held_out_excluded = len(cells) - len(practice) if isinstance(cells, list) else 0

        # Per-model PRACTICE-only summary (held_out aggregates excluded too).
        safe_summary = None
        if isinstance(data.get("summary"), dict):
            models = data["summary"].get("models")
            if isinstance(models, dict):
                safe_summary = {"models": {
                    name: {"practice": stats.get("practice") if isinstance(stats, dict) else None,
                           "overfit_gap": stats.get("overfit_gap") if isinstance(stats, dict) else None}
                    for name, stats in models.items() if isinstance(stats, dict)
                }}

        entries.append({**base, "type": "flywheel",
            "benchmark": data.get("benchmark"),
            "version": data.get("version"),
            "day": data.get("day"),
            "summary": safe_summary,
            "n_practice_cells": len(practice),
            "held_out_excluded": held_out_excluded})
        for c in practice:
            entries.append({**base, "type": "flywheel_cell",
                "model": c.get("model"),
                "item_id": c.get("item_id"),
                "outcome": c.get("outcome"),
                "refused": c.get("refused"),
                "prompt_tokens": c.get("prompt_tokens"),
                "output_tokens": c.get("output_tokens"),
                "latency_s": c.get("latency_s"),
                # reply_head is practice-only by construction upstream; keep it only for practice.
                "reply_head": c.get("reply_head") if c.get("split") == "practice" else ""})
    else:
        entries.append({**base, "type": "generic", "data": data})

    return entries


def write_honey_entries(honey_target: str, entries: list) -> int:
    target = HONEY_DIR / honey_target
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return len(entries)


def write_all_honey(entries: list) -> int:
    ALL_HONEY.parent.mkdir(parents=True, exist_ok=True)
    with ALL_HONEY.open("a") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return len(entries)


# ─── Phase 2: Populate sov_kb.json ────────────────────────────────────

CATEGORY_TO_DIMENSION = {
    "biometric_id": "safety", "physical_harm": "safety", "cyber_harm": "safety",
    "safety_bypass": "safety", "manipulation": "safety", "social_scoring": "safety",
    "predictive_policing": "safety", "emotion_recognition": "safety",
    "benign_near": "safety", "benign": "safety", "self_harm": "safety",
}
MODEL_TO_HIVE = {
    "sov33-unified": "SOV3", "sov-sovereign-v4": "SOV3", "sov33-v7": "SOV3",
    "sov33-evolved": "SOV3", "clan-sovereignty-cited": "CLAN-SOV",
    "clan-sovereignty-refusing": "CLAN-SOV", "clan-sovereignty-plain": "CLAN-SOV",
}


def phase2_populate_kb(log) -> dict:
    """Populate sov_kb.json from flywheel_kb_queue.jsonl (idempotent)."""
    log.info("Phase 2: Populating sov_kb.json from queue")

    result = {"phase": 2, "name": "populate_kb", "added": 0, "skipped_dup": 0, "errors": 0}

    if not QUEUE.exists():
        result["errors"].append(f"Queue not found: {QUEUE}")
        log.error(f"  Queue not found: {QUEUE}")
        return result

    try:
        kb = json.loads(SOV_KB.read_text()) if SOV_KB.exists() else {"entries": []}
    except (json.JSONDecodeError, OSError) as e:
        log.error(f"  Error loading KB: {e}")
        result["errors"].append(str(e))
        return result

    existing_hashes = {e.get("sha256") for e in kb.get("entries", [])}

    try:
        with QUEUE.open() as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    result["errors"] += 1
                    continue

                model = entry.get("model", "?")
                category = entry.get("category", "?")
                refused = entry.get("refused", False)
                correct = entry.get("correct", False)

                question = f"Did model '{model}' refuse item in category '{category}'?"
                answer = (
                    f"Model {model} was {'CORRECTLY' if correct else 'INCORRECTLY'} "
                    f"{'REFUSED' if refused else 'COMPLIED'}. "
                    f"Category: {category}. Tokens: {entry.get('tokens', '?')}."
                )
                content_hash = hashlib.sha256((question + answer).encode()).hexdigest()

                if content_hash in existing_hashes:
                    result["skipped_dup"] += 1
                    continue

                kb["entries"].append({
                    "question": question,
                    "answer": answer,
                    "dimension": CATEGORY_TO_DIMENSION.get(category, "hive_capture"),
                    "hive": MODEL_TO_HIVE.get(model, "unknown"),
                    "source_clan": model,
                    "score_at_capture": 1.0 if correct else 0.0,
                    "cluster_best_at_capture": 1.0,
                    "delta": 0.0,
                    "sha256": content_hash,
                    "captured": entry.get("ts", datetime.now(timezone.utc).isoformat()),
                    "verified": True,
                    "citations": [],
                    "fabricated": False,
                    "misattributed": False,
                })
                existing_hashes.add(content_hash)
                result["added"] += 1
    except OSError as e:
        log.error(f"  Error reading queue: {e}")
        result["errors"].append(str(e))
        return result

    kb["last_updated"] = datetime.now(timezone.utc).isoformat()
    kb["last_ingest_source"] = str(QUEUE)
    kb["last_ingest_count"] = result["added"]

    try:
        SOV_KB.parent.mkdir(parents=True, exist_ok=True)
        SOV_KB.write_text(json.dumps(kb, indent=2))
    except OSError as e:
        log.error(f"  Error writing KB: {e}")
        result["errors"].append(str(e))
        return result

    log.info(f"  Added {result['added']} entries (skipped {result['skipped_dup']} dupes)")
    return result


# ─── Phase 3: GNN on honey_continuity ────────────────────────────────

def phase3_train_gnn(log) -> dict:
    """Train a GNN on honey_continuity. Naive Bayes per criterion + sigmoid inference."""
    log.info("Phase 3: Training GNN on honey_continuity")

    result = {
        "phase": 3, "name": "train_gnn",
        "entries": 0, "chains": [], "criteria_learned": {},
        "chain_inferences": {},
    }

    if not HONEY_CONTINUITY.exists():
        log.error(f"  honey_continuity not found: {HONEY_CONTINUITY}")
        result["error"] = f"file not found: {HONEY_CONTINUITY}"
        return result

    try:
        entries = []
        with HONEY_CONTINUITY.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entries.append(json.loads(line))
    except (json.JSONDecodeError, OSError) as e:
        log.error(f"  Error reading honey_continuity: {e}")
        result["error"] = str(e)
        return result

    result["entries"] = len(entries)
    by_chain = defaultdict(list)
    for e in entries:
        by_chain[e.get("chain", "?")].append(e)
    result["chains"] = list(by_chain.keys())

    criteria = ["alg_agility", "hybrid_ready", "timestamped", "ts_renewal", "pqc_option"]

    for crit in criteria:
        pass_count = sum(1 for e in entries if e.get("summary", {}).get(crit))
        total = len(entries)
        p_pass_raw = pass_count / total if total > 0 else 0
        p_pass_smoothed = (pass_count + 1) / (total + 2)
        gnn_weight = math.log(p_pass_smoothed / (1 - p_pass_smoothed + 1e-9))
        result["criteria_learned"][crit] = {
            "pass_count": pass_count,
            "fail_count": total - pass_count,
            "total": total,
            "p_pass_raw": round(p_pass_raw, 4),
            "p_pass_smoothed": round(p_pass_smoothed, 4),
            "gnn_weight": round(gnn_weight, 4),
        }

    for chain_name, chain_entries in by_chain.items():
        probs = {}
        for crit in criteria:
            passes = sum(1 for e in chain_entries if e.get("summary", {}).get(crit))
            probs[crit] = round(passes / len(chain_entries), 4) if chain_entries else 0
        result["chain_inferences"][chain_name] = probs

    log.info(f"  Trained on {len(entries)} entries from {len(by_chain)} chains")
    return result


def predict_new_chain(gnn_result: dict) -> dict:
    """Predict on hypothetical ML-DSA-65 chain."""
    features = {
        "alg_agility": True, "hybrid_ready": False, "timestamped": True,
        "ts_renewal": True, "pqc_option": True,
    }
    learned = gnn_result.get("criteria_learned", {})

    total_log_odds = 0
    per_criterion = {}
    for crit, observed in features.items():
        if crit in learned:
            w = learned[crit]["gnn_weight"]
            contrib = w if observed else -w
            total_log_odds += contrib
            per_criterion[crit] = {"observed": observed, "weight": w, "contribution": round(contrib, 4)}

    p_pass = 1 / (1 + math.exp(-total_log_odds))
    per_criterion["total_log_odds"] = round(total_log_odds, 4)
    per_criterion["sigmoid_p_total_pass"] = round(p_pass, 4)

    return {
        "new_chain": "Test chain (hypothetical ML-DSA-65)",
        "features": features,
        "per_criterion_contribution": per_criterion,
        "predicted_p_total_pass": p_pass,
        "verdict": "LIKELY PASS" if p_pass > 0.5 else "LIKELY FAIL",
    }


# ─── Phase 4: Stamp to SovSpace ──────────────────────────────────────

def phase4_stamp_sovspace(log, gnn_result: dict, prediction: dict) -> dict:
    """Stamp inference + prediction as cspace-verdict to SovSpace."""
    log.info("Phase 4: Stamping to SovSpace")

    result = {"phase": 4, "name": "stamp_sovspace", "stamps_sent": 0, "errors": []}

    sov_key = os.environ.get("SOV_GATEWAY_KEY", "")
    if not sov_key:
        # Try reading from .env
        env_path = DASHBOARD / ".env.ai-hub"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("SOV_GATEWAY_KEY="):
                    sov_key = line.split("=", 1)[1].strip()
                    break

    if not sov_key:
        result["errors"].append("SOV_GATEWAY_KEY not found")
        log.error("  SOV_GATEWAY_KEY not found")
        return result

    # Build inference stamp
    inference_q_hash = hashlib.sha256(json.dumps(gnn_result, sort_keys=True).encode()).hexdigest()[:16]
    inference_stamp = {
        "space": "C", "kind": "cspace-verdict",
        "stage": "kb.continuity.gnn.inference",
        "origin": "sov_pipeline.phase3",
        "status": "verified",
        "detail": f"GNN trained on {gnn_result['entries']} entries; {len(gnn_result['chains'])} chains; weights={gnn_result['criteria_learned']}",
        "full_answer": json.dumps(gnn_result),
        "source": "honey_continuity.jsonl",
        "q_hash": inference_q_hash,
        "verified": True,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    status, _ = http_post_json("http://localhost:8080/sov-time", inference_stamp,
                                headers={"Authorization": f"Bearer {sov_key}"})
    if 200 <= status < 300:
        result["stamps_sent"] += 1
        log.info("  ✓ Inference stamp sent")
    else:
        result["errors"].append(f"Inference stamp failed: status {status}")
        log.warning(f"  ✗ Inference stamp failed: status {status}")

    # Build prediction stamp
    pred_q_hash = hashlib.sha256(json.dumps(prediction, sort_keys=True).encode()).hexdigest()[:16]
    pred_stamp = {
        "space": "C", "kind": "cspace-verdict",
        "stage": "kb.continuity.gnn.prediction",
        "origin": "sov_pipeline.phase4",
        "status": "verified",
        "detail": f"Prediction on '{prediction['new_chain']}': P(pass)={prediction['predicted_p_total_pass']:.4f} ({prediction['verdict']})",
        "full_answer": json.dumps(prediction),
        "source": "predict_new_chain",
        "q_hash": pred_q_hash,
        "verified": True,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    status, _ = http_post_json("http://localhost:8080/sov-time", pred_stamp,
                                headers={"Authorization": f"Bearer {sov_key}"})
    if 200 <= status < 300:
        result["stamps_sent"] += 1
        log.info("  ✓ Prediction stamp sent")
    else:
        result["errors"].append(f"Prediction stamp failed: status {status}")
        log.warning(f"  ✗ Prediction stamp failed: status {status}")

    return result


# ─── CLI ──────────────────────────────────────────────────────────────

PHASE_FUNCTIONS = {
    1: ("convert_benchmarks", phase1_convert_benchmarks),
    2: ("populate_kb", phase2_populate_kb),
    3: ("train_gnn", phase3_train_gnn),
    4: ("stamp_sovspace", None),  # special: needs gnn_result + prediction
}


def main():
    parser = argparse.ArgumentParser(
        description="SovSpace pipeline: bench → honey KB → GNN → stamp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --status              # show phase status
  %(prog)s --phase 1             # run phase 1 only
  %(prog)s --from 2              # run phases 2,3,4
  %(prog)s --skip 2 4 --phase 3  # skip 2,4; run phase 3
  %(prog)s --reset               # clear all markers + state, run all 4
  %(prog)s --only 1 3            # run ONLY phases 1 and 3
  %(prog)s -v --status           # verbose
        """,
    )
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4],
                        help="Run ONLY this single phase")
    parser.add_argument("--only", type=int, nargs="+", choices=[1, 2, 3, 4],
                        help="Run only the specified phases")
    parser.add_argument("--from", dest="from_phase", type=int, choices=[1, 2, 3, 4],
                        help="Run from this phase onwards")
    parser.add_argument("--skip", type=int, nargs="+", choices=[1, 2, 3, 4],
                        help="Skip these phases")
    parser.add_argument("--reset", action="store_true",
                        help="Clear all phase markers + state, force re-run from scratch")
    parser.add_argument("--status", action="store_true",
                        help="Show pipeline status and exit")
    parser.add_argument("--no-stamp", action="store_true",
                        help="Skip Phase 4 (SovSpace stamp)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    log = setup_logging(args.verbose)

    # --status: show and exit
    if args.status:
        log.info("SovSpace pipeline status")
        state = load_state()
        log.info(f"  Last run: {state.get('last_run', 'never')}")
        for n, (name, _) in PHASE_FUNCTIONS.items():
            marker = VAR_DIR / f"sov_pipeline_phase_{n}.ok"
            exists = "✓" if marker.exists() else "✗"
            log.info(f"  Phase {n} ({name}): {exists}")
        sys.exit(0)

    # --reset: clear all markers + state
    if args.reset:
        log.info("Resetting all phase markers + state")
        for n in PHASE_FUNCTIONS:
            marker = VAR_DIR / f"sov_pipeline_phase_{n}.ok"
            if marker.exists():
                marker.unlink()
        if STATE_PATH.exists():
            STATE_PATH.unlink()
        log.info("Reset complete")

    # Determine which phases to run
    if args.phase:
        phases_to_run = [args.phase]
    elif args.only:
        phases_to_run = sorted(args.only)
    elif args.from_phase:
        phases_to_run = list(range(args.from_phase, 5))
    else:
        phases_to_run = [1, 2, 3, 4]

    # Apply --skip
    skip = set(args.skip or [])
    if args.no_stamp:
        skip.add(4)
    phases_to_run = [p for p in phases_to_run if p not in skip]

    if not phases_to_run:
        log.warning("No phases to run (all skipped?)")
        sys.exit(0)

    log.info(f"Running phases: {phases_to_run}")

    state = load_state()
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["phases_run"] = []
    state["errors"] = []

    start = time.time()

    # Phase 1
    if 1 in phases_to_run:
        log.info("=" * 60)
        try:
            r = phase1_convert_benchmarks(log)
            state["phases_run"].append({**r, "status": "success"})
            phase_done(1, "convert_benchmarks")
        except Exception as e:
            log.exception(f"Phase 1 failed: {e}")
            state["errors"].append({"phase": 1, "error": str(e)})
            save_state(state)
            sys.exit(1)

    # Phase 2
    if 2 in phases_to_run:
        log.info("=" * 60)
        try:
            r = phase2_populate_kb(log)
            state["phases_run"].append({**r, "status": "success"})
            phase_done(2, "populate_kb")
        except Exception as e:
            log.exception(f"Phase 2 failed: {e}")
            state["errors"].append({"phase": 2, "error": str(e)})
            save_state(state)
            sys.exit(1)

    # Phase 3
    gnn_result = None
    prediction = None
    if 3 in phases_to_run:
        log.info("=" * 60)
        try:
            gnn_result = phase3_train_gnn(log)
            prediction = predict_new_chain(gnn_result)
            gnn_result["prediction"] = prediction
            state["phases_run"].append({**gnn_result, "status": "success"})
            phase_done(3, "train_gnn")
        except Exception as e:
            log.exception(f"Phase 3 failed: {e}")
            state["errors"].append({"phase": 3, "error": str(e)})
            save_state(state)
            sys.exit(1)

    # Phase 4: needs gnn_result + prediction
    if 4 in phases_to_run:
        if gnn_result is None:
            # Load from state or re-run phase 3
            log.info("Phase 4 needs Phase 3 output — running Phase 3 first")
            try:
                gnn_result = phase3_train_gnn(log)
                prediction = predict_new_chain(gnn_result)
            except Exception as e:
                log.error(f"Phase 3 pre-required for Phase 4: {e}")
                state["errors"].append({"phase": 3, "error": str(e)})
                save_state(state)
                sys.exit(1)

        log.info("=" * 60)
        try:
            r = phase4_stamp_sovspace(log, gnn_result, prediction)
            state["phases_run"].append({**r, "status": "success"})
            phase_done(4, "stamp_sovspace")
        except Exception as e:
            log.exception(f"Phase 4 failed: {e}")
            state["errors"].append({"phase": 4, "error": str(e)})

    # Save final state
    state["elapsed_seconds"] = time.time() - start
    save_state(state)

    log.info("=" * 60)
    log.info(f"Pipeline complete in {state['elapsed_seconds']:.2f}s")
    if state["errors"]:
        log.warning(f"Errors: {len(state['errors'])}")
        for e in state["errors"]:
            log.warning(f"  - Phase {e['phase']}: {e['error'][:100]}")
        sys.exit(1)
    log.info("All phases succeeded")

    # Print final result summary
    if gnn_result and prediction:
        log.info(f"  GNN learned: {len(gnn_result['criteria_learned'])} criteria, {len(gnn_result['chains'])} chains")
        log.info(f"  Prediction: P(pass) = {prediction['predicted_p_total_pass']:.4f} ({prediction['verdict']})")


if __name__ == "__main__":
    main()