#!/usr/bin/env python3
"""Tick 261 sitemap updater — insert 3 new URLs before </urlset>."""
import re
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
SM = ROOT / "sitemap.xml"
SM_AI = ROOT / "sitemap-ai.xml"

NEW_SLUGS = [
    "defoneos-hm-treasury-economic-fiscal-policy",
    "defoneos-jncc-joint-nature-conservation-committee",
    "defoneos-met-office-meteorological-services",
]

for target in (SM, SM_AI):
    text = target.read_text()
    added = 0
    for slug in NEW_SLUGS:
        url = f"    <loc>https://www.csoai.org/{slug}.html</loc>\n"
        if url.strip() in text:
            continue
        if "</urlset>" not in text:
            print(f"WARN: no </urlset> in {target.name}")
            continue
        text = text.replace("</urlset>", url + "</urlset>", 1)
        added += 1
    target.write_text(text)
    count = len(re.findall(r"<loc>", text))
    print(f"{target.name}: +{added}  total=<loc>={count}  bytes={target.stat().st_size}")
