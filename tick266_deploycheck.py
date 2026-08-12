#!/usr/bin/env python3
"""Tick 266 — post-deploy verification on the live pages.dev domain."""
import subprocess

URLS = [
    "https://csoai-site.pages.dev/sitemap.xml",
    "https://csoai-site.pages.dev/defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack.html",
    "https://csoai-site.pages.dev/defoneos-judicial-appointments-commission-ai-deep-dive-pack.html",
    "https://csoai-site.pages.dev/defoneos-british-academy-humanities-social-sciences-ai-deep-dive-pack.html",
    "https://jv-wave8-production.csoai-site.pages.dev/defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack.html",
]
for u in URLS:
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}|%{size_download}|%{redirect_url}", "-L", "-m", "25", u],
            capture_output=True, text=True, timeout=30,
        )
        print(f"{r.stdout}  {u}")
    except Exception as e:
        print(f"ERR {e}  {u}")
