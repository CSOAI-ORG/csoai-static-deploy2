#!/usr/bin/env python3
"""SOVOS/deploy/a100/test_spec6.py — test that the spec6-e2e.py script
produces the same number consistently.

Run on the A100 pod AFTER install.sh:
    python3 test_spec6.py
"""
import subprocess
import sys
import re

def _run_spec6():
    """Run the absorbed spec6-e2e.py directly."""
    return subprocess.run(
        ["python3", "SOVOS/deploy/a100/spec6-e2e.py"],
        capture_output=True, text=True,
        cwd="/workspace/csoai-static-deploy2",
    )

proc = _run_spec6()
print(proc.stdout)
if proc.returncode != 0:
    print("STDERR:", proc.stderr)
    sys.exit(proc.returncode)

# Verify the spec §6 canonical number
m = re.search(r"SOV SIGNAL distance.*?([0-9]\.[0-9]+)", proc.stdout)
if not m:
    print("FAIL: no SOV SIGNAL distance printed")
    sys.exit(1)
d = float(m.group(1))
if abs(d - 4.2053) > 0.01:
    print(f"FAIL: distance {d} != canonical 4.2053 (drift beyond 0.01)")
    sys.exit(1)
print(f"=== ABSORB PASS: distance={d} matches canonical ===")
