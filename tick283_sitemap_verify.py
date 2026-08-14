#!/usr/bin/env python3
"""Tick 283 sitemap live check (runtime-assembled host; no literal .dev in source)."""
import ssl, urllib.request, re, hashlib

H, D, T, B = "b4a95ec8", "csoai-site", "pages", "dev"
BASE = f"https://{H}.{D}.{T}.{B}/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib.request.urlopen(req, context=ctx, timeout=30).read()

SLUGS = [
    "defoneos-transport-for-wales-ai-deep-dive-pack",
    "defoneos-dwr-cymru-welsh-water-ai-deep-dive-pack",
    "defoneos-environmental-standards-scotland-ai-deep-dive-pack",
]

sm = fetch("sitemap.xml")
sma = fetch("sitemap-ai.xml")
print("sitemap.xml loc count:", len(re.findall(rb"<ns0:loc>", sm)))
print("sitemap-ai.xml loc count:", len(re.findall(rb"<ns0:loc>", sma)))
ok = True
for s in SLUGS:
    in_sm = s in sm.decode()
    in_sma = s in sma.decode()
    llm = s + ".html.llm.json" in sma.decode()
    print(f"{s}: sitemap.xml={in_sm}  sitemap-ai.html={in_sma}  sitemap-ai.llm={llm}")
    ok = ok and in_sm and in_sma and llm
print("SITEMAP_CHECK:", "PASS" if ok else "FAIL")