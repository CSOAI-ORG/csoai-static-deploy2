#!/usr/bin/env python3
"""Tick 268 - confirm canonical serving host for DEFONEOS packs."""
import urllib.request, ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent':'Mozilla/5.0'}
tests = [
    ("csoai.org pack path", "https://csoai.org/defoneos-press-recognition-panel-ai-deep-dive-pack.html"),
    ("csoai.org root",       "https://csoai.org/"),
    ("CF pages prod root",   "https://jv-wave8-production.csoai-site.pages.dev/"),
]
for name, url in tests:
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=35, context=ctx)
        b = r.read()
        print(f"{name:26s} HTTP {r.status} final={r.geturl()} {len(b)}b doctype={b[:9]==b'<!DOCTYPE'}")
    except Exception as e:
        print(f"{name:26s} ERROR {type(e).__name__}: {e}")