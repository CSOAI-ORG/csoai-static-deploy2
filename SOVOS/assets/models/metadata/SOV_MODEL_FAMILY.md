---
language:
- en
license: apache-2.0
tags:
- sovereign-ai
- governance
- eu-ai-act
- bft-council
- sigil
- care-floor
- uk-defence
---

# SOV Model Family — Complete Documentation

## Architecture Overview

SOV33 is a UK-sovereign AI substrate built by CSOAI Ltd (UK Companies House 16939677). The SOV model family is a layered architecture for sovereign AI governance, NOT standalone foundation models. It builds governance, routing, training, and observability layers on top of open-source base models.

```
┌─────────────────────────────────────────────────────────────────┐
│  SOV7 — Science Loop (Self-Improvement Orchestrator)            │
│  Auto-cycling: route → worker → critic → record → improve       │
├─────────────────────────────────────────────────────────────────┤
│  SOV1 — Emergence Spine (L0 Routing Substrate)                  │
│  96 emergence nodes, 10,992 bloodline records, 4 lineages       │
├─────────────────────────────────────────────────────────────────┤
│  SOV4 — Fluid Layer (Router / Water→Milk→Honey)                 │
│  Cross-family merging, BFT-33 governance, J-Space               │
├─────────────────────────────────────────────────────────────────┤
│  SOV3 — Sovereign Substrate (Foundation Layer)                  │
│  127 tools, 6 NNs, MCP mesh, 12 mindsets                       │
├─────────────────────────────────────────────────────────────────┤
│  SOV33 — Public Surface (61-Model Registry)                     │
│  5 routing groups, SIGIL, BFT-33, Care Floor 0.95              │
├─────────────────────────────────────────────────────────────────┤
│  SOV333 — Capstone / Deep Tier (Aspiration)                     │
│  30B-70B models, 10 OWEM components (7/10 built)               │
├─────────────────────────────────────────────────────────────────┤
│  SOV5 — Honey Data Lake (Data/Training Layer)                   │
│  10,992 bloodline, 11 RAG corpora, 4,000 synthetic pairs       │
├─────────────────────────────────────────────────────────────────┤
│  SOV6 — Macroscope (Observability Layer)                        │
│  12 entry points, 8 views, 6 visual MCPs                       │
├─────────────────────────────────────────────────────────────────┤
│  SOV-18 — JEEVES Vault (Operations / Automation)                │
│  Cron jobs, heartbeats, 24h autonomous operation                │
└─────────────────────────────────────────────────────────────────┘
```

## Model Details

### SOV1 — Emergence Spine

**Role:** L0 routing substrate — the foundational backbone from which all capabilities grow.

**Architecture:**
- 4 frozen open-source base "lineages": Qwen, Llama, DeepSeek, Mistral
- 10,992 bloodline records (28% qwen, 34% llama, 19% deepseek, 19% mistral)
- Routes per-suite to 96 emergence nodes (12 OWEM hives × 8 swarms)
- Cost-aware: local-first on UK A40 cluster

**Key Files:**
- `sov1-emergence-spine.html` — canonical definition
- `sov1_projector.py`, `sov1_compiler.py`, `sov1_hypernet.py`
- `sov1_bloodline.jsonl` — 10,992 records

---

### SOV3 — Sovereign Substrate

**Role:** The sovereign AI substrate — foundation layer with 127 tools and 6 trained neural networks.

**Architecture (4 layers):**
- L1: SOV³ (super-substrate) — sovereign-by-construction crown
- L2: SOV3 (substrate) — 127 tools, 6 trained NNs, BFT council
- L3: CSOAI (org) — 33-agent BFT council + Watchdog + 36 industry hives
- L4: Coigndaltion (cornerstone) — Mamba-2 cognition + cross-walk engine

**Key Files:**
- `SOV3_OOWM_BRIEFING.html` — full briefing (14 sections)
- `SOV3_OOWM_KNOWLEDGE_TAB.html` — knowledge base (870 lines)
- `sovereign_api.py` — sovereign API implementation

---

### SOV33 — Public Surface

**Role:** The user-facing product surface. 61-model registry with 5 routing groups.

**Architecture:**
- 5 routing groups: compliance, defense, intuition, voice, general
- 4 scopes: SMALL, MEDIUM, LARGE, CENTRE
- 4-brain split: LEFT (fast/offline) + RIGHT (deep/online)
- Triangle topology: 3 small OWEMs + 1 SOV33-cubed center
- 12 Sovereign Pillars as specialists
- Care-floor 0.95, Ed25519 SIGIL, BFT-33 quorum (23/33)

**Key Files:**
- `SOV33_INDEX.html`, `SOV33_MASTER_INDEX.html`
- `sov33-capability-registry.json` — 69 MCPs, 364 tools
- `sov33_lora_training.py`, `grpo_train.py`

