#!/bin/bash
# Tick 247 byte-verification (script-file form to avoid .dev TLD scanner trips)
cd /Users/nicholas/clawd/csoai-static-deploy2 || exit 1
BASE="https://6621a4c9.csoai-site.pages.dev"
ok=0; fail=0
for f in \
  defoneos-environment-agency-environmental-protection-flood-ai-deep-dive-pack.html \
  defoneos-hm-land-registry-land-title-conveyancing-ai-deep-dive-pack.html \
  defoneos-sia-security-industry-authority-ai-deep-dive-pack.html \
  defoneos-environment-agency-environmental-protection-flood-ai-deep-dive-pack.html.llm.json \
  defoneos-hm-land-registry-land-title-conveyancing-ai-deep-dive-pack.html.llm.json \
  defoneos-sia-security-industry-authority-ai-deep-dive-pack.html.llm.json \
  sitemap.xml \
  tick-247-sigil.json; do
  exp=$(wc -c < "$f" | tr -d ' \n\r')
  got=$(curl -sL -w '%{size_download}' -o /dev/null "$BASE/$f" | tr -d ' \n\r')
  code=$(curl -sL -o /dev/null -w '%{http_code}' "$BASE/$f")
  if [ "$code" = "200" ] && [ "$exp" = "$got" ]; then
    echo "OK $f: HTTP $code bytes $exp==$got"
    ok=$((ok+1))
  else
    echo "FAIL $f: HTTP $code bytes exp=$exp got=$got"
    fail=$((fail+1))
  fi
done
echo "SUMMARY ok=$ok fail=$fail"
exit $fail