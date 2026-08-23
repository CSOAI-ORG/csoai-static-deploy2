#!/usr/bin/env python3
"""DEFONEOS tick 268 - probe candidate deep-dive packs (disk + sitemap) before build + live verify."""

from pathlib import Path
import re, urllib.request, ssl

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
sitemap = ROOT / "sitemap.xml"
smap_text = sitemap.read_text() if sitemap.exists() else ""
# namespace-agnostic loc extraction (tick-266 fix)
locs = re.findall(r"<[^>]*loc>(.*?)</[^>]*loc>", smap_text, re.S)

CANDIDATES = [
    "s4c",
    "criminal-cases-review-commission",
    "homes-england",
    "network-rail",
    "high-speed-2",
    "uk-research-and-innovation",
    "cabinet-office",
    "dstl",
    "defence-science-and-technology",
    "prime-ministers-office",
    "foreign-commonwealth-development-office",
    "home-office",
]
print("=== DISK + SITEMAP PROBE ===")
for c in CANDIDATES:
    ondisk = len(list(ROOT.glob(f"*{c}*deep-dive*.html")))
    in_smap = sum(1 for l in locs if c in l)
    print(f"  {c:45s} disk_html={ondisk}  sitemap_hits={in_smap}")

print("\n=== LIVE VERIFY (councilof.ai paths for prior packs) ===")
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
for slug in ["defoneos-press-recognition-panel-ai-deep-dive-pack",
             "defoneos-investigatory-powers-tribunal-ai-deep-dive-pack",
             "defoneos-channel-4-public-service-broadcasting-ai-deep-dive-pack"]:
    url = f"https://councilof.ai/{slug}.html"
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=30, context=ctx)
        b = r.read()
        print(f"  {slug[:40]:42s} HTTP {r.status} {len(b)}b DOCTYPE={b[:9]==b'<!DOCTYPE'}")
    except Exception as e:
        print(f"  {slug[:40]:42s} ERROR {type(e).__name__}")

print(f"\nSITEMAP total locs: {len(locs)}")