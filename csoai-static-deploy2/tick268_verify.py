#!/usr/bin/env python3
"""DEFONEOS tick 268 - post-deploy byte-verify on live CF Pages deployment URL."""
import urllib.request, ssl, hashlib, re
from pathlib import Path

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent':'Mozilla/5.0'}
BASE = "https://e2c4a6ce.csoai-site.pages.dev"  # unique deployment URL

def fetch(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40, context=ctx)
    return r.status, r.read()

def sha(b): return hashlib.sha256(b).hexdigest()[:12]

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
PACKS = [
    "defoneos-s4c-public-service-broadcasting-ai-deep-dive-pack",
    "defoneos-homes-england-housing-delivery-ai-deep-dive-pack",
    "defoneos-network-rail-railway-infrastructure-ai-deep-dive-pack",
]

print(f"=== LIVE BYTE-VERIFY vs {BASE} ===")
for slug in PACKS:
    local_html = sha((ROOT / f"{slug}.html").read_bytes())
    local_llm  = sha((ROOT / f"{slug}.html.llm.json").read_bytes())
    # html
    try:
        s, b = fetch(f"{BASE}/{slug}.html")
        match_h = (sha(b) == local_html)
    except Exception as e:
        s, match_h, b = "ERR", False, b""
        print(f"  {slug[:40]:42s} ERR {type(e).__name__}")
    # llm
    try:
        s2, b2 = fetch(f"{BASE}/{slug}.html.llm.json")
        match_l = (sha(b2) == local_llm)
    except Exception as e:
        s2, match_l = "ERR", False
    doctype = b[:9] == b'<!DOCTYPE'
    h1 = b"<h1>" in b
    eps = b.count(b'<span class="en">Entry Point')
    chips = b.count(b'<span class="t">')
    print(f"  {slug[:40]:42s} html HTTP{s} match={match_h} dt={doctype} h1={h1} en={eps} chips={chips} | llm HTTP{s2} match={match_l}")

# sitemap live
for sm in ["sitemap.xml", "sitemap-ai.xml"]:
    try:
        s, b = fetch(f"{BASE}/{sm}")
        locs = re.findall(rb'<[^>]*loc>(.*?)</[^>]*loc>', b, re.S)
        n = sum(1 for l in locs if b"defoneos-s4c" in l or b"defoneos-homes-england" in l or b"defoneos-network-rail" in l)
        print(f"  {sm}: HTTP {s} {len(b)}b  locs={len(locs)}  new_pack_hits={n}")
    except Exception as e:
        print(f"  {sm}: ERR {type(e).__name__}")