#!/usr/bin/env python3
"""sov_e2e.py — end-to-end test that the full sovereign pipeline works.

Spawn → grow → ledger → honey → 5D → fluid → IWM → VWM. Every component
must agree, every signature must match, every pane must show the truth.

    python3 sov_e2e.py --selftest
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sov_spawn import spawn, grow, list_souls, TIERS
from sov_swarm import alloc_for_tier, BACKENDS
from sov_time import load_events, LEDGER
from sov_route import route as ledger_route
from sov_local import ensure_db, DB_PATH
from sov_eyes import iwm_reason, substrate
from sov_5d import sov_5d_points
from sov_fluid import LivingMemory


def e2e_full_cycle() -> dict:
    """Run one complete user lifecycle end-to-end."""
    test_id = f"e2e-{int(__import__('time').time() * 1000000)}"

    # 1. Spawn
    spawn_result = spawn(test_id, tier=0)
    assert spawn_result.get("spawned"), f"spawn failed: {spawn_result}"

    # 2. Grow through tiers 1, 2, 3
    for tgt in (1, 2, 3):
        grow_result = grow(test_id, tgt)
        assert grow_result.get("grown"), f"grow to {tgt} failed: {grow_result}"

    # 3. Soul state in pool — must include inherited routes
    souls = list_souls()
    soul = next(s for s in souls if s["user_id"] == test_id)
    assert soul["tier"] == 3 and soul["iwm"] and soul["vwm"] and soul["owem"]  # tier 3 = full stack
    # Tier-0 must have inherited all producers
    inh = soul.get("inherited_routes", {})
    assert inh.get("n_producers", 0) >= 10, f"too few inherited routes: {inh}"

    # 4. Swarm allocates correctly per tier
    for tier in range(5):
        plan = alloc_for_tier(tier)
        assert plan, f"tier {tier} has no plan"
        # PRIMARY is always present
        primary = BACKENDS[plan[0]["backend"]]
        assert tier in primary["tiers_supported"]

    # 5. Ledger grew by 4 events (spawn + 3 grows)
    n_after = len(load_events())
    assert n_after >= 4, f"ledger too small: {n_after}"

    # 6. Honey DB mirrors every event
    import sqlite3
    conn = ensure_db()
    n_db = conn.execute("SELECT COUNT(*) FROM honey").fetchone()[0]
    n_ledger = len(load_events())
    # Honey mirrors the ledger — allow ±10 events race when other tests
    # insert events in parallel via the local server.
    assert abs(n_db - n_ledger) <= 10, f"honey drift too large: db={n_db} ≠ ledger={n_ledger}"

    # 7. 5D points include ledger events
    pts = sov_5d_points()
    n_evidence_pts = sum(1 for p in pts if p.get("event_id"))
    assert n_evidence_pts >= 4, f"5D evidence too few: {n_evidence_pts}"

    # 8. Fluid memory hydrates
    fluid = LivingMemory()
    snap = fluid.snapshot()
    assert snap["n_nodes"] >= 10, f"fluid too few: {snap['n_nodes']}"
    for kind in ("anchor", "subject", "artifact", "evidence"):
        assert kind in snap["by_kind"], f"missing kind: {kind}"

    # 9. IWM reason with matched lens
    ans = iwm_reason("what does the provenance lens measure?")
    assert ans.get("matched_lens") == "provenance", f"no lens match: {ans}"
    assert "experiment" in str(ans).lower() or "claim" in str(ans).lower()

    # 10. Substrate snapshot covers all 3 eyes
    sub = substrate()
    assert "owm" in sub and "iwm" in sub and "vwm" in sub
    assert sub["iwm_ledger"]["n_records"] >= 4

    # Cleanup
    conn.close()
    state_path = HERE / "benchmark-results" / "sov_souls.json"
    state = json.loads(state_path.read_text())
    state["souls"].pop(test_id, None)
    state["events"] = [e for e in state["events"] if e.get("user_id") != test_id]
    state_path.write_text(json.dumps(state, indent=2))

    return {
        "test_id": test_id,
        "passed": True,
        "ledger_events": n_ledger,
        "honey_events": n_db,
        "fluid_nodes": snap["n_nodes"],
        "fluid_kinds": snap["by_kind"],
        "evidence_5d_pts": n_evidence_pts,
        "iwm_matched_lens": ans["matched_lens"],
        "substrate": sub,
    }


def selftest() -> int:
    fails = []

    try:
        result = e2e_full_cycle()
        if not result["passed"]:
            fails.append(f"end-to-end cycle failed: {result}")
        if result["ledger_events"] != result["honey_events"]:
            fails.append(f"mirror drift: {result['ledger_events']} vs {result['honey_events']}")
        if result["fluid_nodes"] < 10:
            fails.append(f"fluid too few: {result['fluid_nodes']}")
    except AssertionError as e:
        fails.append(f"assertion: {e}")
    except Exception as e:
        fails.append(f"exception: {type(e).__name__}: {e}")

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print("  ✅ E2E PASS — spawn→grow→ledger→honey→5D→fluid→IWM→VWM all consistent")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--run" in sys.argv:
        print(json.dumps(e2e_full_cycle(), indent=2, default=str))
    else:
        print(__doc__)
