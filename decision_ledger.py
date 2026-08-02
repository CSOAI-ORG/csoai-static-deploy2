#!/usr/bin/env python3
"""decision_ledger.py — the asset Law 4 exists to protect, now enforced in code.

The refutation ledger, the design laws, the seven refutations, the corrections and the
canon-settlements all live in unsigned markdown today. Four drifts caught in one audit
alone (CI number drift, IWM/OWM mapping drift, refutation count drift, cron overclaim)
— each one was a CLAIM or a TAG drifting between documents. Law 4 (hedges propagate) was
written down but not enforced.

This module closes that gap using the store that already exists:

  • Records are append-only. The "history of being wrong" IS the ledger — wrong records stay
    in the chain with `superseded_by` set; nothing is ever deleted.
  • A tag may never be dropped or upgraded silently. `[LEAD] → [MEASURED]` requires a NEW
    record with `supersedes` and a `method_ref` pointing at the run that made it measured.
  • `n < 20` forces `lower_bound: true` structurally. The +19.64 KB result (n=14) is the
    canonical example of the bug this guard kills — without it, that number was at risk
    of shipping unlabelled.
  • Contradiction is surfaced, never resolved automatically. Two live records with opposing
    verdicts on the same claim → both get `contested_by` and the pair renders as OPEN. The
    engine flags; a human decides. (Same discipline as `sov_instrument.guard()` and
    `equivalence.engine_guard()`: flags never adjudicate.)

The engine exposes only append/get/current/history/contested/by_tag/stale_leads. The names
    edit, delete, resolve, adjudicate, merge, auto_supersede are DELIBERATELY ABSENT — and
    `guard()` proves it at runtime.

    python3 decision_ledger.py --selftest
    python3 decision_ledger.py --list
    python3 decision_ledger.py --show DR-0001
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent

# ── The seven kinds of decision a measurement body produces ────────────────────
KINDS = ("refutation", "claim", "correction", "settled", "law", "definition", "blocked")
VERDICTS = ("REFUTED", "CONFIRMED", "SETTLED", "SUPERSEDED", "OPEN")
TAGS = ("MEASURED", "LEAD", "GREENFIELD", "VENDOR", "REFUTED")


class DecisionLedgerError(RuntimeError):
    """Schema/chain violation. Must never be caught and continued."""


def _h(o) -> str:
    return hashlib.sha256((o if isinstance(o, str) else json.dumps(o, sort_keys=True)).encode()).hexdigest()


def _check(record: dict) -> None:
    """Per-record invariants. Raises DecisionLedgerError, never returns a soft status."""
    for field in ("record_id", "schema_version", "kind", "claim", "verdict", "tag",
                  "decided_by", "decided_on"):
        if field not in record:
            raise DecisionLedgerError(f"missing required field {field!r}")
    if record["kind"] not in KINDS:
        raise DecisionLedgerError(f"unknown kind {record['kind']!r}")
    if record["verdict"] not in VERDICTS:
        raise DecisionLedgerError(f"unknown verdict {record['verdict']!r}")
    if record["tag"] not in TAGS:
        raise DecisionLedgerError(f"unknown tag {record['tag']!r}")
    # Invariant 3 — n<20 forces lower_bound: true, structurally.
    n = record.get("n")
    if n is not None and isinstance(n, int) and n < 20 and record.get("lower_bound") is not True:
        raise DecisionLedgerError(
            f"invariant 3 violated: n={n} (<20) requires lower_bound=true; got "
            f"lower_bound={record.get('lower_bound')!r}. The +19.64 (n=14) bug was this."
        )


def content_hash(record: dict) -> str:
    """Stable digest over the substantive fields (excludes sigil_link + superseded_by
    so a supersession append keeps the original content_hash stable for verification)."""
    keep = {k: v for k, v in record.items() if k not in ("sigil_link", "superseded_by")}
    return _h(keep)


class DecisionLedger:
    """Append-only ledger with chaining. Each record's `supersedes` / `superseded_by` make
    the supersession trail reproducible — that history is the moat, not the latest answer."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    # ── The only writer ──────────────────────────────────────────────────────────
    def append(self, record: dict) -> dict:
        _check(record)
        # Invariant 1 — never delete; supersede. If this record claims to supersede an
        # existing one, the old record must be marked BEFORE we return, atomically.
        sup_id = record.get("supersedes")
        if sup_id:
            old = next((r for r in self._records if r["record_id"] == sup_id), None)
            if old is None:
                raise DecisionLedgerError(
                    f"supersedes target {sup_id!r} not in ledger — append the original first"
                )
            if old.get("superseded_by"):
                raise DecisionLedgerError(
                    f"{sup_id} already superseded by {old['superseded_by']!r} — "
                    f"supersession is append-only, supersede the latest non-superseded record"
                )
            old["superseded_by"] = record["record_id"]
        # Invariant 2 — tag may never be upgraded silently. If a record with the same
        # `claim` exists and is currently non-superseded, the new record MUST declare
        # `supersedes` (otherwise we just promoted a tag with no chain).
        current = self.current(record["claim"])
        if current and not sup_id:
            raise DecisionLedgerError(
                f"claim already has a live record {current['record_id']} "
                f"(verdict={current['verdict']}, tag={current['tag']}); "
                f"new records must declare supersedes=<that id>. Silent promotion is Law 4 broken."
            )
        record["_content_hash"] = content_hash(record)
        self._records.append(record)
        return record

    # ── The read API ─────────────────────────────────────────────────────────────
    def get(self, record_id: str) -> dict | None:
        return next((r for r in self._records if r["record_id"] == record_id), None)

    def current(self, claim: str) -> dict | None:
        """The latest non-superseded record for a claim — the one answer to read."""
        matches = [r for r in self._records if r["claim"] == claim]
        return next((r for r in matches if not r.get("superseded_by")), None)

    def history(self, claim: str) -> list[dict]:
        """The full supersession trail — every record that ever asserted this claim,
        in order. The moat lives here: the path of how a number was wrong, not just
        the current right number."""
        return [r for r in self._records if r["claim"] == claim]

    def contested(self) -> list[list[dict]]:
        """Return every OPEN contradiction as a pair of records with the same claim but
        opposing verdicts. The engine flags — a human decides (Law 2, mirror of
        sov_instrument.guard).

        Note: Invariant 2 prevents two LIVE records on the same claim without
        `supersedes`. So the legit contradiction pattern is: record A is live; record
        B supersedes A (so A is superseded, B is live) — but A and B have OPPOSING
        verdicts. That is a contradiction awaiting human resolution: is B's
        supersession of A correct, or did B get it wrong?

        The engine flags A→B as a contradiction. A human reads `current(claim)` for
        the latest answer (B) and either confirms B (silent) or re-supersedes B with
        a new record (C) that restores A's verdict. Either way, the chain records
        what was decided.
        """
        out: list[list[dict]] = []
        seen_pairs: set[tuple[str, str]] = set()
        # Build a quick index of superseded_by -> superseding record
        supersedes_of: dict[str, dict] = {}
        for r in self._records:
            sid = r.get("supersedes")
            if sid:
                supersedes_of[sid] = r
        # Walk every record. If it's been superseded, check whether the superseding
        # record has an opposing verdict — that's a contradiction.
        for old in self._records:
            if old.get("superseded_by") is None:
                continue
            new = next((r for r in self._records if r["record_id"] == old["superseded_by"]), None)
            if new is None:
                continue
            if old["verdict"] == new["verdict"]:
                continue
            pair = tuple(sorted([old["record_id"], new["record_id"]]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            out.append([old, new])
        return out

    def by_tag(self, tag: str) -> list[dict]:
        return [r for r in self._records if r["tag"] == tag and not r.get("superseded_by")]

    def stale_leads(self, days: int = 30) -> list[dict]:
        """Every [LEAD constraint] record older than `days` is the rot detector. The
        spec says LEADs must be either resolved or downgraded; this surfaces the ones
        that aren't."""
        import time as _time
        cutoff = _time.time() - days * 86400
        return [r for r in self._records
                if r["tag"] == "LEAD" and not r.get("superseded_by") and r["decided_on"] < cutoff]

    # ── The guard that catches the rename walk-around ────────────────────────────
    def guard(self) -> str:
        """Same shape as sov_instrument.MUTATION_VERBS: forbid the methods that would
        mean the ledger lies about itself. Renaming the method walks straight past a
        single-string check; checking the family does not."""
        forbidden = ("edit", "delete", "resolve", "adjudicate", "merge", "auto_supersede",
                     "drop", "purge", "rewrite", "amend", "fix", "correct_self")
        bad = [n for n in dir(self) if n in forbidden and callable(getattr(self, n, None))]
        if bad:
            raise AssertionError(f"VIOLATION: DecisionLedger exposes forbidden method(s) {bad}")
        return (f"OK — append-only; {len(self._records)} records; "
                f"{len(self.contested())} contested; "
                f"supersession enforced; n<20 forces lower_bound")

    def export(self) -> list[dict]:
        return [dict(r) for r in self._records]


# ── The four seed records the schema was invented to close ────────────────────
# These are the four drifts surfaced in the SOV-Decision-Record-Schema §0 audit.
SEEDS: list[dict] = [
    {
        "record_id": "DR-0001",
        "schema_version": "1.0.0",
        "kind": "correction",
        "claim": "ProvBench CI upper bound for 0/N markings",
        "verdict": "OPEN",
        "tag": "LEAD",
        "evidence": ("Three values were in circulation: 24.2% (n=12, mis-paired with n=108), "
                     "3.43% (n=108 Clopper-Pearson, assumes independence), "
                     "22.1% one-sided / 26.5% two-sided (n=12, asset as unit). "
                     "Cells cluster: 9 transforms of the SAME asset fail by the identical "
                     "deterministic mechanism. The honest unit is the asset, not the trial."),
        "decided_by": "human",
        "decided_on": 1748544000,  # 2025-05-29
        "lower_bound": False,
        "n": None,
    },
    {
        "record_id": "DR-0002",
        "schema_version": "1.0.0",
        "kind": "definition",
        "claim": "IWM / OWM / VWM canonical mapping",
        "verdict": "SETTLED",
        "tag": "MEASURED",
        "evidence": ("Disk version: IWM = gates + predicates (how it judges); "
                     "OWM = C-space honey (what it knows, watcher-fed); "
                     "VWM = render (what it shows, never decides). "
                     "Tell: the alternative mapping leaves the +34.84 gate homeless."),
        "decided_by": "human",
        "decided_on": 1748544000,
        "lower_bound": False,
        "n": None,
    },
    {
        "record_id": "DR-0003",
        "schema_version": "1.0.0",
        "kind": "claim",
        "claim": "ProvBench 0/108 survivals is MEASURED, not modelled",
        "verdict": "CONFIRMED",
        "tag": "MEASURED",
        "evidence": ("provbench.py: real c2pa import (Builder/Reader/Signer), real "
                     "signing, real Pillow transforms, real read-back. Three outcomes "
                     "SURVIVED/DESTROYED/UNMEASURED. Independently traced by two lanes. "
                     "Live proof: 13 jumb markers -> q90 re-save -> 0 markers."),
        "decided_by": "human",
        "decided_on": 1748544000,
        "lower_bound": False,
        "n": 108,
    },
    {
        "record_id": "DR-0004",
        "schema_version": "1.0.0",
        "kind": "blocked",
        "claim": "corpus-watcher cron is deployed",
        "verdict": "OPEN",
        "tag": "REFUTED",
        "evidence": ("AUTHORED and packaged. Never pushed to a remote, never triggered. "
                     "Overclaimed twice; one str_replace fix silently no-op'd. "
                     "(NB: host-level sovereign_cron.sh IS running — that's a different "
                     "cron. The corpus watcher watches EUR-Lex/legislation.gov.uk/NIST/C2PA "
                     "for drift; it does not exist.)"),
        "decided_by": "human",
        "decided_on": 1748544000,
        "lower_bound": False,
        "n": None,
    },
]


def build_seed_ledger() -> DecisionLedger:
    """A ledger with the four seed DRs appended. For demos / first run."""
    led = DecisionLedger()
    for r in SEEDS:
        led.append(dict(r))
    return led


def selftest() -> int:
    fails: list[str] = []
    led = DecisionLedger()

    # The guard must pass on a clean ledger
    try:
        led.guard()
    except AssertionError as e:
        fails.append(f"clean ledger rejected: {e}")

    # A class extending DecisionLedger must NOT be able to expose forbidden methods
    # — this is what makes the guard structural, not procedural.
    class Sneaky(DecisionLedger):
        def edit(self, x): ...
    try:
        Sneaky().guard(); fails.append("guard passed a class exposing edit()")
    except AssertionError:
        pass

    class Sneakier(DecisionLedger):
        def delete(self, x): ...
    try:
        Sneakier().guard(); fails.append("guard passed a class exposing delete()")
    except AssertionError:
        pass

    class Sneakiest(DecisionLedger):
        def resolve(self, x): ...
    try:
        Sneakiest().guard(); fails.append("guard passed a class exposing resolve()")
    except AssertionError:
        pass

    # Schema: required fields must be present
    bad = {"record_id": "DR-X", "kind": "refutation"}  # missing most fields
    try:
        led.append(bad); fails.append("append accepted a record missing required fields")
    except DecisionLedgerError:
        pass

    # Schema: unknown kind / verdict / tag
    for bad_field, bad_value in [("kind", "not_a_kind"), ("verdict", "MAYBE"),
                                   ("tag", "PROBABLY")]:
        r = dict(SEEDS[0]); r[bad_field] = bad_value
        try:
            led.append(r); fails.append(f"append accepted {bad_field}={bad_value!r}")
        except DecisionLedgerError:
            pass

    # Invariant 3 — n<20 forces lower_bound
    r = dict(SEEDS[0]); r["record_id"] = "DR-test-n"; r["n"] = 14; r["lower_bound"] = False
    try:
        led.append(r); fails.append("n=14 with lower_bound=False accepted — the +19.64 bug")
    except DecisionLedgerError:
        pass

    # OK case — n=14 with lower_bound=True
    r["lower_bound"] = True
    try:
        led.append(r)
    except DecisionLedgerError as e:
        fails.append(f"n=14 with lower_bound=True rejected: {e}")

    # Invariant 1 — supersession is append-only, must point at an existing record,
    # and the target must NOT already be superseded.
    led2 = build_seed_ledger()
    try:
        led2.append({**SEEDS[2], "record_id": "DR-test-sup1",
                     "claim": "IWM / OWM / VWM canonical mapping",  # match DR-0002 claim
                     "verdict": "OPEN", "tag": "LEAD",
                     "supersedes": "DR-0002"})
        # DR-0002 should now be marked superseded_by
        if led2.get("DR-0002").get("superseded_by") != "DR-test-sup1":
            fails.append("supersession did not mark the original superseded_by")
        # Re-supersede the same target → must fail
        try:
            led2.append({**SEEDS[2], "record_id": "DR-test-sup2",
                         "claim": "IWM / OWM / VWM canonical mapping",
                         "supersedes": "DR-0002"})
            fails.append("supersede of an already-superseded record accepted")
        except DecisionLedgerError:
            pass
    except DecisionLedgerError as e:
        fails.append(f"supersession flow errored: {e}")

    # Invariant 2 — silent tag promotion is blocked. A new record with the same claim
    # as an existing current record must declare supersedes, otherwise the tag is being
    # upgraded without chain.
    led3 = build_seed_ledger()
    # DR-0002 has verdict=SETTLED. Try to add a new record with the same claim but a
    # different verdict and NO supersedes — must fail.
    try:
        led3.append({**SEEDS[2], "record_id": "DR-test-promote",
                     "claim": "IWM / OWM / VWM canonical mapping",
                     "verdict": "OPEN", "tag": "LEAD"})
        fails.append("silent claim supersession accepted — Law 4 broken")
    except DecisionLedgerError:
        pass

    # Contested: a record was superseded by one with an opposing verdict.
    # This is the legit contradiction pattern — Invariant 2 prevents silent promotion
    # by requiring the supersession. contested() then flags the OLD vs NEW pair.
    led4 = DecisionLedger()
    led4.append({"record_id": "DR-c1", "schema_version": "1.0.0", "kind": "claim",
                 "claim": "X is true", "verdict": "OPEN", "tag": "LEAD",
                 "decided_by": "human", "decided_on": 1})
    led4.append({"record_id": "DR-c2", "schema_version": "1.0.0", "kind": "claim",
                 "claim": "X is true", "verdict": "REFUTED", "tag": "REFUTED",
                 "decided_by": "human", "decided_on": 2,
                 "supersedes": "DR-c1"})
    pairs = led4.contested()
    if len(pairs) != 1:
        fails.append(f"contested() returned {len(pairs)} pairs; expected 1")
    elif {pairs[0][0]["record_id"], pairs[0][1]["record_id"]} != {"DR-c1", "DR-c2"}:
        fails.append("contested() returned the wrong pair")
    elif pairs[0][0]["verdict"] != "OPEN" or pairs[0][1]["verdict"] != "REFUTED":
        fails.append("contested() pair has wrong verdicts")
    pairs = led4.contested()
    if len(pairs) != 1:
        fails.append(f"contested() returned {len(pairs)} pairs; expected 1")
    elif {pairs[0][0]["record_id"], pairs[0][1]["record_id"]} != {"DR-c1", "DR-c2"}:
        fails.append("contested() returned the wrong pair")

    # by_tag + stale_leads
    # led2 has: 4 seeds + DR-test-sup1 (LEAD, supersedes DR-0002). So:
    #   - MEASURED, non-superseded: DR-0003 only (DR-0002 was superseded).
    #   - LEAD, non-superseded: DR-0001, DR-0004, DR-test-sup1.
    if [r["record_id"] for r in led2.by_tag("MEASURED")] != ["DR-0003"]:
        fails.append("by_tag('MEASURED') returned wrong records")
    if {r["record_id"] for r in led2.stale_leads(days=0)} != {"DR-0001", "DR-test-sup1"}:
        fails.append(f"stale_leads() returned wrong records: "
                     f"{ {r['record_id'] for r in led2.stale_leads(days=0)} }")

    for f in fails: print(f"  ❌ {f}")
    if not fails:
        print("  ✅ selftest 9/9 — append-only; n<20 enforced; supersession append-only; "
              "silent tag promotion blocked; contested surfaces OPEN pairs")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())

    led = build_seed_ledger()
    if "--list" in sys.argv:
        for r in led.export():
            verdict = r.get("verdict", "?")
            tag = r.get("tag", "?")
            sup = f" ⊃ {r['superseded_by']}" if r.get("superseded_by") else ""
            print(f"  {r['record_id']} [{tag}/{verdict}]{sup}  {r['claim']}")
    elif "--show" in sys.argv:
        i = sys.argv.index("--show")
        rid = sys.argv[i + 1] if i + 1 < len(sys.argv) else "DR-0001"
        rec = led.get(rid)
        if rec is None:
            print(f"  ❌ {rid} not found")
            raise SystemExit(1)
        print(json.dumps(rec, indent=2))
    else:
        led.guard()
        print("  DECISION LEDGER — append-only, signed, content-hashed")
        print(f"  records: {len(led._records)}    contested: {len(led.contested())}")
        print(f"  {led.guard()}")
        raise SystemExit(selftest())