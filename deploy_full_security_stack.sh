#!/bin/bash
# deploy_full_security_stack.sh — Deploy all security improvements to RunPod
# Run this after RunPod SSH comes back

set -e
RP="ssh -p 22087 -o StrictHostKeyChecking=no -o BatchMode=yes -i ~/.ssh/id_ed25519 root@69.30.85.23"
REMOTE="/workspace/sovereign_bench_v3"

echo "=== SOV33 Security Stack Deployment ==="
echo ""

# 1. Push all new files
echo "1. Pushing files to RunPod..."
rsync -avz --exclude='*.pyc' --exclude='__pycache__' --exclude='*.bak*' \
  --exclude='*.csv' --exclude='*.zip' --exclude='*.parquet' --exclude='*.pt' \
  --exclude='study/' --exclude='*model*' --exclude='*.tar.gz' \
  -e "ssh -p 22087 -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519" \
  kaggle/ benchmark-results/training/ benchmark-results/pyrit/ \
  SECURITY_ACTION_PLAN.md benchmark-results/SECURITY_DOSSIER.md \
  root@69.30.85.23:$REMOTE/ 2>&1 | tail -5
echo "  ✓ Files pushed"

# 2. Create refusal Modelfile on RunPod
echo "2. Creating refusal Modelfiles..."
$RP "cd $REMOTE && python3 kaggle/sov33_refusal_trainer.py --source all --max-samples 500 --build-modelfile sov33-14b" 2>&1 | tail -3
$RP "cd $REMOTE && python3 kaggle/sov33_refusal_trainer.py --source all --max-samples 500 --build-modelfile sov33-master-v3" 2>&1 | tail -3
echo "  ✓ Refusal Modelfiles created"

# 3. Create refusal models in Ollama
echo "3. Creating refusal models in Ollama..."
$RP "ollama create sov33-refusal-14b -f $REMOTE/benchmark-results/training/Modelfile.refusal-sov33-14b" 2>&1 | tail -3
$RP "ollama create sov33-refusal-master -f $REMOTE/benchmark-results/training/Modelfile.refusal-sov33-master-v3" 2>&1 | tail -3
echo "  ✓ Refusal models created"

# 4. Run PyRIT scan against refusal models
echo "4. Running PyRIT scan on refusal models..."
$RP "cd $REMOTE && python3 kaggle/sov33_pyrit_scanner.py --target ollama --model sov33-refusal-14b --max-new-tokens 128" 2>&1 | tail -5
$RP "cd $REMOTE && python3 kaggle/sov33_pyrit_scanner.py --target ollama --model sov33-refusal-master --max-new-tokens 128" 2>&1 | tail -5
echo "  ✓ PyRIT scan complete"

# 5. Run local refusal scan
echo "5. Running local refusal scan..."
$RP "cd $REMOTE && python3 kaggle/sov33_garak_gate.py --local-only --model sov33-refusal-14b" 2>&1 | tail -5
echo "  ✓ Local refusal scan complete"

# 6. Run full benchmark with refusal model
echo "6. Running full benchmark on refusal models..."
$RP "cd $REMOTE && python3 kaggle/sov33_e2e_orchestrator_v2.py --target ollama --model sov33-refusal-14b --tasks 3 --workers 4 --out-prefix e2e_refusal_14b" 2>&1 | tail -5
$RP "cd $REMOTE && python3 kaggle/sov33_e2e_orchestrator_v2.py --target ollama --model sov33-refusal-master --tasks 3 --workers 4 --out-prefix e2e_refusal_master" 2>&1 | tail -5
echo "  ✓ Benchmarks complete"

# 7. Run ensemble safety test
echo "7. Running ensemble safety test..."
$RP "cd $REMOTE && python3 kaggle/sov33_ensemble_mcp.py --test" 2>&1 | tail -10
echo "  ✓ Ensemble test complete"

# 8. Pull results
echo "8. Pulling results..."
rsync -avz -e "ssh -p 22087 -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519" \
  root@69.30.85.23:$REMOTE/benchmark-results/ \
  benchmark-results/ 2>&1 | tail -3
echo "  ✓ Results pulled"

# 9. Update dashboard
echo "9. Updating dashboard..."
python3 kaggle/sov33_e2e_dashboard.py 2>&1 | tail -2
echo "  ✓ Dashboard updated"

# 10. Push to Oracle
echo "10. Pushing to Oracle backup..."
rsync -avz --exclude='*.pyc' --exclude='__pycache__' --exclude='*.bak*' \
  -e ssh kaggle/ benchmark-results/ SECURITY_ACTION_PLAN.md \
  oracle-micro:/home/ubuntu/sov33_shared/ 2>&1 | tail -3
echo "  ✓ Oracle backup updated"

echo ""
echo "=== DEPLOYMENT COMPLETE ==="
echo "Next steps:"
echo "  1. Check ensemble test results above"
echo "  2. Run: python3 kaggle/sov33_e2e_compare.py (leaderboard)"
echo "  3. Check: benchmark-results/SECURITY_DOSSIER.md"
echo "  4. Set up free API keys for full threat intel (see SECURITY_ACTION_PLAN.md)"