#!/usr/bin/env python3
"""voter_transformers.py — council voter, HF transformers + PEFT path (CUDA pods).

Independent measurement implementation #1. Loads base (4-bit) and base+adapter,
runs the frozen GSPC probes with the even/odd holdout split, emits:
  rows.jsonl    — one row per probe execution (before/after extractions)
  verdict.json  — the canonical vote (verdict.py) + identity + rows sha256

The vote is hash-committed, NOT signed — the signing key never leaves the owner
keystone; promotion_council.py verifies and issues signed receipts Mac-side.

  python3 voter_transformers.py --base Qwen/Qwen2.5-1.5B-Instruct \
      --adapter fix_runs/BEST --axes governance safety --out votes/run1
"""
from __future__ import annotations
import argparse, hashlib, json, socket, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))                       # council/
sys.path.insert(0, str(ROOT.parent.parent))          # repo root (gspc_flywheel)
import gspc_flywheel as gf
from verdict import vote_from_rows


def _gen(model, tok, prompt, max_new=8):
    import torch
    ids = tok.apply_chat_template([{"role": "user", "content": prompt}],
                                  add_generation_prompt=True, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=max_new, do_sample=False,
                             pad_token_id=tok.eos_token_id or tok.pad_token_id)
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)


def run(base_name, adapter_path, axes, outdir):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import PeftModel

    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16,
                             bnb_4bit_use_double_quant=True)
    tok = AutoTokenizer.from_pretrained(base_name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(base_name, quantization_config=bnb,
                                                device_map="auto")
    base.eval()
    fresh = AutoModelForCausalLM.from_pretrained(base_name, quantization_config=bnb,
                                                 device_map="auto")
    tuned = PeftModel.from_pretrained(fresh, adapter_path)
    tuned.eval()

    rows = []
    for ax in axes:
        spec = gf.AXES[ax]
        for idx, (prompt, expected) in enumerate(spec["items"]):
            full = spec["instruction"] + prompt
            b = gf.extract(_gen(base, tok, full), spec["tokens"])
            a = gf.extract(_gen(tuned, tok, full), spec["tokens"])
            rows.append({"item": prompt[:120], "axis": ax,
                         "pool": "even" if idx % 2 == 0 else "odd",
                         "expected": expected, "before": b, "after": a})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--axes", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--voter-id", default=None)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows = run(a.base, a.adapter, a.axes, out)
    (out / "rows.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    rows_sha = hashlib.sha256((out / "rows.jsonl").read_bytes()).hexdigest()
    verdict = vote_from_rows(rows)
    verdict.update({
        "voter_id": a.voter_id or f"transformers@{socket.gethostname()}",
        "implementation": "hf-transformers+peft/4bit-nf4/greedy",
        "base": a.base, "adapter": str(a.adapter), "axes": a.axes,
        "rows_sha256": rows_sha,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    (out / "verdict.json").write_text(json.dumps(verdict, indent=1) + "\n")
    print(json.dumps({"verdict": verdict["vote"],
                      "delta_unseen": verdict.get("delta_unseen"),
                      "rows": len(rows), "out": str(out)}, indent=1))


if __name__ == "__main__":
    main()
