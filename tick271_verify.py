#!/usr/bin/env python3
import urllib.request, hashlib, re

base = "https://f5fe47aa.csoai-site.pages.dev"
packs = {
    "defoneos-prime-ministers-office-ai-deep-dive-pack": "c4672f8a17f334f39a03ad668c4489ec",
    "defoneos-welsh-government-ai-deep-dive-pack": "58f94add93066754a112855b0d5804eb",
    "defoneos-office-for-national-statistics-ai-deep-dive-pack": "1f44a95e07dfb49d05619c34992f0c32",
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"curl/8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()

for slug, md5 in packs.items():
    status, body = fetch(f"{base}/{slug}.html")
    live_md5 = hashlib.md5(body).hexdigest()
    ok_byte = (live_md5 == md5)
    h1 = b"<h1>" in body
    eps = body.count(b'<span class="en">Entry Point')
    chips = body.count(b'<span class="t">')
    lstatus, lbody = fetch(f"{base}/{slug}.html.llm.json")
    print(f"{slug}")
    print(f"   html: HTTP {status} md5={live_md5[:8]} byte_match={ok_byte} h1={h1} eps={eps} chips={chips}")
    print(f"   llm:  HTTP {lstatus} size={len(lbody)}")

s, sb = fetch(f"{base}/sitemap.xml")
print(f"\nsitemap.xml: HTTP {s} ns0:loc tags={len(re.findall(rb'<ns0:loc>', sb))} (expect 1606)")
s2, sb2 = fetch(f"{base}/sitemap-ai.xml")
print(f"sitemap-ai.xml: HTTP {s2} ns0:loc tags={len(re.findall(rb'<ns0:loc>', sb2))} (expect 1198)")
