#!/bin/bash
# mac-drain-to-pod.sh — detach-migrate heavy Mac data to the RunPod RAG volume.
# Resilient: retries each dir (max 5 attempts), resumable (--partial), logs.
# Run: nohup bash mac-drain-to-pod.sh > /tmp/mac-drain.out 2>&1 & disown
export PATH="/opt/homebrew/bin:$PATH"
KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
PORT=25804
LOG=/tmp/mac-drain.log
DEST="/workspace/RAG/mac-migrate"
TS() { date +%H:%M:%S; }

sync_dir() { # $1=local $2=pod-target
  local src="$1" tgt="$2" attempt=0
  while [ $attempt -lt 5 ]; do
    attempt=$((attempt+1))
    echo "$(TS) SYNC[$attempt] $src -> $tgt" >> "$LOG"
    rsync -az --partial --inplace \
      -e "ssh -i $KEY -p $PORT -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 -o ServerAliveInterval=20 -o ServerAliveCountMax=3" \
      "$src/" "root@213.173.105.83:$tgt/" >> "$LOG" 2>&1
    local rc=$?
    if [ $rc -eq 0 ]; then
      echo "$(TS) OK $src (attempt $attempt)" >> "$LOG"
      return 0
    fi
    echo "$(TS) RETRY $src rc=$rc (attempt $attempt)" >> "$LOG"
    sleep 5
  done
  echo "$(TS) FAILED $src after 5 attempts" >> "$LOG"
}

echo "$(TS) ===== MAC DRAIN START =====" >> "$LOG"
sync_dir "$HOME/clawd/csoai-static-deploy2/mlx_models"         "$DEST/mlx-models"
sync_dir "$HOME/clawd/csoai-static-deploy2/mlx_adapters"       "$DEST/mlx-adapters"
sync_dir "$HOME/clawd/csoai-static-deploy2/sov-hive"           "$DEST/sov-hive"
sync_dir "$HOME/clawd/csoai-static-deploy2/benchmark-results"  "$DEST/benchmark-results"
sync_dir "$HOME/clawd/csoai-static-deploy2/forest"             "$DEST/forest"
sync_dir "$HOME/clawd/csoai-static-deploy2/training_data"      "$DEST/training-data"
sync_dir "$HOME/clawd/agentsociety"                            "$DEST/projects/agentsociety"
sync_dir "$HOME/clawd/oowm-v8-e2e"                             "$DEST/projects/oowm-v8-e2e"
sync_dir "$HOME/clawd/meok-oneos"                              "$DEST/projects/meok-oneos"
sync_dir "$HOME/clawd/mcp-marketplace"                         "$DEST/projects/mcp-marketplace"
sync_dir "$HOME/clawd/sov-town-llm"                            "$DEST/projects/sov-town-llm"
echo "$(TS) ===== MAC DRAIN COMPLETE =====" >> "$LOG"
