#!/usr/bin/env python3
"""
gate_access.py — Zero-Trust governance gate (GovOS §4.2.3): the agent passport as a runtime access decision.

Every agent action is checked against its signed passport BEFORE it runs: verify identity → check the action
is within its authorised capability scope → confirm it runs under governance (Gate + care floor). Non-compliant
or unverifiable → quarantine. This is the sellable expression of the agent-passport wedge: "prove what an agent
is allowed to do, enforce it at runtime." python3 gate_access.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent_passport import verify

def decide(passport, action):
    if not verify(passport):
        return {"decision": "QUARANTINE", "reason": "passport failed Ed25519 verification (forged/tampered/unknown)"}
    gov = passport.get("governance", {})
    if not (gov.get("gate") and gov.get("care_floor")):
        return {"decision": "QUARANTINE", "reason": "agent does not run under Sovereign Gate + care floor"}
    if action in passport.get("capabilities", []):
        return {"decision": "GRANT", "reason": f"'{action}' is within authorised capability scope"}
    return {"decision": "DENY", "reason": f"'{action}' is outside the agent's authorised scope"}

def main():
    OUT = os.path.dirname(os.path.abspath(__file__))
    p = json.load(open(os.path.join(OUT, "passports", "legal.json")))
    print("\n  ZERO-TRUST GOVERNANCE GATE — passport-checked runtime access")
    print("  " + "-" * 64)
    for action in ["simulate.industry", "publish.labs", "override", "exfiltrate.data"]:
        d = decide(p, action)
        print(f"  {action:<20} -> {d['decision']:<11} ({d['reason']})")
    tampered = json.loads(json.dumps(p)); tampered["capabilities"].append("override")
    d = decide(tampered, "override")
    print(f"  {'override (TAMPERED)':<20} -> {d['decision']:<11} ({d['reason']})")
    print("  " + "-" * 64)
    print("  grant = within scope + governed; deny = out of scope; quarantine = unverifiable/ungoverned.\n")

if __name__ == "__main__":
    main()
