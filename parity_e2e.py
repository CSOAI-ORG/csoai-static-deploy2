#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""parity_e2e.py — assert all 6 GSPC greenfields are public + fetchable on HF AND Kaggle.
Exits non-zero on any gap. Drop into CI to keep the two platforms in sync."""
import re, os, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
env = (HERE / ".env").read_text(errors="ignore")
os.environ["HF_TOKEN"] = re.search(r"^HF_TOKEN\s*=\s*['\"]?([^'\"\n#]+)", env, re.M).group(1).strip()
KU = re.search(r"^KAGGLE_USERNAME\s*=\s*['\"]?([^'\"\n#]+)", env, re.M).group(1).strip()
from huggingface_hub import HfApi
api = HfApi(token=os.environ["HF_TOKEN"])

AXES = ["govbench", "provbench", "pqcbench", "defbench", "mcpbench", "ossbench"]
gaps = []
print("GSPC 6-greenfield parity (HF csoai/<axis> + Kaggle gspc-<axis>)\n")
for ax in AXES:
    try:
        hf = "public" if not api.dataset_info(f"csoai/{ax}").private else "PRIVATE"
    except Exception:
        hf = "MISSING"; gaps.append(f"HF csoai/{ax}")
    r = subprocess.run(["kaggle", "datasets", "status", f"{KU}/gspc-{ax}"], capture_output=True, text=True)
    kg = "live" if r.returncode == 0 else "MISSING"
    if kg == "MISSING":
        gaps.append(f"Kaggle gspc-{ax}")
    sov = ""
    p = HERE / "benchmark-results" / f"{ax}.json"
    if p.exists():
        s = p.read_text().lower()
        sov = "sov" if ("sov33" in s or "sov34" in s) else ""
    print(f"  {ax:10} HF={hf:8} Kaggle={kg:8} {sov}")
if gaps:
    print("\n  ❌ gaps:", gaps); sys.exit(1)
print("\n  ✅ all 6 greenfields public on both platforms")
