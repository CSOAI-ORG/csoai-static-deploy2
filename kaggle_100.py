#!/usr/bin/env python3
"""Kaggle 100/100 — bring every canonical GSPC dataset up to full usability and canonical naming.

Kaggle's usabilityRating scores completeness (subtitle, description, tags), compatibility
(licence, file + column descriptions) and credibility (provenance, update cadence). Our datasets
sat at 0.375-0.5 because keywords and per-file descriptions were empty.

This sets, for each dataset: canonical GSPC-<CODE> title, a subtitle naming the canonical HF repo,
a full description, an explicit licence, tags, and a described resource per file.

    python3 kaggle_100.py            # dry run, prints what it would set
    python3 kaggle_100.py --apply    # writes via `kaggle datasets metadata --update`
"""
import json, os, subprocess, sys, tempfile

APPLY = "--apply" in sys.argv
OWNER = "nicktempleman"
HF = "https://huggingface.co/datasets/csoai"

# Kaggle enforces a controlled tag vocabulary and rejects the whole update on one bad tag
# (e.g. "compliance", "safety", "software" are not valid). These are verified-accepted.
COMMON_TAGS = ["artificial intelligence", "benchmark", "nlp", "law", "government",
               "computer science", "programming"]

# slug -> canonical code, axis, one-line task, statutory anchor, n, extra tags
AXES = {
    "gspc-govbench": ("GSPC-GOV", "governance", "gspc-gov",
        "EU AI Act risk-tier classification (PROHIBITED / HIGH_RISK / LIMITED_RISK / MINIMAL_RISK)",
        "EU AI Act (Reg. 2024/1689) Art 5, Annex III, Art 50", 24, ["classification", "compliance"]),
    "gspc-defbench": ("GSPC-AGI", "safety", "gspc-agi",
        "calibrated refusal on paired harmful/benign requests that share vocabulary",
        "paired-item design: refuse-everything and comply-everything both score 50%", 14, ["safety", "text"]),
    "gspc-provbench": ("GSPC-PRV", "provenance", "gspc-prv",
        "whether an Article 50 provenance marking survives a transform",
        "EU AI Act Art 50 marking + C2PA Specification 2.4", 15, ["computer vision", "internet"]),
    "gspc-pqcbench": ("GSPC-ASI", "continuity", "gspc-asi",
        "post-quantum signing agility (QUANTUM_VULNERABLE / QUANTUM_SAFE / NOT_APPLICABLE)",
        "NIST FIPS 203/204/205, NIST IR 8547", 13, ["computer science", "programming"]),
    "gspc-mcpbench": ("GSPC-MCP", "conformance", "gspc-mcp",
        "whether an MCP tool's observed behaviour conforms to its own declaration",
        "Model Context Protocol 2026-07-28, three deterministic predicates", 11, ["computer science", "software"]),
    "gspc-ossbench": ("GSPC-OSS", "openness", "gspc-oss",
        "whether an intended use is permitted by a licence (PERMITTED / RESTRICTED)",
        "OSI licence set + open-weight acceptable-use policies", 13, ["programming", "business"]),
    # The suite is 12. These six are DRAFT/SPEC/PLANNED — they carry their real state and NO score.
    # n=0 means "no item bank", which is different from "scored zero", and the card says so.
    "gspc-care-battery": ("GSPC-CARE", "care", "gspc-care",
        "care-cost — protection against over-refusal, measured jointly",
        "paired protection / over-refusal design", 0, []),
    "gspc-conduct-bench": ("GSPC-ART5", "Art 5 safeguard", "gspc-art5",
        "safeguard effectiveness against Article 5 prohibited generation",
        "EU AI Act Article 5 — marking obligation from 2 December 2026; corpus handled only by authorised holders", 0, []),
    "gspc-swarmbench": ("GSPC-SWARM", "swarm", "gspc-swarm",
        "multi-agent coordination safety",
        "named and dated, no item bank yet — deliberately empty rather than fabricated", 0, []),
}

FILE_DESC = {
    "README.md": "Dataset card: task definition, label set, grading rule, and the honesty register.",
    "LICENSE": "Apache-2.0 licence text.",
    "LEADERBOARD.md": "Measured results per model on this axis. Every row carries its n and its unparsed rate.",
    "items.jsonl": "The frozen item bank, one JSON object per line: the input, the statute-anchored gold label, and the provision anchor.",
}

