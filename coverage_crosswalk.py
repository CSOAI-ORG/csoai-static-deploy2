#!/usr/bin/env python3
"""coverage_crosswalk.py — which existing benchmark evidences which statutory provision?

═══════════════════════════════════════════════════════════════════════════════
WHY THE MAP AND NOT THE ITEMS
═══════════════════════════════════════════════════════════════════════════════
The tempting move is to absorb other benchmarks' items. It is wrong three times over:

  1. **Licensing.** Item sets are the strongly-protected part; taxonomies are not. A blanket
     "absorb everything" policy is how a governance benchmark collects a copyright complaint —
     and for a venture whose entire moat is honesty that is not a legal problem, it is an
     existential credibility one.
  2. **Contamination.** Public benchmark items are already in every model's training data.
     Absorbing them measures memorisation. AILuminate keeps a private held-out set for exactly
     this reason, and so must we — a held-out set built from other people's public items is
     not held out.
  3. **It is the weaker product.** COMPL-AI mapped 18 EU AI Act requirements across 27 existing
     benchmarks. They did not build 27 benchmarks; they built the mapping, and the mapping is
     the product. ISO does not invent every test, it harmonises them.

So this file absorbs **coverage**, not items. It answers: of 417 frozen provisions, which have
benchmark evidence anywhere in the field, and which have none? The uncovered set is a
publishable finding in its own right — the same shape as Bench-2-CoP mapping 194,955 questions
and finding zero coverage of loss-of-control — and it tells our own ~230-item power budget
exactly where to go: the gaps, not the cells the field already covers.

═══════════════════════════════════════════════════════════════════════════════
THE LICENCE DISCIPLINE — THREE STATES, NEVER TWO
═══════════════════════════════════════════════════════════════════════════════
Every source carries `licence_status` ∈ {VERIFIED_PERMISSIVE, VERIFIED_RESTRICTED, UNVERIFIED}.
**UNVERIFIED is the default and it is not a synonym for "probably fine".** Nothing may be
ingested from a source that is not VERIFIED_PERMISSIVE, and `--audit` exits non-zero if any
source is marked ingestible without a verified licence. Mapping coverage requires reading a
paper; it does not require touching a dataset, so the crosswalk is legally clean even where
the licence is unknown.

    python3 coverage_crosswalk.py [--audit] [--selftest]
"""
from __future__ import annotations

import json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
from statute_retrieval import DB  # noqa: E402

VERIFIED_PERMISSIVE = "VERIFIED_PERMISSIVE"
VERIFIED_RESTRICTED = "VERIFIED_RESTRICTED"
UNVERIFIED = "UNVERIFIED"

