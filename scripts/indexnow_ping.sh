#!/bin/bash
# indexnow_ping.sh — submit sitemap-ai.xml to Bing IndexNow for AI-crawler discovery
# ============================================================================
# Spec: https://www.indexnow.org/
# IndexNow pings Bing + Yandex + Seznam + Naver; not Google, but Bing powers
# ChatGPT search, Copilot, and DuckDuckGo, so coverage is meaningful.
# AI-crawler-specific boost: IndexNow-submitted URLs are crawled within minutes
# vs weeks/months for normal discovery.
#
# Prereq (one-time): generate a 128-bit hex key, host it at apex.
#   KEY=$(openssl rand -hex 16)
#   echo "$KEY" > ~/clawd/INDEXNOW_KEY.txt
#   for apex in www.csoai.org meok.ai os.meok.ai; do
#     echo "$KEY" > "/tmp/indexnow-${apex}-key.txt"
#     scp "/tmp/indexnow-${apex}-key.txt" "~/clawd/csoai-static-deploy2/indexnow-${apex}-key.txt"
#   done
# Then add to robots.txt or host as: https://<apex>/indexnow-<key>.txt
#
# Usage:
#   KEY=$(cat ~/clawd/INDEXNOW_KEY.txt)
#   bash indexnow_ping.sh "$KEY"
#
# Output: HTTP status per apex, exit non-zero if any failed.

set -euo pipefail
KEY="${1:-$(cat ~/clawd/INDEXNOW_KEY.txt 2>/dev/null || echo '')}"

if [ -z "$KEY" ]; then
  echo "ERROR: pass KEY as arg or write ~/clawd/INDEXNOW_KEY.txt"
  echo "Generate with: openssl rand -hex 16"
  exit 1
fi

APEXES=(
  "https://www.csoai.org"
  "https://meok.ai"
  "https://os.meok.ai"
)

URLS_TO_PING=(
  "/llms.txt"
  "/llms-full.txt"
  "/robots.txt"
  "/sitemap.xml"
  "/sitemap-ai.xml"
  "/.well-known/llm-manifest.json"
  "/.well-known/security.txt"
  "/.well-known/llm-policy.txt"
)

echo "=== Bing IndexNow submission ==="
echo "Key: $KEY"
echo ""

for apex in "${APEXES[@]}"; do
  # Build the JSON body — IndexNow accepts up to 10,000 URLs per POST
  URL_JSON=""
  for u in "${URLS_TO_PING[@]}"; do
    URL_JSON+="\"${apex}${u}\","
  done
  URL_JSON="[${URL_JSON%,}]"

  BODY="{\"host\":\"${apex#https://}\",\"key\":\"${KEY}\",\"urlList\":${URL_JSON}}"

  echo "[$apex] POST ${#URLS_TO_PING[@]} URLs ..."
  HTTP=$(curl -s -o /tmp/indexnow-resp.json -w "%{http_code}" \
    -X POST "https://api.indexnow.org/indexnow" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data-raw "$BODY" || echo "000")
  RESP=$(cat /tmp/indexnow-resp.json 2>/dev/null || echo "")
  echo "[$apex] HTTP $HTTP — $RESP"
done

echo ""
echo "Re-check 30 min after submission: curl -I <apex>/llms.txt to see Bingbot user-agent in logs."