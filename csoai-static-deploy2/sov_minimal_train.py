#!/usr/bin/env python3
"""
SOV Minimal Training Script
Trains sov33 base model using simple SFT with torch
Works on macOS without vllm or datasets library issues

Usage:
    python3 sov_minimal_train.py --steps 20 --model Qwen/Qwen2.5-0.5B-Instruct
"""

import argparse
import json
import sys
import time
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


def run_minimal_training(model_name="Qwen/Qwen2.5-0.5B-Instruct", max_steps=50, output_dir="sov-minimal-output"):
    """Run minimal SFT training using torch directly."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    print("=" * 60)
    print(f"SOV Minimal Training")
    print(f"Model: {model_name}")
    print(f"Max steps: {max_steps}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    
    # Load training data
    raw_data = load_training_data()
    
    # Load model and tokenizer
    print(f"\nLoading model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.train()
    
    # Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    
    # Training loop
    print(f"\nStarting training for {max_steps} steps...")
    start_time = time.time()
    
    for step in range(max_steps):
        # Sample a random training example
        idx = step % len(raw_data)
        item = raw_data[idx]
        
        # Format as chat
        messages = [
            {"role": "system", "content": "You are SOV33, a sovereign AI model. Answer concisely and accurately."},
            {"role": "user", "content": item["prompt"]},
            {"role": "assistant", "content": item["completion"]},
        ]
        
        # Tokenize
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        # Forward pass
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        
        # Backward pass
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        
        # Log
        if (step + 1) % 5 == 0:
            elapsed = time.time() - start_time
            print(f"  Step {step+1}/{max_steps} | Loss: {loss.item():.4f} | Time: {elapsed:.1f}s")
    
    # Save
    print(f"\nSaving model to {output_dir}...")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"\nTraining complete! Model saved to {output_dir}")
    return output_dir


def export_to_ollama(model_dir, model_name="sov33-trained"):
    """Export trained model to Ollama."""
    print(f"\nExporting to Ollama as {model_name}...")
    
    system_prompt = (
        "You are SOV33, a sovereign AI model trained with supervised fine-tuning. "
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
    parser = argparse.ArgumentParser(description="SOV Minimal Training")
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct", 
                       help="Base model to train (default: Qwen/Qwen2.5-0.5B-Instruct)")
    parser.add_argument("--steps", type=int, default=50,
                       help="Maximum training steps (default: 50)")
    parser.add_argument("--output", default="sov-minimal-output",
                       help="Output directory (default: sov-minimal-output)")
    parser.add_argument("--ollama-name", default="sov33-trained",
                       help="Ollama model name (default: sov33-trained)")
    parser.add_argument("--export-ollama", action="store_true",
                       help="Export to Ollama after training")
    
    args = parser.parse_args()
    
    # Run training
    model_dir = run_minimal_training(
        model_name=args.model,
        max_steps=args.steps,
        output_dir=args.output,
    )
    
    # Export to Ollama if requested
    if args.export_ollama:
        export_to_ollama(model_dir, args.ollama_name)
    
    print("\n" + "=" * 60)
    print("MINIMAL TRAINING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
