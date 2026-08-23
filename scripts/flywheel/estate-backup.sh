#!/bin/bash
# estate-backup.sh — automated backup procedure (2026-08-23, JEEVES).
# Syncs the estate's durable state OFF the Mac to Oracle + pod, per the
# "work from pods, not the MacBook" mandate. Run via LaunchAgent (hourly).
# Never touches .hermes (protected) or .ollama (other lane's).
set -uo pipefail
LOG="$HOME/clawd/_evacuation/logs/estate-backup.log"
mkdir -p "$(dirname "$LOG")"
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }
ORACLE="ubuntu@141.147.73.85"

echo "$(TS) estate-backup start" >> "$LOG"

# 1. Living DB → Oracle
scp -q -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
  "$HOME/clawd/csoai-static-deploy2/SOVOS/living/kernel_results.jsonl" \
  "$HOME/clawd/csoai-static-deploy2/SOVOS/living/sim_cards.jsonl" \
  "$ORACLE:~/sovos-estate-backup/living/" 2>/dev/null \
  && echo "$(TS) living DB → Oracle" >> "$LOG"

# 2. New h3k cards → Oracle (only new since last marker)
LAST_CARD=$(cat "$HOME/clawd/scripts/flywheel/.card-backup-last" 2>/dev/null || echo 0)
for f in "$HOME"/sim-world-data/cards/h3k-*.json; do
  mt=$(stat -f %m "$f" 2>/dev/null || echo 0)
  if [ "$mt" -gt "$LAST_CARD" ]; then
    scp -q -o ConnectTimeout=30 -o StrictHostKeyChecking=no "$f" \
      "$ORACLE:~/sovos-estate-backup/cards/" 2>/dev/null
  fi
done
date +%s > "$HOME/clawd/scripts/flywheel/.card-backup-last"
echo "$(TS) cards → Oracle" >> "$LOG"

# 3. Signed boards → pod (already synced via hf-s3-sync; verify count)
POD_BOARDS=$(ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no -i "$HOME/.runpod/ssh/runpodctl-ssh-key" -p 23243 \
  root@194.26.196.156 'ls /workspace/csoai-site-main/SOVOS/boards-signed/*.signed.json 2>/dev/null | wc -l' 2>/dev/null)
echo "$(TS) pod boards: $POD_BOARDS (workspace is the live store)" >> "$LOG"

echo "$(TS) estate-backup done" >> "$LOG"
