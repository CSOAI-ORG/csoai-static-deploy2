#!/usr/bin/env python3
"""DEFONEOS tick 269 - post-deploy byte verification on unique CF Pages deployment URL."""
from pathlib import Path
import urllib.request, ssl, hashlib

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
BASE = "https://56fdaa3c.csoai-site.pages.dev"
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

SLUGS = [
    "defoneos-hs2-high-speed-rail-delivery-ai-deep-dive-pack",
    "defoneos-ukri-research-innovation-ai-deep-dive-pack",
    "defoneos-dwp-work-pensions-ai-deep-dive-pack",
]

def fetch(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40, context=ctx)
    return r.status, r.read()

print("=== BYTE VERIFY (56fdaa3c) ===")
allok = True
for s in SLUGS:
    local = (ROOT / f"{s}.html").read_bytes()
    lmd5 = hashlib.md5(local).hexdigest()
    code, live = fetch(f"{BASE}/{s}.html")
    doctype = live[:9] == b'<!DOCTYPE'
    size_match = len(live) == len(local)
    md5_match = hashlib.md5(live).hexdigest() == lmd5
    ep_count = live.count(b'<span class="en">Entry Point')
    mcp = live.count(b'<span class="t">')
    ok = (code == 200 and doctype and size_match and md5_match and ep_count == 12 and mcp == 72)
    allok &= ok
    print(f"  {s[:46]:48s} HTTP {code} {len(live)}b DOCTYPE={doctype} size={size_match} md5={md5_match} ep={ep_count} mcp={mcp} -> {'OK' if ok else 'FAIL'}")

    # llm.json
    lc, ll = fetch(f"{BASE}/{s}.html.llm.json")
    lllocal = (ROOT / f"{s}.html.llm.json").read_bytes()
    llmatch = len(ll) == len(lllocal)
    llok = lc == 200 and llmatch
    allok &= llok
    print(f"      .llm.json HTTP {lc} {len(ll)}b size={llmatch} -> {'OK' if llok else 'FAIL'}")

# sitemap live
sc, sl = fetch(f"{BASE}/sitemap.xml")
import re
locs = len(re.findall(rb"<[^>]*loc>", sl))
print(f"  sitemap.xml HTTP {sc} {len(sl)}b ns0:loc_tags={locs} -> {'OK(797)' if sc==200 and locs>=797 else 'CHECK'}")
sc2, sl2 = fetch(f"{BASE}/sitemap-ai.xml")
locs2 = len(re.findall(rb"<[^>]*loc>", sl2))
print(f"  sitemap-ai.xml HTTP {sc2} {len(sl2)}b ns0:loc_tags={locs2} -> {'OK(593)' if sc2==200 and locs2>=593 else 'CHECK'}")

print(f"\nRESULT: {'ALL VERIFIED OK' if allok else 'SOME CHECKS FAILED'}")
