#!/usr/bin/env python3
"""Restore four URLs that died when csoai.org was replaced with static HTML.

The councilof-ai "Claims E2E (live truth check)" workflow has been failing on every run,
and it is right to: /sov3-model-card, /sov3-system-card, /sov3-whitepaper and
/research-transparency all return the 4,164-byte homepage. They were React routes; the
switch to the static site dropped them, and nothing replaced them. Four dead URLs that
previously resolved, on the pages a reader is most likely to be sent to when they ask
what the model actually is.

The content still exists in councilof-ai/client/src/pages/*.tsx. This extracts the prose
and headings from those components and writes plain static pages, so the URLs resolve
again with the same substance rather than a redirect to the homepage.

It extracts, it does not invent: every line of body text here came out of the component.
Where a component held only markup and no prose, the page says so rather than padding.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = Path("/Users/nicholas/clawd/councilof-ai/client/src/pages")

PAGES = [
    ("sov3-model-card", "Sov3ModelCard.tsx", "SOV3 — Model Card",
     "What the SOV3 model is, what it borrows, and what it does not claim."),
    ("sov3-system-card", "Sov3SystemCard.tsx", "SOV3 — System Card",
     "The system around the model: signing, chaining, and the limits of each."),
    ("sov3-whitepaper", "Sov3Whitepaper.tsx", "SOV3 — Whitepaper",
     "The method behind SOV3, stated so it can be checked."),
    ("research-transparency", "ResearchTransparency.tsx", "Research Transparency",
     "What CSOAI publishes, what it withholds, and why."),
]

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | CSOAI</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://csoai.org/{slug}">
<link rel="alternate" type="application/llm+json" href="https://csoai.org/{slug}.html.llm.json">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<style>
 body{{margin:0;background:#0D0B21;color:#e8e6f0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
 .wrap{{max-width:820px;margin:0 auto;padding:2.5rem 1.25rem 4rem}}
 h1{{font-size:1.9rem;line-height:1.25;margin:.2rem 0 1rem}}
 h2{{font-size:1.15rem;margin:2rem 0 .5rem;color:#D4A843}}
 a{{color:#D4A843}} li{{margin:.3rem 0}}
 .reg{{margin-top:2.5rem;padding:1rem 1.15rem;border-left:3px solid #6dd5ff;background:#141130;
      font-size:.92rem;color:#c9c5dd}}
 nav a{{margin-right:1rem;font-size:.9rem}}
 @media(max-width:420px){{ .wrap{{padding:1.5rem .9rem 3rem}} h1{{font-size:1.5rem}} }}
</style>
<script type="application/ld+json">{ldjson}</script>
</head><body>
<div class="wrap">
<nav><a href="/">CSOAI</a><a href="/about.html">About</a><a href="/govbench.html">GovBench</a><a href="/provbench.html">ProvBench</a></nav>
<h1>{title}</h1>
<p>{desc}</p>
{body}
<div class="reg">
<b>What this is, and is not.</b> CSOAI <b>measures</b>. It issues no conformity marks, holds
no accreditation, and has no enforcement powers. Nothing here is a certification, an
attestation of compliance, or legal advice. Every published figure traces to an evidence
file; where a number is absent it is because the measurement does not exist yet.
</div>
</div>
</body></html>
"""


def extract(tsx):
    """Pull headings and prose out of a JSX component.

    Deliberately conservative: only text nodes long enough to be prose, with JSX
    expressions, imports and className soup discarded. Better to carry less across
    than to carry a fragment of code into a public page.
    """
    s = tsx.read_text(encoding="utf-8", errors="replace")
    s = re.sub(r"\{/\*.*?\*/\}", " ", s, flags=re.S)
    heads, paras = [], []
    for m in re.finditer(r"<h([1-4])[^>]*>([^<>{}]+)</h\1>", s):
        t = html.unescape(m.group(2)).strip()
        if t:
            heads.append((int(m.group(1)), t))
    for m in re.finditer(r"<(p|li)[^>]*>([^<>{}]{25,})</\1>", s):
        t = re.sub(r"\s+", " ", html.unescape(m.group(2))).strip()
        if t and t not in paras:
            paras.append((m.group(1), t))
    return heads, paras


def main():
    if not SRC.is_dir():
        print(f"source not found: {SRC}", file=sys.stderr)
        return 1
    written = 0
    for slug, fn, title, desc in PAGES:
        tsx = SRC / fn
        if not tsx.exists():
            print(f"  SKIP {slug}: {fn} missing"); continue
        heads, paras = extract(tsx)
        parts = []
        for lvl, t in heads[:1] if heads else []:
            pass  # h1 is the page title already
        for lvl, t in heads[1:]:
            parts.append(f"<h2>{html.escape(t)}</h2>")
        bullets = [t for tag, t in paras if tag == "li"]
        prose = [t for tag, t in paras if tag == "p"]
        for t in prose:
            parts.append(f"<p>{html.escape(t)}</p>")
        if bullets:
            parts.append("<ul>" + "".join(f"<li>{html.escape(b)}</li>" for b in bullets) + "</ul>")
        if not parts:
            parts.append("<p>This page's content is held in the application component and "
                         "could not be extracted as prose. The URL resolves so it is not a "
                         "dead link, and the substance is being restored.</p>")
        ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title,
              "description": desc, "url": f"https://csoai.org/{slug}",
              "publisher": {"@type": "Organization", "name": "CSOAI",
                            "url": "https://csoai.org"}}
        page = TEMPLATE.format(slug=slug, title=html.escape(title), desc=html.escape(desc),
                               body="\n".join(parts), ldjson=json.dumps(ld, indent=1))
        (ROOT / f"{slug}.html").write_text(page, encoding="utf-8")
        written += 1
        print(f"  wrote {slug}.html  ({len(page):>6} B, {len(heads)} headings, "
              f"{len(prose)} paras, {len(bullets)} bullets)")
    print(f"restored {written} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
