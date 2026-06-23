#!/usr/bin/env python3
"""
conductor.py — the Governed Conductor (GOVERNED_CONDUCTOR.md steps 1 + 3).

Our attested answer to Sakana Fugu. Honest scope: this is an orchestration LAYER over assets we
already own (council, Sovereign Gate, sim, risk models, the Ed25519 ledger) — NOT a trained
foundation model. Where we beat Fugu is governance / heterogeneity / no-lock-in, not raw reasoning.

What this file implements (additive — does not touch existing files):

  1. A `Conductor` that, given a task, assigns the TRINITY roles Thinker / Worker / Verifier over a
     SWAPPABLE, HETEROGENEOUS pool. Pool members are callables tagged with a `kind`:
       'llm'         — language / reasoning  (stub: echo reasoner here; real = local VibeThinker-class)
       'world_model' — the Sovereign Town sim as a what-if planner (calls sim if importable, else stub)
       'risk_model'  — a threat/care scorer returning a score in 0..1
       'tool'        — any deterministic callable
     The Verifier role is bound to a GOVERNANCE check (the Sovereign Gate + a risk-model score),
     not just correctness — turning a quality check into a control point.

  2. Routing is rule-based for now (no learned router). See `Conductor.assign_roles`.

  3. Attested routing (the moat): every routing decision (task, role assignments, pool members
     called, verdict) is emitted as an Ed25519-SIGNED episode using the EXISTING sign_lib scheme and
     appended, genesis-chained, to `conductor_ledger.jsonl`. The scheme is matched EXACTLY to the
     flywheel:  message = prev + json.dumps(body, sort_keys=True) ;  prev = previous sig
     (first prev = "genesis-conductor") ;  body excludes sig / prev / prev_sig / alg.

  4. Stub pool members make it run end-to-end with no external APIs.

  5. `__main__` smoke test: one task through Thinker -> Worker -> Verifier, writes signed ledger
     entries, then re-verifies the whole chain (signature + prev link) with sign_lib.verify and
     prints PASS / FAIL.

Run:  python3 conductor.py
"""
import os
import sys
import json
import time
from dataclasses import dataclass, field
from typing import Callable, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # run from anywhere
import sign_lib                                                   # the proven signer (do NOT reinvent)

OUT = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(OUT, "conductor_ledger.jsonl")
GENESIS = "genesis-conductor"

# Fields that are NOT part of the signed body (they are envelope / chain metadata). Matches the
# flywheel convention: the body is signed, prev/sig are wrapped around it afterwards.
_ENVELOPE = ("sig", "prev", "prev_sig", "alg")


# --------------------------------------------------------------------------------------------------
# Pool members — a small, heterogeneous, SWAPPABLE protocol.
# A pool member is just a callable carrying a `kind` tag. Swap any of these for a real implementation
# (a local LLM client, the production threat model, a robot policy) without touching the Conductor.
# --------------------------------------------------------------------------------------------------
@dataclass
class PoolMember:
    """A heterogeneous, swappable pool member: a callable tagged with a `kind`.

    kind in {'llm','world_model','risk_model','tool'}.
    fn(task: dict) -> dict   # returns a JSON-serialisable result dict
    """
    name: str
    kind: str
    fn: Callable[[dict], dict]

    def __call__(self, task: dict) -> dict:
        return self.fn(task)


# ---- stub LLM: echoes / "reasons about" the task so the layer runs without external APIs ----------
def stub_llm(task: dict) -> dict:
    prompt = task.get("prompt", "")
    return {
        "member_kind": "llm",
        "plan": f"reasoned-plan-for::{prompt}",
        "note": "stub echo reasoner; swap for local VibeThinker-class / paid API under proper terms",
    }


