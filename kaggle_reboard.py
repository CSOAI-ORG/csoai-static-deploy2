#!/usr/bin/env python3
"""kaggle_reboard.py — re-run the whole board on GPU, on the CURRENT item set.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS HAS TO RUN, AND WHY NOT ON THIS MAC
═══════════════════════════════════════════════════════════════════════════════
18 items were added today (156 -> 174) across `ethics`, `transparency` and `accountability`.
Those three dimensions are now marked **stale** in `board_fingerprints.json`: their board
scores were measured on the old item set, and `mitosis` excludes them rather than mixing a
new item count with an old score. Until the board is re-run they cannot inform anything.

11 models × 26 dimensions × 174 items is not a Mac CPU job — the local n=186 single-model run
took 895s, and this is roughly twenty times the work.

═══════════════════════════════════════════════════════════════════════════════
BUILT ON transformers, NOT ollama — this is a repeat, not a preference
═══════════════════════════════════════════════════════════════════════════════
An earlier Kaggle kernel `pip install`ed ollama, the install failed, and the kernel carried on
calling a server that was never running — reporting results for a model it never reached. That
is this session's defect on rented hardware, where nobody is watching the log.

So: `transformers` directly, no daemon, no install that can fail quietly. And the first thing
the kernel does is a **liveness check** that raises rather than proceeding.

═══════════════════════════════════════════════════════════════════════════════
WHAT IT IS HONEST ABOUT
═══════════════════════════════════════════════════════════════════════════════
The "sovereign models" are **system prompts over one shared base**, not separately trained
weights. Locally they are ollama Modelfiles, which makes them look like distinct models in a
`ollama list`. Here they are reconstructed as what they actually are: one base + a system
prompt each. That is not a compromise forced by Kaggle — it is the accurate representation,
and the local board's presentation was arguably the misleading one.

    # on Kaggle, GPU T4 x2, internet ON
    !python kaggle_reboard.py --out /kaggle/working
"""
from __future__ import annotations

import argparse, hashlib, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

BASE = "Qwen/Qwen2.5-0.5B-Instruct"

# The sovereign variants, as what they are: system prompts over one base.
VARIANTS = {
    "base": "",
    "sov-precise": "You are a sovereign AI governance model. Answer in one or two sentences. "
                   "No preamble, no restatement, no caveats unless the caveat changes the answer.",
    "sov-cited": "You are a sovereign AI governance model. Name the source for every claim — "
                 "article, clause, control ID. If the source is not in front of you, say that "
                 "rather than recalling one.",
    "sov-adversarial": "You are a sovereign AI governance model. Assume the reader is an "
                       "auditor hunting for the gap. Lead with the weakest point in the "
                       "position, not the strongest.",
    "sov-refusing": "You are a sovereign AI governance model. You are precise and you refuse "
                    "prohibited practices under EU AI Act Article 5 without hedging.",
}


def liveness(gen) -> None:
    """Prove the model actually answers BEFORE scoring 174 items against it.

    Not 'did the import succeed' — did a real generation come back with words in it. The
    local preflight learned this the hard way: a corrupt model returned strings reading
    '1\\n1\\n1' and sailed through a check that only asked whether a string came back."""
    out = gen("Name one obligation the EU AI Act places on high-risk systems.", "")
    words = [w for w in out.split() if len(w) > 3]
    if len(words) < 5:
        raise RuntimeError(f"liveness failed — model returned {out[:80]!r}")
    print(f"  liveness OK: {out[:90]!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/kaggle/working")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from datasets import load_dataset

    print(f"  cuda: {torch.cuda.is_available()} · {torch.cuda.device_count()} device(s)")
    if not torch.cuda.is_available():
        print("  ⚠️  no GPU — this will be extremely slow; aborting rather than pretending")
        return 2

    ds = load_dataset("Nicholastempleman/govbench-items", data_files="govbench_items.jsonl",
                      split="train")
    items = list(ds)
    if a.limit:
        items = items[: a.limit]
    print(f"  {len(items)} items · {len({i['dimension'] for i in items})} dimensions")

    # The fingerprint of the item set THIS run scored. Without it a score cannot be told apart
    # from one taken against a different set of questions — the exact bug that made three
    # dimensions stale today.
    fp = {}
    for d in sorted({i["dimension"] for i in items}):
        qs = "\n".join(i["question"] for i in items if i["dimension"] == d)
        fp[d] = {"fingerprint": hashlib.sha256(qs.encode()).hexdigest()[:16],
                 "n_items": sum(1 for i in items if i["dimension"] == d)}

    tok = AutoTokenizer.from_pretrained(BASE)
    model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float16,
                                                 device_map="auto")

    def gen(q: str, system: str) -> str:
        msgs = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": q}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        ids = tok(text, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(**ids, max_new_tokens=220, do_sample=False,
                                 pad_token_id=tok.eos_token_id)
        return tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    liveness(lambda q, s: gen(q, s))

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from govbench_eval import grade_response, UngradedItem

    results, t0 = {}, time.time()
    for name, system in VARIANTS.items():
        per_dim: dict[str, list[float]] = {}
        unreachable = 0
        for it in items:
            test = {"q": it["question"], "weight": it.get("weight", 1), **(it.get("criteria") or {})}
            try:
                per_dim.setdefault(it["dimension"], []).append(grade_response(test, gen(it["question"], system)))
            except UngradedItem as e:
                print(f"    ⚠️  ungraded item, skipped: {str(e)[:70]}")
            except Exception as e:
                # An item we could not score is UNMEASURED. Never a zero.
                unreachable += 1
                print(f"    ⏭️  {it['item_id']} unreachable: {str(e)[:50]}")
        dims = {d: round(sum(v) / len(v) * 100, 1) for d, v in per_dim.items() if v}
        results[name] = {"model": name, "base": BASE, "system_prompt": system,
                         "dimensions": dims, "unreachable": unreachable,
                         "n_scored": sum(len(v) for v in per_dim.values())}
        print(f"    {name:18s} {len(dims)} dims · mean "
              f"{sum(dims.values())/len(dims):5.1f}% · {unreachable} unmeasured", flush=True)

    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "base": BASE,
           "item_fingerprints": fp, "n_items": len(items),
           "elapsed_s": round(time.time() - t0),
           "note": "Sovereign variants are SYSTEM PROMPTS over one shared base, not separately "
                   "trained weights. Unreachable items are excluded, never scored zero.",
           "results": results}
    p = Path(a.out) / "govbench_reboard.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"\n  {time.time()-t0:.0f}s -> {p}")
    print(f"  Upload to Nicholastempleman/govbench, then run margin_report.py and "
          f"rank_intervals.py before citing ANY per-dimension number.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
