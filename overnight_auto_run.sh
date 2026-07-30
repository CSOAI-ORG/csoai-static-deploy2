#!/bin/bash
# overnight_auto_run.sh — Full sovereign AI overnight alignment
# Orchestrates OWEM cluster across all free GPU tiers + local pipeline
set -euo pipefail
BASE="/Users/nicholas/clawd/csoai-static-deploy2"
cd "$BASE"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  SOV33 OVERNIGHT OWEM CLUSTER AUTO-ALIGNMENT               ║"
echo "║  $(date -u +%Y-%m-%dT%H:%M:%SZ)                                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Phase 0: Sovereign API health check (cron-like)
echo "[Phase 0a] Sovereign API health check..."
bash "$BASE/sovereign_cron.sh" 2>&1 | tail -5
echo ""

# Phase 0b: OWEM Cluster Manager — Orchestrate all free GPU workers
echo "[Phase 0b] OWEM Cluster Manager — deploying to all free tiers..."
python3 free_gpu/owem_cluster_manager.py deploy all
python3 free_gpu/owem_cluster_manager.py checkpoint save
echo ""

# Phase 1: Unified free pipeline (local Ollama — continuous improvement)
echo "[Phase 1] Local ASI evolution pipeline (qwen2.5:0.5b)..."
nohup python3 unified_free_pipeline.py > unified_overnight_output.log 2>&1 &
UNIFIED_PID=$!
echo "  PID: $UNIFIED_PID  (tail -f unified_overnight_output.log)"
echo ""

# Phase 2: Generate all free-tier artifacts
echo "[Phase 2] Generating all free-tier artifacts..."
python3 free_gpu/setup_colab.py 2>&1 | tail -1
python3 free_gpu/setup_lightning.py 2>&1 | tail -1
python3 free_gpu/setup_hf_spaces.py 2>&1 | tail -1
python3 free_gpu/setup_gradient.py 2>&1 | tail -1
python3 free_gpu/setup_all_tiers.py 2>&1 | grep -E "(✓|✗|#|Cost)"
echo ""

# Phase 3: Consolidate and checkpoint
echo "[Phase 3] Consolidating results + 3-way checkpoint..."
python3 consolidate_and_deploy.py --check-only 2>&1 | tail -10 || true
python3 free_gpu/owem_cluster_manager.py checkpoint save 2>&1 | tail -3
echo ""

# Phase 4: 3-way backup (Local + GitHub + HF)
echo "[Phase 4] 3-way backup..."
# Local
mkdir -p sov-backup/checkpoints
cp -r forest/honey.jsonl sov-backup/ 2>/dev/null || true
cp -r forest/bloodline.json sov-backup/ 2>/dev/null || true
cp -r benchmark-results/unified_overnight/ sov-backup/checkpoints/ 2>/dev/null || true
cp unified_overnight_output.log sov-backup/ 2>/dev/null || true
echo "  ✓ Local backup complete"

# GitHub
git add -A 2>/dev/null || true
git commit -m "owem cluster sync $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null || true
git push origin main 2>&1 | tail -1
echo "  ✓ GitHub backup complete"

# HF (if huggingface-cli available)
if command -v huggingface-cli &>/dev/null; then
  echo "  ⏳ HF backup skipped (manual: huggingface-cli upload)"
else
  echo "  ○ HF backup requires huggingface-cli login"
fi
echo ""

# Phase 5: Status report
echo "[Phase 5] OWEM Cluster Status..."
python3 free_gpu/owem_cluster_manager.py status 2>&1 | grep -E "(Workers:|○|Workloads:|Checkpoints:|Total cost:)"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  OWEM CLUSTER RUNNING                                       ║"
echo "║  Local pipeline PID: $UNIFIED_PID                                    ║"
echo "║                                                              ║"
echo "║  MONITOR:     tail -f unified_overnight_output.log           ║"
echo "║  CLUSTER:     python3 free_gpu/owem_cluster_manager.py status║"
echo "║  COLAB:       free_gpu/sov33_colab_training.ipynb            ║"
echo "║  LIGHTNING:   free_gpu/lightning_studio.yaml                 ║"
echo "║  HF SPACE:    free_gpu/hf_space/                             ║"
echo "║  GRADIENT:    free_gpu/gradient_sov33.ipynb                  ║"
echo "║  CHECKPOINTS: sov-backup/checkpoints/                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Wait for local pipeline
wait $UNIFIED_PID 2>/dev/null || true

# Phase 6: Final sync
echo "[Phase 6] Final checkpoint + push..."
python3 free_gpu/owem_cluster_manager.py checkpoint save 2>&1 | tail -3
git add -A 2>/dev/null || true
git commit -m "owem cluster complete $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null || true
git push origin main 2>&1 | tail -1
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  OVERNIGHT OWEM CLUSTER COMPLETE                            ║"
echo "║  Checkpoints: sov-backup/checkpoints/                       ║"
echo "║  Results:     benchmark-results/unified_overnight/           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
