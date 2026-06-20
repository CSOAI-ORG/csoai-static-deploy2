#!/bin/bash
# SOV3 coordination pulse — replaces Hermes sov3-coordination-pulse job.

set -euo pipefail

LOG_DIR="/Users/nicholas/.kimi/logs/sovereign"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/sov3-pulse.log"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

DASH=$(curl -s -m 8 -X POST http://localhost:3101/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"p","method":"tools/call","params":{"name":"coord_get_dashboard","arguments":{}}}' 2>&1 || true)

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

/usr/bin/python3 - "$DASH" > "$TMP" <<'PY'
import json, sys
text = sys.argv[1]
try:
    d = json.loads(text)
    c = json.loads(d["result"]["content"][0]["text"])
    print(f"agents {c['agents']['active']}/{c['agents']['total']}, tasks queued {c['tasks']['queued']}, completed {c['tasks']['completed']}, locks {c['locks']['active']}")
except Exception as e:
    print(f"parse_error: {e}")
PY

SUMMARY=$(cat "$TMP")

# Emit sigil
curl -s -m 8 -X POST http://localhost:3101/mcp \
  -H 'Content-Type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"id\":\"s\",\"method\":\"tools/call\",\"params\":{\"name\":\"sigil_emit\",\"arguments\":{\"line\":\"C|jeeves-cli|sov3-pulse|$TS|Sovereign takeover pulse: $SUMMARY\"}}}" > /dev/null 2>&1 || true

{
  echo "## SOV3 coordination pulse — $TS"
  echo "- summary: $SUMMARY"
  echo
} >> "$LOG"

tail -n 200 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
