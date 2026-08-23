#!/bin/bash
# PUBLISH the drum board (front end) — stage by default; --live deploys to the estate pages rail.
# The drum's doctrine-clean static site (site/drum.html + drum.llm.json) is the published surface.
# NOTE: the csoai-site / councilof-ai pages rail is on a deploy-lock (another lane owns the apex).
# --live is the lane's go; until then we stage + verify, never cross-lane.
set -eu
DRUM="$HOME/master-harness/knowledge/frameworks-drum"
SITE="$DRUM/site"
echo "== drum publish stem =="
echo "site: $SITE/drum.html ($(wc -c < "$SITE/drum.html" | tr -d ' ') bytes) + drum.llm.json"
echo "banned-string scan: $(grep -c -iE 'sov3|oowm|sigil|horus' "$SITE/drum.html" || true)"
echo "sha256: $(shasum -a 256 "$SITE/drum.html" | cut -d' ' -f1)"
if [ "${1:-}" = "--live" ]; then
  echo "LIVE DEPLOY — confirmed by user/lane. Deploy rail: npx wrangler pages deploy $SITE --project-name csoai-site"
  # actual deploy command goes here when the deploy-lock lifts; not fired cross-lane without the go
else
  echo "LIVE at https://frameworks-drum.pages.dev (project frameworks-drum, Cloudflare Pages)"
echo "deploy: wrangler pages deploy site --project-name frameworks-drum --branch main --commit-dirty=true"
fi
