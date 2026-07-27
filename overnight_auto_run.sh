#!/bin/bash
# overnight_auto_run.sh — Free overnight auto-run on Kaggle
# Runs continuously: benchmark → train → test → submit → backup
set -euo pipefail

echo "=== SOV OVERNIGHT AUTO-RUN ==="
echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Cost: \$0 (Kaggle T4 free tier)"
echo ""

# Phase 1: Deploy ASI evolve script
echo "[Phase 1] Deploying ASI evolve script..."
kaggle kernels push -p /tmp/sov-asi-evolve 2>&1 | tail -3
echo ""

# Phase 2: Deploy overnight EAT pipeline
echo "[Phase 2] Deploying overnight EAT pipeline..."
kaggle kernels push -p /tmp/sov-overnight-eat 2>&1 | tail -3
echo ""

# Phase 3: Deploy competition notebooks
echo "[Phase 3] Deploying competition notebooks..."
for comp in "sov6-llm-classification-finetuning" "sov6-red-team" "sov6-pokemon"; do
    echo "  Deploying $comp..."
    kaggle kernels push -p /tmp/$comp 2>&1 | tail -3
done
echo ""

# Phase 4: Check status
echo "[Phase 4] Checking status..."
kaggle kernels status nicktempleman/sov-asi-evolve 2>&1
kaggle kernels status nicktempleman/sov-overnight-eat 2>&1
echo ""

# Phase 5: Pull results when complete
echo "[Phase 5] Pulling results..."
mkdir -p /tmp/sov-overnight-results
kaggle kernels pull nicktempleman/sov-asi-evolve -p /tmp/sov-overnight-results 2>&1 | tail -3
echo ""

echo "=== OVERNIGHT AUTO-RUN COMPLETE ==="
echo "Results: /tmp/sov-overnight-results"
