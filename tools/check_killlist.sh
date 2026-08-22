#!/usr/bin/env bash
# Kill-list clean-URL leak check. Every banned page must be 308 (or 404), NEVER 200.
# Usage: ./tools/check_killlist.sh [base_url]   (default: https://csoai-site.pages.dev)
set -e
BASE="${1:-https://csoai-site.pages.dev}"
PAGES="master sov_space_visual sov-5d-engine sov-local-viewer sov-fluid-viewer mcp-install pulse experiments oowm-demo bft-council bft-vote-log ceasai sov-three-eyes MASTER_TAKEOVER defoneos-article-50"
LEAKED=0
for p in $PAGES; do
  r=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/$p")
  if [ "$r" = "200" ]; then
    echo "LEAK: /$p -> 200 (clean URL could serve kill-listed content)"; LEAKED=1
  fi
done
if [ "$LEAKED" = "0" ]; then echo "KILL-LIST CLEAN: no banned page serves 200"; else echo "KILL-LIST FAIL: $LEAKED leak(s)"; exit 1; fi
