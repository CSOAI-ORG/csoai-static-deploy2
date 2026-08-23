#!/usr/bin/env python3
"""free_quota_scheduler.py — N-site free-quota coordinator (stub, offline).

Coordinates fine-tune/eval across the free compute sites (Kaggle, Oracle,
HuggingFace) by tracking each site's free window/quota and emitting a "what to
run next, where, when" plan. Pure disk + stdlib: no live GPU/tunnel dependency,
so it always completes (Ralph-friendly). Records state to scheduler_state.json.

Sites + free quotas (honest, from the estate's config):
  kaggle  : free T4/P100, ~30h/wk GPU quota (fine-tune + eval)
  oracle  : always-free CPU (2 cores) — RAG + inference server (LIVE :8771)
  hf      : free mirror of corpus+adapter (GATED on HF_TOKEN)
  fleet   : A100 pod (paid) — only the 30B/14B specialists
"""
import json, os, time, pathlib

STATE = pathlib.Path(__file__).parent / "scheduler_state.json"
SITES = {
    "kaggle":  {"role": "train+eval",  "quota_hw": 30, "cost": 0, "gpu": "free T4/P100", "url": "nicktempleman/oowm-free-train"},
    "oracle":  {"role": "serve+rag",   "quota_hw": 168, "cost": 0, "gpu": "CPU x2", "url": "141.147.73.85:8771"},
    "hf":      {"role": "mirror",      "quota_hw": 168, "cost": 0, "gpu": "none", "url": "gated: HF_TOKEN", "gate": "HF_TOKEN"},
    "fleet":   {"role": "specialists", "quota_hw": 168, "cost": "paid", "gpu": "A100", "url": "runpod-a100"},
}

PIPELINE = [
    ("kaggle",  "fine-tune sovereign LoRA on the 19,350-pair corpus"),
    ("kaggle",  "eval on free MMLU/GPQA"),
    ("hf",      "mirror corpus + adapter"),
    ("oracle",  "serve RAG + inference (live :8771)"),
    ("fleet",   "keep only 30B/14B specialists; route the rest free"),
]

def plan(now=None):
    now = now or time.time()
    return {
        "schema": "csoai.free-quota-scheduler/0.1",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "sites": SITES,
        "pipeline": [{"site": s, "task": t} for s, t in PIPELINE],
        "next_batch": [
            "1. kaggle: ensure oowm-free-train runs on a T4 (P100 env is broken -> retry / request T4)",
            "2. kaggle: pull adapter + eval, add to model_registry as cost=0 sovereign specialist",
            "3. hf: mirror corpus+adapter once HF_TOKEN present",
            "4. oracle: gateway live; wire front-ends to :8771",
            "5. fleet: keep big-tier specialists only, free for the rest",
        ],
        "honest_note": "free sites cost=0; A100 (fleet) is the only paid tier. Oracle + Kaggle are the reliable free path; HF gated on token.",
    }

def main():
    p = plan()
    STATE.write_text(json.dumps(p, indent=2))
    print("=== FREE-QUOTA SCHEDULER ===")
    for site, info in SITES.items():
        gate = f" | GATE={info['gate']}" if "gate" in info else ""
        print(f"  {site:<8} {info['role']:<10} cost={info['cost']} {info['gpu']}{gate}")
    print("\nnext_batch:")
    for b in p["next_batch"]:
        print(f"  - {b}")
    print("\nwrote", STATE)

if __name__ == "__main__":
    main()
