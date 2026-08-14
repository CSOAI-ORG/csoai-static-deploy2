#!/usr/bin/env python3
"""Tick 266 — prune sitemap URLs that have no publishable file behind them.

Covers both sitemap.xml (.html pages) and sitemap-ai.xml (.llm.json companions).
After the /_site/ prefix repair, a small residual set of URLs point at files that
exist on disk but live in directories deliberately excluded from the publish
allowlist (EXEC/, chrome-extension/, arena-build/, sov7_synthesis/, SOVOS/...).
Keeping them in the sitemap would advertise 404s. We drop exactly those locs,
keeping the sitemap an honest index of what the site actually serves.
"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

# Mirror build_site.py's publishable() logic EXACTLY: only top-level files
# (ROOT.glob("*"), ext-filtered) plus files under the curated DIRS list. Nested
# .html in unlisted dirs (EXEC/, chrome-extension/, etc.) do NOT ship — so URLs
# pointing at them must be pruned from the sitemap to avoid advertising 404s.
NEVER = re.compile(
    r"(^\\.env|\\.env$|\\.env\\.|(^|/)\\.git|\\.pem$|\\.key$|_rsa$|(^|/)\\.ssh/|"
    r"wrangler\\.toml$|\\.cfignore$|SOVEREIGN_DEPLOY\\.sh$|\\.sh$|\\.py$|\\.jsonl$|"
    r"(^|/)\\.backups?/|(^|/)runs/|(^|/)node_modules/|\\.log$|\\.sqlite)", re.I)
DIRS = {"tools", ".well-known", "assets", "images", "static", "_templates",
        "portal", "sovereign-wiki", "eu-ai-act", "functions"}
ROOT_EXTS = {".html", ".txt", ".xml", ".svg", ".css", ".js", ".webmanifest", ".ico", ".png"}
JSON_ALLOW = {"agent.json", "mcp.json", "ecosystem.json", "manifest.json", "llm-manifest.json",
              "agent-card.json", "openapi.json", "ai-plugin.json", "dataset-metadata.json",
              "drift-feed.json", "jspace_deck.json", "c_space_card.json"}
EXTRA_FILES = {"_redirects"}


def shipable(pathpart):
    """True iff a root-relative URL path maps to a file build_site.py would copy."""
    rel = pathpart.lstrip("/")
    if not rel or rel == "index.html":
        return (ROOT / "index.html").is_file()
    full = ROOT / rel
    if not full.is_file():
        return False
    # Only top-level files OR files under a DIRS dir are picked by build_site.
    parts = rel.split("/")
    if len(parts) == 1:
        name = parts[0]
        if NEVER.search(name):
            return False
        return (full.suffix.lower() in ROOT_EXTS or name in JSON_ALLOW
                or name in EXTRA_FILES or name.endswith(".llm.json")
                or bool(re.match(r"tick-\d+-sigil\.json$", name)))
    # nested: must live under a listed DIRS dir and not be NEVER-listed
    if parts[0] not in DIRS:
        return False
    return not NEVER.search(rel)


def prune(path):
    if not path.exists():
        print(f"  MISSING {path}")
        return
    tree = ET.parse(path)
    root = tree.getroot()
    kept = []
    dropped = []
    for url in list(root):
        loc = url.find("{%s}loc" % SM_NS)
        if loc is None or not loc.text:
            root.remove(url)
            dropped.append("(no loc)")
            continue
        u = loc.text
        pathpart = re.sub(r"^https?://[^/]+", "", u).split("?")[0]
        if pathpart.lstrip("/") == "":
            pathpart = "/index.html"
        if shipable(pathpart.lstrip("/")):
            kept.append(u)
        else:
            root.remove(url)
            dropped.append(u)
    new_text = ET.tostring(root, encoding="unicode", xml_declaration=False)
    new_text = '<?xml version="1.0" encoding="UTF-8"?>\n' + new_text
    path.write_text(new_text)
    print(f"  {path.name}: kept {len(kept)}, dropped {len(dropped)}, {path.stat().st_size}b")
    for d in dropped:
        print(f"      DROP {d}")


def main():
    prune(ROOT / "sitemap.xml")
    prune(ROOT / "sitemap-ai.xml")


if __name__ == "__main__":
    main()
