Title: SOV33 Training Data
Slug: nicholastempleman/sov33-training-data
---
# SOV33 Training Data

Combined training dataset for SOV33 sovereign AI model.

## Contents
- `merged_safety_chat.jsonl` — 2,436 safety training examples
- `distilled_groq70b.jsonl` — Distilled knowledge from Groq 70B
- `refusal_corpus.jsonl` — 207 refusal training examples
- `refusal_finetune.jsonl` — 124+ refusal fine-tuning examples

## Sources
- Anthropic HH-RLHF (harmless pairs)
- THUDM Safety-Prompts (bilingual safety)
- Microsoft Do-Not-Answer (EU AI Act aligned)
- Deepset prompt-injections
- xTRam1 safe-guard-prompt-injection
- Groq 70B distillation (our teacher model)

## Usage
```python
from datasets import load_dataset
ds = load_dataset("nicholastempleman/sov33-training-data")
```