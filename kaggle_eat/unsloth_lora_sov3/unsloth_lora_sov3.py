#!/usr/bin/env python3
"""
CSOAI LoRA Training on 14k deduped SOV dataset (unsloth on T4, peft fallback on P100)
Runs on Kaggle free GPU (T4 or P100, assigned at Kaggle's discretion)

Pipeline:
  0. Detect assigned GPU BEFORE importing torch (P100 = sm_60 needs a pinned stack;
     current unsloth/torch builds need sm_70+ and crash with
     cudaErrorNoKernelImageForDevice on P100)
  1. Load 14k deduped training data (master_alpaca + synth + honey + sharegpt-normalized)
  2. Format for instruction tuning (alpaca prompt)
  3. Apply LoRA — unsloth FastLanguageModel on T4, peft fallback on P100
  4. Train (~30-60 min)
  5. Export GGUF for Ollama (T4 only; P100 fallback exports the adapter only)
  6. Save results to /kaggle/working/unsloth_training_results.json
"""

import os
import json
import subprocess
import sys
import time
from pathlib import Path

print("=" * 70)
print("CSOAI LoRA Training on 14k deduped SOV dataset (unsloth on T4, peft fallback on P100)")
print("=" * 70)
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 0: Environment setup + GPU detect (BEFORE any torch import)
# ─────────────────────────────────────────────────────────────────────
print("Phase 0: Environment setup")
print(f"  Python: {os.sys.version.split()[0]}")
print(f"  CUDA available: {os.system('nvidia-smi 2>/dev/null') == 0}")

# Kaggle assigns P100 (sm_60) or T4 (sm_75) at its own discretion, and the
# current image torch supports sm_70+ only. Detect the card BEFORE importing
# torch and pick a compatible stack.
try:
    GPU_NAME = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]
    ).decode().strip()
except Exception:
    GPU_NAME = ""
IS_P100 = "P100" in GPU_NAME
print(f"  Assigned GPU: {GPU_NAME or 'none'}")
print(f"  Stack: {'peft fallback (P100/sm_60)' if IS_P100 else 'unsloth (T4/sm_75)'}")
print()

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
MAX_SEQ_LENGTH = 2048

# ─────────────────────────────────────────────────────────────────────
# Phase 1: Install training stack
# ─────────────────────────────────────────────────────────────────────
if IS_P100:
    # sm_60: Pascal support exists up to torch 2.6 (dropped in 2.7);
    # transformers 4.52 needs torch >= 2.5 (ALL_PARALLEL_STYLES guard).
    print("Phase 1: Installing P100-compatible stack (torch 2.5.1 cu121 + peft)")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-q",
        "torch==2.5.1", "torchvision==0.20.1",
        "--index-url", "https://download.pytorch.org/whl/cu121",
    ])
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-q",
        "transformers==4.52.4", "peft==0.13.2", "datasets==2.21.0",
        "accelerate==1.6.0",
    ])
else:
    print("Phase 1: Installing Unsloth")
    os.system("pip install --quiet unsloth 2>&1 | tail -1")
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 2: Load 14k training data
# ─────────────────────────────────────────────────────────────────────
print("Phase 2: Loading 14k training data")

DATA_DIR = Path("/kaggle/input/csoai-sov-training-data-14k")
if not DATA_DIR.exists():
    # Fallback to /kaggle/working if input dataset not found
    DATA_DIR = Path("/kaggle/working")

training_files = [
    "master_alpaca.jsonl",
    "synth_2026-07-30.jsonl",
    "unsloth_synth_2026-07-31.jsonl",
    "honey_training_data_alpaca.jsonl",
    "master_sharegpt_alpaca.jsonl",
]

all_examples = []
for f in training_files:
    fpath = DATA_DIR / f
    if fpath.exists():
        with fpath.open() as fh:
            count = 0
            for line in fh:
                if line.strip():
                    try:
                        ex = json.loads(line)
                        # Normalize format
                        if "instruction" in ex and "output" in ex:
                            all_examples.append({
                                "instruction": ex["instruction"],
                                "input": ex.get("input", ""),
                                "output": ex["output"],
                            })
                        elif "prompt" in ex:
                            all_examples.append({
                                "instruction": ex["prompt"],
                                "input": "",
                                "output": ex.get("response", ex.get("behaviour", "")),
                            })
                        count += 1
                    except json.JSONDecodeError:
                        pass
            print(f"  Loaded {count} examples from {f}")

