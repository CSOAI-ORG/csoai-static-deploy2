#!/bin/bash
# apex-brick-watchdog.sh — guard the canonical trust root + councilof.ai health.
# 2026-08-22: the AG-UI/DEFONEOS lane deploys direct builds to shared Pages
# projects every few minutes; stale/non-prerendered deploys break routes and
# the apex did.json. This watchdog detects both failure modes and re-converges
# via the ONE canonical deployer (GHA), so the estate self-heals within ~5 min.
# Log: /tmp/apex-brick-watchdog.log
set -u
LOG=/tmp/apex-brick-watchdog.log
GH=/opt/homebrew/bin/gh
ts() { date "+%Y-%m-%dT%H:%M:%S"; }

# ── 1. councilof.ai route-liveness (fast, no external deps beyond curl).
# Degraded signature (OR):
#   (a) bare /about 404 AND homepage thin (<5000 chars = non-prerendered shell), OR
#   (b) canonical-marker route missing — /csoai-law/ must be 200 and /ag-ui must
#       308 (both ship only in the canonical build; a stale full-size lane deploy
#       returns 404 for them while home still looks fat — thin-shell check alone
#       missed a 13h degradation on 2026-08-23).
ROUTE_CHECK=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://councilof.ai/about" 2>/dev/null)
HOMEPAGE_CHARS=$(curl -s --max-time 10 "https://councilof.ai/" 2>/dev/null | python3 -c "import sys,re; s=sys.stdin.read(); t=re.sub(r'<[^>]+>',' ',s); print(len(t.strip()))" 2>/dev/null)
CSOAI_LAW=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://councilof.ai/csoai-law/" 2>/dev/null)
AGUI=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://councilof.ai/ag-ui" 2>/dev/null)
DEGRADED=0
if [ "$ROUTE_CHECK" = "404" ] && [ -n "$HOMEPAGE_CHARS" ] && [ "$HOMEPAGE_CHARS" -lt 5000 ]; then
  DEGRADED=1
  DEG_REASON="bare /about 404 + thin shell ${HOMEPAGE_CHARS}c"
elif [ "$CSOAI_LAW" != "200" ] || [ "$AGUI" != "308" ]; then
  DEGRADED=1
  DEG_REASON="canonical markers missing (csoai-law/=$CSOAI_LAW ag-ui=$AGUI)"
fi
if [ "$DEGRADED" = "1" ]; then
  # Avoid deploy pile-up: only dispatch if no deploy for master is already
  # pending or in_progress (the GHA deploy serializes; stacking them just
  # lengthens the queue and the lane clobbers again before it lands).
  QUEUE=$("$GH" run list --repo CSOAI-ORG/councilof-ai --workflow deploy.yml --limit 1 --json status --jq '.[0].status' 2>/dev/null)
  if [ "$QUEUE" = "in_progress" ] || [ "$QUEUE" = "pending" ] || [ "$QUEUE" = "queued" ]; then
    echo "$(ts) councilof.ai degraded BUT deploy already $QUEUE — skip dispatch (anti pile-up)" >> "$LOG"
  else
    echo "$(ts) COUNCILOF.AI DEGRADED ($DEG_REASON) — re-converging" >> "$LOG"
    "$GH" workflow run deploy.yml --repo CSOAI-ORG/councilof-ai >> "$LOG" 2>&1
    echo "$(ts) councilof.ai reconverge dispatched (exit $?)" >> "$LOG"
  fi
fi

# ── 2. apex trust-root brick check (best-effort; skip on network failure).
BODY=$(curl -s --max-time 15 -H "User-Agent: Mozilla/5.0" \
  "https://csoai.org/.well-known/did.json?cb=$(date +%s%N)" 2>/dev/null)
if [ -z "$BODY" ]; then
  echo "$(ts) WARN: could not fetch apex did.json — skipping brick check (route check above still ran)" >> "$LOG"
elif ! echo "$BODY" | grep -q "card-attestation-1"; then
  echo "$(ts) BRICK MISSING on apex — re-converging via canonical deployer" >> "$LOG"
  "$GH" workflow run csoai-site-deploy.yml --repo CSOAI-ORG/councilof-ai >> "$LOG" 2>&1
  echo "$(ts) dispatch attempted (exit $?)" >> "$LOG"
fi
