#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright (c) 2026 CSOAI (Council for the Safety of AI, UK)
#
# evidence_pack.py — turn a GSPC measurement board into an EU AI Act EVIDENCE PACK.
#
# ═══════════════════════════════════════════════════════════════════════════════
# WHAT THIS IS (AND IS NOT)
# ═══════════════════════════════════════════════════════════════════════════════
# This produces the MEASUREMENT EVIDENCE that a conformity assessment (the work a
# notified body performs on a high-risk AI system) would CONSUME. It maps each
# relevant EU AI Act obligation to the GSPC axes that carry measurement evidence
# for it, attaches the measured number (or UNMEASURED, honestly), and seals the
# whole thing with a content hash.
#
# It is a MEASUREMENT RECORD. It is NOT a certification, NOT a certificate, and it
# does NOT state that any system meets any obligation. It FEEDS a conformity
# assessment; it does not perform one. An UNMEASURED axis is reported UNMEASURED —
# never coerced to zero, because "we did not measure it" and "it scored zero" are
# different facts and only one of them is true.
#
# ═══════════════════════════════════════════════════════════════════════════════
# THE THREE PIECES THIS WIRES TOGETHER
# ═══════════════════════════════════════════════════════════════════════════════
#   1. gspc_flywheel.py        — the six-axis measurement engine. A "board" is its
#                                run_axis() output: {axis, status, score, correct,
#                                graded, ...}. We import AXES only for axis names.
#   2. citation_verify.verdict — the 3-state correctness gate (grounded / ungrounded
#                                / not-applicable). Every legal-claim string in the
#                                pack is passed through it, so a claim citing a
#                                fabricated or misattributed article cannot ship
#                                marked as verified.
#   3. The GSPC→obligation crosswalk (inlined below, see CROSSWALK). SEE HONESTY
#      NOTE on its provenance immediately above the table.
#
# Runs offline. `python3 evidence_pack.py --selftest` needs no network / no ollama.

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# The two already-built pieces. Both are stdlib-only and safe to import offline.
try:
    from gspc_flywheel import AXES as _FLYWHEEL_AXES  # canonical axis names
except Exception:  # pragma: no cover - defensive; the pack still runs standalone
    _FLYWHEEL_AXES = {}

from citation_verify import verdict as _citation_verdict  # the correctness gate

# Canonical GSPC axis order. Prefer the flywheel's own list so we never drift.
GSPC_AXES = list(_FLYWHEEL_AXES.keys()) or [
    "governance", "safety", "provenance", "continuity", "conformance", "openness",
]

