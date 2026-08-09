#!/usr/bin/env python3
"""Generate the .llm.json companions that 249 alternate links already promise.

Every page emits <link rel="alternate" type="application/llm+json" href="…llm.json">,
the machine-readable version for AI crawlers. None of the files existed. All 249 links
resolved to the homepage with content-type text/html — so a crawler following the
alternate link got the homepage and no error, on the estate whose entire AEO thesis is
machine-readable surfaces.

Two bugs, one now fixed in the HTML and one fixed here:
  1. 112 of the URLs were built as origin + filename with no separator
     ("https://www.csoai.orgcouncil.html.llm.json"), which does not resolve at all.
  2. The files were never generated. This script generates them.

Content is extracted from the page itself — no claim is invented here, and nothing is
asserted that the HTML does not already say.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TAG = re.compile(r"<(script|style|noscript)[^>]*>.*?</\1>", re.S | re.I)
ANYTAG = re.compile(r"<[^>]+>")


def text_of(s):
    s = TAG.sub(" ", s)
    s = ANYTAG.sub(" ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def meta(s, name):
    m = re.search(rf'<meta[^>]+name=["\']{name}["\'][^>]*content=["\']([^"\']*)', s, re.I)
    if not m:
        m = re.search(rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]*name=["\']{name}["\']', s, re.I)
    return html.unescape(m.group(1)).strip() if m else ""


def build(path):
    s = path.read_text(encoding="utf-8", errors="replace")
    t = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    title = html.unescape(t.group(1)).strip() if t else path.stem
    heads = [text_of(m.group(1))
             for m in re.finditer(r"<h[12][^>]*>(.*?)</h[12]>", s, re.S | re.I)]
    body = text_of(s)
    canonical = ""
    c = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', s, re.I)
    if c:
        canonical = c.group(1)
    return {
        "@context": "https://csoai.org/llm-context.json",
        "type": "LLMPageSummary",
        "url": canonical or f"https://csoai.org/{path.name}",
        "title": title,
        "description": meta(s, "description"),
        "headings": [h for h in heads if h][:12],
        "text": body[:4000],
        "text_truncated": len(body) > 4000,
        "register": {
            "role": "measurement_and_attestation_support",
            "csoai_certifies_systems": False,
            "csoai_is_a_notified_body": False,
            "csoai_has_enforcement_powers": False,
            "note": ("CSOAI measures and publishes evidence. It issues no conformity "
                     "marks and holds no accreditation. Nothing here is certification "
                     "or legal advice."),
        },
        "generated_by": "make_llm_json.py",
    }


def main():
    check = "--check" in sys.argv
    pages = sorted(set(ROOT.glob("*.html")) | set(ROOT.glob("tools/*.html")))
    written = 0
    for p in pages:
        out = p.with_suffix(p.suffix + ".llm.json")   # foo.html -> foo.html.llm.json
        data = build(p)
        if check:
            continue
        out.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
        written += 1
    # The homepage is linked as /.llm.json
    idx = ROOT / "index.html"
    if idx.exists() and not check:
        (ROOT / ".llm.json").write_text(
            json.dumps(build(idx), indent=1, ensure_ascii=False), encoding="utf-8")
        written += 1

    # Emit files for the paths the pages ACTUALLY link to, which are not always
    # <name>.html.llm.json. Two shapes exist in the HTML: some links drop the .html
    # ("/compare.llm.json"), and pages living in tools/ canonicalise at the root
    # ("/bft-council.html.llm.json" for tools/bft-council.html). Generating what we
    # think the name should be, rather than what is linked, leaves the link broken —
    # which is the entire defect being fixed here.
    linked = set()
    link_rx = re.compile(r'href="(?:https?://[a-z.]*csoai\.org)?(/[^"]*?llm\.json)"', re.I)
    for p in pages:
        for m in link_rx.finditer(p.read_text(encoding="utf-8", errors="replace")):
            linked.add(m.group(1))

    by_stem = {}
    for p in pages:
        by_stem.setdefault(p.name, p)                    # foo.html
        by_stem.setdefault(p.stem, p)                    # foo
    aliases = 0
    for href in sorted(linked):
        dst = ROOT / href.lstrip("/")
        if dst.exists() or check:
            continue
        base = href.lstrip("/")[: -len(".llm.json")]
        src = by_stem.get(base) or by_stem.get(base + ".html")
        if not src:
            print(f"  no page behind linked companion {href} — not inventing one")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(build(src), indent=1, ensure_ascii=False), encoding="utf-8")
        aliases += 1
    print(f"pages: {len(pages)}   .llm.json written: {written}   linked-path aliases: {aliases}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