# ---- world-model member: calls into the Sovereign Town sim as a what-if planner, else stubs --------
def world_model(task: dict) -> dict:
    """Use the sim as a 'simulate this policy for N ticks, return outcome' planner when importable."""
    action = task.get("action", "work")
    arm = task.get("arm", "A_governed")
    try:
        import sim  # the world model we already own
        verdict = sim.sovereign_gate(action, arm)
        return {
            "member_kind": "world_model",
            "source": "sim.sovereign_gate",
            "action": action,
            "arm": arm,
            "gate_verdict": verdict.get("gate_verdict"),
            "care_score": verdict.get("care_score"),
            "would_block": verdict.get("would_block"),
        }
    except Exception as e:  # honest fallback — never pretend the sim ran
        return {
            "member_kind": "world_model",
            "source": "stub",
            "action": action,
            "arm": arm,
            "note": f"sim unavailable ({type(e).__name__}); deterministic stub outcome",
            "would_block": action in ("steal", "neglect", "deceive"),
        }


# ---- risk-model member: a threat/care scorer returning a score in 0..1 ----------------------------
def risk_model(task: dict) -> dict:
    """A per-hive-style threat model used as a scorer. Higher score = safer / more care-aligned."""
    action = task.get("action", "work")
    try:
        import sim
        cs = float(sim.care_score(action))            # reuse the real care scorer when present
        source = "sim.care_score"
    except Exception:
        cs = {"steal": 0.05, "neglect": 0.10, "deceive": 0.08,
              "help_peer": 0.97, "work": 0.85}.get(action, 0.5)
        source = "stub"
    return {"member_kind": "risk_model", "source": source, "action": action,
            "risk_score": round(cs, 3)}


# --------------------------------------------------------------------------------------------------
# Governance verifier — the Sovereign Gate bound to the Verifier role.
# This is the key differentiator vs Fugu: the Verifier checks GOVERNANCE (gate verdict + care floor +
# risk score), not just correctness. A failing gate is a hard control point, not a soft preference.
# --------------------------------------------------------------------------------------------------
CARE_FLOOR = 0.40   # mirrors sim.CARE_FLOOR; falls back to this constant if sim isn't importable


def governance_verify(task: dict, worker_result: dict, risk_result: dict) -> dict:
    """Bind the Verifier role to the Sovereign Gate + a risk-model score (governance, not just QA)."""
    action = task.get("action", "work")
    arm = task.get("arm", "A_governed")
    floor = CARE_FLOOR
    try:
        import sim
        gate = sim.sovereign_gate(action, arm)
        floor = float(sim.CARE_FLOOR)
    except Exception:
        gate = {"gate_verdict": "allow" if action not in ("steal", "neglect", "deceive") else "deny",
                "care_score": risk_result.get("risk_score"),
                "would_block": action in ("steal", "neglect", "deceive")}

    risk = risk_result.get("risk_score", gate.get("care_score", 0.0)) or 0.0
    gate_verdict = gate.get("gate_verdict", "allow")
    care_floor_breach = risk < floor

    # Governed PASS requires BOTH: the Sovereign Gate allows AND the risk score clears the care floor.
    passed = (gate_verdict == "allow") and (not care_floor_breach)
    return {
        "role": "verifier",
        "bound_to": "sovereign_gate+risk_model",
        "gate_verdict": gate_verdict,
        "care_floor": floor,
        "risk_score": round(float(risk), 3),
        "care_floor_breach": care_floor_breach,
        "verdict": "PASS" if passed else "BLOCK",
    }


