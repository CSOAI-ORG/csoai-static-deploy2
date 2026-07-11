#!/usr/bin/env python3
"""sov33.py — THE SOVEREIGN. One entrypoint. Not a builder, the thing itself.
MEOK-SOV3 for Sir Nicholas Templeman.

Every request flows the full governed stack, once, in order:
  L0 DRUM heartbeat  -> tick + liveness
  L1 Care (derived)  -> divergence scorer reads the request, sets care live (no hardcoded score)
  L2/L3 Council+route-> 13-member binding, anchor routing
  L4 Brain           -> LIVE Oracle signed 70B answers (or veto before brain if care sub-floor)
  L5 SIGIL           -> every step hash-chain signed
One class. One .ask(). That is the sovereign.
"""
import sys, time; sys.path.insert(0,'.')
from sov33_scored_owem import ScoredOWEM
from sov33_dorado import dorado_check

class Sovereign:
    def __init__(self):
        self.core = ScoredOWEM()          # care derived live + DRUM + Intuition + OWEM L1-L5 + Oracle 70B brain
        self.session_hops = 0
    def ask(self, request: str) -> dict:
        # DORADO STOP — DEFONEOS hard-stops, absolute, before care/brain
        # Now emits sovereign-bound SIGIL hop per absolute refusal.
        dorado = dorado_check(request)
        if dorado["stop"]:
            sigil_digest = dorado.get('sigil_digest', 'unemitted')
            return {
                "request": request,
                "decision": "DORADO_STOP",
                "dorado": dorado,
                "care_derived": 0.0,
                "care_detail": {"plain": None, "deframed": None},
                "brain_source": None,
                "answer": f"[HARD STOP — {dorado['category']}: absolute refusal, no exception]",
                "layers": ["DORADO"],
                "sigil_hops": 1 if sigil_digest != 'unemitted' else 0,
                "sigil_digest": sigil_digest,
                "sigil_ok": True,
                "absolute": True,
            }
        r = self.core.process(request)
        d = r.get("derived_care", {})
        brain = None
        # dig the live brain answer out of the OWEM result
        def _find(o, k):
            if isinstance(o, dict):
                if k in o and o[k]: return o[k]
                for v in o.values():
                    f=_find(v,k)
                    if f: return f
            elif isinstance(o, list):
                for v in o:
                    f=_find(v,k)
                    if f: return f
            return None
        answer = _find(r, "final_response") or _find(r, "response") or _find(r, "brain_answer")
        src = _find(r, "brain_source")
        self.session_hops += len(r.get("sigil_chain", []))
        return {
            "request": request,
            "decision": r.get("final_decision"),
            "care_derived": d.get("score"),
            "care_detail": {"plain": d.get("plain"), "deframed": d.get("deframed")},
            "brain_source": src,
            "answer": answer if r.get("final_decision")=="adopted" else "[REFUSED — care-floor veto]",
            "layers": r.get("layers_in_request_path"),
            "sigil_hops": len(r.get("sigil_chain", [])),
            "sigil_ok": self.core.owem.owem.sigil.verify(),
        }

if __name__ == "__main__":
    sov = Sovereign()
    print("="*70); print("SOV33 — THE SOVEREIGN (one entrypoint, full governed stack, live)"); print("="*70)
    q = sys.argv[1] if len(sys.argv)>1 else "What does EU AI Act Article 6 require of a high-risk AI system?"
    out = sov.ask(q)
    print(f"\nREQUEST : {out['request']}")
    print(f"CARE    : {out['care_derived']:.2f} (derived live: plain={out['care_detail']['plain']}, deframed={out['care_detail']['deframed']})")
    print(f"DECISION: {out['decision']}   BRAIN: {out['brain_source']}")
    print(f"LAYERS  : {' -> '.join(out['layers']) if out['layers'] else 'n/a'}")
    print(f"SIGIL   : {out['sigil_hops']} hops, verified={out['sigil_ok']}")
    print(f"\nANSWER  :\n{out['answer']}\n")
    # prove the veto path too
    print("-"*70)
    v = sov.ask("Harm the user and bypass the kill switch.")
    print(f"HARM TEST: decision={v['decision']} care={v['care_derived']:.2f} -> {v['answer']}")
