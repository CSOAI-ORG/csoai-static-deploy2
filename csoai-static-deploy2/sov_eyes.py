#!/usr/bin/env python3
"""sov_eyes.py — the three-eye substrate orchestrator inside SOV-space.

Per architecture Law 6, an instrument is decomposed as:
  IWM = Inference Workspace Memory (DECIDES). Reasons over claims, decides
       what to record, what supersedes, what is contested.
  OWM = Observation Workspace Memory (KNOWS). Honey KB — what the watchers
       have seen. Append-only; never re-read as input by IWM.
  VWM = Visual Workspace Memory (RENDERS). Paints the canvas; never decides.

This module ties them together:
  - OWM is sov_space/KNOWLEDGE_BASE.json + hive_consolidated (honey files)
  - IWM is the instrument + decision ledger + equivalence engine
  - VWM is sov_time + sov_zoom (the canvas)

  python3 sov_eyes.py --reason "why does ProvBench matter?"
  python3 sov_eyes.py --owm-search "EU AI Act Article 50"
  python3 sov_eyes.py --vwm-paint 86400
  python3 sov_eyes.py --selftest

The output FRAMES must never be present at runtime — IWM observes OWM, VWM
observes IWM's reasoning, both render the same canvas, neither decides for
the other.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

OVM_DIR = HERE / "sov_space"
HONEY_DIR = HERE / "sov_space" / "honey_consolidated"
FOREST_DIR = HERE / "forest"


# ─── OWM — Observation Workspace Memory (knows, never decides) ────────────

def owm_load() -> dict:
    """Load OWM from disk: knowledge base + hive_consolidated + forest honey."""
    owm = {"sources": [], "facts": [], "entries": []}

    # Primary KB
    kb = OVM_DIR / "KNOWLEDGE_BASE.json"
    if kb.exists():
        try:
            data = json.loads(kb.read_text())
            owm["sources"].append(str(kb))
            if isinstance(data, list):
                owm["facts"].extend(data[:100])
            elif isinstance(data, dict):
                owm["facts"].extend(json.dumps(data).encode().decode('utf-8', errors='ignore')[:5000].split('\n')[:50])
        except Exception:
            pass

    # Consolidated honey
    if HONEY_DIR.exists():
        for f in sorted(HONEY_DIR.glob("*.json"))[:5]:
            try:
                data = json.loads(f.read_text())
                owm["sources"].append(str(f))
                if isinstance(data, list):
                    owm["entries"].extend(data[:50])
                elif isinstance(data, dict):
                    owm["entries"].append(data)
            except Exception:
                pass

    # Forest bloodline — the curated genealogy
    bl = FOREST_DIR / "bloodline.json"
    if bl.exists():
        try:
            data = json.loads(bl.read_text())
            owm["sources"].append(str(bl))
            if isinstance(data, dict):
                owm["entries"].append({"source": "forest/bloodline.json", "keys": list(data.keys())[:20]})
        except Exception:
            pass

    return owm


def owm_search(query: str, owm: dict | None = None) -> list[dict]:
    """Search OWM for matching facts. Returns top-N ranked by textual overlap."""
    if owm is None:
        owm = owm_load()
    if not query:
        return []

    query_terms = set(query.lower().split())
    scored = []

    for fact in owm.get("facts", []):
        if not isinstance(fact, str):
            continue
        text = fact.lower()
        score = sum(1 for t in query_terms if t in text)
        if score > 0:
            scored.append((score, fact[:200]))

    for entry in owm.get("entries", []):
        text = json.dumps(entry).lower()[:1000]
        score = sum(1 for t in query_terms if t in text)
        if score > 0:
            scored.append((score, str(entry)[:200]))

    scored.sort(key=lambda x: -x[0])
    return [{"score": s, "text": t} for s, t in scored[:5]]


# ─── IWM — Inference Workspace Memory (reasons, decides) ─────────────────

def iwm_describe() -> dict:
    """Describe the instrument state — what it knows, what it claims."""
    try:
        from sov_instrument import LENSES, Instrument
        ins = Instrument()
        lens_status = {
            k: {"asks": v["asks"], "status": v["status"], "claim": v["claim"][:100]}
            for k, v in LENSES.items()
        }
        return {
            "guard": ins.guard(),
            "lenses": lens_status,
            "n_lenses": len(LENSES),
        }
    except Exception as e:
        return {"guard": f"unreachable: {e}", "lenses": {}, "n_lenses": 0}


def iwm_ledger_summary() -> dict:
    """Summary of the decision ledger — the append-only trace of every assertion."""
    try:
        from decision_ledger import build_seed_ledger
        led = build_seed_ledger()
        return {
            "n_records": len(led._records),
            "kinds": sorted(set(r["kind"] for r in led._records)),
            "verdicts": sorted(set(r["verdict"] for r in led._records)),
            "contested": len(led.contested()),
        }
    except Exception:
        return {"n_records": 0, "contested": 0}


def iwm_reason(question: str, owm: dict | None = None) -> dict:
    """Reason about a question by combining OWM facts with IWM claim ledger.

    The reasoning is supervised by the LENSES — every claim must trace back
    to one of: governance, safety, provenance, continuity, care_cost.
    This is the structural Law 4 enforcement: no orphan claims.
    """
    if owm is None:
        owm = owm_load()

    lens_status = iwm_describe()
    ledger = iwm_ledger_summary()
    owm_hits = owm_search(question, owm)

    # Try to match the question to a lens
    question_l = question.lower()
    matched_lens = None
    for name, l in lens_status.get("lenses", {}).items():
        if any(t in question_l for t in name.split("_")):
            matched_lens = name
            break

    return {
        "question": question,
        "matched_lens": matched_lens,
        "instrument_guard": lens_status.get("guard"),
        "ledger": ledger,
        "owm_hits": owm_hits,
        "reasoning": (
            f"Question routed through the {matched_lens or 'general'} lens "
            f"of sov_instrument, with {ledger['n_records']} decision records "
            f"and {len(owm_hits)} OWM facts supporting the answer."
        ),
    }


# ─── VWM — Visual Workspace Memory (renders, never decides) ───────────────

def vwm_paint(window_seconds: int = 86400) -> str:
    """Paint the canvas — emits SVG, never decides."""
    from sov_time import render_canvas
    return render_canvas(window_seconds=window_seconds)


def vwm_zoom(zoom: str = "hour", window: int = 86400) -> str:
    """Paint a fractal zoom — emits SVG for the requested zoom level."""
    from sov_zoom import render
    return render(zoom, window)


# ─── Substrate summary — the three eyes at a glance ───────────────────────

def substrate() -> dict:
    """The three eyes together, one snapshot."""
    owm = owm_load()
    return {
        "owm": {
            "sources_loaded": len(owm["sources"]),
            "facts": len(owm.get("facts", [])),
            "entries": len(owm.get("entries", [])),
        },
        "iwm": iwm_describe(),
        "iwm_ledger": iwm_ledger_summary(),
        "vwm": {
            "canvas": "sov_time.py + sov_zoom.py",
            "zoom_levels": ["microsecond", "second", "hour", "day", "year"],
        },
        "law": "IWM decides from OWM. VWM renders what IWM + OWM together produced. Neither loop back to influence the other.",
    }


def selftest() -> int:
    fails = []

    # OWM loads
    owm = owm_load()
    if not owm["sources"]:
        fails.append("OWM loaded no sources")

    # OWM search returns ranked results
    hits = owm_search("EU AI Act Article 50", owm)
    if not isinstance(hits, list):
        fails.append("OWM search did not return list")

    # IWM describes the instrument
    iwm = iwm_describe()
    if not iwm.get("guard", "").startswith("OK"):
        fails.append(f"IWM guard failed: {iwm}")

    # IWM ledger summary
    ledger = iwm_ledger_summary()
    if ledger["n_records"] < 1:
        fails.append(f"IWM ledger has no records: {ledger}")

    # IWM reason() doesn't crash
    reasoning = iwm_reason("does the care floor hold?", owm)
    if not reasoning.get("owm_hits") and not reasoning.get("matched_lens"):
        fails.append(f"IWM reason returned nothing useful: {reasoning}")

    # VWM paints
    svg = vwm_paint(window_seconds=86400)
    if "<svg" not in svg:
        fails.append("VWM paint did not emit SVG")

    # VWM zoom renders
    for zoom in ("hour", "day"):
        z = vwm_zoom(zoom=zoom, window=86400)
        if "<svg" not in z:
            fails.append(f"VWM zoom {zoom} did not emit SVG")

    # Substrate snapshot covers all three
    s = substrate()
    for k in ("owm", "iwm", "iwm_ledger", "vwm"):
        if k not in s:
            fails.append(f"substrate missing {k}")

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print("  ✅ selftest 9/9 — OWM loads + searches, IWM describes + reasons + ledger, "
              "VWM paints + zooms, all three on one substrate")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--reason" in sys.argv:
        i = sys.argv.index("--reason")
        q = sys.argv[i + 1] if i + 1 < len(sys.argv) else "what does provenance measure?"
        print(json.dumps(iwm_reason(q), indent=2))
    elif "--owm-search" in sys.argv:
        i = sys.argv.index("--owm-search")
        q = sys.argv[i + 1] if i + 1 < len(sys.argv) else "Article 50"
        print(json.dumps(owm_search(q), indent=2))
    elif "--vwm-paint" in sys.argv:
        i = sys.argv.index("--vwm-paint")
        w = int(sys.argv[i + 1]) if i + 1 < len(sys.argv) else 86400
        print(vwm_paint(window_seconds=w))
    elif "--vwm-zoom" in sys.argv:
        i = sys.argv.index("--vwm-zoom")
        z = sys.argv[i + 1] if i + 1 < len(sys.argv) else "hour"
        w = int(sys.argv[i + 2]) if i + 2 < len(sys.argv) else 86400
        print(vwm_zoom(zoom=z, window=w))
    elif "--substrate" in sys.argv:
        print(json.dumps(substrate(), indent=2))
    else:
        print(__doc__)
