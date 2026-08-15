#!/usr/bin/env python3
"""Tick 266 — live deployment health checks (CF Pages + apex)."""
import subprocess, sys

URLS = [
    "https://jv-wave8-production.csoai-site.pages.dev/",
    "https://jv-wave8-production.csoai-site.pages.dev/sitemap.xml",
    "https://jv-wave8-production.csoai-site.pages.dev/defoneos-uk-supreme-court-appellate-governance-ai-deep-dive-pack.html",
    "https://jv-wave8-production.csoai-site.pages.dev/defoneos-royal-society-scientific-advice-ai-deep-dive-pack.html",
    "https://jv-wave8-production.csoai-site.pages.dev/defoneos-sentencing-council-england-wales-ai-deep-dive-pack.html",
    "https://www.csoai.org/",
]

for u in URLS:
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}|%{redirect_url}", "-m", "20", u],
            capture_output=True, text=True, timeout=30,
        )
        print(f"{r.stdout}  {u}")
    except Exception as e:
        print(f"ERR {e}  {u}")

print("---build_site verification flags---")
out = subprocess.run(["grep", "-n", "argparse\\|--verify\\|--check\\|missing\\|leaks", "build_site.py"],
                     capture_output=True, text=True, cwd="/Users/nicholas/clawd/csoai-static-deploy2")
print(out.stdout[:2000])
sys.exit(0)