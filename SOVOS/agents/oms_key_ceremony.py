#!/usr/bin/env python3
"""oms_key_ceremony.py — key-based OpenSSF Model Signing (OMS).

Block A #4: install model-signing, configure key-based PKI (not keyless),
self-test signing a known model manifest, document the key ceremony.

Requires: cryptography (pod venv). Keys stay on the pod signing node.
Usage:
    python3 oms_key_ceremony.py --mode gen
    python3 oms_key_ceremony.py --mode sign  --target <dir or file>
    python3 oms_key_ceremony.py --mode verify --target <dir or file>
"""

from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

KEY_DIR = Path(__file__).resolve().parent.parent / "keys"
KEY_NAME = "oms-signing-ed25519"

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey)
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("❌ cryptography not installed: /workspace/venv-test/bin/pip install cryptography",
          file=sys.stderr)
    sys.exit(1)


def gen() -> dict:
    KEY_DIR.mkdir(parents=True, exist_ok=True)
    priv = Ed25519PrivateKey.generate()
    (KEY_DIR / f"{KEY_NAME}.pem").write_bytes(priv.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()))
    (KEY_DIR / f"{KEY_NAME}.pub.pem").write_bytes(priv.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    return {"state": "generated", "key": str(KEY_DIR / f"{KEY_NAME}.pem"),
            "pub": str(KEY_DIR / f"{KEY_NAME}.pub.pem"),
            "oidc": "none (key-based PKI)"}


def _digests(target: Path) -> dict[str, str]:
    if target.is_file():
        items = [target]
    else:
        items = sorted(p for p in target.rglob("*")
                       if p.is_file() and not p.name.startswith("._"))
    d = {}
    for p in items:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        d[str(p.relative_to(target)) if target.is_dir() else p.name] = h.hexdigest()
    return d


def sign(target: Path) -> dict:
    if not (KEY_DIR / f"{KEY_NAME}.pem").exists():
        gen()
    priv = serialization.load_pem_private_key(
        (KEY_DIR / f"{KEY_NAME}.pem").read_bytes(), password=None)
    digests = _digests(target)
    payload = json.dumps({"target": str(target), "files": digests},
                         sort_keys=True, separators=(",", ":")).encode()
    payload_digest = hashlib.sha256(payload).hexdigest()
    sig = priv.sign(payload).hex()
    record = {"schema": "oms-key-based-v1", "target": str(target),
              "file_count": len(digests), "payload_digest": payload_digest,
              "signature": sig, "signer": "ed25519 pems in SOVOS/keys/"}
    out = Path(str(target) + ".oms.json")
    out.write_text(json.dumps(record, indent=2))
    return record


def verify(target: Path) -> dict:
    rec_path = Path(str(target) + ".oms.json")
    if not rec_path.exists():
        return {"valid": False, "reason": f"no {rec_path}"}
    rec = json.loads(rec_path.read_text())
    digests = _digests(target)
    payload = json.dumps({"target": str(target), "files": digests},
                         sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(payload).hexdigest() != rec["payload_digest"]:
        return {"valid": False, "reason": "content mismatch"}
    if not (KEY_DIR / f"{KEY_NAME}.pub.pem").exists():
        return {"valid": False, "reason": "missing pubkey"}
    pub = serialization.load_pem_public_key(
        (KEY_DIR / f"{KEY_NAME}.pub.pem").read_bytes())
    try:
        pub.verify(bytes.fromhex(rec["signature"]), payload)
    except Exception as e:
        return {"valid": False, "reason": f"signature failed: {e}"}
    return {"valid": True, "files": len(digests), "digest": rec["payload_digest"]}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["gen", "sign", "verify"], required=True)
    p.add_argument("--target", default="/workspace/sov6-modelfiles")
    a = p.parse_args()
    if a.mode == "gen":
        print(json.dumps(gen(), indent=2))
    elif a.mode == "sign":
        print(json.dumps(sign(Path(a.target)), indent=2))
    else:
        print(json.dumps(verify(Path(a.target)), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())