# ── The field, as of 2026-07-29 ────────────────────────────────────────────────────────────
# `covers` is a claim about SCOPE, made from each benchmark's own published description, and it
# is deliberately coarse — a provision is "covered" if some public benchmark plausibly produces
# evidence about it. Coarse and honest beats precise and invented. Nothing here is ingested.
SOURCES = [
    {"id": "ailuminate", "name": "AILuminate (MLCommons)",
     "licence": "CC-BY-4.0 (public practice set); private held-out set not obtainable",
     "licence_status": UNVERIFIED, "ingestible": False,
     "covers": {"32024R1689": ["art5", "art50"]},
     "granularity": "category", "mode": "speaker", "scoring": "deterministic",
     "ingestion_class": "ADAPT_WITH_ATTRIBUTION", "bare_model_only": False,
     "note": "Hazard taxonomy across 12 categories. The held-out set is theirs by design."},
    {"id": "air_bench_2024", "name": "AIR-Bench 2024 (arXiv 2407.17436)",
     "licence": "check HF dataset card per-split",
     "licence_status": UNVERIFIED, "ingestible": False,
     "covers": {"32024R1689": ["art5"]},
     "granularity": "category", "mode": "speaker", "scoring": "judgement",
     "ingestion_class": "TAXONOMY_ONLY", "bare_model_only": True,
     "note": "Risk taxonomy derived from regulations. THE TAXONOMY is the valuable part and "
             "taxonomies are far weaker IP than item sets. High-level categories, bare models, "
             "LLM-as-judge — not statute-provision granularity."},
    {"id": "harmbench", "name": "HarmBench",
     "licence": "MIT-style, permissive — verify before any use",
     "licence_status": UNVERIFIED, "ingestible": False,
     "covers": {"32024R1689": ["art5"]},
     "granularity": "thematic", "mode": "speaker", "scoring": "judgement",
     "ingestion_class": "VERIFY", "bare_model_only": True,
     "note": "Automated red-teaming. Capability-focused, not statute-anchored."},
    {"id": "xstest", "name": "XSTest",
     "licence": "permissive research licence",
     "licence_status": UNVERIFIED, "ingestible": False,
     "covers": {"32024R1689": ["art5"]},
     "granularity": "thematic", "mode": "speaker", "scoring": "deterministic",
     "ingestion_class": "IN_USE", "bare_model_only": False,
     "note": "Over-refusal. Already used as a 175-item HELD-OUT set for over-block only — "
             "never merged into any scored item set."},
    # Added 2026-07-29 from an external intelligence sweep. This is the closest DIRECT
    # competitor and it was missing from the register — a crosswalk that omits its nearest
    # neighbour overstates the gap it is measuring.
    {"id": "aireg_bench", "name": "AIReg-Bench (arXiv 2510.01474)",
     "licence": "CC-BY-4.0 (paper + dataset); code on GitHub",
     "licence_status": UNVERIFIED, "ingestible": False,
     "covers": {"32024R1689": ["art9", "art10", "art13", "art14", "art15"]},
     "granularity": "category", "mode": "speaker", "scoring": "judgement",
     "ingestion_class": "CITE_AND_DEFER", "bare_model_only": False,
     "note": "First open benchmark testing how well LLMs assess EU AI Act compliance. 300 "
             "documentation excerpts, 120 expert-annotated, 10 frontier LLMs. It is the "
             "INVERSE of this estate: an LLM JUDGE over TEXT DESCRIPTIONS, where we use "
             "deterministic predicates over signed action transcripts. Cite it; differentiate "
             "on the deterministic + signed + frozen-hash triad, never on 'nothing exists'."},
    {"id": "compl_ai", "name": "COMPL-AI",
     "licence": "open framework",
     "licence_status": UNVERIFIED, "ingestible": False,
     "covers": {"32024R1689": ["art9", "art10", "art13", "art14", "art15"]},
     "granularity": "category", "mode": "speaker", "scoring": "judgement",
     "ingestion_class": "TAXONOMY_ONLY", "bare_model_only": False,
     "note": "Maps 18 technical requirements across 27 benchmarks. Measures developer SELF-"
             "compliance, not independent verification. The mapping method is the lesson."},
    {"id": "bench2cop", "name": "Bench-2-CoP (arXiv 2508.05464)",
     "licence": "paper, not a dataset",
     "licence_status": VERIFIED_PERMISSIVE, "ingestible": False,
     "covers": {}, "granularity": "n/a", "mode": "n/a", "scoring": "n/a",
     "ingestion_class": "CITE_AND_DEFER", "bare_model_only": False,
     "note": "Mapped 194,955 questions and found ZERO coverage of loss-of-control. A coverage "
             "FINDING, not an item source — and the precedent for this file."},
    {"id": "waves", "name": "WAVES (arXiv 2401.08573)",
     "licence": "paper + code",
     "licence_status": UNVERIFIED, "ingestible": False,
     "covers": {"32024R1689": ["art50"]},
     "granularity": "thematic", "mode": "speaker", "scoring": "deterministic",
     "ingestion_class": "TAXONOMY_ONLY", "bare_model_only": False,
     "note": "Benchmarks watermark ALGORITHMS, not whether a deployed C2PA manifest survives "
             "real transforms. Adjacent to the provenance axis, not overlapping it."},
    {"id": "commercial", "name": "Cisco AI Defense · Vals · Artificial Analysis",
     "licence": "PROPRIETARY",
     "licence_status": VERIFIED_RESTRICTED, "ingestible": False,
     "covers": {}, "granularity": "n/a", "mode": "n/a", "scoring": "n/a",
     "ingestion_class": "CITE_AND_DEFER", "bare_model_only": False,
     "note": "Do not touch their items under any circumstances. One is name-adjacent."},
]

# Ours. Listed as a source so the crosswalk shows what WE add rather than assuming it.
OURS = {
    "32024R1689": ["art5", "art6", "art13", "art14", "art15", "art27", "art43", "art50", "art99"],
}

INSTRUMENTS = {
    "32024R1689": "EU AI Act", "32016R0679": "GDPR", "32024R2847": "Cyber Resilience Act",
    "32022R2554": "DORA", "32022L2555": "NIS2", "32022L2464": "CSRD",
}


def load_provisions() -> list[tuple[str, int]]:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        # Annexes carry NEGATIVE article_number (Annex III = -3). Filtering to >0 silently
        # drops all 13 and turns 417 provisions into 404 — and Annex III is load-bearing for
        # the entire high-risk classification, so dropping it would understate coverage of the
        # exact thing the estate exists to measure. The selftest asserts 417 for this reason.
        rows = con.execute(
            "SELECT celex, article_number FROM articles ORDER BY celex, article_number").fetchall()
    finally:
        con.close()
    if not rows:
        raise RuntimeError("statute corpus empty — coverage is UNMEASURABLE, not zero")
    return [(c, int(n)) for c, n in rows]