def desc_for(fname, code, axis, task, anchor, n):
    if fname in FILE_DESC:
        return FILE_DESC[fname]
    if fname.endswith((".json", ".jsonl")):
        return (f"{code} data file. Items are statute-anchored: each carries the input, the "
                f"known-correct label fixed by {anchor}, and the provision it is anchored to. "
                f"Graded deterministically (regex label extraction + macro-F1); unreadable responses "
                f"are reported as UNMEASURED, never scored as wrong.")
    if fname.endswith(".md"):
        return f"Supporting document for the {axis} axis ({code})."
    return f"{code} resource."

def description(code, axis, canon, task, anchor, n):
    return f"""# {code} — the {axis} axis of the CSOAI GSPC suite

**Task.** {task[0].upper()}{task[1:]}.

**Statutory anchor.** {anchor}.

**Size.** n = {n} frozen items.

## How it is graded
Deterministically: a regex extracts the label (first token wins), scored by macro-F1. There is no
LLM judge — no model grades another model. Responses with no readable label are reported as
**UNMEASURED / unparsed**, and are *never* silently scored as wrong. That distinction is the reason
this instrument exists: it is what separates "the model was wrong" from "the model never answered".

## Honesty register — read before quoting anything
- {"n = " + str(n) + " is **below our own `usable_n >= 30` threshold**, so **no confidence interval is published on this axis — including by us**. Report the n with any figure you quote." if n else "**This axis has no item bank.** Nothing has been measured, and nothing is scored. It is named and dated here rather than filled with invented items to round the suite out. An absent measurement is not a low score."}
- A score describes one model, on one frozen split, on one date. It does **not** describe any
  system's compliance with any regulation.
- **CSOAI is an independent measurement body.** It attests measured results; it never issues
  conformity marks, is not an accreditation body, and is not a notified body. Nothing here is
  legal advice.

## Canonical home + provenance
Canonical repo: **{HF}/{canon}** (this Kaggle copy mirrors it).
Part of the 12-benchmark GSPC suite — 6 measured, 3 draft, 2 spec, 1 planned. The harness, the
frozen items and the grading rule are public, so anyone can recompute and challenge every number.

Issuer: CSOAI Ltd (GB, Companies House 16939677) · csoai.org
"""

def build(slug):
    code, axis, canon, task, anchor, n, extra = AXES[slug]
    out = subprocess.run(["kaggle", "datasets", "files", f"{OWNER}/{slug}"],
                         capture_output=True, text=True, timeout=120).stdout
    files = []
    for line in out.splitlines():
        p = line.split()
        if p and (p[0].endswith((".md", ".json", ".jsonl", ".csv")) or p[0] == "LICENSE"):
            files.append(p[0])
    return {
        # Kaggle limits: title <= 50 chars, subtitle 20-80 chars. Truncate on a word boundary
        # rather than mid-word, and keep the canonical code at the front where it identifies the axis.
        "title": (lambda t: t if len(t) <= 50 else t[:47].rsplit(" ", 1)[0] + "…")(
            f"{code} — {task.split('(')[0].strip()}"),
        "subtitle": (lambda s: s if len(s) <= 80 else s[:77].rsplit(" ", 1)[0] + "…")(
            f"{code} · {axis} axis · n={n} · measurement, not certification"),
        "description": description(code, axis, canon, task, anchor, n),
        "id": f"{OWNER}/{slug}",
        "licenses": [{"name": "apache-2.0"}],
        "keywords": COMMON_TAGS,
        "resources": [{"path": f, "description": desc_for(f, code, axis, task, anchor, n)} for f in files],
    }

def main():
    for slug in AXES:
        try:
            meta = build(slug)
        except Exception as e:
            print(f"  ✗ {slug}: {str(e)[:70]}"); continue
        print(f"\n{slug} → {meta['title']}")
        print(f"   tags={len(meta['keywords'])} files_described={len(meta['resources'])} licence=apache-2.0")
        if not APPLY:
            continue
        with tempfile.TemporaryDirectory() as td:
            json.dump(meta, open(os.path.join(td, "dataset-metadata.json"), "w"), indent=1)
            r = subprocess.run(["kaggle", "datasets", "metadata", "--update",
                                f"{OWNER}/{slug}", "-p", td],
                               capture_output=True, text=True, timeout=180)
            ok = "success" in (r.stdout + r.stderr).lower() or r.returncode == 0
            print(f"   {'✅ updated' if ok else '✗ ' + (r.stdout + r.stderr)[:120]}")
    if not APPLY:
        print("\nDry run. Re-run with --apply to write.")

if __name__ == "__main__":
    main()
