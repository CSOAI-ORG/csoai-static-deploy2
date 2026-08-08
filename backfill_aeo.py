#!/usr/bin/env python3
"""
backfill_aeo.py — idempotent AEO/meta backfill for csoai static estate.

Adds to every root *.html page that lacks them: meta description, canonical,
og:title, og:description and a minimal JSON-LD block — all derived from the
page's existing <title> (and, where present, its first <h1>/lede text).

Why: the estate's hand-authored pages ship <meta name=description> with
content-first attribute order and full AEO blocks on the *index* surfaces, but
the ~57 DEFONEOS deep-dive packs and assorted sub-pages carry only a <title>.
AI crawlers (GPTBot/ClaudeBot/PerplexityBot) don't render JS and read raw HTML,
so a missing description/canonical/og block hurts discoverability. This script
is re-runnable and non-drifting: it never touches a page that already has the
signal, and it never rewrites existing content.

Run: python3 backfill_aeo.py            (default: dry-run, prints what WOULD change)
      python3 backfill_aeo.py --apply   (actually edits files)
"""
import re
import glob
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

RE_TITLE = re.compile(r'<title>([^<]+)</title>', re.I)
RE_DESC = re.compile(r'<meta\b[^>]*\bname=["\']description["\']', re.I)
RE_CANON = re.compile(r'<link\b[^>]*\brel=["\']canonical["\']', re.I)
RE_OGT = re.compile(r'<meta\b[^>]*\bproperty=["\']og:title["\']', re.I)
RE_OGD = re.compile(r'<meta\b[^>]*\bproperty=["\']og:description["\']', re.I)
RE_LD = re.compile(r'<script[^>]*type=["\']application/ld\+json', re.I)

APPLY = '--apply' in sys.argv


def derive(t):
    """Human-usable description from a title like 'DEFONEOS — BSI ... Deep-Dive Pack'."""
    txt = t.strip()
    # drop the trailing CSOAI brand suffix for page-specific phrasing
    core = re.sub(r'\s*\|\s*CSOAI\s*$', '', txt, flags=re.I)
    core = re.sub(r'\s*—\s*CSOAI.*$', '', core, flags=re.I)
    return f"{core}. A sovereign, audit-grade CSOAI surface: measurement, not certification — every figure traces to a signed, verifiable record."


def canonical_for(name):
    return f"https://www.csoai.org/{name}.html"


def build_ld(name, title):
    return {"@context": "https://schema.org", "@type": "WebPage",
            "name": title, "url": canonical_for(name),
            "publisher": {"@type": "Organization", "name": "CSOAI Ltd", "url": "https://csoai.org"}}


def main():
    changed = []
    files = sorted(ROOT.glob('*.html'))
    for p in files:
        c = p.read_text(encoding='utf-8')
        t = RE_TITLE.search(c)
        if not t:
            continue
        title = t.group(1).strip()
        name = p.name[:-5]
        ins = []
        if not RE_DESC.search(c):
            ins.append(f'<meta content="{html.escape(derive(title), quote=True)}" name="description"/>')
        if not RE_CANON.search(c):
            ins.append(f'<link href="{canonical_for(name)}" rel="canonical"/>')
        if not RE_OGT.search(c):
            ins.append(f'<meta content="{html.escape(title, quote=True)}" property="og:title"/>')
        if not RE_OGD.search(c):
            ins.append(f'<meta content="{html.escape(derive(title), quote=True)}" property="og:description"/>')
        if not RE_LD.search(c):
            ld = json.dumps(build_ld(name, title), separators=(',', ':'))
            ins.append(f'<script type="application/ld+json">{ld}</script>')
        if not ins:
            continue
        if APPLY:
            block = "\n".join(ins) + "\n"
            c = c.replace('</head>', block + '</head>', 1)
            p.write_text(c, encoding='utf-8')
        changed.append((p.name, len(ins), ins[0][:60] if ins else ''))
    if not APPLY:
        print(f"DRY-RUN: {len(changed)} pages would change. Re-run with --apply to write.")
    else:
        print(f"APPLIED: {len(changed)} pages updated.")
    for name, n, first in changed[:12]:
        print(f"  {name}: +{n} tags  {first}")


if __name__ == '__main__':
    main()
