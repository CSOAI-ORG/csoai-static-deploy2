#!/usr/bin/env bash
# indexnow-submit.sh — IndexNow URL submission (N-SITES do-today #1).
# Generates a key, writes {key}.txt (host at csoai.org root), pings URLs.
# One ping propagates to Bing/Yandex/Naver/Seznam/Yep.
set -euo pipefail

KEY_FILE="/tmp/indexnow-key.txt"
KEY="$(cat "$KEY_FILE" 2>/dev/null || openssl rand -hex 16 | tee "$KEY_FILE")"
echo "IndexNow key: $KEY"

# 1. The key file to host at the site root (Nick deploys this once)
printf '%s' "$KEY" > "/tmp/${KEY}.txt"
echo "→ host this file at https://councilof.ai/${KEY}.txt (and csoai.org/${KEY}.txt)"

# 2. The URLs to submit (the live measurement surfaces)
URLS=(
  "https://councilof.ai/"
  "https://councilof.ai/api/gspc"
  "https://councilof.ai/llms.txt"
  "https://councilof.ai/honesty"
  "https://councilof.ai/gspc-verify"
  "https://councilof.ai/signed-verification-wall"
)

# 3. Submit (one POST, propagates to all engines)
PAYLOAD=$(python3 -c "
import json,sys
urls=$(printf '%s ' "${URLS[@]}" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().split()))")
print(json.dumps({'host':'councilof.ai','key':'$KEY','keyLocation':'https://councilof.ai/${KEY}.txt','urlList':$urls}))
")
echo "→ POSTing $PAYLOAD"
curl -s -m 20 -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$PAYLOAD" -o /dev/null -w "indexnow status: %{http_code}\n"

echo "Done. Re-run after each new card/board release (≤10k URLs/day)."
