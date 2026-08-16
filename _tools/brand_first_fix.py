#!/usr/bin/env python3
"""Brand-first top-down fix: replace bare 'CSOAI ' brand prefix on public titles
with 'Council of AI ' across the live apex estate (skip _site, .backups, _archive)."""
import os, re

ROOT = os.path.expanduser("~/clawd/csoai-static-deploy2")
changed = 0
total = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    # prune heavy/unmanaged
    dirnames[:] = [d for d in dirnames if d not in ("_site", ".backups", "_archive", ".git", "node_modules")]
    for fn in filenames:
        if not fn.endswith(".html"): continue
        p = os.path.join(dirpath, fn)
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                c = f.read()
        except OSError:
            continue
        o = c
        c = re.sub(r"<title>CSOAI ", "<title>Council of AI ", c)
        c = re.sub(r"<title>CSOAI ·", "<title>Council of AI ·", c)
        c = re.sub(r'og:title" content="CSOAI ', 'og:title" content="Council of AI ', c)
        c = re.sub(r'og:title" content="CSOAI ·', 'og:title" content="Council of AI ·', c)
        c = re.sub(r'og:description" content="CSOAI ', 'og:description" content="Council of AI ', c)
        if c != o:
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
            changed += 1
        total += 1
print(f"scanned {total} html; brand-fixed {changed}")