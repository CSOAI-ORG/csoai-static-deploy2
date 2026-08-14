#!/usr/bin/env python3
"""Tick 285 - patch sitemap.xml + sitemap-ai.xml with 3 new packs (append before </ns0:urlset>)."""
from pathlib import Path
import re

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
LAST = "2026-08-14T19:30:00+00:00"

PACKS = [
    "defoneos-forestry-land-scotland-ai-deep-dive-pack",
    "defoneos-highlands-islands-enterprise-ai-deep-dive-pack",
    "defoneos-belfast-harbour-ai-deep-dive-pack",
]

def url_block(loc):
    return (
        "  <ns0:url>\n"
        f"    <ns0:loc>{loc}</ns0:loc>\n"
        f"    <ns0:lastmod>{LAST}</ns0:lastmod>\n"
        "    <ns0:changefreq>weekly</ns0:changefreq>\n"
        "    <ns0:priority>0.8</ns0:priority>\n"
        "  </ns0:url>\n"
    )

# ---- sitemap.xml : +3 pack pages ----
sp = ROOT / "sitemap.xml"
txt = sp.read_text()
if txt.count("</ns0:urlset>") != 1:
    raise SystemExit("sitemap.xml has !=1 closing tag; aborting")
if any(slug in txt for slug in PACKS):
    raise SystemExit("sitemap.xml already contains one of the slugs; aborting (do not double-add)")
add = "".join(url_block(f"https://csoai.org/{s}.html") for s in PACKS)
txt = txt.rstrip().replace("</ns0:urlset>", add + "</ns0:urlset>") + "\n"
sp.write_text(txt)

# ---- sitemap-ai.xml : +3 pack pages AND +3 .llm.json companions ----
sa = ROOT / "sitemap-ai.xml"
txt2 = sa.read_text()
if txt2.count("</ns0:urlset>") != 1:
    raise SystemExit("sitemap-ai.xml has !=1 closing tag; aborting")
if any(slug in txt2 for slug in PACKS):
    raise SystemExit("sitemap-ai.xml already contains one of the slugs; aborting")
add2 = "".join(url_block(f"https://csoai.org/{s}.html") for s in PACKS)
add2 += "".join(url_block(f"https://csoai.org/{s}.html.llm.json") for s in PACKS)
txt2 = txt2.rstrip().replace("</ns0:urlset>", add2 + "</ns0:urlset>") + "\n"
sa.write_text(txt2)

def cnt(path):
    return len(re.findall(rb"<ns0:loc>", path.read_bytes()))
print("sitemap.xml ns0:loc count:", cnt(sp))
print("sitemap-ai.xml ns0:loc count:", cnt(sa))
print("PATCHED OK")
