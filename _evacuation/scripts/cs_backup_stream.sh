#!/bin/bash
# cs_backup_stream.sh — LaunchAgent-supervised backup of ~/.claude-science
# -> oracle-micro-2:/home/ubuntu/cs-backup/claude-science-full.tar.gz (root volume,
# 13G free, NOT the contested /evac-bulk). Pre-flight disk check fails loudly on
# short headroom (the silent-ENOSPC class killed earlier unsupervised streams).
# Marker file is written by a trap on ANY exit (0/42/SIGPIPE/SIGTERM) so remote
# monitors always see the verdict, even when the pipe is killed mid-flight.
set -uo pipefail
SRC=/Users/nicholas/.claude-science
REMOTE=oracle-micro-2
# BASE must be an ABSOLUTE remote path (no ~ — it expands LOCALLY otherwise)
BASE=/home/ubuntu/cs-backup
DEST=$BASE/claude-science-full.tar.gz
TMP=$BASE/claude-science-full.tar.gz.part
MARK=$BASE/claude-science-backup.status
NEED_MB=2500
RC=0
VER=PENDING

# Trap runs on ANY exit (incl SIGPIPE/SIGTERM). Writes remote marker + local state
# with the real exit code + verify verdict so monitors never have to guess.
on_exit() {
  local end; end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  # local state — always writable
  echo "{\"start\":\"$START\",\"end\":\"$end\",\"exit\":$RC,\"verify\":\"$VER\"}" > /tmp/cs_agent.state.json 2>/dev/null
  echo "BACKUP_AGENT_DONE end=$end exit=$RC verify=$VER" >> /tmp/cs_agent.state.json 2>/dev/null
  # remote marker — best-effort (ssh may also have died)
  ssh -o BatchMode=yes -o ConnectTimeout=5 "$REMOTE" \
    "echo '{\"end\":\"$end\",\"exit\":$RC,\"verify\":\"$VER\"}' > $MARK" 2>/dev/null || true
  # cleanup partial if we ended without verify
  if [ "$VER" != "VERIFIED" ]; then
    ssh -o BatchMode=yes -o ConnectTimeout=5 "$REMOTE" "rm -f $TMP" 2>/dev/null || true
  fi
}
trap on_exit EXIT INT TERM PIPE

START=$(date -u +%Y-%m-%dT%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"start\":\"$START\",\"state\":\"streaming\",\"dest\":\"$DEST\"}" > /tmp/cs_agent.state.json

# pre-flight: fail loudly rather than silently ENOSPC mid-stream
ssh -o BatchMode=yes -o ConnectTimeout=10 "$REMOTE" "mkdir -p $BASE" || { RC=$?; exit 40; }
FREE_MB=$(ssh -o BatchMode=yes -o ConnectTimeout=10 "$REMOTE" "df -m $BASE | tail -1 | awk '{print \$4}'")
if [ -z "${FREE_MB}" ] || [ "${FREE_MB}" -lt "${NEED_MB}" ]; then
  RC=42; VER="HEADROOM_FAIL_${FREE_MB:-0}MB"; exit 42
fi

tar --no-xattrs --exclude="*.sock" --exclude="*.socket" -czf - -C /Users/nicholas .claude-science 2>/tmp/cs_agent.tar.err \
 | ssh -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=12 "$REMOTE" \
     "cat > $TMP && mv $TMP $DEST && gzip -t $DEST && echo VERIFIED || echo NOTVERIFIED" \
 > /tmp/cs_agent.out.log 2>&1
RC=$?
VER=$(tail -1 /tmp/cs_agent.out.log 2>/dev/null | tr -d '\n' || echo "NO_OUTPUT")
exit $RC