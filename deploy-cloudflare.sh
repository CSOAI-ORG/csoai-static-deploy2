#!/bin/bash
# deploy-cloudflare.sh — Deploy to Cloudflare Pages with Functions
# Requires: npx wrangler login (one-time)
# Usage: ./deploy-cloudflare.sh

set -euo pipefail
BASE="$(cd "$(dirname "$0")" && pwd)"

echo "=== Cloudflare Pages Deploy ==="
echo "Site: $BASE"
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

# Deploy to Cloudflare Pages
echo "Deploying to Cloudflare Pages..."
echo "  Functions directory: functions/"
echo "  Static files: $BASE"
echo ""

npx wrangler pages deploy "$BASE" \
    --project-name "csoai-sovereign" \
    --branch "main" \
    --commit-dirty=true

echo ""
echo "=== Deploy Complete ==="
echo ""
echo "Your site will be available at:"
echo "  https://csoai-sovereign.pages.dev"
echo ""
echo "To add a custom domain:"
echo "  1. Go to https://dash.cloudflare.com"
echo "  2. Pages → csoai-sovereign → Custom domains"
echo "  3. Add csoai.org"
echo ""
echo "API routes available at:"
echo "  /api/orchestrate"
echo "  /api/free-gpu-orchestrator"
echo ""