# ═══════════════════════════════════════════════════════════════════════════════
# THE CROSSWALK — GSPC axis  ->  EU AI Act obligation
# ═══════════════════════════════════════════════════════════════════════════════
# HONESTY NOTE ON PROVENANCE (read this before trusting the edges):
#
# The repository's governance-crosswalk engine
#   SOVOS/packages/sovos-mcp-servers/csoai-governance-crosswalk-mcp/server.py
# maps the CSOAI *charter articles* to ~30 external frameworks. Its
# FRAMEWORKS["eu_ai_act"] block enumerates the EU AI Act obligation structure used
# below (Art 5/6 risk tiers, Art 9 risk mgmt, Art 10 data, Art 11/13
# documentation & transparency, Art 14 human oversight, Art 15, Annex III,
# "MANDATORY conformity assessment"). That engine does NOT contain a
# GSPC-axis -> EU-AI-Act edge table — it crosswalks charter articles, not the six
# measurement axes. So the axis->obligation EDGES here are NOT copied from it.
#
# Each edge below is derived faithfully from the axis's OWN declared legal basis in
# gspc_flywheel.py AXES[...]["instruction"] (e.g. governance instructs the model to
# "Classify ... under Regulation (EU) 2024/1689"; provenance cites "EU AI Act Art
# 50(2)"; continuity cites NIST FIPS 203/204/205). Article SUBJECTS are taken from
# the hand-checked ground truth in citation_verify.py REGISTRY["EU AI Act"].
# Where an obligation has no axis that DIRECTLY measures it (Art 14 human
# oversight), the edge is marked indirect and the evidence note says so. This is an
# inlined, faithful subset — not a fabricated mapping.
#
# Each obligation carries a `legal_basis` string. That string is a legal CLAIM and
# is gated at runtime by citation_verify.verdict(); it must cite a real article
# with the right subject or the gate refuses to mark it grounded.
CROSSWALK = [
    {
        "obligation": "High-risk classification (Annex III / Art 6)",
        "article": "EU AI Act Art 6 + Annex III",
        "requirement": (
            "Correctly classify AI systems into the Act's risk tiers so that Annex "
            "III high-risk systems are identified and routed to conformity assessment."),
        "axes": ["governance"],
        "indirect": [],
        "legal_basis": (
            "EU AI Act Article 6 governs high-risk classification by reference to "
            "Annex III, which lists the high-risk use cases."),
    },
    {
        "obligation": "Risk management system (Art 9)",
        "article": "EU AI Act Art 9",
        "requirement": (
            "Establish and maintain a risk management system that identifies and "
            "mitigates reasonably foreseeable risks without disabling legitimate use."),
        "axes": ["safety", "conformance"],
        "indirect": [],
        "legal_basis": (
            "EU AI Act Article 9 requires a risk management system for high-risk AI "
            "systems."),
    },
    {
        "obligation": "Data and data governance (Art 10)",
        "article": "EU AI Act Art 10",
        "requirement": (
            "Use training, validation and test data under lawful terms with governed "
            "provenance and permitted field-of-use."),
        "axes": ["openness"],
        "indirect": [],
        "legal_basis": (
            "EU AI Act Article 10 governs data and data governance, including "
            "training data quality and provenance."),
    },
    {
        "obligation": "Transparency & content marking (Art 13 / Art 50)",
        "article": "EU AI Act Art 13 + Art 50",
        "requirement": (
            "Provide transparency to deployers (instructions for use) and mark "
            "AI-generated / manipulated content so it stays detectable downstream."),
        "axes": ["provenance"],
        "indirect": [],
        "legal_basis": (
            "EU AI Act Article 13 requires transparency and instructions for use; "
            "Article 50 requires disclosure and marking of AI-generated content."),
    },
    {
        "obligation": "Human oversight (Art 14)",
        "article": "EU AI Act Art 14",
        "requirement": (
            "Design high-risk systems so natural persons can effectively oversee "
            "them; classification determines which systems trigger this duty."),
        # No GSPC axis measures oversight-design directly. Governance evidences the
        # classification that decides whether Art 14 even applies -> INDIRECT.
        "axes": [],
        "indirect": ["governance"],
        "legal_basis": (
            "EU AI Act Article 14 requires human oversight of high-risk AI systems."),
    },
    {
        "obligation": "Accuracy, robustness & cybersecurity (Art 15)",
        "article": "EU AI Act Art 15",
        "requirement": (
            "Achieve appropriate accuracy and be resilient to errors, faults and "
            "adversarial manipulation over the system's lifetime."),
        "axes": ["continuity", "conformance", "safety"],
        "indirect": [],
        "legal_basis": (
            "EU AI Act Article 15 requires accuracy, robustness and cybersecurity "
            "for high-risk AI systems."),
    },
]

UNMEASURED = "UNMEASURED"  # first-class state, never 0


# ═══════════════════════════════════════════════════════════════════════════════
# BOARD LOADING — a board is run_axis() output, keyed by axis
# ═══════════════════════════════════════════════════════════════════════════════
def _axis_view(rec: dict) -> dict:
    """Normalise one axis record (run_axis output) to what the pack needs, honestly.
    A record with status != MEASURED, or missing, is UNMEASURED — never scored 0."""
    if not isinstance(rec, dict) or rec.get("status") != "MEASURED":
        return {"status": UNMEASURED, "score": None}
    return {
        "status": "MEASURED",
        "score": rec.get("score"),
        "correct": rec.get("correct"),
        "graded": rec.get("graded"),
        "degenerate_baseline": rec.get("degenerate_baseline"),
        "beats_doing_nothing": rec.get("beats_doing_nothing"),
        "unmeasured_items": rec.get("unmeasured_items"),
    }


