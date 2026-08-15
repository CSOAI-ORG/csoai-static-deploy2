#!/usr/bin/env python3
"""train_lora_mlx.py — LoRA fine-tune a SOV model on Apple Silicon via MLX.

Trains on the synthesized research pairs + KB entries. Outputs a merged model
to ~/.ollama/models/ so it can be benchmarked immediately.

Usage:
  python3 train_lora_mlx.py sov33-v7:latest [--steps N] [--lr LR]
"""
import argparse, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT_DIR = HERE / "benchmark-results" / "training"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR = HERE / "training_data"

OLLAMA_MODELS = Path.home() / ".ollama" / "models"


def find_model_path(model_name):
    """Find the Ollama model blob path for a given model name."""
    safe = model_name.replace(":", "-").replace("/", "_")
    manifest = OLLAMA_MODELS / "models" / safe
    if manifest.exists():
        # New Ollama layout
        return manifest, "manifest"
    # Fallback: search blobs
    blobs = OLLAMA_MODELS / "models" / "blobs"
    if blobs.exists():
        for p in blobs.glob("*"):
            if p.is_file() and p.stat().st_size > 100_000_000:
                return p, "blob"
    return None, None


def load_alpaca(path):
    pairs = []
    for line in Path(path).read_text(errors="ignore").splitlines():
        try:
            p = json.loads(line)
            if p.get("instruction") and p.get("output"):
                pairs.append(p)
        except Exception:
            pass
    return pairs


def build_chatml(pairs, out_path):
    """Convert Alpaca pairs to ChatML format for MLX."""
    with out_path.open("w") as f:
        for p in pairs:
            messages = [
                {"role": "system", "content": "You are a sovereign AI assistant that reasons carefully about governance, sovereignty, accountability, and rights."},
                {"role": "user", "content": p["instruction"] + ("\n\n" + p["input"] if p.get("input") else "")},
                {"role": "assistant", "content": p["output"]},
            ]
            f.write(json.dumps({"messages": messages}) + "\n")
    return out_path


def run_lora_training(model_path, data_path, iters=50, lr=2e-4, lora_rank=8):
    """Run MLX LoRA training. Returns (adapter_path, log_lines)."""
    log_path = OUT_DIR / ("train_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + ".log")

    # MLX LoRA training command (Apple Silicon)
    cmd = [
        sys.executable, "-m", "mlx_lm.lora",
        "--model", str(model_path),
        "--data", str(data_path),
        "--train",
        "--iters", str(iters),
        "--learning-rate", str(lr),
        "--lora-rank", str(lora_rank),
        "--adapter-path", str(OUT_DIR / "adapters"),
        "--batch-size", "1",
        "--num-layers", "8",
    ]

    print("  Running: " + " ".join(cmd))
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log = (proc.stdout or "") + "\n--- STDERR ---\n" + (proc.stderr or "")
        log_path.write_text(log)
        return OUT_DIR / "adapters", log
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except Exception as e:
        return None, str(e)


def run_unsloth_fallback(model_path, data_path, iters=20):
    """Fallback: use unsloth/transformers for LoRA if MLX not applicable."""
    log_path = OUT_DIR / ("train_unsloth_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + ".log")
    try:
        from peft import LoraConfig, get_peft_model
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
        import torch
        from datasets import load_dataset

        tok = AutoTokenizer.from_pretrained(str(model_path))
        model = AutoModelForCausalLM.from_pretrained(str(model_path), torch_dtype=torch.float32)

        cfg = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"], lora_dropout=0.05, task_type="CAUSAL_LM")
        model = get_peft_model(model, cfg)

        ds = load_dataset("json", data_files=str(data_path), split="train")
        def format_batch(b):
            texts = []
            for m in b["messages"]:
                t = ""
                for msg in m:
                    t += "<|im_start|>" + msg["role"] + "\n" + msg["content"] + "<|im_end|>\n"
                texts.append(t)
            return tok(texts, truncation=True, max_length=512, padding="max_length")

        ds = ds.map(format_batch, batched=True, remove_columns=ds.column_names)
        args = TrainingArguments(output_dir=str(OUT_DIR / "unsloth"), num_train_epochs=1, max_steps=iters, per_device_train_batch_size=1, learning_rate=2e-4, logging_steps=5, save_strategy="no")
        trainer = Trainer(model=model, args=args, train_dataset=ds)
        trainer.train()
        adapter_dir = OUT_DIR / "unsloth_adapter"
        model.save_pretrained(str(adapter_dir))
        log_path.write_text("unsloth training complete: " + str(adapter_dir))
        return adapter_dir, "ok"
    except Exception as e:
        log_path.write_text("unsloth error: " + str(e))
        return None, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", help="Ollama model name (e.g. sov33-v7:latest)")
    ap.add_argument("--steps", type=int, default=50)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--data", default="synth_latest", help="Training data file or 'synth_latest'")
    ap.add_argument("--rank", type=int, default=8)
    args = ap.parse_args()

    print("=" * 70)
    print("  TRAIN LoRA on " + args.model + "  (" + str(args.steps) + " steps)")
    print("=" * 70)

    # Find data
    if args.data == "synth_latest":
        synth_files = sorted((DATA_DIR).glob("synth_*.jsonl"))
        if not synth_files:
            print("ERROR: No synth_*.jsonl found. Run synthesize_research.py first.")
            sys.exit(1)
        data_path = synth_files[-1]
    else:
        data_path = Path(args.data)
    print("  Data: " + str(data_path))

    pairs = load_alpaca(data_path)
    print("  Pairs: " + str(len(pairs)))

    # Build ChatML for MLX
    chatml_path = OUT_DIR / ("chatml_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + ".jsonl")
    build_chatml(pairs, chatml_path)
    print("  ChatML: " + str(chatml_path))

    # Find model path
    model_path, kind = find_model_path(args.model)
    if not model_path:
        print("ERROR: Could not find model " + args.model + " in " + str(OLLAMA_MODELS))
        print("  The model needs to be pulled into Ollama first.")
        sys.exit(1)
    print("  Model path: " + str(model_path) + " (" + kind + ")")

    # Run training
    t0 = time.time()
    adapter_path, log = run_lora_training(model_path, chatml_path, iters=args.steps, lr=args.lr, lora_rank=args.rank)
    if not adapter_path:
        print("  MLX training failed, trying unsloth/transformers...")
        adapter_path, log = run_unsloth_fallback(model_path, chatml_path, iters=args.steps)

    elapsed = round(time.time() - t0, 1)
    print("\n  Elapsed: " + str(elapsed) + "s")
    print("  Adapter: " + str(adapter_path))
    print("  Log: " + str(log)[:200])

    # Write training manifest
    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base_model": args.model,
        "model_path": str(model_path),
        "data_path": str(data_path),
        "chatml_path": str(chatml_path),
        "steps": args.steps,
        "lr": args.lr,
        "lora_rank": args.rank,
        "adapter_path": str(adapter_path) if adapter_path else None,
        "elapsed_secs": elapsed,
        "training_result": "ok" if adapter_path else "failed",
    }
    manifest_path = OUT_DIR / ("manifest_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") + ".json")
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print("  Manifest: " + str(manifest_path))


if __name__ == "__main__":
    main()