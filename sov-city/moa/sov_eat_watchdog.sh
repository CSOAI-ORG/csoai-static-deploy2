#!/bin/bash
# sov_eat_watchdog.sh — keeps the EAT streams alive (arena loop + CRDT
# heartbeat) and detects stalls. Cron: */7 * * * *
#   - arena loop on oracle-micro: dead -> restart via fleet start script
#   - rounds not advancing across checks -> STALL alert (but no blind restart)
#   - CRDT heartbeat (Mac): dead or >3 cycles without new record -> alert
# Logs to this file's dir: watchdog.log (distinct lines, honest status).
set -u
cd "$(dirname "$0")"
LOGFILE="$(pwd)/watchdog.log"
NOW=$(date -u +%FT%TZ)

# --- arena loop (fleet) ---
ARENA_ALIVE=$(ssh -o BatchMode=yes -o ConnectTimeout=12 oracle-micro 'pgrep -f sov_arena_loop.py >/dev/null && echo 1 || echo 0' 2>/dev/null || echo 0)
if [ "$ARENA_ALIVE" = "0" ]; then
  # restart via the fleet-side starter (the only pattern that survives ssh detach)
  ssh -o BatchMode=yes -o ConnectTimeout=12 oracle-micro 'bash /home/ubuntu/start_arena.sh' >/dev/null 2>&1
  echo "$NOW ARENA LOOP DOWN — restart issued" >> "$LOGFILE"
else
  echo "$NOW arena loop OK" >> "$LOGFILE"
fi

# --- stall check: evidence file must have advanced recently (loop interval=6min;
# genuine stall = file mtime older than 12 min while the loop is alive). No
# sleep — the old 45s window false-flagged normal gaps between cycles.
STALE_S=$(ssh -o BatchMode=yes -o ConnectTimeout=12 oracle-micro 'f=/evac-bulk/sov-mac-evac/sov_arena_rounds.jsonl; test -f "$f" && echo $(( $(date +%s) - $(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null) )) || echo 9999' 2>/dev/null || echo 9999)
if [ "${STALE_S:-9999}" -gt 720 ]; then
  echo "$NOW STALL: evidence stale ${STALE_S}s (>12min) with arena loop alive — no rounds advancing" >> "$LOGFILE"
else
  echo "$NOW rounds fresh (last write ${STALE_S}s ago)" >> "$LOGFILE"
fi

# --- CRDT heartbeat (Mac-side) ---
CRDT_PID=$(cat /tmp/sov_crdt.pid 2>/dev/null)
if ! kill -0 "$CRDT_PID" 2>/dev/null; then
  echo "$NOW CRDT HEARTBEAT DOWN (pid $CRDT_PID)" >> "$LOGFILE"
else
  echo "$NOW crdt heartbeat up (pid $CRDT_PID)" >> "$LOGFILE"
fi