#!/usr/bin/env python3
"""Measure the drum's own MAPE-K loop latency (move 88 — "days-to-hours" proof).

Times each automated stage of the RUN → TEST → AUDIT → CHECK loop and writes the result to
`feeds/loop_latency.json`. The proof: the drum's full verification loop runs in seconds, not
hours/days — the loop is fast enough to iterate continuously (the "hours" are the mine/improve
human+AI judgment, which this instrument bounds and reports).

Run: python3 ops/measure_latency.py
"""
import json
import os
import subprocess
import sys
import time

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(PACK, "feeds", "loop_latency.json")

STAGES = [
    ("build (check+lint)", "python3 build_catalog.py --check --lint"),
    ("unit tests", "python3 tests/test_drum.py"),
    ("e2e", "python3 tests/e2e_drum.py"),
    ("property tests", "python3 tests/e2e_properties.py"),
    ("mcp selftest", "python3 mcp/frameworks_drum_server.py --selftest"),
    ("align audit", "python3 ops/align_audit.py"),
]


def main():
    stages = []
    for name, cmd in STAGES:
        t0 = time.time()
        r = subprocess.run(cmd, shell=True, cwd=PACK, capture_output=True, text=True, timeout=120)
        dt = round(time.time() - t0, 3)
        stages.append({"stage": name, "seconds": dt, "pass": r.returncode == 0})
        print(f"  {name:28s} {dt:6.2f}s  {'PASS' if r.returncode == 0 else 'FAIL'}")

    total = round(sum(s["seconds"] for s in stages), 3)
    out = {
        "generated": time.strftime("%Y-%m-%d"),
        "loop": "RUN → TEST → AUDIT → CHECK",
        "total_seconds": total,
        "verdict": f"automated loop completes in {total:.1f}s — minutes-not-days (the mine/improve judgment is the human+AI leg, unbounded here)",
        "stages": stages,
        "note": "the property suite (10k purity trials + fuzz + concurrency) is the dominant stage; all stages stdlib, no GPU/fleet dependency",
    }
    os.makedirs(os.path.dirname(FEED), exist_ok=True)
    with open(FEED, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(f"loop total: {total:.1f}s → {FEED}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
