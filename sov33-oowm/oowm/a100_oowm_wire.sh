#!/bin/bash
# a100_oowm_wire.sh — wire the OOWM estate-mine + Grok referee onto A100-1 on reconnect.
# Runs from the 3090. Degrades gracefully: polls until A100 answers, then syncs
# the sov33-oowm code + estate-mine index and starts the grok referee keeper +
# MCP server there. Safe to run repeatedly (idempotent).
set -u
A100="root@104.255.9.187"
KEY=/root/.ssh/id_runpod
PORT=11703
LOG=/workspace/arena-24x7/a100_oowm_wire.log
FLAG=/workspace/a100_oowm_wired.flag

echo "=== [wire] A100 OOWM wiring starting $(date -u +%H:%M:%S) ===" >> "$LOG"
[ -f "$FLAG" ] && { echo "already wired — skipping ($(date -u +%H:%M:%S))" >> "$LOG"; exit 0; }

for i in $(seq 1 120); do
  if ssh -i "$KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=6 -p $PORT $A100 "echo A100-ALIVE" 2>/dev/null | grep -q ALIVE; then
    echo "A100 reachable at attempt $i ($(date -u +%H:%M:%S))" >> "$LOG"
    # 1. ensure code exists
    ssh -i "$KEY" -o StrictHostKeyChecking=no -p $PORT $A100 "mkdir -p /workspace/sov33-oowm" || continue
    # 2. sync estate-mine OOWM code + index (skip heavy blobs)
    rsync -az --exclude __pycache__ --exclude "*.pyc" \
      -e "ssh -i $KEY -o StrictHostKeyChecking=no -p $PORT" \
      /workspace/sov33-oowm/oowm/ $A100:/workspace/sov33-oowm/oowm/ || echo "rsync failed — retry next cycle" >> "$LOG"
    # 2b. sync referee keys (groq + or) so the A100 referee can measure immediately
    for kf in groq.key or.key; do
      [ -f "/workspace/$kf" ] && scp -i "$KEY" -o StrictHostKeyChecking=no -P $PORT "/workspace/$kf" "$A100:/workspace/$kf" 2>/dev/null
    done
    # 3. verify index boots
    if ssh -i "$KEY" -o StrictHostKeyChecking=no -p $PORT $A100 "cd /workspace/sov33-oowm && python3 -c 'import sys; sys.path.insert(0,\".\"); from oowm.knowledge import OOWMIndex; ix=OOWMIndex.load(\"oowm/index/estate_mine_index.json\"); print(\"MINE_OK\", ix.stats()[\"docs\"])' 2>/dev/null" | grep -q MINE_OK; then
      echo "estate-mine index verified on A100 ($(date -u +%H:%M:%S))" >> "$LOG"
    else
      echo "index NOT verified on A100 — leaving retry-able ($(date -u +%H:%M:%S))" >> "$LOG"
      sleep 30
      continue
    fi
    # 4. start grok referee keeper on A100 (if not running)
    ssh -i "$KEY" -o StrictHostKeyChecking=no -p $PORT $A100 "pgrep -f grok_referee_keeper >/dev/null || (cd /workspace && nohup python3 /workspace/sov33-oowm/oowm/grok_referee_keeper.py > /workspace/arena-24x7/grok_referee_keeper.log 2>&1 &)" 2>/dev/null
    # 5. mark wired
    touch "$FLAG"
    echo "=== [wire] A100 OOWM WIRED $(date -u +%H:%M:%S) ===" >> "$LOG"
    exit 0
  fi
  [ $((i % 20)) -eq 0 ] && echo "attempt $i still flapping ($(date -u +%H:%M:%S))" >> "$LOG"
  sleep 15
done
echo "=== [wire] gave up after 120 attempts ($(date -u +%H:%M:%S)) — will re-arm ===" >> "$LOG"
exit 1
