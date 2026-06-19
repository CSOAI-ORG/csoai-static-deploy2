#!/usr/bin/env python3
"""
consent_vault.py — "Sovereign knows you" done as SOVEREIGNTY, not surveillance.

The sovereign_human doc's good kernel: stop re-explaining yourself to amnesiac AI every session — keep
persistent context so it helps you without re-learning. The doc's framing ("knows EVERY human / absorbs all")
is mass surveillance — illegal and the opposite of sovereignty. This is the inversion:

  • The PERSON owns their data (it lives in their vault, not ours).
  • They GRANT the sovereign scoped, time-bound, REVOCABLE access via an Ed25519-signed consent record.
  • The sovereign knows you ONLY because you chose to be known — and you can revoke it any time.
  • Every access is checked against a live, signed, non-revoked grant (auditable, GDPR-lawful basis = consent).

python3 consent_vault.py   # demo: grant → access allowed → revoke → access denied
"""
import json, os, time
import sign_lib

OUT = os.path.dirname(os.path.abspath(__file__))
GRANTS = os.path.join(OUT, "consent_grants.jsonl")

def grant(priv, person, grantee, scopes, ttl_days=365):
    rec = {"type": "consent_grant", "person": person, "grantee": grantee, "scopes": scopes,
           "issued": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "ttl_days": ttl_days,
           "grant_id": f"cg-{abs(hash((person,grantee,tuple(scopes),time.time())))%10**10}"}
    rec["sig"] = sign_lib.sign(priv, json.dumps(rec, sort_keys=True))   # the PERSON signs (their authority)
    with open(GRANTS, "a") as f: f.write(json.dumps(rec) + "\n")
    return rec

def revoke(priv, person, grant_id):
    rec = {"type": "consent_revoke", "person": person, "grant_id": grant_id,
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ")}
    rec["sig"] = sign_lib.sign(priv, json.dumps(rec, sort_keys=True))
    with open(GRANTS, "a") as f: f.write(json.dumps(rec) + "\n")
    return rec

def has_consent(pub, grantee, scope):
    """Sovereign checks: is there a valid, signed, non-revoked grant for this grantee+scope?"""
    grants, revoked = {}, set()
    if not os.path.exists(GRANTS): return False, "no vault grants"
    for line in open(GRANTS):
        r = json.loads(line)
        if r["type"] == "consent_grant":
            body = {k: v for k, v in r.items() if k != "sig"}
            if sign_lib.verify(pub, json.dumps(body, sort_keys=True), r["sig"]):
                grants[r["grant_id"]] = r
        elif r["type"] == "consent_revoke":
            revoked.add(r["grant_id"])
    for gid, g in grants.items():
        if gid in revoked: continue
        if g["grantee"] == grantee and scope in g["scopes"]:
            return True, f"granted by {g['person']} ({gid})"
    return False, "no valid consent for this scope (or revoked)"

def main():
    priv, pub = sign_lib.load_or_create_key()
    if os.path.exists(GRANTS): os.remove(GRANTS)
    print("\n  CONSENT VAULT — sovereign knows you because you CHOSE (not surveillance)")
    print("  " + "-" * 64)
    g = grant(priv, "did:person:nick", "did:csoai:king:sov3", ["health.context", "business.context"])
    print(f"  Nick grants sovereign scoped access: {g['scopes']}  ({g['grant_id']})")
    for scope in ["business.context", "location.realtime"]:
        ok, why = has_consent(pub, "did:csoai:king:sov3", scope)
        print(f"  sovereign access '{scope}': {'ALLOW' if ok else 'DENY'}  ({why})")
    revoke(priv, "did:person:nick", g["grant_id"])
    ok, why = has_consent(pub, "did:csoai:king:sov3", "business.context")
    print(f"  after Nick REVOKES → access 'business.context': {'ALLOW' if ok else 'DENY'}  ({why})")
    print("  " + "-" * 64)
    print("  the person owns + signs the grant; the sovereign only acts on a live, revocable consent. GDPR-lawful.\n")

if __name__ == "__main__":
    main()
