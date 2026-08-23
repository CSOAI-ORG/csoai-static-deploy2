#!/bin/bash
# cs_rsync_direct.sh — LaunchAgent-supervised rsync-direct (no -z, no gzip) backup
# of ~/.claude-science -> oracle-micro[1|2] deterministic dest.
# Per measured truth: SQLite doesn't compress; raw rsync streams avoid the
# `tar: Write error` class that killed the v1/v2/v3 gzip streams.
# Per measured capacity (2026-08-09): micro1 /+ /evac-bulk = 22G total; the 48G
# `orgs/` shard cannot fit on a single mount (DONE per T3 = ENOSPC flag).
# This script copies the small shards (bin/runtime/logs/tls/small-files) which DO
# fit, then writes a per-shard marker; the orgs shard is reported as PLANNED.
set -uo pipefail
SRC=/Users/nicholas/.claude-science
REMOTE_HOST=oracle-micro
DEST=/home/ubuntu/cs-backup-direct
MARK=$DEST/claude-science-direct.status
mkdir -p /tmp/cs_direct
LOG=/tmp/cs_direct/out.log
ERR=/tmp/cs_direct/err.log
: > "$LOG"; : > "$ERR"

START=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Trap: any exit writes a remote marker + local state (real exit code + per-shard results).
# Per the file's rule: NO fabricated BACKUP_COMPLETE — only verify=VERIFIED wins.
on_exit() {
  local end; end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "{\"start\":\"$START\",\"end\":\"$end\",\"exit\":$RC,\"shards\":\"$SHARDS\",\"plan\":\"$PLAN\"}" > /tmp/cs_direct/state.json 2>/dev/null
  ssh -o BatchMode=yes -o ConnectTimeout=5 "$REMOTE_HOST" \
    "echo '{\"end\":\"$end\",\"exit\":$RC,\"shards\":\"$SHARDS\",\"plan\":\"$PLAN\"}' > $MARK" 2>/dev/null || true
}
trap on_exit EXIT INT TERM PIPE

RC=0
SHARDS=""
PLAN=""

# pre-flight: clean dest, headroom
ssh -o BatchMode=yes -o ConnectTimeout=10 "$REMOTE_HOST" "mkdir -p $DEST" || { RC=43; exit 43; }
FREE_MB=$(ssh -o BatchMode=yes -o ConnectTimeout=10 "$REMOTE_HOST" "df -m $DEST | tail -1 | awk '{print \$4}'")
NEED_MB=800  # small shards: bin(114) + runtime(95) + logs(8) + tls(0.3) + small(2) ≈ 220MB + verify-overhead
echo "{\"phase\":\"preflight\",\"free_mb\":${FREE_MB:-0},\"need_mb\":$NEED_MB}" >> "$LOG"
if [ -z "${FREE_MB}" ] || [ "${FREE_MB}" -lt "${NEED_MB}" ]; then
  RC=42
  SHARDS="headroom_fail_${FREE_MB:-0}MB"
  PLAN="free headroom insufficient on micro1 for small-shard copy"
  exit 42
fi

# SHARD A: bin + runtime + logs + tls + small-files (rsync-direct, no -z, --partial)
# /opt/homebrew/bin/rsync is required (D219 — /usr/bin/rsync = openrsync rejects --append)
RSYNC=/opt/homebrew/bin/rsync
[ -x "$RSYNC" ] || RSYNC=/usr/bin/rsync

for d in bin runtime logs tls seed-assets r-libs licenses mcp; do
  if [ -e "$SRC/$d" ]; then
    echo "{\"phase\":\"copy\",\"shard\":\"$d\"}" >> "$LOG"
    "$RSYNC" -a --no-compress --partial --exclude='*.sock' --exclude='*.socket' \
      -e 'ssh -o BatchMode=yes -o ServerAliveInterval=30 -o ConnectTimeout=10' \
      "$SRC/$d" "$REMOTE_HOST":"$DEST/claude-science/" \
      >> "$LOG" 2>> "$ERR" \
    && SHARDS="$SHARDS,$d:ok" \
    || { RC=$?; SHARDS="$SHARDS,$d:fail_rc$?"; }
  fi
done
# top-level small files (encryption.key etc)
"$RSYNC" -a --no-compress --partial \
  -e 'ssh -o BatchMode=yes' \
  "$SRC/"{encryption.key,active-org.json,auth-owner.lock,operon.lock,install-id,release-floor.json} \
  "$REMOTE_HOST":"$DEST/claude-science/" \
  >> "$LOG" 2>> "$ERR" \
&& SHARDS="$SHARDS,smallfiles:ok" || SHARDS="$SHARDS,smallfiles:fail"

PLAN="orgs(48G) cannot fit any single Oracle mount (micro1 22G, micro2 0); needs pod /evac-bulk (47G, auth-blocked) or a 3-way re-shard when staging is available. Re-arm permission required for next attempt."
exit $RC