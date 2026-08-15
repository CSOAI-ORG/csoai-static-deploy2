#!/bin/bash
cd /Users/nicholas/clawd/csoai-static-deploy2 || exit 1
echo "--- _site/tick-247-sigil.json ---"
ls -la _site/tick-247-sigil.json 2>&1
wc -c _site/tick-247-sigil.json 2>/dev/null
echo "--- repo-root tick-247-sigil.json ---"
ls -la tick-247-sigil.json 2>&1
wc -c tick-247-sigil.json 2>/dev/null
echo "--- other tick-247-sigil files on disk (excluding _site) ---"
find . -name "tick-247-sigil.json" -not -path "./_site/*" 2>/dev/null
echo "--- served content head ---"
curl -sL "https://c1301814.csoai-site.pages.dev/tick-247-sigil.json" | head -c 400
echo ""
echo "--- served content diff vs local (first 200 lines) ---"
diff <(curl -sL "https://c1301814.csoai-site.pages.dev/tick-247-sigil.json") tick-247-sigil.json | head -30