print(f"\n  Total examples: {len(all_examples)}")

# Subsample to 5000 for free-tier GPU memory (Kaggle T4/P100 LoRA training)
import random
random.seed(42)
if len(all_examples) > 5000:
    all_examples = random.sample(all_examples, 5000)
    print(f"  Subsampled to {len(all_examples)} examples for T4/P100 training")

print()

# ─────────────────────────────────────────────────────────────────────
# Phase 3: Load model
# ─────────────────────────────────────────────────────────────────────
if IS_P100:
    print("Phase 3: Loading model via transformers (P100 fallback)")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto",
    )
else:
    print("Phase 3: Loading Unsloth FastLanguageModel")

    from unsloth import FastLanguageModel
    import torch

    # Use Qwen2.5-0.5B (379MB substrate that fits 4-bit on T4 with 12.8GB VRAM)
    DTYPE = None  # Auto detect (float16 for T4)
    LOAD_IN_4BIT = True

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        dtype=DTYPE,
        load_in_4bit=LOAD_IN_4BIT,
    )
print(f"  Model loaded: {MODEL_NAME}")
print(f"  Vocab size: {len(tokenizer)}")
print(f"  Device: {next(model.parameters()).device}")
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 4: Apply LoRA
# ─────────────────────────────────────────────────────────────────────
print("Phase 4: Applying LoRA")

if IS_P100:
    from peft import LoraConfig, get_peft_model

    lora_config = LoraConfig(
        r=16,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0,
        bias="none",
        task_type="CAUSAL_LM",
        # 2026-08-02 backlog #2: PiSSA init (SVD of base weights) — 30-50% faster
        # convergence inside fixed free-GPU windows. A/B vs prior gaussian init.
        init_lora_weights="pissa",
    )
    model = get_peft_model(model, lora_config)
else:
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,  # LoRA rank
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        # 2026-08-02 backlog #2: PiSSA init — see P100 branch comment above.
        init_lora_weights="pissa",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )

trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
all_params = sum(p.numel() for p in model.parameters())
print(f"  Trainable params: {trainable_params:,} ({100 * trainable_params / all_params:.4f}%)")
print(f"  Total params: {all_params:,}")
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 5: Format training data
# ─────────────────────────────────────────────────────────────────────
print("Phase 5: Formatting training data")

from datasets import Dataset

# Format as alpaca prompt
alpaca_prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

def format_example(ex):
    return alpaca_prompt.format(
        ex["instruction"],
        ex.get("input", ""),
        ex["output"]
    ) + tokenizer.eos_token

formatted = [format_example(ex) for ex in all_examples]
dataset = Dataset.from_dict({"text": formatted})
print(f"  Formatted {len(formatted)} examples")
print(f"  Sample: {formatted[0][:200]}...")
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 6: Train
# ─────────────────────────────────────────────────────────────────────
if IS_P100:
    print("Phase 6: Training with transformers Trainer (P100 fallback)")

    from transformers import DataCollatorForLanguageModeling, Trainer, TrainingArguments

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=1024,
        )

    tokenized_dataset = dataset.map(
        tokenize, batched=True, remove_columns=["text"]
    )

    trainer = Trainer(
        model=model,
        train_dataset=tokenized_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
        args=TrainingArguments(
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            warmup_steps=10,
            num_train_epochs=1,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            output_dir="/kaggle/working/lora_outputs",
            report_to="none",
        ),
    )
else:
    print("Phase 6: Training with UnslothTrainer")

    from unsloth import UnslothTrainer, UnslothTrainingArguments

    trainer = UnslothTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=MAX_SEQ_LENGTH,
        args=UnslothTrainingArguments(
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            warmup_steps=10,
            num_train_epochs=1,
            learning_rate=2e-4,
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=10,
            output_dir="/kaggle/working/lora_outputs",
            save_strategy="steps",
            save_steps=500,
            report_to="none",
        ),
    )

