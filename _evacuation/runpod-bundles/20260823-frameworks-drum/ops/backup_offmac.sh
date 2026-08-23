#!/bin/bash
# BACKUP OFF-MAC — keep the drum's source of truth off the Mac.
# Pushes the doctrine-clean drum pack to every reachable compute/storage target (RunPod GPU
# RAG volume + Oracle) and drops a dated tarball on each. The Mac is a controller, not the
# only home. Fail-open per target (a dead target is skipped, never a hard stop).
set -u
DRUM="$HOME/master-harness/knowledge/frameworks-drum"
DATE=$(date +%Y%m%d)
BK="$DRUM/ops/backups"
mkdir -p "$BK"
TAR="$BK/drum-$DATE.tar.gz"

# 1) dated tarball (local staging — the off-Mac copies are the point)
tar -czf "$TAR" --exclude="ops/backups" --exclude=".git" --exclude="__pycache__" -C "$DRUM" . 2>/dev/null
echo "tarball: $TAR ($(du -sh "$TAR" | cut -f1))"

# 2) push the pack + tarball to each reachable target
for TARGET in sov-brain-2 oracle-micro; do
  if ssh -o ConnectTimeout=6 -o BatchMode=yes "$TARGET" 'exit 0' 2>/dev/null; then
    rsync -az --exclude=".git" --exclude="__pycache__" \
      -e "ssh -o ConnectTimeout=12 -o BatchMode=yes" \
      "$DRUM"/ "$TARGET":frameworks-drum/ 2>/dev/null || true
    scp -q -o ConnectTimeout=12 -o BatchMode=yes "$TAR" "$TARGET":~/drum-backup-$DATE.tar.gz 2>/dev/null || true
    if ssh -o ConnectTimeout=6 -o BatchMode=yes "$TARGET" "test -f ~/frameworks-drum/catalog.json" 2>/dev/null; then
      echo "$TARGET: drum pack + backup pushed OK"
    else
      echo "$TARGET: reachable but push incomplete"
    fi
  else
    echo "$TARGET: unreachable (skipped)"
  fi
done
echo "off-mac backup complete"
