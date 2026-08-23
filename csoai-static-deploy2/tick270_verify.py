#!/usr/bin/env python3
"""DEFONEOS tick 270 - post-deploy byte verification on unique CF Pages deployment URL."""
from pathlib import Path
import urllib.request, ssl, hashlib, re

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
BASE = "https://13e33bff.csoai-site.pages.dev"
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

SLUGS = [
    "defoneos-ministry-of-justice-ai-deep-dive-pack",
    "defoneos-foreign-commonwealth-development-office-ai-deep-dive-pack",
    "defoneos-electoral-commission-ai-deep-dive-pack",
]

def fetch(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40, context=ctx)
    return r.status, r.read()

print("=== BYTE VERIFY (13e33bff) ===")
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
    print(f"  {s[:48]:50s} HTTP {code} {len(live)}b DOCTYPE={doctype} size={size_match} md5={md5_match} ep={ep_count} mcp={mcp} -> {'OK' if ok else 'FAIL'}")

    lc, ll = fetch(f"{BASE}/{s}.html.llm.json")
    lllocal = (ROOT / f"{s}.html.llm.json").read_bytes()
    llmatch = len(ll) == len(lllocal)
    llok = lc == 200 and llmatch
    allok &= llok
    print(f"      .llm.json HTTP {lc} {len(ll)}b size={llmatch} -> {'OK' if llok else 'FAIL'}")

sc, sl = fetch(f"{BASE}/sitemap.xml")
locs = len(re.findall(rb"<[^>]*loc>", sl))
print(f"  sitemap.xml HTTP {sc} {len(sl)}b ns0:loc_tags={locs} -> {'OK(1600)' if sc==200 and locs>=1600 else 'CHECK'}")
sc2, sl2 = fetch(f"{BASE}/sitemap-ai.xml")
locs2 = len(re.findall(rb"<[^>]*loc>", sl2))
print(f"  sitemap-ai.xml HTTP {sc2} {len(sl2)}b ns0:loc_tags={locs2} -> {'OK(1192)' if sc2==200 and locs2>=1192 else 'CHECK'}")

print(f"\nRESULT: {'ALL VERIFIED OK' if allok else 'SOME CHECKS FAILED'}")
