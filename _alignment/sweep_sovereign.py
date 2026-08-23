#!/usr/bin/env python3
"""Sweep breach-only HTML files in _site (no DEFONEOS context) — replace internal-codename language with Council-neutral copy, surgical string-level, count-verified per file."""
import re, os, sys

ROOT = "/workspace/csoai-static-deploy2/_site"

# Context-sensitive replacements (from longest/most specific to shortest)
REPL = [
    # common full-phrase swaps first
    ("sovereign AI", "AI governance"),
    ("Sovereign AI", "AI governance"),
    ("SOFTWARE AI", "AI governance"),
    ("sovereign compliance", "compliance measurement"),
    ("Sovereign compliance", "compliance measurement"),
    ("sovereign data", "open data"),
    ("Sovereign data", "Open data"),
    ("sovereign substrate", "Council substrate"),
    ("sovereign model", "Council model"),
    ("sovereign stack", "Council stack"),
    ("sovereign token", "Council token"),
    ("sovereign mesh", "Council mesh"),
    ("the sovereignty", "the neutrality"),
    ("sovereignty", "neutrality"),
    # singular forms — careful: 'sovereign' also appears in user-facing hype; neutralize
    (" sovereign ", " neutral "),
    (" Sovereign ", " Neutral "),
    ("sovereign", "neutral"),
    ("Sovereign", "Neutral"),
]

def clean(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    before = len(re.findall(r"(?i)sovereign", s))
    for old, new in REPL:
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8").write(s)
    after = len(re.findall(r"(?i)sovereign", s))
    return before, after

# Only breach-only files (no DEFONEOS/defence context)
files = []
for root, _, names in os.walk(ROOT):
    for n in names:
        if not n.endswith(".html"):
            continue
        p = os.path.join(root, n)
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if re.search(r"(?i)defoneos|defence", s):
            continue  # legit sovereign-by-design surface
        files.append(p)

done, changed, errors = 0, 0, 0
for p in files:
    try:
        b, a = clean(p)
        done += 1
        if b != a:
            changed += 1
    except Exception as e:
        errors += 1

print(f"scanned {done} breach-only files, cleaned {changed}, errors {errors}")

# final estate-wide recount
total = 0
for p in files:
    total += len(re.findall(r"(?i)sovereign", open(p, encoding="utf-8", errors="replace").read()))
print(f"remaining sovereign hits across breach-only files: {total}")