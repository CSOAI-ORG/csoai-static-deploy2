#!/usr/bin/env python3
"""Sweep ONLY the publish allowlist (what build_site.py ships to _site).
Preserves internal docs/keys/plans. Engine codenames removed everywhere in the
allowlist; sovereign normalized only where no DEFONEOS context (canonical survives)."""
import re, os, sys

ROOT = "/workspace/csoai-static-deploy2"
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import build_site  # gets publishable() + NEVER

picked = build_site.publishable()
print(f"publish allowlist: {len(picked)} files")

ENGINE = re.compile(r"(?i)(sov33|sovos|sov6|bft[- ]?33|sov-)")
ENGINE_REPL = [
    (re.compile(r"(?i)sov33"), "Council"),
    (re.compile(r"(?i)sovos"), "Council OS"),
    (re.compile(r"(?i)sov6"), "tuned clan"),
    (re.compile(r"(?i)bft[- ]?33"), "33-member council"),
]
# NOTE: sov- prefix NOT auto-replaced here to avoid touching URLs/paths like
# sov-space-vwm.html (internal route) — only full codenames get replaced.

sover = re.compile(r"(?i)sovereign")
SOV_REPL = [
    ("sovereign AI", "AI governance"), ("Sovereign AI", "AI governance"),
    ("sovereign compliance", "compliance measurement"), ("Sovereign compliance", "compliance measurement"),
    ("sovereign data", "open data"), ("Sovereign data", "Open data"),
    ("sovereign substrate", "Council substrate"), ("sovereign stack", "Council stack"),
    ("sovereign model", "Council model"), ("sovereign token", "Council token"),
    ("sovereign mesh", "Council mesh"), ("the sovereignty", "the neutrality"),
    ("sovereignty", "neutrality"), (" sovereign ", " neutral "), (" Sovereign ", " Neutral "),
    ("sovereign", "neutral"), ("Sovereign", "Neutral"),
]

eng_files = sov_files = 0
for p in picked:
    if not p.suffix.lower() in {".html", ".js", ".json", ".txt", ".md", ".xml", ".css", ".webmanifest"}:
        continue
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    orig = s
    if ENGINE.search(s):
        for pat, rep in ENGINE_REPL:
            s = pat.sub(rep, s)
        eng_files += 1
    if sover.search(s) and not re.search(r"(?i)defoneos|defence", s):
        for old, new in SOV_REPL:
            s = s.replace(old, new)
        sov_files += 1
    if s != orig:
        p.write_text(s, encoding="utf-8")

print(f"engine-swept: {eng_files} files, sovereign-swept: {sov_files} files")

# verify allowlist
eng_left = sov_left = 0
for p in picked:
    if not p.suffix.lower() in {".html", ".js", ".json", ".txt", ".md", ".xml", ".css", ".webmanifest"}:
        continue
    try:
        s = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    eng_left += len(ENGINE.findall(s))
    if not re.search(r"(?i)defoneos|defence", s):
        sov_left += len(sover.findall(s))
print(f"REMAINING in allowlist: engine={eng_left} sovereign(non-defo)={sov_left}")