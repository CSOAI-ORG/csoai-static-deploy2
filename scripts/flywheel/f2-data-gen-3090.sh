#!/bin/bash
# F2 Data Flywheel — nightly synthetic-pair generation on the 3090 (quiet window).
# Copies the generator to the pod, runs it backgrounded with nohup, records the pid.
set -uo pipefail
SSH_KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
POD="root@194.26.196.156"
PORT=23243
LOG="$HOME/clawd/_evacuation/logs/f2-data-gen.log"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
mkdir -p "$(dirname "$LOG")"
GEN="$HOME/clawd/scripts/flywheel/f2_gen.py"

echo "$TS F2 start" >> "$LOG"

# 1. Pod reachable?
if ! ssh -i "$SSH_KEY" -p "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 "$POD" 'echo OK' 2>>"$LOG" | grep -q OK; then
  echo "$TS F2 pod unreachable — skip" >> "$LOG"
  exit 1
fi

# 2. Already running? Don't double-fire.
if ssh -i "$SSH_KEY" -p "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes "$POD" 'pgrep -f f2_gen.py >/dev/null && echo RUNNING' 2>>"$LOG" | grep -q RUNNING; then
  echo "$TS F2 already running — skip" >> "$LOG"
  exit 0
fi

# 3. Copy generator + launch backgrounded
scp -i "$SSH_KEY" -P "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes "$GEN" "$POD":/workspace/f2_gen.py >> "$LOG" 2>&1
ssh -i "$SSH_KEY" -p "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes "$POD" \
  'cd /workspace && nohup python3 f2_gen.py 400 > f2_run.log 2>&1 & echo "F2 pid $!"' >> "$LOG" 2>&1

echo "$TS F2 launched (400 rows target)" >> "$LOG"
tail -1 "$LOG"

# ─── Dark-axis item factory (det/swarm/art5/mcp) — same pod, same quiet window ───
scp -i "$SSH_KEY" -P "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes \
  "$HOME/clawd/scripts/flywheel/f2_dark_axis_items.py" "$POD":/workspace/f2_dark_axis_items.py >> "$LOG" 2>&1
ssh -i "$SSH_KEY" -p "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes "$POD" \
  'cd /workspace && nohup python3 f2_dark_axis_items.py 40 > f2_dark.log 2>&1 & echo "dark-axis pid $!"' >> "$LOG" 2>&1
echo "$TS dark-axis items launched (40 targets)" >> "$LOG"
