#!/usr/bin/env python3
"""Tick 281: post-deploy byte-verification against the live CF Pages deployment."""
import hashlib, json, re, ssl, urllib.request

BASE = "https://34be85fc.csoai-site.pages.dev"
SLUGS = [
    "defoneos-education-authority-northern-ireland-ai-deep-dive-pack",
    "defoneos-scottish-legal-aid-board-ai-deep-dive-pack",
    "defoneos-social-security-scotland-ai-deep-dive-pack",
]
ctx = ssl._create_unverified_context()
HDRS = {"User-Agent": "Mozilla/5.0 (tick281-verify)"}

def fetch(path):
    req = urllib.request.Request(BASE + path, headers=HDRS)
    with urllib.request.urlopen(req, context=ctx, timeout=40) as r:
        return r.status, r.read()

print("=== live byte-verification on", BASE, "===")
ok = True
for s in SLUGS:
    st, body = fetch(f"/{s}.html")
    md5 = hashlib.md5(body).hexdigest()
    doc = body.decode("utf-8", "replace")
    en = len(re.findall(r'class="en">Entry Point', doc))
    h2 = len(re.findall(r"<h2>", doc))
    h1 = len(re.findall(r"<h1>", doc))
    mcps = len(re.findall(r'class="t">mcp-', doc))
    has_doc = doc.lstrip().startswith("<!DOCTYPE html>")
    print(f"{s}\n  HTTP {st}  md5={md5[:8]}  doctype={has_doc}  h1={h1} en={en} h2={h2} mcp_chips={mcps}")
    stl, llm = fetch(f"/{s}.html.llm.json")
    lmd5 = hashlib.md5(llm).hexdigest()
    try:
        json.loads(llm); llm_ok = True
    except Exception:
        llm_ok = False
    print(f"  llm.json HTTP {stl}  md5={lmd5[:8]}  json_parseable={llm_ok}")
    if not (st == 200 and has_doc and h1 == 1 and en == 12 and h2 == 12 and mcps == 72 and stl == 200 and llm_ok):
        ok = False

# sitemaps live with all 3 slugs present
for fn, expect in [("sitemap.xml", 833), ("sitemap-ai.xml", 629)]:
    st, body = fetch(f"/{fn}")
    txt = body.decode("utf-8", "replace")
    n = len(re.findall(r"<ns0:loc>", txt))
    present = all(s + ".html" in txt for s in SLUGS)
    print(f"{fn} HTTP {st}  loc_count={n} (expect {expect})  all3_present={present}")
    if not (st == 200 and n == expect and present):
        ok = False

print("RESULT:", "PASS" if ok else "FAIL")