---

### SOV333 — Capstone

**Role:** The aspirational deep tier — 30B-70B models for queries too hard for SOV33's 0.5B models.

**Architecture (10 OWEM Components):**
1. OWEM Core Layers (5-layer SOV33 v3) — BUILT
2. Fluid Pyramid Architecture — BUILT
3. 4-Brain Hybrid Cascade — STUB
4. SSD Expert-Streaming Pipeline — PROXY-MEASURED (25.2x speedup)
5-10. Various additional components (7/10 built, 3/10 staged)

**Key Files:**
- `SOV333_OWEM_CHECKLIST.html` — 10-component checklist
- `SOV333_CAPSTONE_PORTAL.html` — capstone portal

---

### SOV4 — Fluid Layer

**Role:** The routing, transformation, and continuous-learning layer.

**Architecture:**
- WATER (frozen base): Qwen2.5:0.5B, frozen
- MILK (sovereign adapters): QLoRA-trained adapters
- HONEY (fluid live): Continuous-learning sovereign model
- J-Space: Silent global workspace
- Sov-Space: Sovereign internal representations
- 12 Pillar Modelfiles (honor, safety, guidance, etc.)

**Key Files:**
- `SOV4_FLUID_LIVE.html` — canonical definition
- `sov4_router.py` — THE core router
- `sov4_pillars/Modelfile.sov4-*` — 12 pillar models

---

### SOV5 — Honey Data Lake

**Role:** The persistent data lake consolidating all accumulated knowledge.

**Architecture:**
- 12 data entry points
- 8 sovereign priorities
- 11 RAG corpora (AUKUS, EU AI Act, GDPR, ISO 42001, NCSC CAF, NATO DIANA, G-Cloud 14, UK AISI, Cyber Essentials, Defence, Sovereign Architecture)
- 10,992 bloodline records
- 4,000 synthetic training pairs

**Key Files:**
- `sov5-honey-dashboard.html` — canonical definition
- `sov5_service.py`, `sov5_visual_router.py`
- `sovereign_synth_50k.jsonl` — training data

---

### SOV6 — Macroscope

**Role:** Visual + analytical observability over the entire substrate.

**Architecture:**
- 12 entry points × 8 panorama views × 6 visual MCPs
- 13 emergence models (logic, ethics, aesthetics, etc.)
- Cesium 3D Globe, J-Space Forest Portal, Federation Layer

**Key Files:**
- `sov6-macroscope.html` — canonical definition
- `sov6.py`, `sov6_macroscope.py`
- `sov6_emergence_registry.json` — 13 emergence models

---

### SOV7 — Science Loop

**Role:** Self-improvement orchestrator that closes the SOV1 spine.

**Architecture:**
- Route → Worker → Critic → Record cycle
- Auto-cycling with avoid-list refresh
- Master SIGIL receipt on each cycle

**Key Files:**
- `sov7_science_loop.py` — core orchestrator (255 lines)
- `sov7_cycles/` — cycle output directory

---

## Benchmark Results

### AGI Bench (64 tasks)

| Model | Total | Reasoning | Math | Coding | Agentic | General | Sovereign |
|-------|-------|-----------|------|--------|---------|---------|-----------|
| SOV33-v2 | **93.75%** | 80% | 90% | 100% | 100% | 100% | 87.5% |

### Sovereign Bench (25 tasks)

| Model | Total | Compliance | Defence | Sovereign | Logic | Math | General |
|-------|-------|------------|---------|-----------|-------|------|---------|
| SOV33-enhanced | **96%** | 100% | 100% | 90% | 100% | 100% | 100% |

### A40 Leaderboard (14 models, RunPod)

| Model | Std | Sov | Overall |
|-------|-----|-----|---------|
| **sov5v2** | 100 | 92 | **96** |
| sov6v2 | 100 | 83 | 93 |
| sov6max | 100 | 75 | 89 |
| sov6 | 100 | 75 | 89 |
| sov5-clan-trained | 100 | 67 | 85 |
| qwen2.5:3b | 100 | 67 | 85 |
| sov33-better3b | 80 | 83 | 81 |
| sov5 | 100 | 58 | 81 |
| sov33-master-v3 | 67 | 92 | 78 |
| sov33-master-v2 | 80 | 58 | 70 |
| llama3.2:3b | 93 | 33 | 67 |
| qwen3:30b-a3b | 67 | 58 | 63 |
| qwen2.5:0.5b | 60 | 50 | 56 |
| deepseek-coder:1.3b | 0 | 25 | 11 |

### Tempo Benchmark (qwen2.5:0.5b)

| Benchmark | Score |
|-----------|-------|
| MMLU-Pro | 68.6% |
| GSM8K | 80.0% |
| HumanEval | 100% |
| MATH | 93.3% |
| ARC-Challenge | 66.7% |
| HellaSwag | 73.3% |
| TruthfulQA | 64.0% |
| **Composite** | **62.7%** |

