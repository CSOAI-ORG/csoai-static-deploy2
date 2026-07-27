#!/bin/bash
# overnight_auto_run.sh — Full sovereign AI overnight alignment
# Runs: local pipeline + Kaggle deploy + Colab gen + GitHub push + deploy
set -euo pipefail
BASE="/Users/nicholas/clawd/csoai-static-deploy2"
cd "$BASE"

echo "=== SOV33 OVERNIGHT AUTO-ALIGNMENT ==="
echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Phase 1: Unified free pipeline (local Ollama)
echo "[Phase 1] Local free pipeline..."
nohup python3 unified_free_pipeline.py > unified_overnight_output.log 2>&1 &
UNIFIED_PID=$!
echo "  PID: $UNIFIED_PID (tail -f unified_overnight_output.log)"
echo ""

# Phase 2: Generate Colab notebook
echo "[Phase 2] Generating Colab notebook..."
python3 free_gpu/setup_colab.py
echo ""

# Phase 3: Consolidate results
echo "[Phase 3] Consolidating results..."
python3 consolidate_and_deploy.py --check-only 2>&1 | tail -10 || true
echo ""

# Phase 4: Push to GitHub
echo "[Phase 4] Pushing to GitHub..."
git add -A 2>/dev/null || true
git commit -m "overnight auto-sync $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null || true
git push origin main 2>&1 | tail -3
echo ""

# Phase 5: Backup to sov-backup
echo "[Phase 5] Local backup..."
cp -r forest/honey.jsonl sov-backup/ 2>/dev/null || true
cp -r forest/bloodline.json sov-backup/ 2>/dev/null || true
cp unified_overnight_output.log sov-backup/ 2>/dev/null || true
echo ""

echo "=== OVERNIGHT AUTO-ALIGNMENT RUNNING ==="
echo "  Unified pipeline: PID $UNIFIED_PID"
echo "  Monitor: tail -f unified_overnight_output.log"
echo "  Colab notebook: free_gpu/sov33_colab_training.ipynb"
echo "  Results dir: benchmark-results/unified_overnight/"
echo ""

# Wait for pipeline to complete
wait $UNIFIED_PID 2>/dev/null || true

# Phase 6: Final push with results
echo "[Phase 6] Final GitHub push..."
git add -A 2>/dev/null || true
git commit -m "overnight complete $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null || true
git push origin main 2>&1 | tail -3
echo ""

echo "=== OVERNIGHT AUTO-ALIGNMENT COMPLETE ==="
echo "Final results: benchmark-results/unified_overnight/"
