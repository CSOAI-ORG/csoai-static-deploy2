#!/usr/bin/env python3
"""Tick 278 live byte-verify on unique deployment URL."""
import urllib.request, hashlib, ssl
CTX = ssl._create_unverified_context()
base = "https://83c3c78e.csoai-site.pages.dev/"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) DEFONEOS-deploy-verify"}
slugs = ["sqa-scottish-qualifications-authority","disclosure-scotland","skills-development-scotland"]
allok = True
for s in slugs:
    slug = f"defoneos-{s}-ai-deep-dive-pack"
    for suffix in [".html", ".html.llm.json"]:
        url = base + slug + suffix
        try:
            req = urllib.request.Request(url, headers=UA)
            body = urllib.request.urlopen(req, timeout=30, context=CTX).read()
            m = hashlib.md5(body).hexdigest()
            local = f"{slug}{suffix}"
            lm = hashlib.md5(open(local,'rb').read()).hexdigest()
            ok = (m == lm)
            allok = allok and ok
            print(f"{suffix:18s} HTTP200 md5={m[:8]} byte-match={ok}")
            if suffix == ".html":
                txt = body.decode('utf-8', 'ignore')
                chip = '<span class="t">'
                print(f"   DOCTYPE={txt.count('<!DOCTYPE html>')} h1={txt.count('<h1>')} eps12={txt.count('Entry Point 01')>0} mcpchips={txt.count(chip)}")
        except Exception as e:
            allok = False
            print(f"{suffix} ERROR {e}")
for sm in ["sitemap.xml","sitemap-ai.xml"]:
    try:
        req = urllib.request.Request(base+sm, headers=UA)
        b = urllib.request.urlopen(req, timeout=30, context=CTX).read().decode('utf-8','ignore')
        print(f"{sm} HTTP200 loc={b.count('<ns0:loc>')} sqa={b.count('sqa-scottish')} disclosure={b.count('disclosure-scotland')} sds={b.count('skills-development')}")
    except Exception as e:
        allok=False; print(f"{sm} ERROR {e}")
print("ALL LIVE BYTE-VERIFIED:", allok)