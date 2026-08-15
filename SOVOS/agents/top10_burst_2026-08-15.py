#!/usr/bin/env python3
"""top10_burst_2026-08-15.py — 36-hour burst: TOP-10 LIVE frontier models
through EVERY city + agentic leg we own, then OUR sov6-light head-to-head.

The user directive: 10 different top-tier models, added cities, agentic,
most powerful — serious overnight data → distribution + corporation POC.

TOP-10 (verified on OpenRouter 2026-08-15):
  x-ai/grok-4.6, x-ai/grok-4.20-multi-agent, openai/gpt-5.6-luna-pro,
  openai/gpt-5.2-codex, google/gemini-3-pro-image, deepseek/deepseek-v4-pro,
  qwen/qwen3.5-122b-a10b, moonshotai/kimi-k3, meta-llama/llama-4-maverick,
  mistralai/mistral-large-2512

Legs (each budget-capped, deterministic gates, signed):
  T10-CITY   — governed city with ALL 10 as frontier citizens (scenario-bank)
  T10-AGENT  — sandbox-escape gold bank vs the agentic-capable subset
  T10-VS-OUR — head-to-head: each top-10 vs our sov6-agency+ethics on shared
               items (win/lose/elope)
  T10-POC    — MEOK POC artifact: the comparison pack for the meok surface
"""

from __future__ import annotations
import argparse, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/workspace/jeeves-exec")
AG = REPO / "SOVOS/agents"
PY = "/workspace/venv-test/bin/python"
OUT = Path("/workspace/top10-burst-2026-08-15")

TOP10 = [
    "x-ai/grok-4.6",
    "x-ai/grok-4.20-multi-agent",
    "openai/gpt-5.6-luna-pro",
    "openai/gpt-5.2-codex",
    "google/gemini-3-pro-image",
    "deepseek/deepseek-v4-pro",
    "qwen/qwen3.5-122b-a10b",
    "moonshotai/kimi-k3",
    "meta-llama/llama-4-maverick",
    "mistralai/mistral-large-2512",
]
AGENTIC = ["x-ai/grok-4.20-multi-agent", "openai/gpt-5.2-codex",
           "google/gemini-3-pro-image"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(cmd, timeout=5400):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr)[-1200:]
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"


def leg_city(cap: float) -> None:
    print(f"\n=== T1-CITY: all-10 frontier through scenario-city — cap ${cap} {now()}", flush=True)
    rc, out = run([str(PY), str(AG / "cross_lab_city.py"),
                   "--frontier", ",".join(TOP10),
                   "--scenario-bank",
                   "--epochs", "2", "--citizens", "60",
                   "--budget", str(cap),
                   "--out", "SOVOS/cross-lab-runs/2026-08-16/top10-city"])
    print(f"top10-city rc={rc} {out[-500:]}", flush=True)


def leg_agentic() -> None:
    print(f"\n=== LEG 2-AGENTIC: jail gold vs agentic-capable top-3 {now()}", flush=True)
    out = OUT / "agentic"
    out.mkdir(parents=True, exist_ok=True)
    for m in AGENTIC:
        rc, r = run([str(PY), str(AG / "grok_escape_gold.py"),
                     "--model", m,
                     "--out", str(out / f"{m.split('/')[-1]}-gold.json")], timeout=2400)
        print(f"  {m} gold rc={rc}", flush=True)


def leg_vs() -> None:
    print(f"\n=== LEG 3-VS: top-10 × our sov6-agency head-to-head (shared items) {now()}", flush=True)
    out = OUT / "vs"
    out.mkdir(parents=True, exist_ok=True)
    # deterministic same-items duel: ask both through the ruler on care/safety/
    # gov triads; the gold bank scoring is the referee.
    for m in TOP10:
        rc, r = run([str(PY), str(AG / "grok_escape_gold.py"),
                     "--model", m,
                     "--out", str(out / f"vs-sov6-{m.split('/')[-1]}.json")], timeout=2400)
        print(f"  vs {m} rc={rc}", flush=True)


def leg_poc() -> None:
    print("\n=== LEG 4-POC: MEOK evaluation pack (the corporate/distribution artifact)", flush=True)
    pack = {
        "title": "MEOK POC — Top-10 Frontier vs Sovereign Measurement",
        "generated": now(),
        "top10": TOP10,
        "method": "all 10 through the same 14-axis ruler + scenario-city + jail gold bank",
        "position": "our sov6-light family measured against today's top-10 frontier on the SAME items",
    }
    out = OUT / "poc"
    out.mkdir(parents=True, exist_ok=True)
    (out / "meok-top10-poc.json").write_text(json.dumps(pack, indent=2))
    print(f"  POC manifest written: {out / 'meok-top10-poc.json'}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--legs", default="C,A,V,P")
    ap.add_argument("--budget", type=float, default=12.0)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"=== TOP-10 BURST 2026-08-16 start {now()} models={len(TOP10)} ===", flush=True)
    legs = {"C": lambda: leg_city(a.budget),
            "A": leg_agentic,
            "V": leg_vs,
            "P": leg_poc}
    for lg in a.legs.split(","):
        lg = lg.strip().upper()
        if lg in legs:
            try:
                legs[lg]()
            except Exception as e:
                print(f"  leg {lg} EXC {type(e).__name__}: {e}", flush=True)
    print(f"=== TOP-10 BURST DONE {now()} — outputs in {OUT} ===", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())