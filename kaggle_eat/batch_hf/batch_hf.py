#!/usr/bin/env python3
"""batch_hf.py — benchmark every SOV expert on free GPU using transformers. No ollama.

═══════════════════════════════════════════════════════════════════════════════
WHY NOT OLLAMA (the v1 kernel failed on this)
═══════════════════════════════════════════════════════════════════════════════
v1 ran `curl … | sh` to install ollama, did NOT check the result, and then called it:

    installing ollama…
    FileNotFoundError: No such file or directory: 'ollama'      (at 2.7s)

The install "completed" in 1.4s — it had silently failed — and the kernel used it anyway.
That is the same failure class as everything else fixed today: **an unchecked operation treated
as successful.** The fix is not to check harder, it is to remove the dependency: Kaggle ships
`transformers` and `torch` natively, and the base model is on the Hub.

**An expert here IS a system prompt.** 16 experts = 28 KB of JSON over one shared base. There is
nothing to install and nothing to rebuild.

Kaggle's free tier is a T4/P100 lottery. This draw was a **P100 (sm_60)** — older, and it breaks
some torch builds — so dtype is chosen from the actual capability rather than assumed.
"""
import json, os, sys, time
from pathlib import Path

OUT = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path("./out")
OUT.mkdir(parents=True, exist_ok=True)
BASE = "Qwen/Qwen2.5-0.5B-Instruct"

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

cap = torch.cuda.get_device_capability() if torch.cuda.is_available() else (0, 0)
name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
# bf16 needs sm_80+. A P100 is sm_60 — fp16 there, and fp32 on CPU.
dtype = torch.bfloat16 if cap[0] >= 8 else (torch.float16 if cap[0] >= 6 else torch.float32)
print(f"  GPU: {name} sm_{cap[0]}{cap[1]} -> dtype={str(dtype).split('.')[-1]}", flush=True)

experts = json.loads(Path("experts.json").read_text())
print(f"  experts: {len(experts)} system prompts over ONE base\n", flush=True)

tok = AutoTokenizer.from_pretrained(BASE)
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=dtype,
                                             device_map="auto" if torch.cuda.is_available() else None)
model.eval()

CURRENT_SYSTEM = {"p": ""}


def call_model(_m, prompt, _provider, timeout=None):
    """Signature-compatible with govbench_eval.call_model so the harness is unchanged."""
    msgs = ([{"role": "system", "content": CURRENT_SYSTEM["p"]}] if CURRENT_SYSTEM["p"] else []) + \
           [{"role": "user", "content": prompt}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    ids = tok([text], return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=180, do_sample=False,
                             pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids.input_ids.shape[1]:], skip_special_tokens=True).strip()


sys.path.insert(0, ".")
import govbench_eval as G
G.call_model = call_model            # swap the transport, keep the identical scoring harness

results, failed = [], []
t0 = time.time()
for i, (nm, sysprompt) in enumerate(experts.items(), 1):
    CURRENT_SYSTEM["p"] = sysprompt
    t = time.time()
    try:
        r = G.evaluate_model(nm, "hf")
        results.append(r)
        print(f"  [{i}/{len(experts)}] {nm:34s} {r['overall_score']:5.1f}%  ({time.time()-t:.0f}s)", flush=True)
    except Exception as e:
        # No result file is written for a failure — it stays pending rather than entering
        # the routing table unmeasured. One failure must not lose the other 15.
        failed.append({"model": nm, "error": str(e)[:140]})
        print(f"  [{i}/{len(experts)}] {nm:34s} FAILED — {str(e)[:60]}", flush=True)

rep = {"gpu": name, "sm": f"{cap[0]}.{cap[1]}", "dtype": str(dtype),
       "requested": len(experts), "measured": len(results), "failed": len(failed),
       "elapsed_s": round(time.time()-t0, 1),
       "per_model_s": round((time.time()-t0)/max(1, len(results)), 1),
       "results": results, "failures": failed}
(OUT / "batch_hf_report.json").write_text(json.dumps(rep, indent=2))
print(f"\n  {len(results)} measured · {len(failed)} failed · {rep['elapsed_s']:.0f}s "
      f"· {rep['per_model_s']:.0f}s/model")
