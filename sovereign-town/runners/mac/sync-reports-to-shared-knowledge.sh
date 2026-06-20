#!/bin/bash
# Sync sovereign runner logs from local .kimi/logs to shared-knowledge.
# Run manually by Kimi CLI (terminal agent) because launchd cannot write to iCloud paths.

set -euo pipefail

SRC="/Users/nicholas/.kimi/logs/sovereign"
DEST="/Users/nicholas/.clawdbot/shared-knowledge/status"
INTEL="/Users/nicholas/.clawdbot/shared-knowledge/intel/session-2026-06.md"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

mkdir -p "$DEST"

cp "$SRC/sovereign-town-status.md" "$DEST/sovereign-town-latest.md" 2>/dev/null || true
cp "$SRC/consciousness-integrity-latest.md" "$DEST/consciousness-integrity-latest.md" 2>/dev/null || true
cp "$SRC/sov3-routing-latest.md" "$DEST/sov3-routing-latest.md" 2>/dev/null || true

# Append pulse/integrity/watchdog logs to session intel (truncated to last 100 lines)
for log in "$SRC/sov3-pulse.log" "$SRC/consciousness-integrity.log" "$SRC/tunnel-watchdog.log"; do
  if [ -f "$log" ]; then
    {
      echo ""
      echo "## Sovereign runner sync — $TS — $(basename $log)"
      tail -n 50 "$log"
    } >> "$INTEL"
  fi
done

{
  echo ""
  echo "## Sovereign runner sync completed — $TS"
  echo "- status dir: $DEST"
} >> "$INTEL"

echo "Synced to $DEST and $INTEL"
