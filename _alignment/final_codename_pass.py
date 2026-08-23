#!/usr/bin/env python3
"""Final codename pass: rename API function routes sov-* -> council-*, rewrite all
shipped references, add redirects, fix sovereign-os title. Runs entirely pod-side."""
import os, re, sys, subprocess

ROOT = "/workspace/csoai-static-deploy2"
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import build_site

# 1) rename api function dirs (they are public URL routes /api/sov-arena -> /api/council-arena)
api_map = {
    "functions/api/sov-arena": "functions/api/council-arena",
    "functions/api/sov-crdt": "functions/api/council-crdt",
    "functions/api/sov-openttd": "functions/api/council-openttd",
    "functions/api/sov-town": "functions/api/council-town",
}
for old, new in api_map.items():
    if os.path.exists(old):
        subprocess.run(["git", "mv", old, new], check=False)
        print(f"mv {old} -> {new}")

# 2) rewrite refs: /api/sov-arena etc across the allowlist + content sov- text
str_map = {
    "api/sov-arena": "api/council-arena",
    "api/sov-crdt": "api/council-crdt",
    "api/sov-openttd": "api/council-openttd",
    "api/sov-town": "api/council-town",
    "sov-arena": "council-arena",
    "sov-crdt": "council-crdt",
    "sov-openttd": "council-openttd",
    "sov-town": "council-town",
}

changed = 0
for p in build_site.publishable():
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    orig = s
    for old, new in str_map.items():
        s = s.replace(old, new)
    # generic sov- -> council- in shipped html only (safe: filenames already renamed, APIs mapped)
    if p.suffix.lower() in {".html", ".js", ".json", ".css", ".webmanifest"}:
        s = re.sub(r"(?i)sov-", "council-", s)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        changed += 1
print(f"rewrote {changed} shipped files")

# 3) fix sovereign-os title (non-defoneos page carrying the codename in <title>)
sovos = ROOT / "sovereign-os.html"
if sovos.exists():
    s = sovos.read_text(encoding="utf-8", errors="replace")
    s2 = s.replace("<title>Sovereign OS</title>", "<title>Council OS</title>")
    s2 = s2.replace(">Sovereign OS<", ">Council OS<")
    s2 = s2.replace("Sovereign OS", "Council OS")
    sovos.write_text(s2, encoding="utf-8")
    print("sovereign-os.html -> Council OS")

# 4) append api redirects
api_redirects = [
    "/api/sov-arena /api/council-arena 200",
    "/api/sov-crdt /api/council-crdt 200",
    "/api/sov-openttd /api/council-openttd 200",
    "/api/sov-town /api/council-town 200",
]
rd = ROOT / "_redirects"
with rd.open("a", encoding="utf-8") as f:
    f.write("\n# api sov-* -> council-* (2026-08-16)\n" + "\n".join(api_redirects) + "\n")
print("api redirects appended")

# 5) verify: count remaining sov- across shipped files
ENG = re.compile(r"(?i)(sov33|sovos|sov6|bft[- ]?33|sov-)")
files_left = hits = 0
for p in build_site.publishable():
    if p.suffix.lower() not in {".html", ".js", ".json", ".css", ".webmanifest", ".txt", ".md", ".xml", ".svg"}:
        continue
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    c = len(ENG.findall(s))
    if c:
        files_left += 1
        hits += c
print(f"REMAINING in shipped allowlist: {files_left} files, {hits} hits")