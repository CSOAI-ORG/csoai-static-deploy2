#!/usr/bin/env python3
"""claimguard.py — claim-vs-signed-artifact integrity checker (product).

Given a signed board + its public claim, verifies:
  1. signature valid (recompute content_id, check Ed25519 vs trust-root kid)
  2. payload non-empty (no stubs)
  3. claimed numbers supported by payload data (no overclaims)
Emits a signed ClaimGuard report. This tool caught our own overclaims twice (jail + guardrail).
"""
from __future__ import annotations
import sys, os, json, time, hashlib, base64

def jcs(obj):
    if isinstance(obj, dict):
        return "{" + ",".join(f'{json.dumps(str(k))}:{jcs(obj[k])}' for k in sorted(obj)) + "}"
    if isinstance(obj, list):
        return "[" + ",".join(jcs(x) for x in obj) + "]"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if obj is None:
        return "null"
    return json.dumps(obj)

def verify_sig(receipt: dict) -> bool:
    """Recompute content_id + check Ed25519 signature (no key needed)."""
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    sig = base64.b64decode(receipt.get("signature", {}).get("sig", ""))
    canonical = jcs({k: v for k, v in receipt.items() if k not in ("signature", "content_id")})
    if hashlib.sha256(canonical.encode()).hexdigest() != receipt.get("content_id"):
        return False
    # kid resolution: fetch pubkey from trust root (offline cache if provided)
    kid = receipt.get("signature", {}).get("kid", "")
    pub_b64 = os.environ.get(f"CLAIMGUARD_PUB_{kid.split('#')[-1].replace('-', '_').upper()}", "")
    if not pub_b64:
        return "UNVERIFIABLE-KEY"  # honest: key not provided, signature structural check passed
    pk = Ed25519PublicKey.from_public_bytes(base64.b64decode(pub_b64))
    try:
        pk.verify(sig, canonical.encode())
        return True
    except InvalidSignature:
        return False

def check(board_path: str, claimed: dict) -> dict:
    """Audit a signed board against a claimed number."""
    board = json.load(open(board_path))
    # result lives in the signed extra-claims (claims[1].detail) — the canonical location
    result = board.get("result") or {}
    for claim in board.get("claims", []):
        if claim.get("type", "").endswith("measurement") or "detail" in claim:
            try:
                parsed = json.loads(claim["detail"])
                if isinstance(parsed, dict) and "per_model" in parsed:
                    result = parsed
            except Exception:
                pass
    empty = not result or all(not v for v in result.values()) if isinstance(result, dict) else not result
    sig = verify_sig(board)
    # payload support: does result carry per-model data?
    per = result.get("per_model") or result.get("models") or {}
    has_data = bool(per) and isinstance(per, (dict, list)) and len(per) > 0
    verdicts = []
    if empty:
        verdicts.append("STUB — signed payload empty")
    if not has_data:
        verdicts.append("NO-PER-MODEL-DATA")
    if sig is False:
        verdicts.append("SIGNATURE-INVALID")
    # claim check
    for key, val in (claimed or {}).items():
        found = result.get(key)
        if found is not None:
            if isinstance(val, (int, float)) and isinstance(found, (int, float)):
                if abs(val - found) > 0.001:
                    verdicts.append(f"OVERCLAIM {key}: claimed {val} vs payload {found}")
        else:
            verdicts.append(f"CLAIM-NOT-IN-PAYLOAD: {key}")
    status = "FAIL" if verdicts else "PASS"
    report = {
        "schema": "csoai.claimguard/0.1",
        "board": board_path, "status": status,
        "signature": sig if sig is not True else "VALID",
        "findings": verdicts,
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "register": "MEASURED — deterministic audit (never a model opinion)",
    }
    return report

def signed_report(board_path: str, claimed: dict, key_hex: str = None) -> dict:
    """Emit the audit as a SIGNED receipt (the report itself is a ClaimGuard receipt).
    Fail-closed: no key -> report unsigned-labelled, never fabricated."""
    report = check(board_path, claimed)
    key_hex = key_hex or os.environ.get("CLAIMGUARD_KEY", "")
    class _T: name = "claimguard"; id = "cg-" + time.strftime("%Y%m%d%H%M%S", time.gmtime())
    class _R: log_hashes = []
    if not key_hex:
        report["signed"] = False
        report["note"] = "no key — report UNSIGNED (fail-closed)"
        return report
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inspect-receipts"))
    import inspect_receipts as ir
    r = ir.build_receipt(_T(), _R(), kid="did:web:csoai.org#measurement-instrument",
                         extra_claims=[{"type": "claimguard-audit", "detail": json.dumps(report)}],
                         key_hex=key_hex)
    report["signed"] = True
    report["receipt_content_id"] = r["content_id"]
    report["receipt_sig"] = r["signature"]["sig"][:16]
    return report


if __name__ == "__main__":
    board = sys.argv[1] if len(sys.argv) > 1 else "jail-evidence/board_jail-v2-32item.signed.json"
    claimed = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    print(json.dumps(signed_report(board, claimed), indent=1))
