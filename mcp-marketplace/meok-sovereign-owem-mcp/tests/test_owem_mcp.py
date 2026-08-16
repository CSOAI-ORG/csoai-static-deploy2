"""Tests for meok-sovereign-owem-mcp."""
import os, sys, importlib.util, json

HERE = os.path.dirname(os.path.abspath(__file__))
MCP_PATH = os.path.join(HERE, "..", "meok_sovereign_owem_mcp", "__init__.py")
spec = importlib.util.spec_from_file_location("owem_mcp", MCP_PATH)
owem = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owem)


def test_7_tools_registered():
    tools = owem.main()
    names = [t["name"] for t in tools["tools"]]
    expected = ["owem_list_sectors", "owem_list_axes", "owem_list_depths",
                "owem_compose_specialist", "owem_compose_clan",
                "owem_arena_route", "owem_install_for_platform"]
    assert set(names) == set(expected), f"got {names}, expected {expected}"


def test_6_sectors():
    r = owem.mcp_list_sectors()
    assert r["count"] == 6
    names = [s["name"] for s in r["sectors"]]
    assert "csoai-adversarial" in names
    assert "csoai-cited" in names
    assert "defoneos-precise" in names
    assert "law-adversarial" in names
    assert "meok-operational" in names
    assert "sovereignty-evidential" in names


def test_4_axes():
    r = owem.mcp_list_axes()
    assert r["count"] == 4
    names = [a["name"] for a in r["axes"]]
    for a in ["governance", "defence", "intuition", "operational"]:
        assert a in names


def test_3_depths():
    r = owem.mcp_list_depths()
    assert r["count"] == 3
    names = [d["name"] for d in r["depths"]]
    assert "depth_1" in names
    assert "depth_2" in names
    assert "depth_3" in names


def test_compose_specialist_live():
    """A specialist with all live components should be routed=True."""
    r = owem.mcp_compose_specialist("csoai-adversarial", "governance", "depth_1")
    assert r["routed"] is True
    assert r["specialist_id"] == "csoai-adversarial:governance:depth_1"
    assert "honest_note" in r


def test_compose_specialist_unrouted():
    """depth_2/3 are not yet routed."""
    r = owem.mcp_compose_specialist("csoai-adversarial", "governance", "depth_2")
    assert r["routed"] is False
    assert r["status"] == "declared"


def test_compose_specialist_unknown_sector():
    r = owem.mcp_compose_specialist("foo-bar", "governance")
    assert "error" in r


def test_compose_clan_known():
    r = owem.mcp_compose_clan("clan-csoai-adversarial:latest")
    assert r["clan"] == "clan-csoai-adversarial:latest"
    assert r["specialist_count"] >= 1
    assert "BFT" in r["composition_rule"]


def test_compose_clan_unknown():
    r = owem.mcp_compose_clan("foo-bar")
    assert "error" in r


def test_arena_route_returns_dict():
    r = owem.mcp_arena_route()
    if "error" not in r:
        assert "routed_clans" in r
        assert "clan_activity" in r
        assert "honest_note" in r


def test_install_for_each_platform():
    for plat in ["claude_desktop", "cursor", "copilot_vscode", "gemini_cli"]:
        r = owem.mcp_install_for_platform(plat)
        assert r["platform"] == plat
        assert "uvx" in r["base_install"]
        assert "npm" in r["base_install"]


def test_no_internal_codenames():
    """Per AGENTS.md: never expose SOVOS/sov6/sov33 on public surfaces."""
    forbidden = ["sov6", "SOVOS", "sov33-"]
    for sector in owem.SECTORS:
        for f in forbidden:
            assert f.lower() not in sector.lower(), f"sector {sector} has internal codename '{f}'"
            assert f.lower() not in owem.SECTORS[sector].lower()
    for axis in owem.AXES:
        for f in forbidden:
            assert f.lower() not in axis.lower()
            assert f.lower() not in owem.AXES[axis].lower()


def test_honest_framing_in_outputs():
    """Every honest claim should be present."""
    r = owem.mcp_compose_specialist("csoai-adversarial", "governance", "depth_1")
    assert "emergence" in r["honest_note"].lower()
    assert "fit gains" in r["honest_note"].lower() or "specialists" in r["honest_note"].lower()
    r2 = owem.mcp_compose_clan("clan-csoai-adversarial:latest")
    assert "forgetting" in r2["honest_note"].lower() or "overfit" in r2["honest_note"].lower()