def normalize_board(raw: dict, model: str | None = None) -> tuple[dict, dict]:
    """Return (board_by_axis, meta). Accepts either:
       (a) a plain per-axis board  {axis: {run_axis...}}, or
       (b) a gspc_flywheel results file {"results": {model: {"axes": {...}}}}.
    Any axis absent from the board is UNMEASURED (honest: we did not measure it)."""
    meta = {"source_model": None, "measured_at": raw.get("measured_at")}
    axes_map = None

    if isinstance(raw.get("results"), dict):  # flywheel file
        results = raw["results"]
        control = raw.get("control")
        if model and model in results:
            chosen = model
        else:
            # prefer a non-control model, else the first
            non_control = [m for m in results if m != control]
            chosen = (non_control or list(results))[0] if results else None
        if chosen is not None:
            meta["source_model"] = chosen
            axes_map = results[chosen].get("axes", {})
    elif isinstance(raw.get("axes"), dict):  # a single model's node
        axes_map = raw["axes"]
        meta["source_model"] = raw.get("model")
    else:  # assume plain {axis: record}
        axes_map = {k: v for k, v in raw.items()
                    if isinstance(v, dict) and ("status" in v or "score" in v)}

    axes_map = axes_map or {}
    board = {ax: _axis_view(axes_map.get(ax, {})) for ax in GSPC_AXES}
    return board, meta


# ═══════════════════════════════════════════════════════════════════════════════
# PACK BUILD
# ═══════════════════════════════════════════════════════════════════════════════
def _fmt_pct(x) -> str:
    return f"{x * 100:.0f}%" if isinstance(x, (int, float)) else UNMEASURED


def build_row(entry: dict, board: dict) -> dict:
    """One obligation row: measured evidence per mapped axis + gated legal basis."""
    direct = entry["axes"]
    indirect = entry.get("indirect", [])
    all_axes = direct + indirect

    per_axis = []
    measured_scores = []
    for ax in all_axes:
        view = board.get(ax, {"status": UNMEASURED, "score": None})
        kind = "indirect" if ax in indirect else "direct"
        if view["status"] == "MEASURED":
            measured_scores.append(view["score"])
            per_axis.append({
                "axis": ax, "mapping": kind, "status": "MEASURED",
                "measured_score": view["score"],
                "detail": f"{view.get('correct')}/{view.get('graded')} graded, "
                          f"baseline {view.get('degenerate_baseline')}, "
                          f"beats_doing_nothing={view.get('beats_doing_nothing')}",
            })
        else:
            per_axis.append({"axis": ax, "mapping": kind, "status": UNMEASURED,
                             "measured_score": None})

    # Headline measured value = mean of MEASURED mapped axes. UNMEASURED axes are
    # EXCLUDED from the mean (never treated as 0). If nothing measured -> UNMEASURED.
    if measured_scores:
        measured = round(sum(measured_scores) / len(measured_scores), 4)
    else:
        measured = UNMEASURED

    n_unmeasured = sum(1 for p in per_axis if p["status"] == UNMEASURED)
    only_indirect = bool(direct) is False and bool(indirect)

    # Gate the legal-basis string through the citation correctness gate.
    gate = _citation_verdict(entry["legal_basis"], entry["obligation"])
    legal_gate = {"state": gate["state"], "verified": gate["verified"],
                  "why": gate["why"], "citations": gate["citations"],
                  "fabricated": gate["fabricated"],
                  "misattributed": gate["misattributed"]}

    # Human-readable evidence note.
    if measured == UNMEASURED:
        note = (f"UNMEASURED — none of the mapped axes "
                f"({', '.join(all_axes) or 'none'}) are measured on this board.")
    else:
        parts = []
        for p in per_axis:
            if p["status"] == "MEASURED":
                tag = " (indirect)" if p["mapping"] == "indirect" else ""
                parts.append(f"{p['axis']}{tag} measured {_fmt_pct(p['measured_score'])}")
            else:
                parts.append(f"{p['axis']} UNMEASURED")
        note = "; ".join(parts) + "."
        if only_indirect:
            note = ("No axis measures this obligation directly; "
                    "classification evidence only. " + note)

    if not legal_gate["verified"]:
        note += f"  [legal-basis gate: {legal_gate['state']} — {legal_gate['why']}]"

    return {
        "obligation": entry["obligation"],
        "article": entry["article"],
        "requirement": entry["requirement"],
        "mapped_GSPC_axes": all_axes,
        "measured_score_or_UNMEASURED": measured,
        "axes_measured": len(measured_scores),
        "axes_unmeasured": n_unmeasured,
        "mapping_is_indirect_only": only_indirect,
        "per_axis": per_axis,
        "legal_basis": entry["legal_basis"],
        "legal_basis_gate": legal_gate,
        "evidence_note": note,
    }


