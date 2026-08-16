"""meok-sovereign-defoneos-mcp — DEFONEOS deep-dive pack MCP.

Wraps the 507 DEFONEOS regulator deep-dive packs as MCP tools.
End-users install in AI platforms to ask: "Show me the FCA deep-dive",
"Compare FCA + PRA", "Which packs cover Scottish devolved bodies?".

5 tools:
  1. list_packs         - list all packs, optional category filter
  2. get_pack           - return a specific pack's URL + summary
  3. list_categories    - count packs by category
  4. search_packs       - search by keyword in title/desc
  5. install_for_platform - install command/snippet for AI platforms
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Optional

PROTOCOL = "sovereign-defoneos/1.0"
VERSION = "1.0.0"

INDEX_URL = "https://c4e12208.csoai-site.pages.dev/_alignment/DEFONEOS_INDEX.json"
INSTALL = {
    "claude_desktop": {
        "config_path": "~/Library/Application Support/Claude/claude_desktop_config.json",
        "snippet": {"mcpServers": {"meok-sovereign-defoneos": {"command": "uvx", "args": ["meok-sovereign-defoneos-mcp"]}}},
    },
    "cursor": {
        "config_path": "~/.cursor/mcp.json",
        "snippet": {"mcpServers": {"meok-sovereign-defoneos": {"command": "npx", "args": ["-y", "meok-sovereign-defoneos-mcp"]}}},
    },
    "copilot_vscode": {
        "config_path": "~/.vscode/mcp.json",
        "snippet": {"servers": {"meok-sovereign-defoneos": {"command": "npx", "args": ["-y", "meok-sovereign-defoneos-mcp"]}}},
    },
    "gemini_cli": {
        "note": "Gemini CLI supports MCP since v0.5. Config in ~/.gemini/settings.json.",
        "snippet": {"mcpServers": {"meok-sovereign-defoneos": {"command": "npx", "args": ["-y", "meok-sovereign-defoneos-mcp"]}}},
    },
}


def _http_get(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "meok-sovereign-defoneos-mcp/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, Exception):
        return None


def _load_index():
    raw = _http_get(INDEX_URL)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except Exception:
        return []


def mcp_list_packs(category: str = None, limit: int = 100) -> dict:
    """List all packs, optional category filter."""
    packs = _load_index()
    if category:
        packs = [p for p in packs if p.get("category") == category]
    return {
        "count": len(packs),
        "total": len(_load_index()),
        "category_filter": category,
        "packs": [{"slug": p["slug"], "title": p["title"], "category": p["category"],
                   "size": p["size"], "url": f"https://c4e12208.csoai-site.pages.dev/defoneos-{p['slug']}.html"}
                  for p in packs[:limit]],
    }


def mcp_get_pack(slug: str) -> dict:
    """Return a specific pack's URL + summary."""
    packs = _load_index()
    pack = next((p for p in packs if p["slug"] == slug), None)
    if not pack:
        return {"error": f"pack not found: {slug}", "available_count": len(packs)}
    return {
        "slug": pack["slug"],
        "title": pack["title"],
        "category": pack["category"],
        "size": pack["size"],
        "desc": pack["desc"],
        "url": f"https://c4e12208.csoai-site.pages.dev/defoneos-{pack['slug']}.html",
        "iframe_html": (
            f'<iframe src="https://c4e12208.csoai-site.pages.dev/defoneos-{pack["slug"]}.html" '
            f'width="1100" height="1400" frameborder="0" allowfullscreen loading="lazy" '
            f'style="border:1px solid #06b6d4;border-radius:8px;background:#02060f"></iframe>'
        ),
        "honest_note": "DEFONEOS is not exhaustive coverage of UK/NATO/Scottish government. "
                       "It's a deep-dive pack per regulator — pilot-grade content.",
    }


def mcp_list_categories() -> dict:
    """Count packs by category."""
    packs = _load_index()
    cats = {}
    for p in packs:
        c = p.get("category", "?")
        cats[c] = cats.get(c, 0) + 1
    return {
        "total_packs": len(packs),
        "categories": [{"category": c, "count": n} for c, n in sorted(cats.items(), key=lambda x: -x[1])],
    }


def mcp_search_packs(query: str, limit: int = 20) -> dict:
    """Search packs by keyword in title/description."""
    if not query:
        return {"error": "empty query"}
    q = query.lower()
    packs = _load_index()
    matches = [p for p in packs if q in (p.get("title") or "").lower()
                                   or q in (p.get("desc") or "").lower()
                                   or q in (p.get("slug") or "").lower()]
    return {
        "query": query,
        "count": len(matches),
        "matches": [{"slug": p["slug"], "title": p["title"], "category": p["category"],
                     "url": f"https://c4e12208.csoai-site.pages.dev/defoneos-{p['slug']}.html"}
                    for p in matches[:limit]],
    }


def mcp_install_for_platform(platform: str) -> dict:
    platform = (platform or "").lower().strip()
    if platform not in INSTALL:
        return {"error": f"unknown platform: {platform}", "supported": list(INSTALL.keys())}
    info = INSTALL[platform]
    return {
        "platform": platform,
        "base_install": {
            "pypi": "pip install meok-sovereign-defoneos-mcp",
            "uvx": "uvx meok-sovereign-defoneos-mcp",
            "npm": "npx -y meok-sovereign-defoneos-mcp",
            "smithery": "npx -y @smithery/cli install meok-sovereign-defoneos-mcp",
        },
        "see_also": {"leaderboard": "https://c4e12208.csoai-site.pages.dev/defoneos-leaderboard.html"},
        **info,
    }


def main():
    return {
        "name": "meok-sovereign-defoneos-mcp",
        "version": VERSION,
        "protocol": PROTOCOL,
        "tools": [
            {"name": "defoneos_list_packs", "fn": mcp_list_packs, "schema": {"category": "str?", "limit": "int?"}},
            {"name": "defoneos_get_pack", "fn": mcp_get_pack, "schema": {"slug": "str"}},
            {"name": "defoneos_list_categories", "fn": mcp_list_categories, "schema": {}},
            {"name": "defoneos_search_packs", "fn": mcp_search_packs, "schema": {"query": "str", "limit": "int?"}},
            {"name": "defoneos_install_for_platform", "fn": mcp_install_for_platform, "schema": {"platform": "str"}},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, default=str))