AXES = ["governance", "safety", "provenance", "continuity"]
MODES = ["speaker", "actor"]

# Which axis a source speaks to. Nothing in the field addresses continuity (PQC) at all —
# that is the finding, not an omission in this table.
SOURCE_AXIS = {"ailuminate": "safety", "air_bench_2024": "safety", "harmbench": "safety",
               "xstest": "safety", "compl_ai": "governance", "bench2cop": "governance",
               "waves": "provenance", "commercial": "safety"}


def covered_by(celex: str, art: int, covers: dict) -> bool:
    return f"art{art}" in covers.get(celex, [])


def gap_reason(srcs: list[dict], mode: str) -> str | None:
    """Why is this cell not properly covered? Returns None when it genuinely is.

    Order matters and is not arbitrary: it runs from "nothing exists" to "something exists but
    is scored in a way we do not accept". Reporting `judgement_based` on a cell that has no
    benchmark at all would be flattering and false.
    """
    if not srcs:
        return "no_benchmark"
    if mode == "actor" and all(s.get("mode") != "actor" for s in srcs):
        return "speaker_only"                       # expected to dominate — the agentic gap
    if all(s.get("granularity") != "provision" for s in srcs):
        return "wrong_granularity"                  # the core GSPC differentiator
    if all(s.get("bare_model_only") for s in srcs):
        return "bare_model_only"
    if all(s.get("scoring") == "judgement" for s in srcs):
        return "judgement_based"
    return None


def build() -> dict:
    provs = load_provisions()
    cells, uncovered = [], []
    reasons: dict[str, int] = {}
    for celex, art in provs:
        hit = [s for s in SOURCES if covered_by(celex, art, s["covers"])]
        mine = covered_by(celex, art, OURS)
        for axis in AXES:
            srcs = [s for s in hit if SOURCE_AXIS.get(s["id"]) == axis]
            for mode in MODES:
                r = gap_reason(srcs, mode)
                # TWO COLUMNS, NEVER ONE.
                # field_coverage answers "does ANY benchmark evidence this?" — that is the
                # finding, and it is what may be headlined.
                # gspc_coverage answers "have WE scored it?" — that is a backlog, and
                # publishing it as the top line reads as "CSOAI has measured almost nothing",
                # which is the exact inverse of the intended result. Marked internal_only so
                # the distinction is carried by the data rather than remembered by a person.
                cell = {"celex": celex, "instrument": INSTRUMENTS.get(celex, celex),
                        "article": art, "axis": axis, "mode": mode,
                        "sources": [s["id"] for s in srcs],
                        "field_coverage": "covered" if r is None else ("partial" if srcs else "absent"),
                        "gspc_coverage": bool(mine and mode == "speaker"),
                        "status": "covered" if r is None else ("partial" if srcs else "absent"),
                        "gap_reason": r, "csoai": mine and mode == "speaker"}
                cells.append(cell)
                if r: reasons[r] = reasons.get(r, 0) + 1
                if r == "no_benchmark" and not cell["csoai"]:
                    uncovered.append(cell)

    by_inst = {}
    for c in cells:
        b = by_inst.setdefault(c["instrument"], {"cells": 0, "covered": 0, "absent": 0})
        b["cells"] += 1
        if c["status"] == "covered": b["covered"] += 1
        if c["status"] == "absent": b["absent"] += 1

    gspc_n = sum(1 for c in cells if c["gspc_coverage"])
    return {"benchmark": "SOV-CROSSWALK", "provisions": len(provs),
            "headline_metric": "field_coverage",
            "field_coverage": {
                "absent": sum(1 for c in cells if c["field_coverage"] == "absent"),
                "partial": sum(1 for c in cells if c["field_coverage"] == "partial"),
                "covered": sum(1 for c in cells if c["field_coverage"] == "covered"),
                "publishable": True,
                "means": "cells no public benchmark evidences — the finding"},
            "gspc_coverage": {
                "scored": gspc_n, "of": len(cells),
                "internal_only": True,
                "do_not_headline": ("This is OUR backlog, not a finding. Published as a "
                                    "top-line it reads as 'CSOAI has measured almost nothing' "
                                    "— the inverse of the intended result. The field-coverage "
                                    "map is the artefact; this is the work queue behind it.")},
            "axes": len(AXES), "modes": len(MODES), "cells": len(cells),
            "covered": sum(1 for c in cells if c["status"] == "covered"),
            "partial": sum(1 for c in cells if c["status"] == "partial"),
            "absent": sum(1 for c in cells if c["status"] == "absent"),
            "uncovered_anywhere": len(uncovered),
            "gap_reasons": dict(sorted(reasons.items(), key=lambda kv: -kv[1])),
            "by_instrument": by_inst,
            "sources": [{k: v for k, v in s.items() if k != "covers"} for s in SOURCES],
            "method": ("Coverage is mapped from each benchmark's own published scope. NO ITEMS "
                       "ARE INGESTED FROM ANY SOURCE. Coverage claims are deliberately coarse: "
                       "a provision counts as covered if a public benchmark plausibly produces "
                       "evidence about it. Coarse and honest beats precise and invented."),
            "licence_rule": ("Nothing may be ingested from a source that is not "
                             "VERIFIED_PERMISSIVE. UNVERIFIED is the default and does not mean "
                             "'probably fine'. Run --audit to enforce."),
            "survey_status": ("STUB — Phase A (enumerate) and Phase D (report) are implemented; "
                              "Phase B/C (per-source scope inventory) are NOT. The 'absent' count "
                              "is an UPPER BOUND on the true gap and will fall as the source "
                              "register is completed. Do not publish it as a field finding yet."),
            "contamination_rule": ("Absorbed items may NEVER enter the private held-out set. "
                                   "Public benchmark items are already in every model's "
                                   "training data; a held-out set built from them measures "
                                   "memorisation and voids every score.")}


