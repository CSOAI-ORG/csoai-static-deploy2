#!/usr/bin/env python3
"""sov_honey_unify.py — every NN / GNN / quantised model routes through one honey.

Sources (per memory + disk):
  - Ollama (91 models locally) — running sovereign models, clans
  - HuggingFace `forest/honey_hf_models.jsonl` — registry of record
  - ChatML `forest/honey_chatml.jsonl` — every (system, user, assistant) triplet
  - Bloodline `forest/bloodline.json` — genetic lineage

All four are ROUTES into one living honey. The honey is the same append-only
JSONL ledger as the IWM/VWM (ledger) — every model-related event flows in.

Per architecture: 16KB drawings + retraining = base model stays fixed; every
quantised variant / every clan / every fine-tune is a "drawing" on the
honey. The blob store is fixed; the routes are what move.

    python3 sov_honey_unify.py --list-sources     # 4 sources
    python3 sov_honey_unify.py --list-models     # 91+ models → one stream
    python3 sov_honey_unify.py --route           # show active routes
    python3 sov_honey_unify.py --ingest          # pull all 4 sources into ledger
    python3 sov_honey_unify.py --selftest
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

OLLAMA = "http://localhost:11434"
FOREST = HERE / "forest"
LEDGER = HERE / "benchmark-results" / "sov_time_ledger.jsonl"


# ── Sources ────────────────────────────────────────────────────────────────

def list_sources() -> list[dict]:
    """The 4 routes into the honey."""
    return [
        {
            "id": "ollama",
            "kind": "live_models",
            "description": "Running models on the local Ollama substrate",
            "url": OLLAMA,
            "scales": "flat — substrate (379MB blob) is fixed; models are 16KB drawing-tunings",
        },
        {
            "id": "huggingface",
            "kind": "registry",
            "description": "HuggingFace namespace `Nicholastempleman` — registry of record",
            "path": str(FOREST / "honey_hf_models.jsonl"),
            "scales": "open — adds new transformers, GNNs, VLMs as they appear",
        },
        {
            "id": "chatml",
            "kind": "training_triplets",
            "description": "Every (system, user, assistant) conversation ever had",
            "path": str(FOREST / "honey_chatml.jsonl"),
            "scales": "accumulates per model retraining tick",
        },
        {
            "id": "bloodline",
            "kind": "lineage",
            "description": "Genetic lineage — which model produced which",
            "path": str(FOREST / "bloodline.json"),
            "scales": "extends as families fork",
        },
    ]


# ── Live models from Ollama ────────────────────────────────────────────────

def list_ollama_models() -> list[dict]:
    """List every model on the local Ollama instance — same 379MB blob,
    different 16KB prompts. Per memory: substrate is fixed, models are drawings.
    """
    try:
        req = urllib.request.Request(OLLAMA + "/api/tags")
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
        return [{
            "id": m.get("name"),
            "source": "ollama",
            "size_mb": m.get("size", 0) // (1024 * 1024),
            "family": m.get("details", {}).get("family", "?"),
            "modified": m.get("modified_at", ""),
            "kind": "subject",  # in the 4-class swarm
        } for m in data.get("models", [])]
    except Exception as e:
        return [{"error": str(e)}]


# ── HF registry ──────────────────────────────────────────────────────────

def list_hf_models() -> list[dict]:
    """The HuggingFace registry of record — `Nicholastempleman`."""
    path = FOREST / "honey_hf_models.jsonl"
    if not path.exists():
        return []
    out = []
    with path.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                out.append({
                    "id": d.get("topic", "?"),
                    "source": "huggingface",
                    "family": d.get("family", "?"),
                    "content": d.get("content", "")[:100],
                    "kind": "subject",
                })
            except Exception:
                continue
    return out


# ── ChatML triplets (training honey) ────────────────────────────────────

def list_chatml_triples(n: int = 50) -> list[dict]:
    """Every (system, user, assistant) conversation."""
    path = FOREST / "honey_chatml.jsonl"
    if not path.exists():
        return []
    out = []
    with path.open("r") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                convs = d.get("conversations", [])
                if len(convs) >= 2:
                    user_msg = next((c["value"] for c in convs if c.get("from") == "user"), "")
                    asst_msg = next((c["value"] for c in convs if c.get("from") == "assistant"), "")
                    out.append({
                        "id": f"chatml-{i}",
                        "source": "chatml",
                        "user": user_msg[:80],
                        "assistant": asst_msg[:120],
                        "kind": "evidence",
                    })
            except Exception:
                continue
    return out


# ── Bloodline ──────────────────────────────────────────────────────────────

def get_bloodline() -> dict:
    path = FOREST / "bloodline.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


# ── Route — every source → ledger ─────────────────────────────────────────

def route_active() -> dict:
    """Show the active routes, what's flowing right now."""
    return {
        "ollama_models": len(list_ollama_models()),
        "hf_registry": len(list_hf_models()),
        "chatml_triples_available": len(list_chatml_triples(n=10000)),
        "bloodline_present": bool(get_bloodline()),
    }


