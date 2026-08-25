"""signature_alg — Continuity white-space grader (P5).

Deterministic predicate: every signed record must name its algorithm so a
verifier need not assume Ed25519. Extracted from deploy2 pqcbench.py
alg_agility criterion; portable for pack selftests without RunPod.

This does NOT mint board scores or DOIs. Board Continuity is already MEASURED
via a separate PQCBench fleet path. This closes the instrument-spine gap.
"""
from __future__ import annotations

from typing import Any

ALG_KEYS = {"alg", "algorithm", "sig_alg", "signature_algorithm", "sigAlg", "crv", "kty"}
SIG_KEYS = ("sig", "signature")


class Unmeasured(Exception):
    """Artefact cannot answer the criterion (distinct from fail)."""


def _is_signed(record: dict[str, Any]) -> bool:
    return any(k in record for k in SIG_KEYS)


def signature_alg(
    records: list[dict[str, Any]] | dict[str, Any],
    *,
    expected_decl: str | None = None,
) -> dict[str, Any]:
    """Grade algorithm naming on signed records.

    Returns:
      status: UNMEASURED | PASS | FAIL
      detail: human-readable
      named / signed counts
      expected_decl_match: optional check that named algs include expected_decl
    """
    if isinstance(records, dict):
        records = [records]
    if not records:
        raise Unmeasured("no records")

    signed = [r for r in records if isinstance(r, dict) and _is_signed(r)]
    if not signed:
        return {
            "status": "UNMEASURED",
            "pass": False,
            "detail": "no signed records — cannot answer signature_alg",
            "named": 0,
            "signed": 0,
            "expected_decl_match": None,
        }

    named_recs = [r for r in signed if ALG_KEYS & set(r.keys())]
    ok = len(named_recs) == len(signed)
    detail = f"{len(named_recs)}/{len(signed)} signed records name an algorithm"

    decl_match: bool | None = None
    if expected_decl is not None:
        decl_l = expected_decl.lower()
        found = []
        for r in named_recs:
            for k in ALG_KEYS:
                if k in r and str(r[k]).lower() == decl_l:
                    found.append(r)
                    break
                if k in r and decl_l in str(r[k]).lower():
                    found.append(r)
                    break
        decl_match = len(found) == len(signed) and ok
        if not decl_match:
            detail += f"; expected_decl={expected_decl!r} not on every signed record"
            ok = False

    return {
        "status": "PASS" if ok else "FAIL",
        "pass": ok,
        "detail": detail,
        "named": len(named_recs),
        "signed": len(signed),
        "expected_decl_match": decl_match,
    }


def selftest() -> int:
    fails: list[str] = []

    # Unsigned → UNMEASURED
    r = signature_alg([{"payload": "x"}])
    if r["status"] != "UNMEASURED":
        fails.append("unsigned should be UNMEASURED")

    # Signed, no alg → FAIL
    r = signature_alg([{"payload": "x", "sig": "ab" * 32}])
    if r["pass"] or r["status"] != "FAIL":
        fails.append("signed without alg should FAIL")

    # Signed with alg → PASS
    r = signature_alg([{"payload": "x", "sig": "ab" * 32, "alg": "Ed25519"}])
    if not r["pass"]:
        fails.append("signed with alg should PASS")

    # Partial labelling → FAIL
    r = signature_alg(
        [
            {"sig": "aa", "alg": "Ed25519"},
            {"sig": "bb"},
        ]
    )
    if r["pass"]:
        fails.append("partially labelled chain should FAIL")

    # expected_decl mismatch → FAIL
    r = signature_alg(
        [{"sig": "aa", "algorithm": "Ed25519"}],
        expected_decl="ML-DSA-65",
    )
    if r["pass"] or r["expected_decl_match"] is not False:
        fails.append("expected_decl mismatch should FAIL")

    # expected_decl match → PASS
    r = signature_alg(
        [{"sig": "aa", "signature_algorithm": "Ed25519"}],
        expected_decl="Ed25519",
    )
    if not r["pass"] or r["expected_decl_match"] is not True:
        fails.append("expected_decl match should PASS")

    for f in fails:
        print(f"  FAIL {f}")
    print(f"  {'PASS signature_alg selftest' if not fails else f'{len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest())
