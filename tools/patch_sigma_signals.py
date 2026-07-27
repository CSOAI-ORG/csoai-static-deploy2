#!/usr/bin/env python3
"""Patch defoneos-*.html files to add missing SIGMA sovereign signals (S4, S6, S8)."""

import glob
import re
import os
from html.parser import HTMLParser


BASE_URL = "https://csoai-sovereign.pages.dev"
DATE_MODIFIED = "2026-07-25"

S4_JSON_LD_TEMPLATE = """\
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{headline}",
    "description": "{description}",
    "url": "{url}",
    "author": {{"@type": "Organization", "name": "CSOAI Ltd (UK 16939677)"}},
    "publisher": {{"@type": "Organization", "name": "DEFONEOS", "url": "{base_url}"}},
    "dateModified": "{date_modified}"
  }}
  </script>"""

S6_NAV_HTML = """\
<nav class="sovereign-nav"><a href="/index.html">CSOAI</a> · <a href="/defoneos.html">DEFONEOS</a> · <a href="/master.html">Sovereign Hub</a> · <a href="/defoneos-pilot-30-day-consolidated-pack.html">30-Day Pilot</a></nav>"""

S8_CTA_HTML = """\
<div class="sovereign-cta-strip" data-marker="SOVEREIGN_CTA" style="background:rgba(34,211,238,.06);border-top:1px solid rgba(34,211,238,.15);padding:1rem 1.5rem;text-align:center;font-size:.82rem;color:#94a3b8">
  <a href="master.html" style="color:#22d3ee;text-decoration:none;font-weight:600;margin:0 .8rem">Sovereign Hub</a>
  <a href="/tools/article50-passport.html" style="color:#fbbf24;text-decoration:none;font-weight:600;margin:0 .8rem">Article 50 Passport</a>
  <a href="defoneos-owem-rfq.html" style="color:#a78bfa;text-decoration:none;font-weight:600;margin:0 .8rem">OWEM RFQ</a>
  <span style="margin:0 .8rem;color:#64748b">CSOAI Ltd · UK 16939677 · Care Floor 0.95 · Charter-anchored</span>
</div>"""


def extract_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else "DEFONEOS Page"


def extract_meta_description(html):
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    m = re.search(
        r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    return m.group(1).strip() if m else "DEFONEOS sovereign AI platform page"


def patch_s4(html, filename):
    """Add JSON-LD Article schema if missing."""
    has_article = '"@type"' in html and '"Article"' in html
    if has_article:
        return html, False

    title = extract_title(html)
    desc = extract_meta_description(html)
    url = f"{BASE_URL}/{filename}"

    json_ld = S4_JSON_LD_TEMPLATE.format(
        headline=title,
        description=desc,
        url=url,
        base_url=BASE_URL,
        date_modified=DATE_MODIFIED,
    )

    title_match = re.search(r"</title>", html, re.IGNORECASE)
    if title_match:
        insert_pos = title_match.end()
        html = html[:insert_pos] + "\n" + json_ld + html[insert_pos:]
        return html, True

    return html, False


def patch_s6(html):
    """Add sovereign-nav link to master.html if missing."""
    has_master = "master.html" in html or "SOV33_OWEM_HUB.html" in html
    if has_master:
        return html, False

    body_tag = re.search(r"<body[^>]*>", html, re.IGNORECASE)
    if body_tag:
        insert_pos = body_tag.end()
        html = html[:insert_pos] + "\n" + S6_NAV_HTML + html[insert_pos:]
        return html, True

    return html, False


def patch_s8(html):
    """Add sovereign-cta-strip before </body> if missing."""
    has_cta = "article50-passport.html" in html or "defoneos-article-50.html" in html or "defoneos-owem-rfq.html" in html
    if has_cta:
        return html, False

    body_close = html.rfind("</body>")
    if body_close != -1:
        html = html[:body_close] + "\n" + S8_CTA_HTML + "\n" + html[body_close:]
        return html, True

    return html, False


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pattern = os.path.join(base_dir, "defoneos-*.html")
    files = sorted(glob.glob(pattern))

    if not files:
        print("No defoneos-*.html files found.")
        return

    print(f"Found {len(files)} defoneos-*.html files.\n")

    s4_patched = []
    s6_patched = []
    s8_patched = []

    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        original = html
        html, s4 = patch_s4(html, filename)
        html, s6 = patch_s6(html)
        html, s8 = patch_s8(html)

        if s4:
            s4_patched.append(filename)
        if s6:
            s6_patched.append(filename)
        if s8:
            s8_patched.append(filename)

        if html != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)

    print("=== SIGMA Signal Patch Report ===\n")
    print(f"S4 (JSON-LD Article schema):  {len(s4_patched)} files patched")
    if s4_patched:
        for f in s4_patched[:10]:
            print(f"  + {f}")
        if len(s4_patched) > 10:
            print(f"  ... and {len(s4_patched) - 10} more")

    print(f"\nS6 (master.html nav link):    {len(s6_patched)} files patched")
    if s6_patched:
        for f in s6_patched[:10]:
            print(f"  + {f}")
        if len(s6_patched) > 10:
            print(f"  ... and {len(s6_patched) - 10} more")

    print(f"\nS8 (CTA to article-50/RFQ):   {len(s8_patched)} files patched")
    if s8_patched:
        for f in s8_patched[:10]:
            print(f"  + {f}")
        if len(s8_patched) > 10:
            print(f"  ... and {len(s8_patched) - 10} more")

    total = len(set(s4_patched + s6_patched + s8_patched))
    print(f"\nTotal unique files modified: {total}")


if __name__ == "__main__":
    main()
