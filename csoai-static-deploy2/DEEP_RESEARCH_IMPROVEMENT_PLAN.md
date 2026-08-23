# SOV DEEP RESEARCH — Improvement Plan from Open Source & White Papers

> Compiled 2026-07-27 from: DeepSeek-R1 (Nature 2025), HuggingFace TRL, Unsloth, AlpacaEval-LC, HuggingFace Daily Papers

---

## 1. TRAINING: GRPO > LoRA for Reasoning

**Source:** DeepSeek-R1 (arXiv:2501.12948, Nature 2025)

DeepSeek proved that pure RL (no human-labeled reasoning data) can incentivize emergent reasoning patterns: self-reflection, verification, dynamic strategy adaptation. Their method is **GRPO** (Group Relative Policy Optimization).

**Why it matters for SOV:**
- Current sov33-evolved is a static Modelfile adapter — no actual training
- ARC 50%, HellaSwag 50% = model doesn't reason, it memorizes
- GRPO can improve reasoning on small models (0.5B-8B) without expensive PPO

**Action:**
```python
# Using HuggingFace TRL (pip install trl)
from trl import GRPOTrainer
from trl.rewards import accuracy_reward

trainer = GRPOTrainer(
    model="Qwen/Qwen2.5-3B-Instruct",  # or sov33 base
    reward_funcs=accuracy_reward,
    train_dataset=sovereign_dataset,  # our 12-pillar Q&A pairs
)
trainer.train()
```

**Concrete steps:**
1. Build reward functions for sovereign knowledge (care floor, BFT, SIGIL, etc.)
2. Build reward functions for reasoning (ARC-style, GSM8K-style)
3. Run GRPO on Kaggle T4 (free) with TRL
4. Push trained model to Ollama

---

## 2. TRAINING SPEED: Unsloth (2x faster, 70% less VRAM)

**Source:** github.com/unslothai/unsloth (68.9k stars)

Unsloth provides:
- 2x faster training, 70% less VRAM
- GRPO with 80% less VRAM
- FP8 training on consumer GPUs
- 500K+ context training
- macOS Apple Silicon support (our M2!)

**Why it matters for SOV:**
- Can train on local M2 Mac (free, no GPU needed)
- Can train on Kaggle T4 with 2x speedup
- FP8 = can train larger models on same hardware

**Action:**
```bash
# Install Unsloth on Mac
curl -fsSL https://unsloth.ai/install.sh | sh

# Train with Unsloth + GRPO
unsloth studio -p 8888
# Or via code:
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained("Qwen/Qwen2.5-3B")
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=32)
```

---

## 3. EVALUATION: Length-Controlled AlpacaEval (0.98 Arena correlation)

**Source:** arXiv:2404.04475 (Stanford, 2024)

Key insight: controlling for length bias increases correlation with Chatbot Arena from 0.94 to 0.98. Most open-source models game benchmarks by being verbose.

**Why it matters for SOV:**
- Our EAT benchmarks may be biased by response length
- sov33-evolved generates long responses (explains ARC/HellaSwag failures)
- Length-controlled evaluation = more honest scores

**Action:**
1. Implement length-controlled win rate in our EAT pipeline
2. Add regression-based debiasing to benchmark scoring
3. Train models to be concise (penalize length in reward function)

---

## 4. REASONING: Chain-of-Thought + Self-Reflection

**Source:** DeepSeek-R1 emergent patterns

DeepSeek-R1 showed that RL-trained models develop:
- Self-reflection ("wait, let me reconsider")
- Verification ("checking my answer...")
- Dynamic strategy adaptation

**Why it matters for SOV:**
- sov33-evolved doesn't self-reflect on wrong answers
- Bat-and-ball failure = no verification step
- Cold-from-cold failure = no self-correction

**Action:**
1. Add `<think>` tags to SYSTEM prompt for reasoning tasks
2. Train with GRPO reward that penalizes wrong first answers
3. Implement self-verification in the model's thinking process

---

## 5. SOVEREIGN KNOWLEDGE: Synthetic Data Generation

**Source:** Current EAT pipeline + DeepSeek-R1 distillation

