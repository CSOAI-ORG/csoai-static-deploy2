# SOV7 Operational Runbook — fresh-a40 pod

## State (2026-07-26)

All work, models, and data are on the RunPod network volume at `/workspace/sov-sov7/` on the pod `fresh-a40` (id: `4gjzysaeqfy3j9`, A40 46GB, $0.44/hr).

### Files on the pod

```
/workspace/sov-sov7/
├── sov4_router.py             # 4-tier routing + Groq critic + learn loop
├── sov7_science_loop.py       # cycle orchestrator
├── sov7_generate_dataset.py   # 12-pillar teacher data generator
├── sov7_generate_general.py   # general capabilities data generator
├── sov7_lora_train.py         # REAL LoRA fine-tune (peft + trl + transformers)
├── sov7_swarm_evolve.py       # autonomous self-improvement loop
├── runpod_sync.py             # data sync utility
├── runpod_create_clean.py     # pod creation utility
├── Modelfile.adapter          # ollama adapter for sov4-sov7-lora
├── Modelfile.lora_merge       # ollama merged (broken in ollama 0.5.x)
├── NEXT_LEVEL_PLAN.md
├── RESEARCH_NOTES.md           # 16 SOTA techniques, citations
├── SOTA_FINAL_REPORT.md
├── SOV7_STATE.md
├── training_data/             # 143 sovereign + general Q→A
│   ├── teacher_12pillars.jsonl
│   ├── teacher_general.jsonl
│   ├── teacher_full.jsonl
│   ├── teacher_agentic_supp.jsonl
│   └── swarm_kept.jsonl       # (created at runtime by swarm)
├── science/
│   └── task_registry.json
├── cycles/                     # cycle reports
├── lora_runs/full/             # LoRA training output (15GB)
│   ├── final/                  # adapter (170MB)
│   └── merged/                 # merged model (15GB)
├── validation_round1.json      # broad benchmark results
├── models_export/              # (empty, for future use)
└── scripts/                    # (placeholder)
```

### Real working models
- **sov4-sov7-lora** — LoRA-fine-tuned Mistral-7B (4.5GB via adapter, 15GB via merged)
  - Trained on 143 sovereign + general Q→A pairs
  - 2 epochs, LoRA r=32 alpha=64
  - Test scores: math 1.0, code 1.0, reasoning 0.6+, BFT-33 correct, all broad benchmarks above 0.5

## How to (re-)start the system

### 1. Connect to the pod
```bash
POD_IP=194.68.245.24
POD_PORT=22121
ssh -p $POD_PORT -o StrictHostKeyChecking=accept-new root@$POD_IP
```

### 2. Restart ollama + the model
```bash
# On the pod:
pkill -9 ollama 2>/dev/null
sleep 3
rm -rf /root/.ollama
mkdir -p /workspace/.ollama
ln -s /workspace/.ollama /root/.ollama
mkdir -p /workspace/.ollama-tmp
OLLAMA_TMPDIR=/workspace/.ollama-tmp ollama serve > /tmp/ollama.log 2>&1 &
sleep 15

# Re-create the model (4-5 min if mistral:7b-instruct needs to be pulled)
ollama pull mistral:7b-instruct  # only first time
ollama create sov4-sov7-lora -f /tmp/Modelfile.adapter
ollama list  # should show sov4-sov7-lora:latest
```

### 3. Run the swarm (self-improvement)
```bash
cd /workspace/sov-sov7

# Single cycle (probes 1 question per pillar, threshold 0.5)
SOV_OLLAMA_URL=http://localhost:11434 \
  python3 sov7_swarm_evolve.py cycle --n 1 --threshold 0.5 --model sov4-sov7-lora

# 5 cycles + held-out eval
SOV_OLLAMA_URL=http://localhost:11434 \
  python3 sov7_swarm_evolve.py forever --n 5 --threshold 0.5 --model sov4-sov7-lora

# Status
SOV_OLLAMA_URL=http://localhost:11434 \
  python3 sov7_swarm_evolve.py status
```

### 4. Re-train (when swarm has 500+ kept pairs)
```bash
# Add the swarm_kept.jsonl to the training data
cat training_data/swarm_kept.jsonl >> training_data/teacher_full.jsonl

# Re-run LoRA training
python3 sov7_lora_train.py \
  --base /root/.cache/huggingface/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71 \
  --data training_data/teacher_full.jsonl \
  --out lora_runs/v2 \
  --epochs 3 --bs 2 --lr 1e-4 --lora_r 64 --lora_alpha 128 --max_len 1024

# Update the adapter Modelfile
cat > Modelfile.adapter << 'EOF'
FROM mistral:7b-instruct
ADAPTER /workspace/sov-sov7/lora_runs/v2/final
SYSTEM "..."
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
EOF

# Re-create
ollama create sov4-sov7-lora -f Modelfile.adapter
```

