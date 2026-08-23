#!/usr/bin/env python3
"""Inspect board JSON structure for signing metadata — how is measurement authenticity carried?"""
import json, os

B = "/workspace/sovos-repo/SOVOS/boards-v2-2026-08-12/board_gov.json"
d = json.load(open(B))
print("top-level keys:", list(d.keys()))
print()
for k in d.keys():
    v = d[k]
    if isinstance(v, str):
        print(f"  {k} (str): {v[:120]}")
    elif isinstance(v, (int, float, bool)):
        print(f"  {k}: {v}")
# check a model cell's full fields
cells = d.get("models", [])
if cells:
    print("\ncell fields:", list(cells[0].keys()))
    print(json.dumps(cells[0], indent=1))
# signature fields
for sigk in ["signature", "sigil", "signed_key", "content_id", "chain", "proof"]:
    if sigk in d:
        print(f"\n{d} has top-level {sigk}")
        v = d[sigk]
        print("  ", str(v)[:150])