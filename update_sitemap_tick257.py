#!/usr/bin/env python3
"""Append tick-257 pack URLs to sitemap.xml (idempotent)."""
from pathlib import Path
from datetime import date

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
sm = ROOT / "sitemap.xml"
text = sm.read_text(encoding="utf-8")

new_packs = [
    "defoneos-orr-office-rail-road-economic-regulation-ai-deep-dive-pack.html",
    "defoneos-ofwat-water-services-regulation-authority-ai-deep-dive-pack.html",
    "defoneos-caa-civil-aviation-consumer-protection-ai-deep-dive-pack.html",
]

def block(url, lastmod):
    return (f'  <url>\n    <loc>{url}</loc>\n'
            f'    <lastmod>{lastmod}</lastmod>\n  </url>\n')

added = 0
for name in new_packs:
    loc = f"https://www.csoai.org/{name}"
    if loc in text:
        print(f"skip (already present): {name}")
        continue
    # insert before closing </urlset>
    if text.rstrip().endswith("</urlset>"):
        text = text.rstrip()
        text = text[: -len("</urlset>")] + block(loc, date.today().isoformat()) + "</urlset>\n"
    else:
        text = text + block(loc, date.today().isoformat())
    added += 1

sm.write_text(text, encoding="utf-8")
print(f"added {added} URLs. total <loc> = {text.count('<loc>')}  bytes = {len(text.encode('utf-8'))}")
