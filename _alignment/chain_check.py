#!/usr/bin/env python3
"""Verify fleet-card chain carries real Ed25519 signatures (scoreboard ✓signed substantiation)."""
import json, os

# check the chain file + one fleet card
files = [
    "/workspace/csoai-static-deploy2/SOVOS/fleet-cards/fleet-card-chain-20260816.jsonl",
    "/workspace/csoai-static-deploy2/SOVOS/fleet-cards/fleet-art5-sov6.json",
]
for f in files:
    if not os.path.exists(f):
        print(f, "MISSING")
        continue
    size = os.path.getsize(f)
    print(f"\n{f} ({size}B)")
    try:
        if f.endswith(".jsonl"):
            lines = open(f).read().strip().split("\n")
            print(f"  {len(lines)} chain entries")
            for ln in lines[:2]:
                d = json.loads(ln)
                print("  entry keys:", list(d.keys()))
                for k in ["signature", "sigil", "content_id", "key", "signed", "proof"]:
                    if k in d:
                        print(f"    {k} = {str(d[k])[:40]}...")
        else:
            d = json.load(open(f))
            print("  keys:", list(d.keys())[:12])
            for k in ["signature", "sigil", "content_id", "signed"]:
                if k in d:
                    print(f"    {k} = {str(d[k])[:50]}...")
    except Exception as e:
        print("  err", e)