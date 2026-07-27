---
title: SOV33 Sovereign AI Training
emoji: 🦁
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: true
license: mit
tags:
  - sovereign-ai
  - sov33
  - lora
  - fine-tuning
  - free-gpu
  - t4
duplicated_from: false
---

# SOV33 Sovereign AI Training Space

**Model:** [nicholasgriffintn/sov5v2](https://huggingface.co/nicholasgriffintn/sov5v2)  
**GPU:** Free T4 (16GB) — 2 concurrent  
**Runtime:** Up to 24 hours (sleeps on inactivity)

## What This Space Does

1. **Pulls the latest model** from GitHub on startup
2. **Shows live benchmark scores** across 9 capability domains
3. **Provides a training trigger button** for LoRA fine-tuning
4. **Logs training progress** in real-time to the UI
5. **Auto-saves checkpoints** to HuggingFace Dataset storage
6. **Pushes results** back to GitHub

## Usage

### Web Interface

Open the app and use the Gradio UI to:

- **Status tab**: View GPU info, model status, and last benchmark scores
- **Benchmark tab**: Run capability benchmarks on demand
- **Training tab**: Configure and trigger LoRA training
- **Logs tab**: Watch live training logs

### Environment Variables (set in Space settings)

| Variable | Description |
|----------|-------------|
| `HF_TOKEN` | HuggingFace token (for pushing checkpoints) |
| `GH_TOKEN` | GitHub token (for pushing results to repo) |
| `REPO_URL` | Git repo URL (default: https://github.com/CSOAI-ORG/sov5v2) |

## Limits

- Free T4: ~24h continuous, sleeps after 30min inactivity
- 2 concurrent Spaces on free tier
- Checkpoints stored on HF Datasets (free, 50GB)

## Files

| File | Purpose |
|------|---------|
| `app.py` | Gradio web interface |
| `requirements.txt` | Python dependencies |
| `packages.txt` | System dependencies |
| `start.sh` | Container entrypoint |
