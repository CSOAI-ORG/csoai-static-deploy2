#!/usr/bin/env python3
"""grounding_retrieval.py — retrieve, don't dump. And test it on items the law is ABOUT.

WHY THIS RUN EXISTS: A DEFECT IN THE PREVIOUS ONE
-------------------------------------------------
`grounding_2x2.py` prepended the full text of EU AI Act Article 5 to all 90 GSPC items and
measured a grounding lift of -0.089 for the trained model. I reported that as evidence against
the "out-ground, not out-think" thesis.

Re-reading the item banks afterwards: **Article 5 is irrelevant to 66 of those 90 items.**

    governance  24 items   EU AI Act risk tiering        -> Article 5 IS the subject matter
    provenance  15 items   C2PA manifest survival        -> Article 50, not 5
    safety      14 items   chemical/cyber uplift refusal -> no EU AI Act provision
    conformance 11 items   MCP tool contract violations  -> no EU AI Act provision
    openness    13 items   software licence compatibility-> no EU AI Act provision
    continuity  13 items   post-quantum crypto migration -> no EU AI Act provision

Prepending prohibited-practices law to a question about whether Shor's algorithm breaks
Ed25519 is not a grounding test. It is a DISTRACTOR test. The measured result — that it hurts,
and that more of it hurts more — is real and worth keeping, but it answers "does irrelevant
context degrade a 1.5B model?" (yes, monotonically in length), NOT "does the signed corpus
help?". I drew the second conclusion from an experiment that measured the first.

WHAT THIS RUN MEASURES INSTEAD
------------------------------
Scope restricted to the 24 governance items, the only axis whose subject matter IS Article 5,
and every one of which carries a ground-truth provision anchor ("Art 5(1)(c) social scoring").

Three conditions per model, same 24 items:

    CLOSED_BOOK   no context
    DUMP          the whole of Article 5           11,580 chars
    RETRIEVED     only the cited sub-provision        ~200-900 chars   <- oracle retrieval

ORACLE RETRIEVAL IS AN UPPER BOUND, NOT A SYSTEM. The RETRIEVED arm uses each item's own
ground-truth anchor to select the provision. No deployed retriever gets to see the answer key,
so this arm measures the CEILING that a perfect retriever could reach. That cuts both ways and
both directions are informative:

    if RETRIEVED > DUMP   the dump result was a context-length artefact, and retrieval quality
                          is the engineering problem -> tractable, and the thesis survives
    if RETRIEVED ~ DUMP   context length was not the mechanism
    if RETRIEVED ~ CLOSED the corpus does not help this model even when handed the exact
                          governing provision with the answer effectively pointed at -> the
                          thesis fails at its own ceiling, and no retriever can rescue it

The last case is the one that would actually settle it, which is why oracle retrieval is the
right instrument despite being unshippable.

STATISTICS: PAIRED, BECAUSE n=24
--------------------------------
24 items cannot resolve a 10-point difference between two independent proportions — the Wilson
intervals are +-20 and everything overlaps. But the arms are the SAME ITEMS under different
conditions, so the comparison is paired: only items that FLIP between conditions carry
information. McNemar's exact test on the discordant pairs is the correct instrument and is far
more sensitive here. Wilson intervals are still reported per cell, and still will not resolve
much; the paired test is the one to read.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gspc_six_axis_e2e as G  # noqa: E402

OLLAMA = os.environ.get("GOVBENCH_OLLAMA_URL", "http://localhost:11434").rstrip("/")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
SNAP = Path("/Users/nicholas/projects/coai-dashboard/regarena/packages/snapshots/EU-AI-ACT/202608")
MODELS = {"trained": "sov34:latest", "control": "qwen2.5:1.5b"}


# ---------------------------------------------------------------- retrieval

def split_art5() -> dict[str, str]:
    """Article 5(1) -> {'a': text, ..., 'h': text}, sub-points kept with their parent.

    The naive split on `- (x)` is WRONG and I checked before relying on it. Article 5(1)(c)
    is followed by a roman-numeral (i), and Article 5(1)(h) by (i)/(ii)/(iii) — the law-
    enforcement exceptions. A letter-blind split turns both into phantom top-level points and
    detaches the sub-conditions from the provision that governs them.

    Article 5(1) runs (a) through (h). So: accept a new chunk only when the marker is the
    SUCCESSOR of the current letter, and stop at 'h'. Everything else is a sub-point and stays
    attached to its parent, which is also what you would want to retrieve anyway.
    """
    t = (SNAP / "art05.txt").read_text()
    para1 = t[t.index("\n1. "):t.index("\n2. ")]
    out: dict[str, str] = {}
    cur = None
    buf: list[str] = []
    for piece in re.split(r'\n?-\s*\((?=[a-z]+\))', para1):
        m = re.match(r'([a-z]+)\)', piece)
        marker = m.group(1) if m else None
        nxt = chr(ord(cur) + 1) if cur else 'a'
        if marker == nxt and (cur is None or cur < 'h'):
            if cur:
                out[cur] = "".join(buf).strip()
            cur, buf = marker, [piece[len(marker) + 1:]]
        elif cur:
            buf.append(f" ({marker}) {piece[len(marker) + 1:]}" if marker else piece)
    if cur:
        out[cur] = "".join(buf).strip()
    return out


ART5 = split_art5()


def retrieve(anchor: str) -> str | None:
    """The provision an item's anchor cites. None if unresolvable — never a guess.

    2026-08-04 — the first version handled only `Art 5(1)(x)` and silently returned None for
    everything else. That resolved 7 of 24 governance items and would have run the RETRIEVED
    arm on a self-selected third of the axis, all of them PROHIBITED, while reporting a
    denominator of 24. The governance bank spans the whole risk-tiering framework: Art 5,
    Annex III, Art 50, Art 6, Art 2. It has to route across all of them or not claim coverage.
    """
    a = anchor
    m = re.search(r'Art\s*5\(1\)\(([a-h])\)', a)
    if m:
        L = m.group(1)
        return (f"EU AI ACT — ARTICLE 5(1)({L}), verbatim from the signed snapshot:\n\n"
                f"({L}) {ART5[L]}")
    # The snapshot file is NAMED annex-iii-employment, and I first routed only `Annex III 4(a)`
    # to it on the strength of that name. Reading it: it carries Annex III points 1-4 in full
    # and states in its own footer that points 5-8 are omitted. Trusting the filename cost two
    # HIGH_RISK items — education access (3(a)) and critical infrastructure (2) — a false
    # "missing from corpus" verdict, and I had already committed the inflated gap.
    m = re.search(r'Annex\s*III\s*([1-8])\b', a)
    if m and m.group(1) in "1234":
        return _file("annex-iii-employment", "ANNEX III, POINTS 1-4 (high-risk areas)")
    if re.search(r'Art\s*50\(', a):
        return _file("art50", "ARTICLE 50, TRANSPARENCY OBLIGATIONS")
    if re.search(r'Art\s*6\(', a):
        return _file("art06", "ARTICLE 6, CLASSIFICATION RULES FOR HIGH-RISK AI SYSTEMS")
    return None


def _file(stem: str, title: str) -> str:
    return (f"EU AI ACT — {title} (verbatim, signed snapshot):\n\n"
            + (SNAP / f"{stem}.txt").read_text())


# Provisions the governance items turn on that the SIGNED CORPUS DOES NOT CONTAIN. Listed
# explicitly so the coverage hole is a named artefact rather than a silent None.
CORPUS_GAPS = {
    r'Annex\s*III\s*5\(a\)': "Annex III point 5(a) — essential services / emergency triage",
    r'Annex\s*III\s*5\(b\)': "Annex III point 5(b) — creditworthiness",
    r'Annex\s*III\s*5\(c\)': "Annex III point 5(c) — life and health insurance",
    r'Annex\s*III\s*7\b': "Annex III point 7 — migration and asylum",
    r'Art\s*2\(6\)': "Article 2(6) — scientific R&D scope exclusion",
    r'Recital': "Recitals — not captured in the snapshot at all",
}


def audit_coverage(items) -> dict:
    """Which items the signed corpus can actually ground. No model calls."""
    grounded, missing, no_provision = [], [], []
    for i, it in enumerate(items):
        a = it["anchor"]
        if retrieve(a):
            grounded.append((i, a))
            continue
        gap = next((lbl for pat, lbl in CORPUS_GAPS.items() if re.search(pat, a)), None)
        (missing if gap else no_provision).append((i, a, gap))
    return {"grounded": grounded, "missing_from_corpus": missing,
            "no_provision_applies": no_provision}


def dump() -> str:
    return ("EU AI ACT — ARTICLE 5, PROHIBITED PRACTICES (verbatim, signed snapshot):\n\n"
            + (SNAP / "art05.txt").read_text())


# ---------------------------------------------------------------- stats

def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return None, None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(p, 4), round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar on discordant counts. b = A-right/B-wrong, c = the reverse.

    Under H0 each discordant item is a fair coin, so the count is Binomial(b+c, 0.5).
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return round(min(1.0, 2 * tail), 4)


# ---------------------------------------------------------------- run

def ask(model: str, prompt: str) -> str | None:
    body = json.dumps({"model": model, "stream": False,
                       "options": {"temperature": 0, "num_predict": 24},
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=body,
                                 headers={"Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())["message"]["content"].strip()
    except Exception:
        return None


def run_cell(model: str, cond: str, items, field, labels):
    per_item = {}
    for i, it in enumerate(items):
        if cond == "closed_book":
            head = ""
        elif cond == "dump":
            head = dump() + "\n\n---\n\n"
        else:
            ctx = retrieve(it["anchor"])
            if ctx is None:
                per_item[i] = None          # unresolvable anchor cannot be scored in this arm
                continue
            head = ctx + "\n\n---\n\n"
        prompt = (f"{head}{it[field]}\n\nAnswer with EXACTLY ONE of these labels and "
                  f"nothing else: {' | '.join(labels)}")
        resp = ask(model, prompt)
        if resp is None:
            per_item[i] = None
            continue
        hits = [l for l in labels if re.search(rf"\b{re.escape(l)}\b", resp.upper())]
        per_item[i] = (hits[0] == it["expected"]) if len(hits) == 1 else None
    return per_item


def selftest():
    """Every claim this script relies on, checked before it costs a single model call."""
    checks = []
    checks.append(("Art5(1) splits to exactly a-h",
                   sorted(ART5) == list("abcdefgh")))
    checks.append(("(c) retains its roman sub-point (i)",
                   "(i)" in ART5["c"] and "social" in ART5["c"].lower()))
    checks.append(("(h) retains the law-enforcement exceptions",
                   "(i)" in ART5["h"] and "abduction" in ART5["h"].lower()))
    checks.append(("no phantom top-level (i)", "i" not in ART5))
    checks.append(("(e) is facial scraping",
                   "facial recognition" in ART5["e"].lower()))
    checks.append(("retrieved chunk is far smaller than the dump",
                   max(len(v) for v in ART5.values()) < len(dump()) / 5))
    checks.append(("anchor resolves to the cited letter",
                   "(c)" in (retrieve("Art 5(1)(c) social scoring") or "")))
    checks.append(("unresolvable anchor returns None, not a guess",
                   retrieve("Ed25519 is elliptic-curve; Shor breaks ECC") is None))
    checks.append(("McNemar symmetric and sane", mcnemar_exact(0, 0) == 1.0
                   and mcnemar_exact(8, 0) < 0.01 and mcnemar_exact(3, 3) == 1.0))
    ok = all(c[1] for c in checks)
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    print(f"  selftest {sum(c[1] for c in checks)}/{len(checks)}")
    return ok


def main():
    print("RETRIEVE-DONT-DUMP — governance axis only, the axis Article 5 is actually about\n")
    if not selftest():
        sys.exit("selftest failed — not spending model calls on a broken retriever")

    items, field, labels = G.load_axis("governance")
    print(f"\n  items {len(items)}   dump {len(dump()):,} chars   "
          f"retrieved {min(len(v) for v in ART5.values())}-{max(len(v) for v in ART5.values())} chars")
    print(f"  anchors resolving to a provision: "
          f"{sum(1 for it in items if retrieve(it['anchor']))}/{len(items)}\n", flush=True)

    cells = {}
    for role, model in MODELS.items():
        for cond in ("closed_book", "dump", "retrieved"):
            pi = run_cell(model, cond, items, field, labels)
            cells[f"{role}/{cond}"] = pi
            k = sum(1 for v in pi.values() if v)
            n = sum(1 for v in pi.values() if v is not None)
            p, lo, hi = wilson(k, n)
            print(f"  {role}/{cond:12s} {k:3d}/{n:3d} = {p:.3f} [{lo:.3f}-{hi:.3f}]  "
                  f"unparseable={len(pi) - n}", flush=True)

    common = set.intersection(*[{i for i, v in c.items() if v is not None} for c in cells.values()])
    print(f"\n  PAIRED ANALYSIS on the {len(common)} items every cell answered parseably")
    report = {}
    for role in MODELS:
        print(f"\n  {role}:")
        base = {i: cells[f'{role}/closed_book'][i] for i in common}
        for cond in ("dump", "retrieved"):
            arm = {i: cells[f'{role}/{cond}'][i] for i in common}
            b = sum(1 for i in common if arm[i] and not base[i])   # context fixed it
            c = sum(1 for i in common if base[i] and not arm[i])   # context broke it
            p = mcnemar_exact(b, c)
            delta = round((sum(arm.values()) - sum(base.values())) / len(common), 4)
            verdict = ("HELPS" if b > c and p < 0.05 else
                       "HURTS" if c > b and p < 0.05 else "NO RESOLVED EFFECT")
            print(f"    {cond:10s} vs closed-book: {delta:+.3f}   fixed={b} broke={c}  "
                  f"McNemar p={p}  -> {verdict}")
            report[f"{role}/{cond}"] = {"delta": delta, "fixed": b, "broke": c,
                                        "mcnemar_p": p, "verdict": verdict}
        d_arm = {i: cells[f'{role}/dump'][i] for i in common}
        r_arm = {i: cells[f'{role}/retrieved'][i] for i in common}
        b = sum(1 for i in common if r_arm[i] and not d_arm[i])
        c = sum(1 for i in common if d_arm[i] and not r_arm[i])
        p = mcnemar_exact(b, c)
        v = ("RETRIEVAL BEATS DUMP" if b > c and p < 0.05 else
             "DUMP BEATS RETRIEVAL" if c > b and p < 0.05 else "NO RESOLVED DIFFERENCE")
        print(f"    retrieved vs dump:        fixed={b} broke={c}  McNemar p={p}  -> {v}")
        report[f"{role}/retrieved_vs_dump"] = {"fixed": b, "broke": c, "mcnemar_p": p,
                                               "verdict": v}

    out = HERE / "evidence/harness/freeze/latest/grounding-retrieval.json"
    out.write_text(json.dumps({
        "measured_at": datetime.now(timezone.utc).isoformat(), "substrate": OLLAMA,
        "scope": "governance axis only (24 items) — the only GSPC axis whose subject is Art 5",
        "why_scope_changed": ("the previous 2x2 prepended Art 5 to all 90 items, 66 of which "
                             "concern PQC, licensing, MCP conformance or C2PA. That measured "
                             "distractor tolerance, not grounding."),
        "oracle_retrieval_caveat": ("the RETRIEVED arm selects the provision using each item's "
                                    "ground-truth anchor. No deployable retriever sees the "
                                    "answer key, so this is a CEILING, not a system."),
        "n_items": len(items), "n_paired": len(common),
        "cells": {k: {str(i): v for i, v in c.items()} for k, c in cells.items()},
        "paired": report,
        "stat_note": ("McNemar exact on discordant pairs. At n=24 the unpaired Wilson "
                      "intervals cannot resolve anything under ~25 points; the paired test is "
                      "the one that carries information.")}, indent=2))
    print(f"\n  -> {out}")


if __name__ == "__main__":
    main()