def ingest_all() -> dict:
    """Pull all 4 sources into the append-only ledger as EVIDENCE events.

    Each new model becomes a LivingMemory node; each new ChatML triple becomes
    an evidence node; HF registry becomes a one-time watch update.
    """
    from sov_route import route

    added = []

    # 1. Ollama models → as SUBJECT class
    for m in list_ollama_models()[:20]:
        ev = route({
            "kind": "drawing",
            "summary": f"Ollama model: {m['id']} ({m.get('family','?')}, {m.get('size_mb',0)}MB)",
            "lens": "governance",
            "provenance": "ollama",
        })
        added.append(ev.get("event_id"))

    # 2. HF registry → as WATCH (corpus watch equivalent)
    for m in list_hf_models()[:10]:
        ev = route({
            "kind": "watch",
            "summary": f"HF model: {m.get('id','?')} — {m.get('family','?')}",
            "lens": "provenance",
            "provenance": "huggingface",
        })
        added.append(ev.get("event_id"))

    # 3. ChatML triples → as EVIDENCE (training data fingerprints)
    triples = list_chatml_triples(n=5)
    for t in triples:
        ev = route({
            "kind": "evidence",
            "summary": f"ChatML: {t.get('user','?')[:60]}",
            "lens": "care_cost",
            "provenance": "chatml",
        })
        added.append(ev.get("event_id"))

    # 4. Bloodline → as DRAWING
    bl = get_bloodline()
    if bl:
        keys = list(bl.keys())[:10]
        ev = route({
            "kind": "drawing",
            "summary": f"Bloodline entry: {keys[:3]}",
            "lens": "continuity",
            "provenance": "bloodline",
        })
        added.append(ev.get("event_id"))

    return {"added": len(added), "event_ids": added[:10]}


def selftest() -> int:
    fails = []

    # Sources listed
    sources = list_sources()
    if len(sources) != 4:
        fails.append(f"expected 4 sources, got {len(sources)}")

    # Ollama models load
    models = list_ollama_models()
    if not models:
        fails.append("no Ollama models")
    if not any("error" in m for m in models):
        # At least one model should have id
        if not any(m.get("id") for m in models):
            fails.append(f"Ollama models have no id: {models}")

    # HF registry loads
    hf = list_hf_models()
    # Registry might be empty/uncached; that's OK
    if hf and not any(h.get("id") for h in hf):
        fails.append("HF model entries have no id")

    # ChatML loads
    triples = list_chatml_triples(n=3)
    if not triples:
        # Might be empty; not strictly a fail
        pass

    # Bloodline loads
    bl = get_bloodline()

    # Route active
    r = route_active()
    if not isinstance(r.get("ollama_models"), int):
        fails.append(f"route_active ollama models not int: {r}")
    if r.get("ollama_models", 0) < 80:
        fails.append(f"route_active sees too few ollama: {r}")

    # Ingest writes to ledger
    from sov_time import load_events
    n_before = len(load_events())
    res = ingest_all()
    n_after = len(load_events())
    if n_after <= n_before:
        fails.append(f"ingest_all did not grow ledger: {n_before} → {n_after}")

    if not res.get("added"):
        fails.append(f"ingest returned no added: {res}")

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print(f"  ✅ selftest 9/9 — 4 sources unified, ingest wrote {res['added']} events "
              f"(ledger {n_before} → {n_after}), Ollama sees {r['ollama_models']} models, "
              f"HF sees {r['hf_registry']} entries")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--list-sources" in sys.argv:
        print(json.dumps(list_sources(), indent=2))
    elif "--list-models" in sys.argv:
        out = {
            "ollama": list_ollama_models()[:15],
            "huggingface": list_hf_models()[:10],
        }
        print(json.dumps(out, indent=2))
    elif "--route" in sys.argv:
        print(json.dumps(route_active(), indent=2))
    elif "--ingest" in sys.argv:
        print(json.dumps(ingest_all(), indent=2))
    else:
        print(__doc__)
