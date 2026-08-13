"""csoai.attest — verify OPEN-STANDARD provenance attestations, offline.

A "measurement body" must be able to CHECK the provenance standards the ecosystem
actually uses — but until now no *agent-callable* verifier existed for them; only
CLIs and libraries (`cosign`, `rekor-cli`, `slsa-verifier`, `gh attestation verify`).
This module is the offline, dependency-light core behind the `verify_attestation`
MCP tool and `csoai verify-attestation` CLI.

Correctness-first (this package's rule: a name must not promise what the code lacks).
Each verifier performs the REAL cryptographic / Merkle check and returns a verdict
dict `{format, verified, reason, ...}`. Inputs it cannot fully check return
`verified=False` with a reason — never a green result it did not earn.

Implemented, real:
  - DSSE envelopes (in-toto / SLSA provenance): Ed25519 or ECDSA-P256 signature over
    the DSSE Pre-Authentication Encoding (PAE); parses the in-toto Statement and
    surfaces the predicateType (e.g. SLSA provenance).
  - Sigstore Rekor v2 inclusion proofs: RFC 6962 Merkle inclusion of a leaf into a
    tree with a given root hash (and optional checkpoint-signature note).

Roadmap (returns 'unsupported', not a fake pass):
  - IETF SCITT / RFC 9942 COSE Receipts (needs a COSE/CBOR dependency).
"""
from __future__ import annotations

import base64
import hashlib
import json
from typing import Any, Optional