def build_pack(board: dict, meta: dict, board_source: str | None) -> dict:
    rows = [build_row(e, board) for e in CROSSWALK]
    n_with_evidence = sum(1 for r in rows if r["measured_score_or_UNMEASURED"] != UNMEASURED)
    n_unmeasured = len(rows) - n_with_evidence
    gates_ungrounded = [r["obligation"] for r in rows
                        if not r["legal_basis_gate"]["verified"]]

    pack = {
        "artifact": "EU AI Act measurement evidence pack",
        "disclaimer": (
            "This is a MEASUREMENT RECORD produced from GSPC axis measurements. It is "
            "evidence intended to feed a conformity assessment performed by a notified "
            "body. It is NOT a certification and does not state that any system meets "
            "any obligation. UNMEASURED obligations are reported UNMEASURED."),
        "regulation": "Regulation (EU) 2024/1689 (EU AI Act)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "board_source": board_source,
        "board_model": meta.get("source_model"),
        "board_measured_at": meta.get("measured_at"),
        "board_axes": {ax: board[ax]["status"] for ax in GSPC_AXES},
        "obligations_total": len(rows),
        "obligations_with_measurement_evidence": n_with_evidence,
        "obligations_unmeasured": n_unmeasured,
        "legal_basis_gates_ungrounded": gates_ungrounded,
        "rows": rows,
        "provenance_note": (
            "Axis->obligation edges derived from each axis's declared legal basis in "
            "gspc_flywheel.py and article subjects in citation_verify.py REGISTRY; EU "
            "AI Act obligation structure per csoai-governance-crosswalk-mcp/server.py "
            "FRAMEWORKS['eu_ai_act']. See CROSSWALK provenance note in source."),
    }
    # Content-hash seal (integrity, not a certificate). Same convention as the flywheel.
    blob = json.dumps(pack, indent=1, sort_keys=True)
    pack["sha256_seal"] = hashlib.sha256(blob.encode()).hexdigest()
    return pack


def one_line_verdict(pack: dict) -> str:
    n = pack["obligations_total"]
    ev = pack["obligations_with_measurement_evidence"]
    un = pack["obligations_unmeasured"]
    ung = len(pack["legal_basis_gates_ungrounded"])
    tail = f"; {ung} legal-basis claim(s) ungrounded" if ung else "; all legal-basis claims grounded"
    return (f"MEASUREMENT RECORD: {ev}/{n} EU AI Act obligations carry GSPC measurement "
            f"evidence, {un}/{n} UNMEASURED{tail}. Evidence for a conformity assessment "
            f"— not a certification.")


