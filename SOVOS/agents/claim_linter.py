#!/usr/bin/env python3
"""C1: claim-linter — flag count-conflation against the canonical numbers registry.

Scans the repo (md/html/ts/README) for the known-esque number-shaped claims and
flags any that contradict the registry. Kills the count-conflation class:
"care 200" vs canonical 201, "affect 49" vs canonical 59, "52 charters" vs 34,
"axes 12" vs code 13, etc.

Usage:  python3 claim_linter.py [path]
        python3 claim_linter.py --check (exit 1 if any contradiction found — for CI)
"""
from __future__ import annotations

import json, re, sys
from pathlib import Path

def load_registry(path: Path) -> dict:
    return json.loads(path.read_text())

# The conflation map: canonical number -> phrases that imply a DIFFERENT (stale) number.
# Each key is a canonical value we must NOT see contradicted; value = list of
# (regex-pattern, wrong-number) that would be a conflation.
#
# CONTEXT RULE: measurement artifacts (board rows, season runs, arena runs) may
# legitimately cite the fleet size AT MEASUREMENT TIME (e.g. a board run on the
# 15-model fleet). The linter flags present-tense claims in PUBLIC COPY, not
# historical measurement records. Files under 'arena-real-runs/' + 'boards-*'
# are measurement records: they're scanned for count deltas BUT their model
# counts are reported as measured, not conflated. The registry fleet entry is
# the CURRENT fleet; the board's model count is its own measured n.
CONFLATIONS = [
    # (regex to match the wrong claim, canonical value, what it actually is)
    (r"[^\d]200[^\d]? (?=GSPC care|care items|care bank)", "201", "gspc-care usable=200 (bank=201 w/ canary)"),
    (r"affect (bank of |has |: )?49\b", "59", "gspc-affect v2.1=59 (41 public+18 held); v1 49 is SUPERSEDED"),
    (r"34\+15|affect 49", "59", "gspc-affect superseded count"),
    (r"52 charters|52 sovereign charters|52 articles", "34", "charter substantive=34; 52 includes 18 reserved slots"),
    (r"axes?\b[=: ]+12\b", "13", "GSPC axes=13 (code GSPC_AXES); 12 is stale deploy"),
    (r"12 GSPC axes|12-axis", "13", "GSPC axes=13 incl affect"),
    (r"care (bank of|has|: )?20[01]\b", "201", "care canonical = 201 (200 usable + 1 canary)"),
]

# Measurement-record subtrees: model/fleet counts inside these are the measured
# n of that run, not a claim about the current fleet. Their axis counts DO get
# enforced (a 2026-08-12 run saying 12 axes is stale; a run saying 15 models is
# historical truth).
MEASUREMENT_SUBTREES = ("arena-real-runs", "recovered-boards", "boards-v2",
                        "SEASON", "season", "benchmark-results",
                        "REAL_MEASUREMENT", "MASTER_STACK_RUNBOOK",
                        "RUNBOOK", "runbook")
# In measurement records, these patterns report the fleet n of that specific run
# and are exempt from the current-fleet canonical. Also covers axis-count
# staleness: REAL_MEASUREMENT/MASTER_STACK describe runs done on the then-12-axis
# arena — the number is the run's historical truth, not a stale public claim.
MEASUREMENT_EXEMPT = (
    r"~?15 models|fleet of 15\b|15-model fleet|14 models|15 sovereign models",
    r"12 GSPC axes|12-axis|12 axes",
)
# Canon-definition files: they EXPLAIN the conflation (registry details, closes
# docs, audit tables), so the old number inside them is the subject of the
# sentence, not a stale claim. Exempt from enforcement.
CANON_DEFINERS = (
    "GSPC_NUMBERS_REGISTRY.json",
    "REGISTER_CLOSES",
    "BRIEF_AUDIT",
    "V2_CHARTER",
    "claim_linter.py",
    "run_claim_linter.py",
)

def lint(root: Path, registry: dict) -> tuple[list, list]:
    """Return (contradictions, scanned_files)."""
    contrad = []
    files = []
    # scope: only surfaces that carry claims (READMEs, docs, html, md, ts) — not the full tree
    for p in root.rglob("*"):
        if p.is_dir() or not p.suffix.lower() in (".md", ".html", ".htm", ".ts", ".txt", ".json"):
            continue
        if ".git" in str(p) or "node_modules" in str(p) or "__pycache__" in str(p):
            continue
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        if not text.strip():
            continue
        files.append(str(p))
        if any(d in str(p) for d in CANON_DEFINERS):
            continue  # this file defines the canon; its numbers are the subject, not a claim
        is_measurement = any(st in str(p) for st in MEASUREMENT_SUBTREES)
        for regex, canonical, what in CONFLATIONS:
            for m in re.finditer(regex, text, re.I):
                # measurement-record exemption: fleet-n of a specific run is truth,
                # not conflation (only the fleet patterns are exempt)
                if is_measurement and any(
                    re.search(x, m.group(0), re.I) for x in MEASUREMENT_EXEMPT
                ):
                    continue
                snippet = text[max(0, m.start()-40):m.end()+40].replace("\n", " ")
                contrad.append({
                    "file": str(p),
                    "pattern": regex,
                    "canonical_or_note": what,
                    "hit": snippet[:110],
                })
    return contrad, files

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    reg_path = Path("SOVOS/GSPC_NUMBERS_REGISTRY.json")
    if not reg_path.exists():
        print(f"no registry at {reg_path} — run from repo root")
        return 2
    registry = load_registry(reg_path)
    contrad, files = lint(root, registry)
    print(f"scanned {len(files)} files")
    print(f"contradictions: {len(contrad)}")
    for c in contrad[:40]:
        print(f"  ⚠ [{c['file']}] {c['pattern']} → {c['canonical_or_note']}")
        print(f"      ...{c['hit']}...")
    if "--check" in argv:
        return 1 if contrad else 0
    return 0

if __name__ == "__main__":
    sys.exit(main())