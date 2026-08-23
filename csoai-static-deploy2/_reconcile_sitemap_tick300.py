#!/usr/bin/env python3
"""Reconcile sitemap: merge live (1316) + missing tick-300 URLs -> authoritative sitemap.xml."""
import re

LIVE = "/tmp/live_sitemap.xml"
OUT = "/Users/nicholas/clawd/csoai-static-deploy2/sitemap.xml"

MISSING = [
    "defoneos-invest-northern-ireland-economic-development-ai-deep-dive-pack.html",
    "defoneos-invest-northern-ireland-economic-development-ai-deep-dive-pack.html.llm.json",
    "defoneos-national-highways-strategic-road-network-ai-deep-dive-pack.html",
    "defoneos-national-highways-strategic-road-network-ai-deep-dive-pack.html.llm.json",
]

with open(LIVE) as f:
    live = f.read()

# Extract existing locs to dedupe
existing = set(re.findall(r"<loc>([^<]+)</loc>", live))

added = []
for slug in MISSING:
    loc = f"https://www.csoai.org/{slug}"
    if loc not in existing:
        added.append(loc)

new_entries = "\n".join(f"  <url>\n    <loc>{loc}</loc>\n  </url>" for loc in added)

# Insert before </urlset>
merged = live.replace("</urlset>", new_entries + "\n</urlset>")

with open(OUT, "w") as f:
    f.write(merged)

total = len(re.findall(r"<loc>", merged))
print(f"MERGED: {len(existing)} existing + {len(added)} added = {total} total <loc> entries")
for a in added:
    print(f"  + {a}")
