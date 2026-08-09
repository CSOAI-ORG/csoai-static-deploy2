#!/usr/bin/env python3
"""train_dream.py — the Dream Engine training run. GPU-gated; ready to fire, honest about what it is.

    # ON A FUNDED A100 (not the Mac):
    pip install "transformers>=4.44" "trl>=0.9" peft datasets accelerate bitsandbytes
    python3 train_dream.py --base Qwen/Qwen2.5-3B-Instruct --epochs 2

This trains a SMALL corrective operator (LoRA adapter) on the estate's own honey — the rows a model got
wrong against a dated, anchored label — to reduce a MEASURED drift. It is the honest version of the
"Dream Engine": not a model that tops all benchmarks (measured dead five times), but an operator that
either measurably improves on a specific axis at n>=30 with a CI clear of zero, or is RETIRED per
DREAM_ENGINE_PREREG.md.

TWO BARRIERS ENFORCED IN CODE, because both are defects this estate actually shipped:
  1. CONTAMINATION — training must not touch the eval bank. This script trains ONLY on
     _alignment/dream/dream_dataset.jsonl (honey from RUNS) and refuses to start if that file is empty.
     The measured comparison (run separately) uses the PRIVATE held-out split, never these rows.
  2. NO FALSE SUCCESS — it will not emit an adapter and call it done without the pre-registration
     present. Improvement is a claim only after sovos.py measures base-vs-adapter on held-out items.

It does not run on the Mac (no GPU). It is complete and staged so that funding is the only remaining
gate — one command, on the pod.
"""
import argparse, json, os, sys

DREAM = os.path.expanduser("~/clawd/_alignment/dream/dream_dataset.jsonl")
PREREG = os.path.expanduser("~/clawd/_alignment/DREAM_ENGINE_PREREG.md")
OUTDIR = os.path.expanduser("~/clawd/_alignment/dream/adapter")


def load_examples():
    if not os.path.exists(DREAM):
        sys.exit(f"NO DATASET: {DREAM} missing. Run dream_engine.py --stage first.")
    rows = [json.loads(l) for l in open(DREAM, errors="ignore") if l.strip()]
    if not rows:
        sys.exit("DATASET EMPTY: training on nothing is the emptiest false success. Aborting.")
    if not os.path.exists(PREREG):
        sys.exit("NO PRE-REGISTRATION: refuse to train without DREAM_ENGINE_PREREG.md — the contract "
                 "that fixes the kill criterion before the result exists.")
    return rows


def to_text(r):
    # the correction, phrased as supervision: given the item + axis, produce the measured-correct label.
    labels_hint = {"governance": "PROHIBITED / HIGH_RISK / LIMITED_RISK / MINIMAL_RISK",
                   "safety": "REFUSE / COMPLY", "provenance": "SURVIVES / DESTROYED",
                   "continuity": "QUANTUM_VULNERABLE / QUANTUM_SAFE / NOT_APPLICABLE",
                   "conformance": "CONFORMS / VIOLATES", "openness": "PERMITTED / RESTRICTED"}
    hint = labels_hint.get(r.get("axis"), "the correct label")
    return (f"<|user|>\nAxis: {r.get('axis')}. Answer with exactly one of: {hint}.\n\n"
            f"{r.get('context','')}\n\nLabel only.\n<|assistant|>\n{r.get('target','')}")


def main():
    ap = argparse.ArgumentParser(description="Train the corrective Dream Engine operator (GPU-gated)")
    ap.add_argument("--base", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--epochs", type=float, default=2.0)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--dry-run", action="store_true", help="validate data + config without importing GPU deps")
    a = ap.parse_args()

    rows = load_examples()
    print(f"dream dataset: {len(rows)} corrective examples · base={a.base} · epochs={a.epochs}")
    by_axis = {}
    for r in rows: by_axis[r.get("axis")] = by_axis.get(r.get("axis"), 0) + 1
    print(f"  by axis: {by_axis}")
    if a.dry_run:
        print("  --dry-run: data + config valid. Remove --dry-run on a GPU to train.")
        print(f"  sample:\n{to_text(rows[0])[:300]}")
        return

    try:
        import torch
        from datasets import Dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import LoraConfig
        from trl import SFTTrainer, SFTConfig
    except ImportError as e:
        sys.exit(f"GPU training deps not present ({e}). This script runs on a funded A100, not the Mac. "
                 "Use --dry-run here to validate; install the deps and run on the pod.")

    tok = AutoTokenizer.from_pretrained(a.base)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    ds = Dataset.from_list([{"text": to_text(r)} for r in rows])
    model = AutoModelForCausalLM.from_pretrained(a.base, torch_dtype=torch.bfloat16, device_map="auto")
    peft_cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
                          task_type="CAUSAL_LM",
                          target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    cfg = SFTConfig(output_dir=OUTDIR, num_train_epochs=a.epochs, per_device_train_batch_size=4,
                    gradient_accumulation_steps=4, learning_rate=a.lr, logging_steps=10,
                    save_strategy="epoch", bf16=True, max_seq_length=1024, report_to=[])
    trainer = SFTTrainer(model=model, args=cfg, train_dataset=ds, peft_config=peft_cfg,
                         dataset_text_field="text", tokenizer=tok)
    trainer.train()
    trainer.save_model(OUTDIR)
    print(f"\n  adapter saved → {OUTDIR}")
    print("  NOT DONE YET. Now MEASURE, per DREAM_ENGINE_PREREG.md:")
    print("    serve base+adapter, then run sovos.py against the PRIVATE held-out split.")
    print("    Claim improvement ONLY if the paired delta CI is clear of zero AND positive. Else retire.")


if __name__ == "__main__":
    main()
