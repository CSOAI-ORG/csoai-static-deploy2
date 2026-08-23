#!/usr/bin/env python3
"""merge h3k cards -> living DB (sim-world measurement fuel).

Each h3k card packs n signed Q&A pairs per axis. This merges them into
SOVOS/living/sim_cards.jsonl (append, dedupe by answer-hash) and updates the
living board's sim-world record count. Run after every card emission.
"""
from __future__ import annotations
import json, hashlib, os, sys
from datetime import datetime, timezone
from pathlib import Path

CARDS_DIR = Path.home() / "sim-world-data/cards"
LIVING = Path.home() / "clawd/csoai-static-deploy2/SOVOS/living"
OUT = LIVING / "sim_cards.jsonl"

def main() -> int:
    # existing answer-hashes
    seen = set()
    if OUT.exists():
        for line in open(OUT):
            try:
                d = json.loads(line)
                if d.get("ah"): seen.add(d["ah"])
            except Exception: pass

    added = 0; axis_count = {}
    with open(OUT, "a") as fh:
        for c in sorted(CARDS_DIR.glob("h3k-*.json")):
            try:
                card = json.loads(c.read_text())
                body = json.loads(card["body"])
                ts = body.get("t", "")
                for p in body.get("p", []):
                    r = p.get("r", {})
                    q, a = r.get("q", ""), r.get("a", "")
                    if not a: continue
                    ah = hashlib.sha256(a.encode()).hexdigest()[:16]
                    if ah in seen: continue
                    seen.add(ah)
                    rec = {"card": c.name, "ts": ts, "axis": r.get("f") or p.get("f"),
                           "q": q, "a": a, "ah": ah, "signed": bool(card.get("sig_b64"))}
                    fh.write(json.dumps(rec) + "\n")
                    added += 1
                    axis_count[rec["axis"]] = axis_count.get(rec["axis"], 0) + 1
            except Exception as e:
                print(f"skip {c.name}: {e}")
    print(f"sim cards merged: +{added} new records -> {OUT}")
    print("per axis:", dict(axis_count) or "none new")
    return 0

if __name__ == "__main__":
    sys.exit(main())
