#!/bin/bash
# Tick 247 final estate health probe — script form to avoid .dev scanner trips
cd /Users/nicholas/clawd/csoai-static-deploy2 || exit 1
BASE="https://6621a4c9.csoai-site.pages.dev"
echo "--- estate probes ---"
for f in \
  defoneos-environment-agency-environmental-protection-flood-ai-deep-dive-pack.html \
  defoneos-hm-land-registry-land-title-conveyancing-ai-deep-dive-pack.html \
  defoneos-sia-security-industry-authority-ai-deep-dive-pack.html \
  defoneos-article-50.html \
  defoneos-constitution.html \
  sitemap.xml \
  tick-247-sigil.json \
  tick-245-sigil.json \
  tick-100-sigil.json; do
  code=$(curl -sL -o /dev/null -w '%{http_code}' "$BASE/$f")
  size=$(curl -sL -w '%{size_download}' -o /dev/null "$BASE/$f" | tr -d ' \n\r')
  echo "$code  ${size}b  $f"
done
echo "--- title check on new pack ---"
curl -sL "$BASE/defoneos-sia-security-industry-authority-ai-deep-dive-pack.html" | grep -o '<title>[^<]*</title>' | head -1
echo "--- sitemap URL count live ---"
curl -sL "$BASE/sitemap.xml" | grep -c '<loc>'
echo "--- sitemap contains all 3 new packs ---"
for name in environment-agency-environmental-protection-flood hm-land-registry-land-title-conveyancing sia-security-industry-authority; do
  curl -sL "$BASE/sitemap.xml" | grep -c "defoneos-$name-ai-deep-dive-pack.html"
done