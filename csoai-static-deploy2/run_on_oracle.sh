#!/bin/bash
# run_on_oracle.sh — Run SOV work on Oracle ARM (free CPU)
# Usage: ./run_on_oracle.sh [command]

set -e
REMOTE="oracle-micro"
DIR="/home/ubuntu/sov33_shared"

ssh_cmd() {
    ssh -o StrictHostKeyChecking=no -o BatchMode=yes $REMOTE "cd $DIR && $@"
}

case "${1:-status}" in
    status)
        echo "=== Oracle ARM Status ==="
        ssh_cmd "uname -a"
        ssh_cmd "df -h /"
        ssh_cmd "free -h 2>/dev/null || echo 'no free'"
        echo ""
        echo "=== Ollama Models ==="
        ssh_cmd "ollama list 2>/dev/null || echo 'Ollama not running'"
        echo ""
        echo "=== Python Version ==="
        ssh_cmd "python3 --version"
        ;;
    
    sync)
        echo "=== Syncing to Oracle ==="
        rsync -avz --progress --exclude='.git' --exclude='.backups' --exclude='__pycache__' --exclude='.venv-training' --exclude='node_modules' --exclude='.DS_Store' --exclude='*.pyc' . $REMOTE:$DIR/
        echo "Sync complete!"
        ;;
    
    e2e)
        echo "=== Running E2E Tests on Oracle ==="
        ssh_cmd "python3 .e2e_tests.py 2>&1 | tail -15"
        ;;
    
    batch)
        echo "=== Running Batch Verifier on Oracle ==="
        ssh_cmd "python3 tools/verify_e2e_batch.py 2>&1 | tail -15"
        ;;
    
    eat)
        echo "=== Running EAT Benchmarks on Oracle ==="
        ssh_cmd "python3 benchmark-results/overnight_eat.py --phase benchmarks 2>&1"
        ;;
    
    overnight)
        echo "=== Running Overnight Runner on Oracle ==="
        ssh_cmd "python3 overnight_runner.py 2>&1"
        ;;
    
    train)
        echo "=== Running Training on Oracle ==="
        ssh_cmd "python3 sov_minimal_train.py --steps 20 --export-ollama --ollama-name sov33-trained 2>&1"
        ;;
    
    benchmark)
        echo "=== Running Full Benchmark on Oracle ==="
        ssh_cmd "python3 sov_length_controlled_eval.py --model sov33-oracle --baseline qwen2.5:0.5b 2>&1 | tail -20"
        ;;
    
    *)
        echo "Usage: $0 [status|sync|e2e|batch|eat|overnight|train|benchmark]"
        ;;
esac
