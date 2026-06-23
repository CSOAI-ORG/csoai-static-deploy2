#!/usr/bin/env python3
"""
test_forecast_card.py — smoke test for the Attested Compliance Forecast Card (additive).

Proves: build -> sign -> write JSON + HTML -> re-verify the Ed25519 signature with town_pub.key
(public key only, reloaded from disk) -> tamper is detected. Also asserts the honesty guardrails
are present in the signed card. Runs under pytest OR as a plain script.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forecast_card as fc

DEMO_ENTITY = {
    "name": "Acme Bank",
    "facts": [
        "EU-authorised credit institution (in DORA scope).",
        "Public statement: ICT risk policy exists but is not board-approved.",
        "No TLPT / TIBER-EU testing reported.",
    ],
    "consent": "Demo entity; facts caller-supplied (no scraping).",
}
REMEDIATIONS = ["dora_ict_risk_framework", "dora_incident_reporting"]


def test_build_sign_verify_and_tamper(tmp_path=None):
    res = fc.generate(DEMO_ENTITY, "DORA", remediations=REMEDIATIONS, out_prefix="forecast_card_demo")
    signed, paths = res["signed"], res["paths"]

    # signed-at-issuance and re-verified from the in-memory object
    assert res["verified"] is True, "card must verify at issuance"

    # files written
    assert os.path.exists(paths["json"]) and os.path.exists(paths["html"])

    # re-verify with PUBLIC KEY ONLY, reloaded from disk (offline-verifiable / portable)
    on_disk = json.load(open(paths["json"]))
    pub = open(os.path.join(fc.OUT, "town_pub.key")).read().strip()
    assert fc.verify_card(on_disk, pub_b64=pub) is True, "card must re-verify from disk with pub key"

    # genesis-chained as its own short ledger
    assert on_disk["prev"] == fc.GENESIS and on_disk["alg"] == "Ed25519" and on_disk.get("sig")

    # honesty guardrails are present and correctly set
    h = on_disk["honesty"]
    assert h["court_admissible"] is False
    assert h["no_fabricated_precision"] is True
    assert "Ed25519" in h["tamper_evidence"] and "anchor" in h["tamper_evidence"].lower()
    assert "NOT legal advice" in on_disk["scope_disclaimer"]
    assert on_disk["summary"]["model_score_meaning"]  # the score is explained, not bare

    # counterfactual is a dose-response, never a prophecy
    cf = on_disk["counterfactual"]
    assert cf["flagged_after"] <= cf["flagged_before"]

    # tamper test: flipping a field breaks the signature
    tampered = json.loads(json.dumps(on_disk))
    tampered["summary"]["flagged_unmet_or_at_risk"] = 0
    assert fc.verify_card(tampered, pub_b64=pub) is False, "tampering must be detected"


if __name__ == "__main__":
    test_build_sign_verify_and_tamper()
    print("PASS — test_forecast_card smoke test")
