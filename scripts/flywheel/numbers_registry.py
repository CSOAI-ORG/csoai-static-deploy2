#!/usr/bin/env python3
"""
NUMBERS REGISTRY v0 — every public number in one file (E2E Stage 0.3).

Resolves the conflicts: care 200-vs-201, affect 13/10/11, gov 237-vs-238,
bank per_item_count vs published n. One file = the source of truth for what
we quote publicly. Every entry: number, source, date, status (QUOTABLE/
DISCREPANCY/RESOLVED), and the resolution note.

Usage: python3 numbers_registry.py    # build + print the registry
"""
from __future__ import annotations
import json, os, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "numbers_registry.json"
BOARDS = Path.home() / "clawd/kimi-regen/SOVOS/boards-v2-2026-08-12"

def live_api() -> dict:
    try:
        req = urllib.request.Request("https://councilof.ai/api/gspc",
                                     headers={"User-Agent": "numbers-reg/1.0", "Accept": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=15).read())
    except Exception:
        return {"axes": []}

def bank_count(axis: str) -> dict:
    """board_<axis>.json: {published: bank_items, pipeline: per_item_count}."""
    f = BOARDS / f"board_{axis}.json"
    if f.exists():
        try:
            d = json.loads(f.read_text())
            return {"published": d.get("bank_items"), "pipeline": d.get("per_item_count")}
        except Exception:
            return {"published": None, "pipeline": None}
    return {"published": None, "pipeline": None}

def main() -> int:
    api = live_api()
    api_axes = {a["axis"]: a for a in api.get("axes", [])}
    registry = {"schema": "csoai.numbers-registry/0.1", "updated": None, "numbers": []}
    for ax in ("governance", "safety", "provenance", "continuity", "conformance",
               "openness", "machinery-conformity", "care", "cross-reality",
               "detector-interop", "art5-safeguard", "swarm", "affect", "jail"):
        api_n = api_axes.get(ax, {}).get("n")
        bank = bank_count(ax)
        bank_pub = bank.get("published")
        bank_pipe = bank.get("pipeline")
        # resolve: API n is the published/quotable number; bank_items should match it
        if api_n is None and bank_pub is None:
            status = "NO_DATA"
        elif api_n == bank_pub:
            status = "CLEAN"
        elif api_n is not None and bank_pub is not None and api_n != bank_pub:
            status = "DISCREPANCY"
        elif api_n is None and bank_pub is not None:
            status = "BANK_ONLY"
        else:
            status = "API_ONLY"
        registry["numbers"].append({
            "axis": ax,
            "published_n": api_n,
            "bank_published": bank_pub,
            "bank_pipeline": bank_pipe,
            "status": status,
            "quote": f"n={api_n}" if api_n else None,
            "note": ("bank_items != API n — quote the API n; bank is the full set"
                     if status == "DISCREPANCY" else ""),
        })
    registry["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.write_text(json.dumps(registry, indent=1))
    print(f"NUMBERS REGISTRY ({registry['updated']})")
    print(f"{'axis':<20} {'published':>9} {'bank':>6}  status")
    for n in registry["numbers"]:
        print(f"{n['axis']:<20} {str(n['published_n']):>9} {str(n['bank_published']):>6}  {n['status']}")
    disc = [n for n in registry["numbers"] if n["status"] == "DISCREPANCY"]
    print(f"\nDISCREPANCIES: {len(disc)} — {', '.join(d['axis'] for d in disc)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
