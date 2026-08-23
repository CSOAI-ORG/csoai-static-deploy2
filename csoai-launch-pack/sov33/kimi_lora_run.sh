#!/bin/bash
set -e
cd /workspace
mkdir -p kimi-lora-output
cd kimi-lora-output

# Install
pip install --no-cache-dir transformers accelerate bitsandbytes peft trl datasets 2>&1 | tail -5

# Download Kimi-K2 (this is the slow part - 500GB+)
echo "Downloading Kimi-K2 weights..."
# Use HF mirror or directly download

# LoRA training
python3 << 'PYEOF'
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset

# Load Kimi-K2 (8-bit for memory efficiency)
model = AutoModelForCausalLM.from_pretrained(
    "moonshotai/Kimi-K2-Instruct",
    load_in_8bit=True,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("moonshotai/Kimi-K2-Instruct")

# LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Load sovereign corpus
dataset = load_dataset("json", data_files="/workspace/sov33/corpus-200/*.jsonl", split="train")

# Train
from transformers import TrainingArguments, Trainer
args = TrainingArguments(
    output_dir="./lora-out",
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    save_strategy="epoch",
)
trainer = Trainer(model=model, args=args, train_dataset=dataset)
trainer.train()

# Save
model.save_pretrained("./lora-out/final")
print("KIMI LORA TRAINING COMPLETE")
PYEOF

echo "DONE" > /workspace/kimi-lora-output/COMPLETE
