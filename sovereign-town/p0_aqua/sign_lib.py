#!/usr/bin/env python3
"""
Ed25519 attestation for Sovereign Town episodes (the proofof.ai signing primitive).

Asymmetric: episodes are signed with a private key, verifiable by ANYONE holding only the public
key — no server, no shared secret (EU AI Act Art-12 record-keeping / Art-14 oversight evidence).
Honest: real Ed25519 if `cryptography` is present; else raises (never fabricates a signature).
"""
import os, base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

OUT = os.path.dirname(os.path.abspath(__file__))
PRIV = os.path.join(OUT, ".town_priv.key")     # gitignored
PUB  = os.path.join(OUT, "town_pub.key")        # publishable verifier key

def _raw(k, kind):
    if kind == "priv":
        return k.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                               serialization.NoEncryption())
    return k.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)

def load_or_create_key():
    if os.path.exists(PRIV):
        priv = Ed25519PrivateKey.from_private_bytes(base64.b64decode(open(PRIV).read().strip()))
    else:
        priv = Ed25519PrivateKey.generate()
        open(PRIV, "w").write(base64.b64encode(_raw(priv, "priv")).decode())
        os.chmod(PRIV, 0o600)
    pub_b64 = base64.b64encode(_raw(priv.public_key(), "pub")).decode()
    open(PUB, "w").write(pub_b64)
    return priv, pub_b64

def sign(priv, message: str) -> str:
    return base64.b64encode(priv.sign(message.encode())).decode()

def verify(pub_b64: str, message: str, sig_b64: str) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64)).verify(
            base64.b64decode(sig_b64), message.encode())
        return True
    except Exception:
        return False
