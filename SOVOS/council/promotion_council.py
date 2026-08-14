#!/usr/bin/env python3
"""promotion_council.py — BFT promotion council for the CSOAI flywheel.

Collects voter verdicts (hash-committed at source), checks the quorum rule,
and — only on CERTIFIED — issues an Ed25519-signed promotion certificate into
signed-cards/council/ (repo + optionally MinIO).

Quorum rule (3-voter council, trusted collector — see QUORUM_NEEDED note):
  CERTIFIED  iff PROMOTE votes >= 2 AND PROMOTE > REVERT
  REJECTED   otherwise (the certificate still issues — a signed REJECTED is
             the audit trail doing its job)
ABSTAIN (UNMEASURED) voters never count toward quorum — a voter that couldn't
measure is not a vote for anything.

v1 honesty: votes are hash-committed at source (rows_sha256 + voter identity);
signatures are issued at collection from the owner keystone. Per-pod Ed25519
lane identities (did:csoai:lane-*) are the v2 — until then, non-repudiation is
at the collector, not the voter. Stated, not hidden.

  python3 promotion_council.py --votes votes/run1 --candidate-adapter fix_runs/BEST \
      [--minio /runpod/sovos-master] [--out artifacts]
  python3 promotion_council.py --selftest
"""
from __future__ import annotations
import argparse, base64, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "agents"))
from card_issuer import _canonical, _keypair, kid, pubkey_b64  # shared crypto

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

QUORUM_F = 1
# Honest threat model: voters are untrusted producers; the collector (the
# keystone machine) is the trusted tally. With centralized collection there is
# no voter-to-voter network partition, so the classic 3f+1 replica rule does not
# bind: 2-of-3 suffices to outvote 1 faulty OR adversarial voter, provided 2 are
# honest. What this does NOT cover: 2 colluding voters, or a compromised
# collector. A 4th independent voter (roadmap: OpenRouter cross-lab voter) lifts
# this toward distributed-BFT parity.
QUORUM_NEEDED = 2   # of 3 voters


def decide(votes: list[dict]) -> dict:
    counts = {"PROMOTE": 0, "REVERT": 0, "NO_CHANGE": 0, "ABSTAIN": 0}
    for v in votes:
        counts[v.get("vote", "ABSTAIN")] = counts.get(v.get("vote", "ABSTAIN"), 0) + 1
    certified = (counts["PROMOTE"] >= QUORUM_NEEDED
                 and counts["PROMOTE"] > counts["REVERT"])
    return {"decision": "CERTIFIED" if certified else "REJECTED",
            "counts": counts, "quorum_rule": "2-of-3 PROMOTE with PROMOTE>REVERT "
            "certifies; ABSTAIN never counts; trusted collector, untrusted voters"}


def certify(votes_dir: str, adapter: str | None, minio: str | None,
            outdir: str | None) -> int:
    d = Path(votes_dir)
    votes, receipts = [], []
    for vf in sorted(d.rglob("verdict.json")):
        v = json.loads(vf.read_text())
        # receipt: re-check the rows hash if rows are alongside the verdict
        rows_file = vf.parent / "rows.jsonl"
        rows_ok = None
        if rows_file.exists() and v.get("rows_sha256"):
            rows_ok = (hashlib.sha256(rows_file.read_bytes()).hexdigest()
                       == v["rows_sha256"])
        receipts.append({"voter_id": v.get("voter_id"),
                         "implementation": v.get("implementation"),
                         "vote": v.get("vote"),
                         "delta_unseen": v.get("delta_unseen"),
                         "rows_sha256": v.get("rows_sha256"),
                         "rows_hash_verified": rows_ok})
        votes.append(v)
    if not votes:
        sys.exit("promotion_council: no verdict.json found under " + votes_dir)

    decision = decide(votes)
    payload = {
        "schema": "csoai.promotion-certificate/1.0",
        "kind": "council-certificate",
        "issuer": "did:csoai:issuer-001",
        "issued_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "candidate": {"adapter_sha256": hashlib.sha256(
                          (Path(adapter) / "adapter_model.safetensors").read_bytes()
                      ).hexdigest() if adapter and
                      (Path(adapter) / "adapter_model.safetensors").exists() else None},
        "votes": receipts,
        "council": decision,
    }
    payload["certificate_id"] = hashlib.sha256(_canonical(payload)).hexdigest()[:16]

    sk, pk = _keypair()
    sig = sk.sign(_canonical(payload))
    pk_b64 = base64.b64encode(pk.public_bytes(Encoding.Raw, PublicFormat.Raw)).decode()
    cert = dict(payload)
    cert["signature"] = {"alg": "Ed25519", "kid": kid(), "pubkey": pk_b64,
                         "sig": base64.b64encode(sig).decode()}

    # probe-the-probe: verify before write
    check = {k: v for k, v in cert.items() if k != "signature"}
    Ed25519PublicKey.from_public_bytes(base64.b64decode(pk_b64)).verify(
        base64.b64decode(cert["signature"]["sig"]), _canonical(check))
    content = {k: v for k, v in check.items() if k != "certificate_id"}
    assert check["certificate_id"] == hashlib.sha256(
        _canonical(content)).hexdigest()[:16]

    blob = json.dumps(cert, indent=1, ensure_ascii=False) + "\n"
    out = Path(outdir) if outdir else Path("artifacts/signed-cards/council")
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{payload['certificate_id']}.json"
    path.write_text(blob)
    if minio:
        dst = Path(minio) / "signed-cards" / "council"
        dst.mkdir(parents=True, exist_ok=True)
        (dst / path.name).write_text(blob)
    print(json.dumps({"certificate": str(path),
                      "certificate_id": payload["certificate_id"],
                      "decision": decision["decision"],
                      "counts": decision["counts"],
                      "bytes": len(blob.encode())}, indent=1))
    return 0 if decision["decision"] == "CERTIFIED" else 2


def selftest() -> int:
    votes = [
        {"vote": "PROMOTE", "delta_unseen": 0.18},
        {"vote": "PROMOTE", "delta_unseen": 0.12},
        {"vote": "ABSTAIN"},
    ]
    assert decide(votes)["decision"] == "CERTIFIED"
    votes[1]["vote"] = "REVERT"
    assert decide(votes)["decision"] == "REJECTED"
    votes[1]["vote"] = "ABSTAIN"
    assert decide(votes)["decision"] == "REJECTED"  # only 1 PROMOTE < quorum
    votes.append({"vote": "PROMOTE"})
    votes.append({"vote": "PROMOTE"})
    assert decide(votes)["decision"] == "CERTIFIED"  # 3 PROMOTE of 5
    print("promotion_council selftest: PASS (certify/reject/abstain-never-counts)")
    return 0


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--votes", required=True)
    ap.add_argument("--candidate-adapter")
    ap.add_argument("--minio")
    ap.add_argument("--out")
    a = ap.parse_args()
    return certify(a.votes, a.candidate_adapter, a.minio, a.out)


if __name__ == "__main__":
    sys.exit(main())
