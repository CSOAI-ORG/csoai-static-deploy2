Title: RWKV-7 SOV33 — Free T4 Training
Slug: nicholastempleman/rwkv7-sov33-train
---
# RWKV-7 SOV33 — Free T4 Training

## What This Does
- Trains RWKV-7 1.6B on our sovereign training data using free Kaggle T4 GPU
- Uses LoRA (rank 16, alpha 32) for efficient fine-tuning
- Tests refusal behavior before/after training
- Saves adapter for deployment

## How to Use
1. Enable GPU T4×1 in Settings
2. Upload `merged_safety_chat.jsonl` as dataset
3. Run all cells
4. Download trained adapter

## Training Data
- 53 distilled examples from Groq 70B (96.4% accuracy)
- 2,436 safety training examples
- 207 refusal training examples
- Total: ~2,700 examples

## Expected Results
- Refusal rate: 0% → 75%+ (based on our testing)
- Knowledge retention: 60%+ on general tasks
- Training time: ~30 min on T4

## Architecture
- Base: RWKV-7 1.6B (linear attention, infinite context)
- LoRA: rank 16, alpha 32, dropout 0.05
- Target modules: attention, ffn
- Optimizer: paged_adamw_8bit
- Scheduler: cosine with warmup