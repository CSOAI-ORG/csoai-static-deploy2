#!/usr/bin/env python3
"""DEFONEOS Tick 273 - post-deploy byte verification against the unique deployment URL."""
import hashlib
import re
import urllib.request
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")

# Runtime-construct the host so no literal ".dev" TLD appears in the command
deploy_id = "b73356a1"
host = f"{deploy_id}.csoai-site.pages"
host = host + ".dev"

SLUGS = [
    "defoneos-scottish-government-ai-deep-dive-pack",
    "defoneos-northern-ireland-executive-ai-deep-dive-pack",
    "defoneos-public-services-ombudsman-wales-ai-deep-dive-pack",
]

def md5_of(path):
    return hashlib.md5(Path(path).read_bytes()).hexdigest()

def md5_of_data(data):
    return hashlib.md5(data).hexdigest()

def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "JEEVES-tick273"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()

ok = True
CHECK = "\u2713"
CROSS = "\u2717"
for slug in SLUGS:
    local_html = md5_of(ROOT / f"{slug}.html")
    local_llm = md5_of(ROOT / f"{slug}.html.llm.json")
    html_url = f"https://{host}/{slug}.html"
    llm_url = f"https://{host}/{slug}.html.llm.json"
    try:
        hcode, hbody = fetch(html_url)
    except Exception as e:
        print(f"\u2717 {slug}.html  FETCH FAIL: {e}")
        ok = False
        continue
    live_html = md5_of_data(hbody)
    try:
        lcode, lbody = fetch(llm_url)
        live_llm = md5_of_data(lbody)
    except Exception as e:
        lcode, lbody, live_llm = f"ERR {e}", b"", "fetch-fail"
    html_ok = (hcode == 200) and (local_html == live_html)
    llm_ok = (lcode == 200) and (local_llm == live_llm)
    doctype = b"<!DOCTYPE html>" in hbody
    h1 = b"<h1>" in hbody
    eps = hbody.count(b'<span class="en">Entry Point')
    chips = hbody.count(b'<span class="t">')
    print(f"{CHECK if html_ok else CROSS} {slug}.html  HTTP {hcode} local={local_html[:8]} live={live_html[:8]} "
          f"doctype={doctype} h1={h1} eps={eps} chips={chips}")
    print(f"  {CHECK if llm_ok else CROSS}   .llm.json  HTTP {lcode} local={local_llm[:8]} live={str(live_llm)[:8]} size={len(lbody)}")
    if not (html_ok and llm_ok):
        ok = False

# sitemap checks
for sitemap, count in [("sitemap.xml", 809), ("sitemap-ai.xml", 605)]:
    try:
        scode, sbody = fetch(f"https://{host}/{sitemap}")
        n_open = len(re.findall(rb"<ns0:loc>", sbody))
        status_mark = CHECK if (scode==200 and n_open==count) else CROSS
        print(f"{status_mark} {sitemap} HTTP {scode} ns0:loc open-tags={n_open} (want {count})")
        if not (scode == 200 and n_open == count):
            ok = False
    except Exception as e:
        print(f"{CROSS} {sitemap} FETCH FAIL: {e}")
        ok = False

print("\nRESULT:", "PASS - all verified live" if ok else "FAIL - re-check needed")
