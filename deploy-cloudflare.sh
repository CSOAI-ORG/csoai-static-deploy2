#!/bin/bash
# deploy-cloudflare.sh — Deploy to Cloudflare Pages with Functions
# Requires: npx wrangler login (one-time)
# Usage: ./deploy-cloudflare.sh
#
# FIX: Stages only static site files to _dist/ before deploying.
# The project root is 13GB+ with benchmark data, models, etc.
# Only HTML, CSS, JS, SVG, and Cloudflare Functions are deployed.

set -euo pipefail
BASE="$(cd "$(dirname "$0")" && pwd)"
DIST="$BASE/_dist"

echo "=== Cloudflare Pages Deploy ==="
echo "Source: $BASE"
echo "Staging: $DIST"
echo ""

# Check wrangler is installed
if ! command -v npx &> /dev/null; then
    echo "ERROR: npx not found. Install Node.js first."
    exit 1
fi

# Check if logged in
echo "Checking Cloudflare login..."
if ! npx wrangler whoami &> /dev/null 2>&1; then
    echo "Not logged in. Running: npx wrangler login"
    npx wrangler login
fi

echo "Cloudflare account OK"
echo ""

# Clean and create staging directory
rm -rf "$DIST"
mkdir -p "$DIST"

echo "Staging static files..."

# Copy HTML files
cp "$BASE"/*.html "$DIST/" 2>/dev/null || true

# Copy CSS files
cp "$BASE"/*.css "$DIST/" 2>/dev/null || true

# Copy SVG files (icons)
cp "$BASE"/*.svg "$DIST/" 2>/dev/null || true

# Copy robots.txt, sitemap.xml, favicon
for f in robots.txt sitemap.xml favicon.ico _headers _redirects; do
    [ -f "$BASE/$f" ] && cp "$BASE/$f" "$DIST/"
done

# Copy JSON files that are part of the site (not benchmark results)
for f in package.json package-lock.json; do
    [ -f "$BASE/$f" ] && cp "$BASE/$f" "$DIST/"
done

# Copy Cloudflare Functions directory (api routes)
if [ -d "$BASE/functions" ]; then
    cp -r "$BASE/functions" "$DIST/"
    echo "  Copied functions/ (Cloudflare Pages Functions)"
fi

# Copy any subdirectories that contain static assets
for dir in chrome-extension; do
    if [ -d "$BASE/$dir" ]; then
        cp -r "$BASE/$dir" "$DIST/"
        echo "  Copied $dir/"
    fi
done

# Copy sovereign-wiki subdirectory (stopgap for sovereign.wiki apex parked)
if [ -d "$BASE/sovereign-wiki" ]; then
    cp -r "$BASE/sovereign-wiki" "$DIST/"
    echo "  Copied sovereign-wiki/"
fi

# Count staged files
FILE_COUNT=$(find "$DIST" -type f | wc -l | tr -d ' ')
STAGE_SIZE=$(du -sh "$DIST" | cut -f1)
echo ""
echo "Staged $FILE_COUNT files ($STAGE_SIZE)"
echo ""

# Deploy staged directory
echo "Deploying to Cloudflare Pages..."
npx wrangler pages deploy "$DIST" \
    --project-name "csoai-sovereign" \
    --branch "main" \
    --commit-dirty=true

DEPLOY_EXIT=$?

# Clean up staging directory
rm -rf "$DIST"

echo ""
if [ $DEPLOY_EXIT -eq 0 ]; then
    echo "=== Deploy Complete ==="
    echo ""
    echo "Your site: https://csoai-sovereign.pages.dev"
    echo "API routes: /api/orchestrate, /api/free-gpu-orchestrator"
else
    echo "=== Deploy Failed (exit $DEPLOY_EXIT) ==="
    exit $DEPLOY_EXIT
fi
