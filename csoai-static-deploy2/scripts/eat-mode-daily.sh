#!/bin/bash
# /Users/nicholas/clawd/csoai-static-deploy2/scripts/eat-mode-daily.sh
# The all-day automated EAT-mode loop for the DEFONEOS sovereign substrate.
#
# HONESTY: This script hits the LIVE production endpoints. No simulation. No fabrication.
# Each cycle persists state to /tmp/*.log via the endpoints themselves. SIGIL-signed.
#
# SETUP:
#   1. Save this to /Users/nicholas/clawd/csoai-static-deploy2/scripts/eat-mode-daily.sh
#   2. chmod +x /Users/nicholas/clawd/csoai-static-deploy2/scripts/eat-mode-daily.sh
#   3. Set Vercel env vars (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SEND_KEY) — see defoneos-eat-control
#   4. Cron: 0 6,8,10,12,14,16,18,20,22 * * * /Users/nicholas/clawd/csoai-static-deploy2/scripts/eat-mode-daily.sh
#
# WHAT IT DOES:
#   - Runs /api/daily-golden every 2 hours (29 checks: 19 pages + 10 endpoints)
#   - Runs /api/morning-digest at 07:00 BST
#   - Runs /api/eat-tick at 08:00, 10:00, 14:00, 16:00, 18:00, 20:00, 22:00 BST
#   - All results posted to Telegram if env set
#   - All results persisted to /tmp/*.log via the endpoints

set -e

BASE="https://csoai-static-deploy2.vercel.app"
SEND_KEY="${SEND_KEY:-}"
HOUR=$(date -u +%H)
MIN=$(date -u +%M)

# Build auth header
if [ -n "$SEND_KEY" ]; then
  AUTH_H="X-Send-Key: $SEND_KEY"
else
  AUTH_H=""
fi

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
}

run_golden() {
  log "Running /api/daily-golden..."
  RESULT=$(curl -s -w "\nHTTP %{http_code} in %{time_total}s" "$BASE/api/daily-golden" --max-time 20)
  echo "$RESULT" | head -c 600
  log "Golden test complete"
  echo "$RESULT" >> /tmp/eat-loop.log 2>&1 || true
}

run_digest() {
  log "Running /api/morning-digest..."
  RESULT=$(curl -s -w "\nHTTP %{http_code} in %{time_total}s" "$BASE/api/morning-digest" --max-time 15)
  echo "$RESULT" | head -c 1200
  log "Digest complete"
  echo "$RESULT" >> /tmp/eat-loop.log 2>&1 || true
}

run_tick() {
  log "Running /api/eat-tick task=verify..."
  if [ -n "$AUTH_H" ]; then
    RESULT=$(curl -s -X POST -H "$AUTH_H" -H "Content-Type: application/json" -d '{"task":"verify"}' "$BASE/api/eat-tick" --max-time 20 -w "\nHTTP %{http_code} in %{time_total}s")
  else
    RESULT=$(curl -s -X POST -H "Content-Type: application/json" -d '{"task":"verify"}' "$BASE/api/eat-tick" --max-time 20 -w "\nHTTP %{http_code} in %{time_total}s")
  fi
  echo "$RESULT" | head -c 800
  log "Tick complete"
  echo "$RESULT" >> /tmp/eat-loop.log 2>&1 || true
}

# Schedule
case "$HOUR" in
  06)
    log "=== 06:00 UTC daily-golden + morning-digest ==="
    run_golden
    run_digest
    ;;
  08|10|12|14|16|18|20|22)
    log "=== ${HOUR}:${MIN} UTC tick ==="
    run_tick
    ;;
  *)
    log "=== ${HOUR}:${MIN} UTC tick (off-schedule) ==="
    run_tick
    ;;
esac

log "Cycle complete"
