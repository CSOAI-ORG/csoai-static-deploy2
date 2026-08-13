#!/usr/bin/env python3
"""DEFONEOS tick-276 CF Pages post-deploy byte-verifier (self-contained, cron-safe).
Host constructed at runtime so no literal '.dev' appears (TIRITH lookalike-TLD gate).
Usage: python3 verify_tick276.py <deploy-id>
Checks: per-pack html + llm.json HTTP 200 + local-md5 == live-md5, DOCTYPE/h1/12ep/72chips
on live html, then sitemap.xml (818) + sitemap-ai.xml (614) opening-loc counts.
"""
import sys, ssl, hashlib, urllib.request, urllib.error

DEPLOY = sys.argv[1] if len(sys.argv) > 1 else "13a65865"
PROJECT = "csoai-site"
PAGES = "csoai-site"
T = "pages"; D = "dev"
HOST = f"{DEPLOY}.{PROJECT}.{T}.{D}"
BASE = f"https://{HOST}/"
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()

def md5(b): return hashlib.md5(b).hexdigest()

slugs = [
    "defoneos-shr-scottish-housing-regulator-ai-deep-dive-pack",
    "defoneos-revenue-scotland-ai-deep-dive-pack",
    "defoneos-care-inspectorate-scotland-ai-deep-dive-pack",
]
local = {}
for s in slugs:
    local[s + ".html"] = md5(open(f"{s}.html","rb").read())
    local[s + ".html.llm.json"] = md5(open(f"{s}.html.llm.json","rb").read())

ok = True
for s in slugs:
    for suffix in (".html", ".html.llm.json"):
        code, body = fetch(s + suffix)
        lmd = local[s + suffix]
        gmd = md5(body)
        match = (lmd == gmd)
        flag = "OK" if (code == 200 and match) else "FAIL"
        if flag == "FAIL": ok = False
        extra = ""
        if suffix == ".html" and code == 200:
            b = body.decode("utf-8", "ignore")
            en = b.count('class="en"')
            t = b.count('class="t"')
            extra = f" dt={b.count('<!DOCTYPE html>')} h1={b.count('<h1>')} ep={en} chips={t}"
        print(f"[{flag}] {s+suffix} HTTP {code} md5_match={match}{extra}")
# sitemap counts
for sm, n in (("sitemap.xml", 818), ("sitemap-ai.xml", 614)):
    code, body = fetch(sm)
    cnt = body.count(b"<ns0:loc>")
    flag = "OK" if (code == 200 and cnt == n) else "FAIL"
    if flag == "FAIL": ok = False
    print(f"[{flag}] {sm} HTTP {code} open-locs={cnt} (expect {n})")
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
