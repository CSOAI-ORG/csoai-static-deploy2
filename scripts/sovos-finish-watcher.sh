#!/bin/bash
# sovos-finish-watcher — runs ON pod: waits for mirror to stabilize, then rebuilds the
# harness git repo, pushes to GitHub, launches training + proof EAT. Autonomous finish.
LOG=/workspace/eat-logs/finish-watcher.log
M=/workspace/offload-dsh/clawd
H=/workspace/sovos-harness

for round in 1 2 3 4 5 6 7 8 9 10 11 12; do
  S1=$(du -sm $M 2>/dev/null | cut -f1)
  sleep 600
  S2=$(du -sm $M 2>/dev/null | cut -f1)
  echo "[$(date -u +%H:%M:%S)] round $round: mirror ${S1}M -> ${S2}M" >> $LOG
  if [ "$S1" = "$S2" ]; then
    echo "[$(date -u +%H:%M:%S)] mirror stable at ${S2}M -> rebuild" >> $LOG
    bash /workspace/sovos-harness-rebuild.sh >> $LOG 2>&1
    cd $H/csoai-static-deploy2
    nohup /workspace/offload-dsh/eatenv/bin/python sov_minimal_train.py --steps 150 \
      --output sov-minimal-output-v2 >> /workspace/eat-logs/train-v2.log 2>&1 &
    nohup /workspace/sovos-eat.sh >> /workspace/eat-logs/proof-eat-$(date -u +%Y%m%d-%H%M).log 2>&1 &
    echo "[$(date -u +%H:%M:%S)] FINISH_DONE" >> $LOG
    exit 0
  fi
done
echo "[$(date -u +%H:%M:%S)] WATCHER_TIMEOUT (12 rounds = 2h; mirror still moving)" >> $LOG
exit 1
