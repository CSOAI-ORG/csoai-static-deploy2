#!/bin/bash
# runpod_migrate.sh — Move ALL SOV33 work to RunPod
# This script creates a RunPod pod, syncs everything, and sets up remote execution
# Run this ONCE to migrate. After that, use runpod_exec.sh for remote commands.

set -euo pipefail

RUNPOD_API_KEY=$(cat ~/.runpod/api_key 2>/dev/null || echo "")
if [ -z "$RUNPOD_API_KEY" ]; then
    echo "ERROR: No RunPod API key at ~/.runpod/api_key"
    exit 1
fi

POD_NAME="sov33-workhorse"
GPU_TYPE="NVIDIA GeForce RTX 3090"
REMOTE_DIR="/workspace/sov33"
LOCAL_BASE="/Users/nicholas/clawd/csoai-static-deploy2"

echo "=== RunPod Migration ==="
echo "Pod: $POD_NAME"
echo "GPU: $GPU_TYPE"
echo "Remote: $REMOTE_DIR"
echo ""

# Step 1: Create pod via GraphQL
echo "Step 1: Creating RunPod pod..."
POD_ID=$(curl -s https://api.runpod.io/graphql \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"query":"mutation { podFindAndDeployOnDemand(input: {name: \"'"$POD_NAME"'\", imageName: \"runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04\", gpuTypeId: \"'"$GPU_TYPE"'\", gpuCount: 1, containerDiskInGb: 50, volumeInGb: 200, ports: \"22/tcp,8080/http,11434/http\"}) { id desiredStatus }}"}' | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data',{}).get('podFindAndDeployOnDemand',{}).get('id','FAILED'))")

if [ "$POD_ID" = "FAILED" ]; then
    echo "  Pod creation failed. Trying to find existing pod..."
    POD_ID=$(curl -s https://api.runpod.io/graphql \
        -H "Authorization: Bearer $RUNPOD_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"query":"{ myself { pod { id name status } } }"}' | python3 -c "import json,sys; d=json.load(sys.stdin); pods=d.get('data',{}).get('myself',{}).get('pod',[]); print(pods[0]['id'] if pods else 'NONE')")
fi

echo "  Pod ID: $POD_ID"

# Step 2: Wait for pod to be ready
echo "Step 2: Waiting for pod to be ready..."
for i in $(seq 1 60); do
    STATUS=$(curl -s https://api.runpod.io/graphql \
        -H "Authorization: Bearer $RUNPOD_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"query":"{ myself { pod { id status machine { gpuDisplayName } runtime { uptimeInSeconds } } } }"}' | python3 -c "import json,sys; d=json.load(sys.stdin); pods=d.get('data',{}).get('myself',{}).get('pod',[]); [print(p['status']) for p in pods if p['id']=='"$POD_ID"']" 2>/dev/null || echo "WAITING")
    
    if [ "$STATUS" = "RUNNING" ]; then
        echo "  Pod is RUNNING"
        break
    fi
    echo "  Status: $STATUS (waiting...)"
    sleep 10
done

# Step 3: Get pod IP
echo "Step 3: Getting pod IP..."
POD_IP=$(curl -s https://api.runpod.io/graphql \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"query":"{ myself { pod { id publicIp portMappings } } }"}' | python3 -c "import json,sys; d=json.load(sys.stdin); pods=d.get('data',{}).get('myself',{}).get('pod',[]); [print(p.get('publicIp','')) for p in pods if p['id']=='"$POD_ID"']" 2>/dev/null)

echo "  Pod IP: $POD_IP"

if [ -z "$POD_IP" ]; then
    echo "  ERROR: Could not get pod IP"
    exit 1
fi

# Step 4: Sync files to RunPod
echo "Step 4: Syncing files to RunPod..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=30 root@$POD_IP "mkdir -p $REMOTE_DIR/benchmark-results $REMOTE_DIR/benchmark-results/rag $REMOTE_DIR/benchmark-results/learning-ready $REMOTE_DIR/kaggle $REMOTE_DIR/tools $REMOTE_DIR/sovereign-charters $REMOTE_DIR/functions"

# Sync benchmark-results (training data, task registry, scripts)
echo "  Syncing benchmark-results/..."
rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    "$LOCAL_BASE/benchmark-results/" \
    root@$POD_IP:"$REMOTE_DIR/benchmark-results/" \
    --exclude='*.sigil.json' \
    --exclude='runpod_results/' \
    --exclude='__pycache__/' 2>&1 | tail -5

# Sync training data
echo "  Syncing learning-ready/..."
rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    "$LOCAL_BASE/benchmark-results/learning-ready/" \
    root@$POD_IP:"$REMOTE_DIR/benchmark-results/learning-ready/" 2>&1 | tail -3

# Sync RAG corpora
echo "  Syncing rag/..."
rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    "$LOCAL_BASE/benchmark-results/rag/" \
    root@$POD_IP:"$REMOTE_DIR/benchmark-results/rag/" 2>&1 | tail -3

# Sync models from ~/.sovereign
echo "  Syncing sovereign models..."
if [ -d ~/.sovereign/models ]; then
    rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
        ~/.sovereign/models/ \
        root@$POD_IP:"$REMOTE_DIR/models/" 2>&1 | tail -3
fi

# Sync kaggle scripts
echo "  Syncing kaggle/..."
rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    "$LOCAL_BASE/kaggle/" \
    root@$POD_IP:"$REMOTE_DIR/kaggle/" 2>&1 | tail -3

# Sync tools
echo "  Syncing tools/..."
rsync -avz --progress -e "ssh -o StrictHostKeyChecking=no" \
    "$LOCAL_BASE/tools/" \
    root@$POD_IP:"$REMOTE_DIR/tools/" 2>&1 | tail -3

# Sync training scripts
echo "  Syncing training scripts..."
for f in train_sovereign_adapter.py train_remaining_owems.py train_multifamily_adapters.py sov33_tempo.py sov33_improvements.py run_benchmark_v3.py run_ollama_benchmark.py; do
    if [ -f "$LOCAL_BASE/benchmark-results/$f" ]; then
        scp -o StrictHostKeyChecking=no "$LOCAL_BASE/benchmark-results/$f" root@$POD_IP:"$REMOTE_DIR/benchmark-results/" 2>/dev/null
    fi
done

# Step 5: Install Ollama and pull models on RunPod
echo "Step 5: Setting up Ollama on RunPod..."
ssh -o StrictHostKeyChecking=no root@$POD_IP "
    curl -fsSL https://ollama.com/install.sh | sh 2>/dev/null
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 5
    ollama pull qwen2.5:0.5b 2>/dev/null
    ollama pull qwen3:0.6b 2>/dev/null
" 2>&1 | tail -5

echo "  Ollama installed and models pulled"

# Step 6: Create remote execution script
echo "Step 6: Creating remote execution script..."
ssh -o StrictHostKeyChecking=no root@$POD_IP "cat > $REMOTE_DIR/exec.sh << 'REMOTE_EOF'
#!/bin/bash
# Remote execution wrapper for SOV33 on RunPod
cd /workspace/sov33

case \"\$1\" in
    bench)
        python3 benchmark-results/run_benchmark_v3.py --model \${2:-sov33-master-v2:latest}
        ;;
    tempo)
        python3 benchmark-results/sov33_tempo.py --benchmark \${2:-sov33-master-v2:latest}
        ;;
    train)
        python3 benchmark-results/train_remaining_owems.py
        ;;
    ollama)
        shift
        ollama \$@
        ;;
    status)
        echo '=== RunPod SOV33 Status ==='
        echo 'Models:' && ollama list
        echo 'Disk:' && df -h /workspace
        echo 'GPU:' && nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo 'no GPU'
        ;;
    *)
        echo 'Usage: exec.sh [bench|tempo|train|ollama|status] [args]'
        ;;
esac
REMOTE_EOF
    chmod +x $REMOTE_DIR/exec.sh"

echo ""
echo "=== Migration Complete ==="
echo ""
echo "Pod ID:    $POD_ID"
echo "Pod IP:    $POD_IP"
echo "SSH:       ssh root@$POD_IP"
echo "Remote:    $REMOTE_DIR"
echo ""
echo "Quick commands:"
echo "  ssh root@$POD_IP '$REMOTE_DIR/exec.sh status'"
echo "  ssh root@$POD_IP '$REMOTE_DIR/exec.sh bench sov33-master-v2:latest'"
echo "  ssh root@$POD_IP '$REMOTE_DIR/exec.sh train'"
echo "  ssh root@$POD_IP '$REMOTE_DIR/exec.sh ollama list'"
echo ""
echo "RunPod URL: https://console.runpod.io/pods/$POD_ID"
