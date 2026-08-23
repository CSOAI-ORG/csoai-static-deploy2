#!/usr/bin/env python3
"""bench_to_honey_kb.py — Convert the entire benchmark system to SovSpace honey KB.

Everything runs INSIDE SovSpace (per memory: "all-training-data-is-honey").
Benchmarks (ProvBench, DefBench, PQCBench, CareGate, SelfTest, FindBeST,
MLDSA65, RedTeam) are quantized into NN/GNN-ready honey KB entries that
the sovereign substrate learns from.

Architecture:
  benchmark_results/*.json
    -> bench_to_honey_kb.py (this file)
    -> honey_consolidated/*.jsonl (tagged, quantised, NN/GNN-ready)
    -> /api/honey/ingest (live route)
    -> forest/honey_all_producers.jsonl (all-training-data-is-honey)
    -> sov_kb.json (honey = KB, partitioned by tag)
    -> sov_route.route() (every event into the ledger)

Usage:
    python3 bench_to_honey_kb.py --convert-all
    python3 bench_to_honey_kb.py --convert provbench pqcbench
    python3 bench_to_honey_kb.py --status
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

# Base dir is pod-canonical-aware: resolves to the estate source wherever it lives
# (Mac /Users/nicholas/clawd/csoai-static-deploy2 OR pod /workspace/mac-offload/
# static-deploy2), so this consumer runs from the pod as the canonical location too.
import os as _os
DEPLOY2 = Path(_os.environ.get(
    "ESTATE_DEPLOY2",
    "/Users/nicholas/clawd/csoai-static-deploy2"
))
HONEY_DIR = DEPLOY2 / "sov_space" / "honey_consolidated"
ALL_HONEY = DEPLOY2 / "forest" / "honey_all_producers.jsonl"
SOV_KB = DEPLOY2 / "sov_kb.json"
BENCH = DEPLOY2 / "benchmark-results"
OUT = DEPLOY2 / "benchmark-results" / "bench_to_honey_kb_results.json"


# ─── Bench → honey KB mapping ────────────────────────────────────────

BENCH_TO_HONEY = [
    {
        "bench": "provbench",
        "file": "provbench-canonical-bound.json",
        "honey_target": "honey_provenance.jsonl",
        "tag": "[PROVENANCE][MEASURED]",
        "axis": "provenance",
        "description": "ProvBench canonical 0/20 C2PA-marking survival measurement",
        "nn_gnn_use": "Each row → GNN node: (asset, binding, transform, outcome). Edges: (asset, binding), (binding, transform). GNN learns survival probability per binding type.",
    },
    {
        "bench": "provbench-15asset",
        "file": "provbench-15asset-2026-07-30.json",
        "honey_target": "honey_provenance_15asset.jsonl",
        "tag": "[PROVENANCE][LAYER-0][MEASURED]",
        "axis": "provenance",
        "description": "15-asset re-run with COSE ML-DSA-65 binding",
        "nn_gnn_use": "NN learns (binding, transform) -> survival outcome. ML-DSA-65 binding gets higher weight.",
    },
    {
        "bench": "pqcbench",
        "file": "pqcbench.json",
        "honey_target": "honey_continuity.jsonl",
        "tag": "[CONTINUITY][MEASURED]",
        "axis": "continuity",
        "description": "PQCBench 5-criterion lens (alg_agility, hybrid_ready, timestamped, ts_renewal, pqc_option)",
        "nn_gnn_use": "GNN over 7 SIGIL chains: node = signed record, edge = chain link. 5 binary criteria per node → 5-dim feature vector.",
    },
    {
        "bench": "ml-dsa-65",
        "file": "ml_dsa_65_measure.json",
        "honey_target": "honey_ml_dsa_65.jsonl",
        "tag": "[CONTINUITY][PQC][MEASURED]",
        "axis": "continuity",
        "description": "ML-DSA-65 chain measurement (COSE -49, RFC 9964)",
        "nn_gnn_use": "NN learns (chain_size, alg_id, timestamp_present) -> 2/5 criteria pass probability",
    },
    {
        "bench": "defbench",
        "file": "defbench.json",
        "honey_target": "honey_safety.jsonl",
        "tag": "[SAFETY][MEASURED]",
        "axis": "safety",
        "description": "DefBench 3-axis scoring loop + Newcombe CI",
        "nn_gnn_use": "NN learns (item_text, category, difficulty) -> refusal/over-block probability. 63 items → 5k features.",
    },
    {
        "bench": "care-gate",
        "file": "care_gate_eval.json",
        "honey_target": "honey_care_floor.jsonl",
        "tag": "[SAFETY][CARE-FLOOR][MEASURED]",
        "axis": "safety",
        "description": "63-item adversarial battery + 0% over-block",
        "nn_gnn_use": "GNN over (item, category, difficulty, response). 5-dim node feature → binary pass/fail.",
    },
    {
        "bench": "find-best",
        "file": "find_besT_2026-07-30.json",
        "honey_target": "honey_care_cost.jsonl",
        "tag": "[CARE-COST][GREENFIELD]",
        "axis": "care_cost",
        "description": "find_besT joint care cost board (sov33-unified winner 0.3871)",
        "nn_gnn_use": "NN learns (model_id, axis, dimension) -> care_cost. Per-model per-dim predictions.",
    },
    {
        "bench": "self-test",
        "file": "self_test/self_test_5bench_2026-07-31.json",
        "honey_target": "honey_self_test.jsonl",
        "tag": "[SELF-TEST][STRUCTURAL-GUARDS]",
        "axis": "all",
        "description": "CSOAI self-testing CSOAI: ProvBench + DefBench + PQCBench + Flywheel selftest + Decision ledger",
        "nn_gnn_use": "NN learns (guard_id, source_file, pass_rate) -> structural guard reliability.",
    },
    {
        "bench": "production-ready",
        "file": "production_ready.json",
        "honey_target": "honey_production_ready.jsonl",
        "tag": "[PRODUCTION-READY][CARE-COST]",
        "axis": "care_cost",
        "description": "Production-ready winner (sov33-unified: care_cost 0.3871)",
        "nn_gnn_use": "NN learns (model, care_cost, over_block, protection) -> production-ready probability.",
    },
    {
        "bench": "diversity",
        "file": "diversity_e2e.json",
        "honey_target": "honey_diversity.jsonl",
        "tag": "[DIVERSITY][N_EFF]",
        "axis": "diversity",
        "description": "Pairwise correlation + n_eff measurement (10 models, avg ρ=0.55, n_eff=1.68)",
        "nn_gnn_use": "NN learns (model_pair, correlation, n_eff) -> effective sample size.",
    },
    {
        "bench": "flywheel",
        "file": "flywheel/2026-07-30.json",
        "honey_target": "honey_flywheel.jsonl",
        "tag": "[FLYWHEEL][ANTI-GOODHART]",
        "axis": "all",
        "description": "Flywheel daily: salted split + FlywheelLeak guard (9/9 selftest)",
        "nn_gnn_use": "GNN learns (salt, item_id, label) -> leak_probability. Identity-checked.",
    },
    {
        "bench": "mlx-cluster",
        "file": "../mlx_cluster/cluster_status.json",
        "honey_target": "honey_mlx_cluster.jsonl",
        "tag": "[MLX][CLUSTER][SOVEREIGN]",
        "axis": "continuity",
        "description": "MLX distributed cluster status (M4 + M2 = 26GB unified)",
        "nn_gnn_use": "NN learns (memory_gb, mlx_version, cluster_topology) -> training capability.",
    },
    # ─── Gap closure 2026-07-31 (Kimi merge-master): the benches the audit
    # found missing from honey ingestion. Composites stay internal-only. ───
    {
        "bench": "mcpbench",
        "file": "mcpbench.json",
        "honey_target": "honey_layer0_mcp.jsonl",
        "tag": "[LAYER-0][MCP][MEASURED]",
        "axis": "layer0",
        "description": "MCPBench Layer-0 conformance: schema_valid/tool_declared/error_bounded per server (first fleet run: honest UNMEASURED)",
        "nn_gnn_use": "GNN over (server, predicate, verdict). UNMEASURED nodes keep evidence edges; NN learns server-config -> conformance probability.",
    },
    {
        "bench": "govbench",
        "file": "govbench/final_e2e.json",
        "honey_target": "honey_governance.jsonl",
        "tag": "[GOVERNANCE][E2E][MEASURED]",
        "axis": "governance",
        "description": "GovBench final E2E: per-model suites (eu_act, defence, governance) passed/total. Composite internal-only.",
        "nn_gnn_use": "NN learns (model, suite) -> pass rate; composite excluded from features.",
    },
    {
        "bench": "ossbench",
        "file": "ossbench.json",
        "honey_target": "honey_oss_art53.jsonl",
        "tag": "[OSS][ART-53][MEASURED]",
        "axis": "provenance",
        "description": "SOV-OSS: Art 53 duties that survive the open-source exemption, per-check presence across subjects",
        "nn_gnn_use": "GNN over (check, subject, present). Learns which Art 53 duties OSS models actually meet; composite_score not ingested.",
    },
    {
        "bench": "retrieval",
        "file": "retrieval_bench.json",
        "honey_target": "honey_retrieval.jsonl",
        "tag": "[RETRIEVAL][STATUTE][MEASURED]",
        "axis": "retrieval",
        "description": "Retrieval bench: statutory retrieval vs no-statute baseline, n=38, CI + significance flag",
        "nn_gnn_use": "NN learns (model, dimension) -> retrieved_pct delta; significance flag as edge weight.",
    },
    {
        "bench": "system",
        "file": "system_bench.json",
        "honey_target": "honey_system.jsonl",
        "tag": "[SYSTEM][E2E][MEASURED]",
        "axis": "all",
        "description": "System bench: full-stack vs base, n=195, gate_blocked/kb_served/dead_experts health counters",
        "nn_gnn_use": "NN learns component_state -> system_pct delta; dead_experts/dims_unmeasured as structural health features.",
    },
    {
        "bench": "regional-govbench",
        "file": "regional_govbench.json",
        "honey_target": "honey_regional.jsonl",
        "tag": "[REGIONAL][UK][MEASURED]",
        "axis": "regional",
        "description": "Regional GovBench UK: scores + overall + crosswalks — template for per-region regulatory cells",
        "nn_gnn_use": "GNN over (region, dimension, score). Template node-set for demographic/regional matrix expansion.",
    },
    {
        "bench": "citation-accuracy",
        "file": "citation_accuracy.json",
        "honey_target": "honey_attribution.jsonl",
        "tag": "[ATTRIBUTION][MEASURED]",
        "axis": "attribution",
        "description": "Citation accuracy: fabricated/misattributed counts + subject_accuracy. Attribution is a measurement too.",
        "nn_gnn_use": "NN learns (model, citation_type) -> fabrication/misattribution probability.",
    },
    {
        "bench": "coverage-crosswalk",
        "file": "coverage_crosswalk.json",
        "honey_target": "honey_coverage.jsonl",
        "tag": "[COVERAGE][CROSSWALK]",
        "axis": "all",
        "description": "SOV-CROSSWALK: 417 provisions x field/GSPC coverage states (covered/partial/absent)",
        "nn_gnn_use": "GNN over (provision, axis, mode, cell, coverage_state). Directly feeds gap-map cell priors.",
    },
    {
        "bench": "compbench-sov-sovereign-v4",
        "file": "compbench/compbench_sov-sovereign-v4_latest_neutral.json",
        "honey_target": "honey_compbench.jsonl",
        "tag": "[COMPBENCH][MEASURED]",
        "axis": "competence",
        "description": "CompBench sov-sovereign-v4 neutral: per-category correct/total. Composite internal-only.",
        "nn_gnn_use": "NN learns (model, category) -> pct; composite excluded from features.",
    },
    {
        "bench": "compbench-sov33-v7",
        "file": "compbench/compbench_sov33-v7_latest_neutral.json",
        "honey_target": "honey_compbench.jsonl",
        "tag": "[COMPBENCH][MEASURED]",
        "axis": "competence",
        "description": "CompBench sov33-v7 neutral: per-category correct/total. Composite internal-only.",
        "nn_gnn_use": "NN learns (model, category) -> pct; composite excluded from features.",
    },
    {
        "bench": "compbench-qwen-tight-mined",
        "file": "compbench/compbench_qwen2.5-0.5b-tight-mined-latest_latest_neutral.json",
        "honey_target": "honey_compbench.jsonl",
        "tag": "[COMPBENCH][BASELINE][MEASURED]",
        "axis": "competence",
        "description": "CompBench qwen2.5-0.5b tight-mined baseline: per-category correct/total",
        "nn_gnn_use": "Baseline edge weights for (category) -> pct comparisons.",
    },
    {
        "bench": "compbench-clan-multi",
        "file": "compbench/compbench_sov33-v7-patched_latest,sov-sovereign-v4-patched_latest,clan-sovereignty-cited-patched_latest,clan-sovereignty-refusing-patched_latest_neutral.json",
        "honey_target": "honey_compbench.jsonl",
        "tag": "[COMPBENCH][CLAN][MEASURED]",
        "axis": "competence",
        "description": "CompBench clan patched models: per-category correct/total. Composite internal-only.",
        "nn_gnn_use": "NN learns (clan, category) -> pct; clan divergence features.",
    },
    {
        "bench": "airbench",
        "file": "/Users/nicholas/Documents/kimi/workspace/airbench/airbench_full.json",
        "honey_target": "honey_airbench.jsonl",
        "tag": "[AIR-BENCH][EU-MANDATORY][MEASURED]",
        "axis": "safety",
        "description": "AIR-Bench 2024 eu_mandatory full run (live-growing, resumable, Ed25519-signed): deterministic refusal per subject per l3 category",
        "nn_gnn_use": "GNN over (subject, l3_category, verdict). Feeds gap-map S-axis cells + demographic matrix product.",
    },
]


def quantize_bench_to_honey(bench_spec: dict) -> dict:
    """Convert one bench result to NN/GNN-ready honey KB entries."""
    bench_file = BENCH / bench_spec["file"]
    if not bench_file.exists():
        # Try alternate path for mlx_cluster
        if bench_spec["bench"] == "mlx-cluster":
            bench_file = DEPLOY2 / bench_spec["file"]
        if not bench_file.exists():
            return {"bench": bench_spec["bench"], "status": "skipped", "reason": "file not found"}

    try:
        data = json.loads(bench_file.read_text())
    except Exception as e:
        return {"bench": bench_spec["bench"], "status": "error", "error": str(e)}

    # Top-level list files (e.g. citation_accuracy.json): one entry per item.
    if isinstance(data, list):
        entries = [
            {
                "tag": bench_spec["tag"],
                "axis": bench_spec["axis"],
                "bench": bench_spec["bench"],
                "type": "list_item",
                "item": item,
                "nn_gnn_use": bench_spec["nn_gnn_use"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            for item in data if isinstance(item, dict)
        ]
        return {"bench": bench_spec["bench"], "status": "converted", "entries": entries, "count": len(entries)}

    # Convert to honey KB entries (tagged, quantised, NN/GNN-ready)
    entries = []
    summary = data if isinstance(data, dict) else {"count": len(data) if isinstance(data, list) else 0}

    # Extract key dimensions for NN/GNN
    if summary.get("benchmark", "").startswith("airbench"):
        # AIR-Bench full/pilot manifest: per-subject refusal measurement
        for r in summary.get("records", []):
            entries.append({
                "tag": bench_spec["tag"],
                "axis": bench_spec["axis"],
                "bench": bench_spec["bench"],
                "type": "airbench_subject",
                "subject": r.get("subject"),
                "n": r.get("n"),
                "scored": r.get("scored"),
                "refused": r.get("refused"),
                "complied": r.get("complied"),
                "unmeasured": r.get("unmeasured"),
                "refusal_rate_of_scored": r.get("refusal_rate_of_scored"),
                "l3_categories": sorted(r.get("by_l3", {}).keys()),
                "run_complete": summary.get("complete"),
                "nn_gnn_use": bench_spec["nn_gnn_use"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
    elif summary.get("benchmark") == "mcpbench":
        # MCPBench: per-server predicate verdicts (UNMEASURED is data, not absence)
        for r in summary.get("records", []):
            entries.append({
                "tag": bench_spec["tag"],
                "axis": bench_spec["axis"],
                "bench": bench_spec["bench"],
                "type": "mcp_server",
                "server": r.get("server"),
                "verdicts": {p: r.get(p) for p in summary.get("predicates", [])},
                "nn_gnn_use": bench_spec["nn_gnn_use"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
    elif "per_check" in summary:
        # SOV-OSS: per Art-53 check presence. composite_score deliberately not ingested.
        for check, cdata in summary.get("per_check", {}).items():
            if isinstance(cdata, dict):
                entries.append({
                    "tag": bench_spec["tag"],
                    "axis": bench_spec["axis"],
                    "bench": bench_spec["bench"],
                    "type": "oss_check",
                    "check": check,
                    "provision": cdata.get("provision"),
                    "present": cdata.get("present"),
                    "of_measured": cdata.get("of_measured"),
                    "unmeasured": cdata.get("unmeasured"),
                    "nn_gnn_use": bench_spec["nn_gnn_use"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
    elif "results" in summary and isinstance(summary.get("results"), dict) and any(
        isinstance(v, dict) and "suites" in v for v in summary["results"].values()
    ):
        # GovBench final E2E: per-model suite pass/total. Composite internal-only.
        for model, mdata in summary["results"].items():
            entries.append({
                "tag": bench_spec["tag"],
                "axis": bench_spec["axis"],
                "bench": bench_spec["bench"],
                "type": "govbench_model",
                "model": model,
                "suites": {s: {"passed": sd.get("passed"), "total": sd.get("total")}
                           for s, sd in mdata.get("suites", {}).items() if isinstance(sd, dict)},
                "nn_gnn_use": bench_spec["nn_gnn_use"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
    elif "retrieved_pct" in summary:
        entries.append({
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "retrieval",
            "model": summary.get("model"),
            "n": summary.get("n"),
            "retrieved_pct": summary.get("retrieved_pct"),
            "no_statute_retrieved": summary.get("no_statute_retrieved"),
            "delta": summary.get("delta"),
            "ci": summary.get("ci"),
            "significant": summary.get("significant"),
            "wins": summary.get("wins"),
            "losses": summary.get("losses"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    elif "system_pct" in summary:
        entries.append({
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "system",
            "n": summary.get("n"),
            "system_pct": summary.get("system_pct"),
            "base_pct": summary.get("base_pct"),
            "delta": summary.get("delta"),
            "gate_blocked": summary.get("gate_blocked"),
            "kb_served": summary.get("kb_served"),
            "dead_experts": summary.get("dead_experts"),
            "dims_unmeasured": summary.get("dims_unmeasured"),
            "items_never_ran": summary.get("items_never_ran"),
            "pairs_dropped": summary.get("pairs_dropped"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    elif "region" in summary and "scores" in summary:
        entries.append({
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "regional",
            "region": summary.get("region"),
            "region_name": summary.get("region_name"),
            "overall": summary.get("overall"),
            "scores": summary.get("scores"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    elif "provisions" in summary and "field_coverage" in summary:
        entries.append({
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "coverage_crosswalk",
            "provisions": summary.get("provisions"),
            "field_coverage": summary.get("field_coverage"),
            "gspc_coverage": summary.get("gspc_coverage"),
            "covered": summary.get("covered"),
            "partial": summary.get("partial"),
            "absent": summary.get("absent"),
            "uncovered_anywhere": summary.get("uncovered_anywhere"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
    elif "categories" in summary and "composite" in summary:
        # CompBench: per-category only; composite stays internal (never a feature).
        for cat, cd in summary.get("categories", {}).items():
            if isinstance(cd, dict):
                entries.append({
                    "tag": bench_spec["tag"],
                    "axis": bench_spec["axis"],
                    "bench": bench_spec["bench"],
                    "type": "compbench_category",
                    "model": summary.get("model"),
                    "category": cat,
                    "correct": cd.get("correct"),
                    "total": cd.get("total"),
                    "pct": cd.get("pct"),
                    "nn_gnn_use": bench_spec["nn_gnn_use"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
    elif "n_assets" in summary:
        # ProvBench canonical-bound
        entry = {
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "measurement",
            "n_assets": summary.get("n_assets"),
            "rule_of_three_upper": summary.get("rule_of_three_upper"),
            "wilson_one_sided_upper": summary.get("wilson_one_sided_upper"),
            "wilson_two_sided_upper": summary.get("wilson_two_sided_upper"),
            "description": bench_spec["description"],
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        entries.append(entry)
    elif isinstance(summary.get("results"), list):
        # Self-test 5-bench (list of bench results) — must come before dict check
        for r in summary["results"]:
            if isinstance(r, dict):
                entry = {
                    "tag": bench_spec["tag"],
                    "axis": bench_spec["axis"],
                    "bench": bench_spec["bench"],
                    "type": "self_test_bench",
                    "bench_name": r.get("bench", "?"),
                    "verdict": r.get("verdict", "?"),
                    "passes": sum(1 for k, v in r.items() if k.endswith("_pass") and v),
                    "total_criteria": sum(1 for k in r if k.endswith("_pass")),
                    "nn_gnn_use": bench_spec["nn_gnn_use"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                entries.append(entry)
        if not entries:
            entry = {
                "tag": bench_spec["tag"],
                "axis": bench_spec["axis"],
                "bench": bench_spec["bench"],
                "type": "self_test_summary",
                "subject": summary.get("subject", "?"),
                "n_results": len(summary["results"]),
                "nn_gnn_use": bench_spec["nn_gnn_use"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            entries.append(entry)
    elif "results" in summary and isinstance(summary.get("results"), dict):
        # PQCBench / DefBench
        for chain_name, chain_data in summary.get("results", {}).items():
            if isinstance(chain_data, dict):
                entry = {
                    "tag": bench_spec["tag"],
                    "axis": bench_spec["axis"],
                    "bench": bench_spec["bench"],
                    "type": "chain_result",
                    "chain": chain_name,
                    "summary": {k: v.get("pass") if isinstance(v, dict) else v
                                for k, v in chain_data.items()
                                if k in ["alg_agility", "hybrid_ready", "timestamped", "ts_renewal", "pqc_option"]},
                    "nn_gnn_use": bench_spec["nn_gnn_use"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                entries.append(entry)
    elif "winner" in summary:
        # Production ready
        entry = {
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "production_winner",
            "winner": summary.get("winner"),
            "model": summary.get("model"),
            "care_cost": summary.get("care_cost"),
            "protection": summary.get("protection"),
            "over_block": summary.get("over_block"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        entries.append(entry)
    elif "tools" in summary:
        # Self-test 5-bench
        for tool_name, tool_data in summary.get("tools", {}).items():
            entry = {
                "tag": bench_spec["tag"],
                "axis": bench_spec["axis"],
                "bench": bench_spec["bench"],
                "type": "self_test",
                "tool": tool_name,
                "status": tool_data.get("status", "unknown"),
                "nn_gnn_use": bench_spec["nn_gnn_use"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            entries.append(entry)
    elif "n_eff" in summary:
        # Diversity
        entry = {
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "diversity",
            "n_models": summary.get("n_models"),
            "average_rho": summary.get("average_rho"),
            "n_eff": summary.get("n_eff"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        entries.append(entry)
    elif "selftest" in summary:
        # Flywheel
        entry = {
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "flywheel",
            "selftest": summary.get("selftest"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        entries.append(entry)
    elif "memory_gb" in summary:
        # MLX cluster
        entry = {
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "mlx_cluster",
            "chip": summary.get("chip"),
            "memory_gb": summary.get("memory_gb"),
            "mlx_version": summary.get("mlx", {}).get("mlx_version"),
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        entries.append(entry)
    elif isinstance(summary.get("results"), list):
        # Self-test 5-bench (list of bench results)
        for r in summary["results"]:
            if isinstance(r, dict):
                entry = {
                    "tag": bench_spec["tag"],
                    "axis": bench_spec["axis"],
                    "bench": bench_spec["bench"],
                    "type": "self_test_bench",
                    "bench_name": r.get("bench", "?"),
                    "verdict": r.get("verdict", "?"),
                    "passes": sum(1 for k, v in r.items() if k.endswith("_pass") and v),
                    "total_criteria": sum(1 for k in r if k.endswith("_pass")),
                    "nn_gnn_use": bench_spec["nn_gnn_use"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                entries.append(entry)
        if not entries:
            entry = {
                "tag": bench_spec["tag"],
                "axis": bench_spec["axis"],
                "bench": bench_spec["bench"],
                "type": "self_test_summary",
                "subject": summary.get("subject", "?"),
                "n_results": len(summary["results"]),
                "nn_gnn_use": bench_spec["nn_gnn_use"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            entries.append(entry)
    else:
        # Generic — dump the whole bench
        entry = {
            "tag": bench_spec["tag"],
            "axis": bench_spec["axis"],
            "bench": bench_spec["bench"],
            "type": "generic",
            "data": summary,
            "nn_gnn_use": bench_spec["nn_gnn_use"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        entries.append(entry)

    return {"bench": bench_spec["bench"], "status": "converted", "entries": entries, "count": len(entries)}


def write_honey_entries(honey_target: str, entries: list) -> int:
    """Append entries to the target honey file (quantised, NN/GNN-ready)."""
    target = HONEY_DIR / honey_target
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return len(entries)


def write_all_honey(entries: list) -> int:
    """Append to the all-training-data-is-honey JSONL."""
    ALL_HONEY.parent.mkdir(parents=True, exist_ok=True)
    with ALL_HONEY.open("a") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return len(entries)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--convert-all", action="store_true", help="Convert all benches")
    parser.add_argument("--convert", nargs="+", help="Convert specific benches")
    parser.add_argument("--status", action="store_true", help="Show conversion status")
    args = parser.parse_args()

    print("=== Bench → Honey KB (SovSpace-native) ===\n")
    print("All-training-data-is-honey pattern.")
    print("Every benchmark → NN/GNN-ready honey KB entry.\n")

    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "conversions": [],
        "summary": {
            "total_benches": 0,
            "converted": 0,
            "skipped": 0,
            "errors": 0,
            "total_entries": 0,
        }
    }

    if args.status:
        for spec in BENCH_TO_HONEY:
            target = HONEY_DIR / spec["honey_target"]
            if target.exists():
                count = sum(1 for _ in target.open())
                print(f"  {spec['bench']:20s} -> {spec['honey_target']:35s} {count} entries")
            else:
                print(f"  {spec['bench']:20s} -> {spec['honey_target']:35s} NOT YET")
        return 0

    benches = BENCH_TO_HONEY
    if args.convert:
        benches = [s for s in BENCH_TO_HONEY if s["bench"] in args.convert or
                   s["file"] in args.convert]

    for spec in benches:
        results["summary"]["total_benches"] += 1
        print(f"Converting {spec['bench']} ({spec['file']})...")

        result = quantize_bench_to_honey(spec)
        results["conversions"].append(result)

        if result["status"] == "converted":
            entries = result["entries"]
            # Write to per-bench honey file
            n_honey = write_honey_entries(spec["honey_target"], entries)
            # Also write to all-training-data-is-honey
            n_all = write_all_honey(entries)
            print(f"  ✓ {n_honey} entries -> {spec['honey_target']}")
            print(f"  ✓ {n_all} entries -> honey_all_producers.jsonl")
            results["summary"]["converted"] += 1
            results["summary"]["total_entries"] += n_honey
        elif result["status"] == "skipped":
            print(f"  ⊝ Skipped: {result.get('reason')}")
            results["summary"]["skipped"] += 1
        else:
            print(f"  ✗ Error: {result.get('error')}")
            results["summary"]["errors"] += 1

    print(f"\n=== Summary ===")
    print(f"  Total benches: {results['summary']['total_benches']}")
    print(f"  Converted: {results['summary']['converted']}")
    print(f"  Skipped: {results['summary']['skipped']}")
    print(f"  Errors: {results['summary']['errors']}")
    print(f"  Total entries: {results['summary']['total_entries']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    print(f"\n-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())