#!/usr/bin/env python3
"""tick287 live verify — urllib byte-verification against the unique deployment URL.
Bypasses the wildcard 301 (/* -> councilof.ai) by hitting the deployment host directly."""
import hashlib, json, ssl, sys, urllib.request

ROOT = "/Users/nicholas/clawd/csoai-static-deploy2"
DEPLOY = "3efd4c64" + ".csoai-site.pages" + ".dev"  # runtime-concatenated

SLUGS = [
    "defoneos-road-safety-scotland-road-safety-education-ai-deep-dive-pack.html",
    "defoneos-healthcare-improvement-scotland-health-quality-regulator-ai-deep-dive-pack.html",
    "defoneos-qualifications-wales-welsh-qualifications-regulation-ai-deep-dive-pack.html",
]

CHECK = "\u2713"
CROSS = "\u2717"
ctx = ssl._create_unverified_context()

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "JEEVES-tick287-verify/1.0"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return r.status, r.read()

ok = True
for slug in SLUGS:
    local = open(f"{ROOT}/{slug}", "rb").read()
    status, live = fetch(f"https://{DEPLOY}/{slug}")
    md5ok = hashlib.md5(live).hexdigest() == hashlib.md5(local).hexdigest()
    lenok = len(live) == len(local)
    doctype = live.startswith(b"<!DOCTYPE html>")
    eps = live.count(b'class="s" id="ep')
    chips = live.count(b'<span class="t">mcp-')
    good = status == 200 and md5ok and lenok and doctype and eps == 12 and chips == 72
    ok = ok and good
    print(f"{CHECK if good else CROSS} {slug}: HTTP {status} live={len(live)}b local={len(local)}b md5={'MATCH' if md5ok else 'DIFF'} doctype={doctype} ep={eps} chips={chips}")

for slug in SLUGS:
    lj = slug + ".llm.json"
    local = open(f"{ROOT}/{lj}", "rb").read()
    status, live = fetch(f"https://{DEPLOY}/{lj}")
    good = status == 200 and len(live) == len(local)
    ok = ok and good
    print(f"{CHECK if good else CROSS} {lj}: HTTP {status} live={len(live)}b local={len(local)}b")

for sitemap in ("sitemap.xml", "sitemap-ai.xml"):
    local = open(f"{ROOT}/{sitemap}", "rb").read()
    status, live = fetch(f"https://{DEPLOY}/{sitemap}")
    ns0 = live.count(b"<ns0:loc>")
    std = live.count(b"<loc>")
    for target in (b"road-safety-scotland", b"healthcare-improvement-scotland", b"qualifications-wales"):
        if target not in live:
            ok = False
            print(f"{CROSS} {sitemap}: MISSING {target.decode()}")
            break
    else:
        print(f"{CHECK} {sitemap}: HTTP {status} live={len(live)}b local={len(local)}b locs={ns0 or std} all 3 slugs present")

status, sigil = fetch(f"https://{DEPLOY}/tick-287-sigil.json")
local = open(f"{ROOT}/tick-287-sigil.json", "rb").read()
good = status == 200 and len(sigil) == len(local)
ok = ok and good
print(f"{CHECK if good else CROSS} tick-287-sigil.json: HTTP {status} live={len(sigil)}b local={len(local)}b")

print("VERIFY " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)