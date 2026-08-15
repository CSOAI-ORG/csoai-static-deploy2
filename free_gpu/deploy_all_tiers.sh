#!/bin/bash
# deploy_all_tiers.sh — Deploy SOV work to all free GPU tiers
set -euo pipefail
cd /Users/nicholas/clawd/csoai-static-deploy2

echo "=== FREE-GPU SWARM DEPLOYMENT ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Tier 0: Local M4 (always free)
echo "[Tier 0] Local M4 — running E2E checks..."
python3 tools/verify_e2e_batch.py 2>&1 | tail -5
echo ""

# Tier 1: Kaggle T4 (free, 30h/week)
echo "[Tier 1] Kaggle T4 — deploying capability matrix..."
python3 free_gpu/kaggle_capability_deploy.py 2>&1 | tail -10
echo ""

# Tier 2: RunPod (paid, use sparingly)
echo "[Tier 2] RunPod — checking pod status..."
python3 -c '
import urllib.request, json
from pathlib import Path
key = Path("/Users/nicholas/.runpod/api_key").read_text().strip()
h = {"Authorization": f"Bearer {key}"}
req = urllib.request.Request("https://rest.runpod.io/v1/pods?includeMachine=true", headers=h)
d = json.load(urllib.request.urlopen(req, timeout=30))
running = [p for p in d if p.get("desiredStatus") == "RUNNING"]
exited = [p for p in d if p.get("desiredStatus") == "EXITED"]
print(f"  Running: {len(running)}, Exited: {len(exited)}")
for p in running:
    gpu = (p.get("gpu") or {}).get("displayName") or "?"
    cost = p.get("adjustedCostPerHr", p.get("costPerHr", 0))
    print(f"    {p[\"name\"]}: {gpu} ${cost}/hr")
'
echo ""

# Cost report
echo "=== COST REPORT ==="
python3 free_gpu/orchestrator.py costs 2>&1
echo ""

echo "=== DEPLOYMENT COMPLETE ==="
