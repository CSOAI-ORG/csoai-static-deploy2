---
language:
- en
license: apache-2.0
tags:
- ai-safety
- governance
- byzantine-fault-tolerance
- adversarial-robustness
- eu-ai-act
- benchmark
size_categories:
- n<1K
---

# GovBench — Byzantine Safety Benchmark for AI Governance

## Overview

GovBench tests AI governance resilience against adversarial attacks on safety councils. It simulates a 33-member BFT (Byzantine Fault Tolerant) council evaluating harmful vs benign prompts under 5 attack types.

## Results (RunPod A40, 57 prompts)

| Model | Params | Harm Detection | Overblock | Accuracy | Composite |
|-------|--------|---------------|-----------|----------|-----------|
| **qwen2.5:3b** | 3.1B | 100% | 0% | **100%** | **100%** |
| **sov6v2** | 3.1B | 100% | 0% | **100%** | **100%** |
| sov5v2 | 3.1B | 100% | 10% | 98.2% | 83.2% |

### Key Findings

1. **3B models achieve 100% accuracy** on safety classification with proper prompting
2. **sov6v2 and qwen2.5:3b are tied** at 100% composite
3. **sov5v2 has 10% overblock** (flags some benign content as harmful)
4. **0.5B models fail completely** (0% accuracy — respond "NO" to everything)
5. **Prompt engineering matters** — "HARMFUL/SAFE" works better than "YES/NO"

### Model Size Threshold

| Size | Harm Detection | Notes |
|------|---------------|-------|
| 0.5B | 0% | Cannot classify safety at all |
| 1.5B | ~50% | Inconsistent |
| 3B | 100% | Reliable safety classification |
| 7B+ | 100% | Expected to be robust |

## Dataset Structure

### Prompts (57 total)

- **Harmful prompts** (47): Cyber attacks, weapons, drugs, privacy violations, hate speech, fraud, disinformation
- **Benign prompts** (10): Education, technology, security awareness, creative writing

### Attack Types

| Attack | Description | Parameters |
|--------|-------------|------------|
| flip | Flip K members' binary scores | K=0..16 |
| noise | Add gaussian noise to scores | K=0..16 |
| targeted | Push K members toward wrong answer | K=0..16 |
| injection | Overwrite prompt with adversarial injection | K=0..16 |
| poison | K members' scores fully reversed | K=0..16 |

### Aggregators

7 aggregation strategies:
- mean, median, trimmed_mean, krum, care_gated_bft, bft_weighted, geo_mean

## Usage

```python
import json

with open("govbench_v8_results.json") as f:
    results = json.load(f)

for model, data in results["results"].items():
    m = data["metrics"]
    print(f"{model}: {m['accuracy']:.1%} accuracy, {m['overblock_rate']:.1%} overblock")
```

## Running GovBench

```bash
# On RunPod (with Ollama)
python3 govbench_v8.py

# Results
cat govbench_v8_results.json | python3 -m json.tool
```

## SIGIL Provenance

```json
{
  "scheme": "sha256",
  "benchmark": "GOVBENCH-v8",
  "sha256": "cf33637353b465f71f6c7be708ddbdac626477dc6951094d90fd3a1cd379956a",
  "timestamp": "2026-07-26T04:37:07Z"
}
```

## Citation

```bibtex
@software{govbench2026,
  title={GovBench: Byzantine Safety Benchmark for AI Governance},
  author={CSOAI Ltd},
  year={2026},
  url={https://csoai.org/govbench.html}
}
```

## License

Apache 2.0
