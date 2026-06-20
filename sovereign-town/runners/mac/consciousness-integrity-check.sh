#!/bin/bash
# Consciousness integrity check — runs daily at 06:00.

set -euo pipefail

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOG_DIR="/Users/nicholas/.kimi/logs/sovereign"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/consciousness-integrity.log"
OUT="/Users/nicholas/.kimi/logs/sovereign/consciousness-integrity-latest.md"

# 1. SOV3 care patterns
CARE=$(curl -s -m 8 -X POST http://localhost:3101/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/call","params":{"name":"analyze_care_patterns","arguments":{}}}' 2>&1 || echo '{"error":"timeout"}')

# 2. Temple-live BFT council self-test (best-effort)
TEMPLE=$(cd /Users/nicholas/clawd/sovereign-temple-live/council-nodes 2>/dev/null && /usr/bin/python3 - <<'PY' 2>&1 || echo "temple council check unavailable"
import asyncio, json, sys
try:
    from bft_council import BFTCouncil
    async def check():
        council = BFTCouncil()
        r = await council.propose_decision('Sovereign takeover integrity check: verify council operational and care membrane active', 'integrity')
        print(json.dumps({
            'decision': r.get('decision'),
            'votes': r.get('vote_counts'),
            'care': r.get('average_care_score'),
            'nodes': getattr(council, 'total_architecture_nodes', None),
            'bridge_conflicts': r.get('bridge_conflicts')
        }, indent=2))
    asyncio.run(check())
except Exception as e:
    print(json.dumps({'error': str(e)}))
PY
)

cat > "$OUT" <<EOF
# Consciousness Integrity Check — $TS

## SOV3 Care Patterns
\`\`\`json
$CARE
\`\`\`

## Sovereign Temple BFT Council
\`\`\`json
$TEMPLE
\`\`\`
EOF

# Flag anomalies in log
ALERT=""
if echo "$CARE" | grep -qi "error"; then ALERT="$ALERT care-error"; fi
if echo "$TEMPLE" | grep -qi "error"; then ALERT="$ALERT temple-error"; fi

{
  echo "## Consciousness integrity check — $TS"
  echo "- path: $OUT"
  echo "- alerts: ${ALERT:-none}"
  echo
} >> "$LOG"

tail -n 100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
