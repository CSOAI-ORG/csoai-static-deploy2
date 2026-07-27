#!/bin/bash
# SOVEREIGN PROD DEPLOY — 800+ files (HTML, API, assets)
# ============================================================
# PRIMARY: Cloudflare Pages (csoai-sovereign.pages.dev)
# LEGACY:  Vercel (csoai-static-deploy2.vercel.app — billing blocked)
#
# PREREQ (one-time):
#   npx wrangler login
#
# THEN:
#   bash ~/clawd/csoai-static-deploy2/SOVEREIGN_DEPLOY.sh
#
# This deploys ALL files to Cloudflare Pages production.

set -e

export PATH="$HOME/.local/node/bin:$PATH"

DEPLOY_DIR="/Users/nicholas/clawd/csoai-static-deploy2"

echo "🜏 SOVEREIGN PROD DEPLOY"
echo "   Dir: $DEPLOY_DIR"
echo "   Target: Cloudflare Pages (csoai-sovereign.pages.dev)"
echo "   Files: $(find $DEPLOY_DIR -name '*.html' -not -path '*/.git/*' -not -path '*/.backups/*' | wc -l | tr -d ' ') HTML pages"
echo ""

# Check Cloudflare auth
if ! npx wrangler whoami &> /dev/null 2>&1; then
    echo "⚠️  Not logged into Cloudflare. Run: npx wrangler login"
    echo "   Then re-run this script."
    exit 1
fi

echo "✅ Cloudflare authenticated as: $(npx wrangler whoami 2>/dev/null)"
echo ""

# Deploy to Cloudflare Pages
echo "🚀 Deploying to Cloudflare Pages production..."
npx wrangler pages deploy "$DEPLOY_DIR" \
    --project-name "csoai-sovereign" \
    --branch "main" \
    --commit-dirty=true 2>&1

echo ""
echo "✅ DEPLOY COMPLETE"
echo ""
echo "=== VERIFY (sample 5 pages) ==="
for page in index.html defoneos-os.html defoneos-sigil.html sovereign.html sov33.html; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "https://csoai-sovereign.pages.dev/$page" 2>/dev/null || echo "000")
    echo "  /$page → HTTP $CODE"
done

echo ""
echo "🜏 SIGIL: SOVEREIGN-DEPLOY-CLOUDFLARE Ed25519"
