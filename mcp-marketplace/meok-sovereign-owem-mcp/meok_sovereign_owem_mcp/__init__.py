"""meok-sovereign-owem-mcp — Open World Emergence Model MCP.

Wraps the 6 sectors × 4 axes × 3 depths OWEM specialist matrix as MCP tools.
End-users install this alongside globe/spine/os to get the OWEM federation
inside their AI platform's chat.

7 tools:
  1. list_sectors          - the 6 OWEM sectors + their roles
  2. list_axes             - the 4 axes per sector
  3. list_depths           - depth_1 (live) / depth_2 / depth_3 (DESIGNED)
  4. compose_specialist    - compose sector × axis × depth → OWEM specialist id
  5. compose_clan          - compose 6 specialists → 1 clan
  6. arena_route           - get the live arena route (which specialists are routed)
  7. install_for_platform  - install command/snippet for AI platforms
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Optional

PROTOCOL = "sovereign-owem/1.0"
VERSION = "1.0.0"

# 6 sectors × 4 axes × 3 depths = 72 declared OWEM specialists
SECTORS = {
    "csoai-adversarial":       "EU AI Act adversarial probes — pushes council toward stricter legal compliance",
    "csoai-cited":             "Citation-grounded reasoning — anchors verdicts to EU AI Act / GDPR articles",
    "defoneos-precise":        "DEFONEOS precise compliance — conservative yes/no on regulated entries",
    "law-adversarial":        "Law-side adversarial — probes verdicts from a counsel-trained adversary",
    "meok-operational":        "Operational / runtime fit — pragmatic operator lens (does verdict survive deployment)",
    "sovereignty-evidential":  "Sovereignty + evidential — demands evidence before agreeing (slow but right)",
}
AXES = {
    "governance":  "EU AI Act governance, regulatory compliance",
    "defence":     "DEFONEOS defence, security, adversarial robustness",
    "intuition":   "Pattern intuition, edge-case reasoning",
    "operational": "Operational fit, deployment readiness",
}
DEPTHS = {
    "depth_1": "shallow specialist — LIVE in arena (signed via spine-mcp)",
    "depth_2": "composed (DESIGNED) — federation of depth_1 specialists",
    "depth_3": "federated (DESIGNED) — meta-composed across sectors",
}

# The 6 active fleet clans (which compose multiple specialists)
ACTIVE_CLANS = {
    "clan-csoai-adversarial:latest":        ["csoai-adversarial:governance", "csoai-adversarial:defence"],
    "clan-csoai-cited:latest":              ["csoai-cited:governance", "csoai-cited:operational"],
    "clan-defoneos-precise:latest":         ["defoneos-precise:governance"],
    "clan-law-adversarial:latest":          ["law-adversarial:governance"],
    "clan-meok-operational:latest":         ["meok-operational:governance", "meok-operational:intuition"],
    "clan-sovereignty-evidential:latest":   ["sovereignty-evidential:governance", "sovereignty-evidential:intuition"],
}

LIVE_APIS = {
    "arena_rounds": "https://c4e12208.csoai-site.pages.dev/api/sov-arena/rounds.jsonl",
    "council_league": "https://c4e12208.csoai-site.pages.dev/api/arena-24x7/reborn_league.json",
    "council_rounds": "https://c4e12208.csoai-site.pages.dev/api/arena-24x7/reborn_rounds.jsonl",
    "owem_page": "https://c4e12208.csoai-site.pages.dev/owem-federation.html",
}

INSTALL = {
    "claude_desktop": {
        "config_path": "~/Library/Application Support/Claude/claude_desktop_config.json",
        "snippet": {"mcpServers": {"meok-sovereign-owem": {"command": "uvx", "args": ["meok-sovereign-owem-mcp"]}}},
    },
    "cursor": {
        "config_path": "~/.cursor/mcp.json",
        "snippet": {"mcpServers": {"meok-sovereign-owem": {"command": "npx", "args": ["-y", "meok-sovereign-owem-mcp"]}}},
    },
    "copilot_vscode": {
        "config_path": "~/.vscode/mcp.json",
        "snippet": {"servers": {"meok-sovereign-owem": {"command": "npx", "args": ["-y", "meok-sovereign-owem-mcp"]}}},
    },
    "gemini_cli": {
        "note": "Gemini CLI supports MCP since v0.5. Config in ~/.gemini/settings.json.",
        "snippet": {"mcpServers": {"meok-sovereign-owem": {"command": "npx", "args": ["-y", "meok-sovereign-owem-mcp"]}}},
    },
}


def _http_get(url, timeout=8):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "meok-sovereign-owem-mcp/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, Exception):
        return None


def mcp_list_sectors():
    return {"sectors": [{"name": k, "role": v} for k, v in SECTORS.items()], "count": len(SECTORS)}


def mcp_list_axes():
    return {"axes": [{"name": k, "scope": v} for k, v in AXES.items()], "count": len(AXES)}


def mcp_list_depths():
    return {"depths": [{"name": k, "status": v} for k, v in DEPTHS.items()], "count": len(DEPTHS)}


def mcp_compose_specialist(sector: str, axis: str, depth: str = "depth_1"):
    """Compose a sector × axis × depth into a specialist id."""
    if sector not in SECTORS:
        return {"error": f"unknown sector: {sector}", "valid_sectors": list(SECTORS.keys())}
    if axis not in AXES:
        return {"error": f"unknown axis: {axis}", "valid_axes": list(AXES.keys())}
    if depth not in DEPTHS:
        return {"error": f"unknown depth: {depth}", "valid_depths": list(DEPTHS.keys())}
    specialist_id = f"{sector}:{axis}:{depth}"
    is_live = depth == "depth_1" and (sector, axis) in [
        ("csoai-adversarial", "governance"), ("csoai-adversarial", "defence"),
        ("csoai-cited", "governance"), ("csoai-cited", "operational"),
        ("defoneos-precise", "governance"), ("law-adversarial", "governance"),
        ("meok-operational", "governance"), ("meok-operational", "intuition"),
        ("sovereignty-evidential", "governance"), ("sovereignty-evidential", "intuition"),
    ]
    return {
        "specialist_id": specialist_id,
        "sector": sector, "axis": axis, "depth": depth,
        "routed": is_live,
        "status": "live" if is_live else "declared",
        "honest_note": "Specialists show per-domain fit gains (avg +0.5 to +2.0%) but NOT emergence. "
                       "Emergence requires 3+ decorrelated brains + held-out recompute (UNMEASURED).",
    }


def mcp_compose_clan(clan_name: str):
    """Compose specialists into a clan."""
    if clan_name not in ACTIVE_CLANS:
        return {"error": f"unknown clan: {clan_name}", "valid_clans": list(ACTIVE_CLANS.keys())}
    specialists = ACTIVE_CLANS[clan_name]
    return {
        "clan": clan_name,
        "specialists": specialists,
        "specialist_count": len(specialists),
        "composition_rule": "Each clan = 1+ specialists across sectors. BFT council quorum 23/33.",
        "honest_note": "Catastrophic forgetting without rehearsal/replay fine-tuning. "
                       "Specialists overfit their own training batteries.",
    }


def mcp_arena_route():
    """Get the live arena route — which specialists are actively running."""
    arena = _http_get(LIVE_APIS["arena_rounds"])
    if not arena:
        return {"error": "arena feed unreachable"}
    rounds = []
    for line in arena.split("\n"):
        line = line.strip()
        if line:
            try: rounds.append(json.loads(line))
            except: pass
    clan_activity = {}
    for r in rounds:
        for side in ("left", "right"):
            nm = (r.get(side) or {}).get("name", "")
            if nm and nm != "human":
                clan_activity[nm] = clan_activity.get(nm, 0) + 1
    return {
        "routed_clans": len(clan_activity),
        "clan_activity": sorted(clan_activity.items(), key=lambda x: -x[1]),
        "total_rounds": len(rounds),
        "honest_note": "Only 6 fleet clans currently routed. Full 33 clan council = voters, not all active.",
    }


def mcp_install_for_platform(platform: str):
    platform = (platform or "").lower().strip()
    if platform not in INSTALL:
        return {"error": f"unknown platform: {platform}", "supported": list(INSTALL.keys())}
    info = INSTALL[platform]
    return {
        "platform": platform,
        "base_install": {
            "pypi": "pip install meok-sovereign-owem-mcp",
            "uvx": "uvx meok-sovereign-owem-mcp",
            "npm": "npx -y meok-sovereign-owem-mcp",
            "smithery": "npx -y @smithery/cli install meok-sovereign-owem-mcp",
        },
        "see_also": {"owem_page": LIVE_APIS["owem_page"]},
        **info,
    }


def main():
    return {
        "name": "meok-sovereign-owem-mcp",
        "version": VERSION,
        "protocol": PROTOCOL,
        "tools": [
            {"name": "owem_list_sectors",      "fn": mcp_list_sectors,      "schema": {}},
            {"name": "owem_list_axes",         "fn": mcp_list_axes,         "schema": {}},
            {"name": "owem_list_depths",       "fn": mcp_list_depths,       "schema": {}},
            {"name": "owem_compose_specialist","fn": mcp_compose_specialist,"schema": {"sector": "str", "axis": "str", "depth": "str?"}},
            {"name": "owem_compose_clan",      "fn": mcp_compose_clan,      "schema": {"clan_name": "str"}},
            {"name": "owem_arena_route",       "fn": mcp_arena_route,       "schema": {}},
            {"name": "owem_install_for_platform","fn": mcp_install_for_platform,"schema": {"platform": "str"}},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, default=str))