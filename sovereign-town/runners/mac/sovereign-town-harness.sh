#!/bin/bash
# Keep the Sovereign Town benchmark harness server alive on localhost:3941.
# Called by com.csoai.sovereign-town-harness.plist; also safe to run manually.
set -euo pipefail
P0="/Users/nicholas/clawd/sovereign-town/p0_aqua"
LOG="/Users/nicholas/.kimi/logs/sovereign/harness-server.log"
mkdir -p "$(dirname "$LOG")"
if pgrep -f 'python3.11 -m benchmark serve' >/dev/null; then
    echo "$(date -Iseconds) harness server already running" >> "$LOG"
    exit 0
fi
cd "$P0"
exec /opt/homebrew/bin/python3.11 -m benchmark serve --port 3941 >> "$LOG" 2>&1
