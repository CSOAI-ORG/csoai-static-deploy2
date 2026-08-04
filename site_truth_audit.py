#!/usr/bin/env python3
"""site_truth_audit.py — do meok.ai and csoai.org do what they say?

Not a liveness check. Liveness is easy and already passes. This asks the harder question: for
every CLAIM the live surfaces make, is there something behind it?

FOUR CLASSES OF FAILURE, because they need different fixes
----------------------------------------------------------
UNREACHABLE     the URL does not serve                       -> infrastructure
INVISIBLE       serves 200 but a crawler sees no content     -> rendering
SOFT_404        serves 200 for a path that cannot exist      -> routing; every stale link and
                                                                crawler probe looks valid, so
                                                                nothing is ever deindexed
UNBACKED_CLAIM  a number or capability asserted on the page  -> honesty; this is the one that
                with no evidence file behind it                 matters to a measurement body

The last class is the point. A measurement company publishing an unevidenced number is not a
cosmetic defect — it is the failure its whole posture exists to prevent, and it is invisible to
every uptime monitor ever written.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EV = HERE / "evidence/harness/freeze/latest"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
# A crawler UA, because several surfaces are meant to serve prerendered content to bots.
BOT = {"User-Agent": "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)"}

ROUTES = {
    "csoai.org": ["/", "/benchmarks", "/gspc-verify", "/models", "/evidence", "/pricing",
                  "/article-50", "/compare", "/certification", "/.well-known/security.txt",
                  "/api/tools", "/robots.txt", "/sitemap.xml"],
    "www.meok.ai": ["/", "/badges", "/registry", "/systemcard", "/council"],
    "os.meok.ai": ["/", "/arena", "/sovspace"],
}
IMPOSSIBLE = "/this-path-cannot-exist-" + "9f3a2b7c1d"


def fetch(url, hdr=UA, timeout=25):
    try:
        r = urllib.request.Request(url, headers=hdr)
        with urllib.request.urlopen(r, timeout=timeout) as z:
            return z.status, z.read().decode("utf-8", "replace"), dict(z.headers)
    except urllib.error.HTTPError as e:
        return e.code, "", {}
    except Exception as e:
        return None, str(e)[:90], {}


def visible(html: str) -> str:
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    return " ".join(re.sub(r"<[^>]+>", " ", t).split())


def numbers_in(text: str) -> list[str]:
    """Quantitative claims a reader would take as fact. Deliberately narrow: bare years and
    small ordinals are not claims, so they are excluded rather than flagged as noise."""
    out = []
    for m in re.finditer(r"\b(\d[\d,]{1,9})\+?\s*"
                         r"(MCP servers?|MCP tools?|tools?|servers?|models?|provisions?|"
                         r"frameworks?|companies|benchmarks?|items?|axes)\b", text, re.I):
        out.append(m.group(0).strip())
    for m in re.finditer(r"\b\d{1,3}(\.\d+)?%", text):
        out.append(m.group(0))
    return sorted(set(out))


def main():
    findings = []
    pages = {}
    for host, paths in ROUTES.items():
        for p in paths:
            url = f"https://{host}{p}"
            st, body, hdrs = fetch(url)
            vis = visible(body) if body else ""
            pages[url] = {"status": st, "visible_chars": len(vis), "text": vis[:4000],
                          "ctype": hdrs.get("Content-Type", "")}
            if st is None:
                findings.append({"class": "UNREACHABLE", "url": url, "detail": body})
            elif st != 200:
                findings.append({"class": "UNREACHABLE", "url": url, "detail": f"HTTP {st}"})
            elif p.endswith((".txt", ".xml")) or p.startswith("/api/"):
                pass                                    # not HTML; no visibility expectation
            elif len(vis) < 200:
                findings.append({"class": "INVISIBLE", "url": url,
                                 "detail": f"HTTP 200 but {len(vis)} visible chars — a crawler "
                                           f"that does not execute JS sees nothing"})
        # soft-404 probe
        st, body, _ = fetch(f"https://{host}{IMPOSSIBLE}")
        if st == 200:
            findings.append({"class": "SOFT_404", "url": f"https://{host}{IMPOSSIBLE}",
                             "detail": "HTTP 200 for a path that cannot exist — every stale "
                                       "link and crawler probe looks valid, so nothing is "
                                       "ever deindexed"})

    # /api/tools must be JSON, not the SPA shell. This was a live P0 once and is worth asserting.
    st, body, hdrs = fetch("https://csoai.org/api/tools", hdr=BOT)
    if st == 200 and "json" not in hdrs.get("Content-Type", "").lower():
        findings.append({"class": "UNBACKED_CLAIM", "url": "https://csoai.org/api/tools",
                         "detail": f"machine-readable endpoint returns {hdrs.get('Content-Type')} "
                                   f"— an agent asking for the tool list gets HTML"})

    # crawler-vs-browser divergence: if a bot sees less than a browser, prerender is not working
    for url in [u for u in pages if u.endswith((".org/", ".ai/"))]:
        st, body, _ = fetch(url, hdr=BOT)
        bot_chars = len(visible(body)) if body else 0
        br = pages[url]["visible_chars"]
        if br > 400 and bot_chars < br * 0.5:
            findings.append({"class": "INVISIBLE", "url": url,
                             "detail": f"browser sees {br} chars, GPTBot sees {bot_chars} — "
                                       f"prerendering is not reaching crawlers"})

    # unbacked numeric claims
    known = {}
    for f, key in [("mcp-census-strict.json", "mcp"), ("axis-saturation.json", "axes")]:
        p = EV / f
        if p.exists():
            known[key] = json.loads(p.read_text())
    live_tools = (known.get("mcp", {}).get("LIVE", {}) or {}).get("total_tools")
    live_servers = (known.get("mcp", {}).get("LIVE", {}) or {}).get("server_count")
    disk_mcp = (known.get("mcp", {}).get("ON_DISK", {}) or {}).get("strict_implementations")

    for url, d in pages.items():
        for claim in numbers_in(d["text"]):
            m = re.match(r"([\d,]+)\+?\s*(MCP servers?|MCP tools?|servers?|tools?)", claim, re.I)
            if not m:
                continue
            n = int(m.group(1).replace(",", ""))
            if n in (live_tools, live_servers, disk_mcp):
                continue
            findings.append({"class": "UNBACKED_CLAIM", "url": url,
                             "detail": f'page says "{claim}" — measured: {live_tools} tools '
                                       f'across {live_servers} servers live, {disk_mcp} '
                                       f'implementations on disk. No evidence file supports '
                                       f'{n}.'})

    by = {}
    for f in findings:
        by.setdefault(f["class"], []).append(f)
    print(f"SITE TRUTH AUDIT — {len(pages)} URLs, {len(findings)} findings\n")
    for cls in ("UNREACHABLE", "SOFT_404", "INVISIBLE", "UNBACKED_CLAIM"):
        got = by.get(cls, [])
        print(f"  {cls}: {len(got)}")
        for f in got[:12]:
            print(f"    {f['url']}")
            print(f"      {f['detail']}")
        print()

    out = EV / "site-truth-audit.json"
    out.write_text(json.dumps({
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "method": "unauthenticated GET as browser and as GPTBot; no cached state",
        "classes": {"UNREACHABLE": "URL does not serve",
                    "SOFT_404": "200 for an impossible path — nothing ever deindexes",
                    "INVISIBLE": "200 but no content without JS execution",
                    "UNBACKED_CLAIM": "a number on the page with no evidence file behind it"},
        "n_urls": len(pages), "n_findings": len(findings),
        "summary": {k: len(v) for k, v in by.items()},
        "findings": findings,
        "pages": {u: {k: v for k, v in d.items() if k != "text"} for u, d in pages.items()},
    }, indent=2))
    print(f"  -> {out}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
