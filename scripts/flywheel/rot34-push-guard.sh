#!/bin/bash
# rot34-push-guard — relaunches the rot4 Kaggle push loop if it dies.
# pgrep-based: any running resume_rot34 instance satisfies liveness (pidfile
# went stale and caused duplicate-loop 429 storms on 2026-08-21).
LOG="$HOME/clawd/scripts/flywheel/rot34-push.log"

# 1. if ANY loop instance is alive, done (pgrep — no stale pidfile races)
if pgrep -f "resume_rot34_push.sh" > /dev/null 2>&1; then
  exit 0
fi

# 2. if log says "resume done" recently, loop finished — don't restart
if [ -f "$LOG" ] && grep -q "rot4 resume done" "$LOG" && [ $(( $(date +%s) - $(stat -f %m "$LOG") )) -lt 86400 ]; then
  exit 0
fi

# 3. relaunch exactly one
nohup bash "$HOME/clawd/scripts/flywheel/resume_rot34_push.sh" >> /tmp/rot34-nohup.log 2>&1 &
echo "$(date -u +%H:%M) guard relaunched rot4 loop pid $!" >> "$LOG"
