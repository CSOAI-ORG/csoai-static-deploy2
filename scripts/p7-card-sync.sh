#!/bin/bash
# p7-card-sync.sh — auto-sync the latest h3k signed card to harness + pod (P7, 2026-08-18).
# Called at the end of runpod-overnight.sh (and manually). Emits a fresh card if none
# since the last sync, then copies the latest card to ~/master-harness + sov-brain-2.
# Log: ~/clawd/_evacuation/logs/p7-card-sync.log
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="$HOME/clawd/_evacuation/logs/p7-card-sync.log"
mkdir -p "$(dirname "$LOG")"
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }
CARDS_DIR="$HOME/sim-world-data/cards"
HARNESS="$HOME/master-harness/instances/meok-firstborn"
RSYNC="/opt/homebrew/bin/rsync"

echo "$(TS) p7 card-sync start" >> "$LOG"

# 1. Find the latest card
LATEST=$(ls -t "$CARDS_DIR"/h3k-*.json 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
  echo "$(TS) no cards found — nothing to sync" >> "$LOG"
  exit 0
fi
BASE=$(basename "$LATEST")
echo "$(TS) latest card: $BASE ($(stat -f %z "$LATEST") bytes)" >> "$LOG"

# 2. Sync to harness (git-tracked)
cp "$LATEST" "$HARNESS/$BASE" && echo "$(TS) copied to harness" >> "$LOG"
cd "$HOME/master-harness"
git add "instances/meok-firstborn/$BASE" >/dev/null 2>&1
git -c user.name="JEEVES" -c user.email="jeeves@meok.ai" commit -m "firstborn: auto-synced h3k card $BASE (P7 pipeline)" >/dev/null 2>&1 \
  && echo "$(TS) committed to harness" >> "$LOG" || echo "$(TS) harness commit: nothing new or skipped" >> "$LOG"

# 3. Sync to pod
$RSYNC -a --partial -e "ssh -o ConnectTimeout=10 -o BatchMode=yes" \
  "$LATEST" "sov-brain-2:/root/master-harness/instances/meok-firstborn/$BASE" >> "$LOG" 2>&1 \
  && echo "$(TS) synced to sov-brain-2" >> "$LOG" || echo "$(TS) pod sync FAILED" >> "$LOG"

echo "$(TS) p7 done" >> "$LOG"
tail -100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