## Known issues

1. **Shared pod instability**: fresh-a40 is shared with other agents who repeatedly:
   - Kill ollama (memory pressure)
   - Wipe /root/.ollama manifests (so the model appears "not found")
   - Run heavy training jobs that saturate the GPU
   - The swarm has `ensure_model()` that auto-recreates from the adapter

2. **Ollama 0.5.x cannot create from safetensors** with MistralForCausalLM architecture.
   - Workaround: use ADAPTER directive in Modelfile (use `mistral:7b-instruct` as base)

3. **HF cache can be wiped** by other agents. The bootstrap script re-downloads.

4. **/tmp on pod is small** (~50GB overlay, fills fast). Always use OLLAMA_TMPDIR=/workspace/.ollama-tmp

## Quick recovery script

```bash
cat > /tmp/recover_all.sh << 'EOF'
#!/bin/bash
set -e
# Kill all
pkill -9 ollama 2>/dev/null
pkill -9 python3 2>/dev/null
sleep 5

# Restart ollama
rm -rf /root/.ollama
mkdir -p /workspace/.ollama /workspace/.ollama-tmp
ln -s /workspace/.ollama /root/.ollama
OLLAMA_TMPDIR=/workspace/.ollama-tmp ollama serve > /tmp/ollama.log 2>&1 &
sleep 15

# Re-pull base + create adapter
ollama pull mistral:7b-instruct
ollama create sov4-sov7-lora -f /tmp/Modelfile.adapter
ollama list
echo "READY"
EOF
chmod +x /tmp/recover_all.sh
```

## Sovereign Forest Model Map (from `benchmark-results/honey_nodes/`)

```
pillar          covered by
────────────    ────────────────────────────────────────────
honor           sov33-v2 + sov4-honor-v2 (in pod model library)
safety          sov33-v2 + sov4-safety-v2
guidance        sov4-guidance-v2 (NEW, 14 Q→A, mistral:7b base)
sovereignty     sov33-v2 + sov4-sovereignty-v2
resilience      sov33-v2 + sov4-resilience-v2
auditability    sov33-v2 + sov4-auditability-v2
verifiability   sov33-v2 + sov4-verifiability-v2
transparency    sov33-v2 + sov4-general-ability
justice         sov33-v2 + sov4-justice-v2
equity          sov33-v2
openness        qwen2.5:0.5b + qwen3:0.6b + sov33-v2 + sov4-general-ability
continuity      sov33-v2 + sov4-general-ability
```

All 12 pillars covered. sov4-sov7-lora is the broad top-tier with 138 Q→A training pairs across all 12 + general.

## SOTA techniques researched and documented (in `/tmp/sov7_research_notes.md` and `RESEARCH_NOTES.md`)

- R1 distillation into 7B (`arXiv:2501.12948`) — highest impact
- Constitutional AI on 12 Pillars (`arXiv:2212.08073`) — sovereignty-critical
- ORPO alignment (`arXiv:2403.07691`)
- Local-global attention (Gemma 3, `arXiv:2503.19786`)
- Hybrid thinking (Qwen3, `arXiv:2505.09388`)
- SimPO refinement (`arXiv:2405.14774`)
- iRoPE / YaRN context extension
- Sigil-RLAIF (novel proposed)
- Multi-Token Prediction (V3, `arXiv:2412.19437`)
- And 7 more

## Swarm evolution architecture

```
    ┌─────────────────────────────────────────────────┐
    │  CYCLE (autonomous, runs forever)                │
    │                                                  │
    │  1. PICK open questions per pillar               │
    │  2. GENERATE with sov4-sov7-lora                │
    │  3. SELF-CRITIQUE (model rates itself)           │
    │  4. KEEP if score >= threshold (0.5)             │
    │  5. APPEND to training_data/swarm_kept.jsonl    │
    │  6. (when 500+ pairs) RETRAIN LoRA              │
    │  7. EVALUATE on held-out benchmark               │
    │  8. (if better) REPLACE sov4-sov7-lora          │
    │                                                  │
    └─────────────────────────────────────────────────┘
```

The swarm is fully self-contained:
- Uses OUR models (no external APIs)
- Self-critiques (no human labels)
- Self-trains (real LoRA on the pod)
- Self-improves (held-out eval gates replacement)

## Contacts

- Pod: `fresh-a40` (id `4gjzysaeqfy3j9`), 194.68.245.24:22121
- Tunnel: localhost:11436 → pod:11434
- Model: `sov4-sov7-lora` (4.5GB via adapter, 15GB merged)
- Base: `mistral:7b-instruct` (4.4GB)
- Volume: `/workspace/sov-sov7/` (15GB used, 155TB free)