DeepSeek-R1 showed that large model reasoning can be distilled into smaller models. We can:
1. Use Groq 70B (free) to generate sovereign Q&A pairs
2. Use NVIDIA Llama-3.1-70B (free) to generate reasoning chains
3. Train sov33-evolved on this synthetic data with GRPO

**Action:**
```python
# Generate synthetic sovereign knowledge data
sovereign_topics = [
    "care floor = 0.95",
    "BFT council = 33 agents, 23/33 quorum",
    "SIGIL = Ed25519, hash-linked",
    "Article 0 = fee-for-service only",
    "EU AI Act Article 50 = 2 Aug 2026",
    "GDPR Article 33 = 72hr breach notification",
    # ... 50+ topics
]

# Use Groq to generate reasoning chains for each
# Train with GRPO + accuracy reward
```

---

## 6. BENCHMARK IMPROVEMENT: ARC & HellaSwag

**Current state:** ARC 50%, HellaSwag 50%

**Root cause:** The model is a 397MB Qwen-based model with a static SYSTEM prompt. It doesn't have the capacity for complex reasoning without actual training.

**Solution pipeline:**
1. Collect ARC-Challenge and HellaSwag training data
2. Generate reasoning chains with Groq 70B
3. Train with GRPO + accuracy reward on Kaggle T4
4. Evaluate with length-controlled metrics
5. Iterate until 80%+

**Target:** ARC 80%+, HellaSwag 80%+

---

## 7. MULTI-MODAL: Vision + Text (Future)

**Source:** HuggingFace Daily Papers (2026-07-27)

- "Scaling Native Multimodal Pre-Training From Scratch" (Tencent)
- Unsloth supports vision RL on consumer GPUs

**Why it matters for SOV:**
- V-space (visual artifacts) currently renders HTML, not actual images
- Could add vision capabilities to sov33 for visual reasoning
- Unsloth supports Gemma 4 vision + audio training

---

## 8. AGENTIC RL: Self-Play for Skill Acquisition

**Source:** "Skill Self-Play" (QwenBusinessUnit-Edu, 2026-07-27)

Key insight: models can co-evolve skills through self-play. Each skill challenges the others.

**Why it matters for SOV:**
- 12 OWEM specialists could self-play against each other
- Logic specialist challenges ethics specialist
- Each specialist improves by trying to beat the others

---

## IMPLEMENTATION PRIORITY

| Priority | Action | Impact | Effort | Cost |
|----------|--------|--------|--------|------|
| 1 | Install Unsloth + TRL on Mac | Foundation | 30min | $0 |
| 2 | Build sovereign reward functions | Enables GRPO | 2hr | $0 |
| 3 | Run GRPO on sov33 base (Kaggle T4) | ARC/HellaSwag +30% | 4hr | $0 |
| 4 | Add length-controlled evaluation | Honest benchmarks | 1hr | $0 |
| 5 | Generate synthetic sovereign data | Knowledge +40% | 2hr | $0 |
| 6 | Distill Groq 70B reasoning chains | Reasoning +20% | 3hr | $0 |
| 7 | Implement self-verification | Error correction | 2hr | $0 |
| 8 | Multi-modal V-space | Visual reasoning | 1day | $0 |

---

## KEY REPOS TO STUDY

1. **huggingface/trl** (18.9k stars) — GRPO, DPO, KTO trainers
2. **unslothai/unsloth** (68.9k stars) — 2x faster training, 70% less VRAM
3. **tatsu-lab/alpaca_eval** (2k stars) — Length-controlled evaluation
4. **deepseek-ai/DeepSeek-R1** — Pure RL reasoning
5. **Qwen/Qwen2.5** — Base model architecture

---

## WHITE PAPERS TO READ

1. DeepSeek-R1: Incentivizing Reasoning via RL (arXiv:2501.12948)
2. Length-Controlled AlpacaEval (arXiv:2404.04475)
3. GRPO: Group Relative Policy Optimization (DeepSeek)
4. DPO: Direct Preference Optimization (arXiv:2305.18290)
5. KTO: Kahneman-Tversky Optimization (arXiv:2402.01306)
