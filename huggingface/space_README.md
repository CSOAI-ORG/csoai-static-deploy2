---
title: SOV33 Benchmark Runner
emoji: 🧪
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: apache-2.0
short_description: SOV33 general + agentic benchmark on HuggingFace
---

# SOV33 Benchmark Runner — HuggingFace Space

Hosts the SOV33 benchmark harness as a Gradio app. Runs general capability
(MMLU-Pro, GSM8K, AIME, HellaSwag, ARC-C, HumanEval, TruthfulQA) and agentic
(GAIA-lite, tau-bench-retail, ALFWorld-text, HotpotQA, SWE-bench-lite) suites
against any uploaded model.

## Use

1. Push the model you want to evaluate to the Hub (or use one of the suggested)
2. Open the Space → paste model id → pick suite → Run
3. Results download as signed JSON; sigil chain stored in `/data/sigil_chain.jsonl`

## Files in this Space

- `sov33_benchmark_general.py` — general capability suite
- `sov33_benchmark_agentic.py` — agentic capability suite
- `harness_loader.py` — HF transformers wrapper
- `app.py` — Gradio UI

## Suggested models

- `Qwen/Qwen2.5-3B-Instruct` (3B, fits T4 small)
- `Qwen/Qwen3-30B-A3B` (MoE 30B/A3B, fits A100 80GB)
- `meta-llama/Meta-Llama-3-8B-Instruct`
- `mistralai/Mistral-7B-Instruct-v0.3`

## Credentials

Set `HF_TOKEN` as a Space secret to enable private models.