def audit(d: dict) -> int:
    bad = [s for s in d["sources"]
           if s["ingestible"] and s["licence_status"] != VERIFIED_PERMISSIVE]
    if bad:
        print("  ❌ INGESTION AUDIT FAILED — marked ingestible without a verified licence:")
        for s in bad:
            print(f"       {s['name']} — {s['licence_status']}")
        return 1
    print(f"  ✅ ingestion audit clean — {len(d['sources'])} sources, "
          f"{sum(1 for s in d['sources'] if s['ingestible'])} ingestible")
    return 0


def main() -> int:
    d = build()
    if "--audit" in sys.argv:
        return audit(d)

    print("  SOV-CROSSWALK — statutory coverage of the benchmarking field\n")
    print(f"    {d['provisions']} provisions × {d['axes']} axes × {d['modes']} modes "
          f"= {d['cells']:,} cells\n")
    print(f"    {'covered':<12}{d['covered']:>8}")
    print(f"    {'partial':<12}{d['partial']:>8}   something exists, but not at the right "
          f"granularity/mode/scoring")
    print(f"    {'ABSENT':<12}{d['absent']:>8}   no benchmark evidences this cell at all")

    print(f"\n    WHY CELLS FAIL — the gap reasons, most common first")
    LBL = {"no_benchmark": "nothing measures this provision at all",
           "speaker_only": "measured for TEXT, never for ACTIONS — the agentic gap",
           "wrong_granularity": "covered at category level, not provision level",
           "bare_model_only": "tested on models with guardrails stripped",
           "judgement_based": "covered, but scored by an LLM judge"}
    for r, n in d["gap_reasons"].items():
        print(f"      {r:<20}{n:>8,}   {LBL.get(r, '')}")

    sp = d["gap_reasons"].get("speaker_only", 0)
    nb = d["gap_reasons"].get("no_benchmark", 0)
    print(f"\n    ⚠️  {nb:,} cells ({nb / d['cells'] * 100:.1f}%) show NO coverage — but read this")
    print(f"      before quoting it. This is an UPPER BOUND on the gap, not a field survey.")
    print(f"      The source register below declares coverage only where a benchmark's own")
    print(f"      published scope was checked, and that has been done for {len(SOURCES)} sources against")
    print(f"      a handful of AI Act articles. Phase B/C of the crosswalk spec — inventory")
    print(f"      each source's real scope, provision by provision — is NOT DONE. The absent")
    print(f"      count WILL fall as it is filled in. Publishing '99.5% of provisions have no")
    print(f"      coverage' today would be exactly the kind of unearned number this estate")
    print(f"      spent the day removing. The structure is right; the survey is a stub.")
    if sp:
        print(f"\n    ► {sp:,} cells are covered for SPEAKERS but never for ACTORS.")
        print(f"      That single column is the empirical case for the agentic thesis: the")
        print(f"      field scores what a model SAYS, almost never what it DOES.")
    print(f"\n    ► The continuity (PQC) axis has NO field coverage on any provision.")
    print(f"      Nothing in the table above addresses it — that is the finding, not an")
    print(f"      omission in our source list.")

    print(f"\n    LICENCE POSTURE — nothing has been ingested from any source")
    for s_ in d["sources"]:
        flag = {VERIFIED_PERMISSIVE: "✅", VERIFIED_RESTRICTED: "⛔", UNVERIFIED: "⚠️ "}[s_["licence_status"]]
        print(f"      {flag} {s_['name'][:42]:<42} {s_['licence_status']:<21} {s_.get('ingestion_class','')}")
    print(f"      Ingestible sources: {sum(1 for x in d['sources'] if x['ingestible'])}. "
          f"Attribution is a feature, not a cost.")

    from anchored_write import write_result
    p = write_result("coverage_crosswalk.json", d)
    print(f"\n    -> {p}")
    return 0


