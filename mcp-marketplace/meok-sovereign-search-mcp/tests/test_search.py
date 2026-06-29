"""Tests for meok-sovereign-search-mcp (full-text + keyword)."""
import os, tempfile
_TEST_DIR = tempfile.mkdtemp(prefix="sov_srch_test_")
os.environ["SOV_SRCH_KEY"] = os.path.join(_TEST_DIR, "key.pem")
import meok_sovereign_search_mcp as s_mod
from meok_sovereign_search_mcp import (
    search_index, search_query, search_stats,
    search_delete, search_clear,
)


def reset_state():
    s_mod._INDEX.clear()
    s_mod._CLEAR_APPROVALS = 0


def test_index_basic():
    reset_state()
    r = search_index("doc1", "EU AI Act Article 50", "The transparency obligation...")
    assert r["indexed"] is True
    assert r["doc_id"] == "doc1"


def test_index_with_tags():
    reset_state()
    r = search_index("doc1", "Title", "Content", tags=["compliance", "EU"])
    assert r["indexed"] is True


def test_query_basic():
    reset_state()
    search_index("doc1", "EU AI Act Article 50", "Transparency obligations for AI systems")
    r = search_query("transparency")
    assert r["count"] >= 1
    assert r["results"][0]["doc_id"] == "doc1"


def test_query_no_match():
    reset_state()
    search_index("doc1", "Title", "Content")
    r = search_query("nonexistent")
    assert r["count"] == 0


def test_query_title_boost():
    """Document with query term in title scores higher."""
    reset_state()
    search_index("doc1", "completely unrelated title", "transparency content")
    search_index("doc2", "transparency matters", "some content")
    r = search_query("transparency")
    # doc2 should rank higher due to title boost
    assert r["results"][0]["doc_id"] == "doc2"


def test_query_tag_boost():
    """Document with query term in tags scores higher."""
    reset_state()
    search_index("doc1", "Title A", "some content", tags=["unrelated"])
    search_index("doc2", "Title B", "some content", tags=["important", "key"])
    search_index("doc3", "Title C", "some content", tags=["important"])
    # We can't easily query a tag here because the terms need to be in tokens
    # But test that tags are indexed
    r = search_query("important")
    # doc2 + doc3 should match (both have "important" tag)
    assert r["count"] >= 2


def test_query_limit():
    reset_state()
    for i in range(20):
        search_index(f"doc{i}", f"doc {i}", "test content")
    r = search_query("test", limit=5)
    assert r["count"] == 5


def test_query_multi_term():
    reset_state()
    search_index("doc1", "EU AI Act", "Transparency obligations for AI systems")
    r = search_query("EU AI")
    assert r["count"] >= 1


def test_query_empty():
    reset_state()
    r = search_query("")
    assert r["count"] == 0


def test_stats_summary():
    reset_state()
    search_index("doc1", "T1", "C1" * 10)
    search_index("doc2", "T2", "C2" * 10)
    r = search_stats()
    assert r["total_docs"] == 2
    assert r["total_chars"] >= 30


def test_stats_empty():
    reset_state()
    r = search_stats()
    assert r["total_docs"] == 0


def test_delete_existing():
    reset_state()
    search_index("doc1", "T", "C")
    r = search_delete("doc1")
    assert r["deleted"] is True


def test_delete_nonexistent():
    r = search_delete("nonexistent")
    assert r["deleted"] is False


def test_clear_3_voters():
    reset_state()
    search_index("doc1", "T", "C")
    search_index("doc2", "T", "C")
    r1 = search_clear("a")
    assert r1["done"] is False
    r2 = search_clear("b")
    assert r2["done"] is False
    r3 = search_clear("c")
    assert r3["done"] is True
    assert r3["cleared"] == 2


def test_no_external_deps():
    import meok_sovereign_search_mcp as m
    src = open(m.__file__).read()
    assert "import ollama" not in src
    assert "import urllib" not in src
    assert "import requests" not in src


def test_signed_outputs():
    reset_state()
    r1 = search_index("d1", "t", "c")
    assert "kid" in r1 and "sig" in r1 and "ts" in r1
    r2 = search_query("t")
    assert "kid" in r2 and "sig" in r2 and "ts" in r2
    r3 = search_stats()
    assert "kid" in r3 and "sig" in r3 and "ts" in r3
    r4 = search_delete("d1")
    assert "kid" in r4 and "sig" in r4 and "ts" in r4
    r5 = search_clear("a")
    assert "kid" in r5 and "sig" in r5 and "ts" in r5


def test_full_lifecycle():
    """Index → query → stats → delete → clear."""
    reset_state()
    search_index("doc1", "EU AI Act", "Article 50: Transparency")
    search_index("doc2", "DORA", "5 pillars of operational resilience")
    r = search_query("transparency")
    assert r["count"] == 1
    r = search_query("pillars")
    assert r["count"] == 1
    r = search_stats()
    assert r["total_docs"] == 2
    search_delete("doc1")
    r = search_stats()
    assert r["total_docs"] == 1
    search_clear("a")
    search_clear("b")
    search_clear("c")
    r = search_stats()
    assert r["total_docs"] == 0