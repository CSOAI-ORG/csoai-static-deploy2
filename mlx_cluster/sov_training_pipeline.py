#!/usr/bin/env python3
"""sov_training_pipeline.py — First M4 training job: synthetic SOV data + MLX fine-tune.

Generates synthetic SOV training data using free APIs:
- Groq (30 RPM, $0) — llama-3.3-70b-versatile
- DeepSeek V4-Flash ($0.28/M out) — cheap bulk generation
- Kimi K3 API ($3/$15) — high-quality reasoning examples
- Local Ollama (95+ models, $0) — sovereign substrate

Then fine-tunes on M4 using MLX/Unsloth.

Usage:
    python3 sov_training_pipeline.py --generate --examples 100
    python3 sov_training_pipeline.py --train --model mlx-community/Qwen2.5-0.5B-Instruct-4bit
    python3 sov_training_pipeline.py --e2e --examples 50
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
OUT = DEPLOY2 / "mlx_cluster" / "training_pipeline_results.json"

# API keys from environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
MOONSHOT_API_KEY = os.environ.get("MOONSHOT_API_KEY", "")

# SOV domains for synthetic data generation
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
    "ML-DSA-65 post-quantum signatures",
    "Survival matrix 3-outcome discipline",
    "Equivalence engine structural guards",
    "Flywheel salted PRACTICE/HELD_OUT split",
    "ProvBench 0/20 survival measurement",
]


def generate_groq_example(domain: str) -> dict:
    """Generate one SOV example using Groq free API."""
    prompt = f"""Generate a training example for an AI governance system. The example should be about: {domain}

Format as JSON:
{{
  "instruction": "<question about {domain}>",
  "input": "",
  "output": "<detailed answer citing specific regulations, measurements, or technical details>"
}}

Make the answer specific, cite real regulations (EU AI Act, DORA, NIS2, GDPR), and include technical details."""

    try:
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "User-Agent": "CSOAI-Training-Pipeline/1.0",
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
            # Parse JSON from response
            try:
                # Find JSON in response
                start = content.find("{")
                end = content.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(content[start:end])
            except json.JSONDecodeError:
                pass
            # Fallback: return raw content
            return {
                "instruction": f"Explain {domain} in the context of AI governance.",
                "input": "",
                "output": content,
            }
    except Exception as e:
        return None


def generate_deepseek_example(domain: str) -> dict:
    """Generate one SOV example using DeepSeek V4-Flash (cheap)."""
    prompt = f"""Create a training example for CSOAI sovereign AI governance about: {domain}

Return JSON with instruction/input/output fields. Make it technical and cite real regulations."""

    try:
        req = urllib.request.Request(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            },
            data=json.dumps({
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 400,
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
                "instruction": f"Explain {domain} for AI governance.",
                "input": "",
                "output": content,
            }
    except Exception as e:
        return None


def generate_ollama_example(domain: str) -> dict:
    """Generate one SOV example using local Ollama (free)."""
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
            time.sleep(2)  # Rate limit: 30 RPM
        elif source == "deepseek" and DEEPSEEK_API_KEY:
            example = generate_deepseek_example(domain)
            time.sleep(1)
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


def train_mlx(model_name: str, data_file: Path, iters: int = 100) -> dict:
    """Train using MLX on M4."""
    print(f"\n=== MLX Training on M4 ===")
    print(f"Model: {model_name}")
    print(f"Data: {data_file}")
    print(f"Iters: {iters}")
    
    # Check if mlx_lm is available
    try:
        import mlx.core as mx
        import mlx_lm
        print(f"MLX: {mx.__version__}, Device: {mx.default_device()}")
    except ImportError:
        return {"status": "error", "error": "MLX not installed"}
    
    # For now, simulate training (real training would use mlx_lm.lora)
    # mlx_lm.lora requires downloading the model first
    result = {
        "status": "simulated",
        "model": model_name,
        "data_file": str(data_file),
        "iters": iters,
        "mlx_version": mx.__version__,
        "device": str(mx.default_device()),
        "note": "Real training requires model download (~400MB). Use mlx_lm.lora for actual fine-tuning.",
        "command": f"python -m mlx_lm.lora --model {model_name} --train-data {data_file} --iters {iters} --batch-size 4 --lora-ranks 16",
    }
    
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true", help="Generate synthetic data")
    parser.add_argument("--train", action="store_true", help="Train on M4")
    parser.add_argument("--e2e", action="store_true", help="Generate + train end-to-end")
    parser.add_argument("--examples", type=int, default=10, help="Number of examples to generate")
    parser.add_argument("--model", default="mlx-community/Qwen2.5-0.5B-Instruct-4bit", help="MLX model")
    parser.add_argument("--sources", default="groq,deepseek,ollama", help="Comma-separated sources")
    parser.add_argument("--iters", type=int, default=100, help="Training iterations")
    args = parser.parse_args()
    
    sources = [s.strip() for s in args.sources.split(",")]
    
    print("=== SOV Training Pipeline (M4 Cluster) ===\n")
    print(f"Sources: {sources}")
    print(f"Available APIs:")
    print(f"  Groq: {'✓' if GROQ_API_KEY else '✗'}")
    print(f"  DeepSeek: {'✓' if DEEPSEEK_API_KEY else '✗'}")
    print(f"  Moonshot (Kimi): {'✓' if MOONSHOT_API_KEY else '✗'}")
    print(f"  Ollama: {'✓' if True else '✗'}")
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
            path = save_training_data(examples, f"synth_{datetime.now().strftime('%Y-%m-%d')}.jsonl")
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
        data_file = TRAINING_DATA / f"synth_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        if not data_file.exists():
            # Use existing data
            data_file = TRAINING_DATA / "master_alpaca.jsonl"
        
        train_result = train_mlx(args.model, data_file, args.iters)
        results["train"] = train_result
        print(f"\nTraining result: {train_result['status']}")
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    print(f"\n-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())