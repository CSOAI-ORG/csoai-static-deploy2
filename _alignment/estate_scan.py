#!/usr/bin/env python3
"""Definitive estate scan on _site."""
import re, os

ROOT = "/workspace/csoai-static-deploy2/_site"
ENGINE = re.compile(r"(?i)(sov33|sovos|sov6|bft[- ]?33|sov-)")

eng_files, eng_hits = 0, 0
defo_files = 0
sovereign_on_defo, sovereign_off_defo = 0, 0
off_defo = []

for root, _, names in os.walk(ROOT):
    for n in names:
        if not n.endswith(".html"):
            continue
        p = os.path.join(root, n)
        s = open(p, encoding="utf-8", errors="replace").read()
        e = len(ENGINE.findall(s))
        if e:
            eng_files += 1
            eng_hits += e
        is_defo = bool(re.search(r"(?i)defoneos|defence", s))
        if is_defo:
            defo_files += 1
        sov = len(re.findall(r"(?i)sovereign", s))
        if sov:
            if is_defo:
                sovereign_on_defo += sov
            else:
                sovereign_off_defo += sov
                off_defo.append(p)

print("engine codenames: files={} hits={}".format(eng_files, eng_hits))
print("defoneos-contexted files:", defo_files)
print("sovereign on defoneos surfaces (canonical):", sovereign_on_defo)
print("sovereign off-defoneos (BREACH):", sovereign_off_defo)
for p in off_defo[:10]:
    print("  ", p)

# crawl-priority check
for f in ["index.html", "llms.txt", "SOV33_BFT33_COUNCIL.html", "sovereign-os.html", "gspc-scoreboard.html"]:
    p = os.path.join(ROOT, f)
    if os.path.isfile(p):
        s = open(p, encoding="utf-8", errors="replace").read()
        locks = len(ENGINE.findall(s)) + len(re.findall(r"(?i)sovereign", s))
        print(f"{f}: {locks} locks")