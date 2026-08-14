#!/usr/bin/env bash
# fix_apex.sh — repair the recurring csoai.org 522 (missing apex record).
#
# The estate is served live from councilof.ai (200) + csoai-site.pages.dev (200), but the
# csoai.org APEX returns 522 because the zone has no @ record pointing at the Pages deploy.
# This adds the flattened apex CNAME @ -> csoai-site.pages.dev (proxied) via the Cloudflare API.
# Idempotent: if the record already exists it reports and exits; it never duplicates.
#
# ── RUN THIS ────────────────────────────────────────────────────────────────
#   Needs a token with **Zone → DNS → Edit** on the csoai.org zone (the deploy token only has
#   Workers/Pages/Routes — either add DNS:Edit to it or use a token that has it):
#       export CLOUDFLARE_API_TOKEN=<token with Zone:DNS:Edit>
#       ./fix_apex.sh                # dry-run: shows what it would do
#       ./fix_apex.sh --apply        # actually create the record
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1
: "${CLOUDFLARE_API_TOKEN:?export a token with Zone:DNS:Edit on csoai.org}"
API="https://api.cloudflare.com/client/v4"
AUTH=(-H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json")
TARGET="csoai-site.pages.dev"

echo "== current apex status =="
code=$(curl -s -o /dev/null -m 8 -w "%{http_code}" "https://csoai.org" || echo 000)
echo "  https://csoai.org -> $code  (522/000 = broken apex; 200 = already fine)"

echo "== resolve zone id for csoai.org =="
ZONE=$(curl -s "${AUTH[@]}" "$API/zones?name=csoai.org" | python3 -c "import sys,json;r=json.load(sys.stdin).get('result',[]);print(r[0]['id'] if r else '')")
[ -n "$ZONE" ] || { echo "  ✗ zone not found or token lacks Zone:Read — check the token's zone scope"; exit 1; }
echo "  zone: $ZONE"

echo "== existing apex (@) record? =="
EXIST=$(curl -s "${AUTH[@]}" "$API/zones/$ZONE/dns_records?name=csoai.org&type=CNAME" | python3 -c "
import sys,json;r=json.load(sys.stdin).get('result',[])
print(r[0]['id']+'|'+r[0].get('content','') if r else '')")
if [ -n "$EXIST" ]; then
  echo "  apex CNAME already exists -> ${EXIST#*|}"
  [ "${EXIST#*|}" = "$TARGET" ] && { echo "  ✅ already points at $TARGET — nothing to do"; exit 0; }
  echo "  ⚠️  points elsewhere; not overwriting automatically. Review in the CF dashboard."
  exit 0
fi

echo "== apex record missing — this is the 522 cause =="
BODY='{"type":"CNAME","name":"@","content":"'"$TARGET"'","proxied":true,"comment":"apex flatten -> Pages (fix_apex.sh)"}'
if [ "$APPLY" = 0 ]; then
  echo "  [dry-run] would POST $API/zones/$ZONE/dns_records"
  echo "  [dry-run] body: $BODY"
  echo "  re-run with --apply to create it."
  exit 0
fi
echo "  creating apex CNAME @ -> $TARGET (proxied)…"
RES=$(curl -s -X POST "${AUTH[@]}" "$API/zones/$ZONE/dns_records" --data "$BODY")
echo "$RES" | python3 -c "import sys,json;d=json.load(sys.stdin);print('  ✅ created:' if d.get('success') else '  ✗ failed:',d.get('result',{}).get('name') or d.get('errors'))"
echo "== verify (propagation can take a minute) =="
sleep 5; curl -s -o /dev/null -m 8 -w "  https://csoai.org -> %{http_code}\n" "https://csoai.org" || true
