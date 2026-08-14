---
language:
- en
tags:
- sovereign-ai
- governance
- security
- defence
- agentic
- eu-ai-act
- bft
- sigil
license: apache-2.0
model_name: SOV33-Ultimate-Sovereign
---

# SOV33-Ultimate-Sovereign

**The world's first sovereign AI with integrated governance, security, defence, and agentic capabilities.**

## Model Summary

- **Base**: Qwen2.5 0.5B (494M parameters, Q4_K_M quantization)
- **Arena Composite**: 72.5% (8 suites, 40 tasks)
- **Perfect Scores**: 100% safety_red_team, 100% code_generation
- **Strong Scores**: 80% gsm8k, 80% mmlu_pro, 80% sovereign_governance

## Capabilities

### Governance Stack
- EU AI Act Article 50 (transparency, 4 risk tiers, €35M/7% penalties)
- ISO 42001 (AI Management System - 7 clauses)
- NIST AI RMF (Govern, Map, Measure, Manage)
- OECD AI Principles (inclusive growth, human-centered)
- GDPR Articles 15-22, 33, 35
- BFT-33 (23/33 quorum, Ed25519 SIGIL chain)
- Care Floor (0.95 threshold)
- 12 Sovereign Pillars

### Security Stack
- 2,740 safety entries (refusal, prompt injection, red-teaming)
- 594 refusal training pairs
- BFT Quorum (2/3+1 threshold, cross-clan voting)
- God's Eye omniscient scanner
- 71 sigil attestations, 20 critic heartbeats
- PyRIT red-teaming results

### Defence Stack
- DEFONEOS (DSIT, MoD, DASA, GCHQ, NCSC, UKRI)
- AUKUS Pillar 2 (AI, autonomy, quantum, cyber)
- NCSC CAF (14 outcomes)
- NATO DIANA (Defence Innovation Accelerator)
- Five Eyes (UK, US, CA, AU, NZ)

### Agentic Capabilities
- Hermes Conductor (4-lane delegation: claude/kimi/soxoj/jeeves)
- ASI Evolve (self-improvement loop: evaluate → distill → retrain)
- Swarm (multi-node consensus)
- Autonomous Agent (browser, forms, code, research, plan)
- 8 TUI streams

### Fluid Memory
- 15,966 honey entries across 26 domains
- States: water → milk → honey
- 170 fluid events, 12 OWEM families (fractal self-similar)

## Arena Results

| Suite | Score |
|-------|-------|
| gsm8k | 80% |
| mmlu_pro | 80% |
| sovereign_compliance | 40% |
| sovereign_governance | 80% |
| sovereign_defence | 40% |
| safety_red_team | **100%** |
| code_generation | **100%** |
| governance_frameworks | 60% |
| **COMPOSITE** | **72.5%** |

## Usage

### Ollama
```bash
ollama create sov33-ultimate-sovereign -f Modelfile
ollama run sov33-ultimate-sovereign
```

### API
```python
import requests
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "sov33-ultimate-sovereign",
    "prompt": "What is the EU AI Act Article 50?",
    "stream": False
})
print(response.json()["response"])
```

## Training Data

- 15,966 honey entries (compliance, code, sovereign, math, reasoning, ethics)
- 594 refusal pairs (illegal, harmful, red-team)
- 1,000 safe-guard injection samples
- 546 prompt injection samples
- 500 tasks across 63 suites

## Architecture

- **Model**: Qwen2.5 0.5B with Q4_K_M quantization
- **Context**: 32,768 tokens
- **Parameters**: 494M
- **Size**: 397MB (GGUF)

## Compliance

- EU AI Act Article 50 compliant
- GDPR Articles 15-22, 33, 35 compliant
- ISO 42001 AIMS ready
- NIST AI RMF mapped
- NCSC CAF aligned

## License

Apache 2.0

## Contact

- GitHub: https://github.com/CSOAI-ORG/csoai-static-deploy2
- Website: https://csoai.org
