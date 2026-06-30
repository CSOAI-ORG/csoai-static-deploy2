"""Tests for meok-sovereign-federation-mcp (33-hive federation)."""
import os, tempfile
_TEST = tempfile.mkdtemp(prefix="sov_fed_")
os.environ["SOV_FED_KEY"] = _TEST + "/k.pem"
from meok_sovereign_federation_mcp import (
    federation_route, federation_topology, federation_discover,
    federation_health, federation_council, HIVES, _hive_by_id,
)


def test_33_hives():
    assert len(HIVES) == 33


def test_federation_route_basic():
    r = federation_route(1, 21)  # London → Tokyo
    assert r["source"] == "London"
    assert r["dest"] == "Tokyo"
    assert r["hops"] > 0
    assert "London" in r["path"]


def test_federation_route_same():
    r = federation_route(1, 1)
    assert r["hops"] == 0
    assert r["path"] == ["London"]


def test_federation_route_unknown():
    r = federation_route(1, 99)
    assert "error" in r


def test_federation_topology():
    r = federation_topology()
    assert r["node_count"] == 33
    assert r["edge_count"] > 0
    assert len(r["nodes"]) == 33


def test_federation_topology_strong_edges():
    r = federation_topology()
    # At least some strong edges (>=0.7)
    strong = [e for e in r["edges"] if e["strength"] >= 0.7]
    assert len(strong) > 0


def test_federation_discover():
    r = federation_discover("dora")
    assert r["count"] > 0
    assert "London" in r["hosts"]


def test_federation_discover_robotics():
    r = federation_discover("robotics")
    assert "Tokyo" in r["hosts"]


def test_federation_discover_unknown():
    r = federation_discover("nonexistent_service_xyz")
    assert r["count"] == 0


def test_federation_health():
    r = federation_health()
    assert r["total_hives"] == 33
    assert r["online"] > 0
    assert r["avg_sovereignty_score"] > 0


def test_federation_council_shield():
    r = federation_council("Shield", "Adopt new defence protocol")
    assert r["general"] == "Shield"
    assert r["voters_count"] > 0
    assert r["yes_count"] == r["voters_count"]
    assert r["quorum_met"]


def test_federation_council_builder():
    r = federation_council("Builder", "Add new McKibben actuator")
    assert r["general"] == "Builder"


def test_federation_council_unknown():
    r = federation_council("NoSuchGeneral", "test")
    assert "error" in r


def test_no_external_deps():
    import meok_sovereign_federation_mcp as m
    src = open(m.__file__).read()
    assert "import ollama" not in src
    assert "import requests" not in src


def test_signed_outputs():
    for r in [federation_route(1, 21), federation_topology(), federation_discover("dora"),
              federation_health(), federation_council("Shield", "test")]:
        assert "kid" in r and "sig" in r and "ts" in r


def test_federation_routing_integration():
    r = federation_route(1, 2)  # London → Cambridge
    # London (Argus) → Cambridge (Owl) is just 1 hop direct
    assert "London" in r["path"]
    assert "Cambridge" in r["path"]


def test_federation_routing_path_quality():
    r = federation_route(1, 21)  # London → Tokyo
    # Should go through at most ~5-10 hops
    assert r["hops"] < 33


def test_federation_health_regions():
    r = federation_health()
    # All regions should be represented
    regions = set(h["region"] for h in r["hives"])
    assert "EU" in regions
    assert "NA" in regions
    assert "AS" in regions


def test_federation_health_statuses():
    r = federation_health()
    # All hives should have a status
    for h in r["hives"]:
        assert h["status"] in ("online", "degraded", "offline")
