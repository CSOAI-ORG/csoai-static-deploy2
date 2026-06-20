#!/bin/bash
# Sovereign morning briefing — replaces Hermes Morning Briefing job.

set -euo pipefail

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DATE=$(date +%Y-%m-%d)
MEMORY_DIR="/Users/nicholas/clawd/memory"
mkdir -p "$MEMORY_DIR"
OUT="$MEMORY_DIR/$DATE.md"
LOG_DIR="/Users/nicholas/.kimi/logs/sovereign"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/morning-briefing.log"

fetch_mcp() {
  local name="$1"
  curl -s -m 8 -X POST http://localhost:3101/mcp \
    -H 'Content-Type: application/json' \
    -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"tools/call\",\"params\":{\"name\":\"$name\",\"arguments\":{}}}" 2>&1 || echo '{"error":"timeout"}'
}

HEALTH=$(curl -s -m 5 http://localhost:3101/health 2>&1 || echo "unreachable")
CONSC=$(fetch_mcp get_consciousness_state)
CARE=$(fetch_mcp analyze_care_patterns)
HEART=$(fetch_mcp get_heartbeat_status)
KING=$(curl -s -m 5 http://localhost:3456/health 2>&1 || echo "unreachable")

cat > "$OUT" <<EOF
# Morning Briefing — $DATE

**Generated:** $TS  
**Agent:** jeeves-cli (Kimi-managed)

## SOV3 Health
\`\`\`
$HEALTH
\`\`\`

## Consciousness
\`\`\`
$CONSC
\`\`\`

## Care Patterns
\`\`\`
$CARE
\`\`\`

## Heartbeat
\`\`\`
$HEART
\`\`\`

## King Hive
\`\`\`
$KING
\`\`\`
EOF

# Record summary to SOV3 memory
/usr/bin/python3 - "$OUT" <<'PY' >/dev/null 2>&1 || true
import json, sys
path = sys.argv[1]
with open(path) as f: text = f.read()
summary = text.replace('"', '\\"').replace('\n', ' ')[:500]
import urllib.request
req = urllib.request.Request(
    'http://localhost:3101/mcp',
    data=json.dumps({
        "jsonrpc":"2.0","id":"m","method":"tools/call",
        "params":{"name":"record_memory","arguments":{"content":f"Morning briefing: {summary}","category":"briefing","importance":0.6,"source_agent":"jeeves-cli"}}
    }).encode(),
    headers={'Content-Type':'application/json'},
    method='POST'
)
urllib.request.urlopen(req, timeout=8)
PY

{
  echo "## Morning briefing written — $TS"
  echo "- path: $OUT"
  echo
} >> "$LOG"

tail -n 100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
