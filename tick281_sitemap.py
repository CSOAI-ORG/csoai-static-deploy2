#!/usr/bin/env python3
"""Tick 281: append 3 new deep-dive pack URLs to sitemap.xml + sitemap-ai.xml."""
import re

NEW = [
    "defoneos-education-authority-northern-ireland-ai-deep-dive-pack",
    "defoneos-scottish-legal-aid-board-ai-deep-dive-pack",
    "defoneos-social-security-scotland-ai-deep-dive-pack",
]
TS = "2026-08-14T06:00:00+00:00"

def block(slug, pri="0.8"):
    return (
        f"  <ns0:url>\n"
        f"    <ns0:loc>https://csoai.org/{slug}.html</ns0:loc>\n"
        f"    <ns0:lastmod>{TS}</ns0:lastmod>\n"
        f"    <ns0:changefreq>weekly</ns0:changefreq>\n"
        f"    <ns0:priority>{pri}</ns0:priority>\n"
        f"  </ns0:url>\n"
    )

for fn in ["sitemap.xml", "sitemap-ai.xml"]:
    t = open(fn).read()
    before = len(re.findall(r'<ns0:loc>', t))
    # guard: never duplicate an existing slug
    missing = [s for s in NEW if f"{s}.html" not in t]
    if not missing:
        print(f"{fn}: all 3 already present, no-op")
        continue
    add = "".join(block(s) for s in missing)
    # insert before final </ns0:urlset>
    idx = t.rfind("</ns0:urlset>")
    assert idx != -1
    newt = t[:idx] + add + t[idx:]
    open(fn, "w").write(newt)
    after = len(re.findall(r'<ns0:loc>', newt))
    print(f"{fn}: {before} -> {after} (+{after-before}) | added {[s.rsplit('-',4)[0] for s in missing]}")