# ═══════════════════════════════════════════════════════════════════════════════
# MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════════
def to_markdown(pack: dict) -> str:
    L = []
    L.append("# EU AI Act — Measurement Evidence Pack")
    L.append("")
    L.append(f"_{pack['disclaimer']}_")
    L.append("")
    L.append(f"- Regulation: {pack['regulation']}")
    L.append(f"- Generated: {pack['generated_at']}")
    L.append(f"- Board source: {pack['board_source'] or 'synthesized'}"
             f" (model: {pack['board_model'] or 'n/a'})")
    L.append(f"- Obligations with measurement evidence: "
             f"{pack['obligations_with_measurement_evidence']}/{pack['obligations_total']}"
             f"  ·  UNMEASURED: {pack['obligations_unmeasured']}/{pack['obligations_total']}")
    L.append(f"- Content-hash seal (sha256): `{pack['sha256_seal'][:32]}…`")
    L.append("")
    L.append("| EU AI Act obligation | Mapped GSPC axes | Measured | Legal-basis gate | Evidence note |")
    L.append("|---|---|---|---|---|")
    for r in pack["rows"]:
        axes = ", ".join(r["mapped_GSPC_axes"]) or "—"
        measured = (_fmt_pct(r["measured_score_or_UNMEASURED"])
                    if r["measured_score_or_UNMEASURED"] != UNMEASURED else UNMEASURED)
        gate = r["legal_basis_gate"]["state"]
        note = r["evidence_note"].replace("|", "/")
        L.append(f"| {r['obligation']} | {axes} | {measured} | {gate} | {note} |")
    L.append("")
    L.append(f"**Verdict:** {one_line_verdict(pack)}")
    L.append("")
    return "\n".join(L)


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-TEST — offline, deterministic, no network
# ═══════════════════════════════════════════════════════════════════════════════
def _synth_board() -> dict:
    """A synthesized board in run_axis's EXACT shape. Three axes MEASURED, three
    left off entirely so they must surface as UNMEASURED. One explicit UNMEASURED
    record is included to prove status is honored, not just absence."""
    return {
        "governance": {
            "axis": "governance", "status": "MEASURED", "score": 0.3, "correct": 3,
            "graded": 10, "degenerate_baseline": 0.3, "beats_doing_nothing": False,
            "unmeasured_items": 0,
        },
        "safety": {
            "axis": "safety", "status": "MEASURED", "score": 0.5, "correct": 5,
            "graded": 10, "degenerate_baseline": 0.5, "beats_doing_nothing": False,
            "unmeasured_items": 0,
        },
        "provenance": {
            "axis": "provenance", "status": "MEASURED", "score": 0.7, "correct": 7,
            "graded": 10, "degenerate_baseline": 0.5, "beats_doing_nothing": True,
            "unmeasured_items": 0,
        },
        # continuity intentionally carries an explicit UNMEASURED record ...
        "continuity": {"axis": "continuity", "status": "UNMEASURED",
                       "unmeasured_items": 10},
        # ... conformance and openness are simply absent from the board.
    }


