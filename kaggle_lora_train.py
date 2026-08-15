#!/usr/bin/env python3
"""kaggle_lora_train.py — LoRA fine-tuning of Mistral-7B on Kaggle T4 GPU.

Run this on Kaggle with:
  - GPU: T4 x1
  - Internet: ON
  - Upload honey_mistral.jsonl as dataset

Uses:
  - Mistral-7B-Instruct-v0.3
  - LoRA r=32, alpha=64
  - bf16 training (T4 supports bf16)
  - 4-bit quantization via QLoRA to fit in 16GB VRAM
"""
import os
import json
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "warning")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def main():
    # === Config ===
    BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
    # Try multiple possible paths
    possible_paths = [
        "/kaggle/input/datasets/nicktempleman/sov7-training-v2/honey_mistral.jsonl",
        "/kaggle/input/sov7-training-v2/honey_mistral.jsonl",
        "/kaggle/input/sov-training-data/honey_mistral.jsonl",
        "/kaggle/input/honey_mistral.jsonl",
    ]
    DATA_PATH = None
    for p in possible_paths:
        if os.path.exists(p):
            DATA_PATH = p
            break
    if DATA_PATH is None:
        # Try to find it dynamically
        import glob
        candidates = glob.glob("/kaggle/input/**/honey_mistral.jsonl", recursive=True)
        if candidates:
            DATA_PATH = candidates[0]
        else:
            print("ERROR: Could not find honey_mistral.jsonl in /kaggle/input/")
            print("Available files:")
            for root, dirs, files in os.walk("/kaggle/input"):
                for f in files:
                    print(f"  {os.path.join(root, f)}")
            sys.exit(1)
    OUTPUT_DIR = "/kaggle/working/lora_sov7"
    EPOCHS = 1
    BATCH_SIZE = 2
    GRAD_ACCUM = 4
    LR = 2e-4
    LORA_R = 32
    LORA_ALPHA = 64
    MAX_LEN = 1024
    USE_QLORA = True  # 4-bit quantization to fit T4 16GB

    print(f"=== SOV7 LoRA Training (Kaggle T4) ===")
    print(f"  base:    {BASE_MODEL}")
    print(f"  data:    {DATA_PATH}")
    print(f"  epochs:  {EPOCHS}  bs: {BATCH_SIZE}  lr: {LR}")
    print(f"  LoRA:    r={LORA_R} alpha={LORA_ALPHA}")
    print(f"  QLoRA:   {USE_QLORA}")

    import torch
    print(f"  cuda:    {torch.cuda.is_available()} ({torch.cuda.device_count()} GPUs)")
    if torch.cuda.is_available():
        print(f"  gpu:     {torch.cuda.get_device_name(0)}")
        print(f"  vram:    {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    # === Install deps (Kaggle has most, but just in case) ===
    try:
        import peft
        import trl
        import bitsandbytes
    except ImportError:
        print("Installing missing packages...")
        os.system("pip install -q peft trl bitsandbytes accelerate")

    from transformers import (
        AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from trl import SFTTrainer, SFTConfig
    from datasets import Dataset

    # === Load data ===
    print(f"\n[1/4] Loading data...")
    records = []
    for line in open(DATA_PATH):
        try:
            d = json.loads(line)
            q = d.get("q", "").strip()
            a = d.get("a", "").strip()
            if q and a:
                records.append({
                    "text": f"<s>[INST] {q} [/INST] {a}</s>"
                })
        except:
            continue
    print(f"  loaded {len(records)} examples")
    if not records:
        print("ERROR: no data")
        sys.exit(1)

    dataset = Dataset.from_list(records)
    print(f"  dataset size: {len(dataset)}")

    # === Load model ===
    print(f"\n[2/4] Loading base model {BASE_MODEL}...")
    model_kwargs = {
        "torch_dtype": torch.bfloat16,
        "device_map": "auto",
        "trust_remote_code": True,
    }

    if USE_QLORA:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        model_kwargs["quantization_config"] = bnb_config

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, **model_kwargs)

    if USE_QLORA:
        model = prepare_model_for_kbit_training(model)

    # === Apply LoRA ===
    print(f"\n[3/4] Applying LoRA...")
    lora_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # === Train ===
    print(f"\n[4/4] Training...")
    sft_config = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        learning_rate=LR,
        bf16=True,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        max_seq_length=MAX_LEN,
        report_to=[],
        seed=42,
        dataset_text_field="text",
        packing=False,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_config,
        train_dataset=dataset,
        tokenizer=tokenizer,
    )

    started = time.time()
    trainer.train()
    elapsed = time.time() - started
    print(f"  training done in {elapsed:.0f}s ({elapsed/60:.1f} min)")

    # === Save ===
    print(f"\nSaving adapter to {OUTPUT_DIR}/final...")
    os.makedirs(f"{OUTPUT_DIR}/final", exist_ok=True)
    model.save_pretrained(f"{OUTPUT_DIR}/final")
    tokenizer.save_pretrained(f"{OUTPUT_DIR}/final")
    print(f"  saved adapter: {OUTPUT_DIR}/final")

    # Save merged for Ollama
    print(f"  merging LoRA into base...")
    merged = model.merge_and_unload()
    merged_path = f"{OUTPUT_DIR}/merged"
    os.makedirs(merged_path, exist_ok=True)
    merged.save_pretrained(merged_path, safe_serialization=True)
    tokenizer.save_pretrained(merged_path)
    print(f"  saved merged: {merged_path}")

    print(f"\n=== DONE ===")
    print(f"  Total time: {elapsed/60:.1f} min")
    print(f"  Adapter: {OUTPUT_DIR}/final")
    print(f"  Merged: {OUTPUT_DIR}/merged")


if __name__ == "__main__":
    main()
