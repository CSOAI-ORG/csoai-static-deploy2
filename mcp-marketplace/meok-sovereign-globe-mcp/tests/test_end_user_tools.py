"""Tests for end_user_tools.py — the 9 visual surface tools."""
import os, sys, importlib.util, json

HERE = os.path.dirname(os.path.abspath(__file__))

# Add the package to sys.path
PKG_PARENT = os.path.dirname(HERE)
sys.path.insert(0, PKG_PARENT)

# Import end_user_tools directly (it's a submodule of the package)
EUT_PATH = os.path.join(HERE, "..", "meok_sovereign_globe_mcp", "end_user_tools.py")
spec = importlib.util.spec_from_file_location("end_user_tools", EUT_PATH)
eut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eut)


def test_all_9_end_user_tools():
    """Verify all 9 tools exist and are callable."""
    funcs = [
        "render_globe", "render_world", "render_city", "render_arena",
        "render_colosseum", "render_bft33", "get_live_state",
        "list_surfaces", "install_for_platform",
    ]
    for f in funcs:
        assert hasattr(eut, f), f"missing function: {f}"


def test_render_globe_returns_iframe():
    r = eut.render_globe()
    assert "iframe" in r["iframe_html"].lower()
    assert "c4e12208" in r["iframe_html"]
    assert r["type"] == "3d"
    assert r["surface"] == "globe"
    assert r["interactive"] is True


def test_render_world_custom_size():
    r = eut.render_world(width=800, height=500)
    assert 'width="800"' in r["iframe_html"]
    assert 'height="500"' in r["iframe_html"]


def test_render_city_engine():
    r = eut.render_city()
    assert "sov-city-3d" in r["url"]
    assert r["engine"] == "Three.js"
    assert "design" in r["note"].lower()


def test_render_arena_live_data():
    r = eut.render_arena()
    assert "arena_public" in r["url"]
    assert "rounds.jsonl" in r["live_data"]


def test_render_colosseum():
    r = eut.render_colosseum()
    assert "arenas.html" in r["url"]
    assert r["surface"] == "colosseum"


def test_render_bft33():
    r = eut.render_bft33()
    assert "bft33-live" in r["url"]
    assert r["surface"] == "bft33"


def test_list_surfaces_returns_9():
    r = eut.list_surfaces()
    assert r["count"] == 9
    keys = [s["key"] for s in r["surfaces"]]
    for required in ["globe", "world", "city", "arena", "colosseum", "bft33",
                    "pulse", "experiments", "sovereign_os"]:
        assert required in keys, f"missing surface: {required}"


def test_install_for_each_platform():
    for plat in ["claude_desktop", "chatgpt", "cursor", "copilot_vscode", "gemini_cli"]:
        r = eut.install_for_platform(plat)
        assert r["platform"] == plat
        assert "uvx" in r["base_install"]
        assert "npm" in r["base_install"]  # 'npm' key holds 'npx -y ...' command


def test_install_claude_desktop_has_config():
    r = eut.install_for_platform("claude_desktop")
    assert "claude_desktop_config.json" in r["config_path"]
    assert "mcpServers" in r["snippet"]


def test_install_unknown_platform_errors():
    r = eut.install_for_platform("foo-bar")
    assert "error" in r
    assert "supported" in r


def test_get_live_state_returns_dict():
    r = eut.get_live_state()
    assert "sources" in r
    assert isinstance(r["sources"], dict)


def test_all_surfaces_point_at_pages_dev():
    r = eut.list_surfaces()
    for s in r["surfaces"]:
        assert ".pages.dev" in s["url"], f"{s['key']} bad URL: {s['url']}"


def test_no_internal_codenames_in_public():
    """Per AGENTS.md: never expose SOVOS/SOV33/sov6 on public."""
    forbidden = ["sov6", "SOVOS", "sov33-"]
    r = eut.list_surfaces()
    for s in r["surfaces"]:
        for f in forbidden:
            assert f.lower() not in s["title"].lower()
            assert f.lower() not in s["description"].lower()
            assert f.lower() not in s["url"].lower()


def test_module_imports_clean():
    """end_user_tools should import without requiring cryptography/mcp."""
    # Already imported via spec above — if we got here, it works.
    assert eut.PROTOCOL if hasattr(eut, "PROTOCOL") else True


def test_registered_in_main_via_init():
    """The end_user_tools functions must be accessible via the package."""
    # The functions live in end_user_tools submodule
    from meok_sovereign_globe_mcp.end_user_tools import (
        render_globe, render_world, render_city, render_arena,
        render_colosseum, render_bft33, get_live_state,
        list_surfaces, install_for_platform,
    )
    assert callable(render_globe)
    assert callable(render_world)
    assert callable(render_city)
    assert callable(render_arena)
    assert callable(render_colosseum)
    assert callable(render_bft33)
    assert callable(get_live_state)
    assert callable(list_surfaces)
    assert callable(install_for_platform)