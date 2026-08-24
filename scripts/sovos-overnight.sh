#!/bin/bash
# sovos-overnight — overnight autonomous driver (Mac side, cron/launchd supervised)
# 1) grow corpus via live teacher distillation (deepseek tier-1 + local policy teachers)
# 2) catch-up rsync to volume mirror (corpus + docs)
# 3) trigger retrain on pod via marker (pod watchdog executes it)
LOG=~/clawd/_alignment/overnight.log
STAMP=$(date -u +%Y-%m-%dT%H:%M:%S)
echo "[$STAMP] overnight pass start" >> $LOG

cd ~/clawd
python3 distill_multi.py --tasks 12 --temps 3 >> $LOG 2>&1
python3 distill_corpus.py >> $LOG 2>&1

# corpus size after passes
N=$(python3 -c "import json;print(len(json.load(open('/Users/nicholas/clawd/csoai-static-deploy2/sov_grpo_training_data.json'))))" 2>/dev/null)
echo "[$STAMP] corpus=$N" >> $LOG

# catch-up sync (quick)
/opt/homebrew/bin/rsync -a --partial -e "ssh -F /dev/null -p 25804 -i ~/.runpod/ssh/runpodctl-ssh-key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=15" \
  ~/clawd/csoai-static-deploy2/sov_grpo_training_data.json ~/clawd/sovereign-distill-corpus.jsonl \
  root@213.173.105.83:/workspace/offload-dsh/clawd/csoai-static-deploy2/ >> $LOG 2>&1

# also refresh harness copy (git working tree) for the pod trainer
/opt/homebrew/bin/rsync -a --partial -e "ssh -F /dev/null -p 25804 -i ~/.runpod/ssh/runpodctl-ssh-key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=15" \
  ~/clawd/csoai-static-deploy2/sov_grpo_training_data.json \
  root@213.173.105.83:/workspace/sovos-harness/csoai-static-deploy2/ >> $LOG 2>&1

# weights (v3) to volume archive if present
if [ -d ~/clawd/csoai-static-deploy2/sov-minimal-output-v3 ]; then
  /opt/homebrew/bin/rsync -a --partial -e "ssh -F /dev/null -p 25804 -i ~/.runpod/ssh/runpodctl-ssh-key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=15" \
    ~/clawd/csoai-static-deploy2/sov-minimal-output-v3/ root@213.173.105.83:/workspace/offload-dsh/clawd/csoai-static-deploy2/sov-minimal-output-v3/ >> $LOG 2>&1
  echo "[$STAMP] v3 weights synced" >> $LOG
fi

# trigger retrain on pod (pod watchdog trains if marker present)
ssh -F /dev/null -p 25804 -i ~/.runpod/ssh/runpodctl-ssh-key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=12 root@213.173.105.83 \
  'touch /workspace/retrain-needed; echo retrain-marker-set' >> $LOG 2>&1

# POD KILLS CPU-HEAVY TRAINING (verified: SIGKILL in 25s, no OOM trace) -> train on MAC, weights -> volume.
TR=~/clawd/csoai-static-deploy2
if ! pgrep -f sov_minimal_train >/dev/null 2>&1; then
  # auto-version: next vN after the highest existing sov-minimal-output-vN
  V=3
  for n in 2 3 4 5 6 7 8; do [ -d "$TR/sov-minimal-output-v$n" ] && V=$((n+1)); done
  nohup bash -c "cd $TR && /tmp/sovtrain/bin/python sov_minimal_train.py --steps 150 --output sov-minimal-output-v$V >> ~/clawd/_alignment/train-v$V.log 2>&1 && /tmp/sovtrain/bin/python ~/clawd/eval_student.py $TR/sov-minimal-output-v$V >> ~/clawd/_alignment/eval-v$V.log 2>&1" >> $LOG 2>&1 &
  echo "[$STAMP] mac train v$V launched" >> $LOG
fi
echo "[$STAMP] overnight pass done (corpus=$N)" >> $LOG
