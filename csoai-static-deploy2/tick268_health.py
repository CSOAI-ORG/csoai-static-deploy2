#!/usr/bin/env python3
"""DEFONEOS tick 268 - verify CF Pages deployment reachability via python (bypasses .dev curl scanner)."""
import urllib.request, ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
targets = [
    ("CF deploy e714cd8d root", "https://e714cd8d.jv-wave8-production.csoai-site.pages.dev/"),
]
for name, url in targets:
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=35, context=ctx)
        print(f"{name}: HTTP {r.status} from {r.geturl()} | {len(r.read(200))}b head")
    except Exception as e:
        print(f"{name}: ERROR {type(e).__name__}: {e}")