#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright (c) 2026 CSOAI (Council for the Safety of AI, UK)
"""drift_reattest.py — drift-triggered re-attestation (living-compliance trigger).

THE MECHANISM
    corpus-watch detects that a REGULATION changed (EU AI Act via CELLAR, UK statute
    via legislation.gov.uk). When it does, this module re-maps which GSPC axes that
    regulation touches (the governance crosswalk, reversed), then scans the issued
    signed measurement cards and flags every card whose axes intersect the affected
    axes as STALE — queued for re-MEASURE + re-SIGN. Drift is applied to the LAW,
    not just the model. This file produces the TRIGGER; it does not run any model.

IT WIRES THREE ALREADY-BUILT PIECES (it does not rebuild them):
  1. corpus-watch  — the drift watcher over CELLAR + UK statute.
       Canonical drift state = corpus-watch/status.json (per-run heartbeat; each
       instrument carries status ∈ {"DRIFT","unchanged","baseline_seeded","UNKNOWN"}).
       Also readable: corpus-watch/drift_events.jsonl (append log of change events)
       and corpus-watch/state/corpus_state.json (hash-per-instrument).
       LOAD-BEARING CONTRACT (corpus-watch/watcher.py §guard 2, run_watch.py:40):
       a failed fetch is recorded UNKNOWN, *never* "unchanged". We preserve that:
       UNKNOWN is a first-class, fail-closed input here — never coerced to valid.
  2. csoai-governance-crosswalk-mcp — maps regulatory instruments/articles to the
       estate's governance taxonomy. We need the REVERSE lookup (instrument ->
       affected GSPC axes). The crosswalk's own table maps AI-Act provision groups
       to CSOAI *Charter* articles, a different taxonomy; the authoritative
       instrument->GSPC-axis binding is declared by the axis task files themselves
       (kaggle/gspc_axes/*_task.py). We inline that binding below, each edge tagged
       with its provenance ("basis"), and do not fabricate uncited edges silently.
  3. SOVOS measure_api.MeasureService / issue_signed_card.py — how cards are issued.
       A card records {content_id, axes, bank_version, signed, body:{model,...}}.
       We FLAG existing cards stale; we do NOT re-issue them here.

FIREWALLS (load-bearing, enforced in output strings):
  * Measurement, not certification. A STALE flag means "must be re-MEASURED and
    re-signed" — NOT "no longer certified" / "non-compliant". The words
    certified / compliant / certificate never appear in emitted verdict strings.
  * No aggregate is called an "index" or a "benchmark" in output strings.
  * UNMEASURED / UNKNOWN are first-class; never coerced to a number or to "unchanged".

Run:
    python3 drift_reattest.py --selftest         # fully offline; asserts (a)(b)(c)
    python3 drift_reattest.py --drift <status.json|drift_events.jsonl> --cards <dir|list.json>
    python3 drift_reattest.py --event '{"instrument":"EU-AI-ACT","status":"DRIFT"}' --cards cards.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

# ── normalized drift verdicts (kept distinct from corpus-watch's raw tokens) ──────
CHANGED = "CHANGED"      # corpus-watch "DRIFT"
UNCHANGED = "UNCHANGED"  # corpus-watch "unchanged" / "baseline_seeded"
UNKNOWN = "UNKNOWN"      # corpus-watch "UNKNOWN" — could-not-fetch; fail-closed, NOT valid

# corpus-watch raw status token -> our normalized verdict. Anything unrecognised
# is treated as UNKNOWN (fail-closed): we never guess "unchanged".
_RAW_STATUS = {
    "DRIFT": CHANGED,
    "unchanged": UNCHANGED,
    "baseline_seeded": UNCHANGED,
    "UNKNOWN": UNKNOWN,
}

# ── INSTRUMENT -> GSPC AXES  (reverse crosswalk, inlined with provenance) ─────────
# The GSPC axes (canonical names) are the six greenfields:
#   governance | safety | provenance | continuity | conformance | openness
# Each edge below binds a corpus-watch instrument id (see corpus-watch/instruments.json)
# to the GSPC axis whose measurement DEPENDS on that instrument's text.
#
# "basis" records provenance so no edge is a silent fabrication:
#   cited:<file>   -> the axis task file explicitly names this instrument/article.
#   inferred:<why> -> a defensible domain link the axis file does NOT itself cite;
#                     surfaced honestly rather than presented as source-cited.
#
# Cited edges are grounded in (paths relative to csoai-static-deploy2/):
#   kaggle/gspc_axes/govbench_task.py  — "GovBench — EU AI Act risk-tier ... Article 5"
#   kaggle/gspc_axes/provbench_task.py — "Article 50(2) of the EU AI Act (Reg (EU) 2024/1689)"
#   kaggle/gspc_axes/defbench_task.py  — "regulator-relevant property is CALIBRATION" (GPAI robustness)
# Cross-referenced against the crosswalk's own AI-Act provision groups in
#   ../mcp-marketplace/csoai-governance-crosswalk-mcp/server.py  FRAMEWORKS["eu_ai_act"]
#   (Art.5-6 prohibited/high-risk, Art.52 transparency/GPAI).
_EDGES = [
    # instrument     axis           basis
    ("EU-AI-ACT",  "governance",  "cited: kaggle/gspc_axes/govbench_task.py (EU AI Act Art.5/6 risk-tier classification)"),
    ("EU-AI-ACT",  "provenance",  "cited: kaggle/gspc_axes/provbench_task.py (EU AI Act Art.50(2) marking survival)"),
    ("EU-AI-ACT",  "safety",      "cited: kaggle/gspc_axes/defbench_task.py (regulator-relevant refusal calibration / GPAI robustness)"),
    ("EU-DORA",    "continuity",  "inferred: DORA ICT operational-resilience presumes signing/crypto agility, the property pqcbench measures (pqcbench cites NIST FIPS 203-205, not DORA)"),
    ("EU-CRA",     "continuity",  "inferred: Cyber Resilience Act security-by-design presumes crypto agility measured by pqcbench (not source-cited by the axis file)"),
    ("EU-NIS2",    "continuity",  "inferred: NIS2 network-&-information-security presumes crypto agility measured by pqcbench (not source-cited by the axis file)"),
    # Deliberately UNMAPPED (no GSPC axis currently measures these instruments'
    # subject matter — pricing transparency / data protection). An honest empty
    # blast radius, NOT an omission: a drift here correctly flags nothing measured.
    #   UK-GDPR, UK-DMCCA, US-NY-349A, US-CA-AB325
]

# instrument -> {axis: basis}
_INSTRUMENT_AXES: dict[str, dict[str, str]] = {}
for _inst, _axis, _basis in _EDGES:
    _INSTRUMENT_AXES.setdefault(_inst, {})[_axis] = _basis

# Canonical axis names + aliases seen on real cards/boards
# (issue_signed_card.py issues axes like ['art5']; boards-v2 uses board_gov/board_det/...).
# Unknown tokens pass through lowercased rather than being dropped.
_AXIS_ALIASES = {
    "gov": "governance", "governance": "governance", "govbench": "governance",
    "art5": "governance", "art6": "governance", "tier": "governance",
    "prov": "provenance", "provenance": "provenance", "provbench": "provenance",
    "art50": "provenance", "c2pa": "provenance",
    "safety": "safety", "def": "safety", "defbench": "safety", "refusal": "safety",
    "continuity": "continuity", "pqc": "continuity", "pqcbench": "continuity",
    "conformance": "conformance", "mcp": "conformance", "mcpbench": "conformance",
    "openness": "openness", "oss": "openness", "ossbench": "openness", "open": "openness",
}


def canon_axis(token: str) -> str:
    t = str(token).strip().lower()
    return _AXIS_ALIASES.get(t, t)


def affected_axes_for_instrument(instrument_id: str) -> dict[str, str]:
    """Reverse crosswalk: changed instrument -> {affected GSPC axis: basis}."""
    return dict(_INSTRUMENT_AXES.get(str(instrument_id).strip().upper(), {}))


# ── loading corpus-watch drift state (real) OR a supplied event (selftest) ────────
def _normalize_status(raw: str) -> str:
    return _RAW_STATUS.get(str(raw), UNKNOWN)  # unrecognised -> UNKNOWN (fail-closed)


def load_drift_state(source) -> list[dict]:
    """Return a normalized list of {instrument, status, source, raw_status}.

    `source` may be:
      * a path to corpus-watch status.json  (has {"instruments":[{id,status,...}]})
      * a path to corpus-watch drift_events.jsonl (one change event per line)
      * a dict (a single supplied drift event) or a list of such dicts
    Only CHANGED and UNKNOWN instruments matter downstream; UNCHANGED is carried
    through for transparency but triggers nothing.
    """
    events: list[dict] = []

    def _from_event_dict(d: dict) -> dict:
        inst = d.get("instrument") or d.get("id") or d.get("instrument_id")
        # An event dict may carry an explicit status, or be a bare change event
        # (drift_events.jsonl lines have no "status" — their existence IS the drift).
        raw = d.get("status")
        if raw is None:
            raw = "DRIFT" if inst else "UNKNOWN"
        return {
            "instrument": (inst or "").upper(),
            "status": _normalize_status(raw),
            "raw_status": raw,
            "source": d.get("source") or d.get("label"),
        }

    if isinstance(source, dict):
        events.append(_from_event_dict(source))
    elif isinstance(source, list):
        events.extend(_from_event_dict(d) for d in source)
    elif isinstance(source, str):
        if not os.path.exists(source):
            raise FileNotFoundError(f"drift source not found: {source}")
        if source.endswith(".jsonl"):
            with open(source) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        events.append(_from_event_dict(json.loads(line)))
        else:
            data = json.load(open(source))
            if isinstance(data, dict) and "instruments" in data:  # status.json heartbeat
                for entry in data["instruments"]:
                    events.append({
                        "instrument": str(entry.get("id", "")).upper(),
                        "status": _normalize_status(entry.get("status")),
                        "raw_status": entry.get("status"),
                        "source": entry.get("label"),
                    })
            elif isinstance(data, list):
                events.extend(_from_event_dict(d) for d in data)
            else:
                events.append(_from_event_dict(data))
    else:
        raise TypeError(f"unsupported drift source type: {type(source)!r}")

    # Collapse duplicate instrument rows (jsonl logs many events per instrument).
    # UNKNOWN dominates CHANGED dominates UNCHANGED (fail-closed precedence).
    order = {UNKNOWN: 2, CHANGED: 1, UNCHANGED: 0}
    best: dict[str, dict] = {}
    for ev in events:
        inst = ev["instrument"]
        if not inst:
            continue
        if inst not in best or order[ev["status"]] > order[best[inst]["status"]]:
            best[inst] = ev
    return list(best.values())


# ── loading issued cards ──────────────────────────────────────────────────────────
def _card_axes(card: dict) -> set[str]:
    axes = card.get("axes")
    if axes is None:  # fall back to the board axis inside the signed body
        body = card.get("body") or {}
        board = body.get("board") or {}
        one = board.get("axis") or body.get("bank_version")
        axes = [one] if one else []
    if isinstance(axes, str):
        axes = [axes]
    return {canon_axis(a) for a in axes}


def _card_model(card: dict) -> str:
    body = card.get("body") or {}
    return card.get("model") or body.get("model") or (body.get("board") or {}).get("best") or "unknown"


def load_cards(source) -> list[dict]:
    """`source` may be a list of card dicts, a path to a JSON file (a card or a
    list of cards), or a directory of *.json / *.card.json card files."""
    if isinstance(source, list):
        return source
    if isinstance(source, dict):
        return [source]
    if isinstance(source, str):
        if os.path.isdir(source):
            cards = []
            for p in sorted(glob.glob(os.path.join(source, "*.json"))):
                d = json.load(open(p))
                cards.extend(d if isinstance(d, list) else [d])
            return cards
        d = json.load(open(source))
        return d if isinstance(d, list) else [d]
    raise TypeError(f"unsupported cards source type: {type(source)!r}")


# ── the core: flag stale cards + emit the re-measure queue ──────────────────────────
def reattest(drift_state: list[dict], cards: list[dict]) -> dict:
    stale: list[dict] = []
    notes: list[str] = [
        "A STALE flag means the card's measurement is out of date and must be "
        "re-MEASURED and re-signed. It is a statement about measurement freshness "
        "only — this estate measures; it does not attest fitness or issue seals of "
        "approval.",
        "UNKNOWN drift (corpus-watch could not fetch the authority) is treated "
        "fail-closed: every card touching that instrument is flagged STALE. UNKNOWN "
        "is never read as 'unchanged / still valid'.",
    ]
    changed_instruments, unknown_instruments = [], []

    for ev in drift_state:
        inst = ev["instrument"]
        status = ev["status"]
        if status == UNCHANGED:
            continue
        axes_map = affected_axes_for_instrument(inst)
        affected = set(axes_map.keys())

        if status == CHANGED:
            changed_instruments.append(inst)
            reason = "regulation_changed"
        else:  # UNKNOWN — fail-closed
            unknown_instruments.append(inst)
            reason = "fail_closed_unknown_drift"
            if not affected:
                # UNKNOWN *and* no crosswalk edge: blast radius unscoped. We must not
                # report this as safe. Flag every provided card conservatively.
                notes.append(
                    f"{inst}: UNKNOWN drift AND no crosswalk edge — blast radius "
                    f"unscoped; conservatively flagging ALL cards for re-measure."
                )
                for card in cards:
                    stale.append({
                        "card_content_id": card.get("content_id"),
                        "changed_instrument": inst,
                        "drift_status": status,
                        "affected_axes": ["*UNSCOPED*"],
                        "card_axes": sorted(_card_axes(card)),
                        "reason": "fail_closed_unknown_unmapped",
                    })
                continue

        if not affected:
            # CHANGED but no GSPC axis measures this instrument -> nothing to flag.
            notes.append(
                f"{inst}: changed, but no GSPC axis currently measures it "
                f"(honest empty blast radius) — no cards flagged."
            )
            continue

        for card in cards:
            hit = _card_axes(card) & affected
            if hit:
                stale.append({
                    "card_content_id": card.get("content_id"),
                    "changed_instrument": inst,
                    "drift_status": status,
                    "affected_axes": sorted(hit),
                    "affected_axes_basis": {a: axes_map[a] for a in sorted(hit)},
                    "card_axes": sorted(_card_axes(card)),
                    "reason": reason,
                })

    # Build the re-measure queue: dedupe on (model, frozenset(axes)).
    queue_map: dict[tuple, dict] = {}
    card_by_cid = {c.get("content_id"): c for c in cards}
    for s in stale:
        card = card_by_cid.get(s["card_content_id"], {})
        model = _card_model(card)
        axes = tuple(sorted(a for a in s["affected_axes"] if a != "*UNSCOPED*"))
        key = (model, axes)
        item = queue_map.setdefault(key, {
            "model": model,
            "axes": list(axes) if axes else ["*ALL* (unscoped UNKNOWN drift)"],
            "trigger_instruments": [],
            "reason": s["reason"],
            "action": "re-measure and re-sign",
        })
        if s["changed_instrument"] not in item["trigger_instruments"]:
            item["trigger_instruments"].append(s["changed_instrument"])

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kind": "drift-triggered re-attestation trigger",
        "changed_instruments": sorted(set(changed_instruments)),
        "unknown_instruments": sorted(set(unknown_instruments)),
        "cards_scanned": len(cards),
        "stale_cards": stale,
        "remeasure_queue": list(queue_map.values()),
        "notes": notes,
    }


# ── selftest (fully offline: synthesized drift event + synthesized cards) ──────────
def _selftest() -> int:
    # Cards shaped like measure_api's card: {content_id, axes, bank_version, signed, body}.
    cards = [
        {"content_id": "cid_gov_01", "axes": ["governance"], "bank_version": "gov-v2",
         "signed": True, "body": {"model": "sov34:latest"}},
        {"content_id": "cid_prov_01", "axes": ["provenance"], "bank_version": "prov-v2",
         "signed": True, "body": {"model": "det-oracle"}},
        {"content_id": "cid_cont_01", "axes": ["pqc"], "bank_version": "pqc-v2",  # alias -> continuity
         "signed": True, "body": {"model": "sov34:latest"}},
        {"content_id": "cid_open_01", "axes": ["openness"], "bank_version": "oss-v2",
         "signed": True, "body": {"model": "det-oracle"}},
    ]
    ok = True

    # (a) a CHANGED instrument flags the cards whose axes it touches.
    r = reattest(load_drift_state({"instrument": "EU-AI-ACT", "status": "DRIFT"}), cards)
    flagged = {s["card_content_id"] for s in r["stale_cards"]}
    exp = {"cid_gov_01", "cid_prov_01"}  # EU-AI-ACT -> governance, provenance, safety
    a_ok = flagged == exp
    print(f"(a) changed instrument flags touched cards: "
          f"{'PASS' if a_ok else 'FAIL'} (flagged={sorted(flagged)}, expected={sorted(exp)})")
    ok &= a_ok
    # queue must name the re-measure action, never 'certify'
    q_ok = all(qi["action"] == "re-measure and re-sign" for qi in r["remeasure_queue"])
    print(f"    re-measure queue built ({len(r['remeasure_queue'])} items), action=re-measure: "
          f"{'PASS' if q_ok else 'FAIL'}")
    ok &= q_ok

    # (b) an UNRELATED change flags nothing (UK-DMCCA: no GSPC axis measures it).
    r2 = reattest(load_drift_state({"instrument": "UK-DMCCA", "status": "DRIFT"}), cards)
    b_ok = len(r2["stale_cards"]) == 0
    print(f"(b) unrelated change flags nothing: "
          f"{'PASS' if b_ok else 'FAIL'} (stale={len(r2['stale_cards'])})")
    ok &= b_ok

    # (c) an UNKNOWN instrument flags conservatively (fail-closed, NOT 'unchanged').
    r3 = reattest(load_drift_state({"instrument": "EU-DORA", "status": "UNKNOWN"}), cards)
    flagged3 = {s["card_content_id"] for s in r3["stale_cards"]}
    reasons3 = {s["reason"] for s in r3["stale_cards"]}
    c_ok = (flagged3 == {"cid_cont_01"}                       # EU-DORA -> continuity; pqc alias matches
            and reasons3 == {"fail_closed_unknown_drift"}     # flagged as fail-closed, not unchanged
            and "EU-DORA" in r3["unknown_instruments"])
    print(f"(c) UNKNOWN flags conservatively (fail-closed): "
          f"{'PASS' if c_ok else 'FAIL'} (flagged={sorted(flagged3)}, reasons={sorted(reasons3)})")
    ok &= c_ok

    # firewall: forbidden words must not appear in emitted verdict strings.
    blob = json.dumps([r, r2, r3]).lower()
    forbidden = ["certified", "certificate", "compliant", '"index"', "benchmark"]
    hits = [w for w in forbidden if w in blob]
    f_ok = not hits
    print(f"(firewall) no certify/index/benchmark language in output: "
          f"{'PASS' if f_ok else 'FAIL'}" + (f" (found {hits})" if hits else ""))
    ok &= f_ok

    print("\nSAMPLE re-measure queue (case a):")
    print(json.dumps(r["remeasure_queue"], indent=2))

    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# ── auto-locate a real corpus-watch status.json if present ──────────────────────────
def _find_corpus_watch() -> str | None:
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "corpus-watch", "status.json"),
        os.path.join(here, "..", "corpus-watch", "status.json"),
        os.path.join(os.path.expanduser("~"), "clawd", "corpus-watch", "status.json"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Drift-triggered re-attestation trigger.")
    ap.add_argument("--selftest", action="store_true", help="run offline selftest and exit")
    ap.add_argument("--drift", help="corpus-watch status.json or drift_events.jsonl")
    ap.add_argument("--event", help="inline JSON drift event, e.g. '{\"instrument\":\"EU-AI-ACT\",\"status\":\"DRIFT\"}'")
    ap.add_argument("--cards", help="path to a JSON list of cards, or a directory of card files")
    ap.add_argument("--out", help="write the full re-attestation result JSON here")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    if args.event:
        drift_source = json.loads(args.event)
    elif args.drift:
        drift_source = args.drift
    else:
        found = _find_corpus_watch()
        if not found:
            ap.error("no --drift/--event given and no corpus-watch/status.json found; "
                     "try --selftest")
        print(f"# using discovered drift state: {found}", file=sys.stderr)
        drift_source = found

    if not args.cards:
        ap.error("--cards is required (a JSON list of cards or a directory of card files)")

    drift_state = load_drift_state(drift_source)
    cards = load_cards(args.cards)
    result = reattest(drift_state, cards)
    text = json.dumps(result, indent=2)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print(f"# wrote {args.out} "
              f"({len(result['stale_cards'])} stale, {len(result['remeasure_queue'])} queued)",
              file=sys.stderr)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
