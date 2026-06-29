"""
MEOK OS Backend — pytest test suite.

Hits every endpoint in app.py. Uses TestClient with a temporary
SQLite + sigil chain so the tests don't touch the real on-disk store.

Run:  pytest -q
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

# Use temp paths before importing the app so its module-level init
# picks them up.
_tmp = tempfile.mkdtemp(prefix="meok-backend-tests-")
os.environ["MEOK_ICHARS_DB"] = str(Path(_tmp) / "ichars.db")
os.environ["MEOK_USERS_DB"] = str(Path(_tmp) / "users.db")
os.environ["MEOK_SIGIL_LOG"] = str(Path(_tmp) / "sigil_chain.jsonl")

# Make app.py importable.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import pytest
from fastapi.testclient import TestClient

import app as app_module
from app import app


@pytest.fixture()
def client():
    return TestClient(app)


# --------------------------------------------------------------------------- #
# 1. /api/backend/status
# --------------------------------------------------------------------------- #
def test_backend_status_shape(client):
    r = client.get("/api/backend/status")
    assert r.status_code == 200
    data = r.json()
    expected = {
        "healthy", "sov3_version", "hive", "council", "bft_quorum",
        "last_sigil", "big_braim", "mcps", "dorado", "x402",
        "eu_ai_act", "ichar",
    }
    assert expected <= set(data.keys())
    assert data["healthy"] is True
    assert data["sov3_version"] == "v2.0.0"
    assert data["hive"] == "34/34"
    assert data["council"] == "13/13"
    assert data["bft_quorum"] == "9/13"
    assert data["big_braim"] == "1.39 TB"
    assert data["mcps"] == 218
    assert data["dorado"] == "west <-> east"
    assert data["x402"] == "ready"
    assert data["eu_ai_act"] == "T-37"
    assert data["ichar"] == "ready"
    assert isinstance(data["last_sigil"], str)
    assert len(data["last_sigil"]) >= 4


# --------------------------------------------------------------------------- #
# 2-6. ichars
# --------------------------------------------------------------------------- #
def test_ichar_create_get_evolve_absorb_user_list(client):
    # create
    body = {
        "user_id": "usr-test-001",
        "name": "Tester Twin",
        "queen_model": "marcus",
        "arcana_lens": 0,
        "voice": "warm",
        "cognition": "balanced",
        "initial_message": "I am the tester twin.",
    }
    r = client.post("/api/ichar/create", json=body)
    assert r.status_code == 200, r.text
    created = r.json()
    assert "ichar_id" in created
    assert "sigil_hash" in created
    ichar_id = created["ichar_id"]

    # get
    r = client.get(f"/api/ichar/{ichar_id}")
    assert r.status_code == 200
    g = r.json()
    assert g["ichar_id"] == ichar_id
    assert g["user_id"] == "usr-test-001"
    assert g["name"] == "Tester Twin"
    assert g["queen_model"] == "marcus"
    assert g["arcana_lens"] == 0
    assert g["interactions"] == 0
    # extra fields are flattened in
    assert g["archetype"] == "Strategist"
    assert "motto" in g

    # evolve
    r = client.post(
        f"/api/ichar/{ichar_id}/evolve", json={"message": "Hello there."}
    )
    assert r.status_code == 200
    e = r.json()
    assert e["interactions"] == 1

    # absorb
    r = client.post(
        f"/api/ichar/{ichar_id}/absorb",
        json={"hive_gcp_vm": "meok-backend-vm-7"},
    )
    assert r.status_code == 200
    a = r.json()
    assert a["absorbed"] is True
    assert a["absorbed_hive"] == "meok-backend-vm-7"

    # list for user
    r = client.get("/api/ichar/user/usr-test-001")
    assert r.status_code == 200
    ulist = r.json()
    assert ulist["count"] >= 1
    assert any(i["ichar_id"] == ichar_id for i in ulist["ichars"])


def test_ichar_get_404(client):
    r = client.get("/api/ichar/ich-doesnotexist")
    assert r.status_code == 404
    assert "not found" in str(r.json()).lower()


def test_ichar_create_invalid_queen(client):
    r = client.post(
        "/api/ichar/create",
        json={
            "user_id": "u1", "name": "x", "queen_model": "no-such-queen",
            "arcana_lens": 0,
        },
    )
    assert r.status_code == 400


def test_ichar_create_invalid_arcana(client):
    r = client.post(
        "/api/ichar/create",
        json={
            "user_id": "u1", "name": "x", "queen_model": "marcus",
            "arcana_lens": 99,
        },
    )
    assert r.status_code == 422  # pydantic validation


# --------------------------------------------------------------------------- #
# 7. /api/geo
# --------------------------------------------------------------------------- #
def test_geo_localhost_is_uk(client):
    r = client.get("/api/geo")
    assert r.status_code == 200
    g = r.json()
    assert g["country_code"] == "GB"
    assert g["country"] == "United Kingdom"
    assert g["city"] == "London"
    assert g["eu"] is False
    assert g["sovereign_region"] == "UK"


# --------------------------------------------------------------------------- #
# 8. /api/cascade/route_query
# --------------------------------------------------------------------------- #
def test_cascade_tier1_short_query(client):
    r = client.post(
        "/api/cascade/route_query",
        json={"query": "hi", "config": {}, "task_type": "chat"},
    )
    assert r.status_code == 200
    c = r.json()
    assert c["tier"] == 1
    assert "tier_name" in c
    assert "model" in c
    assert 0.0 <= c["confidence"] <= 1.0
    assert c["cost_usd"] >= 0
    assert "sigil_hash" in c
    assert c["response"]


def test_cascade_tier3_code(client):
    r = client.post(
        "/api/cascade/route_query",
        json={"query": "x" * 700, "config": {}, "task_type": "code"},
    )
    assert r.status_code == 200
    assert r.json()["tier"] == 3


def test_cascade_tier4_audit(client):
    r = client.post(
        "/api/cascade/route_query",
        json={"query": "x" * 2000, "config": {}, "task_type": "audit"},
    )
    assert r.status_code == 200
    assert r.json()["tier"] == 4


def test_cascade_force_tier(client):
    r = client.post(
        "/api/cascade/route_query",
        json={"query": "tiny", "config": {"force_tier": 2}, "task_type": "chat"},
    )
    assert r.status_code == 200
    assert r.json()["tier"] == 2


# --------------------------------------------------------------------------- #
# 9. /api/sigil/verify
# --------------------------------------------------------------------------- #
def test_sigil_verify_known_and_unknown(client):
    # first pull a known hash from /api/sigl/chain
    r = client.get("/api/sigl/chain")
    assert r.status_code == 200
    entries = r.json()["entries"]
    assert entries
    known = entries[0]["hash"]

    r = client.post("/api/sigil/verify", json={"hash": known})
    assert r.status_code == 200
    v = r.json()
    assert v["verified"] is True
    assert v["block"]["hash"] == known

    r = client.post("/api/sigil/verify", json={"hash": "deadbeef0000"})
    assert r.status_code == 200
    assert r.json()["verified"] is False


# --------------------------------------------------------------------------- #
# 10-11. auth
# --------------------------------------------------------------------------- #
def test_auth_signup_login_flow(client):
    email = "Tester@MEOK.AI"
    pw = "sovereign-2026"
    r = client.post(
        "/api/auth/signup",
        json={"email": email, "password": pw, "name": "Tester"},
    )
    assert r.status_code == 200, r.text
    s = r.json()
    assert s["user_id"].startswith("usr-")
    assert s["email"] == email.lower()
    assert s["token"]
    user_id = s["user_id"]

    r = client.post(
        "/api/auth/login", json={"email": email, "password": pw}
    )
    assert r.status_code == 200
    l = r.json()
    assert l["user_id"] == user_id
    assert l["token"]


def test_auth_signup_duplicate_returns_409(client):
    body = {"email": "dup@meok.ai", "password": "abcdef"}
    r1 = client.post("/api/auth/signup", json=body)
    assert r1.status_code == 200
    r2 = client.post("/api/auth/signup", json=body)
    assert r2.status_code == 409


def test_auth_login_wrong_password(client):
    client.post(
        "/api/auth/signup",
        json={"email": "wrong@meok.ai", "password": "goodpass"},
    )
    r = client.post(
        "/api/auth/login",
        json={"email": "wrong@meok.ai", "password": "badpass"},
    )
    assert r.status_code == 401


def test_auth_signup_invalid_email(client):
    r = client.post(
        "/api/auth/signup",
        json={"email": "noatsign", "password": "goodpass"},
    )
    assert r.status_code == 400


def test_auth_signup_short_password(client):
    r = client.post(
        "/api/auth/signup",
        json={"email": "x@x.com", "password": "abc"},
    )
    assert r.status_code == 400


# --------------------------------------------------------------------------- #
# 12. /api/council/{queen_id}
# --------------------------------------------------------------------------- #
def test_council_known_and_unknown(client):
    for qid in ("marcus", "scout", "athena"):
        r = client.get(f"/api/council/{qid}")
        assert r.status_code == 200
        c = r.json()
        assert c["council_size"] == 13
        assert c["bft_quorum"] == 9
        assert c["queen"]["queen_id"] == qid
    r = client.get("/api/council/who-dat")
    assert r.status_code == 404


# --------------------------------------------------------------------------- #
# 13-14. temples
# --------------------------------------------------------------------------- #
def test_temples_list(client):
    r = client.get("/api/temples")
    assert r.status_code == 200
    t = r.json()
    assert t["count"] == 11
    codes = {x["code"] for x in t["temples"]}
    assert "UK" in codes and "EU" in codes and "US" in codes


def test_temple_get(client):
    r = client.get("/api/temple/uk")
    assert r.status_code == 200
    assert r.json()["code"] == "UK"
    r = client.get("/api/temple/zz")
    assert r.status_code == 404


# --------------------------------------------------------------------------- #
# 15. mcp list
# --------------------------------------------------------------------------- #
def test_mcp_list_count_and_shape(client):
    r = client.get("/api/mcp/list")
    assert r.status_code == 200
    d = r.json()
    assert d["count"] == 218
    sample = d["mcps"][0]
    assert {"name", "domain", "version", "tools", "transport", "sigil"} <= set(sample.keys())


# --------------------------------------------------------------------------- #
# 16. sigil chain
# --------------------------------------------------------------------------- #
def test_sigl_chain_shape(client):
    r = client.get("/api/sigl/chain")
    assert r.status_code == 200
    d = r.json()
    assert d["length"] >= 10
    assert len(d["entries"]) == 10
    for e in d["entries"]:
        assert {"op", "ts", "nonce", "prev", "hash", "fields"} <= set(e.keys())


# --------------------------------------------------------------------------- #
# 17-18. sov3 tools + invoke
# --------------------------------------------------------------------------- #
def test_sov3_tools_count(client):
    r = client.get("/api/sov3/tools")
    assert r.status_code == 200
    d = r.json()
    assert d["count"] == 222
    assert len(d["tools"]) == 222


def test_sov3_invoke_known_and_unknown(client):
    r = client.post(
        "/api/sov3/invoke",
        json={"tool": "sov_route_query", "args": {"q": "hi"}},
    )
    assert r.status_code == 200
    inv = r.json()
    assert inv["tool"] == "sov_route_query"
    assert inv["ok"] is True
    assert inv["sigil_hash"]

    r = client.post(
        "/api/sov3/invoke",
        json={"tool": "no_such_tool", "args": {}},
    )
    assert r.status_code == 404


# --------------------------------------------------------------------------- #
# 19. news
# --------------------------------------------------------------------------- #
def test_news_count(client):
    r = client.get("/api/news")
    assert r.status_code == 200
    d = r.json()
    assert d["count"] == 6
    assert all({"id", "ts", "headline", "category", "priority"} <= set(n.keys())
               for n in d["items"])


# --------------------------------------------------------------------------- #
# 20. temple-os bundle
# --------------------------------------------------------------------------- #
def test_temple_os_bundle(client):
    r = client.get("/api/temple-os/bundle")
    assert r.status_code == 200
    b = r.json()
    assert b["status"]["healthy"] is True
    assert b["mcp_count"] == 218
    assert b["sov3_tool_count"] == 222
    assert len(b["temples"]) == 11
    assert len(b["queens"]) == 13
    assert len(b["arcana"]) == 22
    assert b["news"]["count"] == 6
    assert b["sigil_length"] >= 10


# --------------------------------------------------------------------------- #
# CORS / health
# --------------------------------------------------------------------------- #
def test_cors_preflight(client):
    r = client.options(
        "/api/backend/status",
        headers={
            "Origin": "https://meok.ai",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert r.status_code in (200, 204)
    assert r.headers.get("access-control-allow-origin") in ("*", "https://meok.ai")


def test_healthz(client):
    r = client.get("/api/healthz")
    assert r.status_code == 200
    assert r.json()["ok"] is True
