#!/usr/bin/env python3
"""Tick 284 post-deploy live byte-verification."""
import urllib.request, hashlib, ssl
ctx = ssl._create_unverified_context()
base = "https://c25deef4.csoai-site.pages.dev"
packs = ["defoneos-caledonian-maritime-assets-ai-deep-dive-pack",
         "defoneos-ni-water-northern-ireland-water-ai-deep-dive-pack",
         "defoneos-estyn-wales-education-training-inspection-ai-deep-dive-pack"]
def md5(b): return hashlib.md5(b).hexdigest()
def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 defoneos-verify"})
    return urllib.request.urlopen(req, context=ctx, timeout=30).read()
for p in packs:
    url = base + "/" + p + ".html"
    try:
        b = fetch(url)
        live = md5(b); src = md5(open(p + ".html", "rb").read())
        match = "BYTE-MATCH" if live == src else "DIFF"
        print(f"{p[:46]:48s} HTTP {len(b)}b {match} h1={b'AI Deep-Dive Pack' in b} ep12={b'Entry Point 12' in b} mcp={b'mcp-uk-legislation' in b}")
    except Exception as e:
        print(f"{p[:46]:48s} ERROR {e}")
for p in packs:
    u = base + "/" + p + ".html.llm.json"
    try:
        b = fetch(u)
        print(f"{p[:42]:44s} llm.json HTTP {len(b)}b ok={b'LLMPageSummary' in b}")
    except Exception as e:
        print(f"{p[:42]:44s} llm.json ERROR {e}")
# sitemap live
for sm in ["sitemap.xml", "sitemap-ai.xml"]:
    try:
        b = fetch(base + "/" + sm)
        print(f"{sm}: HTTP {len(b)}b locs={b.count(b'<ns0:loc>')}")
    except Exception as e:
        print(f"{sm}: ERROR {e}")
# sigil live
try:
    b = fetch("https://85e4e9f3.csoai-site.pages.dev/tick-284-sigil.json")
    print(f"sigil: HTTP {len(b)}b tick-284={b'tick-284' in b}")
except Exception as e:
    print(f"sigil: ERROR {e}")
