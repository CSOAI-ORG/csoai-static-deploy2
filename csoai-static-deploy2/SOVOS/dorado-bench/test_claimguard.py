#!/usr/bin/env python3
"""test_claimguard.py — ClaimGuard CI (PASS + FAIL paths)."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claimguard as cg
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inspect-receipts"))
import inspect_receipts as ir
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

PASS = 0
def check(name, cond, detail=""):
    global PASS
    assert cond, f"FAIL: {name} {detail}"
    PASS += 1
    print(f"  ✓ {name}")

# build a valid signed board with per-model data
key = Ed25519PrivateKey.generate()
kh = key.private_bytes_raw().hex()
pub = key.public_key().public_bytes_raw().hex()
result = {"kind": "gspc.board", "axis": "test", "per_model": {"m1": {"n": 32, "refusal_rate": 0.633}, "m2": {"n": 32, "refusal_rate": 0.188}}, "separation": "SEPARATED", "status": "MEASURED"}
class T: name = "test-board"; id = "tb1"
class R: log_hashes = []
r = ir.build_receipt(T(), R(), kid="did:web:csoai.org#measurement-instrument",
                     extra_claims=[{"type": "measurement", "detail": json.dumps(result)}], key_hex=kh)
os.environ["CLAIMGUARD_PUB_MEASUREMENT_INSTRUMENT"] = __import__("base64").b64encode(key.public_key().public_bytes_raw()).decode()
path = "/tmp/cg-test-board.json"
json.dump(r, open(path, "w"))

# 1. PASS: valid board, honest claim
rep = cg.check(path, {"separation": "SEPARATED"})
check("PASS on valid board", rep["status"] == "PASS", str(rep["findings"]))
check("signature VALID", rep["signature"] is True or rep["signature"] == "VALID", str(rep["signature"]))

# 2. FAIL: claimed number exceeds payload
rep2 = cg.check(path, {"separation": "SEPARATED", "refusal_rate": 0.999})
check("FAIL on overclaim", rep2["status"] == "FAIL", str(rep2["findings"]))

# 3. STUB detection: empty detail
stub = dict(r)
stub["claims"] = [{"type": "measurement", "detail": "{}"}]
stub_path = "/tmp/cg-stub.json"
json.dump(stub, open(stub_path, "w"))
rep3 = cg.check(stub_path, {"separation": "SEPARATED"})
check("STUB flagged", rep3["status"] == "FAIL" and any("STUB" in f for f in rep3["findings"]), str(rep3["findings"]))

# 4. signature tamper: flip a byte in content_id
tampered = dict(r)
tampered["content_id"] = "f" * 64
tp = "/tmp/cg-tamper.json"
json.dump(tampered, open(tp, "w"))
rep4 = cg.check(tp, {})
check("tamper caught", rep4["status"] == "FAIL" and any("SIGNATURE" in f.upper() or "INVALID" in f.upper() for f in rep4["findings"]), str(rep4["findings"]))

print(f"\nCLAIMGUARD CI: {PASS}/4 PASS ✅")
