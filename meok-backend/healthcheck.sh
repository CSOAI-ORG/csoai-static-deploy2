#!/usr/bin/env bash
# =====================================================================
# MEOK SOV3 Backend — healthcheck.sh
# Post-MCP probe: sends a JSON-RPC tools/list request to /mcp.
# CRITICAL: per ~/clawd/AGENTS.md §3 — NEVER GET /health (false-kill).
# =====================================================================

set -euo pipefail

# ---- Args / defaults ------------------------------------------------------
URL="${1:-${MEOK_URL:-http://127.0.0.1:3101/mcp}}"
TIMEOUT="${HEALTHCHECK_TIMEOUT:-5}"
RETRIES="${HEALTHCHECK_RETRIES:-3}"

# ---- Pretty output --------------------------------------------------------
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'

PAYLOAD='{"jsonrpc":"2.0","method":"tools/list","id":1}'

probe() {
    local attempt="$1"
    echo -e "${YELLOW}→${NC} attempt ${attempt}/${RETRIES}: ${URL}"
    HTTP_CODE=$(curl -sS --max-time "$TIMEOUT" \
        -o /tmp/sov3-health-$$.json -w "%{http_code}" \
        -X POST "$URL" \
        -H 'Content-Type: application/json' \
        -d "$PAYLOAD" 2>/dev/null || echo "000")
    BODY=$(cat /tmp/sov3-health-$$.json 2>/dev/null || echo "")
    rm -f /tmp/sov3-health-$$.json

    if [ "$HTTP_CODE" = "200" ] && echo "$BODY" | grep -q '"result"'; then
        TOOLS=$(echo "$BODY" | grep -oE '"name":"[^"]+"' | wc -l | tr -d ' ')
        echo -e "${GREEN}✓${NC} SOV3 healthy — ${HTTP_CODE}, tools/list returned ${TOOLS} tools"
        return 0
    else
        echo -e "${RED}✗${NC} HTTP ${HTTP_CODE} (body: $(echo "$BODY" | head -c 80))"
        return 1
    fi
}

# ---- Retry loop ------------------------------------------------------------
for i in $(seq 1 "$RETRIES"); do
    if probe "$i"; then
        echo -e "${GREEN}🜏 HEARTBEAT GREEN${NC}"
        exit 0
    fi
    [ "$i" -lt "$RETRIES" ] && sleep 1
done

echo -e "${RED}💀 HEARTBEAT RED after ${RETRIES} attempts${NC}"
exit 1
