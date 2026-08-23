#!/usr/bin/env python3
"""Rewrite ALL old sov-* references across repo html/js (post-rename), skipping .git/_site/.backups/.wrangler."""
import re, os

ROOT = "/workspace/csoai-static-deploy2"
SKIP = {".git", "_site", ".backups", ".wrangler", "node_modules", ".next", "__pycache__"}

MAP = {
    "sov-5d-engine.html": "council-5d-engine.html",
    "sov-city-3d.html": "council-city-3d.html",
    "sov-fluid-viewer.html": "council-fluid-viewer.html",
    "sov-globe-portal.html": "council-globe-portal.html",
    "sov-infinite-zoom.html": "council-infinite-zoom.html",
    "sov-local-viewer.html": "council-local-viewer.html",
    "sov-portal.html": "council-portal.html",
    "sov-space-vwm.html": "council-space-vwm.html",
    "sov-suburb-3d.html": "council-suburb-3d.html",
    "sov-sync-proof.html": "council-sync-proof.html",
    "sov-three-eyes.html": "council-three-eyes.html",
    "sov-time-canvas.html": "council-time-canvas.html",
    "sov-time-canvas.svg": "council-time-canvas.svg",
    "sov-zoom-day.svg": "council-zoom-day.svg",
    "sov-zoom-hour.svg": "council-zoom-hour.svg",
    "sov-zoom-microsecond.svg": "council-zoom-microsecond.svg",
    "sov-zoom-second.svg": "council-zoom-second.svg",
    "sov-zoom-year.svg": "council-zoom-year.svg",
    "sov_space_visual.html": "council-space-visual.html",
}

changed = 0
total_refs = 0
for root, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for n in names:
        if not n.endswith((".html", ".js", ".json", ".svg", ".css")):
            continue
        p = os.path.join(root, n)
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        orig = s
        for old, new in MAP.items():
            c = s.count(old)
            if c:
                s = s.replace(old, new)
                total_refs += c
        if s != orig:
            open(p, "w", encoding="utf-8").write(s)
            changed += 1

print(f"rewrote refs in {changed} files, {total_refs} refs updated")

# verify no old refs left (except inside this script)
left = 0
for root, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for n in names:
        if not n.endswith((".html", ".js", ".json", ".svg", ".css")):
            continue
        p = os.path.join(root, n)
        try:
            s = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for old in MAP:
            left += s.count(old)
print(f"remaining old refs: {left}")