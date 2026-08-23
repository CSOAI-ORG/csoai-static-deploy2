#!/bin/bash
# a100-bench-collector.sh — pull A100 axis-engine bench into estate + RAG volume.
# Fixes the orphaned-A100-output bug: A100 ($1.39/hr) produced /workspace/bench/
# but nothing collected it — measurements died on the pod.
# Run: nohup bash a100-bench-collector.sh > /tmp/a100-collect.out 2>&1 & disown
export PATH="/opt/homebrew/bin:$HOME/.local/node/bin:$HOME/.local/bin:$PATH"
KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
A100_PORT=23166
A100_IP=38.128.232.57
LOG=/tmp/a100-collect.log
STAGE="$HOME/clawd/_evacuation/runpod-bundles"
TS() { date +%H:%M:%S; }
mkdir -p "$STAGE"
echo "$(TS) a100-collector start (rsync now on pod)" >> "$LOG"

while true; do
  # 1. Keep the axis engine alive on the A100.
  ssh -i "$KEY" -p $A100_PORT -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 \
    root@$A100_IP 'pgrep -f axis-engine.sh >/dev/null || { cd /workspace && setsid nohup bash axis-engine.sh >> axis-engine.log 2>&1 < /dev/null & disown; echo RESTARTED; }' >> "$LOG" 2>&1

  # 2. Pull A100 bench -> Mac bundle (resumable).
  DEST="$STAGE/$(date +%Y%m%d)-a100bench"
  mkdir -p "$DEST"
  rsync -a --partial -e "ssh -i $KEY -p $A100_PORT -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10" \
    root@$A100_IP:/workspace/bench/ "$DEST/" >> "$LOG" 2>&1
  N=$(ls "$DEST"/*.jsonl 2>/dev/null | wc -l | tr -d ' ')
  echo "$(TS) a100 bench pulled: $N files" >> "$LOG"

  # 3. Mirror Mac bundle -> sink RAG volume (Mac has rsync; sink has rsync).
  ssh -i "$KEY" -p 25804 -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=8 \
    root@213.173.105.83 "mkdir -p /workspace/RAG/mac-migrate/a100-bench" >> "$LOG" 2>&1
  rsync -a --partial -e "ssh -i $KEY -p 25804 -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=8" \
    "$DEST/" "root@213.173.105.83:/workspace/RAG/mac-migrate/a100-bench/" >> "$LOG" 2>&1
  echo "$(TS) mirrored to RAG volume" >> "$LOG"

  # 4. Pull EAT-OOWM results (weak-dim evals + stack output) -> Mac + RAG.
  EDEST="$STAGE/$(date +%Y%m%d)-eatoowm"
  mkdir -p "$EDEST"
  rsync -a --partial -e "ssh -i $KEY -p $A100_PORT -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10" \
    root@$A100_IP:/workspace/eat/benchmark-results/ "$EDEST/" >> "$LOG" 2>&1
  NE=$(find "$EDEST" -type f 2>/dev/null | wc -l | tr -d ' ')
  [ "$NE" -gt 0 ] && rsync -a --partial -e "ssh -i $KEY -p 25804 -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=8" \
    "$EDEST/" "root@213.173.105.83:/workspace/RAG/mac-migrate/eat-results/" >> "$LOG" 2>&1
  echo "$(TS) eat-oowm pulled: $NE files -> RAG" >> "$LOG"

  sleep 900
done
