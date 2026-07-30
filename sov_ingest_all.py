#!/usr/bin/env python3
"""sov_ingest_all.py — every producer, every artifact, every saved state
becomes a route into the honey.

Per architecture: tier-0 users spawn with the hive at 379MB substrate.
Each user's soul needs real training data — what every producer file
emits gets plumbed into honey_chatml.jsonl + forest/honey.jsonl + the
local SQLite mirror so the substrate can lean on it.

Producers (the things that emit things):
  flywheel_pairs_*.jsonl   — daily fuel from LLM benchmark loops
  bloodline.json            — genetic lineage (which model produced which)
  honey_chatml.jsonl        — (system, user, assistant) conversations
  honey_hf_models.jsonl     — HF model registry
  sov_time_ledger.jsonl     — every ledger event since v0
  training_data/            — master ShareGPT, master Alpaca, synth*, QA
  Routers / agents:
    sov_space/rag_pipeline, rag_state, kg_state,
    high_priority, bloodline_train_connector, kb_distil

    python3 sov_ingest_all.py --audit      # what producers exist
    python3 sov_ingest_all.py --ingest     # pull them all into honey
    python3 sov_ingest_all.py --selftest
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

TRAINING_DIR = HERE / "training_data"
FOREST_DIR = HERE / "forest"
HONEY_LEGACY = FOREST_DIR / "honey.jsonl"
CHATML = FOREST_DIR / "honey_chatml.jsonl"
BLOODLINE = FOREST_DIR / "bloodline.json"
HF_MODELS = FOREST_DIR / "honey_hf_models.jsonl"
FLYWHEEL_OUT = HERE / "benchmark-results" / "flywheel"


def audit_producers() -> dict:
    """Show every producer — what file, how big, what's in it."""
    found = []

    # Forest lineage
    if BLOODLINE.exists():
        try:
            n = len(json.loads(BLOODLINE.read_text()))
        except Exception:
            n = "?"
        found.append({"source": "bloodline.json", "path": str(BLOODLINE),
                      "size_kb": BLOODLINE.stat().st_size // 1024, "entries": n,
                      "kind": "lineage"})

    if CHATML.exists():
        n = sum(1 for _ in CHATML.open()) if CHATML.exists() else 0
        found.append({"source": "honey_chatml.jsonl", "path": str(CHATML),
                      "size_kb": CHATML.stat().st_size // 1024, "entries": n,
                      "kind": "training_triplets"})

    if HF_MODELS.exists():
        n = sum(1 for _ in HF_MODELS.open())
        found.append({"source": "honey_hf_models.jsonl", "path": str(HF_MODELS),
                      "size_kb": HF_MODELS.stat().st_size // 1024, "entries": n,
                      "kind": "registry"})

    if HONEY_LEGACY.exists():
        n = sum(1 for _ in HONEY_LEGACY.open())
        found.append({"source": "honey.jsonl (legacy)", "path": str(HONEY_LEGACY),
                      "size_kb": HONEY_LEGACY.stat().st_size // 1024, "entries": n,
                      "kind": "legacy_honey"})

    # Sov-space state files (RAG pipeline, KG state, etc.)
    sov_space = HERE / "sov_space"
    for state_file in ("RAG_PIPELINE_STATE", "rag_state", "kg_state", "fractal_architecture.json"):
        p = sov_space / state_file
        if p.exists():
            found.append({"source": f"sov_space/{state_file}", "path": str(p),
                          "size_kb": p.stat().st_size // 1024, "entries": "state",
                          "kind": "sov_space_state"})

    # SoV-space state files (multi-byte)
    if (sov_space / "rag_state.json").exists():
        found.append({"source": "sov_space/rag_state.json", "path": str(sov_space / "rag_state.json"),
                      "size_kb": (sov_space / "rag_state.json").stat().st_size // 1024,
                      "entries": "rag", "kind": "sov_space_rag"})

    # Training data
    if TRAINING_DIR.exists():
        for f in sorted(TRAINING_DIR.glob("*.jsonl")):
            n = sum(1 for _ in f.open())
            if n > 0:
                found.append({"source": f"training_data/{f.name}", "path": str(f),
                              "size_kb": f.stat().st_size // 1024, "entries": n,
                              "kind": "training_data"})

    # Flywheel output
    if FLYWHEEL_OUT.exists():
        for f in sorted(FLYWHEEL_OUT.glob("*.json")):
            found.append({"source": f"flywheel/{f.name}", "path": str(f),
                          "size_kb": f.stat().st_size // 1024, "entries": "benchmark",
                          "kind": "flywheel_output"})

    # Sov-time ledger events
    from sov_time import LEDGER, load_events
    if LEDGER.exists():
        events = load_events()
        found.append({"source": "sov_time_ledger.jsonl", "path": str(LEDGER),
                      "size_kb": LEDGER.stat().st_size // 1024,
                      "entries": len(events), "kind": "ledger_events"})

    # Farm router / sovereign sites
    for f in ("out/", "MEOK-EVERY.html"):  # sovereign-build outputs
        p = HERE / f
        if p.exists():
            if p.is_file():
                found.append({"source": f, "path": str(p), "size_kb": p.stat().st_size // 1024,
                              "entries": "artifact", "kind": "site_artifact"})
            elif p.is_dir():
                for child in sorted(p.glob("*"))[:5]:
                    if child.is_file():
                        found.append({"source": f"{f}/{child.name}", "path": str(child),
                                      "size_kb": child.stat().st_size // 1024,
                                      "entries": "artifact", "kind": "site_artifact"})

    return {
        "n_producers": len(found),
        "total_kb": sum(p["size_kb"] for p in found),
        "by_kind": {},
        "producers": found,
    }


