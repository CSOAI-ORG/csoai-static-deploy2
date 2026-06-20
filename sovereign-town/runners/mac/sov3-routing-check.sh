#!/bin/bash
# SOV3 routing probe — reports which instance answers localhost:3101.

set -euo pipefail

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
OUT="/Users/nicholas/.clawdbot/shared-knowledge/status/sov3-routing-latest.md"
mkdir -p "$(dirname "$OUT")"

HEALTH=$(curl -s -m 5 http://localhost:3101/health 2>&1 || echo "unreachable")

INSTANCE=$(/usr/bin/python3 -c '
import json, sys
text = sys.argv[1]
try:
    d = json.loads(text)
    print("VM (canonical)" if d.get("version") == "2.0.0" else "Mac (fallback)")
except Exception:
    print("unknown")
' "$HEALTH")

HOSTNAME=$(/usr/bin/python3 -c '
import json, sys
text = sys.argv[1]
try:
    print(json.loads(text).get("hostname", "unknown"))
except Exception:
    print("unknown")
' "$HEALTH")

cat > "$OUT" <<EOF
# SOV3 Routing Check — $TS

- localhost:3101 resolves to: **$INSTANCE**
- reported hostname: $HOSTNAME
- raw health (first 300 chars):
\`\`\`json
${HEALTH:0:300}
\`\`\`

*Canonical substrate is VM ":3101" via tunnel. If this shows Mac (fallback), the tunnel is down.*
EOF
