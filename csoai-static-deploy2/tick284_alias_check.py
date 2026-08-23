#!/usr/bin/env python3
"""Final tick-284 check on the stable feat-sandbox-arena-seam alias."""
import urllib.request, hashlib, ssl
ctx = ssl._create_unverified_context()
base = "https://feat-sandbox-arena-seam.csoai-site.pages.dev"
packs = ["defoneos-caledonian-maritime-assets-ai-deep-dive-pack",
         "defoneos-ni-water-northern-ireland-water-ai-deep-dive-pack",
         "defoneos-estyn-wales-education-training-inspection-ai-deep-dive-pack"]
def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 defoneos-verify"})
    return urllib.request.urlopen(req, context=ctx, timeout=30).read()
for p in packs:
    try:
        b = fetch(base + "/" + p + ".html")
        src = hashlib.md5(open(p + ".html", "rb").read()).hexdigest()
        live = hashlib.md5(b).hexdigest()
        print(f"{p[:46]:48s} HTTP {len(b)}b match={'BYTE-MATCH' if live==src else 'DIFF'} ep12={b'Entry Point 12' in b}")
    except Exception as e:
        print(f"{p[:46]:48s} ERROR {e}")
