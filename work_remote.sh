#!/bin/bash
# work_remote.sh — Run ALL work on Oracle/RunPod, NOT on Mac
# Usage: bash work_remote.sh [oracle|runpod] [command]
#
# Examples:
#   bash work_remote.sh oracle status
#   bash work_remote.sh oracle run-benchmark
#   bash work_remote.sh oracle run-funnel
#   bash work_remote.sh runpod deploy-refusal
#   bash work_remote.sh runpod run-pyrit

set -e

ORACLE="oracle-micro"
RUNPOD="ssh -p 22087 -o StrictHostKeyChecking=no -o BatchMode=yes -i ~/.ssh/id_ed25519 root@69.30.85.23"
REMOTE_DIR="/home/ubuntu/sov33_shared"

TARGET=${1:-oracle}
CMD=${2:-status}

echo "=== SOV33 Remote Work ==="
echo "Target: $TARGET"
echo "Command: $CMD"
echo ""

case $TARGET in
  oracle)
    SSH="$ORACLE"
    DIR="$REMOTE_DIR"
    ;;
  runpod)
    SSH="$RUNPOD"
    DIR="/workspace/sovereign_bench_v3"
    ;;
  *)
    echo "Unknown target: $TARGET"
    exit 1
    ;;
esac

case $CMD in
  status)
    echo "Checking status on $TARGET..."
    $SSH "echo '=== Disk ==='; df -h / $DIR 2>&1 | head -3; echo '=== Files ==='; ls $DIR/ 2>&1 | head -10; echo '=== Models ==='; curl -s http://localhost:11434/api/tags 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d[\"models\"]),\"models\")' 2>/dev/null || echo 'Ollama not running'"
    ;;
  sync)
    echo "Syncing code to $TARGET..."
    rsync -avz --exclude='*.pyc' --exclude='__pycache__' --exclude='*.bak*' \
      --exclude='*.csv' --exclude='*.zip' --exclude='*.parquet' --exclude='*.pt' \
      --exclude='study/' --exclude='*model*' --exclude='*.tar.gz' \
      -e "ssh" /Users/nicholas/clawd/csoai-static-deploy2/ $SSH:$DIR/
    echo "✓ Synced"
    ;;
  run-benchmark)
    echo "Running benchmark on $TARGET..."
    $SSH "cd $DIR && python3 kaggle/sov33_e2e_orchestrator_v2.py --target ollama --tasks 3 --workers 4 --out-prefix e2e_remote"
    ;;
  run-funnel)
    echo "Running funnel on $TARGET..."
    $SSH "cd $DIR && python3 kaggle/sov33_e2e_funnel.py --auto --tasks 3 --workers 4 --out-prefix funnel_remote"
    ;;
  run-pyrit)
    echo "Running PyRIT on $TARGET..."
    $SSH "cd $DIR && python3 kaggle/sov33_pyrit_scanner.py --target ollama --model sov33-refusal-14b --max-new-tokens 128"
    ;;
  deploy-refusal)
    echo "Deploying refusal models on $TARGET..."
    $SSH "cd $DIR && bash deploy_refusal_models.sh"
    ;;
  deploy-all)
    echo "Deploying everything on $TARGET..."
    $SSH "cd $DIR && bash deploy_everything.sh"
    ;;
  pull-results)
    echo "Pulling results from $TARGET..."
    rsync -avz -e "ssh" $SSH:$DIR/benchmark-results/ /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/
    echo "✓ Results pulled"
    ;;
  shell)
    echo "Opening shell on $TARGET..."
    $SSH
    ;;
  *)
    echo "Unknown command: $CMD"
    echo "Commands: status, sync, run-benchmark, run-funnel, run-pyrit, deploy-refusal, deploy-all, pull-results, shell"
    ;;
esac