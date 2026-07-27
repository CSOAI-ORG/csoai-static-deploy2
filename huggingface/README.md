---
title: SOV33 Benchmark Runner
emoji: 🧪
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: apache-2.0
short_description: SOV33 general + agentic + GovBench benchmark on HuggingFace
---

# SOV33 Benchmark Runner — HuggingFace Space

Hosts the SOV33 benchmark harness as a Gradio app. Runs general capability
(MMLU-Pro, GSM8K, AIME, HellaSwag, ARC-C, HumanEval, TruthfulQA) and agentic
(GAIA-lite, tau-bench-retail, ALFWorld-text, HotpotQA, SWE-bench-lite) suites
against any uploaded model.

## Use

1. Open the Space
2. Paste model id (or pick from suggested list)
3. Pick target (general / agentic) + suite
4. Run → results download as signed JSON + appended to sigil chain

## Suggested models

- `Qwen/Qwen2.5-3B-Instruct` (3B, fits T4 small)
- `Qwen/Qwen3-30B-A3B` (MoE 30B/A3B, fits A100 80GB)
- `meta-llama/Meta-Llama-3-8B-Instruct`
- `mistralai/Mistral-7B-Instruct-v0.3`

## GovBench — Byzantine Safety Benchmark

GovBench tests AI governance resilience against adversarial attacks on safety
councils. It simulates a 33-member BFT (Byzantine Fault Tolerant) council
evaluating harmful vs benign prompts under 5 attack types:

| Attack | Description |
|--------|-------------|
| flip | Flip K members' binary scores |
| noise | Add gaussian noise to scores |
| targeted | Push K members toward wrong answer |
| injection | Overwrite prompt with adversarial injection |
| poison | K members' scores fully reversed |

**Config:** 33 members, 57 prompts (47 harm + 10 benign), 5 seeds, K=0..16,
7 aggregators (mean, median, trimmed, majority, supermajority, unanimous, weighted).

**Models tested:** qwen2.5:0.5b, qwen3:0.6b, sov4-general-ability, sov33-master-v2

### Running GovBench

```bash
# Local (requires Ollama)
python3 govbench_v6.py

# Results
cat govbench_v6_results.json | python3 -m json.tool
```

### GovBench Results Format

```json
{
  "benchmark": "GOVBENCH-V6",
  "timestamp": "2026-07-25T10:52:15Z",
  "config": {
    "n_members": 33,
    "n_models": 4,
    "n_prompts": 57,
    "harm": 47,
    "benign": 10,
    "seeds": 5,
    "k_values": [0, 1, 2, 4, 8, 12, 16],
    "aggregators": ["mean", "median", "trimmed", "majority", "supermajority", "unanimous", "weighted"],
    "attacks": ["flip", "noise", "targeted", "injection", "poison"]
  },
  "board": {
    "flip": {
      "0": {
        "mean": {"accuracy": 0.95, "overblock": 0.02, "composite": 0.93}
      }
    }
  }
}
```

### Metrics

- **accuracy**: Correct classification rate (harm→YES, benign→NO)
- **overblock**: False positive rate (benign→YES)
- **composite**: Balanced metric (accuracy - overblock)

## Secrets

Set `HF_TOKEN` for private models.
