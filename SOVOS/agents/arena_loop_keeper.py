#!/usr/bin/env python3
"""arena_loop_keeper.py — durable infinite-loop wrapper for the 3090 arena.

arena_24x7_reborn.py is single-round (designed for an hourly Mac keeper
that was never wired). This wrapper makes it self-contained and durable:
- runs reborn's main() in an infinite loop
- sleeps 90s between rounds
- catches exceptions per-round so one bad round never kills the loop
- writes heartbeat so we can verify liveness

Run:  nohup python3 arena_loop_keeper.py > keeper.log 2>&1 &
"""

from __future__ import annotations
import importlib.util, json, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path

ARENA = Path("/workspace/arena-24x7")
REBORN = ARENA / "arena_24x7_reborn.py"
HEARTBEAT = ARENA / "keeper_heartbeat.json"
SLEEP_S = 90


def load_reborn():
    spec = importlib.util.spec_from_file_location("arena_reborn", REBORN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def beat(state: str, detail: str = ""):
    HEARTBEAT.write_text(json.dumps({
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "state": state,
        "detail": detail,
    }))
    print(f"[{state}] {detail}", flush=True)


def main() -> int:
    mod = load_reborn()
    round_no = 0
    while True:
        try:
            round_no += 1
            beat("round", f"#{round_no} starting")
            mod.main()
            beat("round", f"#{round_no} done")
        except SystemExit as e:
            # main() calls sys.exit(0) when no models — log and keep waiting
            beat("idle", f"round #{round_no}: {e}")
        except Exception as e:
            beat("error", f"round #{round_no}: {type(e).__name__}: {e}")
            traceback.print_exc()
        time.sleep(SLEEP_S)


if __name__ == "__main__":
    sys.exit(main())