#!/usr/bin/env python3
"""
selftest.py — fast regression guard for the Sovereign OS. Run before any commit.

Exercises the core invariants on tiny inputs (no fleet writes): the engine, shared helpers, signing,
passports, the zero-trust gate, consent vault, and the looking-glass enforcement curve. Exits non-zero
on any failure so it can gate CI. python3 selftest.py
"""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check(name, fn):
    try:
        ok, detail = fn()
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:<34} {detail}")
        return ok
    except Exception as e:
        print(f"  [FAIL] {name:<34} {type(e).__name__}: {e}")
        return False

def t_engine():
    import sim
    a = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47)
    return a["violations"] == 0, f"governed aqua = {a['violations']} crimes (expect 0)"

def t_common():
    import common, sim
    p = common.profile_for("legal"); f = common.features  # importable + callable
    return "off" in p and len(common.FEATURE_NAMES) == 9, f"profile keys ok, {len(common.FEATURE_NAMES)} features"

def t_sign():
    import sign_lib
    priv, pub = sign_lib.load_or_create_key()
    s = sign_lib.sign(priv, "hello")
    return sign_lib.verify(pub, "hello", s) and not sign_lib.verify(pub, "tampered", s), "Ed25519 roundtrip + tamper-reject"

def t_passport():
    import agent_passport, sign_lib
    priv, pub = sign_lib.load_or_create_key()
    p = agent_passport.issue(priv, pub, "did:csoai:test", "t", "hive", ["x"], ["EU AI Act"])
    bad = json.loads(json.dumps(p)); bad["capabilities"].append("override")
    return agent_passport.verify(p) and not agent_passport.verify(bad), "verify ok + tamper-reject"

def t_gate():
    import agent_passport, sign_lib, gate_access
    priv, pub = sign_lib.load_or_create_key()
    p = agent_passport.issue(priv, pub, "did:csoai:test", "t", "hive", ["simulate.industry"], [])
    g = gate_access.decide(p, "simulate.industry")["decision"]
    d = gate_access.decide(p, "exfiltrate.data")["decision"]
    return g == "GRANT" and d == "DENY", f"in-scope={g}, out-of-scope={d}"

def t_looking_glass():
    import sim
    strict = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47, block_rate=1.0)
    loose  = sim.run_arm("A_governed", None, {"sig": ""}, None, sign=False, district="aqua", seed=47, block_rate=0.0)
    return strict["violations"] < loose["violations"], f"strict {strict['violations']} < ungoverned {loose['violations']}"

def main():
    print("\n  SOVEREIGN OS — SELFTEST")
    print("  " + "-" * 56)
    tests = [("engine: governed = 0 crimes", t_engine), ("common: shared helpers", t_common),
             ("sign_lib: Ed25519", t_sign), ("agent_passport", t_passport),
             ("zero-trust gate", t_gate), ("looking-glass enforcement curve", t_looking_glass)]
    results = [check(n, f) for n, f in tests]
    print("  " + "-" * 56)
    p = sum(results)
    print(f"  {p}/{len(results)} passed\n")
    sys.exit(0 if p == len(results) else 1)

if __name__ == "__main__":
    main()
