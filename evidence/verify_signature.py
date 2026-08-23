#!/usr/bin/env python3
"""verify_signature.py — STANDALONE Ed25519 verifier for csoai signed verdicts.

No signing node, no sign.py, no private key. A stranger verifies with JUST:
  1. the signed verdict JSON (embeds pubkey + sig), and
  2. the `cryptography` library (pip install cryptography).

Usage:
    python3 verify_signature.py <signed-verdict.json> [pubkey_b64]
    # pubkey optional — taken from the artifact's embedded signature.pubkey if omitted

Prints "VALID" (exit 0) or exits non-zero with "INVALID".

PQC note: the signature primitive is Ed25519; verify is one swap to ML-DSA-65 (liboqs) per sign.py.
"""
import json, sys, base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def canonical_body(obj):
    # Sign the body WITHOUT signature/sha256/sig fields, so verification is stable (mirrors sign.py).
    clean = {k: v for k, v in obj.items() if k not in ("signature", "sha256", "sig")}
    return json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()


def main(path, pub=None):
    obj = json.load(open(path))
    s = obj.get("signature")
    if not s or s.get("kind") != "ed25519":
        sys.exit("NO ED25519 SIGNATURE — this may be an honestly-unsigned checksum record, not a signed verdict.")
    pub_b64 = pub or s.get("pubkey")
    if not pub_b64:
        sys.exit("no public key available — supply it as a second argument.")
    pk = Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64))
    try:
        pk.verify(base64.b64decode(s["sig"]), canonical_body(obj))
        print(f"VALID — signed by the holder of the published key; unaltered. (subject={obj.get('id')})")
        return 0
    except Exception:
        sys.exit("INVALID — signature does not verify. The verdict was altered or signed by a different key.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 verify_signature.py <signed-verdict.json> [pubkey_b64]")
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
