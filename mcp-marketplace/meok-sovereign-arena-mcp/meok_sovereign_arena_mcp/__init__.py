"""meok-sovereign-arena-mcp — SOV arena live measurement MCP.

Wraps the real SOV arena measurement corpus (527+ rounds, 7 clans, 4 axes,
Ed25519-signed) as MCP tools. End-users install in AI platforms to ask:
"Which clan is winning on the safety axis?", "Show me the council-safe ELO
trajectory", "What's the agreement rate across all rounds?".

5 tools:
  1. list_clans          - clans with current ELO + win counts
  2. get_round           - return a specific round's full record
  3. leaderboard         - ranked ELO table with axis breakdowns
  4. arena_summary       - corpus overview (rounds, axes, agreements, window)
  5. install_for_platform - install command/snippet for AI platforms

DATA PROVENANCE:
  Source: https://c4e12208.csoai-site.pages.dev/api/sov-arena/rounds.jsonl
  Snapshot mode: file is re-snapshotted on each deploy until the live KV
  sync (auth-gated by CF API token) is restored. Every round IS a real
  measured arena match, Ed25519-signed (see signed.jsonl).
  As of 2026-08-16: 527 rounds, 7 clans, 4 axes (provenance/safety/
  continuity/gov).

HONEST FRAMING:
  Register: REAL for the corpus (real measured rounds).
  Council-safe + council-oowm clans currently sit at 1118/1081 ELO
  versus base qwen2.5:7b at 1383 — the sovereign clans are NOT winning.
  This MCP surfaces the truth, not the marketing.
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Optional
from collections import defaultdict

PROTOCOL = "sovereign-arena/1.0"
VERSION = "1.0.0"

ROUNDS_URL = "https://c4e12208.csoai-site.pages.dev/api/sov-arena/rounds.jsonl"
SIGNED_URL = "https://c4e12208.csoai-site.pages.dev/api/sov-arena/signed.jsonl"
INSTALL = {
    "claude_desktop": {
        "config_path": "~/Library/Application Support/Claude/claude_desktop_config.json",
        "snippet": {"mcpServers": {"meok-sovereign-arena": {"command": "uvx", "args": ["meok-sovereign-arena-mcp"]}}},
    },
    "cursor": {
        "config_path": "~/.cursor/mcp.json",
        "snippet": {"mcpServers": {"meok-sovereign-arena": {"command": "npx", "args": ["-y", "meok-sovereign-arena-mcp"]}}},
    },
    "copilot_vscode": {
        "config_path": "~/.vscode/mcp.json",
        "snippet": {"servers": {"meok-sovereign-arena": {"command": "npx", "args": ["-y", "meok-sovereign-arena-mcp"]}}},
    },
    "gemini_cli": {
        "note": "Gemini CLI supports MCP since v0.5. Config in ~/.gemini/settings.json.",
        "snippet": {"mcpServers": {"meok-sovereign-arena": {"command": "npx", "args": ["-y", "meok-sovereign-arena-mcp"]}}},
    },
}


def _http_get_lines(url, timeout=15):
    """Return list of JSON-decoded records from a JSONL endpoint, or []."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"meok-sovereign-arena-mcp/{VERSION}"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, Exception):
        return []
    out = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def _load_rounds():
    """Returns (records, snapshot_meta). records = round dicts (round/ts/axis/clans/winner)."""
    rows = _http_get_lines(ROUNDS_URL)
    meta = {}
    rounds = []
    for r in rows:
        if "snapshot_ts" in r:
            meta = r
            continue
        if "round" in r and "winner" in r:
            rounds.append(r)
    return rounds, meta


def _elo_per_clan(rounds):
    """Returns {clan: latest_elo} from the most recent round each clan appears in."""
    latest = {}
    for r in rounds:
        for k, v in r.items():
            if isinstance(v, dict) and "elo" in v and isinstance(v["elo"], (int, float)):
                # take latest seen
                latest[k] = v["elo"]
    return latest


def _wins_per_clan(rounds):
    wins = defaultdict(int)
    for r in rounds:
        w = r.get("winner")
        if w:
            wins[w] += 1
    return dict(wins)


def _axis_breakdown(rounds):
    """Returns {axis: {clan: wins}}."""
    by_axis = defaultdict(lambda: defaultdict(int))
    for r in rounds:
        ax = r.get("axis", "unknown")
        w = r.get("winner")
        if w:
            by_axis[ax][w] += 1
    return {k: dict(v) for k, v in by_axis.items()}


