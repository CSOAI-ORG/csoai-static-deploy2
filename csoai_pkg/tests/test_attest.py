"""Real verification tests for csoai.attest — no fixtures faked green.

Merkle: build a reference RFC 6962 tree, generate inclusion proofs, and check the
verifier reproduces the root (and rejects tampering). DSSE: sign real PAEs with
Ed25519 and ECDSA-P256 and verify. Honesty: unchecked/unsupported inputs are NOT
reported valid. Run:  python tests/test_attest.py
"""
import base64
import hashlib
import json

from csoai import attest


# --- reference RFC 6962 tree (independent of the verifier, to generate proofs) ---
def _leaf(d):
    return hashlib.sha256(b"\x00" + d).digest()


def _node(l, r):
    return hashlib.sha256(b"\x01" + l + r).digest()


def _mth(leaves):
    n = len(leaves)
    if n == 1:
        return _leaf(leaves[0])
    k = 1
    while k * 2 < n:
        k *= 2
    return _node(_mth(leaves[:k]), _mth(leaves[k:]))


def _proof(leaves, m):
    n = len(leaves)
    if n == 1:
        return []
    k = 1
    while k * 2 < n:
        k *= 2
    if m < k:
        return _proof(leaves[:k], m) + [_mth(leaves[k:])]
    return _proof(leaves[k:], m - k) + [_mth(leaves[:k])]


def test_merkle_roundtrip():
    for n in (1, 2, 3, 4, 5, 8, 13, 100):
        leaves = [f"entry-{i}".encode() for i in range(n)]
        root = _mth(leaves)
        for m in range(n):
            proof = _proof(leaves, m)
            assert attest.verify_inclusion(_leaf(leaves[m]), m, n, proof, root), f"n={n} m={m} should verify"
            # tamper: wrong root
            assert not attest.verify_inclusion(_leaf(leaves[m]), m, n, proof, b"\x00" * 32)
            # tamper: wrong leaf
            if n > 1:
                assert not attest.verify_inclusion(_leaf(b"forged"), m, n, proof, root)
    print("  ✓ merkle inclusion: round-trips for n∈{1..100}, rejects tampered root & leaf")


def test_rekor_entry():
    leaves = [f"log-entry-{i}".encode() for i in range(9)]
    idx = 4
    entry = {
        "body": base64.b64encode(leaves[idx]).decode(),
        "inclusionProof": {
            "logIndex": idx,
            "treeSize": len(leaves),
            "rootHash": _mth(leaves).hex(),
            "hashes": [h.hex() for h in _proof(leaves, idx)],
        },
    }
    v = attest.verify_rekor_v2(entry)
    assert v["verified"] and v["format"] == "rekor-v2", v
    # tamper the body → must fail
    bad = json.loads(json.dumps(entry))
    bad["body"] = base64.b64encode(b"tampered").decode()
    assert not attest.verify_rekor_v2(bad)["verified"]
    print("  ✓ rekor-v2 inclusion: real entry verifies, tampered body rejected")


def test_dsse_ed25519():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    sk = Ed25519PrivateKey.generate()
    pub_raw = sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    payload = json.dumps({
        "_type": "https://in-toto.io/Statement/v1",
        "predicateType": "https://slsa.dev/provenance/v1",
        "subject": [{"name": "pkg.tar.gz", "digest": {"sha256": "abc"}}],
        "predicate": {"buildType": "demo"},
    }).encode()
    ptype = "application/vnd.in-toto+json"
    sig = sk.sign(attest.pae(ptype, payload))
    env = {"payloadType": ptype, "payload": base64.b64encode(payload).decode(),
           "signatures": [{"sig": base64.b64encode(sig).decode()}]}
    v = attest.verify_dsse(env, base64.b64encode(pub_raw).decode())
    assert v["verified"] and v.get("is_slsa") and v["predicateType"] == "https://slsa.dev/provenance/v1", v
    # tamper payload → fail
    bad = dict(env, payload=base64.b64encode(payload + b" ").decode())
    assert not attest.verify_dsse(bad, base64.b64encode(pub_raw).decode())["verified"]
    # no key → NOT verified (honesty), but structure parsed
    nk = attest.verify_dsse(env)
    assert nk["verified"] is False and nk.get("predicateType"), nk
    print("  ✓ dsse ed25519: SLSA envelope verifies, tamper rejected, no-key→not-verified (honest)")


def test_dsse_ecdsa():
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization, hashes
    sk = ec.generate_private_key(ec.SECP256R1())
    pem = sk.public_key().public_bytes(serialization.Encoding.PEM,
                                        serialization.PublicFormat.SubjectPublicKeyInfo)
    payload = b'{"_type":"https://in-toto.io/Statement/v1","predicateType":"x"}'
    ptype = "application/vnd.in-toto+json"
    sig = sk.sign(attest.pae(ptype, payload), ec.ECDSA(hashes.SHA256()))
    env = {"payloadType": ptype, "payload": base64.b64encode(payload).decode(),
           "signatures": [{"sig": base64.b64encode(sig).decode()}]}
    assert attest.verify_dsse(env, pem)["verified"], "ecdsa-p256 DSSE should verify"
    print("  ✓ dsse ecdsa-p256: envelope verifies with PEM key")


def test_dispatcher_and_honesty():
    # unknown → not verified
    assert attest.detect_and_verify({"foo": "bar"})["verified"] is False
    # SCITT recognised but unsupported → not a fake pass
    s = attest.detect_and_verify({"kind": "scitt", "protected": "x"})
    assert s["verified"] is False and s["format"] == "scitt-cose", s
    print("  ✓ dispatcher: unknown & SCITT return NOT-verified (never a fake green)")


if __name__ == "__main__":
    tests = [test_merkle_roundtrip, test_rekor_entry, test_dsse_ed25519,
             test_dsse_ecdsa, test_dispatcher_and_honesty]
    for t in tests:
        t()
    print(f"\nALL {len(tests)} attest test groups passed.")
