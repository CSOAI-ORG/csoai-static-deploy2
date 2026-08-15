#!/usr/bin/env python3
"""keystone_runner.py — JSON-in / JSON-out wrapper around the two keystone modules the
Fastify flywheel runner can't import directly.

Why this script exists:
  The flywheel-runner at /Users/nicholas/projects/coai-dashboard/flywheel/src/server.ts shells
  out to Python. To also surface equivalence + survival_matrix, we need ONE Python entry point
  that the wrapper can call with `--action <name>`. This script imports both modules, dispatches
  on `action`, prints a single JSON object, exits 0 on success or 2 on guard failure.

Endpoints (driven by the Fastify wrapper):
  --action survival_run --cells '<json>' [--version VER]
      cells: {asset_id, binding} list. Runs run_matrix + survival_ci.
  --action ec_measure  --ec '<json>' --behaviour '<json>'
      Applies a (signed) EC against a measured behaviour_result. Reports divergence.
  --action guards
      Runs both structural guards. No inputs.
  --action decision_ledger --dl-action <sub> [options]
      Sub-actions: selftest, list, show, current, history, contested, by_tag, stale_leads, append.
      --record '<json>' for append; --record-id for show/current/history; --tag for by_tag; --days for stale_leads.

JSON output schema (always):
  { "action": <str>, "ok": <bool>, "result": <dict|object>, "signed": {alg:digest}, "elapsed_ms": <int> }

Laws welded in:
  - The equivalence engine has NO create/modify/adjudicate/resolve path. We assert that with
    engine_guard() on every invocation that touches an EC.
  - survival_matrix.py is run only after selftest() passes.
  - We never write anything to disk from this runner — output is stdout only. Disk writes go to
    anchored_write.py upstream.

Usage:
    python3 keystone_runner.py --action guards
    python3 keystone_runner.py --action survival_run --cells '[{"asset_id":"X","binding":"hard_hash"}]'
    python3 keystone_runner.py --action ec_measure --ec '{"ec_id":"...", ...}' --behaviour '{"EU":{"predicate_pass":true}, ...}'
    python3 keystone_runner.py --action decision_ledger --dl-action selftest
    python3 keystone_runner.py --action decision_ledger --dl-action list
    python3 keystone_runner.py --action decision_ledger --dl-action show --record-id DR-0001
    python3 keystone_runner.py --action decision_ledger --dl-action append --record '{"record_id":"DR-0005", ...}'
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from equivalence import engine_guard as eq_guard, EquivalenceClass, measure_divergence  # noqa: E402
from survival_matrix import selftest as sm_selftest, run_matrix, survival_ci  # noqa: E402
from decision_ledger import (
    DecisionLedger, DecisionLedgerError, selftest as dl_selftest, build_seed_ledger,
    KINDS, VERDICTS, TAGS,
)  # noqa: E402


def _err(payload: dict, code: int = 1) -> int:
    payload["ok"] = False
    print(json.dumps(payload, default=str))
    return code


def _sign(payload: dict) -> dict:
    """sha256 over the canonical payload, sort_keys=True."""
    body = json.dumps(payload, sort_keys=True).encode()
    return {"alg": "sha256", "digest": hashlib.sha256(body).hexdigest()}


def _ok(action: str, result: dict, t0: float) -> int:
    payload = {"action": action, "result": result, "elapsed_ms": int((time.time() - t0) * 1000)}
    payload["signed"] = _sign(payload)
    payload["ok"] = True
    print(json.dumps(payload, default=str, sort_keys=True))
    return 0


def action_guards() -> int:
    t0 = time.time()
    eq_ok, eq_msg = eq_guard()
    sm_ok, sm_msg = sm_selftest()
    result = {
        "equivalence_engine_guard": {"ok": eq_ok, "msg": eq_msg},
        "survival_matrix_selftest": {"ok": sm_ok, "msg": sm_msg},
        "law": "no LLM-as-judge; no adjudicate/resolve; signed-only; models-as-subjects",
    }
    if not (eq_ok and sm_ok):
        return _err({"action": "guards", "result": result,
                     "err": "structural guard refused the request"}, code=2)
    return _ok("guards", result, t0)


def action_survival_run(cells_json: str) -> int:
    t0 = time.time()
    sm_ok, sm_msg = sm_selftest()
    if not sm_ok:
        return _err({"action": "survival_run", "err": f"survival_matrix selftest refused: {sm_msg}"}, code=2)
    try:
        cells = json.loads(cells_json)
    except json.JSONDecodeError as e:
        return _err({"action": "survival_run", "err": f"invalid JSON in --cells: {e}"}, code=1)
    if not isinstance(cells, list) or not all(isinstance(c, dict) and "asset_id" in c and "binding" in c for c in cells):
        return _err({"action": "survival_run", "err": "cells must be a list of {asset_id, binding} dicts"}, code=1)
    res = run_matrix(cells)
    ci = survival_ci(res["n_survive"], res["n_total"])
    return _ok("survival_run",
               {"n_cells": len(cells), "run": res, "ci": ci,
                "scoreboard_role": "structural diagnostic; not in leader composite"}, t0)


def action_ec_measure(ec_json: str, behaviour_json: str) -> int:
    t0 = time.time()
    eq_ok, eq_msg = eq_guard()
    if not eq_ok:
        return _err({"action": "ec_measure", "err": f"equivalence engine guard refused: {eq_msg}"}, code=2)
    try:
        ec_d = json.loads(ec_json)
        behaviour = json.loads(behaviour_json)
    except json.JSONDecodeError as e:
        return _err({"action": "ec_measure", "err": f"invalid JSON: {e}"}, code=1)
    if not isinstance(ec_d, dict) or "members" not in ec_d:
        return _err({"action": "ec_measure", "err": "ec must be a dict with `members` list"}, code=1)
    try:
        ec = EquivalenceClass(ec_d)
    except KeyError as e:
        return _err({"action": "ec_measure", "err": f"EC schema invalid, missing required field: {e}"}, code=1)
    div = measure_divergence(ec, behaviour)
    # Strip fields the caller doesn't need from the rows to keep the response small.
    out = {
        "ec_id": div["ec_id"],
        "obligation_type": div["obligation_type"],
        "axis": div["axis"],
        "predicate": div["predicate"],
        "members": div["members"],
        "diverges": div["diverges"],
        "pass_in": div["pass_in"],
        "fail_in": div["fail_in"],
        "framing": div["framing"],
        "scoreboard_role": "structural diagnostic; not in leader composite",
    }
    return _ok("ec_measure", out, t0)


def action_decision_ledger(dl_action: str, record_json: str | None, record_id: str | None,
                           tag: str | None, days: int) -> int:
    t0 = time.time()
    dl_ok = dl_selftest()
    if dl_ok != 0:
        return _err({"action": "decision_ledger", "err": "decision_ledger selftest failed"}, code=2)

    led = build_seed_ledger()

    if dl_action == "selftest":
        guard_msg = led.guard()
        return _ok("decision_ledger", {"sub": "selftest", "guard": guard_msg,
                                       "n_records": len(led.export()),
                                       "n_contested": len(led.contested())}, t0)

    if dl_action == "list":
        return _ok("decision_ledger", {"sub": "list", "records": led.export()}, t0)

    if dl_action == "show":
        if not record_id:
            return _err({"action": "decision_ledger", "err": "--record-id is required for show"}, code=1)
        rec = led.get(record_id)
        if rec is None:
            return _err({"action": "decision_ledger", "err": f"{record_id} not found"}, code=1)
        return _ok("decision_ledger", {"sub": "show", "record": rec}, t0)

    if dl_action == "current":
        if not record_id:
            return _err({"action": "decision_ledger", "err": "--record-id is required for current"}, code=1)
        # Accept either a record_id (DR-NNNN) or a raw claim string.
        lookup = led.get(record_id)
        claim = lookup["claim"] if lookup else record_id
        rec = led.current(claim)
        if rec is None:
            return _err({"action": "decision_ledger", "err": f"no current record for claim {claim!r}"}, code=1)
        return _ok("decision_ledger", {"sub": "current", "record": rec}, t0)

    if dl_action == "history":
        if not record_id:
            return _err({"action": "decision_ledger", "err": "--record-id is required for history"}, code=1)
        # Accept either a record_id (DR-NNNN) or a raw claim string.
        lookup = led.get(record_id)
        claim = lookup["claim"] if lookup else record_id
        return _ok("decision_ledger", {"sub": "history", "records": led.history(claim)}, t0)

    if dl_action == "contested":
        pairs = led.contested()
        return _ok("decision_ledger", {"sub": "contested", "pairs": pairs, "n_pairs": len(pairs)}, t0)

    if dl_action == "by_tag":
        if not tag:
            return _err({"action": "decision_ledger", "err": "--tag is required for by_tag"}, code=1)
        if tag not in TAGS:
            return _err({"action": "decision_ledger", "err": f"unknown tag {tag!r}; valid: {TAGS}"}, code=1)
        return _ok("decision_ledger", {"sub": "by_tag", "tag": tag, "records": led.by_tag(tag)}, t0)

    if dl_action == "stale_leads":
        return _ok("decision_ledger", {"sub": "stale_leads", "days": days,
                                        "records": led.stale_leads(days)}, t0)

    if dl_action == "append":
        if not record_json:
            return _err({"action": "decision_ledger", "err": "--record JSON is required for append"}, code=1)
        try:
            record = json.loads(record_json)
        except json.JSONDecodeError as e:
            return _err({"action": "decision_ledger", "err": f"invalid JSON in --record: {e}"}, code=1)
        try:
            led.append(record)
        except DecisionLedgerError as e:
            return _err({"action": "decision_ledger", "err": str(e)}, code=2)
        return _ok("decision_ledger", {"sub": "append", "record": record,
                                        "n_records": len(led.export())}, t0)

    return _err({"action": "decision_ledger", "err": f"unknown dl-action {dl_action!r}"}, code=1)


def main():
    p = argparse.ArgumentParser(description="keystone_runner — Fastify-callable wrapper for equivalence + survival_matrix + decision_ledger.")
    p.add_argument("--action", required=True, choices=["guards", "survival_run", "ec_measure", "decision_ledger"])
    p.add_argument("--cells",   help='JSON list of {asset_id, binding} cells (survival_run).')
    p.add_argument("--ec",      help='JSON encoded EquivalenceClass (ec_measure).')
    p.add_argument("--behaviour", help='JSON encoded behaviour_result (ec_measure).')
    p.add_argument("--dl-action", choices=["selftest", "list", "show", "current", "history",
                                            "contested", "by_tag", "stale_leads", "append"],
                   help='Sub-action for decision_ledger.')
    p.add_argument("--record",    help='JSON encoded decision record (decision_ledger append).')
    p.add_argument("--record-id", help='Record ID or claim string (decision_ledger show/current/history).')
    p.add_argument("--tag",       help='Tag filter (decision_ledger by_tag).')
    p.add_argument("--days", type=int, default=30, help='Stale-lead threshold in days (default 30).')
    args = p.parse_args()

    if args.action == "guards":
        sys.exit(action_guards())
    if args.action == "survival_run":
        if not args.cells:
            sys.exit(_err({"action": "survival_run", "err": "--cells is required"}, code=1))
        sys.exit(action_survival_run(args.cells))
    if args.action == "ec_measure":
        if not args.ec or not args.behaviour:
            sys.exit(_err({"action": "ec_measure", "err": "--ec and --behaviour are required"}, code=1))
        sys.exit(action_ec_measure(args.ec, args.behaviour))
    if args.action == "decision_ledger":
        if not args.dl_action:
            sys.exit(_err({"action": "decision_ledger", "err": "--dl-action is required"}, code=1))
        sys.exit(action_decision_ledger(args.dl_action, args.record, args.record_id,
                                        args.tag, args.days))


if __name__ == "__main__":
    main()
