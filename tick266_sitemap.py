#!/usr/bin/env python3
"""DEFONEOS Tick 266 — sitemap.xml + sitemap-ai.xml update for the 3 new packs."""
from pathlib import Path
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

NEW_SLUGS = [
    "defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack",
    "defoneos-judicial-appointments-commission-ai-deep-dive-pack",
    "defoneos-british-academy-humanities-social-sciences-ai-deep-dive-pack",
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
    if not path.exists():
        print(f"  MISSING: {path}")
        return 0
    text = path.read_text()
    tree = ET.fromstring(text)
    before = sum(1 for _ in tree.findall("{%s}url" % SM_NS))
    for slug in NEW_SLUGS:
        tree.append(build_url_element(slug, ai_only=ai_only))
    after = sum(1 for _ in tree.findall("{%s}url" % SM_NS))
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