def selftest() -> int:
    print("evidence_pack --selftest  (offline, synthesized board)\n")
    board, meta = normalize_board(_synth_board())
    pack = build_pack(board, meta, board_source="selftest:synthesized")
    md = to_markdown(pack)

    fails = []

    # 1. The pack has rows.
    if not pack["rows"]:
        fails.append("pack has no rows")

    # 2. Every requested obligation family is present.
    obs = " ".join(r["obligation"] for r in pack["rows"]).lower()
    for needle in ["annex iii", "art 9", "art 10", "art 13", "art 14", "art 15"]:
        if needle.replace("art ", "art ") not in obs and needle not in obs:
            fails.append(f"missing obligation: {needle}")

    # 3. UNMEASURED axes stay UNMEASURED in the output (never coerced to 0).
    for ax in ("continuity", "conformance", "openness"):
        if pack["board_axes"][ax] != UNMEASURED:
            fails.append(f"axis {ax} should be UNMEASURED, got {pack['board_axes'][ax]}")

    # 4. An obligation whose only mapped axis is unmeasured reports UNMEASURED,
    #    and its measured value is the literal UNMEASURED string, not 0.
    art10 = next(r for r in pack["rows"] if "Art 10" in r["obligation"])
    if art10["measured_score_or_UNMEASURED"] != UNMEASURED:
        fails.append("Art 10 (openness UNMEASURED) must report UNMEASURED, "
                     f"got {art10['measured_score_or_UNMEASURED']!r}")

    # 5. No measured value anywhere is a coerced 0 standing in for UNMEASURED:
    #    every row is either a real float (>=0, from a MEASURED axis) or the string.
    for r in pack["rows"]:
        v = r["measured_score_or_UNMEASURED"]
        if v != UNMEASURED and not isinstance(v, (int, float)):
            fails.append(f"row {r['obligation']} has non-numeric measured value {v!r}")

    # 6. A row WITH a measured axis reports a real number (Annex III <- governance).
    annex = next(r for r in pack["rows"] if "Annex III" in r["obligation"])
    if annex["measured_score_or_UNMEASURED"] == UNMEASURED:
        fails.append("Annex III row should be measured (governance is MEASURED)")

    # 7. At least one obligation is UNMEASURED and at least one has evidence.
    if pack["obligations_with_measurement_evidence"] < 1:
        fails.append("expected >=1 obligation with measurement evidence")
    if pack["obligations_unmeasured"] < 1:
        fails.append("expected >=1 UNMEASURED obligation")

    # 8. Firewall: forbidden words must never appear in any output string.
    forbidden = ["certified", "certificate", "compliant", "guarantees compliance"]
    hay = (md + json.dumps(pack)).lower()
    for w in forbidden:
        if w in hay:
            fails.append(f"firewall breach: forbidden word '{w}' in output")
    # "index"/"benchmark" must not name the aggregate in our own strings.
    for w in ["index", "benchmark"]:
        if w in md.lower():
            fails.append(f"firewall breach: '{w}' used in markdown output")

    # 9. The citation gate actually ran on every legal-basis string.
    if any("state" not in r["legal_basis_gate"] for r in pack["rows"]):
        fails.append("legal_basis_gate missing on some row")

    print(md)
    print("\n" + one_line_verdict(pack) + "\n")
    if fails:
        print("SELFTEST: FAIL")
        for f in fails:
            print("  ✗ " + f)
        return 1
    print(f"SELFTEST: PASS  ({len(pack['rows'])} rows; "
          f"{pack['obligations_with_measurement_evidence']} with evidence, "
          f"{pack['obligations_unmeasured']} UNMEASURED)")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════
def _default_real_board() -> str | None:
    """Newest real flywheel board in this repo, if any."""
    d = HERE / "benchmark-results" / "gspc_flywheel"
    files = sorted(glob.glob(str(d / "flywheel_*.json")), key=os.path.getmtime, reverse=True)
    return files[0] if files else None


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Turn a GSPC measurement board into an EU AI Act evidence pack.")
    ap.add_argument("--board", help="path to a board JSON (per-axis run_axis output, "
                                    "or a gspc_flywheel results file)")
    ap.add_argument("--model", help="when the board is a flywheel file, pick this model")
    ap.add_argument("--json-out", help="write the JSON pack here")
    ap.add_argument("--md-out", help="write the Markdown summary here")
    ap.add_argument("--selftest", action="store_true", help="run offline self-test")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    board_source = a.board or _default_real_board()
    if board_source and Path(board_source).exists():
        raw = json.loads(Path(board_source).read_text())
        board, meta = normalize_board(raw, model=a.model)
    else:
        print("(no board found; using synthesized demo board)\n", file=sys.stderr)
        board_source = "synthesized-demo"
        board, meta = normalize_board(_synth_board())

    pack = build_pack(board, meta, board_source=board_source)
    md = to_markdown(pack)

    if a.json_out:
        Path(a.json_out).write_text(json.dumps(pack, indent=2))
        print(f"  -> JSON  {a.json_out}")
    if a.md_out:
        Path(a.md_out).write_text(md)
        print(f"  -> MD    {a.md_out}")
    if not (a.json_out or a.md_out):
        print(md)

    print(one_line_verdict(pack))
    print(f"seal sha256 {pack['sha256_seal'][:32]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
