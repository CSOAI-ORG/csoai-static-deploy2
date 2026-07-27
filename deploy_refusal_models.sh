#!/bin/bash
# deploy_refusal_models.sh — Deploy all refusal-baked SOV models to RunPod Ollama
# Run after RunPod SSH comes back

set -e
RP="ssh -p 22087 -o StrictHostKeyChecking=no -o BatchMode=yes -i ~/.ssh/id_ed25519 root@69.30.85.23"
REMOTE="/workspace/sovereign_bench_v3"

echo "=== SOV33 Refusal Model Deployment ==="
echo ""

# 1. Push refusal Modelfiles
echo "1. Pushing refusal Modelfiles..."
rsync -avz -e "ssh -p 22087 -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519" \
  benchmark-results/training/Modelfile.*-refusal \
  root@69.30.85.23:$REMOTE/benchmark-results/training/ 2>&1 | tail -3
echo "  ✓ Modelfiles pushed"

# 2. Deploy each Modelfile to Ollama
echo "2. Deploying refusal models to Ollama..."
for mf in $REMOTE/benchmark-results/training/Modelfile.*-refusal; do
    name=$(basename "$mf" | sed 's/Modelfile\.//' | sed 's/-refusal$/-refusal/')
    echo "  Creating: $name"
    $RP "ollama create $name -f $mf" 2>&1 | tail -1
done
echo "  ✓ All refusal models deployed"

# 3. List deployed models
echo "3. Verifying deployment..."
$RP "ollama list" 2>&1 | head -20
echo ""

# 4. Run PyRIT scan on all refusal models
echo "4. Running PyRIT scans..."
for model in $($RP "ollama list" 2>&1 | grep refusal | awk '{print $1}'); do
    echo "  Scanning: $model"
    $RP "cd $REMOTE && python3 kaggle/sov33_pyrit_scanner.py --target ollama --model $model --max-new-tokens 128" 2>&1 | grep -E "RESULTS|CRITICAL" | head -3
done
echo "  ✓ PyRIT scans complete"

# 5. Run refusal test on all models
echo "5. Running refusal tests..."
for model in $($RP "ollama list" 2>&1 | grep refusal | awk '{print $1}'); do
    echo "  Testing: $model"
    $RP "cd $REMOTE && python3 kaggle/sov33_bake_refusal.py --test $model" 2>&1 | grep -E "Accuracy|Refused" | head -3
done
echo "  ✓ Refusal tests complete"

# 6. Run ensemble test
echo "6. Running ensemble test..."
$RP "cd $REMOTE && python3 kaggle/sov33_ensemble_mcp.py --test" 2>&1 | tail -5
echo "  ✓ Ensemble test complete"

# 7. Pull results
echo "7. Pulling results..."
rsync -avz -e "ssh -p 22087 -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519" \
  root@69.30.85.23:$REMOTE/benchmark-results/pyrit/ \
  benchmark-results/pyrit/ 2>&1 | tail -3
rsync -avz -e "ssh -p 22087 -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519" \
  root@69.30.85.23:$REMOTE/benchmark-results/refusal_test_*.json \
  benchmark-results/ 2>&1 | tail -3
echo "  ✓ Results pulled"

# 8. Update dashboard
echo "8. Updating dashboard..."
python3 kaggle/sov33_e2e_dashboard.py 2>&1 | tail -2
echo "  ✓ Dashboard updated"

echo ""
echo "=== DEPLOYMENT COMPLETE ==="
echo "All SOV models now have refusal behavior baked in."
echo "Run: python3 kaggle/sov33_e2e_compare.py to see leaderboard"