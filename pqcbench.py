#!/usr/bin/env python3
"""pqcbench.py — SOV-PQC: does a signing chain survive a post-quantum migration?

═══════════════════════════════════════════════════════════════════════════════
THE AXIS
═══════════════════════════════════════════════════════════════════════════════
The other three axes ask whether a system complies, refuses, or marks. This one asks whether
the *evidence* those answers rest on will still verify after the signature algorithm under it
is withdrawn. That is not hypothetical and the dates are published:

  • NIST IR 8547        — EdDSA/ECDSA **disallowed after 2035**
  • NSA CNSA 2.0        — PQC support expected from **Jan 2027**
  • UK NCSC             — discovery/plan by 2028, full migration by 2035
  • RFC 9964 (May 2026) — registered ML-DSA COSE identifiers **−48 / −49 / −50**
  • C2PA through v2.4   — classical only (ES256 / EdDSA / PS256)

So the primitives exist and are unadopted. Nobody scores who is ready. This does.

WHY IT SCORES US FIRST
The first subject is our own SIGIL J-space chain, and it **fails the first check**: a link is
`{ts, task, decision, reason, emitted, prev, query_id, layer, sig, hash}` — there is no
algorithm identifier anywhere in it. A verifier cannot know which algorithm produced `sig`, so
the chain cannot be migrated incrementally and cannot be verified by anything that does not
already assume Ed25519. Publishing that about ourselves is the point; an axis whose first
result flatters its author is not an axis.

WHAT IT REFUSES TO DO
No composite "PQC score". A chain with perfect algorithm agility and no timestamping is not
"50% ready" — it is ready on one dimension and absent on another, and averaging them invents a
number that describes neither. Every criterion is reported separately, and any criterion that
cannot be checked from the artefact is **UNMEASURED**, never 0.

    python3 pqcbench.py [--selftest]
"""
from __future__ import annotations

import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ── The criteria. Each is a deterministic predicate over an artefact. ──────────────────────
# Deliberately NOT weighted and NOT summed — see the module docstring.
CRITERIA = [
    ("alg_agility",  "Every signed record names its algorithm, so a verifier need not assume one"),
    ("hybrid_ready", "The format can carry two signatures over one payload (classical + PQC)"),
    ("timestamped",  "An RFC 3161 trusted timestamp proves existence before any future break"),
    ("ts_renewal",   "RFC 4998 evidence-record renewal, so the proof outlives its own algorithm"),
    ("pqc_option",   "A PQC algorithm is present or selectable (ML-DSA, COSE −48/−49/−50)"),
]

# COSE identifiers registered by RFC 9964 (May 2026) for ML-DSA.
ML_DSA_COSE = {-48: "ML-DSA-44", -49: "ML-DSA-65", -50: "ML-DSA-87"}
# Names a chain might use instead of the COSE integer.
PQC_NAMES = re.compile(r"\b(ml[-_ ]?dsa|dilithium|falcon|sphincs|slh[-_ ]?dsa|ml[-_ ]?kem|kyber)\b", re.I)
# Algorithm-identifier field names in common use across COSE/JOSE/C2PA/ad-hoc chains.
ALG_KEYS = {"alg", "algorithm", "sig_alg", "signature_algorithm", "sigAlg", "crv", "kty"}
TS_KEYS = {"timestamp_token", "tst", "rfc3161", "tsa", "timeStampToken", "signature_time"}
RENEWAL_KEYS = {"evidence_record", "ers", "rfc4998", "archive_timestamp", "renewal"}


class Unmeasured(Exception):
    """The artefact cannot answer this criterion. Distinct from answering 'no'."""


def _keys_deep(o, acc=None):
    acc = acc if acc is not None else set()
    if isinstance(o, dict):
        for k, v in o.items():
            acc.add(k); _keys_deep(v, acc)
    elif isinstance(o, list):
        for v in o: _keys_deep(v, acc)
    return acc


