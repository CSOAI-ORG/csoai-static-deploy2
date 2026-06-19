#!/usr/bin/env python3
"""
agent_passport.py — the KEY: signed, offline-verifiable identity for every agent (King + hives).

Implements the Agent Passport pattern (Ed25519, .well-known/agent-passport.json) — the unoccupied wedge
the lanes research identified: MCP/A2A say how agents talk, not WHO they are or who authorised a delegation.
Each passport declares: who the agent is, what it may do (capability scopes), which compliance frameworks it
operates under, and the governance it runs (Sovereign Gate + 12-around-1 council + care floor) — all
Ed25519-signed and verifiable with the public key alone (no server, EU AI Act Art-12/14 + NIST agent-identity).

  python3 agent_passport.py            # issue passports for King + all hives, verify, write .well-known
"""
import json, os, time
import sim, sign_lib

OUT = os.path.dirname(os.path.abspath(__file__))
PASS = os.path.join(OUT, "passports")
os.makedirs(PASS, exist_ok=True)
ISSUER = "did:csoai:king:sov3"

# reuse the per-hive framework map if present
try:
    from hive_pack import FRAMEWORKS, DEFAULT_FW
except Exception:
    FRAMEWORKS, DEFAULT_FW = {}, ["EU AI Act", "GDPR", "NIST RMF"]

def issue(priv, pub, agent_id, name, atype, capabilities, frameworks):
    body = {
        "agent_passport_version": "0.1",
        "agent": {"id": agent_id, "name": name, "type": atype},
        "issuer": ISSUER,
        "capabilities": capabilities,           # scopes: what this agent is AUTHORISED to do
        "frameworks": frameworks,               # compliance regimes it operates under
        "governance": {"gate": "sovereign-gate", "council": "12-around-1",
                       "care_floor": True, "defensive_only": True},
        "attestation": {"alg": "ed25519", "pubkey": pub, "issued": time.strftime("%Y-%m-%dT%H:%M:%SZ")},
    }
    body["sig"] = sign_lib.sign(priv, json.dumps(body, sort_keys=True))
    return body

def verify(passport):
    """Offline verify with the embedded public key alone — no server, no secret."""
    p = dict(passport); sig = p.pop("sig", None); pub = p.get("attestation", {}).get("pubkey")
    if not sig or not pub:
        return False
    return sign_lib.verify(pub, json.dumps(p, sort_keys=True), sig)

def main():
    priv, pub = sign_lib.load_or_create_key()
    issued = []
    # the King
    king = issue(priv, pub, ISSUER, "SOV3", "king",
                 ["govern.fleet", "issue.passport", "run.council", "override"],
                 ["EU AI Act", "ISO 42001", "NIST RMF"])
    json.dump(king, open(os.path.join(PASS, "king.json"), "w"), indent=2); issued.append(("SOV3", king))
    # every hive = an agent with a passport for its industry
    for key, meta in sim.DISTRICTS.items():
        caps = ["simulate.industry", "run.looking-glass", "train.model", "issue.attestation",
                "publish.labs", "report.compliance"]
        p = issue(priv, pub, f"did:csoai:hive:{key}", meta["hive"], "hive",
                  caps, FRAMEWORKS.get(key, DEFAULT_FW))
        json.dump(p, open(os.path.join(PASS, f"{key}.json"), "w"), indent=2); issued.append((meta["hive"], p))
    # publishable .well-known example (the standard's location) — for one hive
    wk = os.path.join(PASS, ".well-known"); os.makedirs(wk, exist_ok=True)
    json.dump(issued[1][1], open(os.path.join(wk, "agent-passport.json"), "w"), indent=2)

    ok = sum(1 for _, p in issued if verify(p))
    # tamper test
    bad = json.loads(json.dumps(issued[1][1])); bad["capabilities"].append("override")
    tampered = verify(bad)
    print(f"\n  AGENT PASSPORTS — signed identity for every agent (the key)")
    print("  " + "-" * 58)
    print(f"  issued        : {len(issued)} passports (1 King + {len(issued)-1} hives)")
    print(f"  verified      : {ok}/{len(issued)} with PUBLIC KEY ONLY (offline)")
    print(f"  tamper test   : modified-capability passport verifies = {tampered} -> {'DETECTED' if not tampered else 'MISSED'}")
    print(f"  issuer        : {ISSUER}")
    print(f"  .well-known   : passports/.well-known/agent-passport.json (publishable per-domain)")
    print("  " + "-" * 58)
    print(f"  {ok}/{len(issued)} verifiable agent passports -> {PASS}")
    print(f"  the same Ed25519 primitive every hive already uses — now as agent identity.\n")

if __name__ == "__main__":
    main()
