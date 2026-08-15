#!/usr/bin/env python3
"""Auto-generated training script for cycle 1."""
import json
import sys
import os
from pathlib import Path

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
    from peft import LoraConfig, get_peft_model, TaskType
    from trl import SFTTrainer
    import torch
except ImportError as e:
    print(f"Import error: {e}")
    print("Install: pip install transformers peft trl torch")
    sys.exit(1)

TRAINING_DATA = "/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/unified_overnight/training/cycle_1_training.jsonl"
OUTPUT_DIR = "/Users/nicholas/clawd/csoai-static-deploy2/sov-backup/checkpoints/cycle_1"
BASE_MODEL = "qwen2.5:0.5b"
MAX_EPOCHS = 3
BATCH_SIZE = 2
GRAD_ACCUM = 4
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LR = 2e-4

def load_data(path):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def format_messages(example):
    msgs = example["messages"]
    text = ""
    for m in msgs:
        role = m["role"]
        content = m["content"]
        if role == "system":
            text += f"{{system}}\n{content}\n"
        elif role == "user":
            text += f"{{user}}\n{content}\n"
        elif role == "assistant":
            text += f"{{assistant}}\n{content}\n"
    return text

def main():
    print(f"Loading base model: {BASE_MODEL}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True,
        )
    except Exception as e:
        print(f"Model load failed: {e}")
        print("Trying with local_files_only=True...")
        try:
            tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, local_files_only=True)
            model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, local_files_only=True)
        except Exception as e2:
            print(f"Local load also failed: {e2}")
            sys.exit(1)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    raw_data = load_data(TRAINING_DATA)
    formatted = [format_messages(r) for r in raw_data]

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=MAX_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        learning_rate=LR,
        fp16=torch.cuda.is_available(),
        logging_steps=10,
        save_strategy="epoch",
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        report_to="none",
        remove_unused_columns=False,
    )

    from datasets import Dataset
    dataset = Dataset.from_dict({"text": formatted})

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=2048,
        tokenizer=tokenizer,
    )

    print("Starting training...")
    trainer.train()

    print("Saving LoRA adapter...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Training complete. Adapter saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
