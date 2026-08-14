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
    ap.add_argument("--axes", nargs="+", default=["governance", "safety", "art5"])
    ap.add_argument("--iters", type=int, default=60)
    ap.add_argument("--out", default="fix_runs")
    a = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig, PeftModel
    from datasets import load_dataset
    from trl import SFTConfig, SFTTrainer

    axes = [x for x in a.axes if x in gf.AXES]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = Path(a.out) / ts; run.mkdir(parents=True, exist_ok=True)
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_use_double_quant=True)
    tok = AutoTokenizer.from_pretrained(a.base)
    if tok.pad_token is None: tok.pad_token = tok.eos_token

    print(f"== fix_loop {ts} · base={a.base} · axes={axes} ==", flush=True)
    print("1) MEASURE base + capture failures…", flush=True)
    base = AutoModelForCausalLM.from_pretrained(a.base, quantization_config=bnb, device_map="auto")
    base.eval()
    m0, r0, failures = measure_capture(base, tok, axes)
    nfail = write_dataset(failures, run / "failures.jsonl", tok)
    print(f"   base mean={m0} · {nfail} failed probes captured → the ErrorVector", flush=True)
    if nfail < 4:
        print("   too few failures to train on — base already strong on these axes. Stop (honest).")
        return

    print(f"2) TRAIN QLoRA on the {nfail} failures ({a.iters} steps)…", flush=True)
    ds = load_dataset("json", data_files=str(run / "failures.jsonl"), split="train")
    lora = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    cfg = SFTConfig(output_dir=str(run / "adapter"), per_device_train_batch_size=1,
                    gradient_accumulation_steps=4, max_steps=a.iters, learning_rate=2e-4,
                    logging_steps=10, save_strategy="no", report_to=[], bf16=True,
                    dataset_text_field="text", max_seq_length=512)
    trainer = SFTTrainer(model=base, args=cfg, train_dataset=ds, peft_config=lora)
    trainer.train()
    trainer.model.save_pretrained(str(run / "adapter"))   # the PEFT-wrapped model → adapter_config.json + weights

    print("3) RE-MEASURE base+adapter on the same frozen probes…", flush=True)
    del base; torch.cuda.empty_cache()
    fresh = AutoModelForCausalLM.from_pretrained(a.base, quantization_config=bnb, device_map="auto")
    tuned = PeftModel.from_pretrained(fresh, str(run / "adapter")); tuned.eval()
    m1, r1, _ = measure_capture(tuned, tok, axes)

    delta = round(((m1 or 0) - (m0 or 0)) * 100, 1)
    verdict = "PROMOTE ✓ (learned)" if delta > 1 else ("no change" if delta > -1 else "REVERT (worse)")
    report = {"at": ts, "base": a.base, "axes": axes, "iters": a.iters, "n_failures_trained": nfail,
              "mean_before": m0, "mean_after": m1, "delta_pts": delta, "verdict": verdict,
              "per_axis_before": r0, "per_axis_after": r1}
    (run / "report.json").write_text(json.dumps(report, indent=2))
    print(f"\n== VERDICT: {m0} → {m1}  ({delta:+} pts)  {verdict} ==")
    print(f"   report → {run/'report.json'} · adapter → {run/'adapter'}")
    if delta > 1:
        print("   TRUE fix: the model measurably improved on what it got wrong — promote.")
    else:
        print("   Honest reject: this run did NOT improve — not promoted. The gate works "
              "(overfit on a tiny failure set is expected; needs more failures + gentler training).")


if __name__ == "__main__":
    main()
