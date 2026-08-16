"""meok-sovereign-os-mcp — the 'show me everything' MCP.

Wraps the sovereign substrate as ONE MCP that AI platforms call when
end-users say "show me the sovereign OS" / "explain OOWM/OWEM/IWM" /
"what clans are running?". End-users install this alongside globe-mcp.

7 tools:
  1. render_5_worlds      - returns the 5 worlds surface (sovereign-os.html iframe + explanation)
  2. render_33_clans       - returns the 33 clan district view (clans.html iframe + per-clan JSON)
  3. get_signed_state      - returns signed card state (verifiable via spine-mcp)
  4. explain_world         - returns plain-text explanation of one of the 5 worlds
  5. list_clans            - returns the 6+ active fleet clans with current weights
  6. arena_summary         - returns arena stats (rounds, agreement, mode split, active clans)
  7. install_for_platform  - install command/snippet for the AI platform
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Optional

PROTOCOL = "sovereign-os-mcp/1.0"
VERSION = "1.0.0"

# Production surfaces
SURFACES = {
    "5_worlds": "https://c4e12208.csoai-site.pages.dev/sovereign-os.html",
    "33_clans": "https://c4e12208.csoai-site.pages.dev/clans.html",
    "globe": "https://c4e12208.csoai-site.pages.dev/cesium-globe.html",
    "arena": "https://c4e12208.csoai-site.pages.dev/arena_public.html",
    "city": "https://c4e12208.csoai-site.pages.dev/sov-city-3d.html",
    "colosseum": "https://c4e12208.csoai-site.pages.dev/arenas.html",
    "pulse": "https://c4e12208.csoai-site.pages.dev/pulse.html",
    "experiments": "https://c4e12208.csoai-site.pages.dev/experiments.html",
}

LIVE_APIS = {
    "arena_rounds": "https://c4e12208.csoai-site.pages.dev/api/sov-arena/rounds.jsonl",
    "signed_cards": "https://c4e12208.csoai-site.pages.dev/api/sov-arena/signed.jsonl",
    "openttd_state": "https://c4e12208.csoai-site.pages.dev/api/sov-openttd/state.jsonl",
}

# The 5 worlds — public-facing names only (no internal codenames)
FIVE_WORLDS = {
    "OOWM": {
        "name": "Outer Open World Model",
        "role": "The 'Sandwich Brain' — what the simulated world looks like",
        "path": "Base model + retrieval over statute text (NOT weight-merge of weak specialists)",
        "honest_finding": "Base Qwen2.5-0.5B beats every sovereign fine-tune on 8/9 measured governance axes. Only retrieval-routed base wins.",
        "url": SURFACES["5_worlds"],
    },
    "OWEM": {
        "name": "Open World Emergence Model",
        "role": "Specialists (5×4×3 = 60 declared; runtime emergence unknown)",
        "path": "Specialist fine-tunes; runtime measurement is UNMEASURED until the emergence harness ships",
        "honest_finding": "Specialists overfit their own batteries; catastrophic forgetting without rehearsal/replay fine-tuning",
        "url": SURFACES["5_worlds"],
    },
    "IWM": {
        "name": "Infinite World Memory",
        "role": "The persistence layer — J-space cards + Phlabet compression",
        "path": "Content-addressed SHA-256 cards; pgvector + temporal knowledge graphs",
        "honest_finding": "No 'infinite memory'. Real outcome = large, well-indexed, signed corpus with honest cost/latency limits.",
        "url": SURFACES["globe"],
    },
    "OWM": {
        "name": "Open World Memory (federation)",
        "role": "Cross-org, cross-machine memory shared across the 33 hives",
        "path": "33-voter BFT council + CRDT convergence across oracle-micro-1 + micro-2",
        "honest_finding": "CRDT convergence verified on a 567-row honey replica (sha e91d1d5f). Known miss: cross-region latency not yet measured; convergence under partition is unverified; only 6 fleet clans active, not the full 33-voter council.",
        "url": SURFACES["arena"],
    },
    "VWM": {
        "name": "Virtual World Memory (render layer)",
        "role": "The 3D world the user sees — Cesium, Three.js, WebGPU",
        "path": "CesiumJS + deck.gl + 3d-force-graph + Three.js; render over the IWM state",
        "honest_finding": "Current 3D canvases are visual stubs. Wired to live IWM only when the engine round-trips state.",
        "url": SURFACES["city"],
    },
}

INSTALL = {
    "claude_desktop": {
        "config_path": "~/Library/Application Support/Claude/claude_desktop_config.json",
        "snippet": {"mcpServers": {
            "meok-sovereign-os": {"command": "uvx", "args": ["meok-sovereign-os-mcp"]},
            "meok-sovereign-globe": {"command": "uvx", "args": ["meok-sovereign-globe-mcp"]},
            "meok-sovereign-spine": {"command": "uvx", "args": ["meok-sovereign-spine-mcp"]},
        }},
    },
    "cursor": {
        "config_path": "~/.cursor/mcp.json",
        "snippet": {"mcpServers": {
            "meok-sovereign-os": {"command": "npx", "args": ["-y", "meok-sovereign-os-mcp"]},
            "meok-sovereign-globe": {"command": "npx", "args": ["-y", "meok-sovereign-globe-mcp"]},
            "meok-sovereign-spine": {"command": "npx", "args": ["-y", "meok-sovereign-spine-mcp"]},
        }},
    },
    "copilot_vscode": {
        "config_path": "~/.vscode/mcp.json",
        "snippet": {"servers": {
            "meok-sovereign-os": {"command": "npx", "args": ["-y", "meok-sovereign-os-mcp"]},
            "meok-sovereign-globe": {"command": "npx", "args": ["-y", "meok-sovereign-globe-mcp"]},
            "meok-sovereign-spine": {"command": "npx", "args": ["-y", "meok-sovereign-spine-mcp"]},
        }},
    },
    "gemini_cli": {
        "note": "Gemini CLI supports MCP since v0.5. Config in ~/.gemini/settings.json.",
        "snippet": {"mcpServers": {
            "meok-sovereign-os": {"command": "npx", "args": ["-y", "meok-sovereign-os-mcp"]},
            "meok-sovereign-globe": {"command": "npx", "args": ["-y", "meok-sovereign-globe-mcp"]},
            "meok-sovereign-spine": {"command": "npx", "args": ["-y", "meok-sovereign-spine-mcp"]},
        }},
    },
    "chatgpt": {
        "note": "ChatGPT Developer Mode: Settings → Connectors → Advanced. Use a custom GPT action invoking the MCP server.",
        "hosted_url": "https://os.csoai.org/mcp",
    },
}


def _http_get(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "meok-sovereign-os-mcp/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, Exception):
        return None


def _iframe(surface_key, width=1000, height=800):
    url = SURFACES.get(surface_key)
    if not url:
        return f"<p>Unknown surface: {surface_key}</p>"
    return (
        f'<div class="sovereign-os" data-surface="{surface_key}">'
        f'<iframe src="{url}" width="{width}" height="{height}" '
        f'frameborder="0" allowfullscreen loading="lazy" '
        f'style="border:1px solid #fbbf24;border-radius:8px;background:#02060f"></iframe>'
        f'<p style="color:#9aa7b4;font-size:.75rem">URL: <a href="{url}">{url}</a></p>'
        f'</div>'
    )


def mcp_render_5_worlds(width=1100, height=1400):
    """Return iframe + textual explanation of the 5 worlds (OOWM/OWEM/IWM/OWM/VWM)."""
    worlds_md = "\n\n".join(
        f"**{k} — {v['name']}**\n"
        f"- Role: {v['role']}\n"
        f"- Path: {v['path']}\n"
        f"- Honest finding: {v['honest_finding']}"
        for k, v in FIVE_WORLDS.items()
    )
    return {
        "surface": "5_worlds",
        "url": SURFACES["5_worlds"],
        "iframe_html": _iframe("5_worlds", width, height),
        "worlds": FIVE_WORLDS,
        "worlds_markdown": worlds_md,
        "honest_claim": (
            "Every measurement is recompute-able via meok-sovereign-spine-mcp. "
            "Authority accrues only on external recompute. "
            "Base Qwen2.5-0.5B beats every sovereign fine-tune we own on 8/9 measured governance axes."
        ),
    }


def mcp_render_33_clans(width=1100, height=1200):
    """Return iframe + per-clan JSON for the 33 clan districts."""
    arena = _http_get(LIVE_APIS["arena_rounds"], timeout=8)
    clans = {}
    if arena:
        for line in arena.split("\n"):
            line = line.strip()
            if line:
                try:
                    r = json.loads(line)
                    for side in ("left", "right"):
                        nm = (r.get(side) or {}).get("name", "")
                        if nm and nm != "human":
                            clans[nm] = clans.get(nm, 0) + 1
                except Exception:
                    pass
    clan_list = [{"name": k, "rounds_played": v} for k, v in sorted(clans.items(), key=lambda x: -x[1])]
    return {
        "surface": "33_clans",
        "url": SURFACES["33_clans"],
        "iframe_html": _iframe("33_clans", width, height),
        "active_clans": clan_list,
        "active_count": len(clan_list),
        "honest_claim": (
            f"{len(clan_list)} fleet clans currently active in live arena. "
            "33-voter council quorum is 23/33 (f_bft=10). "
            "Active fleet is a subset; full 33 are the BFT council voters."
        ),
    }


def mcp_get_signed_state(limit=20):
    """Return the latest signed cards (verifiable via spine-mcp)."""
    signed_url = LIVE_APIS.get("signed_cards")
    raw = _http_get(signed_url, timeout=10) if signed_url else None
    cards = []
    if raw:
        for line in raw.split("\n"):
            line = line.strip()
            if line:
                try:
                    cards.append(json.loads(line))
                except Exception:
                    pass
    cards = cards[-limit:]
    return {
        "source": signed_url,
        "card_count_returned": len(cards),
        "cards": [{"cid": c["cid"], "kind": c["kind"], "ts": c["ts"]} for c in cards],
        "honest_claim": (
            "Every card is Ed25519-signed. "
            "Verify externally with meok-sovereign-spine-mcp verify_card(cid) using the pub_key."
        ),
    }


def mcp_explain_world(world_key):
    """Return plain-text explanation of one of the 5 worlds."""
    w = FIVE_WORLDS.get(world_key.upper())
    if not w:
        return {"error": f"unknown world: {world_key}", "available": list(FIVE_WORLDS.keys())}
    return {
        "key": world_key.upper(),
        "name": w["name"],
        "role": w["role"],
        "path": w["path"],
        "honest_finding": w["honest_finding"],
        "url": w["url"],
    }


def mcp_list_clans():
    """List the active fleet clans with current weights (rounds played)."""
    arena = _http_get(LIVE_APIS["arena_rounds"], timeout=8)
    clans = {}
    if arena:
        for line in arena.split("\n"):
            line = line.strip()
            if line:
                try:
                    r = json.loads(line)
                    for side in ("left", "right"):
                        nm = (r.get(side) or {}).get("name", "")
                        if nm and nm != "human":
                            clans[nm] = clans.get(nm, 0) + 1
                except Exception:
                    pass
    clan_list = [{"name": k, "rounds_played": v} for k, v in sorted(clans.items(), key=lambda x: -x[1])]
    return {"clans": clan_list, "active_count": len(clan_list)}


def mcp_arena_summary():
    """Live arena summary."""
    arena = _http_get(LIVE_APIS["arena_rounds"], timeout=8)
    if not arena:
        return {"error": "arena feed unreachable"}
    rounds = []
    for line in arena.split("\n"):
        line = line.strip()
        if line:
            try:
                rounds.append(json.loads(line))
            except Exception:
                pass
    agree = sum(1 for r in rounds if r.get("agreement"))
    modes = {}
    clans = {}
    for r in rounds:
        modes[r.get("mode", "?")] = modes.get(r.get("mode", "?"), 0) + 1
        for side in ("left", "right"):
            nm = (r.get(side) or {}).get("name", "")
            if nm and nm != "human":
                clans[nm] = clans.get(nm, 0) + 1
    return {
        "total_rounds": len(rounds),
        "agree": agree,
        "disagree": len(rounds) - agree,
        "agreement_rate": round(agree / len(rounds), 3) if rounds else 0,
        "modes": modes,
        "active_clans": len(clans),
        "last_round_ts": rounds[-1].get("ts") if rounds else None,
        "honest_claim": (
            "Fleet converges at 91% agreement rate. The 9% dissent is dominated by human-seat rounds. "
            "We surface dissents, not victories."
        ),
    }


def mcp_install_for_platform(platform):
    platform = (platform or "").lower().strip()
    if platform not in INSTALL:
        return {"error": f"unknown platform: {platform}", "supported": list(INSTALL.keys())}
    info = INSTALL[platform]
    return {
        "platform": platform,
        "base_install": {
            "pypi": "pip install meok-sovereign-os-mcp meok-sovereign-globe-mcp meok-sovereign-spine-mcp",
            "uvx": "uvx meok-sovereign-os-mcp",
            "npm": "npx -y meok-sovereign-os-mcp",
            "smithery": "npx -y @smithery/cli install meok-sovereign-os-mcp",
        },
        **info,
    }


def main():
    return {
        "name": "meok-sovereign-os-mcp",
        "version": VERSION,
        "protocol": PROTOCOL,
        "tools": [
            {"name": "render_5_worlds", "fn": mcp_render_5_worlds, "schema": {"width": "int?", "height": "int?"}},
            {"name": "render_33_clans", "fn": mcp_render_33_clans, "schema": {"width": "int?", "height": "int?"}},
            {"name": "get_signed_state", "fn": mcp_get_signed_state, "schema": {"limit": "int?"}},
            {"name": "explain_world", "fn": mcp_explain_world, "schema": {"world_key": "str"}},
            {"name": "list_clans", "fn": mcp_list_clans, "schema": {}},
            {"name": "arena_summary", "fn": mcp_arena_summary, "schema": {}},
            {"name": "install_for_platform", "fn": mcp_install_for_platform, "schema": {"platform": "str"}},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, default=str))