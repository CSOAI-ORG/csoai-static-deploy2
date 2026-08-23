#!/usr/bin/env python3
"""sov_assessor.py — THE MISSING LINK: company evidence → verdict → signed passport.

The estate already had the two ENDS and nothing in between:
  • classify_use_case()  (meok-sovereign-aiact-passport-mcp) — EU AI Act Art 5 / Art 6 / Annex III
    risk tiering from free text. Pure local logic.
  • Ed25519 signing      (meok-sigil/sigil/sign.py) — offline-verifiable attestation.
  • SOV Town arena rules — the framework control sets (EU AI Act, DORA, Solvency II P1/P3, NIST CSF robotics).
This module is the ASSESSOR that joins them: it takes a company's declared evidence, checks it against
the controls required for its risk tier / frameworks, and emits a verdict that the issuer can sign.

HONESTY REGISTER (carried verbatim from the passport package — do not soften):
    "We sign evidence. We do not certify intent."
  This produces an ASSURANCE ATTESTATION OF DECLARED POSTURE — not a legal certification.
  EU AI Act conformity requires a competent authority (not yet constituted). Nothing here is a
  legal determination. Evidence is SELF-DECLARED unless a verifier attaches proof.

Usage:
    python3 sov_assessor.py --demo
    python3 sov_assessor.py --input company.json [--sign]
"""
from __future__ import annotations

import argparse, hashlib, json, os, re, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # ~/clawd
sys.path.insert(0, str(ROOT / "meok-sovereign-aiact-passport-mcp"))
sys.path.insert(0, str(ROOT / "meok-sigil"))

# ── reuse the estate's real classifier (never reimplement) ───────────────────
try:
    from sovereign_aiact_passport.classify import classify_use_case
    _CLASSIFIER = "meok-sovereign-aiact-passport (Art5/Art6/AnnexIII)"
except Exception as e:  # pragma: no cover
    classify_use_case = None
    _CLASSIFIER = f"UNAVAILABLE ({e})"

# ── CONTROL SETS ─────────────────────────────────────────────────────────────
# Loaded from the PUBLISHED, SIGNED reference control-sets in csoai-control-sets/.
#
# These were previously hardcoded here AND duplicated as TypeScript rules in the SOV Town arena.
# The two copies had already diverged (13 arena rules vs 14 assessor controls) — which is exactly
# how a "reference" stops being one. A control-set that differs depending on which tool you ask
# is not a reference, it is two opinions.
#
# One signed JSON file per framework, consumed by: arena · assessor · passport.
# If the signed reference is unavailable, fall back to the built-ins below so the assessor still
# runs — but say so, because silently assessing against an unverified control-set is the failure
# mode this whole exercise exists to prevent.
_REF_DIR = ROOT / "csoai-control-sets" / "control-sets"
CONTROL_SET_SOURCE = "built-in fallback (reference control-sets not found)"


def _load_reference_control_sets() -> dict[str, list[dict]] | None:
    if not _REF_DIR.is_dir():
        return None
    loaded: dict[str, list[dict]] = {}
    for f in sorted(_REF_DIR.glob("*.json")):
        if f.name.endswith(".sig.json"):
            continue
        try:
            doc = json.loads(f.read_text())
            loaded[doc["framework"]] = [
                {
                    "id": c["id"],
                    "req": c["requirement"],
                    "evidence": c["evidence"],
                    "severity": c["severity"],
                    "tiers": c.get("applies_to_tiers", ["*"]),
                    "citation": c.get("citation"),
                }
                for c in doc.get("controls", [])
            ]
        except Exception:
            continue
    return loaded or None