start_time = time.time()
print(f"  Starting training...")
trainer_stats = trainer.train()
end_time = time.time()

training_time = end_time - start_time
print(f"\n  Training completed in {training_time / 60:.1f} minutes")
print(f"  Trainable params: {trainer_stats.training_loss}")
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 7: Export LoRA adapter
# ─────────────────────────────────────────────────────────────────────
print("Phase 7: Exporting LoRA adapter")

adapter_dir = "/kaggle/working/sov3-lora-adapter"
model.save_pretrained(adapter_dir)
tokenizer.save_pretrained(adapter_dir)
print(f"  Adapter saved to: {adapter_dir}")
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 8: Merge LoRA + export GGUF for Ollama (T4/unsloth only)
# ─────────────────────────────────────────────────────────────────────
if IS_P100:
    print("Phase 8: Merge + GGUF export")
    print("  GGUF export skipped on P100 fallback — adapter only")
    merged_dir = None
    gguf_dir = None
else:
    print("Phase 8: Merging LoRA + exporting GGUF for Ollama")

    # Merge LoRA into base model
    merged_dir = "/kaggle/working/sov3-merged"
    model.save_pretrained_merged(merged_dir, tokenizer, save_method="merged_16bit")
    print(f"  Merged model saved to: {merged_dir}")

    # Export GGUF for Ollama
    gguf_dir = "/kaggle/working/sov3-gguf"
    model.save_pretrained_gguf(gguf_dir, tokenizer, quantization_method="q4_k_m")
    print(f"  GGUF model saved to: {gguf_dir}")
print()

# ─────────────────────────────────────────────────────────────────────
# Phase 9: Write results to benchmark-results/
# ─────────────────────────────────────────────────────────────────────
print("Phase 9: Writing results")

results = {
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "gpu": GPU_NAME,
    "trainer": "peft-fallback" if IS_P100 else "unsloth",
    "model": MODEL_NAME,
    "dataset_size": len(all_examples),
    "lora_rank": 16,
    "lora_alpha": 16,
    "max_seq_length": MAX_SEQ_LENGTH,
    "training_time_minutes": training_time / 60,
    "trainable_params": trainable_params,
    "total_params": all_params,
    "trainable_pct": 100 * trainable_params / all_params,
    "adapter_dir": adapter_dir,
    "merged_dir": merged_dir,
    "gguf_dir": gguf_dir,
    "training_loss": float(trainer_stats.training_loss) if hasattr(trainer_stats, "training_loss") else None,
}

with open("/kaggle/working/unsloth_training_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"  Results saved to: /kaggle/working/unsloth_training_results.json")
print()

# ─────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────
print("=" * 70)
print("Training Summary")
print("=" * 70)
print(f"  GPU: {GPU_NAME} ({'peft-fallback' if IS_P100 else 'unsloth'})")
print(f"  Model: {MODEL_NAME}")
print(f"  Dataset: 14k deduped SOV examples (subsampled to 5000 for free-tier GPU)")
print(f"  LoRA: rank={16}, alpha={16}")
print(f"  Trainable params: {trainable_params:,} ({100 * trainable_params / all_params:.4f}%)")
print(f"  Training time: {training_time / 60:.1f} minutes")
if gguf_dir:
    print(f"  Output: GGUF at {gguf_dir}")
else:
    print(f"  Output: adapter only at {adapter_dir} (GGUF skipped on P100 fallback)")
print()
print("Next steps:")
if gguf_dir:
    print("  1. Download the GGUF adapter from Kaggle")
    print("  2. Copy to Ollama: ollama create sov3-lora -f Modelfile")
    print("  3. Run on M4: ollama run sov3-lora")
    print("  4. Wire to sov-gateway as upstream")
else:
    print("  1. Download the LoRA adapter from Kaggle")
    print("  2. Merge + convert to GGUF on a sm_70+ machine (M4 local or T4 rerun)")
    print("  3. Copy to Ollama: ollama create sov3-lora -f Modelfile")
print()
