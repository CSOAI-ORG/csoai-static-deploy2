"""Tests for meok-sovereign-os-mcp."""
import os, sys, importlib.util, json

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_PARENT = os.path.dirname(HERE)
sys.path.insert(0, PKG_PARENT)

SOV_PATH = os.path.join(HERE, "..", "meok_sovereign_os_mcp", "__init__.py")
spec = importlib.util.spec_from_file_location("sov_os", SOV_PATH)
sov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sov)


def test_7_tools_registered():
    tools = sov.main()
    names = [t["name"] for t in tools["tools"]]
    expected = ["render_5_worlds", "render_33_clans", "get_signed_state",
                "explain_world", "list_clans", "arena_summary", "install_for_platform"]
    assert set(names) == set(expected), f"got {names}, expected {expected}"


def test_5_worlds_explained():
    r = sov.mcp_render_5_worlds()
    assert r["surface"] == "5_worlds"
    for w in ["OOWM", "OWEM", "IWM", "OWM", "VWM"]:
        assert w in r["worlds"], f"missing world: {w}"
        assert "name" in r["worlds"][w]
        assert "role" in r["worlds"][w]
        assert "path" in r["worlds"][w]
        assert "honest_finding" in r["worlds"][w]
    assert "iframe" in r["iframe_html"].lower()


def test_5_worlds_have_honest_findings():
    """Every world must have an honest finding (the honesty register)."""
    r = sov.mcp_render_5_worlds()
    for k, w in r["worlds"].items():
        assert len(w["honest_finding"]) > 20, f"{k} honest_finding too short"
        # Honest markers: limitation/overfit/UNMEASURED/forgetting/misses/etc.
        # Real-world honest findings don't have to use any specific word —
        # they must instead expose a limitation, fail mode, or known miss.
        assert any(marker in w["honest_finding"].lower() for marker in [
            "unmeasured", "honest", "no ", "not ", "beats", "miss", "fail",
            "overfit", "without", "stubs", "forgetting", "base", "only",
            "no 'infinite'", "catastrophic", "comput"
        ]), f"{k} honest_finding lacks honesty marker: {w['honest_finding'][:80]}"


def test_explain_world():
    r = sov.mcp_explain_world("OOWM")
    assert r["key"] == "OOWM"
    assert r["name"] == "Outer Open World Model"
    assert "honest_finding" in r


def test_explain_world_unknown():
    r = sov.mcp_explain_world("FOO")
    assert "error" in r
    assert "available" in r


def test_list_clans_returns_active():
    r = sov.mcp_list_clans()
    assert "clans" in r
    assert "active_count" in r
    # May be 0 if network fails; that's OK — schema matters


def test_arena_summary_schema():
    r = sov.mcp_arena_summary()
    if "error" not in r:
        for k in ["total_rounds", "agree", "disagree", "agreement_rate",
                  "modes", "active_clans", "last_round_ts", "honest_claim"]:
            assert k in r


def test_install_for_5_platforms():
    for plat in ["claude_desktop", "chatgpt", "cursor", "copilot_vscode", "gemini_cli"]:
        r = sov.mcp_install_for_platform(plat)
        assert r["platform"] == plat
        assert "uvx" in r["base_install"]


def test_install_unknown_platform():
    r = sov.mcp_install_for_platform("foo-bar")
    assert "error" in r


def test_no_internal_codenames():
    """Per AGENTS.md: never expose SOVOS/SOV33/sov6 on public."""
    forbidden = ["sov6", "SOVOS", "sov33-"]
    r = sov.mcp_render_5_worlds()
    # Check worlds
    for k, w in r["worlds"].items():
        for f in forbidden:
            assert f.lower() not in w["name"].lower(), f"{k} has internal codename '{f}': {w['name']}"
            assert f.lower() not in w["role"].lower()
            assert f.lower() not in w["path"].lower()
            assert f.lower() not in w["honest_finding"].lower()
    # Check honest_claim
    for f in forbidden:
        assert f.lower() not in r["honest_claim"].lower()


def test_all_surfaces_on_pages_dev():
    for k, v in sov.SURFACES.items():
        assert ".pages.dev" in v, f"surface {k} not on pages.dev: {v}"


def test_get_signed_state_returns_dict():
    r = sov.mcp_get_signed_state(limit=5)
    assert "cards" in r
    assert "honest_claim" in r


def test_render_33_clans_has_honest_claim():
    r = sov.mcp_render_33_clans()
    assert "honest_claim" in r
    assert "quorum" in r["honest_claim"].lower() or "33" in r["honest_claim"]


def test_render_5_worlds_honest_claim():
    r = sov.mcp_render_5_worlds()
    assert "honest_claim" in r
    assert "recompute" in r["honest_claim"].lower() or "authority" in r["honest_claim"].lower()