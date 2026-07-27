#!/bin/bash
# run_master_batch.sh — Run master batch in background
# Usage:
#   ./run_master_batch.sh              # 10 cycles (default)
#   ./run_master_batch.sh 50           # 50 cycles
#   ./run_master_batch.sh infinite     # run forever
#   ./run_master_batch.sh 10 --parallel  # parallel mode

set -euo pipefail
cd /Users/nicholas/clawd/csoai-static-deploy2

CYCLES="${1:-10}"
shift 2>/dev/null || true
EXTRA_ARGS="$*"

if [ "$CYCLES" = "infinite" ]; then
    CYCLE_ARG="--cycles 0"
else
    CYCLE_ARG="--cycles $CYCLES"
fi

echo "=== Master Batch Runner ==="
echo "Cycles: $CYCLES"
echo "Extra args: $EXTRA_ARGS"
echo "Log: master_batch.log"
echo ""

nohup python3 -u master_batch.py $CYCLE_ARG $EXTRA_ARGS > master_batch.log 2>&1 &
PID=$!

echo "Master batch PID: $PID"
echo ""
echo "Monitor with:"
echo "  tail -f master_batch.log"
echo "  cat batch_results/summary.json | python3 -m json.tool"
echo ""
echo "Stop with:"
echo "  kill $PID"