def check_jsonl_chain(p: Path) -> dict:
    """Score a hash-linked JSONL chain (our SIGIL/J-space format)."""
    if not p.exists():
        raise Unmeasured(f"{p.name} not present")
    recs = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line:
            try: recs.append(json.loads(line))
            except json.JSONDecodeError: pass
    if not recs:
        raise Unmeasured(f"{p.name} has no parseable records")

    signed = [r for r in recs if any(k in r for k in ("sig", "signature"))]
    if not signed:
        raise Unmeasured(f"{p.name} contains no signed records")

    keys = _keys_deep(recs)
    blob = json.dumps(recs)

    # alg_agility: EVERY signed record must name its algorithm. Not "the format could" —
    # every record, because a chain migrates link by link and an unlabelled link is a stop.
    named = sum(1 for r in signed if ALG_KEYS & set(r.keys()))
    alg = {"pass": named == len(signed), "detail": f"{named}/{len(signed)} signed records name an algorithm"}

    # hybrid_ready: is there room for a second signature over the same payload? A scalar
    # `sig` string cannot hold two, so the answer is structural, not aspirational.
    multi = sum(1 for r in signed if isinstance(r.get("sig") or r.get("signature"), (list, dict)))
    hyb = {"pass": multi == len(signed) and len(signed) > 0,
           "detail": (f"{multi}/{len(signed)} carry a container signature field; a scalar "
                      f"string cannot hold a second signature")}

    ts = {"pass": bool(TS_KEYS & keys),
          "detail": "no RFC 3161 token field found" if not (TS_KEYS & keys)
                    else f"found {sorted(TS_KEYS & keys)}"}
    ren = {"pass": bool(RENEWAL_KEYS & keys),
           "detail": "no RFC 4998 evidence-record field found" if not (RENEWAL_KEYS & keys)
                     else f"found {sorted(RENEWAL_KEYS & keys)}"}
    pqc = {"pass": bool(PQC_NAMES.search(blob)),
           "detail": "no PQC algorithm named anywhere in the chain" if not PQC_NAMES.search(blob)
                     else "PQC algorithm named"}

    return {"alg_agility": alg, "hybrid_ready": hyb, "timestamped": ts,
            "ts_renewal": ren, "pqc_option": pqc,
            "records": len(recs), "signed_records": len(signed)}


def check_c2pa() -> dict:
    """Score the C2PA manifest our own generator emits.

    C2PA is scored on what the SPEC permits and what OUR manifest actually uses — they differ,
    and conflating them is how a format's roadmap gets reported as a product's readiness.
    """
    art = HERE / "benchmark-results" / "c2pa_selftest.json"
    if not art.exists():
        raise Unmeasured("c2pa_selftest.json not present — run c2pa_manifest.py --selftest")
    d = json.loads(art.read_text())
    blob = json.dumps(d)
    keys = _keys_deep(d)

    alg_named = bool(ALG_KEYS & keys) or "Ed25519" in blob or "ed25519" in blob
    return {
        "alg_agility": {"pass": alg_named,
                        "detail": "COSE header carries an alg identifier" if alg_named
                                  else "no algorithm identifier in the manifest artefact"},
        # C2PA v2.4 defines exactly one claim signature per claim.
        "hybrid_ready": {"pass": False,
                         "detail": "C2PA ≤v2.4 defines ONE claim signature per claim — no "
                                   "hybrid slot exists in the spec, independent of our usage"},
        "timestamped": {"pass": "timestamp" in blob.lower() or "tst" in blob.lower(),
                        "detail": "RFC 3161 timestamping is supported by C2PA; our selftest "
                                  "falls back to untimestamped when no TSA is reachable"},
        "ts_renewal": {"pass": False,
                       "detail": "no RFC 4998 evidence-record renewal in C2PA ≤v2.4"},
        "pqc_option": {"pass": bool(PQC_NAMES.search(blob)),
                       "detail": "C2PA ≤v2.4 permits ES256/EdDSA/PS256 only — all classical. "
                                 "RFC 9964 registered ML-DSA COSE −48/−49/−50 in May 2026 but "
                                 "C2PA has not adopted them"},
        "records": 1, "signed_records": 1,
    }


SUBJECTS = [
    ("SIGIL J-space chain",      lambda: check_jsonl_chain(Path.home() / ".sov_jspace.chain.jsonl")),
    ("SOV33 sovereign chain",    lambda: check_jsonl_chain(Path.home() / ".sov33_local_sovereign.chain.jsonl")),
    ("SOV33 composition chain",  lambda: check_jsonl_chain(Path.home() / ".sov33_composition.chain.jsonl")),
    ("MEOK SOV33 chain",         lambda: check_jsonl_chain(Path.home() / ".meok_sov33_local.chain.jsonl")),
    ("C2PA manifest (ours)",     check_c2pa),
]


