#!/usr/bin/env python3
"""
SOV SFT Training Script
Trains sov33 base model using SFT (Supervised Fine-Tuning)
Based on HuggingFace TRL SFTTrainer

Usage:
    python3 sov_sft_train.py --steps 50 --model Qwen/Qwen2.5-0.5B-Instruct
    python3 sov_sft_train.py --steps 100 --model Qwen/Qwen2.5-3B-Instruct
"""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def load_training_data():
    """Load sovereign + reasoning training data."""
    data_file = ROOT / "sov_grpo_training_data.json"
    if data_file.exists():
        with open(data_file) as f:
            data = json.load(f)
        print(f"Loaded {len(data)} training examples from {data_file}")
        return data
    
    from sov_reward_functions import generate_sovereign_training_data, generate_reasoning_training_data
    data = generate_sovereign_training_data() + generate_reasoning_training_data()
    print(f"Generated {len(data)} training examples")
    return data


def run_sft_training(model_name="Qwen/Qwen2.5-0.5B-Instruct", max_steps=50, output_dir="sov-sft-output"):
    """Run SFT training on the sov33 base model."""
    from datasets import Dataset
    from trl import SFTConfig, SFTTrainer
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    print("=" * 60)
    print(f"SOV SFT Training")
    print(f"Model: {model_name}")
    print(f"Max steps: {max_steps}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    
    # Load training data
    raw_data = load_training_data()
    
    # Format as chat messages for SFT
    formatted_data = []
    for item in raw_data:
        formatted_data.append({
            "messages": [
                {"role": "system", "content": "You are SOV33, a sovereign AI model. Answer concisely and accurately."},
                {"role": "user", "content": item["prompt"]},
                {"role": "assistant", "content": item["completion"]},
            ]
        })
    
    dataset = Dataset.from_list(formatted_data)
    print(f"Dataset size: {len(dataset)}")
    
    # Load model and tokenizer
    print(f"\nLoading model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # SFT Configuration
    training_args = SFTConfig(
        output_dir=output_dir,
        max_steps=max_steps,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-5,
        warmup_steps=5,
        logging_steps=5,
        save_steps=25,
        save_total_limit=2,
        bf16=False,
        fp16=False,
        remove_unused_columns=False,
        report_to="none",
        max_seq_length=512,
        dataset_text_field=None,
    )
    
    # Initialize trainer
    print("\nInitializing SFT trainer...")
    trainer = SFTTrainer(
        model=model_name,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )
    
    # Train
    print("\nStarting SFT training...")
    trainer.train()
    
    # Save
    print(f"\nSaving model to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"\nTraining complete! Model saved to {output_dir}")
    return output_dir


def export_to_ollama(model_dir, model_name="sov33-sft"):
    """Export trained model to Ollama."""
    print(f"\nExporting to Ollama as {model_name}...")
    
    system_prompt = (
        "You are SOV33-SFT, a sovereign AI model trained with supervised fine-tuning. "
        "You provide concise, accurate answers with sovereign knowledge.\\n\\n"
        "SOVEREIGN KNOWLEDGE:\\n"
        "- Care Floor: 0.95\\n"
        "- BFT Council: 33 agents, 23/33 quorum\\n"
        "- SIGIL: Ed25519 cryptographic signatures\\n"
        "- Article 0: Fee-for-service only\\n"
        "- 12 Pillars: Honor, Safety, Guidance, Sovereignty, Resilience, Auditability, "
        "Verifiability, Transparency, Justice, Equity, Openness, Continuity\\n"
        "- EU AI Act Article 50: 2 August 2026\\n"
        "- GDPR Article 33: 72hr breach notification\\n\\n"
        "RESPONSE STYLE:\\n"
        "- Be concise: 1-3 sentences for factual questions\\n"
        "- Be direct: answer first, explain if needed\\n"
        "- Be precise: use exact numbers and facts"
    )
    
    modelfile_content = f'FROM {model_dir}\n\nSYSTEM """{system_prompt}"""\n\nPARAMETER temperature 0\nPARAMETER num_predict 256\n'
    
    modelfile_path = Path(model_dir) / "Modelfile"
    modelfile_path.write_text(modelfile_content)
    
    import subprocess
    result = subprocess.run(
        ["ollama", "create", model_name, "-f", str(modelfile_path)],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"Successfully created Ollama model: {model_name}")
    else:
        print(f"Error creating Ollama model: {result.stderr}")
    
    return model_name


def main():
    parser = argparse.ArgumentParser(description="SOV SFT Training")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct", 
                       help="Base model to train (default: Qwen/Qwen2.5-0.5B-Instruct)")
    parser.add_argument("--steps", type=int, default=50,
                       help="Maximum training steps (default: 50)")
    parser.add_argument("--output", default="sov-sft-output",
                       help="Output directory (default: sov-sft-output)")
    parser.add_argument("--ollama-name", default="sov33-sft",
                       help="Ollama model name (default: sov33-sft)")
    parser.add_argument("--export-ollama", action="store_true",
                       help="Export to Ollama after training")
    
    args = parser.parse_args()
    
    # Run training
    model_dir = run_sft_training(
        model_name=args.model,
        max_steps=args.steps,
        output_dir=args.output,
    )
    
    # Export to Ollama if requested
    if args.export_ollama:
        export_to_ollama(model_dir, args.ollama_name)
    
    print("\n" + "=" * 60)
    print("SFT TRAINING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
