#!/usr/bin/env python3
"""verify_via_didweb.py — verify a signed card against the PUBLISHED did:web identity.

This closes the identity half of "verify without trusting us". A verifier does NOT trust the
card's self-reported `signer`; it resolves the CSOAI signing key from the did:web document
(hosted at https://csoai.org/.well-known/did.json — a location only the domain controller can
publish), then checks the card's Ed25519 signature over its `content_id` against THAT key.

Trust model: you trust that the domain csoai.org controls the DID (that is did:web's whole
premise). You do NOT trust CSOAI's word about who signed. Ed25519 today; ML-DSA-65 is roadmap
and is NOT claimed. Full C2PA-trust-list / CA recognition is a separate owner-gated step.

    python3 verify_via_didweb.py --card card.json                # verify a card file
    python3 verify_via_didweb.py --did https://csoai.org/.well-known/did.json --card card.json
    python3 verify_via_didweb.py --selftest
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DID = str(ROOT / ".well-known" / "did.json")

_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def _b58decode(s: str) -> bytes:
    n = 0
    for ch in s:
        n = n * 58 + _B58.index(ch)
    body = n.to_bytes((n.bit_length() + 7) // 8, "big")
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + body


def _load_did(src: str) -> dict:
    if src.startswith("http://") or src.startswith("https://"):
        with urllib.request.urlopen(src, timeout=10) as r:
            return json.loads(r.read())
    return json.loads(Path(src).read_text())


def resolve_ed25519_keys(did_doc: dict) -> list[bytes]:
    """Return every Ed25519 public key (raw 32 bytes) published in the DID document."""
    keys = []
    for vm in did_doc.get("verificationMethod", []):
        jwk = vm.get("publicKeyJwk")
        if jwk and jwk.get("kty") == "OKP" and jwk.get("crv") == "Ed25519":
            x = jwk["x"] + "=" * (-len(jwk["x"]) % 4)
            keys.append(base64.urlsafe_b64decode(x))
        mb = vm.get("publicKeyMultibase")
        if mb and mb.startswith("z"):
            dec = _b58decode(mb[1:])
            if dec[:2] == b"\xed\x01" and len(dec) == 34:      # ed25519-pub multicodec
                keys.append(dec[2:])
    # de-dup
    seen, out = set(), []
    for k in keys:
        if k not in seen:
            seen.add(k); out.append(k)
    return out


def verify_card(card: dict, did_doc: dict) -> dict:
    """Verify the card's signature over its content_id against a key from the DID document."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature

    cid = card.get("content_id")
    sig = card.get("signature")
    if not cid or not sig:
        return {"verified": False, "reason": "card missing content_id or signature"}
    published = resolve_ed25519_keys(did_doc)
    if not published:
        return {"verified": False, "reason": "no Ed25519 key in the DID document"}

    for raw in published:
        try:
            Ed25519PublicKey.from_public_bytes(raw).verify(bytes.fromhex(sig), cid.encode())
            resolved_hex = raw.hex()
            return {
                "verified": True,
                "resolved_signer": resolved_hex,
                "did": did_doc.get("id"),
                # defense-in-depth: does the card's self-reported signer match the published key?
                "card_signer_matches_did": (card.get("signer") == resolved_hex),
                "trust": "domain controls did:web — signer resolved from published DID, not the card",
            }
        except InvalidSignature:
            continue
    return {"verified": False, "reason": "signature does not verify against any published DID key"}


def signer_did(pubkey_hex: str, did_src: str = DEFAULT_DID) -> dict | None:
    """Return the DID that PUBLISHES this Ed25519 pubkey, or None if it isn't published there.
    Honest by construction: an identity is asserted only when the key genuinely resolves."""
    try:
        doc = _load_did(did_src)
        raw = bytes.fromhex(pubkey_hex)
    except Exception:
        return None
    if raw in resolve_ed25519_keys(doc):
        return {"signer_did": doc.get("id"), "verification_method": f"{doc.get('id')}#keys-1"}
    return None


def bind_did(card: dict, did_src: str = DEFAULT_DID) -> dict:
    """Stamp a signed card with its resolvable did:web signer IFF its key is published there.
    Does nothing for demo/unpublished keys — it never asserts an identity that can't be resolved."""
    signer = (card or {}).get("signer")
    if not signer:
        return card
    b = signer_did(signer, did_src)
    if b:
        card["signer_did"] = b["signer_did"]
        card["verification_method"] = b["verification_method"]
        card["verify_hint"] = ("resolve signer via did:web (.well-known/did.json) and verify the "
                               "Ed25519 signature over content_id — do not trust the card's own signer field")
    return card


def _selftest() -> int:
    # Issue a fresh REAL card, then verify it against the published DID (not the card's claim).
    sys.path.insert(0, str(ROOT / "SOVOS" / "packages" / "sovos-city" / "src"))
    import tempfile
    from sovos_city.chain import Chain
    from sovos_city.measure_api import MeasureService

    chain = Chain(str(Path(tempfile.gettempdir()) / "didweb_selftest.jsonl"),
                  key_path=str(Path("~/.sovos/city_ed25519").expanduser()))
    svc = MeasureService(chain, store=Path(tempfile.gettempdir()) / "didweb-jobs")
    body = {"kind": "didweb-selftest", "hello": "world"}
    job = svc.measure(protocol="didweb-selftest", model="selftest", bank_version="v1",
                      axes=["selftest"], run_fn=lambda *a: body)
    card = job.card
    assert card and card.get("signed"), "need a real signed card for the selftest"

    did_doc = _load_did(DEFAULT_DID)
    res = verify_card(card, did_doc)
    print(json.dumps(res, indent=2))
    assert res["verified"] is True, "a valid card MUST verify against the published DID key"
    assert res["card_signer_matches_did"] is True, "the local signer must be the one published in did:web"

    # Tamper: corrupt the signature → must FAIL against the published key.
    bad = dict(card); bad["signature"] = ("0" * 8) + str(card["signature"])[8:]
    assert verify_card(bad, did_doc)["verified"] is False, "tampered signature must not verify"

    # Wrong identity: a DID doc with a different key → must FAIL.
    other = {"id": "did:web:evil.example", "verificationMethod": [
        {"id": "#k", "type": "JsonWebKey2020",
         "publicKeyJwk": {"kty": "OKP", "crv": "Ed25519",
                          "x": base64.urlsafe_b64encode(b"\x01" * 32).rstrip(b"=").decode()}}]}
    assert verify_card(card, other)["verified"] is False, "must not verify against a foreign DID"

    print("\n  ✅ did:web identity verification holds — real card verifies against the PUBLISHED key, "
          "tamper fails, foreign DID fails. Signer identity now resolves without trusting us.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--card"); ap.add_argument("--did", default=DEFAULT_DID)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    elif a.card:
        card = json.loads(Path(a.card).read_text())
        card = card.get("signed_card", card.get("attestation", {}).get("signed_card", card))
        print(json.dumps(verify_card(card, _load_did(a.did)), indent=2))
    else:
        ap.print_help()
