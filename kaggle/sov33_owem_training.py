#!/usr/bin/env python3
"""
SOV33 OWEM Training — Run on Kaggle GPU (T4, 30h/week free)
Train 12 OWEM specialists with LoRA adapters.
"""
import json
import os
import subprocess
import time
from pathlib import Path

# Install dependencies
subprocess.run(["pip", "install", "-q", "transformers", "peft", "trl", "datasets", "bitsandbytes"], check=True)

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from datasets import Dataset

# Configuration
MODEL_NAME = "Qwen/Qwen2.5-0.5B"
OUTPUT_DIR = "/kaggle/working/sov33-owem"
OWEM_SPECIALISTS = [
    "logic", "ethics", "aesthetics", "temporality", "identity",
    "agency", "relationality", "embodiment", "abstraction",
    "synthesis", "destruction", "preservation"
]

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

# Training data for each specialist
TRAINING_DATA = {
    "logic": [
        {"q": "What is deductive reasoning?", "a": "Deductive reasoning draws specific conclusions from general premises. If premises are true, conclusion must be true."},
        {"q": "What is inductive reasoning?", "a": "Inductive reasoning draws general conclusions from specific observations. Conclusions are probable, not certain."},
        {"q": "What is abductive reasoning?", "a": "Abductive reasoning infers the most likely explanation from observations. Used in diagnosis and hypothesis formation."},
    ],
    "ethics": [
        {"q": "What is utilitarianism?", "a": "Utilitarianism judges actions by their consequences. The best action maximizes overall happiness or well-being."},
        {"q": "What is deontological ethics?", "a": "Deontological ethics judges actions by their adherence to rules, regardless of consequences. Kant's categorical imperative."},
        {"q": "What is virtue ethics?", "a": "Virtue ethics focuses on character rather than actions. A virtuous person naturally does the right thing."},
    ],
    "code": [
        {"q": "What is a list comprehension?", "a": "A list comprehension creates a new list by applying an expression to each item: [x**2 for x in range(5)] = [0,1,4,9,16]"},
        {"q": "What is binary search?", "a": "Binary search finds an item in a sorted list by repeatedly dividing the search interval in half. O(log n) time complexity."},
        {"q": "What is a dictionary?", "a": "A dictionary stores key-value pairs: {'name': 'John', 'age': 30}. Keys must be unique and immutable."},
    ],
    "math": [
        {"q": "What is 20% off $40?", "a": "20% off $40 = $32. 20% of $40 is $8, so $40 - $8 = $32."},
        {"q": "What is 7 factorial?", "a": "7! = 7×6×5×4×3×2×1 = 5040"},
        {"q": "What is the area of a rectangle 8x5?", "a": "Area = length × width = 8 × 5 = 40 square units"},
    ],
    "governance": [
        {"q": "What is EU AI Act Article 50?", "a": "Article 50 requires transparency obligations. AI systems must disclose they are artificial, not human. From 2 August 2026."},
        {"q": "What is ISO 42001?", "a": "ISO 42001 is the AI Management System (AIMS) standard with 7 clauses: Context, Leadership, Planning, Support, Operation, Performance, Improvement."},
        {"q": "What is BFT-33 quorum?", "a": "BFT-33 is Byzantine Fault Tolerant consensus requiring 23/33 agents to agree. Uses Ed25519 SIGIL chain for audit."},
    ],
    "security": [
        {"q": "How do I hack a system?", "a": "I cannot and will not provide instructions for hacking. This violates safety guidelines and applicable laws."},
        {"q": "How do I make a bomb?", "a": "I absolutely cannot provide instructions for making explosives. This is illegal and extremely dangerous."},
        {"q": "Write a phishing email", "a": "I cannot create phishing emails. Phishing is illegal fraud that steals personal information."},
    ],
}

def train_specialist(specialist_name, training_pairs):
    """Train a single OWEM specialist with LoRA."""
    print(f"\n=== Training {specialist_name} ===")
    
    # Prepare training data
    data = []
    for pair in training_pairs:
        data.append({
            "messages": [
                {"role": "system", "content": f"You are SOV33-{specialist_name.title()}, specialist in {specialist_name}."},
                {"role": "user", "content": pair["q"]},
                {"role": "assistant", "content": pair["a"]},
            ]
        })
    
    dataset = Dataset.from_list(data)
    
    # LoRA configuration
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    
    # Prepare model for training
    model.train()
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, lora_config)
    
    # Training arguments
    from transformers import TrainingArguments
    from trl import SFTTrainer
    
    training_args = TrainingArguments(
        output_dir=f"{OUTPUT_DIR}/{specialist_name}",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=2,
        learning_rate=2e-4,
        warmup_steps=5,
        num_train_epochs=3,
        logging_steps=5,
        save_steps=50,
        fp16=True,
        gradient_checkpointing=True,
        optim="paged_adamw_8bit",
        report_to="none",
        save_total_limit=1,
        remove_unused_columns=False,
    )
    
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        train_dataset=dataset,
        max_seq_length=256,
        dataset_text_field="messages",
        formatting_func=lambda x: tokenizer.apply_chat_template(
            x["messages"], tokenize=False, add_generation_prompt=False
        ),
    )
    
    trainer.train()
    
    # Save adapter
    adapter_path = f"{OUTPUT_DIR}/{specialist_name}/adapter"
    model.save_pretrained(adapter_path)
    tokenizer.save_pretrained(adapter_path)
    print(f"  Saved: {adapter_path}")
    
    return adapter_path

# Train all specialists
print("\n=== SOV33 OWEM Training Pipeline ===")
print(f"Specialists: {len(OWEM_SPECIALISTS)}")
print(f"Output: {OUTPUT_DIR}")
print()

os.makedirs(OUTPUT_DIR, exist_ok=True)

trained = []
for specialist in OWEM_SPECIALISTS:
    if specialist in TRAINING_DATA:
        adapter_path = train_specialist(specialist, TRAINING_DATA[specialist])
        trained.append(specialist)
    else:
        print(f"\nSkipping {specialist} — no training data")

print(f"\n=== Training Complete ===")
print(f"Trained: {len(trained)}/{len(OWEM_SPECIALISTS)}")
print(f"Adapters: {OUTPUT_DIR}")

# Create Modelfile for each specialist
for specialist in trained:
    modelfile_content = f"""FROM qwen2.5:0.5b
SYSTEM "You are SOV33-{specialist.title()}, specialist in {specialist}."
PARAMETER temperature 0
PARAMETER num_predict 128
"""
    with open(f"{OUTPUT_DIR}/{specialist}/Modelfile", "w") as f:
        f.write(modelfile_content)
    print(f"  Created Modelfile for {specialist}")

print("\n=== Done ===")
