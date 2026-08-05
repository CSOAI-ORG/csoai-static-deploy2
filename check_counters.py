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
SKIP_FILES = {"check_counters.py", "SOV-Counter-Canon.md",
              # Audit/retraction documents QUOTE unevidenced counters in order to
              # retract them; scanning them as if they published the claim makes
              # the gate attack its own audit trail.
              "FRONT_TO_BACK_AUDIT.md"}

# 2026-08-04 — the gate blocked STALE numbers but let UNEVIDENCED ones publish freely.
# The canon's law is not "don't use the old number", it is "no number exists without a file
# on disk". An audit found three canon counters whose evidence file does not exist anywhere
# on this machine — and one of them, "30 frameworks", appears 78 times across the estate.
# A gate that catches 349-instead-of-417 while waving through a number with no evidence at
# all is enforcing the easy half of the law.
#
# Matched as exact PHRASES, not bare digits: "30" alone appears innocently everywhere, so a
# digit-level block would drown the gate in false positives and get it switched off — which
# is how gates die. Each entry mirrors the canon's "exact public phrasing" column.
UNEVIDENCED_PHRASES = {
    "30 frameworks": "canon #4 — 4 framework control-sets on disk; no artifact enumerates 30",
    "30 regulatory frameworks": "canon #4 — same",
    "19 signed agents": "canon #6 — largest registry export found holds 7",
    "9 MCP tools": "canon #9 — largest registry found holds 7",
}

# Register-locked strings: the canon fixes exact wording for findings whose meaning collapses
# when paraphrased. Dropping the denominator or the interval turns a careful result into a
# marketing claim.
FORBIDDEN_VARIANTS = {
    "0 of 12 assets survived": ("ProvBench register-lock — the only permitted phrasing is "
                                "'0 of 20 assets survived (95% CI, clustered by asset)'"),
    "0% survival rate": "ProvBench register-lock — drops denominator and interval",
    "all 20 assets failed": "ProvBench register-lock — drops the interval and clustering note",
}

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
        for phrase, reason in UNEVIDENCED_PHRASES.items():
            if phrase in text:
                failures.append(
                    f"{rel}: UNEVIDENCED counter '{phrase}' — {reason}. "
                    f"G3: produce evidence/harness/freeze/latest/ for it, or remove the claim.")

        for variant, reason in FORBIDDEN_VARIANTS.items():
            if variant in text:
                failures.append(f"{rel}: FORBIDDEN VARIANT '{variant}' — {reason}")

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
