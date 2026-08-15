#!/usr/bin/env python3
"""Tick 259 deploy verification — fetch pages.dev URLs WITHOUT following redirects
to prove the deployment host itself serves the new files (200) before the
documented wildcard 301->councilof.ai redirect on the public apex kicks in."""
import urllib.request

HOST = "jv-wave8-production.csoai-site.pages.dev"
pages = [
    "defoneos-insolvency-service-corporate-insolvency.html",
    "defoneos-money-pensions-service-guidance.html",
    "defoneos-sports-grounds-safety-authority.html",
    "defoneos-office-for-students-higher-education-regulation-ai-deep-dive-pack.html",
    "sitemap.xml",
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = urllib.request.build_opener(NoRedirect)
for p in pages:
    url = f"https://{HOST}/{p}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"})
    try:
        with opener.open(req, timeout=30) as r:
            data = r.read()
            print(f"{p}  HTTP={r.status}  bytes={len(data)}  type={r.headers.get('Content-Type')}")
    except urllib.error.HTTPError as e:
        body = e.read()[:80]
        print(f"{p}  HTTP={e.code}  loc={e.headers.get('Location')}  body={body!r}")
    except Exception as e:
        print(f"{p}  EXC={e}")
