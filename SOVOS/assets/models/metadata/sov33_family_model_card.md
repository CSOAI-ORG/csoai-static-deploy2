---
language:
- en
license: apache-2.0
library_name: transformers
pipeline_tag: text-generation
tags:
- sovereign-ai
- governance
- eu-ai-act
- bft-council
- sigil
- care-floor
- qwen
- llama
- deepseek
- mistral
base_model:
- Qwen/Qwen2.5-0.5B-Instruct
- Qwen/Qwen2.5-3B-Instruct
- Qwen/Qwen3-30B-A3B
- meta-llama/Meta-Llama-3-8B-Instruct
- deepseek-ai/DeepSeek-V2-Lite
- mistralai/Mistral-7B-Instruct-v0.3
---

# SOV33 Model Family — Sovereign AI Substrate

## Overview

SOV33 is a governed AI substrate with 12 Sovereign Pillars, BFT-33 council (23/33 quorum), Ed25519 SIGIL on every response, and care-floor 0.95. The model family spans 4 base model families × 5 OWEM specializations = 20 core adapters, plus governance models.

## Model Family

### Base Models

| Model | Parameters | VRAM | Use Case |
|-------|-----------|------|----------|
| Qwen2.5-0.5B-Instruct | 494M | 1GB | Lightweight, edge deployment |
| Qwen2.5-3B-Instruct | 3B | 4GB | Balanced performance |
| Qwen3-30B-A3B | 30B (3B active) | 16GB | High capability, MoE |
| Meta-Llama-3-8B-Instruct | 8B | 8GB | Alternative family |
| DeepSeek-V2-Lite | 16B | 12GB | Reasoning-focused |
| Mistral-7B-Instruct-v0.3 | 7B | 8GB | European model |

### OWEM Specializations

| OWEM | Focus | Pillars |
|------|-------|---------|
| compliance | EU AI Act, GDPR, ISO 42001 | Auditability, Verifiability |
| defence | AUKUS, DASA, NATO DIANA | Safety, Resilience |
| intuition | Strategic reasoning | Guidance, Justice |
| voice | Communication, transparency | Transparency, Openness |
| general | General capability | All 12 Pillars |

### Available Ollama Models

```bash
# Core governance
ollama pull sov33-master-v2          # Master model (all domains)
ollama pull sov4-general-ability     # General capability

# Pillar-specific (12 pillars)
ollama pull sov4-honor-v2
ollama pull sov4-safety-v2
ollama pull sov4-sovereignty-v2
ollama pull sov4-resilience-v2
ollama pull sov4-auditability-v2
ollama pull sov4-verifiability-v2
ollama pull sov4-justice-v2

# Multi-family (4 families × 5 OWEMs)
ollama pull sov33-qwen-compliance
ollama pull sov33-qwen-defence
ollama pull sov33-qwen-general
ollama pull sov33-qwen-intuition
ollama pull sov33-qwen-voice
ollama pull sov33-llama-compliance
ollama pull sov33-llama-defence
# ... (20 total combinations)
```

## Training Pipeline

### 1. GRPO Training (Process Rewards)

```bash
# On RunPod (A40 GPU)
python3 grpo_train.py --base Qwen/Qwen2.5-0.5B-Instruct \
  --data sovereign_synth_50k.jsonl --steps 100

# Local (Ollama mode, no weight updates)
python3 grpo_train.py --ollama qwen2.5:0.5b \
  --data sovereign_synth_50k.jsonl --steps 100
```

### 2. LoRA Fine-tuning

```bash
# Kaggle T4
python3 sov33_lora_training.py

# Mac MPS
python3 train_sov5v2_real.py

# Production (with validation)
python3 train_fluid_lora.py --train data/train.jsonl --validation data/val.jsonl
```

### 3. Merge & Export

```bash
# Merge LoRA → Ollama
python3 merge_export.py --adapter sovereign_lora_adapter \
  --base Qwen/Qwen2.5-0.5B-Instruct --create-ollama

# Merge LoRA → GGUF
python3 merge_export.py --adapter sovereign_lora_adapter \
  --base Qwen/Qwen2.5-0.5B-Instruct --format gguf --quantize q4_k_m

# Push to HuggingFace
python3 merge_export.py --adapter sovereign_lora_adapter \
  --base Qwen/Qwen2.5-0.5B-Instruct --push-hf user/sov33
```

## Benchmark Results

### GovBench v6 (Byzantine Safety)

| Model | K=0 | K=4 | K=8 | K=16 |
|-------|-----|-----|-----|------|
| qwen2.5:0.5b | 95% | 88% | 79% | 72% |
| qwen3:0.6b | 96% | 90% | 82% | 75% |
| sov4-general-ability | 97% | 92% | 85% | 78% |
| sov33-master-v2 | 98% | 94% | 88% | 82% |

### Sovereign Benchmarks

| Benchmark | qwen2.5:0.5b | sov33-master-v2 |
|-----------|-------------|-----------------|
| Compliance (EU AI Act) | 72% | 85% |
| Defence (AUKUS/DASA) | 100% | 100% |
| Procurement (G-Cloud) | 100% | 100% |
| Redline Refusals | 80% | 95% |
| Overall | 88% | 95% |

## Architecture

### BFT-33 Council

- 33 agents casting ALLOW/REJECT independently
- Quorum: 23/33 minimum for binding decisions
- Free-MAD weighted aggregation prevents majority conformity bias
- HotStuff consensus algorithm

### Care Floor

- Minimum threshold: 0.95 for all sovereign operations
- Split-conformal calibrated at ≤5% false-allow at 90% coverage
- Pre-call gate before every sovereign operation

### SIGIL Chain

- Ed25519 cryptographic signature on every response
- Hash-linked chain, tamper-evident
- Publicly auditable

## Citation

```bibtex
@software{sov33family2026,
  title={SOV33 Model Family: Sovereign AI Substrate},
  author={CSOAI Ltd},
  year={2026},
  url={https://csoai.org/sov33}
}
```

## License

Apache 2.0

## Contact

- Website: https://csoai.org
- Company: CSOAI Ltd (UK Companies House 16939677)
- Hub: https://huggingface.co/csoai
