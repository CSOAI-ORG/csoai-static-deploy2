"""spine_v2.py — the SIGNING SPINE.

RFC 8785-style canonical JSON + SHA-256 content addressing + Ed25519 detached signatures.
Supports 5 card kinds: measurement, arena-round, honey-data, provenance, charter.

Authority model:
- Every card has a content hash (CID) = sha256(canonical_json(payload))
- Every card has an Ed25519 signature (detached) over the canonical bytes
- Verification recomputes the CID from the payload and checks sig with public key
- Authority accrues when an external party recomputes a card and gets the same CID

Substrate reality:
- cryptography library for Ed25519 (PyNaCl not always available)
- canonical_json() implements RFC 8785 (sorted keys, UTF-8, no whitespace, number normalisation)
- 5 card kinds defined; new kinds can be registered via register_kind()
"""
from __future__ import annotations
import json
import hashlib
import os
import time
import base64
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

PROTOCOL = "sovereign-spine/2.0"
VERSION = "2.0.0"

# RFC 8785 minimal canonical JSON: sorted keys, no whitespace, UTF-8, no BOM
# Numbers: we keep ints and floats as-is; clients must serialise floats as JSON numbers
# Strings: standard JSON escape (no surrogate pairs)
# Arrays: ordered
# Objects: keys sorted lexicographically by Unicode code point

def canonical_json(payload: Any) -> bytes:
    """RFC 8785-style canonical JSON serialisation.

    Sorts object keys by Unicode code point (codepoint order, not locale).
    No whitespace. UTF-8 encoded. Returns bytes ready to hash/sign.
    """
    if payload is None:
        return b"null"
    if isinstance(payload, bool):
        return b"true" if payload else b"false"
    if isinstance(payload, int):
        return str(payload).encode("utf-8")
    if isinstance(payload, float):
        # JSON spec doesn't distinguish int/float, but RFC 8785 says "use shortest round-trippable"
        if payload != payload:  # NaN
            raise ValueError("NaN not allowed in canonical JSON")
        if payload == float("inf") or payload == float("-inf"):
            raise ValueError("Infinity not allowed in canonical JSON")
        # Round-trip via repr — for sane values this gives shortest form
        return repr(payload).encode("utf-8")
    if isinstance(payload, str):
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if isinstance(payload, (list, tuple)):
        parts = [b"[", canonical_json(payload[0])] if payload else [b"["]
        for item in payload[1:]:
            parts.append(b",")
            parts.append(canonical_json(item))
        parts.append(b"]")
        return b"".join(parts)
    if isinstance(payload, dict):
        # sort keys by codepoint (UTF-8 byte order matches codepoint for BMP; use that)
        items = sorted(payload.items(), key=lambda kv: kv[0])
        parts = [b"{"]
        for i, (k, v) in enumerate(items):
            if i > 0:
                parts.append(b",")
            parts.append(canonical_json(k))
            parts.append(b":")
            parts.append(canonical_json(v))
        parts.append(b"}")
        return b"".join(parts)
    raise TypeError(f"Cannot canonicalise type {type(payload)}")


def content_hash(payload: Any) -> str:
    """Return the content-address (CID-style) for a payload — sha256 of canonical bytes."""
    return "sha256:" + hashlib.sha256(canonical_json(payload)).hexdigest()


# Ed25519 via cryptography library (always available; fallback to hash-sig if no key)

