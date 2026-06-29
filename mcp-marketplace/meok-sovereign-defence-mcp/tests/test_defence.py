"""Tests for meok-sovereign-defence-mcp."""
import os, sys, importlib.util

# Load sovereign_defence.py via absolute path to avoid the PyPI 'server' name-clash
MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "sovereign_defence.py")
spec = importlib.util.spec_from_file_location("sovereign_defence", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

defence_list_products = mod.defence_list_products
defence_jsp936_audit = mod.defence_jsp936_audit
defence_jsp440_audit = mod.defence_jsp440_audit
defence_attack_vector_check = mod.defence_attack_vector_check
defence_bft_council_consensus = mod.defence_bft_council_consensus
defence_pqc_status = mod.defence_pqc_status
defence_threat_assessment = mod.defence_threat_assessment
defence_sigil_emit = mod.defence_sigil_emit
defence_incident_response = mod.defence_incident_response
defence_posture = mod.defence_posture
VERSION = mod.VERSION
TOOLS = mod.TOOLS


def test_version():
    assert VERSION == "1.0.0"


def test_tools_count():
    assert len(TOOLS) == 10


def test_list_products():
    r = defence_list_products()
    assert r["count"] == 8


def test_jsp936_pass():
    r = defence_jsp936_audit("drone-control", ["sensor", "ml", "ux"])
    assert r["compliant"] is True


def test_jsp440_pass():
    r = defence_jsp440_audit("auth", ["encryption", "auth", "audit", "rate_limit", "secure_coding"])
    assert r["compliant"] is True


def test_jsp440_fail():
    r = defence_jsp440_audit("auth", ["none"])
    assert r["compliant"] is False


def test_attack_vector():
    r = defence_attack_vector_check(1, "PQC-signed")
    assert r["score"] == 100
    assert r["family"] == "LLM01"


def test_attack_vector_invalid():
    r = defence_attack_vector_check(99, "mitigated")
    assert "error" in r


def test_bft_consensus_pass():
    votes = {f"q{i}": "for" for i in range(15)}
    votes["q15"] = "against"
    r = defence_bft_council_consensus("attack-plan-alpha", votes)
    assert r["passed"] is True


def test_bft_consensus_fail():
    votes = {f"q{i}": "against" for i in range(13)}
    votes["q13"] = "for"
    r = defence_bft_council_consensus("plan", votes)
    assert r["passed"] is False


def test_pqc_status():
    r = defence_pqc_status()
    assert r["ml-dsa-65"] == "active"
    assert r["fips-203"] == "active"


def test_threat_assessment_high():
    r = defence_threat_assessment("APT-29", "APT")
    assert r["risk_score"] == 90


def test_threat_assessment_low():
    r = defence_threat_assessment("script-kiddie", "skiddie")
    assert r["risk_score"] == 20


def test_sigil_emit():
    r = defence_sigil_emit("incident-response", {"incident": "K-1"})
    assert len(r["digest"]) == 16
    assert r["alg"] == "ed25519"


def test_incident_response():
    r = defence_incident_response("data_exfiltration", "high")
    assert "jsp936" in r["playbook"]


def test_posture():
    r = defence_posture()
    assert r["sovereign_bond"] == 0.937
    assert r["bft_council_size"] == 21
