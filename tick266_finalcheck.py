#!/usr/bin/env python3
"""Tick 266 — verify packs on the just-deployed CF Pages deployment."""
import subprocess

BASE = "https://e815af59.csoai-site.pages.dev"
URLS = [
    f"{BASE}/defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack.html",
    f"{BASE}/defoneos-judicial-appointments-commission-ai-deep-dive-pack.html",
    f"{BASE}/defoneos-british-academy-humanities-social-sciences-ai-deep-dive-pack.html",
    f"{BASE}/defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack.html.llm.json",
    f"{BASE}/sitemap.xml",
]
for u in URLS:
    r = subprocess.run(["curl", "-s", "-L", "-m", "25", u], capture_output=True, text=True, timeout=30)
    body = r.stdout
    name = u.split("/")[-1]
    if name.endswith(".html") and "court-of-appeal" in u:
        ok = "Entry Point 01" in body and "Court of Appeal AI Deep-Dive Pack" in body
        sz = len(body)
        print(f"{name}: len={sz} packs_content={'OK' if ok else 'MISSING'}")
    elif name == "sitemap.xml":
        import xml.etree.ElementTree as ET
        try:
            t = ET.fromstring(body)
            nloc = sum(1 for e in t.iter() if e.tag.endswith("loc"))
            print(f"sitemap.xml: {nloc} locs")
        except Exception as ex:
            print("sitemap.xml parse ERR", ex)
    else:
        print(f"{name}: len={len(body)}")
