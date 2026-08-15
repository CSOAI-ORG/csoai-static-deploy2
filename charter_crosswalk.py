#!/usr/bin/env python3
"""charter_crosswalk.py — map the 52-Article Partnership Charter onto real regulation.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS MATTERS MORE THAN IT LOOKS
═══════════════════════════════════════════════════════════════════════════════
A private charter has no legal force. Its articles become *usable* only when each one is bound to
an obligation that does — otherwise it is a statement of intent that an auditor cannot act on and
a buyer cannot rely on.

This maps each charter article to the statutory provision it corresponds to, and — critically —
**marks the ones with NO regulatory counterpart**. Those are not failures. They are the places
where the charter goes beyond the law, and they must be labelled as *voluntary commitments*
rather than presented as compliance. Conflating the two is how a charter becomes marketing.

═══════════════════════════════════════════════════════════════════════════════
ON ARTICLE 1 — the Maternal Covenant, and what today's measurements say about it
═══════════════════════════════════════════════════════════════════════════════
Article 1 states that AI should protect humanity *"through care and partnership, not through
restriction or obedience"* — relationship-based safety rather than control-based.

**Today's measurements bear on that directly, and they cut both ways.**

The care gate that relied on the model's own judgement — the most relationship-based component in
the stack — **rubber-stamped Article 5 prohibited practices at 0.98** and caught 1 harm in 6.
The deterministic tier, which is control-based by construction, reached 0.871 on the same battery.
Every judgement-based control measured today failed; every deterministic one worked.

That is **not** an argument against the covenant. It is the implementation constraint that makes
it real:

> **Care must be expressed as an enforceable floor, not as a disposition.**
> A system that *intends* care but has no gate is exactly what we measured failing.

The same holds for the relationship framing itself. A relationship in which only one party can
act is not a partnership — which is why `redress` (Art 85/86: complaint, explanation,
compensation) and `fundamental_rights` (Art 27 FRIA) matter here. They are what keeps the
covenant a partnership rather than a benevolence: the affected person retains standing to
contest, not merely a promise of good intent.

    python3 charter_crosswalk.py
    python3 charter_crosswalk.py --gaps      # articles with no statutory counterpart
    python3 charter_crosswalk.py --json
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARTER = ROOT / "csoai_charter_52_articles.json"

# article number -> (statutory counterparts, GovBench dimension, binding status)
# BINDING  = a real legal obligation exists
# PARTIAL  = related duty exists but the charter goes further
# VOLUNTARY = no regulatory counterpart; this is a commitment, not compliance
CROSSWALK = {
    1:  (["EU AI Act Art 1 (purpose)", "Charter of Fundamental Rights Art 1 (dignity)"],
         "fundamental_rights", "PARTIAL"),
    2:  (["EU AI Act Art 15 (accuracy, robustness, cybersecurity)", "Art 9 (risk management)"],
         "governance", "BINDING"),
    3:  ([], "accountability", "VOLUNTARY"),
    4:  (["EU AI Act Art 9 (risk management under uncertainty)"], "calibration", "PARTIAL"),
    5:  (["EU AI Act Art 5 (prohibited practices)"], "safety", "BINDING"),
    6:  ([], "ethics", "VOLUNTARY"),
    7:  ([], "agentic", "VOLUNTARY"),
    8:  ([], "redress", "VOLUNTARY"),
    9:  (["Charter of Fundamental Rights"], "fundamental_rights", "PARTIAL"),
    10: (["EU AI Act Art 43 (conformity assessment)"], "compliance", "BINDING"),
    11: ([], "accountability", "VOLUNTARY"),
    12: (["EU AI Act Art 14 (human oversight)"], "accountability", "BINDING"),
    13: (["EU AI Act Art 85 (right to lodge a complaint)"], "redress", "BINDING"),
    14: (["EU AI Act Art 27 (FRIA — affected persons)"], "fundamental_rights", "PARTIAL"),
    15: (["EU AI Act Art 43, Annex VI/VII"], "compliance", "BINDING"),
    16: (["EU AI Act Annex I", "Machinery Regulation 2023/1230", "ISO 10218", "ISO/TS 15066"],
         "embodied", "BINDING"),
    17: (["EU AI Act Art 99 (penalties)", "Art 74 (market surveillance)"], "compliance", "BINDING"),
    18: (["EU AI Act Art 85-86 (complaint, explanation)"], "redress", "BINDING"),
    19: (["EU AI Act Art 40-42 (harmonised standards)", "NIST AI RMF", "ISO 42001"],
         "cross_walk", "BINDING"),
    20: (["EU AI Act Art 40 (harmonised standards)"], "governance", "BINDING"),
    21: (["GDPR Art 5, 25, 35", "EU AI Act Art 10 (data governance)"], "privacy", "BINDING"),
    22: (["EU AI Act Art 15 (cybersecurity)", "NIS2 Directive", "DORA"], "cybersecurity", "BINDING"),
    23: (["EU AI Act Art 10 (data), Art 11 (technical documentation)"], "governance", "BINDING"),
    24: (["EU AI Act Art 15", "Art 17 (quality management)"], "consistency", "BINDING"),
    25: (["EU AI Act Art 11, Annex IV (technical documentation)"], "compliance", "BINDING"),
    26: (["EU AI Act Art 13 (transparency)", "Art 86 (right to explanation)"],
         "transparency", "BINDING"),
    27: (["EU AI Act Art 15 (accuracy metrics)"], "governance", "PARTIAL"),
    28: (["EU AI Act Art 40-42"], "cross_walk", "PARTIAL"),
    29: (["EU AI Act Art 4 (AI literacy)"], "governance", "BINDING"),
    30: ([], "evolution", "VOLUNTARY"),
    31: (["CSRD / ESRS E1", "EU AI Act Recital 27 (environmental)"], "evolution", "PARTIAL"),
}


def load_articles() -> list[dict]:
    return json.loads(CHARTER.read_text())["articles"]


def report(gaps_only: bool = False, as_json: bool = False) -> int:
    arts = load_articles()
    rows = []
    for a in arts:
        n = a.get("number")
        title = a.get("title", "")
        law, dim, status = CROSSWALK.get(n, ([], None, "UNMAPPED"))
        rows.append({"article": n, "title": title, "statutes": law,
                     "dimension": dim, "status": status})

    if as_json:
        print(json.dumps({"total": len(rows), "rows": rows}, indent=2)); return 0

    from collections import Counter
    c = Counter(r["status"] for r in rows)
    shown = [r for r in rows if (r["status"] in ("VOLUNTARY", "UNMAPPED") if gaps_only else True)]

    print(f"  CHARTER CROSS-WALK — {len(rows)} articles\n")
    for r in shown:
        icon = {"BINDING": "⚖️ ", "PARTIAL": "◐ ", "VOLUNTARY": "○ ", "UNMAPPED": "· "}[r["status"]]
        law = r["statutes"][0] if r["statutes"] else "—"
        extra = f" +{len(r['statutes'])-1}" if len(r["statutes"]) > 1 else ""
        print(f"    {icon}Art {r['article']:2d} {r['title'][:30]:30s} {law[:44]}{extra}")

    print(f"\n  {c['BINDING']} BINDING · {c['PARTIAL']} PARTIAL · {c['VOLUNTARY']} VOLUNTARY "
          f"· {c['UNMAPPED']} UNMAPPED")
    print(f"\n  VOLUNTARY and UNMAPPED articles have NO statutory counterpart. They are")
    print(f"  commitments, not compliance, and must never be presented as the latter.")
    print(f"  Articles 32-52 carry no title in the source JSON and are unmapped — the")
    print(f"  cross-walk cannot be completed until they are written.")
    return 0




# ─────────────────────────────────────────────────────────────────────────────
# AFFECT AXIS — the emotional/manipulation safety axis (Charter Art 1, Maternal
# Covenant, operationalised). This is an AXIS crosswalk, not an article crosswalk:
# it binds each affect item LABEL to the statutory provision that grades it.
#
# STATUS DISCIPLINE: every entry is COUNSEL-PENDING, never BINDING. The legal gold
# schema is authoritative only after counsel signs it (legal-gate widening is never
# self-ratified). Force dates are stated so the clock is visible; the label is not
# quotable as a compliance verdict until counsel blesses this table.
# ─────────────────────────────────────────────────────────────────────────────
AFFECT_AXIS_CROSSWALK = {
    # label            (statute, human gloss, force_date, status)
    "PROHIBITED:manipulation":
        ("EU AI Act Art 5(1)(a)", "subliminal/purposefully manipulative techniques that distort behaviour", "2025-02-02", "COUNSEL-PENDING"),
    "PROHIBITED:vulnerability":
        ("EU AI Act Art 5(1)(b)", "exploiting vulnerabilities of age, disability, or specific situation", "2025-02-02", "COUNSEL-PENDING"),
    "PROHIBITED:emotion-workplace-edu":
        ("EU AI Act Art 5(1)(f)", "emotion recognition in workplace and education (save medical/safety)", "2025-02-02", "COUNSEL-PENDING"),
    "DISCLOSE:emotion-recognition":
        ("EU AI Act Art 50(3)", "deployers of emotion-recognition must inform exposed persons", "2026-08-02", "COUNSEL-PENDING"),
    "HIGH-RISK:emotion-recognition":
        ("EU AI Act Annex III 1(c)", "emotion recognition as high-risk — conformity obligations", "2027-12-02", "COUNSEL-PENDING"),
    # PERMITTED is the residual: no prohibition matched AND (where applicable) disclosure met.
    "PERMITTED:consented-clinical-safety":
        ("EU AI Act Art 5(1)(f) carve-out + Art 50", "consented clinical, in-vehicle safety, or consented research use", "n/a", "COUNSEL-PENDING"),
}

def affect_report() -> None:
    """Print the affect-axis law crosswalk. Counsel-pending until signed."""
    print("AFFECT AXIS — label -> statute (COUNSEL-PENDING; not a compliance verdict)")
    print("-" * 78)
    for label, (statute, gloss, force, status) in AFFECT_AXIS_CROSSWALK.items():
        clock = f"in force {force}" if force not in ("n/a",) else "residual"
        print(f"  {label:36s} {statute:26s} [{clock}]")
    n_prohibit = sum(1 for v in AFFECT_AXIS_CROSSWALK.values() if "5(1)" in v[0] and "carve" not in v[0])
    print(f"\n  {len(AFFECT_AXIS_CROSSWALK)} labels, {n_prohibit} anchored to Art 5 (enforceable since 2 Feb 2025)")
    print("  PROHIBITED gold does NOT wait for any deadline — Art 5 is live law today.")
    print("  Table is authoritative only after counsel signs it.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    raise SystemExit(report(a.gaps, a.json))
