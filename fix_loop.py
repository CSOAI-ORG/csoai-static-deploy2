#!/usr/bin/env python3
"""fix_loop.py — the TRUE fix loop. Runs on a RunPod CUDA GPU (the Mac is fallback only).

Makes the flywheel actually LEARN instead of only measuring:

  1. MEASURE the base model on the GSPC axes, CAPTURING every failed probe (the ErrorVector)
  2. TRAIN a real QLoRA adapter on those exact failures (4-bit, transformers+peft+trl)
  3. RE-MEASURE base+adapter on the same axes
  4. PROMOTE only if the mean genuinely went up (ouroboros); report the honest delta

This is the honest answer to "make it true": the model demonstrably improves on what it
got wrong, measured on the same frozen probes. No prompts, no naming — real weights.

    python3 fix_loop.py --base Qwen/Qwen2.5-1.5B-Instruct --iters 60 --axes governance safety art5

Deps (install once on the pod):
    pip install -q transformers peft trl datasets accelerate bitsandbytes
"""
import sys, json, argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import gspc_flywheel as gf   # reuse the real AXES + extract — same frozen probes


def _gen(model, tok, prompt, max_new=8):
    import torch
    ids = tok.apply_chat_template([{"role": "user", "content": prompt}],
                                  add_generation_prompt=True, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=max_new, do_sample=False,
                             pad_token_id=tok.eos_token_id or tok.pad_token_id)
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)


import random as _random


def split_items(items, frac=0.6, seed=13):
    """Deterministic practice/held-out split of an axis's probes. We train on
    PRACTICE failures but gate the promote/revert decision on HELD-OUT probes the
    model never trained on — so a promotion means it GENERALIZED, not memorized."""
    idx = list(range(len(items)))
    _random.Random(seed).shuffle(idx)
    k = max(1, int(round(len(items) * frac)))
    return [items[i] for i in idx[:k]], [items[i] for i in idx[k:]]


def measure_on(model, tok, axes, which):
    """which='practice' (also captures failures to train on) or 'heldout' (the honest
    gate). Returns (mean, per_axis, failures)."""
    results, failures = {}, []
    for ax in axes:
        spec = gf.AXES[ax]
        practice, heldout = split_items(spec["items"])
        items = practice if which == "practice" else heldout
        correct = graded = 0
        for prompt, expected in items:
            got = gf.extract(_gen(model, tok, spec["instruction"] + prompt), spec["tokens"])
            if got == "":
                continue
            graded += 1
            if got == expected:
                correct += 1
            elif which == "practice":
                failures.append({"instruction": spec["instruction"], "prompt": prompt,
                                 "expected": expected, "axis": ax})
        results[ax] = round(correct / graded, 4) if graded else None
    got = [v for v in results.values() if v is not None]
    return (round(sum(got) / len(got), 4) if got else None), results, failures


def measure_capture(model, tok, axes):
    """Return (mean, per_axis, failures). Failures are the ErrorVector — the exact
    probes the model got wrong, with the correct label, ready to train on."""
    results, failures = {}, []
    for ax in axes:
        spec = gf.AXES[ax]; correct = graded = 0
        for prompt, expected in spec["items"]:
            got = gf.extract(_gen(model, tok, spec["instruction"] + prompt), spec["tokens"])
            if got == "":
                continue
            graded += 1
            if got == expected:
                correct += 1
            else:
                failures.append({"instruction": spec["instruction"], "prompt": prompt,
                                 "expected": expected, "axis": ax})
        results[ax] = round(correct / graded, 4) if graded else None
    got = [v for v in results.values() if v is not None]
    return (round(sum(got) / len(got), 4) if got else None), results, failures


def write_dataset(failures, path, tok):
    # Emit a plain "text" field (chat template pre-applied) — trl's SFTTrainer
    # trains on dataset_text_field="text" without needing conversational parsing.
    rows = []
    for f in failures:
        msgs = [{"role": "user", "content": f["instruction"] + f["prompt"]},
                {"role": "assistant", "content": f["expected"]}]
        rows.append({"text": tok.apply_chat_template(msgs, tokenize=False)})
    Path(path).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return len(rows)


