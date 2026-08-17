#!/usr/bin/env python3
"""grok_referee_keeper.py — durable infinite-loop wrapper for grok_referee.py.

Runs one referee round every REFRESH_S, catches per-round exceptions, writes
a heartbeat, and survives pod restarts via nohup. Degrades gracefully: when
no XAI_API_KEY is present the rounds log UNMEASURED and the loop keeps going
(so wiring the key later needs no restart).

Run:  nohup python3 grok_referee_keeper.py > grok_referee_keeper.log 2>&1 &
"""
from __future__ import annotations
import importlib.util, json, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path

REFEREE = Path("/workspace/sov33-oowm/oowm/grok_referee.py")
HEARTBEAT = Path("/workspace/arena-24x7/grok_referee_heartbeat.json")
REFRESH_S = 300  # one referee round every 5 min (24/7 = ~288 rounds/day)


def load_referee():
    spec = importlib.util.spec_from_file_location("grok_referee", REFEREE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load_referee()
    while True:
        try:
            mod.main()
        except Exception:
            traceback.print_exc()
        try:
            HEARTBEAT.write_text(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "loop": "grok_referee_keeper",
                "refresh_s": REFRESH_S,
            }))
        except Exception:
            pass
        time.sleep(REFRESH_S)


if __name__ == "__main__":
    main()
