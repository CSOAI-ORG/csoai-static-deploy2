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

REPO_DIR="/Users/nicholas/clawd/csoai-static-deploy2"

# Deploy the ALLOWLIST build, never the repo root. Publishing the repo root put
# /.env (1,296 bytes), /wrangler.toml (with SIGIL_SECRET in plaintext),
# /govbench_eval.py and 807 KB of red-team transcripts on the public internet —
# all verified live on 2026-08-05. .cfignore did not prevent it: it lists *.jsonl
# and a .jsonl was served anyway, and .cfignore itself was served.
# build_site.py asserts that .env, wrangler.toml, *.py, *.jsonl and runs/ cannot
# be in the output, and exits non-zero if any of them are.
# Generate the machine-readable companions BEFORE assembling the publish dir. 249
# rel="alternate" links promised a .llm.json for every page and not one file existed;
# every link resolved to the homepage as text/html. Generated, not committed, so they
# cannot drift from the pages they describe.
echo "🤖 Generating .llm.json companions..."
python3 "$REPO_DIR/make_llm_json.py" || { echo "❌ make_llm_json.py failed — NOT deploying"; exit 1; }

echo "🔒 Assembling allowlisted publish directory..."
python3 "$REPO_DIR/build_site.py" || { echo "❌ build_site.py failed — NOT deploying"; exit 1; }

# Inject the math-integrity widget into DEFONEOS packs that use the GRID-A layout.
# Idempotent — re-running inject_math_check.py is safe.
echo "🧮 Injecting DEFONEOS math-integrity widget..."
python3 "$REPO_DIR/inject_math_check.py" || { echo "❌ inject_math_check.py failed — NOT deploying"; exit 1; }

DEPLOY_DIR="$REPO_DIR/_site"

echo "🜏 SOVEREIGN PROD DEPLOY"
echo "   Dir: $DEPLOY_DIR (allowlisted build, not the repo root)"
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
echo "=== VERIFY (sample 5 HTML pages) ==="
for page in index.html defoneos-os.html defoneos-sigil.html sovereign.html sov33.html; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "https://csoai-sovereign.pages.dev/$page" 2>/dev/null || echo "000")
    echo "  /$page → HTTP $CODE"
done

echo ""
echo "=== VERIFY (AI-SEO edge files — 2026-08-05 Layer-0 kit) ==="
# AI crawlers do NOT run JS — these 8 files MUST serve HTTP 200 for the kit to work.
EDGE_FILES=(
  "llms.txt"
  "llms-full.txt"
  "robots.txt"
  "sitemap.xml"
  "sitemap-ai.xml"
  "agents.txt"
  ".well-known/llm-manifest.json"
  ".well-known/security.txt"
  ".well-known/llm-policy.txt"
  ".well-known/ai-plugin.json"
  ".well-known/change-log.txt"
  ".well-known/agent-card.json"
)
EDGE_PASS=0
EDGE_FAIL=0
for f in "${EDGE_FILES[@]}"; do
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "https://csoai-sovereign.pages.dev/$f" 2>/dev/null || echo "000")
    if [ "$CODE" = "200" ]; then
        echo "  /$f → HTTP $CODE ✓"
        EDGE_PASS=$((EDGE_PASS+1))
    else
        echo "  /$f → HTTP $CODE ✗  ← AI-crawler kit BROKEN for this file"
        EDGE_FAIL=$((EDGE_FAIL+1))
    fi
done
echo ""
echo "  Edge files: $EDGE_PASS pass / $EDGE_FAIL fail (out of ${#EDGE_FILES[@]})"
if [ "$EDGE_FAIL" -gt 0 ]; then
    echo "  ⚠️  $EDGE_FAIL edge files missing on apex — AI crawlers will not see them."
    echo "      Check that $DEPLOY_DIR/{llms.txt,llms-full.txt,sitemap-ai.xml,agents.txt} exist"
    echo "      and that $DEPLOY_DIR/.well-known/ is non-empty."
fi

echo ""
echo "🜏 SIGIL: SOVEREIGN-DEPLOY-CLOUDFLARE Ed25519"
