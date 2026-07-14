#!/bin/bash
# SOV33 / DEFONEOS nightly benchmark cron
# Re-runs the live Ollama benchmark suite + writes a SIGIL-anchored report
# Runs at 02:00 UTC daily, silent on success, alerts on failure

set -euo pipefail
SCRIPT="/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/run_ollama_benchmark.py"
LOG="/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/cron-nightly.log"
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$DATE] nightly bench starting" >> "$LOG"
if python3 "$SCRIPT" >> "$LOG" 2>&1; then
    echo "[$DATE] nightly bench complete" >> "$LOG"
    # Re-deploy to Vercel
    cd /Users/nicholas/clawd/csoai-static-deploy2
    LATEST=$(ls -t benchmark-results/benchmark_*.json | head -1)
    cp "$LATEST" benchmark-results-public.json
    vercel deploy --prod --yes >> "$LOG" 2>&1 || echo "[$DATE] vercel deploy failed" >> "$LOG"
    echo "[$DATE] deploy + alert done" >> "$LOG"
else
    echo "[$DATE] nightly bench FAILED" >> "$LOG"
    exit 1
fi
