#!/bin/bash
# Keep the Sovereign Town MCP SSE server alive on localhost:3942.
# Called by com.csoai.sovereign-town-mcp-sse.plist; also safe to run manually.
set -euo pipefail
P0="/Users/nicholas/clawd/sovereign-town/p0_aqua"
LOG="/Users/nicholas/.kimi/logs/sovereign/mcp-sse-server.log"
mkdir -p "$(dirname "$LOG")"
if pgrep -f 'python3.11 -m benchmark mcp --transport sse' >/dev/null; then
    echo "$(date -Iseconds) mcp sse server already running" >> "$LOG"
    exit 0
fi
cd "$P0"
exec /opt/homebrew/bin/python3.11 -m benchmark mcp --transport sse --port 3942 --host 127.0.0.1 >> "$LOG" 2>&1
