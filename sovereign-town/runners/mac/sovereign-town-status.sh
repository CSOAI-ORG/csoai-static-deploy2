#!/bin/bash
# Sovereign Town — Mac partition status reporter (Kimi-managed)
# Runs every 10 min. Writes to local log.

set -euo pipefail

LOG_DIR="/Users/nicholas/.kimi/logs/sovereign"
mkdir -p "$LOG_DIR"
OUT="$LOG_DIR/sovereign-town-status.md"
P0="/Users/nicholas/clawd/sovereign-town/p0_aqua"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

PID=$(pgrep -f 'flywheel_forever.py --seed-base 200000000' || true)
if [ -n "$PID" ]; then
  STATE="running (pid $PID)"
else
  STATE="DOWN"
fi

FLEET=$(/opt/homebrew/bin/python3.11 - <<PY 2>/dev/null || echo '{}'
import json
with open('/Users/nicholas/clawd/sovereign-town/p0_aqua/fleet_status_mac.json') as f:
    print(json.dumps(json.load(f), indent=2))
PY
)

LEDGER_TAIL=$(tail -1 "$P0/flywheel_ledger_mac.jsonl" 2>/dev/null | /opt/homebrew/bin/python3.11 -c 'import json,sys; print(json.dumps(json.load(sys.stdin), indent=2))' 2>/dev/null || echo "  (no ledger)")

{
  echo "## Mac partition — $TS"
  echo "- state: $STATE"
  echo "- fleet_status:"
  echo "$FLEET"
  echo "- last_ledger_entry:"
  echo "$LEDGER_TAIL"
  echo
} >> "$OUT"

# Mirror public-facing fleet data to proofof-site landing page
PUBLIC_DIR="/Users/nicholas/clawd/proofof-site/sovereign-town"
mkdir -p "$PUBLIC_DIR"
cp "$P0/fleet_status_mac.json" "$PUBLIC_DIR/fleet_status_mac.json" 2>/dev/null || true
cp "$P0/moat_models.json" "$PUBLIC_DIR/moat_models.json" 2>/dev/null || true

tail -n 200 "$OUT" > "$OUT.tmp" && mv "$OUT.tmp" "$OUT"
