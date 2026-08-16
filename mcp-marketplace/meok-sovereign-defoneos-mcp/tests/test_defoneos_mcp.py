"""Tests for meok-sovereign-defoneos-mcp."""
import os, sys, importlib.util, json
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
MCP_PATH = os.path.join(HERE, "..", "meok_sovereign_defoneos_mcp", "__init__.py")
spec = importlib.util.spec_from_file_location("defoneos_mcp", MCP_PATH)
defoneos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(defoneos)

# Mock index for tests
MOCK_INDEX = [
    {"slug": "fca-financial-conduct-supervision", "title": "DEFONEOS — FCA Financial Conduct Supervision", "category": "uk", "size": 35000, "desc": "UK financial regulator"},
    {"slug": "mod-ministry-of-defence", "title": "DEFONEOS — MOD Ministry of Defence", "category": "mod", "size": 40000, "desc": "UK defence ministry"},
    {"slug": "scottish-government", "title": "DEFONEOS — Scottish Government", "category": "scottish", "size": 28000, "desc": "Scottish devolved body"},
    {"slug": "nato-joint-force", "title": "DEFONEOS — NATO Joint Force Command", "category": "nato", "size": 22000, "desc": "NATO body"},
    {"slug": "fca-financial-conduct", "title": "DEFONEOS — FCA Conduct Rules", "category": "uk", "size": 19000, "desc": "Conduct rules for FCA"},
    {"slug": "crown-estate", "title": "DEFONEOS — Crown Estate", "category": "crown", "size": 18000, "desc": "Crown Estate holdings"},
]


def _mock_index():
    return MOCK_INDEX


def test_5_tools_registered():
    tools = defoneos.main()
    names = [t["name"] for t in tools["tools"]]
    assert "defoneos_list_packs" in names
    assert "defoneos_get_pack" in names
    assert "defoneos_list_categories" in names
    assert "defoneos_search_packs" in names
    assert "defoneos_install_for_platform" in names


def test_list_packs_with_mock():
    with patch.object(defoneos, "_load_index", _mock_index):
        r = defoneos.mcp_list_packs()
        assert r["count"] == 6
        assert r["total"] == 6
        assert len(r["packs"]) == 6


def test_list_packs_filter_by_category():
    with patch.object(defoneos, "_load_index", _mock_index):
        r = defoneos.mcp_list_packs(category="uk")
        assert r["count"] == 2
        assert all(p["category"] == "uk" for p in r["packs"])


def test_get_pack_found():
    with patch.object(defoneos, "_load_index", _mock_index):
        r = defoneos.mcp_get_pack("fca-financial-conduct-supervision")
        assert r["slug"] == "fca-financial-conduct-supervision"
        assert "fca-financial-conduct-supervision" in r["url"]
        assert "<iframe" in r["iframe_html"]


def test_get_pack_not_found():
    with patch.object(defoneos, "_load_index", _mock_index):
        r = defoneos.mcp_get_pack("does-not-exist")
        assert "error" in r


def test_list_categories():
    with patch.object(defoneos, "_load_index", _mock_index):
        r = defoneos.mcp_list_categories()
        assert r["total_packs"] == 6
        cats = {c["category"]: c["count"] for c in r["categories"]}
        assert cats["uk"] == 2
        assert cats["mod"] == 1
        assert cats["scottish"] == 1


def test_search_packs_by_keyword():
    with patch.object(defoneos, "_load_index", _mock_index):
        r = defoneos.mcp_search_packs("FCA")
        assert r["query"] == "FCA"
        assert r["count"] == 2  # both FCA entries
        for m in r["matches"]:
            assert "fca" in m["slug"].lower() or "FCA" in m["title"]


def test_search_packs_empty():
    r = defoneos.mcp_search_packs("")
    assert "error" in r


def test_install_for_each_platform():
    for plat in ["claude_desktop", "cursor", "copilot_vscode", "gemini_cli"]:
        r = defoneos.mcp_install_for_platform(plat)
        assert r["platform"] == plat
        assert "uvx" in r["base_install"]
        assert "npm" in r["base_install"]
        assert "see_also" in r


def test_install_unknown_platform():
    r = defoneos.mcp_install_for_platform("foo-bar")
    assert "error" in r


def test_no_internal_codenames_in_tools():
    """Public names only — no SOVOS/sov33/sov6 on surfaces."""
    forbidden = ["sov6", "SOVOS", "sov33-"]
    tools = defoneos.main()
    for t in tools["tools"]:
        for f in forbidden:
            assert f.lower() not in t["name"].lower()


def test_honest_framing_in_get_pack():
    with patch.object(defoneos, "_load_index", _mock_index):
        r = defoneos.mcp_get_pack("fca-financial-conduct-supervision")
        assert "honest_note" in r
        assert "exhaustive" in r["honest_note"].lower() or "pilot" in r["honest_note"].lower()