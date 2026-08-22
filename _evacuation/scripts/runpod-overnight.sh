#!/bin/bash
# runpod-overnight.sh — Mac-side overnight dispatcher (orchestration ONLY).
# Every 30 min: pushes the batch script to the 3090 pod + runs it there.
# At 04:00 local: pulls the results bundle back, merges into the living DB,
# signs, commits to the deploy repo, and lands a copy on the EU-RO-1 volume
# via croc when the volume-sink pod is up. All heavy compute stays on the pod.
# Log: ~/clawd/_evacuation/logs/runpod-overnight.log
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

LOG="$HOME/clawd/_evacuation/logs/runpod-overnight.log"
LOCK="$HOME/clawd/_evacuation/.runpod-overnight.lock"
mkdir -p "$(dirname "$LOG")" "$HOME/clawd/_evacuation/runpod-bundles"
TS() { date +%Y-%m-%d\ %H:%M:%S; }

# Self-healing lock: if the lock dir exists but is STALE (older than 30m OR the
# PID written in it is dead), reclaim it. This killed ~6h of pod idles (22 Aug
# 06:02→11:58) where every 15-min retry saw the lock and exited.
STALE=1800  # 30 min
if ! mkdir "$LOCK" 2>/dev/null; then
  LOCK_AGE=999999; LOCK_PID=0
  if [ -f "$LOCK/pid" ]; then
    LOCK_PID=$(cat "$LOCK/pid" 2>/dev/null || echo 0)
    LOCK_CTIME=$(stat -f %m "$LOCK" 2>/dev/null || stat -c %Y "$LOCK" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    LOCK_AGE=$(( NOW - LOCK_CTIME ))
  fi
  # stale if old, or the recorded PID is no longer alive
  PID_DEAD=1
  if [ "$LOCK_PID" -gt 0 ] 2>/dev/null && kill -0 "$LOCK_PID" 2>/dev/null; then PID_DEAD=0; fi
  if [ "$LOCK_AGE" -gt "$STALE" ] || [ "$PID_DEAD" -eq 1 ]; then
    echo "$(TS) stale lock (age ${LOCK_AGE}s, pid ${LOCK_PID:-none} dead) — reclaiming, will run now" >> "$LOG"
    rm -rf "$LOCK" 2>/dev/null
    mkdir "$LOCK" 2>/dev/null || { echo "$(TS) reclaim failed — exit" >> "$LOG"; exit 0; }
    echo "$$" > "$LOCK/pid" 2>/dev/null
  else
    echo "$(TS) another instance running (pid ${LOCK_PID}) — exit" >> "$LOG"; exit 0
  fi
else
  echo "$$" > "$LOCK/pid" 2>/dev/null
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

SSH_KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
# Auto-resolve the 3090 endpoint (drifts across pod restarts — 2026-08-22 fix).
POD_ID="fpowppss5ngtkw"   # sov-repull (3090)
_RUNPODCTL=$(command -v runpodctl || echo /opt/homebrew/bin/runpodctl)
RESOLVE=$($_RUNPODCTL ssh info "$POD_ID" 2>/dev/null | python3 -c "import json,sys
try:
    d=json.load(sys.stdin); print(d.get('ip',''),d.get('port',''))
except: print('ERROR')" 2>/dev/null)
POD_IP=$(echo "$RESOLVE" | awk '{print $1}')
POD_PORT=$(echo "$RESOLVE" | awk '{print $2}')
[ -z "$POD_IP" ] || [ -z "$POD_PORT" ] && { echo "$(TS) 3090 endpoint unresolved — aborting (will retry next tick)" >> "$LOG"; exit 0; }
POD="root@$POD_IP"; PORT="$POD_PORT"
SINK_IP="213.173.105.83"; SINK_PORT=25804
SSHO="-i $SSH_KEY -p $PORT -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10"
SCPO="-i $SSH_KEY -P $PORT -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10"
BATCH="$HOME/clawd/_evacuation/scripts/runpod-overnight-batch.sh"
STAGE="$HOME/clawd/_evacuation/runpod-bundles"

# ── 04:00 cutoff (next occurrence) ──
NOW_EPOCH=$(date +%s)
TODAY_0400=$(date -j -f "%Y-%m-%d %H:%M" "$(date +%Y-%m-%d) 04:00" +%s 2>/dev/null || date -d "$(date +%Y-%m-%d) 04:00" +%s 2>/dev/null)
if [ "$NOW_EPOCH" -lt "$TODAY_0400" ]; then STOP_EPOCH=$TODAY_0400; else STOP_EPOCH=$((TODAY_0400 + 86400)); fi
echo "$(TS) runpod-overnight window until $(date -r $STOP_EPOCH +%H:%M)" >> "$LOG"

while [ "$(date +%s)" -lt "$STOP_EPOCH" ]; do
  # pod reachable?
  if ! ssh $SSHO "$POD" 'echo OK' 2>>"$LOG" | grep -q OK; then
    echo "$(TS) pod unreachable — retry in 30m" >> "$LOG"
    sleep 1800; continue
  fi
  # push batch + run it
  scp $SCPO "$BATCH" "$POD":/workspace/overnight_batch.sh >> "$LOG" 2>&1
  ssh $SSHO "$POD" 'bash /workspace/overnight_batch.sh' >> "$LOG" 2>&1

  # pull results bundle (resumable: rsync --partial)
  mkdir -p "$STAGE/$(date +%Y%m%d)"
  /opt/homebrew/bin/rsync -a --partial -e "ssh $SSHO" "$POD":/workspace/overnight/out/ "$STAGE/$(date +%Y%m%d)/" >> "$LOG" 2>&1
  echo "$(TS) pulled: $(ls "$STAGE/$(date +%Y%m%d)" 2>/dev/null | tr '\n' ' ')" >> "$LOG"

  # ── volume sync: estate -> sovos-merge-800 (EU-RO-1 sink pod, auto-stops 04:30Z) ──
  if ssh -i "$SSH_KEY" -p "$SINK_PORT" -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=8 "root@$SINK_IP" 'echo OK' 2>>"$LOG" | grep -q OK; then
    SCP_SINK="-i $SSH_KEY -P $SINK_PORT -o StrictHostKeyChecking=no -o BatchMode=yes"
    SINK_SSH="ssh -i $SSH_KEY -p $SINK_PORT -o StrictHostKeyChecking=no -o BatchMode=yes root@$SINK_IP"
    $SINK_SSH 'mkdir -p /workspace/SOVOS/living /workspace/overnight-$(date +%Y%m%d)' >> "$LOG" 2>&1
    scp $SCP_SINK "$HOME/clawd/csoai-static-deploy2/SOVOS/living/board_living.json" \
        "$HOME/clawd/csoai-static-deploy2/SOVOS/living/goldbank_jail.json" \
        "$HOME/clawd/csoai-static-deploy2/SOVOS/living/kernel_results.jsonl" \
        "root@$SINK_IP:/workspace/SOVOS/living/" >> "$LOG" 2>&1
    scp $SCP_SINK "$STAGE/$(date +%Y%m%d)"/*.json* "root@$SINK_IP:/workspace/overnight-$(date +%Y%m%d)/" >> "$LOG" 2>&1
    echo "$(TS) volume sync: $(ls "$STAGE/$(date +%Y%m%d)" 2>/dev/null | wc -l | tr -d ' ') files -> sovos-merge-800" >> "$LOG"
  else
    echo "$(TS) volume sink unreachable — skip sync" >> "$LOG"
  fi

  # ── at 04:00 (final pass): merge + sign + commit ──
  if [ "$(date +%s)" -ge $((STOP_EPOCH - 300)) ]; then
    echo "$(TS) FINAL — merging + signing" >> "$LOG"
    # 1) merge gold verdict into living board (idempotent; reuses today's results)
    if [ -f "$STAGE/$(date +%Y%m%d)/gold_results.json" ]; then
      cp "$STAGE/$(date +%Y%m%d)/gold_results.json" /tmp/gold_results.json
      cd "$HOME/clawd/csoai-static-deploy2" && python3 SOVOS/merge_gold_verdict.py >> "$LOG" 2>&1
    fi
    # 1b) merge slot15 + human-vs-ai verdicts (from the pod measure pass)
    if [ -f "$STAGE/$(date +%Y%m%d)/axis_verdicts.json" ]; then
      cp "$STAGE/$(date +%Y%m%d)/axis_verdicts.json" /tmp/axis_verdicts.json
      cd "$HOME/clawd/csoai-static-deploy2" && python3 SOVOS/merge_axis_verdicts.py >> "$LOG" 2>&1
    fi
    # 1c) merge sim-world h3k cards into the living DB (training fuel)
    cd "$HOME/clawd/csoai-static-deploy2" && python3 SOVOS/merge_sim_cards.py >> "$LOG" 2>&1
    # 1d) harvest any completed rotation kernels (400-model scale waves)
    HARVEST_LOG="$HOME/clawd/_evacuation/logs/rot-harvest.log"
    for rot in 1 2 3 4; do
      for d in "$HOME/clawd/scripts/flywheel/multicluster-kernels-rot$rot"/kaggle-*; do
        [ -d "$d" ] || continue
        ax=$(basename "$d" | sed 's/kaggle-//')
        slug="owem-$ax-rot$rot"
        out=$(kaggle kernels output nicktempleman/$slug -p /tmp/kout_$slug 2>&1)
        if echo "$out" | grep -q "downloaded"; then
          echo "$(date +%H:%M) $slug downloaded" >> "$HARVEST_LOG"
        fi
      done
    done
    # 2) merge arena rounds into the signed_rounds archive
    ROUNDS="$STAGE/$(date +%Y%m%d)/reborn_rounds.jsonl"
    ARCHIVE="$HOME/clawd/csoai-static-deploy2/SOVOS/living/arena_reborn_$(date +%Y%m%d).jsonl"
    if [ -f "$ROUNDS" ] && [ ! -f "$ARCHIVE" ]; then
      cp "$ROUNDS" "$ARCHIVE" && echo "$(TS) arena rounds archived: $(wc -l < "$ARCHIVE")" >> "$LOG"
    fi
    # 3) commit by name (never git add -A — multi-lane repo)
    cd "$HOME/clawd/csoai-static-deploy2"
    git add SOVOS/living/board_living.json SOVOS/living/goldbank_jail.json \
            SOVOS/living/arena_reborn_$(date +%Y%m%d).jsonl SOVOS/merge_gold_verdict.py \
            SOVOS/merge_axis_verdicts.py SOVOS/merge_sim_cards.py SOVOS/living/kernel_results.jsonl \
            SOVOS/living/sim_cards.jsonl \
            forest/slot15.jsonl forest/human-vs-ai.jsonl 2>>"$LOG"
    git -c user.name="AEO Gap Fix Bot" -c user.email="nicholas@csoai.org" \
        commit -m "overnight: gold verdict + slot15/hvai verdicts signed + kernel cards + arena rounds ($(date -u +%Y-%m-%d))" >> "$LOG" 2>&1
    git push origin main >> "$LOG" 2>&1 || echo "$(TS) push failed (retry next pass)" >> "$LOG"
    # 4) push site bundle (living_board.ts + data) to the site repo
    cd "$HOME/councilof-ai-wt"
    git add functions/api/living_board.ts functions/api/data/board_living.json \
            functions/api/data/goldbank_jail.json 2>>"$LOG"
    git -c user.name="AEO Gap Fix Bot" -c user.email="nicholas@csoai.org" \
        commit -m "overnight: living board bundle (gold + slot15/hvai verdicts) $(date -u +%Y-%m-%d)" >> "$LOG" 2>&1
    git push origin feat/part-cj-sovereign-route-kill >> "$LOG" 2>&1 || echo "$(TS) site push failed" >> "$LOG"
    echo "$(TS) FINAL DONE — next window tomorrow" >> "$LOG"
  fi
  # 5) P7: auto-sync the latest h3k card to harness + pod (2026-08-18)
  bash "$HOME/clawd/scripts/p7-card-sync.sh" >> "$LOG" 2>&1

  echo "$(TS) pass complete — sleep 1800" >> "$LOG"
  sleep 1800
done
echo "===== runpod-overnight parked $(TS) (04:00 reached) =====" >> "$LOG"

# ── A100 axis-engine guard (2026-08-22): keep the 16-axis engine alive on the A100 ──
A100_ID="l7g747oivyq6ab"   # sovos-light-master-mine (A100 80GB)
A100_RES=$($_RUNPODCTL ssh info "$A100_ID" 2>/dev/null | python3 -c "import json,sys
try:
    d=json.load(sys.stdin); print(d.get('ip',''),d.get('port',''))
except: print('ERROR')" 2>/dev/null)
A100_IP=$(echo "$A100_RES" | awk '{print $1}')
A100_PORT=$(echo "$A100_RES" | awk '{print $2}')
if [ -n "$A100_IP" ] && [ -n "$A100_PORT" ]; then
  A100_SSH="-i $SSH_KEY -p $A100_PORT -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10"
  # Start ollama + axis engine if not running on the A100
  ssh $A100_SSH root@$A100_IP 'pgrep -x ollama >/dev/null || { setsid nohup /usr/local/bin/ollama serve > /tmp/ollama-serve.log 2>&1 < /dev/null & disown; sleep 4; }; pgrep -f axis-engine >/dev/null || { setsid nohup bash /workspace/axis-engine.sh > /dev/null 2>&1 < /dev/null & disown; echo "$(date -u +%FT%TZ) axis engine auto-restarted"; }' 2>/dev/null \
    && echo "$(TS) A100 axis engine guarded (alive or restarted)" >> "$LOG"
fi
