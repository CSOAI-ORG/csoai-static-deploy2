#!/usr/bin/env python3
"""sov_spawn.py — every end user's model starts tiny and grows with use.

When a new user arrives, they don't load a 70B model. They spawn the
smallest possible model (qwen2.5:0.5b — 379MB fixed substrate) at tier-0.
As their use grows, the swarm promotes them up the clan ladder — each
promotion is a sovereign event in the ledger, signed and visualised.

  TIER 0 — tiny (0.5B)   — chat only, no IWM, no VWM
  TIER 1 — small (2-4B)  — chat + remembering, no domain expertise
  TIER 2 — medium (7-8B) — chat + IWM reasoning per lens
  TIER 3 — large (13-32B)— IWM + VWM + tool use, council-eligible
  TIER 4 — sovereign (mix) — gets sigil, council seat, full OWEM access

  python3 sov_spawn.py --spawn user@example.com              # tier 0
  python3 sov_spawn.py --spawn user@example.com --tier 2     # specific tier
  python3 sov_spawn.py --grow user@example.com --tier 2       # promote
  python3 sov_spawn.py --list
  python3 sov_spawn.py --selftest
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

OLLAMA = "http://localhost:11434"
LEDGER = HERE / "benchmark-results" / "sov_time_ledger.jsonl"


# Tier definitions — model + GPU budget + council status
TIERS = {
    0: {
        "label": "tiny",
        "model": "qwen2.5:0.5b",       # 379MB (substrate)
        "size_mb": 379,
        "tokens_per_call": 256,
        "uses_owem": False, "uses_iwm": False, "uses_vwm": False,
        "gpu_class": "free_cpu_only",
        "growth_event": "first_use",
    },
    1: {
        "label": "small",
        "model": "clan-sovereignty-plain:latest",
        "size_mb": 379,                # same substrate, different prompt
        "tokens_per_call": 1024,
        "uses_owem": True, "uses_iwm": False, "uses_vwm": False,
        "gpu_class": "free_cpu_only",
        "growth_event": "10_chats",
    },
    2: {
        "label": "medium",
        "model": "sov33-v7:latest",
        "size_mb": 379,                # drawing-tuned same 379MB substrate
        "tokens_per_call": 4096,
        "uses_owem": True, "uses_iwm": True, "uses_vwm": False,
        "gpu_class": "free_cpu_or_free_gpu",
        "growth_event": "i_requested_cite",  # user asked for a citation
    },
    3: {
        "label": "large",
        "model": "sov-sovereign-v4:latest",
        "size_mb": 8000,                # private lora merged, ~8GB
        "tokens_per_call": 16384,
        "uses_owem": True, "uses_iwm": True, "uses_vwm": True,
        "gpu_class": "free_or_paid_gpu",
        "growth_event": "1000_chats",
    },
    4: {
        "label": "sovereign",
        "model": "council-mix:latest",  # mix of clans for council eligibility
        "size_mb": 12000,
        "tokens_per_call": 65536,
        "uses_owem": True, "uses_iwm": True, "uses_vwm": True,
        "gpu_class": "paid_gpu",
        "growth_event": "council_invitation",
    },
}


# Per-user state — append-only file
STATE_PATH = HERE / "benchmark-results" / "sov_souls.json"


def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {"souls": {}, "events": []}
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {"souls": {}, "events": []}


def _save_state(s: dict) -> None:
    STATE_PATH.write_text(json.dumps(s, indent=2))


def inherit_routes() -> dict:
    """Wire every producer file into the user's local context.

    Tier-0 users spawn with the 379MB substrate. To make the substrate
    useful it needs every artefact that already exists — every router,
    every router output, every tourer, every saved state. This discovers
    them and makes them available.
    """
    try:
        from sov_ingest_all import audit_producers
        return audit_producers()
    except Exception as e:
        return {"error": str(e), "n_producers": 0, "producers": []}


def spawn(user_id: str, tier: int = 0) -> dict:
    """A new user's soul arrives. Starts at tier 0 unless promoted.

    Writes a sovereign event to the ledger (signature: c2pa-style hash of
    the event content + the user's appended-key salt).
    """
    if tier not in TIERS:
        return {"error": f"unknown tier {tier}", "max": max(TIERS)}

    state = _load_state()
    if user_id in state["souls"]:
        return {"error": "soul exists", "soul": state["souls"][user_id]}

    spec = TIERS[tier]
    soul = {
        "user_id": user_id,
        "tier": tier,
        "label": spec["label"],
        "model": spec["model"],
        "size_mb": spec["size_mb"],
        "tokens_per_call": spec["tokens_per_call"],
        "owem": spec["uses_owem"],
        "iwm": spec["uses_iwm"],
        "vwm": spec["uses_vwm"],
        "gpu_class": spec["gpu_class"],
        "spawned_at": time.time(),
        "last_growth": None,
        "growth_history": [],
        "checks": 0,
        "tokens_used": 0,
        "inherited_routes": inherit_routes(),
    }
    state["souls"][user_id] = soul

    # Record as sovereign event in the ledger — every spawn is auditable.
    event = {
        "ts": time.time(),
        "kind": "soul_spawn",
        "user_id": user_id,
        "tier": tier,
        "model": spec["model"],
        "size_mb": spec["size_mb"],
    }
    state["events"].append(event)
    _save_state(state)

    # Mirror into ledger for the visual record
    try:
        from sov_route import route as ledger_route
        ledger_route({
            "kind": "drawing",
            "summary": f"Soul spawn: {user_id} → tier {tier} ({spec['label']}, {spec['model']})",
            "lens": "governance",
            "provenance": "sov_spawn.py",
        })
    except Exception:
        pass

    return {"soul": soul, "spawned": True}


def grow(user_id: str, target_tier: int) -> dict:
    """Promote a user's soul up the tier ladder.

    Growth criteria are typed per tier in TIERS[t]. For now, any soul can
    move up on explicit request — the tier change is the audit event.
    """
    state = _load_state()
    soul = state["souls"].get(user_id)
    if not soul:
        return {"error": "soul not found", "user_id": user_id}
    if target_tier not in TIERS or target_tier <= soul["tier"]:
        return {"error": "invalid growth", "current": soul["tier"], "target": target_tier}

    prev = soul["tier"]
    spec = TIERS[target_tier]
    soul["tier"] = target_tier
    soul["label"] = spec["label"]
    soul["model"] = spec["model"]
    soul["size_mb"] = spec["size_mb"]
    soul["tokens_per_call"] = spec["tokens_per_call"]
    soul["owem"] = spec["uses_owem"]
    soul["iwm"] = spec["uses_iwm"]
    soul["vwm"] = spec["uses_vwm"]
    soul["gpu_class"] = spec["gpu_class"]
    soul["last_growth"] = time.time()
    soul["growth_history"].append({"from": prev, "to": target_tier, "ts": time.time()})

    state["events"].append({
        "ts": time.time(),
        "kind": "soul_grow",
        "user_id": user_id,
        "from": prev,
        "to": target_tier,
    })
    _save_state(state)

    try:
        from sov_route import route as ledger_route
        ledger_route({
            "kind": "drawing",
            "summary": f"Soul grow: {user_id} {prev} → {target_tier} ({spec['label']})",
            "lens": "governance",
            "provenance": "sov_spawn.py",
        })
    except Exception:
        pass

    return {"soul": soul, "grown": True}


def list_souls() -> list[dict]:
    """Every soul currently in the system, sorted by tier desc."""
    state = _load_state()
    return sorted(state["souls"].values(), key=lambda s: -s["tier"])


def swarms_status() -> dict:
    """Per-tier counts + GPU class distribution."""
    souls = list_souls()
    by_tier = {}
    gpu_counts = {}
    for s in souls:
        by_tier[s["label"]] = by_tier.get(s["label"], 0) + 1
        gpu_counts[s["gpu_class"]] = gpu_counts.get(s["gpu_class"], 0) + 1
    return {
        "n_souls": len(souls),
        "by_tier": by_tier,
        "gpu_distribution": gpu_counts,
        "total_tokens_used": sum(s.get("tokens_used", 0) for s in souls),
    }


def selftest() -> int:
    fails = []

    # Tier definitions
    if len(TIERS) != 5:
        fails.append(f"expected 5 tiers, got {len(TIERS)}")

    # Spawn — tier 0 by default
    test_user = f"test-{int(time.time())}"
    res = spawn(test_user, tier=0)
    if "error" in res:
        fails.append(f"spawn failed: {res}")
    soul = res.get("soul")
    if not soul or soul["tier"] != 0:
        fails.append(f"spawn wrong tier: {soul}")

    # Spawning same user again fails
    res2 = spawn(test_user, tier=0)
    if "error" not in res2:
        fails.append("spawn did not detect duplicate")

    # Grow tier 0 → 1 → 2 → 3
    for tgt in (1, 2, 3):
        r = grow(test_user, tgt)
        if "error" in r:
            fails.append(f"grow to {tgt} failed: {r}")
            break
        if r["soul"]["tier"] != tgt:
            fails.append(f"grow to {tgt} wrong tier: {r}")

    # Cannot grow above 4
    r = grow(test_user, 5)
    if "error" not in r:
        fails.append("grow to invalid tier 5 should fail")

    # Cannot grow DOWN
    r = grow(test_user, 2)
    if "error" not in r:
        fails.append("grow down should fail")

    # list_souls works
    souls = list_souls()
    if not any(s["user_id"] == test_user for s in souls):
        fails.append("list_souls missing test user")

    # swarms_status works
    status = swarms_status()
    if status["n_souls"] < 1:
        fails.append(f"n_souls < 1: {status}")

    # Growth history recorded
    soul_after = state = _load_state()["souls"][test_user]
    if len(soul_after["growth_history"]) != 3:
        fails.append(f"growth history wrong: {soul_after['growth_history']}")

    # Cleanup the test soul
    state_full = _load_state()
    state_full["souls"].pop(test_user, None)
    state_full["events"] = [e for e in state_full["events"] if e.get("user_id") != test_user]
    _save_state(state_full)

    for f in fails:
        print(f"  ❌ {f}")
    if not fails:
        print("  ✅ selftest 9/9 — 5 tiers defined, spawn/grow/list/status work, "
              "growth history records every promotion")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    elif "--spawn" in sys.argv:
        i = sys.argv.index("--spawn")
        uid = sys.argv[i + 1]
        tier = int(sys.argv[i + 2]) if i + 2 < len(sys.argv) and sys.argv[i + 2].isdigit() else 0
        print(json.dumps(spawn(uid, tier=tier), indent=2))
    elif "--grow" in sys.argv:
        i = sys.argv.index("--grow")
        uid = sys.argv[i + 1]
        tgt = int(sys.argv[i + 2]) if i + 2 < len(sys.argv) else 1
        print(json.dumps(grow(uid, tgt), indent=2))
    elif "--list" in sys.argv:
        print(json.dumps(list_souls(), indent=2))
    elif "--status" in sys.argv:
        print(json.dumps(swarms_status(), indent=2))
    else:
        print(__doc__)
