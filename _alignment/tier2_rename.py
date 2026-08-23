#!/usr/bin/env python3
"""Tier-2 rename: legacy codename FILENAMES -> council-* + redirects + ref rewrite."""
import os, re, sys, subprocess

ROOT = "/workspace/csoai-static-deploy2"
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import build_site

# file-name map for shipped files with codenames (content already zeroed)
MAP = {
    "sov3-model-card.html": "council-model-card.html",
    "sov3-system-card.html": "council-system-card.html",
    "sov3-whitepaper.html": "council-whitepaper.html",
    "sov7_synthesis_dashboard.html": "council-synthesis-dashboard.html",
    "sov7_visual_synthesis.html": "council-visual-synthesis.html",
    "sovos.html": "council-os.html",
    "sovereign.html": "council.html",
    "sovereign-os.html": "council-os-page.html",
    "sovereign-2026.css": "council-2026.css",
    "sovereign-wiki": "council-wiki",          # dir
    "SOV33_BFT33_COUNCIL.html": "council-bft-council.html",
    "SOV33_PQC_SSM_Photonic_Speculative_Hypotheses_2026-07-30.txt": "council-pqc-ssm-photonic-hypotheses-2026-07-30.txt",
    "blog-sovereign-fleet-gspc.html": "blog-council-fleet-gspc.html",
}

picked = build_site.publishable()
picked_map = {}
for p in picked:
    picked_map[str(p)] = p

# do renames that exist (git mv)
for old, new in MAP.items():
    # search in picked or root
    src = None
    for key, p in picked_map.items():
        if os.path.basename(key) == old or old in key:
            src = key
            break
    if src is None:
        # try root file
        cand = os.path.join(ROOT, old)
        if os.path.exists(cand):
            src = cand
    if src is None:
        continue
    dst = src.replace(old, new) if os.path.basename(src) == old else os.path.join(os.path.dirname(src), new)
    subprocess.run(["git", "mv", src, dst], check=False)
    print(f"mv {os.path.basename(src)} -> {os.path.basename(dst)}")

# rewrite refs (including css references + href/src)
str_map2 = {old: new for old, new in MAP.items()}
extras = {
    "sovereign-wiki/": "council-wiki/",
    "sovereign-wiki": "council-wiki",
}
str_map2.update(extras)

changed = 0
removed = 0
for p in picked:
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    orig = s
    for old, new in str_map2.items():
        s = s.replace(old, new)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        changed += 1

# redirects
rd = os.path.join(ROOT, "_redirects")
with open(rd, "a", encoding="utf-8") as f:
    f.write("\n# tier-2 codename file renames (2026-08-16)\n")
    for old, new in MAP.items():
        f.write(f"/{old} /{new} 200\n")
print("tier-2 redirects appended")
print(f"rewrote {changed} files")