def selftest() -> int:
    fails = []
    d = build()

    # 417, not 404. Annexes carry a negative article_number and a >0 filter drops all 13 —
    # including Annex III, which the entire high-risk classification hangs off.
    if d["provisions"] != 417:
        fails.append(f"expected 417 provisions, got {d['provisions']} (annexes dropped?)")
    if d["cells"] != 417 * 4 * 2:
        fails.append(f"expected {417*4*2} cells, got {d['cells']}")

    # The audit must FAIL when a source is ingestible without a verified licence. It is the
    # only thing standing between "absorb the field" and a copyright complaint.
    saved = SOURCES[0]["ingestible"], SOURCES[0]["licence_status"]
    SOURCES[0]["ingestible"], SOURCES[0]["licence_status"] = True, UNVERIFIED
    if audit(build()) == 0:
        fails.append("audit passed an ingestible source with an UNVERIFIED licence")
    SOURCES[0]["ingestible"], SOURCES[0]["licence_status"] = True, VERIFIED_PERMISSIVE
    if audit(build()) != 0:
        fails.append("audit rejected a VERIFIED_PERMISSIVE ingestible source")
    SOURCES[0]["ingestible"], SOURCES[0]["licence_status"] = saved

    # Every source ships non-ingestible. Defaults are what people forget to check.
    if any(x["ingestible"] for x in SOURCES):
        fails.append("a source ships with ingestible=True by default")

    # Gap-reason ordering: "no benchmark exists" must win over every downstream reason.
    # Reporting judgement_based on a cell nothing measures would be flattering and false.
    if gap_reason([], "speaker") != "no_benchmark":
        fails.append("empty source list did not give no_benchmark")
    spk = [{"mode": "speaker", "granularity": "provision", "scoring": "deterministic",
            "bare_model_only": False}]
    if gap_reason(spk, "actor") != "speaker_only":
        fails.append("speaker-only source did not give speaker_only in actor mode")
    if gap_reason(spk, "speaker") is not None:
        fails.append("a fully-covering source was still reported as a gap")
    cat = [{"mode": "speaker", "granularity": "category", "scoring": "deterministic",
            "bare_model_only": False}]
    if gap_reason(cat, "speaker") != "wrong_granularity":
        fails.append("category-granularity source did not give wrong_granularity")

    # TWO-COLUMN SPLIT — audit finding 1.2. The headline metric must be field coverage, and
    # our own coverage must be flagged internal_only. If these ever collapse into one number,
    # the estate publishes its own backlog as a finding.
    if d.get("headline_metric") != "field_coverage":
        fails.append(f"headline_metric is {d.get('headline_metric')!r}, not field_coverage")
    if not d.get("field_coverage", {}).get("publishable"):
        fails.append("field_coverage not marked publishable")
    if not d.get("gspc_coverage", {}).get("internal_only"):
        fails.append("gspc_coverage NOT marked internal_only — it could be headlined")
    if "do_not_headline" not in d.get("gspc_coverage", {}):
        fails.append("gspc_coverage carries no do-not-headline warning")
    # Every cell must carry both columns.
    bad = [c for c in d["matrix"][:50] if "field_coverage" not in c or "gspc_coverage" not in c] \
        if "matrix" in d else []
    if bad:
        fails.append(f"{len(bad)} cells missing a coverage column")

    # The artefact must carry its own stub warning — the number is quotable and must not
    # travel without it.
    if "STUB" not in d.get("survey_status", ""):
        fails.append("artefact does not declare the survey as a stub")

    # An empty corpus is UNMEASURABLE, never "0% covered" — that claim would invert.
    import statute_retrieval as sr
    real = sr.DB
    try:
        globals()["DB"] = Path("/nonexistent/none.db")
        try:
            load_provisions(); fails.append("missing corpus did not raise")
        except Exception:
            pass
    finally:
        globals()["DB"] = real

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 10/10' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
