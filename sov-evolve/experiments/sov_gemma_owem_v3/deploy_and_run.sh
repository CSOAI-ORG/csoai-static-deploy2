#!/bin/bash
# deploy_and_run.sh — Deploy ASI-Evolve to RunPod and run evolution
# Usage: ./deploy_and_run.sh <pod_ip> [rounds]

set -e

POD_IP="${1:?Usage: $0 <pod_ip> [rounds]}"
ROUNDS="${2:-10}"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=15"
EXPERIMENT_DIR="$(dirname "$0")"
REMOTE_DIR="/workspace/sov-evolve/experiments/sov_gemma_owem_v3"

echo "=== ASI-Evolve Deploy & Run ==="
echo "Pod: $POD_IP"
echo "Rounds: $ROUNDS"
echo ""

# 1. Create remote directories
echo "[1/5] Creating remote directories..."
ssh $SSH_OPTS root@$POD_IP "mkdir -p $REMOTE_DIR/{programs,evaluations,mutations,logs}"

# 2. Sync experiment files
echo "[2/5] Syncing experiment files..."
scp $SSH_OPTS -r "$EXPERIMENT_DIR"/* root@$POD_IP:$REMOTE_DIR/

# 3. Install dependencies
echo "[3/5] Installing dependencies on pod..."
ssh $SSH_OPTS root@$POD_IP "pip install -q urllib3 2>/dev/null; which ollama || (curl -fsSL https://ollama.com/install.sh | sh)"

# 4. Ensure gemma3:12b is available
echo "[4/5] Ensuring gemma3:12b is pulled..."
ssh $SSH_OPTS root@$POD_IP "ollama pull gemma3:12b" &
PULL_PID=$!

# 5. Start evolution while model downloads
echo "[5/5] Starting evolution ($ROUNDS rounds)..."
echo "  SSH into pod and run:"
echo "  cd $REMOTE_DIR && python3 asi_evolve.py $ROUNDS"
echo ""
echo "Or wait for pull to complete and run automatically..."

wait $PULL_PID

echo ""
echo "=== Starting ASI-Evolve ==="
ssh $SSH_OPTS root@$POD_IP "cd $REMOTE_DIR && python3 asi_evolve.py $ROUNDS"

echo ""
echo "=== Evolution complete ==="
echo "Results at: $REMOTE_DIR/evolution_report.json"
echo "Download with: scp $SSH_OPTS root@$POD_IP:$REMOTE_DIR/evolution_report.json ./"
