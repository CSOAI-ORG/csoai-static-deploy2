#!/bin/bash
# nightly-e2e.sh — overnight E2E for the sovereign pipeline.
# Schedule: 02:00 local time every night.
#
# Install via: crontab -e  then add:
#   0 2 * * * /Users/nicholas/clawd/csoai-static-deploy2/nightly-e2e.sh >> /tmp/sovereign-nightly.log 2>&1

set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Make sure the local server is running
if ! lsof -i :8766 -P -n 2>/dev/null | grep -q LISTEN; then
    echo "[$DATE] starting local server"
    cd "$HERE"
    nohup python3 sov_local_server.py > /tmp/sov_local_nightly.log 2>&1 &
    sleep 3
fi

# Run the overnight pipeline: audit + ingest + spawn/grow + e2e + selftests
echo "[$DATE] running overnight E2E"
python3 "$HERE/sov_e2e_overnight.py" 2>&1
echo "[$DATE] done"
