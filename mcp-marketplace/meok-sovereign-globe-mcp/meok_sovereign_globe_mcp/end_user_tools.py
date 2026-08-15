"""end_user_tools.py — additional end-user visual tools for the sovereign-globe MCP.

Adds 9 tools that wrap the LIVE 3D / globe / city / arena / colosseum / clan /
council surfaces as iframe-able MCP tools. End-users install the package
once in ChatGPT/Claude/Cursor/Copilot/Gemini and get the 3D + arena
state rendered directly inside their chat — no website visit needed.

The existing meok_sovereign_globe_mcp.py (Cesium + deck.gl + hive registry)
remains the substrate-authoring toolset; this module adds the
end-user-facing visual renderers.
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Optional

# Canonical production surfaces (csoai-site Cloudflare Pages project)
SURFACES = {
    "globe": {
        "url": "https://c4e12208.csoai-site.pages.dev/cesium-globe.html",
        "title": "🌐 Cesium 3D Sovereign Hive Globe",
        "type": "3d",
        "engine": "Cesium",
        "interactive": True,
        "description": "3D photorealistic Earth with 33 sovereign hives, hive connection lines, open-data layers.",
    },
    "world": {
        "url": "https://c4e12208.csoai-site.pages.dev/world-3d.html",
        "title": "🌍 Photorealistic Sovereign Earth",
        "type": "3d",
        "engine": "World-3D",
        "interactive": True,
        "description": "Photorealistic 3D Earth. 33 sovereign hives. CC0 + MIT layers.",
    },
    "city": {
        "url": "https://c4e12208.csoai-site.pages.dev/sov-city-3d.html",
        "title": "🏛️ Council City 3D",
        "type": "3d",
        "engine": "Three.js",
        "interactive": True,
        "description": "Dual-substrate governance city with 33 clan districts, AI swarm skirmishes, human participation meter.",
    },
    "arena": {
        "url": "https://c4e12208.csoai-site.pages.dev/arena_public.html",
        "title": "⚔️ Sovereign Arena",
        "type": "dashboard",
        "interactive": True,
        "description": "Live fleet rounds dashboard. 6 fleet clans. Real rounds from /api/sov-arena/rounds.jsonl.",
    },
    "colosseum": {
        "url": "https://c4e12208.csoai-site.pages.dev/arenas.html",
        "title": "🏛️ Colosseum — SOV33 Arena Hub",
        "type": "dashboard",
        "interactive": True,
        "description": "Multi-arena colosseum. SOV33 council arena, awareness surfaces, BFT33 configurator.",
    },
    "bft33": {
        "url": "https://c4e12208.csoai-site.pages.dev/bft33-live.html",
        "title": "⚖️ BFT-33 Live Council",
        "type": "dashboard",
        "interactive": True,
        "description": "33-voter council (f_bft=10, quorum 23/33). 5 lineages, 4 temperature buckets.",
    },
    "pulse": {
        "url": "https://c4e12208.csoai-site.pages.dev/pulse.html",
        "title": "🫀 Sovereign Pulse",
        "type": "dashboard",
        "interactive": True,
        "description": "Live substrate heartbeat — arena BPM, OpenTTD tick, BFT health, 3σ drift detection.",
    },
    "experiments": {
        "url": "https://c4e12208.csoai-site.pages.dev/experiments.html",
        "title": "🧪 Sovereign Experiments",
        "type": "dashboard",
        "interactive": True,
        "description": "Wilson 95% CI + McNemar A/B harness. Live clan activity from real arena rounds.",
    },
    "sovereign_os": {
        "url": "https://c4e12208.csoai-site.pages.dev/sovereign-os.html",
        "title": "🐉 Sovereign OS — The 5 Worlds",
        "type": "dashboard",
        "interactive": True,
        "description": "Canonical surface for OOWM/OWEM/IWM/OWM/VWM (the 5 worlds).",
    },
}

LIVE_APIS = {
    "arena_rounds": "https://c4e12208.csoai-site.pages.dev/api/sov-arena/rounds.jsonl",
    "openttd_state": "https://c4e12208.csoai-site.pages.dev/api/sov-openttd/state.jsonl",
    "health": "https://c4e12208.csoai-site.pages.dev/api/health",
}

INSTALL = {
    "claude_desktop": {
        "config_path": "~/Library/Application Support/Claude/claude_desktop_config.json",
        "snippet": {"mcpServers": {"meok-sovereign-globe": {"command": "uvx", "args": ["meok-sovereign-globe-mcp"]}}},
    },
    "chatgpt": {
        "note": "ChatGPT supports MCP via Developer Mode. Enable in Settings → Connectors → Advanced. Use uvx meok-sovereign-globe-mcp in a custom GPT action.",
    },
    "cursor": {
        "config_path": "~/.cursor/mcp.json",
        "snippet": {"mcpServers": {"meok-sovereign-globe": {"command": "npx", "args": ["-y", "meok-sovereign-globe-mcp"]}}},
    },
    "copilot_vscode": {
        "config_path": "~/.vscode/mcp.json",
        "snippet": {"servers": {"meok-sovereign-globe": {"command": "npx", "args": ["-y", "meok-sovereign-globe-mcp"]}}},
    },
    "gemini_cli": {
        "note": "Gemini CLI supports MCP since v0.5. Config in ~/.gemini/settings.json.",
        "snippet": {"mcpServers": {"meok-sovereign-globe": {"command": "npx", "args": ["-y", "meok-sovereign-globe-mcp"]}}},
    },
}


def _http_get(url: str, timeout: int = 10) -> Optional[str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "meok-sovereign-globe-mcp/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, Exception):
        return None


def _iframe_html(surface_key: str, width: int = 1000, height: int = 700) -> str:
    s = SURFACES.get(surface_key)
    if not s:
        return f"<p>Unknown surface: {surface_key}</p>"
    return (
        f'<div class="sovereign-surface" data-surface="{surface_key}">'
        f'<h3>{s["title"]}</h3>'
        f'<p style="color:#9aa7b4">{s["description"]}</p>'
        f'<iframe src="{s["url"]}" width="{width}" height="{height}" '
        f'frameborder="0" allowfullscreen loading="lazy" '
        f'style="border:1px solid #fbbf24;border-radius:8px;background:#02060f"></iframe>'
        f'<p style="color:#9aa7b4;font-size:.75rem">URL: <a href="{s["url"]}">{s["url"]}</a></p>'
        f'</div>'
    )


def render_globe(width: int = 1000, height: int = 700) -> dict:
    return {
        "surface": "globe",
        "title": SURFACES["globe"]["title"],
        "url": SURFACES["globe"]["url"],
        "iframe_html": _iframe_html("globe", width, height),
        "type": "3d",
        "engine": "Cesium",
        "interactive": True,
    }


def render_world(width: int = 1000, height: int = 700) -> dict:
    return {
        "surface": "world",
        "title": SURFACES["world"]["title"],
        "url": SURFACES["world"]["url"],
        "iframe_html": _iframe_html("world", width, height),
        "type": "3d",
        "interactive": True,
    }


def render_city(width: int = 1000, height: int = 700) -> dict:
    return {
        "surface": "city",
        "title": SURFACES["city"]["title"],
        "url": SURFACES["city"]["url"],
        "iframe_html": _iframe_html("city", width, height),
        "type": "3d",
        "engine": "Three.js",
        "interactive": True,
        "note": "Substrate-backed; design-labelled measurements only, never fabricated.",
    }


def render_arena(width: int = 1000, height: int = 800) -> dict:
    return {
        "surface": "arena",
        "title": SURFACES["arena"]["title"],
        "url": SURFACES["arena"]["url"],
        "iframe_html": _iframe_html("arena", width, height),
        "type": "dashboard",
        "interactive": True,
        "live_data": LIVE_APIS["arena_rounds"],
    }


def render_colosseum(width: int = 1000, height: int = 800) -> dict:
    return {
        "surface": "colosseum",
        "title": SURFACES["colosseum"]["title"],
        "url": SURFACES["colosseum"]["url"],
        "iframe_html": _iframe_html("colosseum", width, height),
        "type": "dashboard",
        "interactive": True,
    }


def render_bft33(width: int = 1000, height: int = 600) -> dict:
    return {
        "surface": "bft33",
        "title": SURFACES["bft33"]["title"],
        "url": SURFACES["bft33"]["url"],
        "iframe_html": _iframe_html("bft33", width, height),
        "type": "dashboard",
        "interactive": True,
    }


def get_live_state() -> dict:
    state = {"sources": {}}
    arena = _http_get(LIVE_APIS["arena_rounds"], timeout=8)
    if arena:
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
        state["sources"]["arena"] = {
            "total_rounds": len(rounds),
            "agree": agree,
            "disagree": len(rounds) - agree,
            "agreement_rate": round(agree / len(rounds), 3) if rounds else 0,
            "modes": modes,
            "active_clans": len(clans),
            "last_round_ts": rounds[-1].get("ts") if rounds else None,
        }
    openttd = _http_get(LIVE_APIS["openttd_state"], timeout=8)
    if openttd:
        last = None
        for line in openttd.split("\n"):
            line = line.strip()
            if line:
                try:
                    last = json.loads(line)
                except Exception:
                    pass
        if last:
            state["sources"]["openttd"] = {
                "tick": last.get("tick"),
                "date": last.get("date"),
                "substrate": last.get("substrate"),
                "label": last.get("label"),
                "govbench_score": last.get("govbench_score"),
            }
    health = _http_get(LIVE_APIS["health"], timeout=5)
    if health:
        try:
            state["sources"]["health"] = json.loads(health)
        except Exception:
            pass
    return state


def list_surfaces() -> dict:
    return {
        "count": len(SURFACES),
        "surfaces": [
            {"key": k, "title": v["title"], "type": v["type"], "engine": v.get("engine"),
             "interactive": v["interactive"], "url": v["url"], "description": v["description"]}
            for k, v in SURFACES.items()
        ]
    }


def install_for_platform(platform: str) -> dict:
    platform = (platform or "").lower().strip()
    if platform not in INSTALL:
        return {"error": f"unknown platform: {platform}", "supported": list(INSTALL.keys())}
    info = INSTALL[platform]
    return {
        "platform": platform,
        "base_install": {
            "pypi": "pip install meok-sovereign-globe-mcp",
            "uvx": "uvx meok-sovereign-globe-mcp",
            "npm": "npx -y meok-sovereign-globe-mcp",
            "smithery": "npx -y @smithery/cli install meok-sovereign-globe-mcp",
        },
        **info,
    }