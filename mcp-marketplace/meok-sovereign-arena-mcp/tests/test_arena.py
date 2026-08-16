"""meok-sovereign-arena-mcp — tests."""
from meok_sovereign_arena_mcp import (
    mcp_list_clans, mcp_get_round, mcp_leaderboard,
    mcp_arena_summary, mcp_install_for_platform, PROTOCOL, VERSION,
)


def test_protocol_and_version():
    assert PROTOCOL == "sovereign-arena/1.0"
    assert VERSION == "1.0.0"


def test_list_clans_shape():
    r = mcp_list_clans()
    assert r["register"] == "REAL — real measured arena rounds, Ed25519-signed corpus"
    assert r["clan_count"] >= 1
    assert isinstance(r["clans"], list)
    # sorted by ELO descending
    elos = [c["elo"] for c in r["clans"]]
    assert elos == sorted(elos, reverse=True)
    # each clan has required keys
    for c in r["clans"]:
        assert {"clan", "elo", "wins"} <= set(c.keys())
    assert "honest_note" in r


def test_get_round_found_and_missing():
    r_ok = mcp_get_round(1)
    assert r_ok["found"] is True
    assert r_ok["round"]["round"] == 1
    r_miss = mcp_get_round(999999)
    assert r_miss["found"] is False
    assert "corpus" in r_miss["note"]


def test_leaderboard_default():
    r = mcp_leaderboard()
    assert r["axis_filter"] == "all"
    assert r["rounds_in_scope"] > 0
    assert isinstance(r["leaderboard"], list)
    assert len(r["leaderboard"]) <= 20
    elos = [row["elo"] for row in r["leaderboard"]]
    assert elos == sorted(elos, reverse=True)


def test_leaderboard_axis_filter():
    r = mcp_leaderboard(axis="safety")
    assert r["axis_filter"] == "safety"
    # safety rounds may be smaller subset
    assert r["rounds_in_scope"] >= 0


def test_arena_summary():
    r = mcp_arena_summary()
    assert r["register"] == "REAL"
    assert r["rounds_measured"] >= 1
    assert isinstance(r["axes"], list) and len(r["axes"]) >= 1
    assert 0.0 <= r["agreement_pct"] <= 100.0
    assert isinstance(r["top_5_winners"], list)
    # all four canonical axes appear in arena summary axes
    expected_axes = {"provenance", "safety", "continuity", "gov"}
    assert expected_axes & set(r["axes"])


def test_install_for_platform_supported():
    for plat in ("claude_desktop", "cursor", "copilot_vscode", "gemini_cli"):
        r = mcp_install_for_platform(plat)
        assert r["ok"] is True
        assert r["platform"] == plat
        assert "snippet" in r
        assert r["protocol"] == PROTOCOL
        assert r["version"] == VERSION


def test_install_for_platform_unsupported():
    r = mcp_install_for_platform("bogus_platform")
    assert r["ok"] is False
    assert "Unknown platform" in r["error"]


def test_honest_framing_intact():
    """Council-safe/oowm clans must NOT be portrayed as winning."""
    r = mcp_list_clans()
    note = r["honest_note"]
    assert "council-safe" in note
    assert "council-oowm" in note
    assert "trail" in note or "losing" in note or "currently" in note


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))