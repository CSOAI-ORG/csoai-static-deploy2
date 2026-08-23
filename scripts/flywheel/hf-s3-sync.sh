#!/bin/bash
# Sync signed evidence + sim cards to HF S3 (durable object storage).
# Boards live on the pod; living DB is local. Creds from keystone.
# INCREMENTAL (2026-08-22): only pulls boards newer than the last sync marker —
# a 345-board full pull took ~1h and was redundant every cycle.
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
export AWS_ACCESS_KEY_ID="$(grep HF_S3_ACCESS_KEY ~/.dsh/.env | cut -d= -f2)"
export AWS_SECRET_ACCESS_KEY="$(grep HF_S3_SECRET_KEY ~/.dsh/.env | cut -d= -f2)"
ENDPOINT="https://s3.hf.co/Nicholastempleman"
LIVING="$HOME/clawd/csoai-static-deploy2/SOVOS/living"
SSH_KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
MARKER="$HOME/clawd/scripts/flywheel/.s3-sync-last"
echo "$(date -u +%H:%M) S3 sync start"

# 1. boards from pod — INCREMENTAL: pull only boards newer than marker
mkdir -p /tmp/s3-signed
LAST=$(cat "$MARKER" 2>/dev/null || echo 0)
# list pod boards with mtimes, filter newer than marker, pull only those
ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" -p 23243 \
  "root@194.26.196.156" "find /workspace/csoai-site-main/SOVOS/boards-signed -name '*.signed.json' -newermt @$LAST -printf '%f\n'" \
  > /tmp/s3-new-files.txt 2>/dev/null
NEW_N=$(wc -l < /tmp/s3-new-files.txt | tr -d ' ')
if [ "$NEW_N" -gt 0 ]; then
  # pull only the new files
  while read -r f; do
    [ -z "$f" ] && continue
    scp -q -o StrictHostKeyChecking=no -i "$SSH_KEY" -P 23243 \
      "root@194.26.196.156:/workspace/csoai-site-main/SOVOS/boards-signed/$f" /tmp/s3-signed/ 2>/dev/null
  done < /tmp/s3-new-files.txt
fi
N=$(ls /tmp/s3-signed/*.signed.json 2>/dev/null | wc -l | tr -d ' ')
echo "  pulled $N new boards (since marker)"
if [ "$N" -gt 0 ]; then
  aws --endpoint-url "$ENDPOINT" s3 cp /tmp/s3-signed/ "s3://csoai-cards/boards-signed/" --recursive 2>&1 | tail -1
  rm -f /tmp/s3-signed/*.signed.json
fi
date +%s > "$MARKER"

# 2. living DB (always current — small files)
for f in sim_cards.jsonl kernel_results.jsonl; do
  aws --endpoint-url "$ENDPOINT" s3 cp "$LIVING/$f" "s3://csoai-cards/living/$f" 2>&1 | tail -1
done
aws --endpoint-url "$ENDPOINT" s3 cp "$LIVING/units/units.jsonl" "s3://csoai-cards/living/units.jsonl" 2>&1 | tail -1
echo "$(date -u +%H:%M) S3 sync done ($N new boards + living DB)"