def _load_or_create_keypair(key_path: str = "/tmp/spine_ed25519.key"):
    """Load or create an Ed25519 signing keypair. Stores in PEM at key_path."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            pem = f.read()
        priv = serialization.load_pem_private_key(pem, password=None)
    else:
        priv = Ed25519PrivateKey.generate()
        pem = priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with open(key_path, "wb") as f:
            f.write(pem)
        os.chmod(key_path, 0o600)
    pub = priv.public_key()
    return priv, pub


def _sign(payload_canon: bytes, priv) -> str:
    """Sign canonical bytes with Ed25519 private key. Return base64-encoded sig."""
    sig = priv.sign(payload_canon)
    return base64.b64encode(sig).decode("ascii")


def _verify(payload_canon: bytes, sig_b64: str, pub) -> bool:
    """Verify a base64 Ed25519 sig against canonical bytes."""
    from cryptography.exceptions import InvalidSignature
    try:
        sig = base64.b64decode(sig_b64)
        pub.verify(sig, payload_canon)
        return True
    except (InvalidSignature, Exception):
        return False


def _pub_to_b64(pub) -> str:
    from cryptography.hazmat.primitives import serialization
    raw = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return base64.b64encode(raw).decode("ascii")


# Card kinds registry (5 standard kinds + extensible)
_KINDS: Dict[str, Dict[str, Any]] = {}


def register_kind(name: str, schema: Dict[str, Any], description: str = "") -> dict:
    """Register a new card kind with its required schema. Idempotent."""
    if name in _KINDS:
        return {"kind": name, "status": "already_registered"}
    _KINDS[name] = {"schema": schema, "description": description}
    return {"kind": name, "status": "registered", "schema_keys": list(schema.keys())}


def _ensure_kinds():
    """Lazily register the 5 standard card kinds on first use."""
    if _KINDS:
        return
    # measurement: a measurement result (e.g., Wilson CI, McNemar p)
    register_kind("measurement", {
        "axis": str, "metric": str, "value": (int, float),
        "n": int, "ci95": list, "p_value": (int, float, type(None)),
    }, "A signed measurement result with axis/metric/value/n/CI/p-value.")
    # arena-round: a single arena comparison round (fleet vs fleet or human vs AI)
    register_kind("arena-round", {
        "ts": str, "mode": str, "probe": str,
        "left": dict, "right": dict, "agreement": bool,
    }, "A single arena comparison: probe text, two verdicts, agreement bool.")
    # honey-data: a training pair (input + output + provenance)
    register_kind("honey-data", {
        "ts": str, "kind": str, "input": dict, "output": dict,
        "model": str, "weights_cid": str, "training_eligible": bool,
    }, "A training pair (prompt + response + model + weights CID). Gate 1 closure.")
    # provenance: an attestation (who built what from where)
    register_kind("provenance", {
        "subject_cid": str, "builder": str, "build_instructions": str,
        "inputs": list, "ts": str,
    }, "An in-toto/SLSA-style provenance attestation over a subject CID.")
    # charter: a council decision / vote
    register_kind("charter", {
        "ts": str, "council": str, "decision": str,
        "votes": dict, "quorum_met": bool,
    }, "A council charter: decision text + vote tally + quorum check.")


# Card ledger (in-memory; production would persist to IPFS / Zenodo / pgvector)
_LEDGER: Dict[str, Dict[str, Any]] = {}


def sign_card(kind: str, payload: Dict[str, Any], key_path: Optional[str] = None) -> dict:
    """Sign a card of the given kind with the given payload.

    Returns a signed card with: cid (content hash), sig (base64 Ed25519), pub_key, kind, payload.
    """
    _ensure_kinds()
    if kind not in _KINDS:
        raise ValueError(f"unknown card kind: {kind}")
    # Validate payload has the required schema keys (light check)
    schema = _KINDS[kind]["schema"]
    missing = [k for k in schema if k not in payload]
    if missing:
        raise ValueError(f"missing required keys for kind={kind}: {missing}")
    priv, pub = _load_or_create_keypath(key_path)
    canon = canonical_json(payload)
    cid = "sha256:" + hashlib.sha256(canon).hexdigest()
    sig = _sign(canon, priv)
    pub_b64 = _pub_to_b64(pub)
    ts = datetime.now(timezone.utc).isoformat()
    card = {
        "cid": cid,
        "kind": kind,
        "payload": payload,
        "sig": sig,
        "pub_key": pub_b64,
        "ts": ts,
        "protocol": PROTOCOL,
        "version": VERSION,
    }
    _LEDGER[cid] = card
    return card


def verify_card(card: Dict[str, Any]) -> dict:
    """Verify a signed card. Recomputes CID from payload and checks sig."""
    _ensure_kinds()
    cid = card.get("cid")
    sig = card.get("sig")
    pub_b64 = card.get("pub_key")
    payload = card.get("payload")
    if not (cid and sig and pub_b64 and payload is not None):
        return {"valid": False, "reason": "missing fields"}
    # Recompute CID from payload
    canon = canonical_json(payload)
    expected_cid = "sha256:" + hashlib.sha256(canon).hexdigest()
    if expected_cid != cid:
        return {"valid": False, "reason": "cid_mismatch", "expected": expected_cid, "got": cid}
    # Verify sig
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization
    try:
        pub_bytes = base64.b64decode(pub_b64)
        pub = Ed25519PublicKey.from_public_bytes(pub_bytes)
        if not _verify(canon, sig, pub):
            return {"valid": False, "reason": "sig_invalid"}
    except Exception as e:
        return {"valid": False, "reason": f"key_error: {e}"}
    return {"valid": True, "cid": cid, "kind": card.get("kind")}


def recompute_check(cid: str) -> dict:
    """External-recompute probe: is this CID in the ledger, and does it verify?"""
    card = _LEDGER.get(cid)
    if not card:
        return {"in_ledger": False, "cid": cid}
    v = verify_card(card)
    return {"in_ledger": True, "cid": cid, **v}


def list_kinds() -> dict:
    _ensure_kinds()
    return {"kinds": [{"name": k, "schema_keys": list(v["schema"].keys()), "description": v["description"]} for k, v in _KINDS.items()]}


def list_cards(kind: Optional[str] = None, limit: int = 100) -> dict:
    cards = list(_LEDGER.values())
    if kind:
        cards = [c for c in cards if c.get("kind") == kind]
    cards = cards[-limit:]
    return {"count": len(cards), "total_in_ledger": len(_LEDGER), "cards": [{"cid": c["cid"], "kind": c["kind"], "ts": c["ts"]} for c in cards]}


def _load_or_create_keypath(key_path: Optional[str]) -> tuple:
    if key_path is None:
        key_path = os.environ.get("SPINE_KEY_PATH", "/tmp/spine_ed25519.key")
    return _load_or_create_keypair(key_path)


def main():
    import sys
    print(json.dumps({
        "name": "spine_v2",
        "version": VERSION,
        "protocol": PROTOCOL,
        "operations": [
            {"name": "sign_card", "fn": sign_card},
            {"name": "verify_card", "fn": verify_card},
            {"name": "register_kind", "fn": register_kind},
            {"name": "recompute_check", "fn": recompute_check},
            {"name": "list_kinds", "fn": list_kinds},
            {"name": "list_cards", "fn": list_cards},
            {"name": "canonical_json", "fn": canonical_json},
            {"name": "content_hash", "fn": content_hash},
        ],
    }))


if __name__ == "__main__":
    main()
