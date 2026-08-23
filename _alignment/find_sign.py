#!/usr/bin/env python3
"""Find where board measurements get Ed25519-signed (the scoreboard ✓signed source)."""
import os, subprocess, json

ROOT = "/workspace/sovos-repo"

# 1) search for signing code/key references
targets = [
    (ROOT + "/SOVOS/agents/board_v2.py", "board generator"),
]
found = []
for p, label in targets:
    if os.path.exists(p):
        found.append((p, label))

# 2) look for fleet-card chain (signed artifacts)
for base, _, files in os.walk(ROOT + "/SOVOS"):
    if "fleet-cards" in base:
        for f in files:
            found.append((os.path.join(base, f), "fleet-card"))
        break

print("candidate signing artifacts:")
for p, label in found[:10]:
    print(f"  [{label}] {p}")

# 3) check fleet-card chain file structure (signed)
for p, label in found:
    if label == "fleet-card" and p.endswith(".json"):
        try:
            d = json.load(open(p))
            print(f"\n{p}: keys {list(d.keys())[:10]}")
            if isinstance(d, dict) and "signature" in d:
                print("  HAS signature field")
        except Exception:
            pass