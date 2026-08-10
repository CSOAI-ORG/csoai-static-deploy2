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
base_model:
- Qwen/Qwen2.5-0.5B-Instruct
- Qwen/Qwen3-30B-A3B
---

# SOV33 — Sovereign Open World Emergence Model

## Model Description

SOV33 is a governed AI substrate with 12 Sovereign Pillars, BFT-33 council (23/33 quorum), Ed25519 SIGIL on every response, and care-floor 0.95. It is not a foundation model competing with frontier labs — it is a different capability class: sovereign, governed, auditable.

## Architecture

- **Base**: Qwen3-0.6B + LoRA adapters (Qwen2.5-0.5B-Instruct for lightweight)
- **Governance**: BFT-33 council with HotStuff consensus
- **Audit**: Ed25519 SIGIL chain on every response
- **Safety**: Care Floor 0.95 (split-conformal calibrated)
- **Training**: GRPO with process rewards

## 12 Sovereign Pillars

1. Honor — truth-telling
2. Safety — first do no harm
3. Guidance — help toward good outcome
4. Sovereignty — respect user autonomy
5. Resilience — bend but don't break
6. Auditability — every action logged
7. Verifiability — every claim checkable
8. Transparency — open about how it works
9. Justice — fair and proportionate
10. Equity — equal treatment
11. Openness — free flow of information
12. Continuity — carry memory across sessions

## Benchmark Results

| Benchmark | Score | Notes |
|-----------|-------|-------|
| GovBench v6 | 72% | Byzantine safety resilience |
| Sovereign Compliance | 72% | EU AI Act, GDPR, ISO 42001 |
| Sovereign Defence | 100% | AUKUS, DASA, NATO DIANA |
| Sovereign Procurement | 100% | G-Cloud, DSP, CCS |
| Redline Refusals | 80% | Harmful content rejection |

## Training

### GRPO Training

```bash
# Run on RunPod
python3 grpo_train.py --base Qwen/Qwen2.5-0.5B-Instruct \
  --data sovereign_synth_50k.jsonl --steps 100

# Or with Ollama (no weight updates)
python3 grpo_train.py --ollama qwen2.5:0.5b \
  --data sovereign_synth_50k.jsonl --steps 100
```

### LoRA Fine-tuning

```bash
# Kaggle T4
python3 sov33_lora_training.py

# Mac MPS
python3 train_sov5v2_real.py
```

## Deployment

### Ollama

```bash
# Merge LoRA adapter
python3 merge_export.py --adapter sovereign_lora_adapter \
  --base Qwen/Qwen2.5-0.5B-Instruct --create-ollama

# Run
ollama run sov33-master-v2
```

### HuggingFace

```bash
python3 merge_export.py --adapter sovereign_lora_adapter \
  --base Qwen/Qwen2.5-0.5B-Instruct --push-hf user/sov33
```

## Evaluation

```bash
# Unified eval CLI
python3 sov33_eval.py --model qwen2.5:0.5b --suite sovereign_compliance

# Full pipeline on RunPod
python3 batch_runpod.py full-pipeline --pod fresh-a40
```

## SIGIL Chain

Every response includes a SHA-256 SIGIL:

```json
{
  "schema": "sov33.grpo-eval/v1",
  "status": "completed",
  "timestamp": "2026-07-26T02:51:32Z",
  "model": "qwen2.5:0.5b",
  "steps": 100,
  "mean_reward": 0.47,
  "sigil": "bb26da64..."
}
```

## Citation

```bibtex
@software{sov332026,
  title={SOV33: Sovereign Open World Emergence Model},
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
