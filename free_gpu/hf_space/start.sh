#!/bin/bash
set -euo pipefail

# SOV33 HF Space entrypoint
echo "Starting SOV33 HF Space at $(date -u '+%Y-%m-%d %H:%M UTC')"

# Ensure workspace exists
mkdir -p /workspace/sov33/checkpoints /workspace/sov33/benchmark-results

# Clone repo if not present
if [ ! -d /workspace/sov33/.git ]; then
    echo "Cloning ${REPO_URL:-https://github.com/CSOAI-ORG/sov5v2}..."
    git clone --depth=1 "${REPO_URL:-https://github.com/CSOAI-ORG/sov5v2}" /workspace/sov33
fi

# Install any additional deps
if [ -f /workspace/sov33/requirements.txt ]; then
    pip install -q -r /workspace/sov33/requirements.txt 2>/dev/null || true
fi

# Start Gradio app
echo "Launching Gradio interface on port 7860..."
exec python /app/app.py
