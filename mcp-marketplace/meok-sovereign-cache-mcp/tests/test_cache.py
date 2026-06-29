"""Tests for meok-sovereign-cache-mcp (in-memory + TTL)."""
import os, tempfile
_TEST_DIR = tempfile.mkdtemp(prefix="sov_cache_test_")
os.environ["SOV_CACHE_KEY"] = os.path.join(_TEST_DIR, "key.pem")
import meok_sovereign_cache_mcp as c_mod
from meok_sovereign_cache_mcp import (
    cache_set, cache_get, cache_delete, cache_stats, cache_clear,
)


def reset_state():
    c_mod._CACHE.clear()
    c_mod._CLEAR_APPROVALS = 0


def test_set_basic():
    reset_state()
    r = cache_set("key1", "value1")
    assert r["key"] == "key1"
    assert r["stored"] is True


def test_set_with_ttl():
    reset_state()
    r = cache_set("key1", "value1", ttl_seconds=60)
    assert r["ttl_seconds"] == 60
    assert r["expires_at"] is not None


def test_set_no_ttl():
    reset_state()
    r = cache_set("key1", "value1")
    assert r["expires_at"] is None


def test_get_existing():
    reset_state()
    cache_set("key1", "value1")
    r = cache_get("key1")
    assert r["value"] == "value1"
    assert r["found"] is True


def test_get_missing():
    reset_state()
    r = cache_get("nonexistent")
    assert r["value"] is None
    assert r["found"] is False


def test_get_expired():
    reset_state()
    cache_set("key1", "value1", ttl_seconds=1)
    # Manually expire
    import meok_sovereign_cache_mcp as c
    c._CACHE["key1"]["expires_at"] = "2020-01-01T00:00:00+00:00"
    r = cache_get("key1")
    assert r["value"] is None
    assert r["expired"] is True


def test_delete_existing():
    reset_state()
    cache_set("key1", "value1")
    r = cache_delete("key1")
    assert r["deleted"] is True


def test_delete_nonexistent():
    reset_state()
    r = cache_delete("nonexistent")
    assert r["deleted"] is False


def test_stats_summary():
    reset_state()
    cache_set("key1", "v1")
    cache_set("key2", "v2")
    r = cache_stats()
    assert r["total_keys"] == 2


def test_clear_3_voters():
    reset_state()
    cache_set("k1", "v1")
    cache_set("k2", "v2")
    r1 = cache_clear("scribe")
    assert r1["done"] is False
    r2 = cache_clear("shield")
    assert r2["done"] is False
    r3 = cache_clear("lex")
    assert r3["done"] is True
    assert r3["cleared"] == 2


def test_clear_resets_approvals():
    """After clear completes, approvals reset to 0."""
    reset_state()
    cache_clear("a")
    cache_clear("b")
    cache_clear("c")
    # Now approvals should be 0 again
    assert c_mod._CLEAR_APPROVALS == 0


def test_no_external_deps():
    import meok_sovereign_cache_mcp as m
    src = open(m.__file__).read()
    assert "import ollama" not in src
    assert "import urllib" not in src
    assert "import requests" not in src


def test_signed_outputs():
    reset_state()
    r1 = cache_set("k", "v")
    assert "kid" in r1 and "sig" in r1 and "ts" in r1
    r2 = cache_get("k")
    assert "kid" in r2 and "sig" in r2 and "ts" in r2
    r3 = cache_delete("k")
    assert "kid" in r3 and "sig" in r3 and "ts" in r3
    r4 = cache_stats()
    assert "kid" in r4 and "sig" in r4 and "ts" in r4
    r5 = cache_clear("a")
    assert "kid" in r5 and "sig" in r5 and "ts" in r5


def test_complex_values():
    """Cache should handle complex values (dicts, lists)."""
    reset_state()
    cache_set("dict_key", {"nested": {"value": [1, 2, 3]}})
    r = cache_get("dict_key")
    assert r["value"]["nested"]["value"] == [1, 2, 3]


def test_persistence():
    """Values should persist to disk."""
    reset_state()
    cache_set("persist_key", "persist_value")
    assert c_mod.PERSIST_PATH.exists()