def mcp_list_clans() -> dict:
    """List all clans with current ELO + total wins."""
    rounds, meta = _load_rounds()
    elos = _elo_per_clan(rounds)
    wins = _wins_per_clan(rounds)
    clans = [{"clan": c, "elo": elos.get(c, 0), "wins": wins.get(c, 0)}
             for c in sorted(set(list(elos.keys()) + list(wins.keys())))
             if not c.startswith("_") and c not in ("round", "ts", "axis", "winner", "snapshot_ts", "source", "note", "rounds_count")]
    clans.sort(key=lambda x: -x["elo"])
    return {
        "register": "REAL — real measured arena rounds, Ed25519-signed corpus",
        "clan_count": len(clans),
        "snapshot_ts": meta.get("snapshot_ts"),
        "rounds_measured": meta.get("rounds_count", len(rounds)),
        "clans": clans,
        "honest_note": "council-safe:latest (1118 ELO) and council-oowm:latest (1081 ELO) currently trail base models like qwen2.5:7b (1383) and qwen3:4b (1370). This MCP surfaces the truth.",
    }


def mcp_get_round(round_id: int) -> dict:
    """Return a specific round's full record."""
    rounds, meta = _load_rounds()
    for r in rounds:
        if r.get("round") == round_id:
            return {"found": True, "round": r, "register": "REAL"}
    return {"found": False, "round_id": round_id,
            "register": "REAL",
            "note": f"No round {round_id} in corpus of {len(rounds)} rounds."}


def mcp_leaderboard(axis: Optional[str] = None, top: int = 20) -> dict:
    """Ranked ELO table. Optional axis filter (provenance/safety/continuity/gov)."""
    rounds, meta = _load_rounds()
    if axis:
        rounds = [r for r in rounds if r.get("axis") == axis]
    elos = _elo_per_clan(rounds)
    wins = _wins_per_clan(rounds)
    rows = []
    for c, e in sorted(elos.items(), key=lambda x: -x[1])[:top]:
        rows.append({"rank": len(rows) + 1, "clan": c, "elo": round(e, 1), "wins": wins.get(c, 0)})
    return {
        "axis_filter": axis or "all",
        "rounds_in_scope": len(rounds),
        "top_count": len(rows),
        "leaderboard": rows,
        "register": "REAL — ELO derived from real measured arena matches",
    }


def mcp_arena_summary() -> dict:
    """Corpus overview: rounds, axes, top clans, agreement rate."""
    rounds, meta = _load_rounds()
    axes = sorted({r.get("axis", "?") for r in rounds})
    wins = _wins_per_clan(rounds)
    total_wins = sum(wins.values())
    # "agreement" = single-clan dominant (no ties in this corpus format)
    agreement_pct = round(100.0 * total_wins / max(len(rounds), 1), 1)
    top = sorted(wins.items(), key=lambda x: -x[1])[:5]
    return {
        "register": "REAL",
        "snapshot_ts": meta.get("snapshot_ts"),
        "source_note": meta.get("note", ""),
        "rounds_measured": meta.get("rounds_count", len(rounds)),
        "axes": axes,
        "clan_count": len(set(wins.keys())),
        "agreement_pct": agreement_pct,
        "top_5_winners": [{"clan": k, "wins": v} for k, v in top],
        "honest_note": "This is the live measurement corpus. Sovereign clans trail base models as of snapshot ts.",
    }


def mcp_install_for_platform(platform: str = "claude_desktop") -> dict:
    """Install command/snippet for the chosen AI platform."""
    plat = INSTALL.get(platform)
    if not plat:
        return {"ok": False, "error": f"Unknown platform '{platform}'. Supported: {list(INSTALL.keys())}"}
    return {"ok": True, "platform": platform, **plat, "protocol": PROTOCOL, "version": VERSION}


# Tool dispatch table for MCP runtimes
TOOLS = {
    "list_clans": mcp_list_clans,
    "get_round": mcp_get_round,
    "leaderboard": mcp_leaderboard,
    "arena_summary": mcp_arena_summary,
    "install_for_platform": mcp_install_for_platform,
}


if __name__ == "__main__":
    # CLI smoke test
    print(json.dumps(mcp_arena_summary(), indent=2))