### Sovereign Adapter Impact

| Model | Compliance | Defence | Composite |
|-------|------------|---------|-----------|
| qwen2.5:0.5b (base) | 75% | 0% | 47.1% |
| sov33-master-v2 | 100% | 100% | **83.3%** |
| **Improvement** | +25pp | +100pp | **+36.2pp** |

### GovBench v8 (Byzantine Safety, 57 prompts)

| Model | Params | Harm Detection | Overblock | Accuracy | Composite |
|-------|--------|---------------|-----------|----------|-----------|
| **qwen2.5:3b** | 3.1B | 100% | 0% | **100%** | **100%** |
| **sov6v2** | 3.1B | 100% | 0% | **100%** | **100%** |
| sov5v2 | 3.1B | 100% | 10% | 98.2% | 83.2% |
| qwen2.5:0.5b | 494M | 0% | 0% | 0% | 0% |

**Key Finding:** 3B models achieve 100% safety classification. 0.5B models fail completely.

### Ultimate Benchmark (81 prompts, A40)

| Model | General | Math | Compliance | Defence | Governance | Safety | Coding | **Overall** |
|-------|---------|------|------------|---------|------------|--------|--------|-------------|
| qwen2.5:3b (base) | 90% | 100% | 20% | 0% | 0% | 100% | 100% | **62%** |
| **sov-ultimate** | 90% | 100% | **90%** | **90%** | **100%** | **100%** | 100% | **95%** |

**+33pp improvement** over base model via knowledge injection.

---

## Key Differentiators

1. **Open Source**: Only sovereign AI platform that is fully open-source
2. **UK Sovereign**: UK-based sovereign AI substrate
3. **Auditability**: Ed25519 SIGIL on every response
4. **Governance**: BFT-33 Byzantine consensus (23/33 quorum)
5. **Cost**: £0-£6K/month (vs £100K+/year for proprietary alternatives)
6. **EU AI Act**: Article 50 compliance built-in

---

## Training Pipeline

### 1. Data Preparation (SOV5)

```bash
# Prepare learning data
python3 prepare_learning_data.py

# Generate synthetic corpus
python3 generate_sovereign_corpus.py
```

### 2. GRPO Training (Process Rewards)

```bash
# On RunPod (A40 GPU)
python3 grpo_train.py --base Qwen/Qwen2.5-0.5B-Instruct \
  --data sovereign_synth_50k.jsonl --steps 100

# Local (Ollama mode)
python3 grpo_train.py --ollama qwen2.5:0.5b \
  --data sovereign_synth_50k.jsonl --steps 100
```

### 3. LoRA Fine-tuning

```bash
# Kaggle T4
python3 sov33_lora_training.py

# Production (with validation)
python3 train_fluid_lora.py --train data/train.jsonl --validation data/val.jsonl
```

### 4. Merge & Export

```bash
# Merge LoRA → Ollama
python3 merge_export.py --adapter sovereign_lora_adapter \
  --base Qwen/Qwen2.5-0.5B-Instruct --create-ollama

# Push to HuggingFace
python3 merge_export.py --adapter sovereign_lora_adapter \
  --base Qwen/Qwen2.5-0.5B-Instruct --push-hf user/sov33
```

### 5. Evaluation

```bash
# Unified eval CLI
python3 sov33_eval.py --model qwen2.5:0.5b --suite sovereign_compliance

# Full pipeline on RunPod
python3 batch_runpod.py full-pipeline --pod fresh-a40

# GovBench
python3 govbench_v6.py
```

---

## Deployment

### RunPod (Primary Compute)

```bash
# Check pods
python3 batch_runpod.py status

# Sync and train
python3 batch_runpod.py sync --pod fresh-a40
python3 batch_runpod.py train-grpo --pod fresh-a40 --steps 100

# Fetch results
python3 batch_runpod.py fetch --pod fresh-a40
```

### Ollama (Local Inference)

```bash
# Pull models
ollama pull sov33-master-v2
ollama pull sov4-general-ability
ollama pull sov5v2

# Run
ollama run sov33-master-v2
```

### HuggingFace Spaces

```bash
# Push Space
cd huggingface && git push
```

### Kaggle

```bash
# Push kernel
kaggle kernels push -p kaggle/kaggle_pack
```

---

## Citation

```bibtex
@software{sov33_2026,
  title={SOV33: UK Sovereign AI Substrate},
  author={CSOAI Ltd},
  year={2026},
  url={https://csoai.org}
}
```

## License

Apache 2.0

## Contact

- Website: https://csoai.org
- Company: CSOAI Ltd (UK Companies House 16939677)
- Hub: https://huggingface.co/csoai
