#!/usr/bin/env bash
# deploy_sentinel.sh — DEPLOY + SENTINEL in one command (the doctrine).
#
# The 2026-08-15 lesson: a deploy that doesn't change production is a
# FAILED deploy. Every static deploy must assert a sentinel on the
# production alias — not the preview alias — before reporting success.
#
# Usage:
#   bash deploy_sentinel.sh                      # build + deploy prod + assert
#   SENTINEL_URL="https://csoai-site.pages.dev/gspc-scoreboard" SENTINEL_STRING="phi4:14b" \
#     bash deploy_sentinel.sh
#
set -euo pipefail

PROJECT="${CF_PROJECT:-csoai-site}"
BRANCH="${CF_BRANCH:-main}"
SENTINEL_URL="${SENTINEL_URL:-https://csoai-site.pages.dev/gspc-scoreboard}"
SENTINEL_STRING="${SENTINEL_STRING:-phi4:14b}"   # marker that ONLY exists in the fresh build
EXPECTED_MIN_BYTES="${SENTINEL_MIN_BYTES:-60000}"  # 62KB scoreboard = fresh; 25KB = old

echo "=== [1/3] build ==="
python3 build_site.py 2>&1 | tail -2

echo "=== [2/3] deploy to PRODUCTION branch ($BRANCH) ==="
OUT=$(npx wrangler pages deploy _site --project-name "$PROJECT" --branch "$BRANCH" 2>&1)
echo "$OUT" | tail -3
DEPLOY_URL=$(echo "$OUT" | grep -oE "https://[a-z0-9]{8}\.${PROJECT}\.pages\.dev" | head -1)
echo "deployment: $DEPLOY_URL"

echo "=== [3/3] SENTINEL ASSERT on production alias ==="
SIZE=$(curl -sL -o /tmp/sentinel-body.html -w "%{size_download}" "$SENTINEL_URL")
CODE=$(curl -sL -o /dev/null -w "%{http_code}" "$SENTINEL_URL")
echo "  prod alias: HTTP $CODE, ${SIZE} bytes"

FAIL=0
if [ "$CODE" != "200" ]; then echo "  ✗ FAIL: expected HTTP 200 on $SENTINEL_URL"; FAIL=1; fi
if [ "$SIZE" -lt "$SENTINEL_MIN_BYTES" ]; then
  echo "  ✗ FAIL: size ${SIZE}B < ${SENTINEL_MIN_BYTES}B — production is serving an OLD build"; FAIL=1
fi
if ! grep -q "$SENTINEL_STRING" /tmp/sentinel-body.html 2>/dev/null; then
  echo "  ✗ FAIL: sentinel string '${SENTINEL_STRING}' missing — production not updated"; FAIL=1
else
  echo "  ✓ sentinel '${SENTINEL_STRING}' PRESENT on production"
fi

if [ "$FAIL" -eq 1 ]; then
  echo "=== ✗ DEPLOY FAILED SENTINEL — production unchanged. Investigate before claiming success. ==="
  exit 1
fi
echo "=== ✓ DEPLOY+ASSERT PASSED — production alias serves the fresh build ==="