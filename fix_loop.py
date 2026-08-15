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


def measure_capture(model, tok, axes, pool=None, detail=None):
    """Return (mean, per_axis, failures). Failures are the ErrorVector — the exact
    probes the model got wrong, with the correct label, ready to train on.
    pool: None = all items; 'even'/'odd' = deterministic index-parity split per axis.
      The parity split exists to kill train==test contamination: train on the even
      pool's failures, and the odd pool stays UNSEEN — its delta is the honest one.
    detail: optional dict to receive per-axis per-pool [correct, graded] counts."""
    results, failures = {}, []
    for ax in axes:
        spec = gf.AXES[ax]; correct = graded = 0
        pools = {"even": [0, 0], "odd": [0, 0]}
        for idx, (prompt, expected) in enumerate(spec["items"]):
            item_pool = "even" if idx % 2 == 0 else "odd"
            if pool and item_pool != pool:
                continue
            got = gf.extract(_gen(model, tok, spec["instruction"] + prompt), spec["tokens"])
            if got == "":
                continue
            graded += 1
            pools[item_pool][1] += 1
            if got == expected:
                correct += 1
                pools[item_pool][0] += 1
            else:
                failures.append({"instruction": spec["instruction"], "prompt": prompt,
                                 "expected": expected, "axis": ax, "pool": item_pool})
        results[ax] = round(correct / graded, 4) if graded else None
        if detail is not None:
            detail[ax] = pools
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
    ap.add_argument("--no-holdout", action="store_true",
                    help="train on ALL failures and re-measure on the same probes "
                         "(legacy mode — cannot rule out memorization; default is the "
                         "honest holdout: train on even-pool failures, verdict on UNSEEN odd pool)")
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
    holdout = not a.no_holdout
    print("1) MEASURE current model + capture failures"
          + (" (even/odd split — verdict will key on the UNSEEN pool)" if holdout else "") + "…", flush=True)
    base = AutoModelForCausalLM.from_pretrained(a.base, quantization_config=bnb, device_map="auto")
    model = PeftModel.from_pretrained(base, str(BEST), is_trainable=True) if resumed else base
    model.eval()
    base_detail = {}
    m0, r0, failures = measure_capture(model, tok, axes, detail=base_detail)
    train_failures = [f for f in failures if f["pool"] == "even"] if holdout else failures
    nfail = write_dataset(train_failures, run / "failures.jsonl", tok)
    print(f"   base mean={m0} · {len(failures)} failed probes captured"
          + (f" ({nfail} in the train pool, {len(failures)-nfail} held out UNSEEN)" if holdout else "")
          + " → the ErrorVector", flush=True)
    if nfail < 4:
        print("   too few failures to train on — base already strong on these axes. Stop (honest).")
        return

    print(f"2) TRAIN QLoRA on the {nfail} {'train-pool ' if holdout else ''}failures ({a.iters} steps)…", flush=True)
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

    print("3) RE-MEASURE base+adapter — " +
          ("SEEN pool (memorization ceiling) and UNSEEN pool (the honest number)" if holdout
           else "the same frozen probes (legacy: train==test)") + "…", flush=True)
    del base, model; torch.cuda.empty_cache()
    fresh = AutoModelForCausalLM.from_pretrained(a.base, quantization_config=bnb, device_map="auto")
    tuned = PeftModel.from_pretrained(fresh, str(run / "adapter")); tuned.eval()

    def _pool_mean(detail, pool):
        vals = [c / g for c, g in (detail[ax][pool] for ax in detail) if g > 0]
        return round(sum(vals) / len(vals), 4) if vals else None

    def _pool_per_axis(detail, pool):
        return {ax: round(c / g, 4) if g > 0 else None
                for ax, (c, g) in ((a_, detail[a_][pool]) for a_ in detail)}

    if holdout:
        m1_seen, r1_seen, _ = measure_capture(tuned, tok, axes, pool="even")
        m1_unseen, r1_unseen, _ = measure_capture(tuned, tok, axes, pool="odd")
        m0_seen = _pool_mean(base_detail, "even")
        m0_unseen = _pool_mean(base_detail, "odd")
        delta = round(((m1_unseen or 0) - (m0_unseen or 0)) * 100, 1)   # verdict keys on UNSEEN
        delta_seen = round(((m1_seen or 0) - (m0_seen or 0)) * 100, 1)
        verdict = "PROMOTE ✓ (generalized)" if delta > 1 else ("no change" if delta > -1 else "REVERT (worse)")
        m1, r1 = m1_unseen, r1_unseen
    else:
        m1, r1, _ = measure_capture(tuned, tok, axes)
        delta = round(((m1 or 0) - (m0 or 0)) * 100, 1)
        delta_seen = None
        verdict = "PROMOTE ✓ (learned)" if delta > 1 else ("no change" if delta > -1 else "REVERT (worse)")
        m0_seen = m0_unseen = None

    report = {"at": ts, "base": a.base, "axes": axes, "iters": a.iters,
              "holdout": holdout, "n_failures_captured": len(failures),
              "n_failures_trained": nfail,
              "mean_before": m0, "mean_after": m1, "delta_pts": delta, "verdict": verdict,
              "per_axis_before": (_pool_per_axis(base_detail, "odd") if holdout else r0),
              "per_axis_after": r1,
              "per_axis_before_full": r0}
    if holdout:
        report["holdout_detail"] = {
            "seen": {"before": m0_seen, "after": m1_seen, "delta_pts": delta_seen,
                     "note": "memorization ceiling — never quote as learning"},
            "unseen": {"before": m0_unseen, "after": m1_unseen, "delta_pts": delta,
                       "note": "generalization — the verdict number"},
        }
    (run / "report.json").write_text(json.dumps(report, indent=2))
    if holdout:
        print(f"\n== VERDICT (UNSEEN pool): {m0_unseen} → {m1_unseen}  ({delta:+} pts)  {verdict} ==")
    else:
        print(f"\n== VERDICT: {m0} → {m1}  ({delta:+} pts)  {verdict} ==")
    if holdout:
        print(f"   seen-pool delta {delta_seen:+} pts (memorization ceiling) · "
              f"unseen-pool delta {delta:+} pts (generalization — the number that counts)")
    print(f"   report → {run/'report.json'} · adapter → {run/'adapter'}")
    if delta > 1:
        import shutil
        if BEST.exists():
            shutil.rmtree(BEST)
        shutil.copytree(run / "adapter", BEST)
        print("   TRUE fix: improved on UNSEEN probes — PROMOTED + saved as new BEST (compounds).")
    else:
        print("   Honest reject: did NOT improve on unseen probes — not promoted; BEST unchanged. The gate works.")


if __name__ == "__main__":
    main()
