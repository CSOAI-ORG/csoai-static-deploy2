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

# FORBIDDEN codenames — legal/brand hygiene (2-lane convergence + confirmed
# SOVOS US Reg #6876686, Sovos Compliance LLC). These NEVER appear on PUBLIC
# surfaces. The linter FAILS a public-bound file that carries them.
# Scope: only public/render surfaces (READMEs, html, api/deploy/site, JSON docs
# that ship). Internal status/doctrine/ops notes may legitimately use SOVOS as
# an internal codename or the SOVOS/ repo path — those are not public-bound.
FORBIDDEN = [
    r"\bSOVOS\b",
    r"\bSOV4\b",
    r"\bsov34\b",
    r"\bsovereign-os\b",
    r"\bsov-town\b",
]
# Public-bound file markers (a file is public iff its path matches).
# Scoped to the ACTUAL public web/HF estate (councilof/meok sites, api/deploy,
# HF card copy) — NOT monorepo package READMEs, which ship code and legitimately
# reference the SOVOS/ repo path / internal codename. Brand-hygiene = web surface.
PUBLIC_SURFACES = (
    # councilof.ai / meok.ai site + api (the rendered web estate)
    "/councilof-ai/", "councilof-ai", "client/src", "functions/api",
    "meok-ai-landing", "meok.ai", "os.meok.ai",
    # deploy/site artifacts that render publicly (deploy RUNBOOKS are ops docs,
    # not rendered surfaces — only _site/ build output + public/ web dirs qualify)
    "/_site/", "pages/", "public/",
    # HF-bound card copy (data cards that ship to HF)
    "hf_card", "model_card", "dataset_card",
)

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
        # FORBIDDEN codename enforcement (legal/brand hygiene) — PUBLIC surfaces only
        is_public = any(s in str(p) for s in PUBLIC_SURFACES)
        if is_public:
            for fb in FORBIDDEN:
                for m in re.finditer(fb, text):
                    snippet = text[max(0, m.start()-50):m.end()+50].replace("\n", " ")
                    contrad.append({
                        "file": str(p),
                        "pattern": f"FORBIDDEN:{fb}",
                        "canonical_or_note": "public-codename exile (SOVOS kill)",
                        "hit": snippet[:110],
                    })
            # GATE3 — pooled-rows masquerading as per-(axis,model) quotable n.
            # Recurring 495-vs-33 class: "usable_n 517" (= items x models) quoted
            # as if each model were measured on 517 items. A Wilson interval on a
            # card is PER MODEL and needs n = items for THAT model.
            for m in re.finditer(
                r"(usable[ _-]?n|items?|per[ -]model n|quotable)[^\n]{0,40}"
                r"(\d{3,})\b(?!\s*(models|×\d| x \d))", text, re.I
            ):
                snip = text[max(0, m.start()-40):m.end()+40].replace("\n", " ")
                # heuristic guard: 3-digit n with no "models" divisor on the same
                # sentence is a pooled-count smoke signal on PUBLIC copy.
                contrad.append({
                    "file": str(p),
                    "pattern": "GATE3:POOLED_N",
                    "canonical_or_note": "n>=30 is per-(axis,model) items, "
                                          "never pooled rows (items x models) "
                                          "; divide by the model count",
                    "hit": snip[:120],
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