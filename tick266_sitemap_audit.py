#!/usr/bin/env python3
"""Analyze sitemap health: quantify _site-prefixed, host split, and true gaps."""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
t = ET.parse(ROOT / "sitemap.xml")
locs = [e.text for e in t.getroot().iter() if e.tag.endswith("loc")]

# Real publishable file list from repo root (mirrors build_site.py publishable())
import re
from pathlib import Path as P

# Build a set of path -> exists-at-root check (case-insensitive-ish)
def root_exists(path):
    p = (ROOT / path.lstrip("/")).resolve()
    rel = str(p.relative_to(ROOT))
    # mimic: file at root, or <file>.html
    if (ROOT / rel).exists():
        return True
    candidates = [rel, rel + ".html", rel + "/index.html"]
    return any((ROOT / c).exists() for c in candidates)

site_prefixed = [l for l in locs if "/_site/" in l]
non_site = [l for l in locs if "/_site/" not in l]

def relpath(l):
    return re.sub(r"^https?://[^/]+", "", l).split("?")[0]

# For _site-prefixed: what does stripping _site give?
fixable = []
unfixable = []
for l in site_prefixed:
    stripped = l.replace("/_site/", "/")
    if root_exists(relpath(stripped)):
        fixable.append((l, stripped))
    else:
        unfixable.append(l)

# Genuine gaps among non-_site
non_site_missing = [l for l in non_site if not root_exists(relpath(l))]

print(f"total locs      : {len(locs)}")
print(f"_site-prefixed  : {len(site_prefixed)}")
print(f"  -> fixable    : {len(fixable)} (root counterpart exists, strip _site)")
print(f"  -> unfixable  : {len(unfixable)} (no root counterpart even after strip)")
print(f"non-_site       : {len(non_site)}")
print(f"  -> genuine missing: {len(non_site_missing)}")
print()
print("--- unfixable _site (root counterpart missing even after strip) ---")
for l in unfixable[:20]:
    print("  ", l)
print()
print("--- genuine non-_site missing ---")
for l in non_site_missing[:30]:
    print("  ", l)
print()
print("--- hostsplit ---")
import collections
hosts = collections.Counter(re.sub(r"(https?://[^/]+).*", r"\1", l) for l in locs)
print(hosts)
print("fixable sample:", fixable[:3])
