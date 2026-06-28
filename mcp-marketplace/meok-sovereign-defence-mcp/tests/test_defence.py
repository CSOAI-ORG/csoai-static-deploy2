"""Tests for meok-sovereign-defence-mcp."""
import os, tempfile
_TEST_DIR = tempfile.mkdtemp(prefix="sov_def_test_")
os.environ["SOV_DEF_KEY"] = os.path.join(_TEST_DIR, "key.pem")
from meok_sovereign_defence_mcp import (
    sov_threat_assess, sov_iwc_calculate, sov_jsp936_audit,
    sov_c2_route, sov_doctrine, DEFENSIVE_DOCTRINE, VERSION, PROTOCOL,
)


def test_threat_assess_low():
    r = sov_threat_assess("Routine perimeter check, no anomalies.")
    assert r["threat_score"] <= 2
    assert r["threat_level"] == "low"


def test_threat_assess_critical():
    r = sov_threat_assess("Critical infrastructure cyber attack with active insider breach")
    assert r["threat_score"] >= 8
    assert r["threat_level"] == "critical"


def test_threat_assess_signed():
    r = sov_threat_assess("test")
    assert "kid" in r and "sig" in r


def test_iwc_calculate_sovereign():
    r = sov_iwc_calculate(100, 90, 85)
    assert r["capacity"] == "sovereign"
    assert r["iwc"] > 0.8


def test_iwc_calculate_exposed():
    r = sov_iwc_calculate(100, 5, 1)
    assert r["capacity"] == "exposed"


def test_iwc_calculate_zero_scans():
    r = sov_iwc_calculate(0, 0, 0)
    assert "error" in r


def test_jsp936_audit_sovereign():
    pillars = {p: {"documented": True, "tested": True, "incident_history": True} for p in DEFENSIVE_DOCTRINE["jsp_936_audit_pillars"]}
    r = sov_jsp936_audit("CSOAI", pillars)
    assert r["assurance_level"] in ("sovereign", "robust")
    assert len(r["scores"]) == 5


def test_jsp936_audit_missing_pillars():
    r = sov_jsp936_audit("Test", {"identify": True})
    assert "error" in r


def test_c2_route_normal():
    r = sov_c2_route("asset-1", "secure-vault", priority="normal", requires_approval=False)
    assert r["route"]["asset_id"] == "asset-1"
    assert r["route"]["approval"] == "auto_approved"
    assert len(r["route"]["hops"]) == 3


def test_c2_route_critical_pending_council():
    r = sov_c2_route("asset-2", "frontline", priority="critical", requires_approval=True)
    assert r["route"]["approval"] == "pending_council_vote"


def test_doctrine():
    r = sov_doctrine()
    assert r["doctrine"]["motto"].startswith("Defend")
    assert "Offensive action" in str(r["doctrine"]["principles"])
    assert len(r["doctrine"]["jsp_936_audit_pillars"]) == 5


def test_doctrine_defensive_only():
    r = sov_doctrine()
    assert "Never Offend" in r["doctrine"]["motto"]
    assert "NOT in scope" in str(r["doctrine"]["principles"])


def test_all_signed():
    r1 = sov_threat_assess("test")
    r2 = sov_iwc_calculate(100, 50, 25)
    r3 = sov_jsp936_audit("org", {p: True for p in DEFENSIVE_DOCTRINE["jsp_936_audit_pillars"]})
    r4 = sov_c2_route("a", "b")
    r5 = sov_doctrine()
    for r in [r1, r2, r3, r4, r5]:
        assert "kid" in r and "sig" in r