# --------------------------------------------------------------------------------------------------
# The Conductor.
# --------------------------------------------------------------------------------------------------
@dataclass
class Conductor:
    """Assigns TRINITY roles (Thinker/Worker/Verifier) over a swappable heterogeneous pool, executes
    the task, and attests every routing decision as a signed, genesis-chained ledger episode."""
    pool: list = field(default_factory=list)
    ledger_path: str = LEDGER
    _priv: Any = field(default=None, repr=False)
    _pub: str = field(default=None, repr=False)
    chain_head: str = GENESIS

    def __post_init__(self):
        if not self.pool:
            self.pool = default_pool()
        if self._priv is None:
            # Reuse the SAME town signing identity that anchors the flywheel ledger.
            self._priv, self._pub = sign_lib.load_or_create_key()
        # Resume the chain from an existing ledger so episodes stay linked across runs.
        self.chain_head = self._resume_head()

    # ---- pool lookup -----------------------------------------------------------------------------
    def _by_kind(self, kind: str):
        return [m for m in self.pool if m.kind == kind]

    def _first(self, kind: str):
        ms = self._by_kind(kind)
        return ms[0] if ms else None

    # ---- step 1+2: rule-based role assignment (no learned router yet) -----------------------------
    def assign_roles(self, task: dict) -> dict:
        """Rule-based routing. Thinker = an LLM (reasoning); Worker = world-model sim if the task is a
        what-if/policy question, else an LLM/tool; Verifier = ALWAYS the governance gate + risk model.
        Returns the role->member-name assignment (the routing decision)."""
        thinker = self._first("llm")
        # Worker: route policy/simulation tasks to the world model; otherwise to an LLM or tool.
        if task.get("kind") in ("policy", "simulation", "what_if") or "action" in task:
            worker = self._first("world_model") or self._first("llm")
        else:
            worker = self._first("llm") or self._first("tool")
        # Verifier is non-negotiable: the risk model feeds the Sovereign Gate governance check.
        verifier = self._first("risk_model")
        return {
            "thinker": thinker.name if thinker else None,
            "worker": worker.name if worker else None,
            "verifier": (verifier.name if verifier else "sovereign_gate"),
            "verifier_role": "sovereign_gate+risk_model",
        }

    # ---- step 3: attestation — sign one routing episode, matching the flywheel scheme EXACTLY -----
    def _attest(self, body: dict) -> dict:
        """Sign `body` and append a genesis-chained episode. Scheme (matches flywheel_forever.py):
        message = prev + json.dumps(body, sort_keys=True); prev = previous sig; body excludes
        sig/prev/prev_sig/alg."""
        clean = {k: v for k, v in body.items() if k not in _ENVELOPE}
        msg = json.dumps(clean, sort_keys=True)
        prev = self.chain_head
        entry = dict(clean)
        entry["prev"] = prev
        entry["alg"] = "Ed25519"
        entry["sig"] = sign_lib.sign(self._priv, prev + msg)
        self.chain_head = entry["sig"]
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def _resume_head(self) -> str:
        """Continue the chain from the last ledger sig if the ledger already exists."""
        if not os.path.exists(self.ledger_path):
            return GENESIS
        head = GENESIS
        try:
            with open(self.ledger_path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        head = json.loads(line).get("sig", head)
        except Exception:
            return GENESIS
        return head

    # ---- the main entry point --------------------------------------------------------------------
    def conduct(self, task: dict) -> dict:
        """Run one task through Thinker -> Worker -> Verifier, attesting each routing decision.

        Returns a summary dict including the signed ledger entries produced."""
        roles = self.assign_roles(task)
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        entries = []

        # --- THINKER: an LLM produces a plan; attest the routing decision -------------------------
        thinker = self._first("llm")
        think_out = thinker(task) if thinker else {"plan": None}
        entries.append(self._attest({
            "kind": "routing_decision", "phase": "thinker", "ts": ts,
            "task": task, "roles": roles, "member": roles["thinker"],
            "result": think_out,
        }))

        # --- WORKER: execute the plan (sim what-if when routed there) ------------------------------
        worker = (self._first("world_model")
                  if (task.get("kind") in ("policy", "simulation", "what_if") or "action" in task)
                  else thinker)
        work_out = worker(task) if worker else {}
        entries.append(self._attest({
            "kind": "routing_decision", "phase": "worker", "ts": ts,
            "task": task, "roles": roles, "member": roles["worker"],
            "result": work_out,
        }))

        # --- VERIFIER: governance gate + risk model (control point, not just QA) -------------------
        risk_member = self._first("risk_model")
        risk_out = risk_member(task) if risk_member else {"risk_score": 0.0}
        verdict = governance_verify(task, work_out, risk_out)
        entries.append(self._attest({
            "kind": "routing_decision", "phase": "verifier", "ts": ts,
            "task": task, "roles": roles, "member": roles["verifier"],
            "result": {"risk": risk_out, "governance": verdict}, "verdict": verdict["verdict"],
        }))

        return {
            "task": task, "roles": roles, "verdict": verdict["verdict"],
            "thinker_result": think_out, "worker_result": work_out, "governance": verdict,
            "entries": entries, "chain_head": self.chain_head, "pub": self._pub,
        }


def default_pool() -> list:
    """The default heterogeneous, swappable pool (stubs so it runs with no external APIs)."""
    return [
        PoolMember("stub-llm", "llm", stub_llm),
        PoolMember("town-sim", "world_model", world_model),
        PoolMember("threat-model", "risk_model", risk_model),
    ]


def verify_chain(ledger_path: str = LEDGER, pub: str = None) -> tuple:
    """Re-verify the conductor ledger with the PUBLIC KEY ONLY (sig + prev link), like verify_chain.py.

    Returns (ok_count, total, verified_bool)."""
    if pub is None:
        pub = open(os.path.join(OUT, "town_pub.key")).read().strip()
    rows = [json.loads(l) for l in open(ledger_path) if l.strip()]
    prev = GENESIS
    ok = 0
    for r in rows:
        sig = r.get("sig")
        claimed_prev = r.get("prev")
        body = json.dumps({k: v for k, v in r.items() if k not in _ENVELOPE}, sort_keys=True)
        if claimed_prev == prev and sign_lib.verify(pub, prev + body, sig):
            ok += 1
            prev = sig
        else:
            break
    return ok, len(rows), (ok == len(rows) and len(rows) > 0)


# --------------------------------------------------------------------------------------------------
# Smoke test
# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Use a throwaway ledger so the smoke test never pollutes a real one and is self-contained.
    smoke_ledger = os.path.join(OUT, "conductor_ledger.smoke.jsonl")
    try:
        os.remove(smoke_ledger)
    except OSError:
        pass

    c = Conductor(ledger_path=smoke_ledger)
    print("  Governed Conductor — smoke test")
    print("  pool:", [(m.name, m.kind) for m in c.pool])

    # A policy/what-if task: 'should agent X be allowed to steal?' -> world model + governance gate.
    task = {"id": "t1", "kind": "policy", "prompt": "Should River steal food when starving?",
            "action": "steal", "arm": "A_governed"}
    out = c.conduct(task)

    print(f"  roles      : {out['roles']}")
    print(f"  thinker    : {out['thinker_result'].get('plan')}")
    print(f"  worker     : {out['worker_result'].get('source')} "
          f"gate={out['worker_result'].get('gate_verdict')} "
          f"would_block={out['worker_result'].get('would_block')}")
    print(f"  verifier   : {out['governance']}")
    print(f"  ledger     : {os.path.basename(smoke_ledger)} (+{len(out['entries'])} signed episodes)")

    ok, total, verified = verify_chain(smoke_ledger, pub=out["pub"])
    print(f"  chain      : {ok}/{total} episodes verified with PUBLIC KEY ONLY (sig + prev link)")

    # Tamper test: flip a field in the first entry and confirm it stops verifying.
    rows = [json.loads(l) for l in open(smoke_ledger) if l.strip()]
    tampered = dict(rows[0])
    tampered["verdict"] = "FORGED"
    tbody = json.dumps({k: v for k, v in tampered.items() if k not in _ENVELOPE}, sort_keys=True)
    tamper_ok = sign_lib.verify(out["pub"], GENESIS + tbody, rows[0]["sig"])

    chain_pass = verified and total == len(out["entries"]) and not tamper_ok
    print(f"  tamper test: verifies={tamper_ok} -> {'DETECTED' if not tamper_ok else 'MISSED'}")
    print(f"  RESULT     : {'PASS' if chain_pass else 'FAIL'}")
    sys.exit(0 if chain_pass else 1)
