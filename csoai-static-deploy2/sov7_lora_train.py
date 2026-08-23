#!/usr/bin/env python3
"""sov7_lora_train.py — Real LoRA fine-tuning of Mistral-7B on RunPod A40.

Implements the SOTA recipe from research notes:
- SFT on R1-distilled reasoning traces
- LoRA r=64, alpha=128, target=all-linear
- bf16 training
- 4-bit quantization available if QLoRA needed

Saves adapter in Ollama-compatible format.
"""
import os
import json
import sys
import argparse
import time
from pathlib import Path

# Must be set BEFORE importing torch/transformers
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "warning")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="mistralai/Mistral-7B-Instruct-v0.3",
                    help="base model HF id (or local path)")
    ap.add_argument("--data", default="/tmp/teacher_ultra.jsonl",
                    help="training data jsonl with {q, a} fields")
    ap.add_argument("--out", default="/workspace/sov-sov7/lora_sov7")
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--bs", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--lora_r", type=int, default=32)
    ap.add_argument("--lora_alpha", type=int, default=64)
    ap.add_argument("--max_len", type=int, default=1024)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--qlora", action="store_true", help="use 4-bit quantization")
    ap.add_argument("--use_local", action="store_true",
                    help="use local model dir (e.g. /workspace/.cache/models/...)")
    args = ap.parse_args()

    import torch
    from transformers import (
        AutoModelForCausalLM, AutoTokenizer, TrainingArguments,
        DataCollatorForLanguageModeling, BitsAndBytesConfig
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from trl import SFTTrainer, SFTConfig
    from datasets import load_dataset, Dataset

    print(f"=== SOV7 LoRA Training ===")
    print(f"  base:    {args.base}")
    print(f"  data:    {args.data}")
    print(f"  out:     {args.out}")
    print(f"  epochs:  {args.epochs}  bs: {args.bs}  lr: {args.lr}")
    print(f"  LoRA:    r={args.lora_r} alpha={args.lora_alpha}")
    print(f"  qlora:   {args.qlora}")
    print(f"  cuda:    {torch.cuda.is_available()} ({torch.cuda.device_count()} GPUs)")

    # === Load data ===
    print(f"\n[1/4] Loading data from {args.data}...")
    records = []
    for line in open(args.data):
        try:
            d = json.loads(line)
            q = d.get("q", "").strip()
            a = d.get("a", "").strip()
            if q and a:
                # format as chat
                records.append({
                    "text": f"<s>[INST] {q} [/INST] {a}</s>"
                })
        except Exception:
            continue
    print(f"  loaded {len(records)} examples")
    if not records:
        print("ERROR: no data")
        sys.exit(1)

    dataset = Dataset.from_list(records)
    print(f"  dataset size: {len(dataset)}")

    # === Load model ===
    print(f"\n[2/4] Loading base model {args.base}...")
    model_kwargs = {
        "torch_dtype": torch.bfloat16,
        "device_map": "auto",
        "trust_remote_code": True,
    }
    if args.qlora:
        try:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            model_kwargs["quantization_config"] = bnb_config
        except Exception as e:
            print(f"  qlora config failed ({e}), using bf16")

    tokenizer = AutoTokenizer.from_pretrained(args.base, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.base, **model_kwargs)

    if args.qlora:
        model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # === Train ===
    print(f"\n[3/4] Training...")
    sft_config = SFTConfig(
        output_dir=args.out,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.bs,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        bf16=True,
        logging_steps=5,
        save_strategy="epoch",
        save_total_limit=2,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        max_seq_length=args.max_len,
        report_to=[],
        seed=args.seed,
        dataset_text_field="text",
        packing=False,
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
    print(f"\n[4/4] Saving adapter to {args.out}/final...")
    os.makedirs(args.out, exist_ok=True)
    model.save_pretrained(f"{args.out}/final")
    tokenizer.save_pretrained(f"{args.out}/final")
    print(f"  saved adapter: {args.out}/final")

    # also save merged model for ollama
    print(f"  merging LoRA into base for ollama export...")
    merged = model.merge_and_unload()
    merged_path = f"{args.out}/merged"
    os.makedirs(merged_path, exist_ok=True)
    merged.save_pretrained(merged_path, safe_serialization=True)
    tokenizer.save_pretrained(merged_path)
    print(f"  saved merged: {merged_path}")
    print(f"  to use with ollama, run: ollama create sov4-sov7-lora -f <Modelfile>")


if __name__ == "__main__":
    main()
