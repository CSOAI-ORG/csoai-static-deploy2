#!/usr/bin/env python3
"""Check the honest gov/care register: who actually leads per the signed boards."""
import json, glob, os

DIR = "/workspace/sovos-repo/SOVOS/boards-v2-2026-08-12"
for axis in ["gov", "care", "art5"]:
    p = os.path.join(DIR, f"board_{axis}.json")
    if not os.path.exists(p):
        print(f"{axis}: no board")
        continue
    b = json.load(open(p))
    cells = b.get("models", [])
    top = sorted([c for c in cells if c.get("quotable")],
                 key=lambda c: -float(c.get("accuracy", 0)))
    print(f"--- {axis} ---")
    print("  declared best:", b.get("best"))
    for c in top[:3]:
        print(f"  {c.get('model')}: acc={c.get('accuracy')} n={c.get('n')} signed={c.get('signed')}")