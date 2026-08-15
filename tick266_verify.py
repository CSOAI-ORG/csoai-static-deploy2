#!/usr/bin/env python3
"""Tick 266 — byte-verify the 3 new packs (structure + canonical JSON-LD)."""
import json, re
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
slugs = [
    "defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack",
    "defoneos-judicial-appointments-commission-ai-deep-dive-pack",
    "defoneos-british-academy-humanities-social-sciences-ai-deep-dive-pack",
]
all_ok = True
for s in slugs:
    h = (ROOT / f"{s}.html").read_text()
    ok_doctype = h.startswith("<!DOCTYPE html>")
    ok_html_close = h.rstrip().endswith("</html>")
    n_ep = h.count('class="sh"')
    n_pri = h.count('class="p"')
    n_mcp = h.count('class="t"')
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    ld = json.loads(m.group(1)) if m else None
    canonical = ld is not None and ld.get("@type") == "WebPage" and ld.get("@context") == "https://schema.org"
    bad = (n_ep != 12) or (n_pri != 96) or (n_mcp != 72) or (not ok_doctype) or (not ok_html_close) or (not canonical)
    all_ok = all_ok and not bad
    print(f"{s}: DOCTYPE={ok_doctype} close={ok_html_close} ep={n_ep} pri={n_pri} mcp={n_mcp} ld_canonical={canonical} {'OK' if not bad else 'FAIL'}")

# Also verify llm.json url field correctness
for s in slugs:
    lj = json.loads((ROOT / f"{s}.html.llm.json").read_text())
    url_ok = lj.get("url") == f"https://csoai.org/{s}.html"
    heads_ok = len(lj.get("headings", [])) == 13  # 1 title + 12 entry points
    print(f"{s}.llm.json: url_ok={url_ok} headings={len(lj.get('headings',[]))} type={lj.get('type')}")
    all_ok = all_ok and url_ok and heads_ok

print("\nALL_VERIFY_OK" if all_ok else "\nVERIFY_FAILED")