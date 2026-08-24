#!/bin/bash
# sovos-train-v3 — run as its own launchd service (survives /tmp purges + session reaping)
# Permanent venv at ~/clawd/.venv-sovtrain (python3.11, torch 2.8.0, transformers 4.57.6).
TR=/Users/nicholas/clawd/csoai-static-deploy2
LOG=/Users/nicholas/clawd/_alignment/train-v3.log
cd "$TR" || exit 2
export OMP_NUM_THREADS=4
/Users/nicholas/clawd/.venv-sovtrain/bin/python -u sov_minimal_train.py --steps 150 --output sov-minimal-output-v3 >> "$LOG" 2>&1
RC=$?
echo "TRAIN_RC=$RC at $(date -u)" >> "$LOG"
# eval chain (same permanent venv)
/Users/nicholas/clawd/.venv-sovtrain/bin/python /Users/nicholas/clawd/eval_student.py "$TR/sov-minimal-output-v3" >> /Users/nicholas/clawd/_alignment/eval-v3.log 2>&1
echo "EVAL_DONE at $(date -u)" >> /Users/nicholas/clawd/_alignment/eval-v3.log
exit $RC
