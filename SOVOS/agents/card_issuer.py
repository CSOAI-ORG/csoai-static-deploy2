#!/usr/bin/env python3
"""card_issuer.py — CSOAI signed-card issuance leg. Real Ed25519, not hash theater.

The missing e2e leg: measurement artifacts (board runs, fix-loop verdicts) become
signed ~3KB cards that land in the MinIO signed-cards bucket and the repo.

Doctrine:
  - Cards are signed with the estate Ed25519 key (keystone `meok-keystone` /
    account `CSOAI_ED25519_SK` on macOS, or env CSOAI_ED25519_SK as 64-hex seed).
  - Sign → verify roundtrip MUST pass before anything is written (probe-the-probe).
  - The public key is published in-repo so any third party can verify cards.
  - A card over 3KB is a design smell: keep the payload a summary, hash the bulk.

Usage:
  python3 card_issuer.py issue --report path/report.json --kind fix-loop-verdict \
      [--adapter path/adapter_model.safetensors] [--out DIR] [--minio /runpod/sovos-master]
  python3 card_issuer.py verify --card path/card.json
  python3 card_issuer.py pubkey            # print/publish the estate public key
"""
from __future__ import annotations
import argparse, base64, hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

ISSUER_DID = "did:csoai:issuer-001"
CARD_SCHEMA = "csoai.signed-card/1.0"
SIZE_BUDGET = 3072  # the 3KB doctrine


def _load_seed() -> bytes:
    hexseed = os.environ.get("CSOAI_ED25519_SK", "").strip()
    if not hexseed:
        try:
            hexseed = subprocess.run(
                ["security", "find-generic-password", "-s", "meok-keystone",
                 "-a", "CSOAI_ED25519_SK", "-w"],
                capture_output=True, text=True, check=True).stdout.strip()
        except Exception:
            pass
    if not hexseed or len(hexseed) != 64:
        sys.exit("card_issuer: no Ed25519 seed (env CSOAI_ED25519_SK or keystone account)")
    return bytes.fromhex(hexseed)


def _keypair():
    sk = Ed25519PrivateKey.from_private_bytes(_load_seed())
    pk = sk.public_key()
    return sk, pk


def pubkey_b64() -> str:
    _, pk = _keypair()
    return base64.b64encode(pk.public_bytes(Encoding.Raw, PublicFormat.Raw)).decode()


def kid() -> str:
    return "ed25519:" + hashlib.sha256(base64.b64decode(pubkey_b64())).hexdigest()[:16]


def _sha256_file(p: Path) -> str | None:
    if not p or not p.exists():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode()


def build_payload(report_path: Path, kind: str, adapter_path: Path | None) -> dict:
    report = json.loads(report_path.read_text())
    measurement = {k: report.get(k) for k in (
        "mean_before", "mean_after", "delta_pts", "verdict",
        "n_failures_trained", "iters", "per_axis_before", "per_axis_after")
        if report.get(k) is not None}
    payload = {
        "schema": CARD_SCHEMA,
        "kind": kind,
        "issuer": ISSUER_DID,
        "issued_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "subject": {"base": report.get("base"), "run": report.get("at"),
                    "axes": report.get("axes")},
        "measurement": measurement,
        "provenance": {
            "report_sha256": _sha256_file(report_path),
            "adapter_sha256": _sha256_file(adapter_path) if adapter_path else None,
        },
    }
    payload["card_id"] = hashlib.sha256(_canonical(payload)).hexdigest()[:16]
    return payload


def issue(report: str, kind: str, adapter: str | None, out: str | None,
          minio: str | None) -> int:
    report_path = Path(report)
    payload = build_payload(report_path, kind, Path(adapter) if adapter else None)

    sk, pk = _keypair()
    sig = sk.sign(_canonical(payload))
    pk_b64 = base64.b64encode(
        pk.public_bytes(Encoding.Raw, PublicFormat.Raw)).decode()
    card = dict(payload)
    card["signature"] = {"alg": "Ed25519", "kid": kid(),
                         "pubkey": pk_b64, "sig": base64.b64encode(sig).decode()}

    # probe-the-probe: verify before anything is written
    if not _verify_obj(card):
        sys.exit("card_issuer: self-verification FAILED — nothing written (gate held)")

    blob = json.dumps(card, indent=1, ensure_ascii=False)
    size = len(blob.encode())
    if size > SIZE_BUDGET:
        print(f"warning: card is {size}B > {SIZE_BUDGET}B budget — "
              "summary only, bulk stays hash-referenced", file=sys.stderr)

    outdir = Path(out) if out else Path("artifacts/signed-cards") / kind
    outdir.mkdir(parents=True, exist_ok=True)
    card_path = outdir / f"{payload['card_id']}.json"
    card_path.write_text(blob + "\n")

    if minio:
        dst = Path(minio) / "signed-cards" / kind
        dst.mkdir(parents=True, exist_ok=True)
        (dst / card_path.name).write_text(blob + "\n")

    print(json.dumps({"card": str(card_path), "card_id": payload["card_id"],
                      "bytes": size, "verified": True,
                      "minio": str(minio) if minio else None}, indent=1))
    return 0


def _verify_obj(card: dict) -> bool:
    try:
        sig = card["signature"]
        payload = {k: v for k, v in card.items() if k != "signature"}
        pk = Ed25519PublicKey.from_public_bytes(base64.b64decode(sig["pubkey"]))
        pk.verify(base64.b64decode(sig["sig"]), _canonical(payload))
        # kid must match the embedded pubkey
        if sig["kid"] != "ed25519:" + hashlib.sha256(
                base64.b64decode(sig["pubkey"])).hexdigest()[:16]:
            return False
        # identity field: card_id (fix-loop cards) or certificate_id (council
        # certificates) — hash of the content WITHOUT the identity field
        # (the signature above covers the payload WITH it, so it can't be swapped)
        id_field = next((f for f in ("card_id", "certificate_id") if f in payload),
                        None)
        if id_field is None:
            return False
        content = {k: v for k, v in payload.items() if k != id_field}
        return payload[id_field] == hashlib.sha256(
            _canonical(content)).hexdigest()[:16]
    except Exception:
        return False


def verify(card: str) -> int:
    obj = json.loads(Path(card).read_text())
    ok = _verify_obj(obj)
    print(json.dumps({"card": card,
                      "card_id": obj.get("card_id") or obj.get("certificate_id"),
                      "valid": ok}, indent=1))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="CSOAI signed-card issuer (Ed25519)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("issue")
    i.add_argument("--report", required=True)
    i.add_argument("--kind", required=True)
    i.add_argument("--adapter")
    i.add_argument("--out")
    i.add_argument("--minio")
    v = sub.add_parser("verify")
    v.add_argument("--card", required=True)
    sub.add_parser("pubkey")
    a = ap.parse_args()
    if a.cmd == "issue":
        return issue(a.report, a.kind, a.adapter, a.out, a.minio)
    if a.cmd == "verify":
        return verify(a.card)
    print(json.dumps({"alg": "Ed25519", "kid": kid(), "pubkey_b64": pubkey_b64(),
                      "did": ISSUER_DID}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
