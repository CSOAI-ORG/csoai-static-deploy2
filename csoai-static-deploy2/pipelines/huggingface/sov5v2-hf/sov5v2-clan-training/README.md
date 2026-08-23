---
language:
  - en
tags:
  - sovereign-ai
  - training-data
  - clan
license: apache-2.0
---

# SOV5v2 Clan Training Dataset

4,757 examples organized into 8 clans for sovereign AI training.

## Clans

| Clan | Examples | Description |
|------|----------|-------------|
| Compliance | 1,128 | EU AI Act, GDPR, ISO 42001 |
| Defence | 1,092 | AUKUS, DASA, NCSC, JSP 936 |
| Governance | 32 | BFT council, SIGIL chain, Care Floor |
| Procurement | 21 | G-Cloud, DSP, CCS |
| Intuition | 1,003 | World model, emergence, trends |
| Voice | 1,001 | Sovereign identity, privacy, ethics |
| General | 200 | Math, logic, code |
| Cross-family | 275 | Multi-domain reasoning |

## Format

Each example:
```json
{
  "instruction": "What is the BFT quorum?",
  "input": "",
  "output": "The BFT council requires 23 out of 33 votes (2/3 majority)."
}
```

## Usage

```python
from datasets import load_dataset
ds = load_dataset("CSOAI/sov5v2-clan-training")
```
