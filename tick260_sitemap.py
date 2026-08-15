#!/usr/bin/env python3
"""Tick 260 — add 3 new regulator deep-dive packs to sitemap."""
import re
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
NOW = "2026-08-11"

NEW = [
    "defoneos-certification-officer-trade-unions-ai-deep-dive-pack",
    "defoneos-legal-aid-agency-ai-deep-dive-pack",
    "defoneos-uk-hydrographic-office-ai-deep-dive-pack",
]

for sitemap_name in ("sitemap.xml", "sitemap-ai.xml"):
    target = ROOT / sitemap_name
    text = target.read_text()
    before = len(re.findall(r"<loc>", text))
    for slug in NEW:
        url = f"https://www.csoai.org/{slug}.html"
        if url in text:
            print(f"  {sitemap_name}: already has {slug}")
            continue
        # Insert as a <url> block just before </urlset>
        block = (
            f"  <url>\n"
            f"    <loc>{url}</loc>\n"
            f"    <lastmod>{NOW}</lastmod>\n"
            f"  </url>\n"
        )
        text = text.replace("</urlset>\n", block + "</urlset>\n", 1)
        print(f"  {sitemap_name}: added {slug}")
    target.write_text(text)
    after = len(re.findall(r"<loc>", text))
    print(f"{sitemap_name}: {before} -> {after}  bytes={target.stat().st_size}")