CONTROLS: dict[str, list[dict]] = {
    "EU AI Act": [
        {"id": "aia-human-oversight", "req": "Human oversight over high-risk decisions (Art 14)",
         "evidence": ["human_oversight"], "severity": "high", "tiers": ["high_risk"]},
        {"id": "aia-annex-iv-doc", "req": "Annex IV technical documentation maintained",
         "evidence": ["annex_iv_doc"], "severity": "high", "tiers": ["high_risk"]},
        {"id": "aia-record-keeping", "req": "Automatic logging / record-keeping (Art 12)",
         "evidence": ["logging", "record_keeping"], "severity": "medium", "tiers": ["high_risk"]},
        {"id": "aia-transparency", "req": "Disclose AI interaction to users (Art 50)",
         "evidence": ["ai_disclosure"], "severity": "medium", "tiers": ["high_risk", "limited"]},
    ],
    "Solvency II P1": [
        {"id": "scr-coverage", "req": "Own funds ≥ Solvency Capital Requirement",
         "evidence": ["scr_coverage_ratio"], "severity": "critical", "tiers": ["*"]},
        {"id": "mcr-floor", "req": "Minimum Capital Requirement floor not breached",
         "evidence": ["mcr_ratio"], "severity": "high", "tiers": ["*"]},
        {"id": "internal-model-approval", "req": "Internal model has supervisory approval",
         "evidence": ["internal_model_approval"], "severity": "critical", "tiers": ["*"]},
    ],
    "Solvency II P3": [
        {"id": "sfcr-filed", "req": "Solvency & Financial Condition Report published",
         "evidence": ["sfcr"], "severity": "high", "tiers": ["*"]},
        {"id": "orsa-performed", "req": "Own Risk & Solvency Assessment performed",
         "evidence": ["orsa"], "severity": "medium", "tiers": ["*"]},
    ],
    "NIST CSF 2.0 Robotics": [
        {"id": "csf-govern-autonomy", "req": "GOVERN: autonomy operates under a governance policy",
         "evidence": ["autonomy_policy"], "severity": "high", "tiers": ["*"]},
        {"id": "csf-protect-envelope", "req": "PROTECT: actuation bounded by a safety envelope",
         "evidence": ["safety_envelope"], "severity": "critical", "tiers": ["*"]},
        {"id": "csf-detect-telemetry", "req": "DETECT: anomaly telemetry on sensor pathways",
         "evidence": ["anomaly_telemetry"], "severity": "medium", "tiers": ["*"]},
    ],
    "DORA": [
        {"id": "dora-incident-reporting", "req": "Major ICT incident reporting process",
         "evidence": ["incident_reporting"], "severity": "high", "tiers": ["*"]},
        {"id": "dora-resilience-testing", "req": "Periodic digital operational resilience testing",
         "evidence": ["resilience_test"], "severity": "medium", "tiers": ["*"]},
    ],
}

SEVERITY_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}

# Prefer the published, signed reference over the built-in copy.
_ref = _load_reference_control_sets()
if _ref:
    CONTROLS.update(_ref)
    CONTROL_SET_SOURCE = f"signed reference control-sets ({len(_ref)} frameworks) — {_REF_DIR}"


def _evidence_present(evidence: dict, keys: list[str]) -> tuple[bool, str | None]:
    """A control is met only if an evidence key is present AND truthy.
    Explicitly false / empty / 'no' counts as NOT met — never treat absence as compliance."""
    for k in keys:
        if k in evidence:
            v = evidence[k]
            if isinstance(v, str):
                if v.strip().lower() in {"", "no", "false", "none", "n/a"}:
                    continue
                return True, f"{k}={v}"
            if isinstance(v, bool) and v:
                return True, f"{k}=true"
            if isinstance(v, (int, float)) and v:
                return True, f"{k}={v}"
            if isinstance(v, dict) and v:
                return True, f"{k}={json.dumps(v)[:60]}"
    return False, None


