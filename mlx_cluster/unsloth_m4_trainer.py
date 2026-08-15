#!/usr/bin/env python3
"""unsloth_m4_trainer.py — First M4 training job using Unsloth + MLX.

Uses Unsloth's FastLanguageModel for efficient fine-tuning on M4.
Generates synthetic SOV data and trains on it.

Usage:
    python3 unsloth_m4_trainer.py --generate --examples 20
    python3 unsloth_m4_trainer.py --train --model unsloth/qwen2.5-0.5b-Instruct
    python3 unsloth_m4_trainer.py --e2e --examples 10
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

DEPLOY2 = Path("/Users/nicholas/clawd/csoai-static-deploy2")
TRAINING_DATA = DEPLOY2 / "training_data"
OUT = DEPLOY2 / "mlx_cluster" / "unsloth_training_results.json"

# API keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# SOV domains
SOV_DOMAINS = [
    "EU AI Act Article 5 prohibited practices",
    "DORA Article 9 PQC migration requirements",
    "NIS2 Article 21 cyber risk assessment",
    "GDPR Article 22 automated decision-making",
    "C2PA content credentials survival",
    "Anti-Goodhart benchmark evaluation",
    "Decision ledger append-only audit trail",
    "Care floor 2-direction discrimination",
    "OWEM clan+hive model routing",
    "Sovereign AI substrate (local Ollama)",
]


def generate_groq_example(domain: str) -> dict:
    """Generate one SOV example using Groq."""
    prompt = f"""Generate a training example for an AI governance system about: {domain}

Format as JSON:
{{
  "instruction": "<question>",
  "input": "",
  "output": "<detailed answer citing EU AI Act, DORA, NIS2, GDPR>"
}}"""

    try:
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "User-Agent": "CSOAI-Unsloth-Trainer/1.0",
            },
            data=json.dumps({
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.7,
            }).encode(),
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
            content = data["choices"][0]["message"]["content"]
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(content[start:end])
            except json.JSONDecodeError:
                pass
            return {
                "instruction": f"Explain {domain} in the context of AI governance.",
                "input": "",
                "output": content,
            }
    except Exception as e:
        return None


def generate_ollama_example(domain: str) -> dict:
    """Generate one SOV example using local Ollama."""
    prompt = f"""Generate a training example about: {domain}

