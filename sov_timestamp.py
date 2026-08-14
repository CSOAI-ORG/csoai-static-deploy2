#!/usr/bin/env python3
"""sov_timestamp.py — a REAL time anchor for signed cards, honest about its limits.

The estate charters claimed "OTS Bitcoin proof on 4,721 files". The code had ~1
reference. That is the exact "names promise what code lacks" trap. This replaces
the claim with something true and checkable:

  • RFC-3161 — POST the card's content hash to a public Time-Stamping Authority
    (TSA). The TSA returns a signed token binding {your hash, a trusted time}.
    That is a genuine third-party anchor: you cannot backdate it, and anyone can
    verify the token against the TSA certificate with `openssl ts -verify`.

  • When the TSA is unreachable (offline / sandbox), it returns an HONEST
    unanchored record — `kind="unanchored"`, local time only, explicitly NOT a
    third-party proof. It never dresses a local clock up as an anchor.

What it deliberately does NOT claim: Bitcoin/OpenTimestamps calendar anchoring.
That needs the `opentimestamps` client + calendar round-trips; until that is
wired, saying "Bitcoin proof" is theater. RFC-3161 is the honest, standards-based
anchor we can actually produce today.

    python3 sov_timestamp.py --hash <sha256hex>
    python3 sov_timestamp.py --selftest
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone

# A public, free RFC-3161 TSA. Overridable; never silently trusted beyond "it timestamped".
DEFAULT_TSA = "https://freetsa.org/tsr"
SHA256_OID_DER = bytes.fromhex("0609608648016503040201")  # OID 2.16.840.1.101.3.4.2.1 (TLV)


# ── minimal DER encoder (just enough for a TimeStampReq) ────────────────────────
def _der_len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def _tlv(tag: int, body: bytes) -> bytes:
    return bytes([tag]) + _der_len(len(body)) + body


def _int(n: int) -> bytes:
    b = n.to_bytes(max(1, (n.bit_length() + 8) // 8), "big")
    return _tlv(0x02, b)


def build_tsq(sha256_hex: str, cert_req: bool = True) -> bytes:
    """Build an RFC-3161 TimeStampReq (DER) for a sha256 digest."""
    digest = bytes.fromhex(sha256_hex)
    if len(digest) != 32:
        raise ValueError("expected a 32-byte (64-hex) sha256 digest")
    algid = _tlv(0x30, SHA256_OID_DER + bytes.fromhex("0500"))      # AlgorithmIdentifier + NULL
    imprint = _tlv(0x30, algid + _tlv(0x04, digest))               # MessageImprint
    version = _int(1)
    certreq = _tlv(0x01, b"\xff" if cert_req else b"\x00")          # BOOLEAN
    return _tlv(0x30, version + imprint + certreq)                  # TimeStampReq SEQUENCE


def timestamp_sha256(sha256_hex: str, tsa_url: str = DEFAULT_TSA, timeout: int = 12) -> dict:
    """Anchor a sha256 digest. Returns a dict whose `kind` states honestly what it is:
      kind="rfc3161"    → a real TSA token (base64) you can verify offline later
      kind="unanchored" → TSA unreachable; local time only, NOT a third-party proof
    """
    now = datetime.now(timezone.utc).isoformat()
    try:
        tsq = build_tsq(sha256_hex)
        req = urllib.request.Request(
            tsa_url, data=tsq,
            headers={"Content-Type": "application/timestamp-query",
                     "Content-Length": str(len(tsq))})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            tsr = r.read()
        if not tsr:
            raise ValueError("empty TSA response")
        return {
            "kind": "rfc3161",
            "tsa": tsa_url,
            "digest_sha256": sha256_hex,
            "token_b64": base64.b64encode(tsr).decode(),
            "token_sha256": hashlib.sha256(tsr).hexdigest(),
            "requested_at_utc": now,
            "verify_hint": "openssl ts -reply -in token.tsr -text  (token = base64-decode token_b64)",
        }
    except Exception as e:
        return {
            "kind": "unanchored",
            "digest_sha256": sha256_hex,
            "local_time_utc": now,
            "note": "TSA unreachable — LOCAL TIME ONLY, not a third-party anchor. Do not present as proof.",
            "error": str(e)[:100],
        }


def anchor_for(payload: dict | str, tsa_url: str = DEFAULT_TSA) -> dict:
    """Convenience: sha256 an arbitrary payload (card body / content_id) then anchor it."""
    if isinstance(payload, dict):
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    else:
        raw = str(payload).encode()
    return timestamp_sha256(hashlib.sha256(raw).hexdigest(), tsa_url=tsa_url)


def _selftest() -> int:
    # 1. TSQ encoder is deterministic and structurally valid for a known digest.
    h = "a" * 64
    tsq = build_tsq(h)
    assert tsq[0] == 0x30, "TimeStampReq must be a DER SEQUENCE"
    assert bytes.fromhex(h) in tsq, "digest must be embedded in the request"
    assert SHA256_OID_DER in tsq, "sha256 OID must be present"
    # 2. Offline path is honestly labeled (force failure via an unroutable TSA).
    off = timestamp_sha256(h, tsa_url="http://127.0.0.1:9/nope", timeout=1)
    assert off["kind"] == "unanchored", "unreachable TSA must yield an unanchored record"
    assert "not a third-party" in off["note"].lower(), "must not dress local time as a proof"
    # 3. anchor_for hashes payloads deterministically.
    a1 = anchor_for({"x": 1, "y": 2}, tsa_url="http://127.0.0.1:9/nope")
    a2 = anchor_for({"y": 2, "x": 1}, tsa_url="http://127.0.0.1:9/nope")
    assert a1["digest_sha256"] == a2["digest_sha256"], "canonical hashing must be order-stable"
    print("  ✅ sov_timestamp invariants hold — real TSQ, honest unanchored fallback, stable hashing")
    # 4. Best-effort live probe (never asserted — network may be blocked).
    live = timestamp_sha256(h)
    print(f"  live TSA probe: kind={live['kind']}"
          + (f" · token {len(live['token_b64'])}b from {live['tsa']}" if live["kind"] == "rfc3161"
             else " (offline/blocked — expected in sandbox)"))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", help="sha256 hex digest to anchor")
    ap.add_argument("--tsa", default=DEFAULT_TSA)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    elif a.hash:
        print(json.dumps(timestamp_sha256(a.hash, tsa_url=a.tsa), indent=2))
    else:
        ap.print_help()
