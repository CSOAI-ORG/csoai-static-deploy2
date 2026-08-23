#!/usr/bin/env python3
"""unsloth_owem_train.py — QLoRA training for OWEM adapters on FREE GPU (Kaggle T4/P100).

WHY THIS AND NOT A SIGNUP: the free-GPU arsenal doc's real unlock is not another account,
it is Unsloth — ~70% less VRAM and ~2x faster QLoRA via custom kernels. It needs NO account,
NO credits, NO crypto wallet. It runs on the Kaggle T4 that is already authenticated and was
proven working today ($0, signed results).

⚠️ HONEST VRAM CEILING — the arsenal doc overstates this and it matters:
    "Fine-tune 70B on 24GB / what needed 80GB now fits on a T4"
  Unsloth's 70B-on-24GB figure is for a 24GB card (4090/A10/L4). A Kaggle **T4 is 16GB**.
  What actually fits, QLoRA 4-bit, seq 2048, batch 1 + grad-accum:
      ✅  0.5B - 8B   comfortable   (7-8B is the sweet spot on T4)
      ⚠️  13B         tight; needs short seq + grad checkpointing, often OOMs
      ❌  30B / 70B   DOES NOT FIT on 16GB, with or without Unsloth
  Kaggle P100 is also 16GB. Kaggle T4 x2 = 2x16GB but NOT pooled for a single model
  without FSDP/DeepSpeed sharding, which is slow enough to usually not be worth it.

  So: free GPU trains the 7-13B tier. The 30-70B tier needs credits or paid hardware.
  Stacking more free sites buys THROUGHPUT (more 7B runs in parallel), never CAPACITY.
  Anyone planning a 70B fine-tune on free T4s is planning something that cannot happen.

Usage (as a Kaggle kernel, GPU + Internet on):
    python3 unsloth_owem_train.py --base unsloth/Qwen2.5-7B-Instruct-bnb-4bit --data honey.jsonl
"""
from __future__ import annotations

import argparse, json, os, subprocess, sys, time
from pathlib import Path

OUT = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path("./out")
OUT.mkdir(parents=True, exist_ok=True)


def sh(cmd: str):
    print(f"$ {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def vram_gb() -> float:
    r = sh("nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits")
    try:
        return int(r.stdout.strip().split("\n")[0]) / 1024
    except Exception:
        return 0.0


# Empirically safe QLoRA ceilings by card size. Refuse rather than OOM 40 minutes in.
def max_params_b(vram: float) -> float:
    if vram >= 79: return 70.0     # H100/A100-80
    if vram >= 39: return 34.0     # A100-40
    if vram >= 23: return 13.0     # 4090 / L4 / A10
    if vram >= 15: return 8.0      # T4 / P100  <- the free tier
    return 3.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="unsloth/Qwen2.5-7B-Instruct-bnb-4bit")
    ap.add_argument("--data", default="honey.jsonl")
    ap.add_argument("--params-b", type=float, default=7.0, help="base size in billions")
    ap.add_argument("--seq", type=int, default=2048)
    ap.add_argument("--steps", type=int, default=60)
    ap.add_argument("--force", action="store_true", help="override the VRAM refusal")
    a = ap.parse_args()

    v = vram_gb()
    cap = max_params_b(v)
    print(f"  GPU VRAM      : {v:.0f} GB")
    print(f"  QLoRA ceiling : ~{cap:.0f}B")
    print(f"  requested     : {a.params_b:.0f}B ({a.base})")

    # FAIL CLOSED on capacity. An OOM 40 minutes into a free-tier session wastes the session
    # AND the quota; refusing in 2 seconds with the real number is strictly better.
    if a.params_b > cap and not a.force:
        print(f"\n  ❌ REFUSING: {a.params_b:.0f}B does not fit QLoRA on {v:.0f}GB.")
        print(f"     Max here is ~{cap:.0f}B. This is a hardware limit — Unsloth reduces VRAM,")
        print(f"     it does not remove the ceiling. For 30B+ you need >=40GB (credits/paid).")
        print(f"     Override with --force only if you know something this table does not.")
        return 2

    sh("pip install -q -U 'unsloth[kaggle-new] @ git+https://github.com/unslothai/unsloth.git' 2>/dev/null || pip install -q unsloth")

    try:
        from unsloth import FastLanguageModel
        import torch
        from trl import SFTTrainer
        from transformers import TrainingArguments
        from datasets import load_dataset
    except ImportError as e:
        print(f"  import failed: {e}"); return 2

    t0 = time.time()
    model, tok = FastLanguageModel.from_pretrained(
        model_name=a.base, max_seq_length=a.seq, dtype=None, load_in_4bit=True)
    model = FastLanguageModel.get_peft_model(
        model, r=16, lora_alpha=32, lora_dropout=0,
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
        use_gradient_checkpointing="unsloth", random_state=3407)

    ds = load_dataset("json", data_files=a.data, split="train")
    trainer = SFTTrainer(
        model=model, tokenizer=tok, train_dataset=ds,
        dataset_text_field="text", max_seq_length=a.seq,
        args=TrainingArguments(
            per_device_train_batch_size=2, gradient_accumulation_steps=4,
            warmup_steps=5, max_steps=a.steps, learning_rate=2e-4,
            fp16=not torch.cuda.is_bf16_supported(), bf16=torch.cuda.is_bf16_supported(),
            logging_steps=10, optim="adamw_8bit", weight_decay=0.01,
            lr_scheduler_type="linear", seed=3407, output_dir=str(OUT / "ckpt")),
    )
    stats = trainer.train()
    model.save_pretrained(str(OUT / "owem_adapter"))
    tok.save_pretrained(str(OUT / "owem_adapter"))

    report = {"base": a.base, "vram_gb": v, "params_b": a.params_b, "steps": a.steps,
              "train_loss": float(stats.training_loss), "elapsed_s": round(time.time()-t0, 1),
              "cost_usd": 0.0, "adapter": str(OUT / "owem_adapter")}
    (OUT / "unsloth_train_report.json").write_text(json.dumps(report, indent=2))
    print(f"\n  ✅ loss={report['train_loss']:.4f} in {report['elapsed_s']}s at $0")
    print(f"  -> {OUT/'owem_adapter'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