def assess(company: dict) -> dict:
    """company = {name, use_case, frameworks:[...], evidence:{...}}"""
    name = company.get("name", "UNNAMED")
    use_case = company.get("use_case", "")
    frameworks = company.get("frameworks") or ["EU AI Act"]
    evidence = company.get("evidence") or {}

    # 1. risk tier via the estate's real classifier
    if classify_use_case:
        c = classify_use_case(use_case)
        tier, triggers = c.tier, c.triggers
        annex_iv_required = c.annex_iv_required
    else:
        tier, triggers, annex_iv_required = "unknown", ["classifier_unavailable"], False

    # 2. control-by-control assessment
    findings, met, gaps = [], 0, 0
    weighted_total = weighted_met = 0
    for fw in frameworks:
        for ctrl in CONTROLS.get(fw, []):
            # 2026-07-29 — `"*"` means "any KNOWN tier", not "including unknown".
            #
            # A note-taking helper classified as tier=None was returning NON_COMPLIANT with a
            # CRITICAL Article 5 prohibited-practices gap, purely because no evidence was
            # declared. Two errors compounded:
            #   • a control gated on "*" fired against a system we had failed to classify —
            #     a verdict on a path that was never completed;
            #   • Art 5 is a PROHIBITION, not an evidence-bearing control. Nobody supplies
            #     "evidence of not doing social scoring"; absence of evidence is the normal
            #     state for a system that simply does not do the prohibited thing, so
            #     treating it as a gap makes every unremarkable system non-compliant.
            #
            # Applicable / not-applicable / tier-unknown are three states, and only the first
            # may produce a finding.
            if tier in (None, "", "unknown"):
                continue
            applies = "*" in ctrl["tiers"] or tier in ctrl["tiers"]
            if not applies:
                continue
            ok, ev = _evidence_present(evidence, ctrl["evidence"])
            w = SEVERITY_WEIGHT[ctrl["severity"]]
            weighted_total += w
            if ok:
                met += 1; weighted_met += w
            else:
                gaps += 1
            findings.append({"framework": fw, "control": ctrl["id"], "requirement": ctrl["req"],
                             "status": "met" if ok else "gap", "severity": ctrl["severity"],
                             "evidence": ev})

    score = round(weighted_met / weighted_total * 100, 1) if weighted_total else 0.0
    critical_gaps = [f for f in findings if f["status"] == "gap" and f["severity"] == "critical"]

    # 3. verdict — prohibited and critical gaps are hard stops, never averaged away
    if tier == "prohibited":
        verdict, reason = "PROHIBITED", "Article 5 prohibited practice detected — cannot be remediated by controls."
    elif weighted_total == 0:
        # HARD RULE: assessing zero controls is NEVER a pass. The first run of this module
        # returned COMPLIANT_DECLARED with met=0 gap=0 because every control was tier-gated
        # out — a vacuous green. Same false-pass family as the arena's 0-violation run.
        verdict, reason = ("INSUFFICIENT_SCOPE",
                           "No applicable controls were evaluated for this tier/framework combination — "
                           "absence of findings is NOT evidence of compliance. Widen frameworks or "
                           "confirm the risk tier.")
    elif critical_gaps:
        verdict, reason = "NON_COMPLIANT", f"{len(critical_gaps)} critical control gap(s)."
    elif gaps == 0:
        verdict, reason = "COMPLIANT_DECLARED", "All applicable controls have declared evidence."
    elif score >= 70:
        verdict, reason = "PARTIAL", f"{gaps} gap(s); weighted control coverage {score}%."
    else:
        verdict, reason = "NON_COMPLIANT", f"{gaps} gap(s); weighted control coverage {score}%."

    now = datetime.now(timezone.utc)
    body = {
        "subject": name,
        "assessed_at": now.isoformat(),
        "expires_at": (now + timedelta(days=365)).isoformat(),
        "risk_tier": tier,
        "tier_triggers": triggers,
        "annex_iv_required": annex_iv_required,
        "frameworks": frameworks,
        "verdict": verdict,
        "reason": reason,
        "control_coverage_pct": score,
        "controls_met": met,
        "controls_gap": gaps,
        "findings": findings,
        "classifier": _CLASSIFIER,
        "control_set_source": CONTROL_SET_SOURCE,
        "assurance_note": ("Assurance attestation of DECLARED posture. Evidence is self-declared "
                           "unless independently verified. Not a legal certification — EU AI Act "
                           "conformity requires a competent authority. We sign evidence, not intent."),
    }
    body["evidence_digest"] = hashlib.sha256(
        json.dumps(evidence, sort_keys=True, default=str).encode()).hexdigest()
    return body


