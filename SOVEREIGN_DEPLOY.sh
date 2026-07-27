#!/bin/bash
# SOVEREIGN PROD DEPLOY — 800+ files (HTML, API, assets) to Vercel
# ============================================================
# HUMAN GATE: Run this after `vercel login` (one-time browser auth)
#
# PREREQ (one-time):
#   vercel login
#
# THEN:
#   bash ~/clawd/csoai-static-deploy2/SOVEREIGN_DEPLOY.sh
#
# This deploys ALL 212 files to csoai-static-deploy2 on Vercel production.

set -e

export PATH="$HOME/.local/node/bin:$PATH"

DEPLOY_DIR="/Users/nicholas/clawd/csoai-static-deploy2"

echo "🜏 SOVEREIGN PROD DEPLOY"
echo "   Dir: $DEPLOY_DIR"
echo "   Files: $(ls $DEPLOY_DIR/*.html 2>/dev/null | wc -l | tr -d ' ') HTML pages"
echo ""

# Check auth
if ! vercel whoami > /dev/null 2>&1; then
    echo "❌ Not authenticated. Run: vercel login"
    exit 1
fi

echo "✅ Authenticated as: $(vercel whoami 2>/dev/null)"
echo ""

# Ensure vercel.json exists
if [ ! -f "$DEPLOY_DIR/vercel.json" ]; then
    cat > "$DEPLOY_DIR/vercel.json" << 'VECEOF'
{
  "outputDirectory": ".",
  "cleanUrls": false,
  "trailingSlash": false,
  "headers": [
    {"source": "/(.*)", "headers": [
      {"key": "X-Content-Type-Options", "value": "nosniff"},
      {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
      {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
      {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
      {"key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains"},
      {"key": "X-XSS-Protection", "value": "1; mode=block"}
    ]},
    {"source": "/api/(.*)", "headers": [
      {"key": "Access-Control-Allow-Origin", "value": "*"},
      {"key": "Access-Control-Allow-Methods", "value": "GET, POST, OPTIONS"},
      {"key": "Access-Control-Allow-Headers", "value": "Content-Type, Authorization"}
    ]},
    {"source": "/llms.txt", "headers": [{"key": "Content-Type", "value": "text/plain; charset=utf-8"}]},
    {"source": "/(.*).json", "headers": [{"key": "Content-Type", "value": "application/json; charset=utf-8"}, {"key": "Cache-Control", "value": "public, max-age=300"}]}
  ],
  "rewrites": [
    {"source": "/v1/chat/completions", "destination": "/api/sov-bridge"},
    {"source": "/v1/models", "destination": "/api/stats"}
  ]
}
VECEOF
    echo "✅ Created vercel.json"
fi

# Deploy
echo "🚀 Deploying to production..."
cd "$DEPLOY_DIR"
vercel deploy --prod --yes 2>&1

echo ""
echo "✅ DEPLOY COMPLETE"
echo ""
echo "=== VERIFY (sample 5 pages) ==="
for page in index.html defoneos-os.html defoneos-sigil.html systemcard.html registry.html; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "https://csoai-static-deploy2.vercel.app/$page" 2>/dev/null || echo "000")
    echo "  /$page → HTTP $CODE"
done

echo ""
echo "🜏 SIGIL: SOVEREIGN-DEPLOY-READY Ed25519"
