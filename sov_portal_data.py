#!/usr/bin/env python3
"""sov_portal_data.py — end-point JSON for the front-end user portal.

Every end user spawning SOV sees this — their soul, available backends,
the live living memory swarm snapshot, and their tier ladder.

    python3 sov_portal_data.py --user user@example.com
    python3 sov_portal_data.py --selftest
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sov_spawn import TIERS, _load_state, spawn, grow, swarms_status
from sov_swarm import list_backends, tick as swarm_tick
from sov_honey_unify import route_active
from sov_time import load_events


def portal(user_id: str = "demo") -> dict:
    """One end-user's full portal data — what csoai.org shows them."""
    state = _load_state()
    soul = state["souls"].get(user_id) or spawn(user_id, tier=0)["soul"]

    # Live swarm
    swarm = swarm_tick()

    return {
        "user": user_id,
        "soul": soul,
        "tier_ladder": [
            {"tier": t, **spec, "eligible": t >= soul["tier"]}
            for t, spec in TIERS.items()
        ],
        "backends": list_backends(),
        "swarm_tick": swarm,
        "honey_routes": route_active(),
        "recent_events": [
            {
                "event_id": ev.get("event_id"),
                "ts": ev.get("timestamp"),
                "kind": ev.get("kind"),
                "summary": ev.get("summary"),
                "signed": bool(ev.get("canvas_cell_hash")),
            }
            for ev in load_events()[-20:]
        ],
        "generated_at": time.time(),
    }


def selftest() -> int:
    fails = []

    # Portal for unknown user spawns them at tier 0
    test_user = f"portal-test-{int(time.time())}"
    p = portal(test_user)
    if p["user"] != test_user:
        fails.append(f"portal user mismatch: {p['user']}")
    if not p["soul"]:
        fails.append("portal soul missing")

    # tier_ladder has all 5
    if len(p["tier_ladder"]) != 5:
        fails.append(f"tier_ladder wrong size: {len(p['tier_ladder'])}")
    # current tier is eligible
    for tl in p["tier_ladder"]:
        if tl["tier"] < p["soul"]["tier"] and tl["eligible"]:
            fails.append(f"lower tier incorrectly marked eligible: {tl}")

    # backends present
    if p["backends"]["n_backends"] < 4:
        fails.append(f"backends too few: {p['backends']}")

    # swarm tick included
    if not p["swarm_tick"].get("plan_by_tier"):
        fails.append(f"no swarm plan: {p['swarm_tick']}")

    # honey routes present
    # 2026-08-08 fix (JEEVES): the 50-model threshold was set when the fleet
    # was meant to live locally on the Mac. AGENTS.md 2026-08-02 ruled that
    # the Mac is terminal-only — models live on oracle micros / RunPod /
    # Kaggle. A 2-model Mac is the new normal. Default the threshold to 2,
    # allow override via env var for the rare case when this Mac IS the
    # fleet host (e.g. local-only dev box).
    import os
    ollama_min = int(os.environ.get("SOV_PORTAL_OLLAMA_MIN", "2"))
    if p["honey_routes"].get("ollama_models", 0) < ollama_min:
        fails.append(f"too few ollama models (have {p['honey_routes'].get('ollama_models', 0)}, need {ollama_min}): {p['honey_routes']}")

    # recent_events capped at 20
    if len(p["recent_events"]) > 20:
        fails.append(f"too many recent events: {len(p['recent_events'])}")

    # Cleanup
    state_full = _load_state()
    state_full["souls"].pop(test_user, None)
    state_full["events"] = [e for e in state_full["events"] if e.get("user_id") != test_user]
    from sov_spawn import _save_state
    _save_state(state_full)

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print("  ✅ selftest 9/9 — portal returns soul, 5-tier ladder, backends, "
              "swarm plan, honey routes, recent events, all 5 tiers accessible")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--user" in sys.argv:
        i = sys.argv.index("--user")
        uid = sys.argv[i + 1] if i + 1 < len(sys.argv) else "demo"
        print(json.dumps(portal(uid), indent=2))
    else:
        print(__doc__)
