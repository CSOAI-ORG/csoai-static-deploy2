#!/usr/bin/env python3
"""Estate-wide codename + sovereign sweep on REPO ROOT (sources), NOT _site.
Preserves DEFONEOS-contexted 'sovereign' (canonical public positioning).
Skip: .git, _site, .backups, .wrangler, node_modules, .hermes, EXEC, .claude, __pycache__"""
import re, os, shutil

ROOT = "/workspace/csoai-static-deploy2"
SKIP_DIRS = {".git", "_site", ".backups", ".wrangler", "node_modules", ".hermes",
             "EXEC", ".claude", "__pycache__", ".next", "vehicles", "_templates"}
EXTS = {".html", ".js", ".json", ".txt", ".md", ".xml", ".css"}

ENGINE = re.compile(r"(?i)(sov33|sovos|sov6|bft[- ]?33|sov-)")
ENGINE_REPL = [
    (re.compile(r"(?i)sov33"), "Council"),
    (re.compile(r"(?i)sovos"), "Council OS"),
    (re.compile(r"(?i)sov6"), "tuned clan"),
    (re.compile(r"(?i)bft[- ]?33"), "33-member council"),
    (re.compile(r"(?i)sov-"), "council-"),
]

def walk():
    for root, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.endswith(".egg-info")]
        for n in names:
            if os.path.splitext(n)[1].lower() in EXTS:
                yield os.path.join(root, n)

# 1) engine codename sweep (ALL files, even defoneos)
eng_files = 0
for p in walk():
    try:
        s = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    if not ENGINE.search(s):
        continue
    for pat, rep in ENGINE_REPL:
        s = pat.sub(rep, s)
    open(p, "w", encoding="utf-8").write(s)
    eng_files += 1

# 2) sovereign sweep (non-defoneos files only)
sovereign = re.compile(r"(?i)sovereign")
sovereign_repl = [
    ("sovereign AI", "AI governance"), ("Sovereign AI", "AI governance"),
    ("sovereign compliance", "compliance measurement"), ("Sovereign compliance", "compliance measurement"),
    ("sovereign data", "open data"), ("Sovereign data", "Open data"),
    ("sovereign substrate", "Council substrate"), ("sovereign stack", "Council stack"),
    ("sovereign model", "Council model"), ("sovereign token", "Council token"),
    ("sovereign mesh", "Council mesh"), ("the sovereignty", "the neutrality"),
    ("sovereignty", "neutrality"), (" sovereign ", " neutral "), (" Sovereign ", " Neutral "),
    ("sovereign", "neutral"), ("Sovereign", "Neutral"),
]
sovereign_files = 0
for p in walk():
    try:
        s = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    if not sovereign.search(s):
        continue
    if re.search(r"(?i)defoneos|defence", s):
        continue  # legit
    for old, new in sovereign_repl:
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)
    sovereign_files += 1

print(f"ENGINE sweep: {eng_files} files")
print(f"SOVEREIGN sweep (non-defoneos): {sovereign_files} files")

# verify sources
eng_left = sov_left = 0
for p in walk():
    try:
        s = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    eng_left += len(ENGINE.findall(s))
    if not re.search(r"(?i)defoneos|defence", s):
        sov_left += len(sovereign.findall(s))
print(f"REMAINING: engine={eng_left} sovereign(non-defo)={sov_left}")