#!/usr/bin/env bash
# syncp.sh — SYNC with PROOF (the md5-fail-loud pattern).
#
# Fixes the silent-sync-failure class: scp/tar that "succeeds" while
# delivering stale bytes. Every pull asserts per-file md5 against the
# remote BEFORE reporting success. No hash, no claim.
#
# Usage:
#   syncp.sh pull  <remote-path> <local-dir> [ssh-host:port]   (default root@104.255.9.187:11703)
#   syncp.sh push  <local-path> <remote-dir> [ssh-host:port]
#   syncp.sh verify <local-path> <remote-path> [ssh-host:port]
set -euo pipefail

SSH_DEF="root@104.255.9.187:11703"
CMD="${1:?usage: syncp.sh pull|push|verify <src> <dst> [host:port]}"
SRC="${2}"; DST="${3}"
HOSTPORT="${4:-$SSH_DEF}"
HOST="${HOSTPORT%%:*}"; PORT="${HOSTPORT##*:}"

echo "=== syncp $CMD $SRC -> $DST ($HOST:$PORT) ==="

case "$CMD" in
  pull)
    mkdir -p "$DST"
    # remote md5 for every file we're about to pull (fail loud if bulk)
    REMOTE_LIST=$(ssh -p "$PORT" -o ConnectTimeout=20 -o BatchMode=yes "$HOST" \
      "cd $SRC 2>/dev/null && md5sum * 2>/dev/null || echo MISSING:$SRC")
    if echo "$REMOTE_LIST" | grep -q "MISSING:"; then
      echo "✗ remote dir not found"; exit 1
    fi
    scp -P "$PORT" -o ConnectTimeout=20 -o BatchMode=yes \
      "$HOST:$SRC/"* "$DST/" 2>&1 | grep -v "^Total\|^  \|Speed" | head -5 || true
    # verify each local file matches remote md5 (fail loud)
    FAIL=0
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      RHASH=$(echo "$line" | awk '{print $1}')
      RFILE=$(echo "$line" | awk '{print $2}')
      LHASH=$(md5 -q "$DST/$RFILE" 2>/dev/null || echo MISSING)
      if [ "$RHASH" != "$LHASH" ]; then
        echo "  ✗ MISMATCH $RFILE: remote=$RHASH local=$LHASH"; FAIL=1
      else
        echo "  ✓ $RFILE hash-verified"
      fi
    done <<< "$REMOTE_LIST"
    if [ "$FAIL" -eq 1 ]; then echo "=== ✗ PULL FAILED — stale bytes detected ==="; exit 1; fi
    echo "=== ✓ PULL VERIFIED (all $(echo "$REMOTE_LIST" | wc -l | tr -d ' ') files md5-matched) ==="
    ;;
  push)
    # push then pull-back md5 to verify (roundtrip proof)
    scp -P "$PORT" -o ConnectTimeout=20 -o BatchMode=yes "$SRC" "$HOST:$DST/" 2>&1 | grep -v "^stating" | head -3 || true
    B=$(basename "$SRC")
    RHASH=$(ssh -p "$PORT" -o ConnectTimeout=20 -o BatchMode=yes "$HOST" "md5sum $DST/$B | awk '{print \$1}'")
    LHASH=$(md5 -q "$SRC")
    if [ -z "$RHASH" ] || [ "$RHASH" != "$LHASH" ]; then
      echo "  ✗ PUSH MISMATCH remote=$RHASH local=$LHASH"; exit 1
    fi
    echo "  ✓ pushed $B (md5 $LHASH) remote-verified"
    ;;
  verify)
    B=$(basename "$SRC")
    RHASH="$(ssh -p "$PORT" -o ConnectTimeout=20 -o BatchMode=yes "$HOST" "md5sum $DST/$B 2>/dev/null | awk '{print \$1}'" 2>/dev/null || echo MISSING)"
    L=$(md5 -q "$SRC" 2>/dev/null || echo MISSING)
    echo "  remote=$RHASH"; echo "  local =$L"
    [ "$RHASH" = "$L" ] && { echo "=== ✓ HASH-MATCH ==="; exit 0; } || { echo "=== ✗ MISMATCH ==="; exit 1; }
    ;;
  *) echo "usage: pull|push|verify"; exit 1;;
esac