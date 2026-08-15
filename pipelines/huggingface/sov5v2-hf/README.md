---
language:
  - en
tags:
  - sovereign-ai
  - government
  - defence
  - uk
  - compliance
  - eu-ai-act
  - gdpr
  - iso-42001
  - open-source
  - apache-2.0
license: apache-2.0
pipeline_tag: text-generation
---

# CSOAI/sov5v2 - UK Sovereign AI Model

**The UK's first open-source sovereign AI model** for government, defence, and compliance.

## Key Features

- 95% MMLU (general knowledge)
- 90% Sovereign Knowledge (EU AI Act, GDPR, ISO 42001)
- Apache 2.0 License (fully open source)
- UK Sovereign (data never leaves UK jurisdiction)

## Quick Start

```bash
ollama pull sov5v2
ollama run sov5v2 "What is the EU AI Act Article 50 deadline?"
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