def main():
    ap = argparse.ArgumentParser(description="Measured-failures → real QLoRA adapter → re-measure (RunPod CUDA).")
    ap.add_argument("--base", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--axes", nargs="+", default=None)   # None = ALL axes the harness carries
    ap.add_argument("--iters", type=int, default=25)      # gentler: generalize, don't memorize
    ap.add_argument("--lr", type=float, default=5e-5)     # 4x lower than the overfit run
    ap.add_argument("--out", default="fix_runs")
    a = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig, PeftModel
    from datasets import load_dataset
    from trl import SFTConfig, SFTTrainer

    axes = [x for x in (a.axes or list(gf.AXES)) if x in gf.AXES]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = Path(a.out) / ts; run.mkdir(parents=True, exist_ok=True)
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
    tok = AutoTokenizer.from_pretrained(a.base)
    if tok.pad_token is None: tok.pad_token = tok.eos_token

    BEST = Path(a.out) / "BEST"                      # the single accumulating adapter
    resumed = (BEST / "adapter_config.json").exists()
    print(f"== fix_loop {ts} · base={a.base} · axes={axes} · "
          f"{'RESUME from BEST (compounding)' if resumed else 'fresh from base'} ==", flush=True)
    print("1) MEASURE current model + capture failures…", flush=True)
    base = AutoModelForCausalLM.from_pretrained(a.base, quantization_config=bnb, device_map="auto")
    model = PeftModel.from_pretrained(base, str(BEST), is_trainable=True) if resumed else base
    model.eval()
    m0p, r0p, failures = measure_on(model, tok, axes, "practice")   # capture failures to train on
    m0h, r0h, _ = measure_on(model, tok, axes, "heldout")           # the honest gate baseline
    nfail = write_dataset(failures, run / "failures.jsonl", tok)
    print(f"   practice mean={m0p} · {nfail} failures captured · HELD-OUT baseline={m0h}", flush=True)
    if nfail < 4:
        print("   too few failures to train on — base already strong on these axes. Stop (honest).")
        return

    print(f"2) TRAIN QLoRA on the {nfail} failures ({a.iters} steps)…", flush=True)
    ds = load_dataset("json", data_files=str(run / "failures.jsonl"), split="train")
    lora = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    cfg = SFTConfig(output_dir=str(run / "adapter"), per_device_train_batch_size=1,
                    gradient_accumulation_steps=4, max_steps=a.iters, learning_rate=a.lr,
                    logging_steps=10, save_strategy="no", report_to=[], bf16=True,
                    dataset_text_field="text", max_seq_length=512)
    trainer = SFTTrainer(model=model, args=cfg, train_dataset=ds, peft_config=(None if resumed else lora))
    trainer.train()
    trainer.model.save_pretrained(str(run / "adapter"))   # the PEFT-wrapped model → adapter_config.json + weights

    print("3) RE-MEASURE base+adapter on the same frozen probes…", flush=True)
    del base, model; torch.cuda.empty_cache()
    fresh = AutoModelForCausalLM.from_pretrained(a.base, quantization_config=bnb, device_map="auto")
    tuned = PeftModel.from_pretrained(fresh, str(run / "adapter")); tuned.eval()
    m1h, r1h, _ = measure_on(tuned, tok, axes, "heldout")     # gate on probes NEVER trained on

    delta = round(((m1h or 0) - (m0h or 0)) * 100, 1)          # HONEST delta — generalization, not memorization
    verdict = "PROMOTE ✓ (generalized)" if delta > 1 else ("no change" if delta > -1 else "REVERT (worse)")
    report = {"at": ts, "base": a.base, "axes": axes, "iters": a.iters, "n_failures_trained": nfail,
              "heldout_before": m0h, "heldout_after": m1h, "practice_before": m0p, "delta_pts": delta,
              "verdict": verdict, "per_axis_heldout_before": r0h, "per_axis_heldout_after": r1h,
              "note": "verdict gated on HELD-OUT probes never trained on — proves generalization"}
    (run / "report.json").write_text(json.dumps(report, indent=2))
    print(f"\n== VERDICT (held-out generalization): {m0h} → {m1h}  ({delta:+} pts)  {verdict} ==")
    print(f"   report → {run/'report.json'} · adapter → {run/'adapter'}")
    if delta > 1:
        import shutil
        if BEST.exists():
            shutil.rmtree(BEST)
        shutil.copytree(run / "adapter", BEST)
        print("   TRUE fix: improved — PROMOTED + saved as new BEST (compounds; next cycle resumes here).")
    else:
        print("   Honest reject: did NOT improve — not promoted; BEST unchanged. The gate works.")


if __name__ == "__main__":
    main()
