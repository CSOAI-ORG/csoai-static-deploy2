#!/bin/bash
# swarm_resume.sh — Resume SOV33 swarm from any reachable GPU site
# Tries RunPod first, falls back to Oracle + local Ollama

set -e
SITES=("69.30.85.23:22087")
echo "=== SOV33 Swarm Resume ==="
for site in "${SITES[@]}"; do
    IFS=':' read -r host port <<< "$site"
    echo "Trying $host:$port..."
    if ssh -p "$port" -o ConnectTimeout=10 -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 "root@$host" 'echo OK' 2>/dev/null; then
        echo "✓ RunPod reachable"
        # Push latest code
        rsync -az -e "ssh -p $port -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519" \
            kaggle/ benchmark-results/ "root@$host:/workspace/sovereign_bench_v3/" 2>&1 | tail -3
        ssh -p "$port" -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 "root@$host" 'cd /workspace/sovereign_bench_v3 && bash launch_funnel.sh' 2>&1 | tail -3
        exit 0
    fi
done

echo "RunPod unreachable. Falling back to local swarm..."
# Pull latest from Oracle (which has full backup)
echo "Pulling latest from Oracle..."
rsync -az oracle-micro:/home/ubuntu/sov33_shared/ /tmp/oracle_sync/ 2>&1 | tail -3

# Use local Ollama + APIs
if curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "✓ Local Ollama available"
    python3 kaggle/sov33_local_swarm.py --mode status 2>&1 | head -20
fi

# Run self-eval with available APIs
python3 kaggle/sov33_local_swarm.py --mode self-eval --tasks 3 --workers 3 --out-prefix swarm_resume 2>&1 | tail -20
