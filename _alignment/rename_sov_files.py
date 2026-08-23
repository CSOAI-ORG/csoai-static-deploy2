#!/usr/bin/env python3
"""Rename public sov-* files to council-* + rewrite internal refs + _redirects.
Only renames files that SHIP (in build_site publishable()); preserves internal-doc
references that aren't shipped. Old URLs get 301/200 redirects in _redirects."""
import re, os, sys, subprocess

ROOT = "/workspace/csoai-static-deploy2"
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import build_site

picked = build_site.publishable()
picked_names = {os.path.basename(str(p)) for p in picked}
print(f"allowlist: {len(picked)} files")

# The 20 shipped sov-* names -> council-* (verified live files only)
MAP = {}
for p in picked:
    base = os.path.basename(str(p))
    if base.startswith("sov-") and base.endswith((".html", ".svg")):
        new = "council-" + base[4:]
        MAP[base] = new
    elif base == "sov_space_visual.html":
        MAP[base] = "council-space-visual.html"
    elif base == "sov-bridge.js" and "functions" in str(p):
        MAP[base] = "council-bridge.js"

print(f"renames: {len(MAP)}")
for o, n in sorted(MAP.items()):
    print(f"  {o} -> {n}")

# 1) git mv files
for old, new in MAP.items():
    # find the file path
    for p in picked:
        if os.path.basename(str(p)) == old:
            subprocess.run(["git", "mv", str(p), str(p).replace(old, new)], check=False)
            break

# 2) rewrite references inside allowlist files (exact filenames only)
REFS = []
for old, new in MAP.items():
    REFS.append((old, new))
ref_count = 0
for p in picked:
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    orig = s
    for old, new in REFS:
        s = s.replace(old, new)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        ref_count += 1
print(f"rewrote refs in {ref_count} files")

# 3) append redirects (old -> new, 200 rewrite so it does not break any deep links)
redirect_lines = []
for old, new in sorted(MAP.items(), key=lambda x: -len(x[0])):
    redirect_lines.append(f"/{old} /{new} 200")
rd = ROOT / "_redirects"
existing = rd.read_text(encoding="utf-8") if rd.exists() else ""
if redirect_lines:
    with rd.open("a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write("\n# sov-* -> council-* renames (2026-08-16, pod sweep)\n")
        f.write("\n".join(redirect_lines) + "\n")
print(f"redirects: {rd} +{len(redirect_lines)} rules")

# 4) verify: no shipped sov-* names left
after = {os.path.basename(str(p)) for p in build_site.publishable()}
left = sorted(x for x in after if x.startswith("sov-") and x.endswith((".html", ".svg")))
print(f"remaining sov-* shipped names: {len(left)}")
for x in left[:5]:
    print("  ", x)