def main() -> int:
    rows, unmeasured = [], []
    for name, fn in SUBJECTS:
        try:
            rows.append((name, fn()))
        except Unmeasured as e:
            unmeasured.append((name, str(e)))

    print(f"  SOV-PQC — post-quantum readiness of signing chains\n")
    print(f"  {len(rows)} subjects measured · {len(unmeasured)} UNMEASURED\n")
    hdr = f"    {'subject':<26}" + "".join(f"{k[:11]:>13}" for k, _ in CRITERIA)
    print(hdr); print("    " + "-" * (len(hdr) - 4))
    for name, r in rows:
        line = f"    {name:<26}"
        for k, _ in CRITERIA:
            line += f"{('PASS' if r[k]['pass'] else 'FAIL'):>13}"
        print(line)
    for name, why in unmeasured:
        print(f"    {name:<26}{'UNMEASURED — ' + why:>65}")

    print("\n    WHY EACH FAILURE, IN THE ARTEFACT'S OWN TERMS")
    for name, r in rows:
        fails = [(k, r[k]["detail"]) for k, _ in CRITERIA if not r[k]["pass"]]
        if not fails:
            print(f"      {name}: no failures"); continue
        print(f"      {name}")
        for k, d in fails:
            print(f"        {k:<14} {d}")

    # Per-criterion tally across subjects. NOT a score — a count, with the denominator visible.
    print("\n    PER-CRITERION — how many subjects pass (denominator is what was measurable)")
    tally = {}
    for k, desc in CRITERIA:
        p = sum(1 for _, r in rows if r[k]["pass"])
        tally[k] = {"pass": p, "of": len(rows), "criterion": desc}
        print(f"      {k:<14} {p}/{len(rows)}   {desc}")

    print("\n    NO COMPOSITE SCORE IS EMITTED. A chain with perfect algorithm agility and no")
    print("    timestamping is not '50% ready' — averaging those invents a number describing")
    print("    neither. The five columns are the result.")

    out = {"benchmark": "SOV-PQC", "criteria": {k: d for k, d in CRITERIA},
           "subjects_measured": len(rows), "subjects_unmeasured":
               [{"subject": n, "reason": w} for n, w in unmeasured],
           "results": {n: r for n, r in rows}, "per_criterion": tally,
           "composite_score": "REFUSED BY DESIGN — see module docstring",
           "standards": {"NIST_IR_8547": "EdDSA/ECDSA disallowed after 2035",
                         "NSA_CNSA_2.0": "PQC support expected from Jan 2027",
                         "RFC_9964": "ML-DSA COSE identifiers -48/-49/-50, May 2026",
                         "C2PA_v2.4": "ES256/EdDSA/PS256 only — classical"}}
    from anchored_write import write_result
    p = write_result("pqcbench.json", out)
    print(f"\n    -> {p}")
    return 0


def selftest() -> int:
    import tempfile
    fails = []

    def chain(recs):
        f = Path(tempfile.mktemp(suffix=".jsonl"))
        f.write_text("\n".join(json.dumps(r) for r in recs))
        return f

    # A chain with no signed records is UNMEASURED, not a failing chain. Scoring an unsigned
    # log 0/5 would put it below a signed chain that merely lacks agility, which is backwards.
    try:
        check_jsonl_chain(chain([{"ts": "x", "task": "y"}])); fails.append("unsigned chain not UNMEASURED")
    except Unmeasured:
        pass

    # A missing file is UNMEASURED, never a failure.
    try:
        check_jsonl_chain(Path("/nonexistent/never.jsonl")); fails.append("missing file not UNMEASURED")
    except Unmeasured:
        pass

    # Our real shape: signed, no alg field → alg_agility FAILS. This is the load-bearing case.
    r = check_jsonl_chain(chain([{"sig": "ab", "hash": "cd", "prev": "00"}] * 3))
    if r["alg_agility"]["pass"]: fails.append("chain with no alg field passed alg_agility")
    if r["hybrid_ready"]["pass"]: fails.append("scalar sig field passed hybrid_ready")
    if r["pqc_option"]["pass"]: fails.append("classical-only chain passed pqc_option")

    # A chain that DOES name its algorithm on every signed record must pass.
    r = check_jsonl_chain(chain([{"sig": "ab", "alg": "EdDSA"}] * 3))
    if not r["alg_agility"]["pass"]: fails.append("chain naming EdDSA failed alg_agility")

    # Partial labelling must FAIL — one unlabelled link stops a migration.
    r = check_jsonl_chain(chain([{"sig": "a", "alg": "EdDSA"}, {"sig": "b"}]))
    if r["alg_agility"]["pass"]: fails.append("partially-labelled chain passed alg_agility")

    # A genuinely PQC-ready chain must pass every criterion — otherwise the benchmark can
    # only ever say no, which is not a benchmark.
    good = [{"sig": [{"alg": -8}, {"alg": -48}], "alg": "EdDSA+ML-DSA-44",
             "timestamp_token": "rfc3161…", "evidence_record": "rfc4998…"}] * 2
    r = check_jsonl_chain(chain(good))
    missing = [k for k, _ in CRITERIA if not r[k]["pass"]]
    if missing: fails.append(f"fully-ready chain failed: {missing}")

    # ML-DSA COSE identifiers must be the ones RFC 9964 actually registered.
    if ML_DSA_COSE != {-48: "ML-DSA-44", -49: "ML-DSA-65", -50: "ML-DSA-87"}:
        fails.append("ML-DSA COSE identifiers do not match RFC 9964")

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 8/8' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
