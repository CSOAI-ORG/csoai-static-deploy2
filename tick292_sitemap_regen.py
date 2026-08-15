#!/usr/bin/env python3
"""Tick 292 — Regenerate sitemap.xml + sitemap-ai.xml from the live on-disk estate
using build_site.py's allowlist (Pitfall 31 os.walk-equivalent). Domain:
www.csoai.org (sitemap.xml) / csoai.org (sitemap-ai.xml)."""
import datetime
import build_site

ROOT = build_site.ROOT
today = datetime.date.today().isoformat()
ts = f"{today}T06:00:00+00:00"

files = build_site.publishable()
rels = sorted(f.relative_to(ROOT).as_posix() for f in files)

urls = []
for r in rels:
    if r.startswith("functions/"):
        continue
    if r == "_redirects":
        continue
    urls.append(r)

std = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
ns0 = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<ns0:urlset xmlns:ns0="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    std.append(f'  <url>\n    <loc>https://www.csoai.org/{u}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.7</priority>\n  </url>')
    ns0.append(f'  <ns0:url>\n    <ns0:loc>https://csoai.org/{u}</ns0:loc>\n    <ns0:lastmod>{ts}</ns0:lastmod>\n    <ns0:changefreq>weekly</ns0:changefreq>\n    <ns0:priority>0.8</ns0:priority>\n  </ns0:url>')
std.append('</urlset>')
ns0.append('</ns0:urlset>')

sm = "\n".join(std) + "\n"
sm_ai = "\n".join(ns0) + "\n"
open(ROOT / "sitemap.xml", "w").write(sm)
open(ROOT / "sitemap-ai.xml", "w").write(sm_ai)
print(f"sitemap.xml: {len(sm.encode())}b / {len(urls)} URLs")
print(f"sitemap-ai.xml: {len(sm_ai.encode())}b / {len(urls)} URLs")
for probe in ["scottish-ambulance-service-emergency-care", "scottish-land-commission-land-reform", "nhs-education-for-scotland-health-workforce"]:
    assert probe in sm and probe in sm_ai, f"MISSING {probe}"
print("all 3 tick-292 slugs present in both sitemaps")
