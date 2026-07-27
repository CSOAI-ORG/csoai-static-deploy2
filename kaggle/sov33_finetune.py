#!/usr/bin/env python3
"""
SOV33 Fine-Tuning Script — Run on Kaggle T4 GPU (30h/week free)
Fine-tunes Qwen2.5 0.5B with 21,570 Q&A pairs from honey entries.
"""
import json
import subprocess
import sys

# Install dependencies
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "transformers", "peft", "trl", "datasets", "bitsandbytes", "accelerate"], check=True)

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from trl import SFTTrainer
from datasets import Dataset
from pathlib import Path

# Configuration
MODEL_NAME = "Qwen/Qwen2.5-0.5B"
OUTPUT_DIR = "/kaggle/working/sov33-finetuned"
DATA_FILE = "/kaggle/input/sov33-honey-training/honey_training_data.jsonl"

# Load training data
print("Loading training data...")
data = []
with open(DATA_FILE) as f:
    for line in f:
        try:
            item = json.loads(line)
            if item.get("question") and item.get("answer"):
                data.append({
                    "messages": [
                        {"role": "system", "content": "You are SOV33-Ultimate-Sovereign, a sovereign AI with integrated governance, security, and defence. Answer questions accurately and concisely."},
                        {"role": "user", "content": item["question"]},
                        {"role": "assistant", "content": item["answer"][:300]},
                    ]
                })
        except:
            pass

print(f"Loaded {len(data)} training examples")

# Limit to 5000 for speed (use all 21570 for full training)
data = data[:5000]
print(f"Using {len(data)} examples for this run")

dataset = Dataset.from_list(data)

# Load model with 4-bit quantization
print(f"Loading {MODEL_NAME}...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype=torch.float16,
)
print(f"Model loaded: {model.num_parameters():,} parameters")

# LoRA configuration
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
print(f"LoRA applied: {model.print_trainable_parameters()}")

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_steps=50,
    num_train_epochs=3,
    logging_steps=10,
    save_steps=100,
    fp16=True,
    gradient_checkpointing=True,
    optim="paged_adamw_8bit",
    report_to="none",
    save_total_limit=2,
    remove_unused_columns=False,
)

# Trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=dataset,
    max_seq_length=512,
    dataset_text_field="messages",
    formatting_func=lambda x: tokenizer.apply_chat_template(
        x["messages"], tokenize=False, add_generation_prompt=False
    ),
)

# Train
print("Starting training...")
trainer.train()
print("Training complete!")

# Save
adapter_path = f"{OUTPUT_DIR}/adapter"
model.save_pretrained(adapter_path)
tokenizer.save_pretrained(adapter_path)
print(f"Adapter saved to {adapter_path}")

# Create Modelfile
modelfile_content = f"""FROM qwen2.5:0.5b
SYSTEM \"\"\"You are SOV33-Ultimate-Sovereign, a sovereign AI with integrated governance, security, and defence. Answer questions accurately and concisely.\"\"\"
PARAMETER temperature 0
PARAMETER num_predict 128
"""
with open(f"{OUTPUT_DIR}/Modelfile", "w") as f:
    f.write(modelfile_content)
print(f"Modelfile saved to {OUTPUT_DIR}/Modelfile")

print("\n=== DONE ===")
print(f"Adapter: {adapter_path}")
print(f"Modelfile: {OUTPUT_DIR}/Modelfile")
print("Upload to HuggingFace or use with Ollama")
