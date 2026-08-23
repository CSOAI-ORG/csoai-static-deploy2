#!/bin/bash
# kaggle_evolve.sh — Push ASI evolution kernel to Kaggle, wait for results, pull back
# Uses Kaggle CLI to push/pull kernel results
set -euo pipefail

KERNEL_NAME="sov33-asi-evolve"
KERNEL_DIR="$(dirname "$0")/../kaggle"
RESULTS_DIR="$(dirname "$0")/../benchmark-results"
LOCAL_RESULTS="$(dirname "$0")/../asi_results/distributed"

mkdir -p "$LOCAL_RESULTS"

echo "=== Kaggle Evolution ==="
echo "Kernel: $KERNEL_NAME"
echo ""

# Check kaggle CLI
if ! command -v kaggle &> /dev/null; then
    echo "ERROR: kaggle CLI not found. Install with: pip install kaggle"
    exit 1
fi

# Check for kernel metadata
METADATA="$KERNEL_DIR/kernel-metadata.json"
if [ ! -f "$METADATA" ]; then
    echo "Creating kernel metadata..."
    cat > "$METADATA" << EOF
{
  "id": "nicholaslawrance/$KERNEL_NAME",
  "title": "SOV33 ASI Evolve",
  "code_file": "sov33_asi_evolve.py",
  "language": "python",
  "kernel_type": "script",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": true,
  "dataset_sources": [],
  "competition_sources": [],
  "kernel_sources": []
}
EOF
fi

# Push kernel
echo "Pushing kernel to Kaggle..."
kaggle kernels push -p "$KERNEL_DIR"

echo "Kernel pushed. Waiting for completion..."

# Poll for completion (max 60 minutes)
MAX_WAIT=3600
POLL_INTERVAL=30
elapsed=0

while [ $elapsed -lt $MAX_WAIT ]; do
    STATUS=$(kaggle kernels status "$KERNEL_NAME" 2>/dev/null | grep -oP 'status:\s*\K\S+' || echo "unknown")
    echo "  Status: $STATUS (${elapsed}s elapsed)"

    if [ "$STATUS" = "complete" ]; then
        echo "Kernel complete!"
        break
    elif [ "$STATUS" = "error" ] || [ "$STATUS" = "cancelled" ]; then
        echo "ERROR: Kernel $STATUS"
        kaggle kernels log "$KERNEL_NAME" 2>/dev/null | tail -20
        exit 1
    fi

    sleep $POLL_INTERVAL
    elapsed=$((elapsed + POLL_INTERVAL))
done

if [ $elapsed -ge $MAX_WAIT ]; then
    echo "TIMEOUT: Kernel did not complete in ${MAX_WAIT}s"
    exit 1
fi

# Pull results
echo ""
echo "Pulling results..."
kaggle kernels output "$KERNEL_NAME" -p "$LOCAL_RESULTS"

# Copy to benchmark-results if they exist
if ls "$LOCAL_RESULTS"/asi_cycle_*.json 1>/dev/null 2>&1; then
    cp "$LOCAL_RESULTS"/asi_cycle_*.json "$RESULTS_DIR/" 2>/dev/null || true
    echo "Results copied to $RESULTS_DIR/"
fi

echo ""
echo "=== Kaggle evolution complete ==="
echo "Results: $LOCAL_RESULTS/"
