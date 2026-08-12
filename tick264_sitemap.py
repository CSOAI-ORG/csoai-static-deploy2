#!/usr/bin/env python3
"""DEFONEOS Tick 264 — sitemap.xml + sitemap-ai.xml update for the 3 new packs.

Adds 3 URLs to each sitemap:
  - defoneos-ministry-of-defence-central-ai-deep-dive-pack.html
  - defoneos-british-army-ai-deep-dive-pack.html
  - defoneos-royal-air-force-ai-deep-dive-pack.html

Pattern proven in ticks 256-263: insert before </urlset> closing tag.
"""

from pathlib import Path
from datetime import datetime, timezone
import re
import xml.etree.ElementTree as ET

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

NEW_SLUGS = [
    "defoneos-ministry-of-defence-central-strategic-policy-ai-deep-dive-pack",
    "defoneos-british-army-land-service-ai-deep-dive-pack",
    "defoneos-royal-air-force-air-space-service-ai-deep-dive-pack",
]

SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def build_url_element(slug, ai_only=False):
    url = ET.Element("{%s}url" % SM_NS)
    loc = ET.SubElement(url, "{%s}loc" % SM_NS)
    if ai_only:
        loc.text = f"https://www.csoai.org/{slug}.html.llm.json"
    else:
        loc.text = f"https://www.csoai.org/{slug}.html"
    lastmod = ET.SubElement(url, "{%s}lastmod" % SM_NS)
    lastmod.text = NOW
    changefreq = ET.SubElement(url, "{%s}changefreq" % SM_NS)
    changefreq.text = "monthly"
    priority = ET.SubElement(url, "{%s}priority" % SM_NS)
    priority.text = "0.7"
    return url


def update_sitemap(path, ai_only=False):
    """Insert 3 new <url> entries before </urlset>."""
    if not path.exists():
        print(f"  MISSING: {path}")
        return 0
    text = path.read_text()
    # Use ElementTree to round-trip — keeps it canonical XML
    tree = ET.fromstring(text)
    before = sum(1 for _ in tree.findall("{%s}url" % SM_NS))
    for slug in NEW_SLUGS:
        tree.append(build_url_element(slug, ai_only=ai_only))
    after = sum(1 for _ in tree.findall("{%s}url" % SM_NS))
    # Serialize with xml declaration
    new_text = ET.tostring(tree, encoding="unicode", xml_declaration=False)
    new_text = '<?xml version="1.0" encoding="UTF-8"?>\n' + new_text
    path.write_text(new_text)
    print(f"  {path.name}: {before} -> {after} urls, {path.stat().st_size}b")
    return after - before


def main():
    added_main = update_sitemap(ROOT / "sitemap.xml", ai_only=False)
    added_ai = update_sitemap(ROOT / "sitemap-ai.xml", ai_only=True)
    print(f"\nAdded {added_main} urls to sitemap.xml, {added_ai} urls to sitemap-ai.xml.")


if __name__ == "__main__":
    main()
