#!/usr/bin/env python3
"""Kaggle T4 Monitor — Polls notebook status, pulls results when done."""
import json, os, subprocess, time
from datetime import datetime
from pathlib import Path

WORK = Path("/home/ubuntu/sov-work")
RESULTS = WORK / "kaggle_results"
RESULTS.mkdir(exist_ok=True)

NOTEBOOKS = [
    "nicktempleman/sov7-reasoning-lora",
    "nicktempleman/sov-asi-evolve",
    "nicktempleman/sov-overnight-eat",
    "nicktempleman/sov-capability-matrix",
]

def check_status(nb):
    try:
        r = subprocess.run(["kaggle", "kernels", "status", nb],
                          capture_output=True, text=True, timeout=15)
        return r.stdout.strip()
    except: return "UNKNOWN"

def pull_results(nb):
    out = RESULTS / nb.split("/")[-1]
    out.mkdir(exist_ok=True)
    try:
        subprocess.run(["kaggle", "kernels", "pull", nb, "-p", str(out)],
                      capture_output=True, timeout=120)
        return True
    except: return False

print(f"Kaggle Monitor started at {datetime.now()}")
print(f"Monitoring {len(NOTEBOOKS)} notebooks")
print()

while True:
    for nb in NOTEBOOKS:
        status = check_status(nb)
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {nb}: {status}")
        
        if "COMPLETE" in status:
            print(f"  → Pulling results...")
            if pull_results(nb):
                print(f"  → Saved to {RESULTS / nb.split('/')[-1]}")
    
    print(f"\nSleeping 5 minutes...\n")
    time.sleep(300)
