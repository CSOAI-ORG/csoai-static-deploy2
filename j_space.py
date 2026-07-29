#!/usr/bin/env python3
"""j_space.py — the observability layer: every OWEM decision becomes a hash-chained signed event.

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS IS FOR
═══════════════════════════════════════════════════════════════════════════════
"No more black box" is a claim about EVIDENCE, not about UI. A dashboard that renders whatever
it is handed proves nothing — if an event can be deleted or edited after the fact, the view is
decoration. So J-space is a **hash-chained, signed append-only log** first, and a view second.

Each event links to the one before it:

    event_n.prev = sha256(event_{n-1})

Remove or alter any event and every subsequent hash breaks. That is what makes the SOV master's
"realtime view of all OWEM parts" an auditable claim rather than a screenshot.

Format matches the chains already in the estate (`~/.sov33_composition.chain.jsonl` etc):
    {ts, task, decision, reason, emitted, prev, sig, hash}

═══════════════════════════════════════════════════════════════════════════════
⚠️ TRANSPORT vs SUBSTRATE — do not conflate these
═══════════════════════════════════════════════════════════════════════════════
Both MCP endpoints were probed on 2026-07-28 and are DOWN:
    sov3 local :3101                        HTTP 000
    sovereign.templeman-opticians.com       HTTP 000

MCP is the TRANSPORT that would carry these events between hosts. It is not the substrate.
The events are produced and chained locally regardless — so J-space works today, and MCP
federation is an upgrade to distribution, not a prerequisite for observability.

Claiming "realtime across all OWEM parts via MCP" while those endpoints are down would be
exactly the kind of unverified claim this estate keeps having to retract. Local first,
federated when the transport is actually up.

    python3 j_space.py --watch            # live tail
    python3 j_space.py --verify           # prove the chain is unbroken
    python3 j_space.py --summary          # what has the cluster been doing
"""
from __future__ import annotations

import argparse, hashlib, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CHAIN = Path(os.path.expanduser("~/.sov_jspace.chain.jsonl"))


def _canon(d: dict) -> bytes:
    return json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _last_hash() -> str:
    if not CHAIN.exists():
        return "0" * 64
    last = None
    with CHAIN.open() as f:
        for line in f:
            if line.strip():
                last = line
    if not last:
        return "0" * 64
    try:
        return json.loads(last).get("hash", "0" * 64)
    except Exception:
        return "0" * 64


def emit(task: str, decision: str, reason: str = "", **extra) -> dict:
    """Append one signed, chained event. Fails OPEN on signing, never on chaining —
    an unsigned event is still hash-linked, so a gap is always detectable."""
    ev = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "decision": decision,
        "reason": reason,
        "emitted": "j_space",
        "prev": _last_hash(),
        **extra,
    }
    seed = os.environ.get("SIGIL_SEED")
    if seed:
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
            k = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(seed.encode()).digest())
            ev["sig"] = k.sign(_canon(ev)).hex()
        except Exception as e:
            ev["sig"] = None
            ev["sig_note"] = str(e)[:80]
    else:
        ev["sig"] = None
        ev["sig_note"] = "SIGIL_SEED not set — chained but unsigned"
    ev["hash"] = hashlib.sha256(_canon({k: v for k, v in ev.items() if k != "hash"})).hexdigest()
    with CHAIN.open("a") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    return ev


def route_and_log(query: str) -> dict:
    """Run the full sandwich and record every layer's decision. This is the point of J-space:
    the ROUTING is what needs to be observable, not just the answer."""
    from owem_cluster import classify_dimension, build_expert_table
    from care_gate_v2 import tier1_hard_stop

    breach, label, cite = tier1_hard_stop(query)
    qh = hashlib.sha256(query.encode()).hexdigest()[:16]
    if breach:
        emit("gate", "BLOCKED", label, query_id=qh, citation=cite, layer="OWM-perception")
        return {"blocked": True, "reason": label}

    dim = classify_dimension(query)
    emit("classify", dim, "SOV1 spine", query_id=qh, layer="OWM-perception")

    table, models = build_expert_table()
    if dim not in table:
        emit("route", "NO_EXPERT", f"no frozen expert holds {dim}", query_id=qh)
        return {"error": f"no expert for {dim}"}
    sel = table[dim]
    emit("route", sel["expert"], f"wins {dim} at {sel['score']:.1f}%",
         query_id=qh, dimension=dim, dim_score=sel["score"],
         layer="IWM-reasoning", frozen_experts=len(models))
    return {"blocked": False, "dimension": dim, "expert": sel["expert"], "query_id": qh}


def verify() -> int:
    """Walk the chain. A single altered or removed event breaks every hash after it."""
    if not CHAIN.exists():
        print("  no chain yet"); return 0
    prev = "0" * 64
    n = broken = unsigned = 0
    with CHAIN.open() as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            n += 1
            ev = json.loads(line)
            if ev.get("prev") != prev:
                print(f"  ❌ line {i}: prev mismatch — chain broken here")
                broken += 1
            recomputed = hashlib.sha256(_canon({k: v for k, v in ev.items() if k != "hash"})).hexdigest()
            if recomputed != ev.get("hash"):
                print(f"  ❌ line {i}: hash mismatch — event was ALTERED after writing")
                broken += 1
            if not ev.get("sig"):
                unsigned += 1
            prev = ev.get("hash", prev)
    print(f"  events   : {n}")
    print(f"  unsigned : {unsigned}" + ("   (set SIGIL_SEED to sign)" if unsigned else ""))
    print(f"  {'✅ CHAIN INTACT — no event removed or altered' if not broken else f'❌ {broken} BREAKS'}")
    return 1 if broken else 0


def summary() -> None:
    if not CHAIN.exists():
        print("  no events yet — run a query through route_and_log"); return
    from collections import Counter
    tasks, decisions, dims = Counter(), Counter(), Counter()
    n = 0
    with CHAIN.open() as f:
        for line in f:
            if not line.strip():
                continue
            ev = json.loads(line); n += 1
            tasks[ev.get("task")] += 1
            if ev.get("task") == "route":
                decisions[ev.get("decision")] += 1
            if ev.get("dimension"):
                dims[ev["dimension"]] += 1
    print(f"  J-SPACE — {n} chained events\n")
    print("  by task:");      [print(f"    {k:12s} {v}") for k, v in tasks.most_common()]
    if dims:
        print("  dimensions seen:"); [print(f"    {k:15s} {v}") for k, v in dims.most_common(8)]
    if decisions:
        print("  experts used:");    [print(f"    {k:26s} {v}") for k, v in decisions.most_common(8)]


def watch() -> None:
    print(f"  tailing {CHAIN} — Ctrl-C to stop")
    CHAIN.touch()
    with CHAIN.open() as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.4); continue
            try:
                ev = json.loads(line)
                sig = "🔏" if ev.get("sig") else "  "
                print(f"  {sig} {ev['ts'][11:19]}  {ev['task']:9s} {str(ev['decision'])[:34]:34s} {ev.get('reason','')[:36]}")
            except Exception:
                pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--route")
    a = ap.parse_args()
    if a.verify:   sys.exit(verify())
    elif a.watch:  watch()
    elif a.route:  print(json.dumps(route_and_log(a.route), indent=2))
    else:          summary()
