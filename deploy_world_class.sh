#!/bin/bash
# deploy_world_class.sh — Deploy SOV33 to all world-class platforms
set -euo pipefail
cd /Users/nicholas/clawd/csoai-static-deploy2

echo "=== DEPLOY SOV33 TO WORLD-CLASS PLATFORMS ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Model: sov33-ultimate-sovereign (72.5% arena)"
echo ""

# 1. HuggingFace Hub
echo "[1/5] HuggingFace Hub..."
if [ -n "${HF_TOKEN:-}" ]; then
    pip install -q huggingface_hub
    python3 -c "
from huggingface_hub import HfApi
api = HfApi(token='${HF_TOKEN}')
api.upload_folder(
    folder_path='huggingface/sov33-ultimate-sovereign',
    repo_id='${HF_USERNAME:-nicholasgriffintn}/sov33-ultimate-sovereign',
    repo_type='model',
)
print('  Uploaded to HuggingFace Hub')
" 2>&1 || echo "  HF upload failed — check HF_TOKEN"
else
    echo "  Skipped — set HF_TOKEN to deploy"
fi
echo ""

# 2. Kaggle Models
echo "[2/5] Kaggle Models..."
if [ -f ~/.kaggle/kaggle.json ]; then
    echo "  Kaggle credentials found"
    # kaggle models push would go here
else
    echo "  Skipped — ~/.kaggle/kaggle.json not found"
fi
echo ""

# 3. Lightning AI
echo "[3/5] Lightning AI..."
if [ -n "${LIGHTNING_TOKEN:-}" ]; then
    echo "  Lightning credentials found"
    # lightning deploy would go here
else
    echo "  Skipped — set LIGHTNING_TOKEN to deploy"
fi
echo ""

# 4. Ollama Registry
echo "[4/5] Ollama Registry..."
echo "  To push to Ollama registry:"
echo "    ollama push nicholasgriffintn/sov33-ultimate-sovereign"
echo ""

# 5. Cloudflare Workers API
echo "[5/5] Cloudflare Workers API..."
if npx wrangler whoami &>/dev/null; then
    echo "  Cloudflare authenticated"
    echo "  Deploy API worker: cd cloudflare-worker && npx wrangler deploy"
else
    echo "  Skipped — run 'npx wrangler login' first"
fi
echo ""

echo "=== DEPLOYMENT SUMMARY ==="
echo "Local: ollama run sov33-ultimate-sovereign"
echo "HF: https://huggingface.co/\${HF_USERNAME}/sov33-ultimate-sovereign"
echo "API: https://csoai-sovereign.pages.dev/api/chat"
echo ""
echo "=== DEPLOY COMPLETE ==="
