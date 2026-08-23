#!/bin/bash
# F2 sync — pull generated items off the 3090 into the estate's items-full/ dir.
# Run after the nightly generation (e.g. 04:10 UTC) to feed measure_full.py.
set -uo pipefail
SSH_KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
POD="root@194.26.196.156"; PORT=23243
DEST="$HOME/clawd/kimi-regen/arena-build/items-full"
mkdir -p "$DEST"
scp -i "$SSH_KEY" -P "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes \
  "$POD":/workspace/f2/items/*.jsonl "$DEST/" 2>/dev/null
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) synced $(ls "$DEST" 2>/dev/null | wc -l | tr -d ' ') axis files"
