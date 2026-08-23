#!/usr/bin/env python3
"""Repair a sov_kb.json that has been corrupted by concatenation of two
top-level JSON objects (json.loads -> 'Extra data' error).

Strategy:
  - Back up the original to sov_kb.json.corrupt-<ts>.bak
  - Stream-decode all top-level JSON values with json.JSONDecoder.raw_decode
  - If all are dicts: deep-merge (later overrides earlier) -> one dict
  - If all are lists: concatenate
  - Mixed / single: keep the LAST complete object (most likely the freshest full KB)
  - Write a single valid JSON file back.
"""
import json, sys, shutil, datetime, pathlib

KB = pathlib.Path("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/sov_kb.json")
assert KB.exists(), f"KB not found: {KB}"

data = KB.read_text(encoding="utf-8", errors="replace")
dec = json.JSONDecoder()
objects = []
idx = 0
n = len(data)
while idx < n:
    # skip whitespace
    while idx < n and data[idx] in " \t\r\n":
        idx += 1
    if idx >= n:
        break
    try:
        obj, end = dec.raw_decode(data, idx)
    except json.JSONDecodeError as e:
        print(f"WARN: decode stalled at {idx}: {e}", file=sys.stderr)
        break
    objects.append(obj)
    idx = end

print(f"decoded {len(objects)} top-level JSON object(s)")

# backup
ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
bak = KB.with_suffix(f".json.corrupt-{ts}.bak")
shutil.copy2(KB, bak)
print(f"backup -> {bak}")

types = {type(o).__name__ for o in objects}
print(f"object types: {types}")

if len(objects) == 1:
    merged = objects[0]
elif types == {"dict"}:
    merged = {}
    for o in objects:
        merged.update(o)
    print(f"deep-merged {len(objects)} dicts into one (keys now {len(merged)})")
elif types == {"list"}:
    merged = []
    for o in objects:
        merged.extend(o)
    print(f"concatenated {len(objects)} lists -> {len(merged)} items")
else:
    # mixed or unknown: keep the last complete, largest object
    merged = max(objects, key=lambda o: (isinstance(o, (dict, list)), len(o) if isinstance(o, (dict, list)) else 0))
    print(f"mixed types -> kept last/largest object of type {type(merged).__name__}")

KB.write_text(json.dumps(merged, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"WROTE repaired KB -> {KB} ({KB.stat().st_size} bytes)")
# self-check
json.loads(KB.read_text())
print("SELF-CHECK: json.loads OK")
