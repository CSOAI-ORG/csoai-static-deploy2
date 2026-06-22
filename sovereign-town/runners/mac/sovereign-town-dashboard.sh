#!/bin/bash
# Keep the Sovereign Town dashboard server alive on localhost:3940.
# Called by com.csoai.sovereign-town-dashboard.plist; also safe to run manually.
set -euo pipefail
P0="/Users/nicholas/clawd/sovereign-town/p0_aqua"
LOG="/Users/nicholas/.kimi/logs/sovereign/dashboard-server.log"
mkdir -p "$(dirname "$LOG")"
if pgrep -f 'dashboard_server.py' >/dev/null; then
    echo "$(date -Iseconds) dashboard_server already running" >> "$LOG"
    exit 0
fi
cd "$P0"
# Load local env overrides (SOV_TOWN_SOV3_MESH_URL, SOV_TOWN_FREELLMAPI_KEY, etc.)
if [ -f "$P0/.env" ]; then
  set -a
  # shellcheck source=/dev/null
  . "$P0/.env"
  set +a
fi
exec /opt/homebrew/bin/python3.11 dashboard_server.py >> "$LOG" 2>&1
