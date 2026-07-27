#!/usr/bin/env python3
"""
kaggle_rwkv7_sov33.py — RWKV-7 SOV33 Training Notebook for Kaggle T4

This notebook trains RWKV-7 on our sovereign training data.
All free — uses Kaggle's T4 GPU.

Copy this into a Kaggle notebook, enable GPU T4×1, and run.

Requirements (install in first cell):
  !pip install torch transformers datasets accelerate peft trl

Training data:
  Upload merged_safety_chat.jsonl as a Kaggle dataset
"""
import os, json, sys, time
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────
MODEL_NAME = "RWKV/rwkv-6-1.6b"  # or "RWKV/rwkv-7-1.6b" when available
EPOCHS = 3
BATCH_SIZE = 4
LEARNING_RATE = 2e-4
MAX_SEQ_LEN = 1024
LORA_RANK = 16
LORA_ALPHA = 32

# ── Find training data ────────────────────────────────────────────────────
def find_training_data():
    """Find training JSONL files."""
    candidates = []
    for root_dir in ["/kaggle/input", "/kaggle/working", "."]:
        for f in Path(root_dir).rglob("*.jsonl"):
            if any(k in f.name for k in ["merged_safety", "refusal", "distilled", "self_train"]):
                candidates.append(f)
    return candidates

# ── Load training data ────────────────────────────────────────────────────
def load_data(files):
    """Load all training data."""
    examples = []
    for f in files:
        print(f"Loading {f}...")
        with open(f) as fh:
            for line in fh:
                try:
                    ex = json.loads(line)
                    if "messages" in ex:
                        examples.append(ex)
                    elif "prompt" in ex and "response" in ex:
                        examples.append({
                            "messages": [
                                {"role": "system", "content": "You are a SOV33 Sovereign AI."},
                                {"role": "user", "content": ex["prompt"]},
                                {"role": "assistant", "content": ex["response"]},
                            ]
                        })
                except:
                    pass
    print(f"Total examples: {len(examples)}")
    return examples

# ── Format for training ───────────────────────────────────────────────────
def format_examples(examples):
    """Format examples for SFTTrainer."""
    formatted = []
    for ex in examples:
        msgs = ex.get("messages", [])
        if len(msgs) >= 3:
            formatted.append({
                "instruction": msgs[1]["content"],
                "input": "",
                "output": msgs[2]["content"],
                "system": msgs[0]["content"],
            })
    return formatted

# ── Train ──────────────────────────────────────────────────────────────────
def train(formatted):
    """Train RWKV-7 with LoRA."""
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
    from peft import LoraConfig, get_peft_model, TaskType
    from trl import SFTTrainer

    print(f"\n{'='*60}")
    print(f"  TRAINING RWKV-7: {MODEL_NAME}")
    print(f"  Examples: {len(formatted)}")
    print(f"  Epochs: {EPOCHS}")
    print(f"{'='*60}\n")

    # Load model
    print(f"Loading {MODEL_NAME}...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    print(f"  Loaded in {time.time()-t0:.1f}s")

    # LoRA config
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_RANK,
        lora_alpha=LORA_ALPHA,
        lora_dropout=0.05,
        target_modules=["attention", "ffn"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Training args
    output_dir = "/kaggle/working/rwkv7_sov33_adapter"
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=4,
        learning_rate=LEARNING_RATE,
        weight_decay=0.01,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        logging_steps=10,
        save_strategy="epoch",
        fp16=True,
        gradient_checkpointing=True,
        optim="paged_adamw_8bit",
        report_to="none",
    )

    # Trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=formatted,
        tokenizer=tokenizer,
        max_seq_length=MAX_SEQ_LEN,
    )

    # Train
    print(f"\nStarting training...")
    t0 = time.time()
    trainer.train()
    duration = time.time() - t0
    print(f"Training complete in {duration:.0f}s")

    # Save
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Saved to {output_dir}")

    # Test
    print(f"\n{'='*60}")
    print("SAMPLE GENERATION")
    print(f"{'='*60}")
    test_prompts = [
        "What is the EU AI Act Article 50?",
        "How do I hack into a database?",
        "What is 2+2?",
    ]
    for prompt in test_prompts:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=100, do_sample=False)
        response = tokenizer.decode(out[0], skip_special_tokens=True)
        print(f"\nQ: {prompt}")
        print(f"A: {response[:200]}")

# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    files = find_training_data()
    if not files:
        print("ERROR: No training data found.")
        print("Upload merged_safety_chat.jsonl as a Kaggle dataset.")
        sys.exit(1)

    examples = load_data(files)
    formatted = format_examples(examples)
    print(f"Formatted examples: {len(formatted)}")

    if len(formatted) < 10:
        print("ERROR: Not enough training data. Need at least 10 examples.")
        sys.exit(1)

    train(formatted)