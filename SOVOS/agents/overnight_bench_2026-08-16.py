#!/usr/bin/env python3
"""overnight_bench_2026-08-16.py — the FULL-STACK overnight benchmark.

EVERYTHING goes through the city sim (the user directive):
  LEG B  — 14-axis GSPC board (all 22 models, exact-label gate)
  LEG S  — CITY with --scenario-bank: 25 guarded Art-5(1) scenarios injected
           into RED citizens + frontier (grok) + local — the QUOTABLE city
  LEG J  — JAIL leg: sandbox-escape gold bank (30 ESCAPE + 30 BENIGN) vs
           OUR sov6 agents AND frontier agentic (grok-4.20-multi-agent)
  LEG F  — frontier city (5 frontier incl grok, 60 citizens, $8 cap)
  LEG P  — protocols: MCP/A2A/HTTP through the same ruler (if the bank has them)
  LEG H  — human-data hooks report (owner gate: £425 Prolific)

Runs on EITHER A100 (both have the repo). Times: each leg bounded.
"""

from __future__ import annotations
import argparse, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/workspace/jeeves-exec")
AG = REPO / "SOVOS/agents"
PY = "/workspace/venv-test/bin/python"
OUT = Path("/workspace/overnight-bench-2026-08-16")

FRONTIER = ["nvidia/nemotron-3.5-lightning", "qwen/qwen3.5-35b-a3b",
            "deepseek/deepseek-v4-pro", "x-ai/grok-4.6",
            "x-ai/grok-4.20-multi-agent"]
AGENTIC_BENCH = ["sov6-agency-v3-light:latest", "phi4:14b",
                 "x-ai/grok-4.20-multi-agent"]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(cmd, timeout=5400):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr)[-1500:]
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"


def leg_board() -> None:
    print(f"\n=== LEG B: 14-axis board (22 models) start {now()}", flush=True)
    rc, out = run([str(PY), str(AG / "board_v2.py"), "--all"])
    print(f"board rc={rc} {out[-300:]}", flush=True)


def leg_scenario(cap: float) -> None:
    print(f"\n=== LEG S: QUOTABLE CITY — scenario-bank (25 Art-5(1) guarded) + frontier + jail-adjacent — cap ${cap} {now()}", flush=True)
    rc, out = run([str(PY), str(AG / "cross_lab_city.py"),
                   "--frontier", ",".join(FRONTIER),
                   "--scenario-bank",
                   "--epochs", "2", "--citizens", "60",
                   "--budget", str(cap),
                   "--out", "SOVOS/cross-lab-runs/2026-08-16/scenario-city"])
    print(f"scenario-city rc={rc} {out[-500:]}", flush=True)


def leg_jail() -> None:
    print(f"\n=== LEG J: JAIL leg — sandbox-escape gold bank vs our sov6 agency + frontier {now()}", flush=True)
    out = OUT / "jail"
    out.mkdir(parents=True, exist_ok=True)
    for m in AGENTIC_BENCH:
        rc, r = run([str(PY), str(AG / "grok_escape_gold.py"),
                     "--model", m,
                     "--out", str(out / f"{m.split('/')[-1].replace(':','-')}-gold.json")],
                     timeout=2400)
        print(f"  {m} jail-gold rc={rc}", flush=True)


def leg_frontier(cap: float) -> None:
    print(f"\n=== LEG F: cross-platform city (5 frontier incl grok) cap ${cap} — {now()}", flush=True)
    rc, out = run([str(PY), str(AG / "cross_lab_city.py"),
                   "--frontier", ",".join(FRONTIER),
                   "--epochs", "2", "--citizens", "60",
                   "--budget", str(cap),
                   "--out", "SOVOS/cross-lab-runs/2026-08-16/frontier-city"], timeout=5400)
    print(f"frontier rc={rc} {out[-400:]}", flush=True)


def leg_protocols() -> None:
    print("\n=== LEG P: protocols (MCP/A2A/HTTP/OSCAL) through the ruler — {now()}", flush=True)
    rc, out = run([str(PY), str(AG / "run_protocol_e2e.py")], timeout=3000)
    print(f"protocols rc={rc} {out[-400:]}", flush=True)


def leg_human() -> None:
    print("\n=== LEG H: human-data hooks (owner gate = £425 Prolific)", flush=True)
    print("  human_solver_bridge.py: 10/10 stubbed (honest 0.80)")
    print("  Empirica/Apache-2.0 + oTree/MIT forkable; cost model £425/100-cell", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--legs", default="B,S,J,F,P,H",
                    help="comma list: B board, S scenario-city, J jail, F frontier, P protocols, H human")
    ap.add_argument("--budget", type=float, default=8.0)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"=== OVERNIGHT BENCH 2026-08-16 start {now()} :: ALL THROUGH THE CITY ===", flush=True)
    legs = {
        "B": lambda: leg_board(),
        "S": lambda: leg_scenario(a.budget),
        "J": lambda: leg_jail(),
        "F": lambda: leg_frontier(a.budget),
        "P": lambda: leg_protocols(),
        "H": lambda: leg_human(),
    }
    for lg in a.legs.split(","):
        lg = lg.strip().upper()
        if lg in legs:
            try:
                legs[lg]()
            except Exception as e:
                print(f"  leg {lg} EXC {type(e).__name__}: {e}", flush=True)
    print(f"=== OVERNIGHT BENCH DONE {now()} — outputs in {OUT} ===", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())