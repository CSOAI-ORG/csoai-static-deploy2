"""Tests for meok-sovereign-federation-mcp (5D Hive + 12 Generals)."""
import os, tempfile
_TEST_DIR = tempfile.mkdtemp(prefix="sov_fed_test_")
os.environ["SOV_FED_KEY"] = os.path.join(_TEST_DIR, "key.pem")
from meok_sovereign_federation_mcp import (
    federation_status, federation_route, federation_broadcast,
    federation_sync, federation_health, GENERALS,
)


def test_status_has_12_generals():
    r = federation_status(include_health=False)
    assert r["general_count"] == 12
    assert len(r["generals"]) == 12


def test_status_includes_health():
    r = federation_status(include_health=True)
    for g in r["generals"]:
        assert "health" in g
        assert g["health"]["vm_up"] is True


def test_12_general_names():
    r = federation_status(include_health=False)
    names = [g["name"] for g in r["generals"]]
    assert names == ["Argus", "Scribe", "Shield", "Builder", "Abacus",
                     "Lex", "Scale", "Crow", "Gear", "Voice", "Owl", "Dragon"]


def test_12_sephiroth():
    r = federation_status(include_health=False)
    sephs = [g["sephirah"] for g in r["generals"]]
    assert "Keter" in sephs  # Dragon
    assert "Malkuth" in sephs  # Abacus
    assert "Chokhmah" in sephs  # Owl


def test_route_compliance_to_scribe():
    # May route to Scribe OR Argus depending on load balance.
    # The key is that score['compliance'] is non-zero.
    r = federation_route("Audit this against EU AI Act")
    assert r["score"]["compliance"] > 0
    assert r["score"]["watchdog"] > 0  # 'audit' matches both
    assert r["target_general"]["role"] in ["compliance", "watchdog"]


def test_route_sov_to_dragon():
    r = federation_route("Configure the sovereign substrate")
    # 'sovereign' keyword matches 'sovereign' role
    assert r["score"]["sovereign"] > 0
    assert r["target_general"]["role"] == "sovereign"


def test_route_load_balances():
    """The actual_vm may be different from target_general due to load."""
    r = federation_route("Monitor the iOK Farm pond")
    assert "actual_vm" in r
    assert "all_vm_loads" in r
    assert len(r["all_vm_loads"]) == 12


def test_broadcast_to_all_generals():
    r = federation_broadcast("Test message", from_general="Dragon")
    assert r["recipient_count"] == 12
    assert r["from_general"] == "Dragon"
    assert r["status"] == "BROADCAST"


def test_broadcast_care_floor_impact():
    r = federation_broadcast("Critical change", from_general="Scale",
                              care_floor_impact=True)
    assert r["status"] == "PENDING_BFT_APPROVAL"
    assert r["bft_quorum_needed"] == 3


def test_sync_5d_hive():
    r = federation_sync()
    assert r["synced"] is True
    assert r["source_vm"] == "gen-12-dragon"
    assert r["general_count"] == 12
    assert r["sephiroth_count"] == 12


def test_health_includes_bft():
    r = federation_health(include_bft=True)
    assert r["bft_result"] is not None
    assert "verdict" in r["bft_result"]
    assert r["bft_result"]["verdict"] in ["HEALTHY", "DEGRADED", "CRITICAL"]


def test_health_per_general():
    r = federation_health(include_bft=True)
    assert len(r["generals"]) == 12
    for g in r["generals"]:
        assert "cpu_pct" in g
        assert "memory_pct" in g
        assert "load_avg" in g
        assert "ollama_busy" in g
        assert "up" in g


def test_bft_verdict_healthy_when_idle():
    """If load_avg < 5, BFT verdict should be HEALTHY."""
    r = federation_health(include_bft=True)
    if r["healthy_count"] >= 10:
        assert r["bft_result"]["verdict"] == "HEALTHY"


def test_12_generals_5d_qowm_unique():
    """Each General has a unique QOwm architecture."""
    r = federation_status(include_health=False)
    archs = set()
    for g in r["generals"]:
        archs.add(g["qowm"])
    assert len(archs) == 12  # All unique


def test_3_bft_modes_per_general():
    """Each General has a bft_default in [fast, balanced, secure]."""
    r = federation_status(include_health=False)
    for g in r["generals"]:
        assert g["bft_default"] in ["fast", "balanced", "secure"]


def test_bft_default_distribution():
    """At least 2 generals in each bft_default category."""
    r = federation_status(include_health=False)
    defaults = [g["bft_default"] for g in r["generals"]]
    for mode in ["fast", "balanced", "secure"]:
        assert defaults.count(mode) >= 2, f"{mode} only {defaults.count(mode)}"


def test_no_external_dependencies():
    """Module should not import ollama, urllib, or requests."""
    import meok_sovereign_federation_mcp as m
    src = open(m.__file__).read()
    assert "import ollama" not in src
    assert "import urllib" not in src
    assert "import requests" not in src


def test_signed_outputs():
    """Every output has kid + sig + ts."""
    for func in [federation_status, federation_route, federation_broadcast,
                 federation_sync, federation_health]:
        if func is federation_route:
            r = func("test query")
        elif func is federation_broadcast:
            r = func("test message", "Dragon")
        else:
            r = func()
        assert "kid" in r
        assert "sig" in r
        assert "ts" in r