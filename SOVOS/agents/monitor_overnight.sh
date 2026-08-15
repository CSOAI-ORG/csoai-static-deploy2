#!/bin/bash
# monitor_overnight.sh — watch both A100 pods through the night, write ONE
# digest at 07:00 UTC (Monday morning) for the impact report.
# Usage: nohup bash monitor_overnight.sh > /tmp/monitor-overnight.log 2>&1 &

POD1="root@104.255.9.187 -p 11703"   # main A100 — LEG S/J/F
POD2="root@104.255.9.187 -p 11628"   # bench A100 v2 — board + sov6 rebuild

LOG=/tmp/overnight-digest.md
echo "# Overnight Bench Digest — $(date -u +%FT%TZ)" > "$LOG"

for i in $(seq 1 420); do   # poll every 2 min up to 14h
  TS=$(date -u +%FT%TZ)
  S1=$(ssh $P1 'pgrep -fc overnight_bench 2>/dev/null || echo 0' 2>/dev/null)
  S2=$(ssh $P2 'pgrep -fc overnight_bench 2>/dev/null || echo 0' 2>/dev/null)
  # capture results each cycle
  R1=$(ssh $P1 'ls /workspace/overnight-bench-2026-08-16/ 2>/dev/null | wc -l' 2>/dev/null)
  R2=$(ssh $P2 'ls /workspace/overnight-bench-2026-08-16/ 2>/dev/null | wc -l' 2>/dev/null)
  B2=$(ssh $P2 'ollama list 2>/dev/null | wc -l' 2>/dev/null)
  if [ "$(date -u +%H%M)" = "0700" ] || [ $i = 420 ]; then
    {
      echo "## final: pod1 bench=$S1 results=$R1 | pod2 bench=$S2 results=$R2 models=$B2"
      echo "### POD1 tail:"
      ssh $P1 'tail -20 /tmp/overnight-bench.log 2>/dev/null' 2>/dev/null
      echo "### POD2 tail:"
      ssh $P2 'tail -10 ~/sov6-build.log 2>/dev/null' 2>/dev/null
      echo "### boards (main):"
      ssh $P1 'python3 -c "import json,glob; [print(f.split(\"/\")[-1], json.load(open(f)).get(\"status\")) for f in glob.glob(\"/workspace/csoai-static-deploy2/SOVOS/boards-v2-2026-08-12/board_*.json\")]" 2>/dev/null | tail -14' 2>/dev/null
    } >> $LOG
    echo "DIGEST READY at $TS — see $LOG"
    exit 0
  fi
  sleep 120
done