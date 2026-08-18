#!/usr/bin/env python3
"""
GSPC PER-AXIS ITEM TRACKER — 16 axes × item count vs quotable threshold.

Shows every axis, how many items it has, whether it's quotable (n>=30),
and what the next action is (measure / grow items / publish).

Usage: python3 gspc_axis_tracker.py [--json]
Reads: live /api/gspc + on-disk item banks (items-full/) for the item counts.
"""
from __future__ import annotations
import json, os, sys, urllib.request
from pathlib import Path

ESTATE = Path(os.environ.get("GSPC_ESTATE", str(Path.home() / "clawd/kimi-regen/arena-build")))
QUOTABLE_N = 30

# 17 axes in the board (13 measured + jail quotable + 3 gated: slot15, human-vs-ai, human-baseline).
# PUBLIC-COUNT RULING (GSPC roadmap 2026-08-18): quotable = 13 core + jail = 14.
# Gated axes (slot15, human-vs-ai, human-baseline) are LANE-MEASURED/DESIGNED and NOT
# counted in the public quotable total until SITTING 1 moves the ladder.
AXES = [
    "governance", "safety", "provenance", "continuity", "conformance", "openness",
    "machinery-conformity", "care", "cross-reality", "detector-interop",
    "art5-safeguard", "swarm", "affect", "jail", "slot15", "human-vs-ai",
    "human-baseline",
]
GATED = {"slot15", "human-vs-ai", "human-baseline"}


def fetch_living() -> dict:
    """The living DB (all merged sources incl. jail)."""
    try:
        p = Path.home() / "clawd/csoai-static-deploy2/SOVOS/living/board_living.json"
        return json.loads(p.read_text())
    except Exception:
        return {"axes": []}

def fetch_api() -> dict:
    try:
        req = urllib.request.Request("https://councilof.ai/api/gspc",
                                     headers={"User-Agent": "gspc-tracker/1.0", "Accept": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=15).read())
    except Exception as e:
        return {"error": str(e), "axes": []}

def local_items(axis: str) -> int:
    """Count items in the local bank (the real scarce-resource measure)."""
    n = 0
    candidates = [
        ESTATE / "items-full" / f"{axis}.jsonl",
        ESTATE / f"{axis}.jsonl",
        Path.home() / "clawd/csoai-static-deploy2/forest" / f"{axis}.jsonl",
    ]
    for f in candidates:
        if not f.exists():
            continue
        try:
            for line in f.read_text(errors="ignore").splitlines():
                if line.strip():
                    try:
                        d = json.loads(line)
                        if isinstance(d, dict) and d.get("axis", axis) == axis:
                            n += 1
                    except Exception:
                        pass
        except Exception:
            pass
    return n

def main() -> int:
    as_json = "--json" in sys.argv
    api = fetch_api()
    living = fetch_living()
    # living DB wins per-axis (it has jail + real boards merged)
    api_axes = {a.get("axis"): a for a in (living.get("axes") or api.get("axes", []))}
    rows = []
    for ax in AXES:
        api_a = api_axes.get(ax, {})
        n_api = api_a.get("n", 0)
        items_local = local_items(ax)
        # For gated axes the board's n is authoritative (bank paths are stale);
        # for public axes take the max (local banks are the scarce resource).
        n = n_api if ax in GATED else max(n_api, items_local)
        status = api_a.get("status", "UNMEASURED")
        # PUBLIC-COUNT RULING: gated axes are never public-quotable until SITTING 1
        if ax in GATED:
            quotable = False
            action = f"GATED (owner — {status})"
        elif ax == "jail":
            # jail = the 14th public-quotable axis (C-extension, containment)
            quotable = n >= QUOTABLE_N and status in ("MEASURED", "QUOTABLE")
            action = "PUBLISH" if quotable else "MEASURE"
        else:
            quotable = n >= QUOTABLE_N and status == "MEASURED"
            action = ("PUBLISH" if quotable else
                      "MEASURE" if n >= QUOTABLE_N else
                      f"GROW ITEMS (need {QUOTABLE_N - n} more)")
        rows.append({
            "axis": ax, "n": n, "n_api": n_api, "n_local": items_local,
            "status": status, "quotable": quotable, "action": action,
        })
    if as_json:
        print(json.dumps({"quotable_n": QUOTABLE_N, "rows": rows}, indent=1))
        return 0
    print(f"GSPC ITEM TRACKER — quotable at n>={QUOTABLE_N}")
    print(f"{'axis':<20} {'n':>5} {'status':<11} {'quotable':<9} action")
    print("-" * 70)
    for r in rows:
        print(f"{r['axis']:<20} {r['n']:>5} {r['status']:<11} {str(r['quotable']):<9} {r['action']}")
    q = sum(1 for r in rows if r["quotable"])
    gated_n = sum(1 for r in rows if r["axis"] in GATED)
    print(f"\nQuotable: {q}/14 public axes (13 core + jail; {gated_n} gated not counted — GSPC ruling 2026-08-18)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
