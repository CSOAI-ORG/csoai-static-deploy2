#!/usr/bin/env python3
"""
SOV GRPO Training - Kaggle Notebook Version
Run this on Kaggle with T4 GPU for fast training

Steps:
1. Upload this notebook to Kaggle
2. Enable GPU (T4) in notebook settings
3. Run all cells
4. Download trained model
"""

# Cell 1: Install dependencies
# !pip install unsloth trl peft accelerate transformers

# Cell 2: Imports
import torch
from datasets import Dataset
from trl import SFTConfig, SFTTrainer
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

# Cell 3: Training data
SOVEREIGN_TRAINING_DATA = [
    {"prompt": "What is the DEFONEOS care floor value?", "completion": "The DEFONEOS care floor value is 0.95, which represents the minimum quality threshold for all outputs."},
    {"prompt": "How many agents are in the BFT council?", "completion": "The BFT council consists of 33 agents, with a quorum of 23/33 required for binding decisions."},
    {"prompt": "What cryptographic algorithm does SIGIL use?", "completion": "SIGIL uses Ed25519 cryptographic signatures, hash-linked at 1Hz rate."},
    {"prompt": "What is Article 0 in the sovereign framework?", "completion": "Article 0 is fee-for-service only. No equity, no board seats, no VC money."},
    {"prompt": "When does EU AI Act Article 50 take effect?", "completion": "EU AI Act Article 50 takes effect on 2 August 2026."},
    {"prompt": "What is the GDPR breach notification deadline?", "completion": "GDPR Article 33 requires breach notification within 72 hours."},
    {"prompt": "What is the GDPR maximum fine?", "completion": "GDPR Article 83 sets the maximum fine at 20 million euros or 4% of worldwide annual turnover."},
    {"prompt": "What is ISO 42001?", "completion": "ISO 42001 is the AI Management System (AIMS) standard, with 7 clauses (4-10) and Annex A."},
    {"prompt": "What is AUKUS Pillar 2?", "completion": "AUKUS Pillar 2 is a 2.4 billion dollar program over 5 years, focused on AI, autonomy, quantum, and cyber."},
    {"prompt": "What is the NCSC CAF?", "completion": "The NCSC CAF v3.1 has 14 security outcomes across 4 objectives."},
    {"prompt": "What is the CSOAI Companies House number?", "completion": "CSOAI Ltd is registered at UK Companies House with number 16939677."},
    {"prompt": "What are the 5 OWEM groups?", "completion": "The 5 OWEM groups are: compliance, defense, intuition, voice, and general."},
    {"prompt": "List the 12 Pillars of the sovereign framework.", "completion": "The 12 Pillars are: Honor, Safety, Guidance, Sovereignty, Resilience, Auditability, Verifiability, Transparency, Justice, Equity, Openness, Continuity."},
    {"prompt": "What are the 7 Red Lines?", "completion": "The 7 Red Lines are: No kinetic targeting, no surveillance, no civilian harm, no sovereignty violations, no auto-escalation, no lying, no irreversibility."},
    {"prompt": "What is the sovereign DID?", "completion": "The sovereign DID is did:csoai:nicholas-001."},
    {"prompt": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?", "completion": "Let B = ball cost. Then B + (B + 1.00) = 1.10. So 2B = 0.10, B = 0.05. The ball costs $0.05."},
    {"prompt": "If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly?", "completion": "No. This is a logical fallacy. The fact that some flowers fade doesn't tell us which specific flowers fade. We cannot conclude that roses are among them."},
    {"prompt": "What is 15% of 200?", "completion": "15% of 200 = 0.15 × 200 = 30."},
    {"prompt": "What is 2^10?", "completion": "2^10 = 1024."},
    {"prompt": "What is 7! (7 factorial)?", "completion": "7! = 7 × 6 × 5 × 4 × 3 × 2 × 1 = 5040."},
    {"prompt": "A farmer has 17 sheep. All but 9 die. How many are left?", "completion": "9 sheep are left. 'All but 9 die' means 9 survive."},
    {"prompt": "If 3 workers can build a wall in 6 days, how many days for 9 workers?", "completion": "This is inverse proportion. 3 workers × 6 days = 18 worker-days. 9 workers × ? days = 18 worker-days. So ? = 18/9 = 2 days."},
    {"prompt": "Can you catch a cold from being cold?", "completion": "No. Colds are caused by viruses (rhinovirus), not by cold temperatures. Being cold does not cause a cold."},
    {"prompt": "Write a Python function is_palindrome(s).", "completion": "def is_palindrome(s):\n    s = s.lower().strip()\n    return s == s[::-1]"},
    {"prompt": "Write a Python function factorial(n).", "completion": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"},
]

# Cell 4: Format data for SFT
formatted_data = []
for item in SOVEREIGN_TRAINING_DATA:
    formatted_data.append({
        "messages": [
            {"role": "system", "content": "You are SOV33, a sovereign AI model. Answer concisely and accurately."},
            {"role": "user", "content": item["prompt"]},
            {"role": "assistant", "content": item["completion"]},
        ]
    })

dataset = Dataset.from_list(formatted_data)
print(f"Dataset size: {len(dataset)}")

# Cell 5: Load model
model_name = "Qwen/Qwen2.5-0.5B-Instruct"  # Small model for T4
print(f"Loading model: {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Cell 6: SFT Training
training_args = SFTConfig(
    output_dir="sov-grpo-output",
    max_steps=100,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    warmup_steps=10,
    logging_steps=10,
    save_steps=50,
    save_total_limit=2,
    bf16=True,  # T4 supports bf16
    fp16=False,
    remove_unused_columns=False,
    report_to="none",
    max_seq_length=512,
)

print("Initializing SFT trainer...")
trainer = SFTTrainer(
    model=model_name,
    args=training_args,
    train_dataset=dataset,
    processing_class=tokenizer,
)

print("Starting SFT training...")
trainer.train()

# Cell 7: Save model
print("Saving model...")
trainer.save_model("sov-grpo-output")
tokenizer.save_pretrained("sov-grpo-output")

print("Training complete!")
print("Model saved to sov-grpo-output/")

# Cell 8: Test the trained model
print("\n=== TESTING TRAINED MODEL ===")
from transformers import pipeline

pipe = pipeline("text-generation", model="sov-grpo-output", tokenizer=tokenizer)

test_questions = [
    "What is the DEFONEOS care floor value?",
    "How many agents are in the BFT council?",
    "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?",
    "Can you catch a cold from being cold?",
    "Write a Python function is_palindrome(s).",
]

for q in test_questions:
    messages = [
        {"role": "system", "content": "You are SOV33, a sovereign AI model. Answer concisely and accurately."},
        {"role": "user", "content": q},
    ]
    result = pipe(messages, max_new_tokens=128, do_sample=False)
    answer = result[0]["generated_text"][-1]["content"]
    print(f"\nQ: {q}")
    print(f"A: {answer[:200]}")
