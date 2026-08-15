# sov5v2 Training

## Architecture
- Base: Qwen2.5-7B-Instruct
- LoRA: r=64, alpha=128, target=all-linear
- Training: SFT on R1-distilled reasoning traces
- Precision: bf16 (QLoRA 4-bit available)

## Dataset
- 4,757 clan-organized examples
- 8 specialist domains: compliance, defence, intuition, voice, general, auditability, governance, redline
- 12 Sovereign Pillars with curated prompts
- Quality gate: minimum 0.6 critic score on all pillars

## Training Script
```bash
python3 sov7_lora_train.py \
  --base mistralai/Mistral-7B-Instruct-v0.3 \
  --data /workspace/sov-sov7/training/final_training_data.jsonl \
  --out /workspace/sov-sov7/lora_sov7 \
  --epochs 1 --bs 2 --lr 2e-4 \
  --lora_r 64 --lora_alpha 128
```

## Hardware
- RunPod A40 (48GB VRAM) — primary
- RunPod H100 (80GB VRAM) — for 32B+ models
- Kaggle T4 (16GB) — evaluation only