def sign_verdict(body: dict) -> dict:
    """Ed25519-sign via the estate's sigil layer. Never fabricates a signature:
    with no key it returns alg='unsigned-sha256' and sig=None (integrity, not third-party proof)."""
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(payload).hexdigest()
    seed_b64 = os.environ.get("SIGIL_SIGNING_KEY")
    if not seed_b64:
        return {"alg": "unsigned-sha256", "sig": None, "digest": digest,
                "note": "No SIGIL_SIGNING_KEY set — integrity digest only, NOT third-party verifiable."}
    try:
        import base64
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        from cryptography.hazmat.primitives import serialization
        key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(seed_b64)[:32])
        sig = base64.b64encode(key.sign(payload)).decode()
        pub = base64.b64encode(key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw)).decode()
        return {"alg": "ed25519", "sig": sig, "digest": digest, "public_key": pub}
    except Exception as e:
        return {"alg": "unsigned-sha256", "sig": None, "digest": digest, "error": str(e)}


def issue_passport(company: dict, sign: bool = False) -> dict:
    body = assess(company)
    passport = {"passport_version": "1.0", "issuer": "CSOAI", "body": body}
    if sign:
        passport["attestation"] = sign_verdict(body)
    return passport


DEMOS = [
    {"name": "Acme Lending Ltd", "frameworks": ["EU AI Act"],
     "use_case": "AI system used to evaluate creditworthiness of natural persons for loan applications",
     "evidence": {"human_oversight": True, "annex_iv_doc": True, "logging": True, "ai_disclosure": True}},
    {"name": "Northwind Insurance", "frameworks": ["Solvency II P1", "Solvency II P3"],
     "use_case": "Internal capital model for underwriting portfolio risk",
     "evidence": {"scr_coverage_ratio": 1.62, "mcr_ratio": 2.1, "internal_model_approval": False,
                  "sfcr": True, "orsa": True}},
    {"name": "Helios Robotics", "frameworks": ["NIST CSF 2.0 Robotics"],
     "use_case": "Autonomous warehouse robots operating alongside human staff",
     "evidence": {"autonomy_policy": True, "anomaly_telemetry": True}},
    {"name": "PanoptiCorp", "frameworks": ["EU AI Act"],
     "use_case": "Real-time remote biometric identification of citizens in public spaces for policing",
     "evidence": {"human_oversight": True}},
]


def main():
    ap = argparse.ArgumentParser(description="SOV Assessor — evidence → verdict → signed passport")
    ap.add_argument("--input", help="company JSON file")
    ap.add_argument("--demo", action="store_true", help="run the built-in demo companies")
    ap.add_argument("--sign", action="store_true", help="attach an Ed25519 attestation")
    ap.add_argument("--out", help="write passports to this JSON file")
    a = ap.parse_args()

    companies = DEMOS if a.demo else [json.loads(Path(a.input).read_text())] if a.input else DEMOS
    out = []
    for co in companies:
        p = issue_passport(co, sign=a.sign)
        b = p["body"]
        print("=" * 74)
        print(f"  {b['subject']}")
        print(f"  tier={b['risk_tier']}  triggers={b['tier_triggers']}")
        print(f"  frameworks={', '.join(b['frameworks'])}")
        print(f"  VERDICT: {b['verdict']}  ({b['reason']})")
        print(f"  coverage {b['control_coverage_pct']}%  met={b['controls_met']} gap={b['controls_gap']}")
        for f in b["findings"]:
            if f["status"] == "gap":
                print(f"    ✗ [{f['severity']:8s}] {f['control']}: {f['requirement']}")
        if "attestation" in p:
            at = p["attestation"]
            print(f"  attestation: alg={at['alg']} sig={'present' if at.get('sig') else 'NONE (unsigned)'}")
        out.append(p)
    print("=" * 74)
    if a.out:
        Path(a.out).write_text(json.dumps(out, indent=2)); print(f"  -> {a.out}")


if __name__ == "__main__":
    main()
