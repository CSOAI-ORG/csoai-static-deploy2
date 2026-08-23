#!/bin/bash
# oracle_arm_setup.sh — Deploy data synthesis daemon to Oracle ARM
# Sets up a cron job on the Oracle ARM instance to run data synthesis
set -euo pipefail

INSTANCE_IP="${1:-}"
if [ -z "$INSTANCE_IP" ]; then
    echo "Usage: $0 <oracle-instance-ip>"
    echo "You need to replace with your actual Oracle ARM instance IP."
    echo ""
    echo "Setup steps:"
    echo "  1. Create Oracle ARM instance (always-free, Ubuntu 22.04)"
    echo "  2. Note the public IP"
    echo "  3. Run: $0 <ip>"
    exit 1
fi

echo "=== Oracle ARM Data Synthesis Daemon ==="
echo "Target: $INSTANCE_IP"
echo ""

# Create remote dir and copy scripts
ssh -o StrictHostKeyChecking=accept-new "ubuntu@$INSTANCE_IP" "mkdir -p ~/sov-synthesis"

# Copy synthesis script
scp -o StrictHostKeyChecking=accept-new \
    benchmark-results/synthesize_training_data.py \
    "ubuntu@$INSTANCE_IP:~/sov-synthesis/"

# Copy oracle daemon
scp -o StrictHostKeyChecking=accept-new \
    oracle_daemon.sh \
    "ubuntu@$INSTANCE_IP:~/sov-synthesis/"

# Install Python deps and set up cron
ssh -o StrictHostKeyChecking=accept-new "ubuntu@$INSTANCE_IP" bash -s << 'REMOTE'
    set -e
    sudo apt-get update -qq
    sudo apt-get install -y -qq python3-pip python3-venv
    cd ~/sov-synthesis
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q requests tqdm

    # Set up hourly cron for synthesis
    SCRIPT_DIR="$HOME/sov-synthesis"
    CRON_JOB="0 * * * * cd $SCRIPT_DIR && .venv/bin/python3 synthesize_training_data.py --mode light >> ~/synthesis.log 2>&1"
    (crontab -l 2>/dev/null | grep -v synthesize; echo "$CRON_JOB") | crontab -
    echo "Cron installed. Runs hourly."
    echo "Logs: ~/synthesis.log"
REMOTE

echo ""
echo "=== Oracle ARM daemon deployed ==="
echo "Synthesis runs hourly. Results accumulate in ~/sov-synthesis/"
echo ""
echo "To pull results:"
echo "  scp ubuntu@$INSTANCE_IP:~/sov-synthesis/*.jsonl ./free_gpu/"
