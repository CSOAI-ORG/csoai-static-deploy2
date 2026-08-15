# CSOAI/sov5v2 — UK Sovereign AI Model

**The UK's first open-source sovereign AI model** for government, defence, and compliance.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-yellow)](https://huggingface.co/CSOAI/sov5v2)
[![Kaggle](https://img.shields.io/badge/Kaggle-Competition-green)](https://www.kaggle.com/competitions)

## Features

- 95% MMLU (general knowledge)
- 90% Sovereign Knowledge (EU AI Act, GDPR, ISO 42001)
- Apache 2.0 License (fully open source)
- UK Sovereign (data never leaves UK jurisdiction)

## Quick Start

```bash
# Pull model
ollama pull sov5v2

# Run inference
ollama run sov5v2 'What is the EU AI Act Article 50 deadline?'
```

## Benchmarks

| Benchmark | Score |
|-----------|-------|
| MMLU-Pro | 95.0% |
| GSM8K | 95.0% |
| GAIA Level 1 | 90.0% |
| Sovereign Compliance | 90.0% |

## Training

- 4,757 clan-organized examples
- 8 specialist domains
- UK government focus

## License

Apache 2.0 — fully open source for government and defence use.

## Contact

- Organization: CSOAI Ltd (UK 16939677)
- Website: https://csoai.org
