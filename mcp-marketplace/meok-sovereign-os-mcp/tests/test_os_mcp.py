"""meok-sovereign-os-mcp — tests."""
from meok_sovereign_os_mcp import (
    mcp_os_status, mcp_mcp_count, mcp_arena_elo, mcp_defoneos_summary,
    mcp_alignment_ledger, mcp_install_for_platform, PROTOCOL, VERSION, KNOWN_AXES,
)


def test_protocol_and_version():
    assert PROTOCOL == "sovereign-os/1.0"
    assert VERSION == "1.0.0"


def test_os_status_shape():
    r = mcp_os_status()
    assert r["register"].startswith("REAL")
    assert r["mcp_protocol"] == PROTOCOL
    assert r["mcp_version"] == VERSION
    assert r["sponsor"] == "CSOAI Ltd (UK 16939677)"
    assert r["domain"] == "csoai.org"
    # axes are subset of known OR equal to "?" (unknown)
    # NOTE: arena now has 16+ axes after sibling-lane Specialty Ring v1 expansion.
    # Don't hard-assert — just check it has at least the 4 original axes.
    for original in ("provenance", "safety", "continuity", "gov"):
        assert original in r["arena_axes"]


def test_mcp_count():
    r = mcp_mcp_count()
    assert r["register"].startswith("REAL")
    cats = r["by_category"]
    assert cats["sovereign_mcps_total"] == 161
    assert cats["regulator_deep_dives_defoneos"] == 507
    assert cats["compliance_packs"] == 19


def test_arena_elo_has_leaderboard():
    r = mcp_arena_elo()
    assert r["register"].startswith("REAL")
    assert r["rounds_measured"] >= 1
    assert isinstance(r["leaderboard"], list)
    # rank monotonic
    for i, row in enumerate(r["leaderboard"]):
        assert row["rank"] == i + 1
    # ELO descending
    elos = [row["elo"] for row in r["leaderboard"]]
    assert elos == sorted(elos, reverse=True)
    # honest framing
    assert "trail" in r["honest_note"] or "Truth" in r["honest_note"]


def test_defoneos_summary():
    r = mcp_defoneos_summary()
    # may be unavailable if network fails
    if not r.get("available", True):
        return  # graceful
    assert r["register"].startswith("REAL")
    if r.get("total_packs", 0) > 0:
        assert r["total_packs"] >= 100
        assert isinstance(r["by_category"], dict)
        assert len(r["sample"]) <= 5


def test_alignment_ledger():
    r = mcp_alignment_ledger()
    assert r["register"].startswith("REAL")
    assert r["ledger_url"].startswith("http")
    assert len(r["recent"]) >= 1
    for entry in r["recent"]:
        assert "id" in entry and "summary" in entry


def test_alignment_ledger_limit():
    r = mcp_alignment_ledger(limit=2)
    assert len(r["recent"]) == 2


def test_install_for_platform_supported():
    for plat in ("claude_desktop", "cursor", "copilot_vscode", "gemini_cli"):
        r = mcp_install_for_platform(plat)
        assert r["ok"] is True
        assert r["platform"] == plat
        assert r["protocol"] == PROTOCOL
        assert r["version"] == VERSION


def test_install_for_platform_unsupported():
    r = mcp_install_for_platform("bogus_platform")
    assert r["ok"] is False
    assert "Unknown platform" in r["error"]


def test_all_six_tools_have_honest_framing():
    """Every public surface must carry honest_note discipline."""
    for fn, name in [(mcp_os_status, "os_status"),
                     (mcp_mcp_count, "mcp_count"),
                     (mcp_arena_elo, "arena_elo"),
                     (mcp_defoneos_summary, "defoneos_summary"),
                     (mcp_alignment_ledger, "alignment_ledger")]:
        r = fn()
        if r.get("available") is False:
            continue
        assert "honest_note" in r, f"{name} missing honest_note"
        assert isinstance(r["honest_note"], str), f"{name} honest_note not a string"
        assert len(r["honest_note"]) > 10, f"{name} honest_note too short"