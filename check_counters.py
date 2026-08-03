#!/usr/bin/env python3
"""G3 CI gate — SOV Counter Canon enforcement.

Fails the build if any public page serves a quarantined counter or if a
canonical counter lacks its evidence file. Canon doc: SOV-Counter-Canon.md.
Rule: the canon is never edited to match a page; the page is corrected.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent

# Quarantined values that must never appear in a public property
QUARANTINED = {
    "349": "stale provisions count — canon: 417 (evidence/harness/freeze/latest/statutory-provisions.json)",
    "174": "stale GovBench item count — canon: 193 (evidence/harness/freeze/latest/govbench-results.json)",
    "72": "stale framework count — canon candidate: 30 pending harness freeze",
}

# Files/dirs excluded from the gate (archives, third-party packs, generators)
EXCLUDE_PARTS = {".backups", ".git", "node_modules", "defoneos", "kaggle_results", "__pycache__"}
SCAN_GLOBS = ("*.html", "*.js", "*.md")
SKIP_FILES = {"check_counters.py", "SOV-Counter-Canon.md"}

REQUIRED_EVIDENCE = [
    "evidence/harness/freeze/latest/statutory-provisions.json",
    "evidence/harness/freeze/latest/govbench-results.json",
    "evidence/registry/companies-house-16939677.json",
]


def iter_files():
    for pat in SCAN_GLOBS:
        for p in ROOT.rglob(pat):
            rel = p.relative_to(ROOT)
            if any(part in EXCLUDE_PARTS for part in rel.parts):
                continue
            if p.name in SKIP_FILES:
                continue
            yield rel, p


def main() -> int:
    failures = []

    for rel, p in iter_files():
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        for bad, reason in QUARANTINED.items():
            # match the quarantined number only in a counter-like context
            for token in (f"{bad} legal provisions", f"{bad} provisions", f"{bad}-item", f"{bad} frameworks"):
                if token in text:
                    failures.append(f"{rel}: quarantined counter '{token}' — {reason}")

    for ev in REQUIRED_EVIDENCE:
        evp = ROOT / ev
        if not evp.exists():
            failures.append(f"MISSING evidence file: {ev} (G3: no number without a file on disk)")
        else:
            try:
                json.loads(evp.read_text())
            except json.JSONDecodeError:
                failures.append(f"CORRUPT evidence file: {ev}")

    if failures:
        print("COUNTER CANON GATE: FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("COUNTER CANON GATE: PASS — no quarantined counters, evidence files present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