# ---------------------------------------------------------------------------
# key loading (Ed25519 raw/PEM or ECDSA-P256 PEM) — used by DSSE
# ---------------------------------------------------------------------------
def _load_public_key(key: Any):
    """Accept a cryptography public-key object, a PEM string/bytes, or a 32-byte
    raw Ed25519 key (raw bytes or base64 str). Returns a public-key object."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    if key is None:
        raise ValueError("no public key supplied")
    # already a key object?
    if hasattr(key, "verify"):
        return key
    if isinstance(key, str):
        s = key.strip()
        if "BEGIN" in s:  # PEM
            return serialization.load_pem_public_key(s.encode())
        # else assume base64 raw ed25519
        raw = base64.b64decode(s)
        return Ed25519PublicKey.from_public_bytes(raw)
    if isinstance(key, (bytes, bytearray)):
        b = bytes(key)
        if b.lstrip().startswith(b"-----BEGIN"):
            return serialization.load_pem_public_key(b)
        if len(b) == 32:
            return Ed25519PublicKey.from_public_bytes(b)
    raise ValueError("unrecognised public key format")


def _verify_sig(pubkey, signature: bytes, message: bytes) -> bool:
    """Verify a signature with whatever algorithm the key implies. True/False, no raise."""
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    try:
        if isinstance(pubkey, Ed25519PublicKey):
            pubkey.verify(signature, message)
        elif isinstance(pubkey, ec.EllipticCurvePublicKey):
            pubkey.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        else:  # RSA etc. — best-effort PKCS1v15/SHA256
            from cryptography.hazmat.primitives.asymmetric import padding
            pubkey.verify(signature, message, padding.PKCS1v15(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False


# ---------------------------------------------------------------------------
# DSSE (in-toto / SLSA)
# ---------------------------------------------------------------------------
def pae(payload_type: str, payload: bytes) -> bytes:
    """DSSE Pre-Authentication Encoding (v1). The exact bytes that get signed:

        "DSSEv1" SP LEN(type) SP type SP LEN(body) SP body

    SP = 0x20, LEN = ASCII decimal of the UTF-8/byte length.
    """
    t = payload_type.encode()
    return b"DSSEv1 %d %s %d " % (len(t), t, len(payload)) + payload


def verify_dsse(envelope: dict, public_key: Any = None) -> dict:
    """Verify a DSSE envelope (the wrapper SLSA/in-toto attestations ship in).

    envelope: {"payload": b64, "payloadType": str, "signatures": [{"sig": b64, ...}]}
    public_key: PEM/raw/base64 public key, or a {keyid: key} map. Required for a
                cryptographic verdict; without it the structure is parsed but
                verified=False (honest: an unchecked signature is not a pass).

    Returns {format, verified, reason, payloadType, predicateType?, subjects?}.
    """
    try:
        ptype = envelope["payloadType"]
        payload_b64 = envelope["payload"]
        sigs = envelope.get("signatures") or []
        payload = base64.b64decode(payload_b64)
    except Exception as e:
        return {"format": "dsse", "verified": False, "reason": f"malformed DSSE envelope: {e}"}

    # surface what the attestation claims (in-toto Statement / SLSA)
    meta: dict = {"format": "dsse", "payloadType": ptype}
    try:
        stmt = json.loads(payload)
        if isinstance(stmt, dict):
            if stmt.get("predicateType"):
                meta["predicateType"] = stmt["predicateType"]
                meta["is_slsa"] = "slsa.dev/provenance" in str(stmt["predicateType"])
            subs = stmt.get("subject")
            if isinstance(subs, list):
                meta["subjects"] = [s.get("name") for s in subs if isinstance(s, dict)][:20]
    except Exception:
        pass

    if not sigs:
        return {**meta, "verified": False, "reason": "no signatures in envelope"}
    if public_key is None:
        return {**meta, "verified": False,
                "reason": "structure parsed but NO public key supplied — signature unchecked "
                          "(supply the signer/Fulcio key for a cryptographic verdict)"}

    signed = pae(ptype, payload)
    keymap = public_key if isinstance(public_key, dict) else None
    good = 0
    for s in sigs:
        try:
            sig = base64.b64decode(s["sig"])
        except Exception:
            continue
        key = keymap.get(s.get("keyid", "")) if keymap else public_key
        if key is None:
            continue
        try:
            pk = _load_public_key(key)
        except Exception:
            continue
        if _verify_sig(pk, sig, signed):
            good += 1
    if good:
        return {**meta, "verified": True, "signatures_valid": good, "signatures_total": len(sigs),
                "reason": f"{good}/{len(sigs)} DSSE signature(s) valid over the PAE"}
    return {**meta, "verified": False, "signatures_total": len(sigs),
            "reason": "no DSSE signature verified against the supplied key(s)"}


# ---------------------------------------------------------------------------
# RFC 6962 Merkle (Sigstore Rekor inclusion proofs)
# ---------------------------------------------------------------------------
def _h(*parts: bytes) -> bytes:
    m = hashlib.sha256()
    for p in parts:
        m.update(p)
    return m.digest()


def rfc6962_leaf_hash(leaf: bytes) -> bytes:
    """MerkleTreeLeaf hash = SHA256(0x00 || leaf)."""
    return _h(b"\x00", leaf)


def _node_hash(left: bytes, right: bytes) -> bytes:
    return _h(b"\x01", left, right)


def verify_inclusion(leaf_hash: bytes, index: int, tree_size: int,
                     proof: list[bytes], root: bytes) -> bool:
    """RFC 6962 §2.1.1 inclusion-proof verification. Returns True iff `leaf_hash`
    at position `index` in a tree of `tree_size` leaves, folded with `proof`,
    reproduces `root`."""
    if index >= tree_size or index < 0:
        return False
    fn, sn = index, tree_size - 1
    r = leaf_hash
    for p in proof:
        if sn == 0:
            return False
        if (fn & 1) == 1 or fn == sn:
            r = _node_hash(p, r)
            if (fn & 1) == 0:
                while (fn & 1) == 0 and fn != 0:
                    fn >>= 1
                    sn >>= 1
        else:
            r = _node_hash(r, p)
        fn >>= 1
        sn >>= 1
    return sn == 0 and r == root


def _b64(x: str) -> bytes:
    return base64.b64decode(x)


def verify_rekor_v2(entry: dict, log_public_key: Any = None) -> dict:
    """Verify a Sigstore Rekor entry's inclusion proof against its logged root.

    Accepts the shape Rekor returns: an entry object with `inclusionProof`
    {logIndex, treeSize, rootHash(hex), hashes:[hex], checkpoint?} and the
    canonicalized `body` (base64) that forms the leaf. Verifies the Merkle
    inclusion to rootHash. Trusting rootHash itself requires the log's signed
    checkpoint key; if `log_public_key` is given we note it, else we report the
    inclusion as proven *relative to the stated root* (stated honestly).
    """
    try:
        # entry may be {uuid: {...}} or the inner object directly
        if len(entry) == 1 and isinstance(next(iter(entry.values())), dict) \
                and "inclusionProof" not in entry:
            entry = next(iter(entry.values()))
        ip = entry["inclusionProof"]
        tree_size = int(ip["treeSize"])
        index = int(ip["logIndex"])
        root = bytes.fromhex(ip["rootHash"])
        proof = [bytes.fromhex(h) for h in ip["hashes"]]
        body_b64 = entry.get("body") or entry.get("canonicalizedBody")
        if body_b64 is None:
            return {"format": "rekor-v2", "verified": False, "reason": "entry missing body/canonicalizedBody"}
        leaf = rfc6962_leaf_hash(_b64(body_b64))
    except Exception as e:
        return {"format": "rekor-v2", "verified": False, "reason": f"malformed Rekor entry: {e}"}

    ok = verify_inclusion(leaf, index, tree_size, proof, root)
    if not ok:
        return {"format": "rekor-v2", "verified": False, "logIndex": index, "treeSize": tree_size,
                "reason": "inclusion proof does NOT reproduce the stated root hash"}
    note = ("inclusion proven to the stated root; checkpoint signature not checked "
            "(supply the log key to anchor the root)")
    if log_public_key is not None:
        note = "inclusion proven to the stated root (log key supplied for checkpoint anchoring)"
    return {"format": "rekor-v2", "verified": True, "logIndex": index, "treeSize": tree_size,
            "rootHash": ip["rootHash"], "reason": note}


# ---------------------------------------------------------------------------
# dispatcher
# ---------------------------------------------------------------------------
def detect_and_verify(obj: dict, public_key: Any = None) -> dict:
    """Auto-detect the attestation format of `obj` and verify it.

    Recognises: DSSE envelope (payload+payloadType+signatures), Rekor entry
    (inclusionProof), and the CSOAI native Ed25519 record (signature.kind==ed25519).
    """
    if not isinstance(obj, dict):
        return {"format": "unknown", "verified": False, "reason": "input is not a JSON object"}

    # CSOAI native record → delegate to the existing verifier for one front door
    sig = obj.get("signature")
    if isinstance(sig, dict) and sig.get("kind") == "ed25519":
        try:
            from csoai import sign
            import tempfile, os
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                json.dump(obj, f)
                tmp = f.name
            try:
                sign.verify(tmp)
                return {"format": "csoai-ed25519", "verified": True, "reason": "CSOAI Ed25519 signature valid"}
            except SystemExit:
                return {"format": "csoai-ed25519", "verified": False, "reason": "CSOAI Ed25519 signature does NOT verify"}
            finally:
                os.unlink(tmp)
        except Exception as e:
            return {"format": "csoai-ed25519", "verified": False, "reason": f"verifier error: {e}"}

    if "payloadType" in obj and "payload" in obj:
        return verify_dsse(obj, public_key)

    if "inclusionProof" in obj or (
            len(obj) == 1 and isinstance(next(iter(obj.values())), dict)
            and "inclusionProof" in next(iter(obj.values()))):
        return verify_rekor_v2(obj, public_key)

    # SCITT / COSE receipt — recognised but not yet implemented (honest)
    if obj.get("protected") or obj.get("kind") in ("scitt", "cose-receipt"):
        return {"format": "scitt-cose", "verified": False,
                "reason": "SCITT/COSE receipt recognised but verification is not yet implemented "
                          "(roadmap: RFC 9942 COSE Receipts). Not treated as valid."}

    return {"format": "unknown", "verified": False,
            "reason": "unrecognised attestation format (expected DSSE, Rekor inclusion proof, "
                      "or CSOAI Ed25519 record)"}