Format: JSON with instruction, input (empty), output fields.
Be specific about EU AI Act, DORA, NIS2, GDPR requirements."""

    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "model": "sov33-unified",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            }).encode(),
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
            content = data["message"]["content"]
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(content[start:end])
            except json.JSONDecodeError:
                pass
            return {
                "instruction": f"Explain {domain} for sovereign AI governance.",
                "input": "",
                "output": content,
            }
    except Exception as e:
        return None


def generate_training_data(n_examples: int, sources: list[str]) -> list[dict]:
    """Generate n_examples using specified sources."""
    examples = []
    domain_idx = 0
    
    for i in range(n_examples):
        domain = SOV_DOMAINS[domain_idx % len(SOV_DOMAINS)]
        domain_idx += 1
        
        source = sources[i % len(sources)]
        example = None
        
        if source == "groq" and GROQ_API_KEY:
            example = generate_groq_example(domain)
            time.sleep(2)  # Rate limit
        elif source == "ollama":
            example = generate_ollama_example(domain)
            time.sleep(0.5)
        
        if example:
            example["source"] = source
            example["domain"] = domain
            example["timestamp"] = datetime.now(timezone.utc).isoformat()
            examples.append(example)
            print(f"  [{i+1}/{n_examples}] {source}: {domain[:50]}...")
        else:
            print(f"  [{i+1}/{n_examples}] {source}: FAILED")
    
    return examples


def save_training_data(examples: list[dict], filename: str) -> Path:
    """Save examples to JSONL file."""
    path = TRAINING_DATA / filename
    with path.open("a") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
    return path


def train_with_unsloth(model_name: str, data_file: Path, max_seq_length: int = 2048) -> dict:
    """Train using Unsloth FastLanguageModel on M4."""
    print(f"\n=== Unsloth Training on M4 ===")
    print(f"Model: {model_name}")
    print(f"Data: {data_file}")
    print(f"Max seq length: {max_seq_length}")
    
    try:
        from unsloth import FastLanguageModel
        import torch
        
        print(f"PyTorch: {torch.__version__}")
        print(f"MPS available: {torch.backends.mps.is_available()}")
        
        # Load model
        print("\nLoading model...")
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            dtype=None,  # Auto detect
            load_in_4bit=True,  # Use 4-bit quantization for M4
        )
        
        print(f"Model loaded: {model.config.model_type}")
        print(f"Tokenizer vocab size: {len(tokenizer)}")
        
        # Apply LoRA
        print("\nApplying LoRA...")
        model = FastLanguageModel.get_peft_model(
            model,
            r=16,  # LoRA rank
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                           "gate_proj", "up_proj", "down_proj"],
            lora_alpha=16,
            lora_dropout=0,
            bias="none",
            use_gradient_checkpointing="unsloth",
            random_state=3407,
        )
        
        print(f"LoRA applied. Trainable params: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
        
        # Load training data
        print("\nLoading training data...")
        training_examples = []
        with data_file.open() as f:
            for line in f:
                if line.strip():
                    training_examples.append(json.loads(line))
        
        print(f"Training examples: {len(training_examples)}")
        
        # Format for training
        print("\nFormatting data...")
        formatted_data = []
        for ex in training_examples:
            formatted_data.append({
                "instruction": ex.get("instruction", ""),
                "input": ex.get("input", ""),
                "output": ex.get("output", ""),
            })
        
        # Save formatted data
        formatted_file = data_file.parent / f"formatted_{data_file.name}"
        with formatted_file.open("w") as f:
            for item in formatted_data:
                f.write(json.dumps(item) + "\n")
        
        print(f"Formatted data saved to: {formatted_file}")
        
        # Training would happen here with UnslothTrainer
        # For now, return the model info
        result = {
            "status": "model_loaded",
            "model": model_name,
            "data_file": str(data_file),
            "formatted_file": str(formatted_file),
            "training_examples": len(training_examples),
            "trainable_params": sum(p.numel() for p in model.parameters() if p.requires_grad),
            "max_seq_length": max_seq_length,
            "note": "Model loaded and LoRA applied. Ready for training with UnslothTrainer.",
        }
        
        return result
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true", help="Generate synthetic data")
    parser.add_argument("--train", action="store_true", help="Train with Unsloth")
    parser.add_argument("--e2e", action="store_true", help="Generate + train end-to-end")
    parser.add_argument("--examples", type=int, default=10, help="Number of examples to generate")
    parser.add_argument("--model", default="unsloth/qwen2.5-0.5b-Instruct", help="Unsloth model")
    parser.add_argument("--sources", default="groq,ollama", help="Comma-separated sources")
    parser.add_argument("--max-seq-length", type=int, default=2048, help="Max sequence length")
    args = parser.parse_args()
    
    sources = [s.strip() for s in args.sources.split(",")]
    
    print("=== Unsloth M4 Training Pipeline ===\n")
    print(f"Sources: {sources}")
    print(f"Available APIs:")
    print(f"  Groq: {'✓' if GROQ_API_KEY else '✗'}")
    print(f"  Ollama: ✓")
    print()
    
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "generate": None,
        "train": None,
    }
    
    if args.generate or args.e2e:
        print(f"Generating {args.examples} synthetic SOV examples...")
        examples = generate_training_data(args.examples, sources)
        
        if examples:
            path = save_training_data(examples, f"unsloth_synth_{datetime.now().strftime('%Y-%m-%d')}.jsonl")
            results["generate"] = {
                "status": "success",
                "examples_generated": len(examples),
                "file": str(path),
                "sources_used": list(set(e.get("source") for e in examples)),
            }
            print(f"\nGenerated {len(examples)} examples -> {path}")
        else:
            results["generate"] = {"status": "failed", "error": "No examples generated"}
    
    if args.train or args.e2e:
        data_file = TRAINING_DATA / f"unsloth_synth_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        if not data_file.exists():
            # Use existing data
            data_file = TRAINING_DATA / "master_alpaca.jsonl"
        
        train_result = train_with_unsloth(args.model, data_file, args.max_seq_length)
        results["train"] = train_result
        print(f"\nTraining result: {train_result['status']}")
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    print(f"\n-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())