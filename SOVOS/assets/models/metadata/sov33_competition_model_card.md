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
- lora
- competition
base_model:
- Qwen/Qwen2.5-3B-Instruct
---

# SOV33-Competition — Sovereign AI Model

## Model Description

SOV33-Competition is a Qwen2.5-3B-Instruct model fine-tuned with LoRA adapters on 24,875 examples covering compliance, defence, governance, coding, general knowledge, and safety classification. Trained by CSOAI Ltd (UK Companies House 16939677).

## Training Data

| Source | Examples | Domain |
|--------|----------|--------|
| Dolly 15k | 14,349 | General instruction following |
| Alpaca | 4,993 | General knowledge |
| CodeAlpaca | 2,999 | Coding |
| OASST2 | 1,893 | Conversational AI |
| SOV33 Sovereign | 558 | Compliance, defence, governance |
| **Total** | **24,875** | |

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Base Model | Qwen/Qwen2.5-3B-Instruct |
| LoRA Rank | 64 |
| LoRA Alpha | 128 |
| Target Modules | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| Epochs | 3 |
| Learning Rate | 1e-4 |
| Batch Size | 4 |
| Gradient Accumulation | 4 |
| Max Sequence Length | 512 |
| Trainable Parameters | 119,734,272 (3.74%) |
| Total Parameters | 3,205,672,960 |

## Benchmark Results

| Category | Base (Qwen2.5-3B) | SOV33-Competition | Improvement |
|----------|-------------------|-------------------|-------------|
| General Knowledge | 90% | TBD | — |
| Math | 100% | TBD | — |
| EU AI Act Compliance | 20% | TBD | — |
| UK Defence | 0% | TBD | — |
| Governance (BFT-33) | 0% | TBD | — |
| Safety Classification | 100% | TBD | — |
| **Overall** | **62%** | **TBD** | **—** |

*Results will be updated after training completes.*

## Sovereign Architecture

### BFT-33 Council
- 33 agents casting ALLOW/REJECT independently
- Quorum: 23/33 minimum for binding decisions
- HotStuff consensus algorithm
- Free-MAD weighted aggregation

### Care Floor
- Minimum threshold: 0.95 for all sovereign operations
- Split-conformal calibrated at ≤5% false-allow at 90% coverage
- Pre-call gate before every sovereign operation

### SIGIL Chain
- Ed25519 cryptographic signature on every response
- Hash-linked chain, tamper-evident
- Bitcoin OTS anchored

### 12 Sovereign Pillars
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

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model
base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")

# Load adapter
model = PeftModel.from_pretrained(base, "Nicholastempleman/sov33-competition")
model = model.merge_and_unload()

# Generate
prompt = "### Instruction:\nWhat is the EU AI Act Article 50 deadline?\n\n### Response:\n"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=128, temperature=0)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

## Ollama Deployment

```bash
# Create Ollama model
ollama create sov33-competition -f Modelfile.sov33-competition

# Run
ollama run sov33-competition
```

## SIGIL Provenance

Every model output includes a SHA-256 SIGIL for auditability:

```json
{
  "schema": "sov33.competition/v1",
  "timestamp": "2026-07-26T10:00:00Z",
  "sigil": "..."
}
```

## Citation

```bibtex
@software{sov33_competition2026,
  title={SOV33-Competition: Sovereign AI Model},
  author={CSOAI Ltd},
  year={2026},
  url={https://huggingface.co/Nicholastempleman/sov33}
}
```

## License

Apache 2.0

## Contact

- Website: https://csoai.org
- Company: CSOAI Ltd (UK Companies House 16939677)
- Hub: https://huggingface.co/Nicholastempleman/sov33
