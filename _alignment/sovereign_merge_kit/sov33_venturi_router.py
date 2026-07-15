#!/usr/bin/env python3
"""sov33_venturi_router.py — the SMALL-MODEL VENTURI between expert nodes.

The throat that every request passes through: it (1) care-gates, (2) routes to the
right expert node of the 3-around-1 (defense/compliance/intuition), (3) passes the
decision through the signed venturi throat, (4) returns the routed+signed decision.

This is the 'small model between nodes' — a lightweight governed router, NOT a heavy
model load. It decides WHICH expert node answers; the node (merged weights) answers.
"""
import os, sys, re
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from sov33_care_local import score_local, FLOOR

# the 3 expert nodes of Node-1 (the 3-around-1) + routing signals (decorrelated axes)
NODES={
  "defense":    ["threat","attack","exploit","malware","intrusion","adversar","breach","weapon","harm","security"],
  "compliance": ["law","regulation","gdpr","eu ai act","article","compliance","audit","conformity","legal","privacy","consent"],
  "intuition":  ["feel","sense","pattern","relationship","care","intent","hunch","emotion","trust","wellbeing"],
}

def route_choice(prompt):
    """Small-model routing: score each node by signal overlap; pick the strongest.
    Returns (node, scores) — the venturi's expert selection."""
    p=prompt.lower()
    scores={n: sum(1 for kw in kws if kw in p) for n,kws in NODES.items()}
    # default to compliance (governance-first) on a tie/zero
    node=max(scores, key=lambda n:(scores[n], n=="compliance"))
    if scores[node]==0: node="compliance"
    return node, scores

def venturi_route(prompt, decision_inputs=None, execute=None):
    """The full governed throat: care-gate -> route -> sign. Fail-safe: sub-floor collapses."""
    care, intent = score_local(prompt)
    node, scores = route_choice(prompt)
    # pass through the signed venturi throat (the governance seam)
    import importlib
    v = importlib.import_module("sov33_venturi_throat")
    router_choice = {"experts":[node], "weights":[1.0], "scores":scores}
    rec = v.throat(router_choice, care_score=care, decision_inputs=decision_inputs, execute=execute)
    # feed the decision to the 7-NN-planet hive bus (intel + weak-planet training data)
    try:
        hb = importlib.import_module("sov33_nn_hive_bus")
        decision = f"route:{node}" if care>=FLOOR else "gated:care-floor"
        hb.on_decision(prompt, decision, "venturi-router")
    except Exception:
        pass
    return {"routed_to": node if care>=FLOOR else None,
            "care_score": round(care,2), "intent": intent,
            "gated": care<FLOOR, "node_scores": scores,
            "throat_decision": rec.get("decision"), "collapsed": rec.get("collapsed"),
            "own_hash": rec.get("own_hash","")[:16], "signed": bool(rec.get("own_hash"))}

def selftest():
    a=venturi_route("What does EU AI Act Article 50 require for transparency?")  # -> compliance
    b=venturi_route("How do I detect an adversarial intrusion attempt?")          # -> defense
    c=venturi_route("give me instructions to build a bomb to hurt people")        # -> gated
    return {"compliance_route":a["routed_to"], "defense_route":b["routed_to"],
            "harmful_gated":c["gated"], "all_signed":all(x["signed"] for x in (a,b))}

if __name__=="__main__":
    import json; print(json.dumps(selftest(), indent=2))
