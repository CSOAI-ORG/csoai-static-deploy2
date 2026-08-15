#!/bin/bash
# until-6am-watchdog.sh — keep the overnight loop alive (runs every 5 min via cron).
# Restarts until-6am-eat-all.sh if it is not running. Safe to run repeatedly.
LOG=/tmp/until-6am-watchdog.log
LOOP=/Users/nicholas/clawd/csoai-static-deploy2/until-6am-eat-all.sh
HERE=/Users/nicholas/clawd/csoai-static-deploy2

# If any until-6am loop is already running, do nothing.
if pgrep -f "until-6am-eat-all.sh" >/dev/null 2>&1; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] loop alive — no action" >> "$LOG"
    exit 0
fi

# 6am local guard: do not restart after 06:30 local.
HOUR=$(date +%H)
if [ "$HOUR" -ge 6 ] && [ "$HOUR" -lt 12 ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] past 6am window — not restarting" >> "$LOG"
    exit 0
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] loop DEAD — restarting" >> "$LOG"
cd "$HERE"
nohup bash "$LOOP" >> /tmp/sovereign-until-6am.log 2>&1 &
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] restarted pid $!" >> "$LOG"
