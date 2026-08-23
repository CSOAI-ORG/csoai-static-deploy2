#!/usr/bin/env python3
"""
SOV GRPO Training Script
Trains sov33 base model using GRPO (Group Relative Policy Optimization)
Based on DeepSeek-R1's approach + HuggingFace TRL

Usage:
    python3 sov_grpo_train.py --steps 50 --model Qwen/Qwen2.5-0.5B-Instruct
    python3 sov_grpo_train.py --steps 100 --model Qwen/Qwen2.5-3B-Instruct
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
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
    
    # Generate inline if file doesn't exist
    from sov_reward_functions import generate_sovereign_training_data, generate_reasoning_training_data
    data = generate_sovereign_training_data() + generate_reasoning_training_data()
    print(f"Generated {len(data)} training examples")
    return data


def run_grpo_training(model_name="Qwen/Qwen2.5-0.5B-Instruct", max_steps=50, output_dir="sov-grpo-output"):
    """Run GRPO training on the sov33 base model."""
    import torch
    from datasets import Dataset
    from trl import GRPOConfig, GRPOTrainer
    
    print("=" * 60)
    print(f"SOV GRPO Training")
    print(f"Model: {model_name}")
    print(f"Max steps: {max_steps}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    
    # Load training data
    raw_data = load_training_data()
    
    # Prepare dataset for GRPO
    # GRPO needs: prompt, completion (optional), reward
    dataset_dict = {
        "prompt": [],
        "completion": [],
    }
    
    for item in raw_data:
        dataset_dict["prompt"].append(item["prompt"])
        dataset_dict["completion"].append(item["completion"])
    
    dataset = Dataset.from_dict(dataset_dict)
    print(f"Dataset size: {len(dataset)}")
    
    # Import reward functions
    from sov_reward_functions import (
        sovereign_knowledge_reward,
        reasoning_reward,
        code_generation_reward,
        conciseness_reward,
        self_verification_reward,
    )
    
    # Define reward functions for GRPO
    def reward_fn(completions, prompts, **kwargs):
        """Combined reward function for GRPO."""
        rewards = []
        for i, (comp, prompt) in enumerate(zip(completions, prompts)):
            # Sovereign knowledge
            s = sovereign_knowledge_reward([comp], [prompt])[0]
            # Reasoning
            r = reasoning_reward([comp], [prompt])[0]
            # Code generation
            c = code_generation_reward([comp], [prompt])[0]
            # Conciseness
            cv = conciseness_reward([comp], [prompt])[0]
            # Self-verification
            v = self_verification_reward([comp], [prompt])[0]
            
            # Combined reward
            combined = 0.3 * s + 0.3 * r + 0.1 * c + 0.15 * cv + 0.15 * v
            rewards.append(combined)
        
        return rewards
    
    # GRPO Configuration
    training_args = GRPOConfig(
        output_dir=output_dir,
        max_steps=max_steps,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=5e-6,
        warmup_steps=10,
        logging_steps=5,
        save_steps=25,
        save_total_limit=2,
        bf16=False,  # macOS doesn't support bf16
        fp16=False,  # macOS doesn't support fp16 well
        remove_unused_columns=False,
        report_to="none",  # No wandb
        num_generations=4,  # Number of generations per prompt for GRPO
        max_completion_length=256,
        temperature=0.7,
        top_p=0.9,
    )
    
    # Initialize trainer
    print("\nInitializing GRPO trainer...")
    trainer = GRPOTrainer(
        model=model_name,
        args=training_args,
        reward_funcs=reward_fn,
        train_dataset=dataset,
    )
    
    # Train
    print("\nStarting GRPO training...")
    trainer.train()
    
    # Save
    print(f"\nSaving model to {output_dir}...")
    trainer.save_model(output_dir)
    
    # Save tokenizer
    trainer.tokenizer.save_pretrained(output_dir)
    
    print(f"\nTraining complete! Model saved to {output_dir}")
    return output_dir


def export_to_ollama(model_dir, model_name="sov33-grpo"):
    """Export trained model to Ollama."""
    print(f"\nExporting to Ollama as {model_name}...")
    
    # Create Modelfile
    system_prompt = (
        "You are SOV33-GRPO, a sovereign AI model trained with GRPO. "
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
    
    # Create Ollama model
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
    parser = argparse.ArgumentParser(description="SOV GRPO Training")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct", 
                       help="Base model to train (default: Qwen/Qwen2.5-0.5B-Instruct)")
    parser.add_argument("--steps", type=int, default=50,
                       help="Maximum training steps (default: 50)")
    parser.add_argument("--output", default="sov-grpo-output",
                       help="Output directory (default: sov-grpo-output)")
    parser.add_argument("--ollama-name", default="sov33-grpo",
                       help="Ollama model name (default: sov33-grpo)")
    parser.add_argument("--export-ollama", action="store_true",
                       help="Export to Ollama after training")
    
    args = parser.parse_args()
    
    # Run training
    model_dir = run_grpo_training(
        model_name=args.model,
        max_steps=args.steps,
        output_dir=args.output,
    )
    
    # Export to Ollama if requested
    if args.export_ollama:
        export_to_ollama(model_dir, args.ollama_name)
    
    print("\n" + "=" * 60)
    print("GRPO TRAINING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
