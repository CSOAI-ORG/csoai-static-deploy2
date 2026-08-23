#!/usr/bin/env python3
"""Tick 282 POST-DEPLOY byte-verification on the live CF Pages alias (honest-verified)."""
import hashlib, ssl, urllib.request

BASE = "https://feat-sandbox-arena-seam.csoai-site.pages.dev"
SLUGS = [
    "defoneos-scottish-water-ai-deep-dive-pack",
    "defoneos-northern-ireland-housing-executive-ai-deep-dive-pack",
    "defoneos-scotrail-scotland-railway-services-ai-deep-dive-pack",
]
LOCAL = "/Users/nicholas/clawd/csoai-static-deploy2"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def md5(b):
    return hashlib.md5(b).hexdigest()

def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 (JEEVES-deploy-verify)"})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return r.status, r.read()

import os
ok = True
def check(slug):
    global ok
    for ext in [".html", ".html.llm.json"]:
        loc = open(LOCAL + "/" + slug + ext, "rb").read()
        try:
            st, live = fetch("/" + slug + ext)
        except Exception as e:
            print(f"  {slug}{ext}: FETCH ERROR {e}")
            ok = False; continue
        m = "MATCH" if md5(loc) == md5(live) else "MISMATCH"
        if m == "MISMATCH": ok = False
        print(f"  {slug}{ext}: HTTP {st} {m} (md5 {md5(live)[:8]})")

for s in SLUGS:
    check(s)

# structural spot-check on one live page
st, live = fetch("/" + SLUGS[0] + ".html")
t = live.decode("utf-8", "ignore")
epc = t.count('Entry Point')
mcpc = t.count('<span class="t">')
print("\n%s: DOCTYPE=%s h1=%s eps=%d mcps=%d" % (SLUGS[0], '<!DOCTYPE html>' in t, '<h1>' in t, epc, mcpc))

# sitemaps live with new slugs
for sm, n in [("sitemap.xml", 836), ("sitemap-ai.xml", 632)]:
    st, s = fetch("/" + sm)
    present = all(f"{slug}.html" in s.decode() for slug in SLUGS)
    print(f"{sm}: HTTP {st} all3_present={present} count={s.decode().count('<ns0:loc>')}")
    if not present or s.decode().count('<ns0:loc>') < n:
        ok = False

print("\nVERIFY_RESULT:", "ALL_OK" if ok else "FAILURES_DETECTED")