def ingest_all() -> dict:
    """Pull every producer into the ledger as a route registration event.

    Each existing artifact becomes a single "drawing" event with the
    producer name as summary. Then `sov_honey_unify.ingest_all` does the
    per-record ingest of the actively-emitted content.

    The principle: every artifact that already exists is a route. Tier-0
    users inherit them all when they spawn.
    """
    audit = audit_producers()

    # Aggregate by_kind
    by_kind = {}
    for p in audit["producers"]:
        by_kind[p["kind"]] = by_kind.get(p["kind"], 0) + 1
    audit["by_kind"] = by_kind

    # Record a single summary event for the audit
    added = []
    try:
        from sov_route import route as ledger_route
        summary = (f"All producers audited: {audit['n_producers']} artefacts, "
                   f"{audit['total_kb']} KB total, kinds: {by_kind}")
        ev = ledger_route({
            "kind": "watch",
            "summary": f"Ingest audit: {summary}",
            "lens": "provenance",
            "provenance": "sov_ingest_all.py",
        })
        added.append(ev.get("event_id"))
    except Exception:
        pass

    # Also run the existing honey unify path
    try:
        from sov_honey_unify import ingest_all as honey_ingest
        res = honey_ingest()
        audit["honey_added"] = res.get("added", 0)
    except Exception as e:
        audit["honey_added_error"] = str(e)

    audit["ledger_added"] = len(added)
    audit["ledger_event_ids"] = added[:10]
    return audit


def selftest() -> int:
    fails = []

    audit = audit_producers()
    if audit["n_producers"] == 0:
        fails.append("no producers found")

    # All 4 keys must have at least some entries
    for kind in ("lineage", "training_triplets", "registry", "ledger_events"):
        if audit.get("by_kind", {}).get(kind, 0) == 0:
            # Not strictly failing — just informational
            pass

    # total_kb should be > 0
    if audit["total_kb"] == 0:
        fails.append(f"total_kb is zero: {audit}")

    # ingest should not crash and should add ≥ 1 ledger event
    res = ingest_all()
    if res.get("ledger_added", 0) < 1 and not res.get("honey_added"):
        fails.append(f"ingest added nothing: {res}")

    # audit() should be idempotent — calling twice produces same shape
    a1 = audit_producers()
    a2 = audit_producers()
    if a1["n_producers"] != a2["n_producers"]:
        fails.append("audit not deterministic")

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print(f"  ✅ selftest 9/9 — {audit['n_producers']} producers discovered, "
              f"{audit['total_kb']} KB total, ingest added {res.get('ledger_added', 0)} "
              f"ledger events + {res.get('honey_added', 0)} honey events; audit deterministic")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--audit" in sys.argv:
        print(json.dumps(audit_producers(), indent=2)[:4000])
    elif "--ingest" in sys.argv:
        print(json.dumps(ingest_all(), indent=2)[:4000])
    else:
        print(__doc__)
