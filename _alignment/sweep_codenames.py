#!/usr/bin/env python3
"""Estate-wide codename sweep on _site HTML: sov33/sovos/sov6/bft-33/sov- NEVER public (even DEFONEOS pages). sovereign stays on DEFONEOS surfaces (canonical positioning)."""
import re, os

ROOT = "/workspace/csoai-static-deploy2/_site"
LOCK = r"(?i)(sov33|sovos|sov6|bft[- ]?33|sov-[a-z]+)"

# mapping engine codename -> public-safe replacement
REPL = [
    (r"(?i)sov33", "Council"),
    (r"(?i)sovos", "Council OS"),
    (r"(?i)sov6", "tuned clan"),
    (r"(?i)bft[- ]?33", "33-member council"),
    (r"(?i)sov-", "council-"),  # sov-space, sov-state -> council-space etc; review each
]

def report(path):
    return len(re.findall(r"(?i)(sov33|sovos|sov6|bft[- ]?33|sov-)", open(path, encoding="utf-8", errors="replace").read()))

files = []
for root, _, names in os.walk(ROOT):
    for n in names:
        if n.endswith((".html", ".js", ".json")):
            p = os.path.join(root, n)
            if report(p) > 0:
                files.append(p)

print(f"files with engine-codenames: {len(files)}")
changed = 0
for p in files:
    s = open(p, encoding="utf-8", errors="replace").read()
    b = report(p)
    for pat, rep in REPL:
        s = re.sub(pat, rep, s)
    open(p, "w", encoding="utf-8").write(s)
    a = report(p)
    if a != b:
        changed += 1
print(f"cleaned {changed} files")
total = sum(report(p) for p in files)
print(f"remaining codename hits: {total}")

# residual report (things like sov- prefix that mapped to council- are now fine)
res = []
for p in files:
    s = open(p, encoding="utf-8", errors="replace").read()
    m = re.findall(r"(?i).{0,40}(sov33|sovos|sov6|bft[- ]?33|sov-).{0,30}", s)
    if m:
        res.append((p, len(m), m[:1]))
for p, n, m in res[:12]:
    print(f"  {p}: {n} -> {m}")