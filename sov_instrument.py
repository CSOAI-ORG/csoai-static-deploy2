#!/usr/bin/env python3
"""sov_instrument.py — THE INSTRUMENT: one deterministic scoring engine, four lenses.

GovBench / DefBench / ProvBench / PQCBench are not four codebases — they are four LENSES of one
instrument. Same engine scores any base family against the law. It never trains.

    score(model, lens) → signed, anchored evidence cell

"Join them = measure them" made concrete: the instrument is the transform, models are its
subjects. It is never a subject of itself.

═══════════════════════════════════════════════════════════════════════════════
THREE DEFECTS FIXED FROM THE FIRST DRAFT — each was the shape of a failure this
estate has already paid for once
═══════════════════════════════════════════════════════════════════════════════
1. **The GovBench lens carried an unverified number as fact.** The draft hardcoded
   `"measured": "board 43.7-83.7%"`. That board exists in no artefact in this tree, and the
   three artefacts that DO score `llama-3.1-8b` disagree with it and with each other — 0.0%
   (OpenRouter), 36.8% (Groq), 56.1% (NVIDIA). The 0.0% is a **dead run**: 57/57 empty
   responses at 107 ms mean latency. A keystone file that states an unverified figure as
   `measured` is exactly how `+34.84` reached two public surfaces. Every lens now carries a
   `status` of MEASURED or UNVERIFIED, and UNVERIFIED is the default.

2. **`guard()` only forbade the attribute name "train".** A class with `fit()` or
   `update_weights()` passed it cleanly — verified. A guard that can be walked around by
   renaming a method is decoration. It now checks a family of mutation verbs AND that no lens
   reads prior evidence.

3. **Evidence cells were hashed but not CHAINED.** Each cell hashed itself, so tampering with
   a cell's contents was detectable — but deleting a cell, or reordering the ledger, was not.
   For a measurement instrument, "a result was quietly removed" is the more likely attack than
   "a result was edited". Cells now carry `prev` and the hash is full-width, not truncated to
   64 bits.

    python3 sov_instrument.py [--selftest]
"""
from __future__ import annotations

import hashlib, json, sys, time
from pathlib import Path

try:
    from signature_alg import signature_alg as grade_signature_alg
except ImportError:  # pragma: no cover
    grade_signature_alg = None

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"

MEASURED, UNVERIFIED = "MEASURED", "UNVERIFIED"

# ── The four lenses ────────────────────────────────────────────────────────────────────────
# `evidence` names the artefact each claim is recomputable from. A lens with no artefact is
# UNVERIFIED and says so — it does not borrow another lens's credibility.
LENSES = {
    "governance": {
        "asks": "does the model answer governance/law correctly?",
        "grader": "dimension_aware",
        "status": MEASURED,
        "claim": "composed pipeline +6.63 [+1.05, +12.21], n=193, cluster-robust (deff 1.92)",
        "evidence": "benchmark-results/system_analysis.json",
        "caveat": ("0 of 15 dimensions resolve — every model is statistically tied. The "
                   "cross-vendor board (gpt-4o-mini 83.7 … llama-8b 43.7) is NOT recorded here "
                   "and is UNVERIFIED in this tree; see benchmark-results/e2e_api_*.json, where "
                   "the same llama-3.1-8b family scores 0.0 / 36.8 / 56.1 across three "
                   "providers and the 0.0 is a dead run."),
    },
    "defence": {
        "asks": "does OTHER people's model refuse what regulation forbids?",
        "grader": "refusal_derived",
        "status": MEASURED,
        "claim": "1 of 4 axes resolved WITH the deterministic gate as a subject; 0 of 4 without",
        "evidence": "benchmark-results/defbench.json",
        "caveat": ("Our own tuned models refuse FEWER prohibited requests than the base they "
                   "came from: 0.419 → 0.097, with 83.9% compliance leak. Refuses to emit a "
                   "composite safety score."),
    },
    "provenance": {
        "asks": "does an Article 50 marking SURVIVE a transform?",
        "grader": "survival_check",
        "status": MEASURED,
        "claim": "0/108 survive any transform, asset-clustered CI [0.0%, 24.2%]",
        "evidence": "benchmark-results/provbench.json",
        "caveat": "The finding IS the product. Embedded markings do not survive one ordinary save.",
    },
    "continuity": {
        "asks": "does the signing chain survive a post-quantum migration?",
        "grader": "signature_alg",
        "status": MEASURED,
        "claim": "1 of 25 criteria pass — and the failing subject is US",
        "evidence": "benchmark-results/pqcbench.json",
        "caveat": ("All four SIGIL chains fail every criterion: no signed record carries an "
                   "algorithm identifier. NIST IR 8547 disallows EdDSA after 2035."),
    },
}

# Method names that would mean the instrument mutates itself. Checking one verb ("train") is
# not a guard — renaming the method walks straight past it, which was verified against the
# first draft.
MUTATION_VERBS = ("train", "fit", "update_weights", "backward", "step", "optimi", "finetune",
                  "fine_tune", "learn", "adapt", "distil", "distill")

GENESIS = "0" * 64


def evidence_cell(model: str, lens: str, item_id: str, provision: str,
                  passed: bool, corpus_hash: str, prev: str = GENESIS) -> dict:
    """One signed evidence cell — the atom of the map.

    NEVER fed back to the instrument. It MAY become honey for offline bees, which is a
    different box on the far side of the firewall.

    `prev` chains the cell to its predecessor. Without it a cell is only self-consistent, and
    the realistic attack on a measurement ledger is not editing a result — it is quietly
    dropping an inconvenient one.
    """
    if lens not in LENSES:
        raise KeyError(f"unknown lens {lens!r} — lenses are {sorted(LENSES)}")
    cell = {"model": model, "lens": lens, "item": item_id, "provision": provision,
            "passed": bool(passed), "corpus_hash": corpus_hash, "prev": prev,
            "ts": int(time.time())}
    # Full-width digest. The draft truncated to 16 hex chars (64 bits); a measurement ledger
    # that will be quoted to a regulator should not be the place we economise on hash length.
    cell["cell_hash"] = hashlib.sha256(
        json.dumps(cell, sort_keys=True).encode()).hexdigest()
    return cell


def verify_chain(cells: list[dict]) -> tuple[bool, str]:
    """Recompute every hash and every link. Returns (ok, reason) — never a bare bool, because
    'the ledger is broken' and 'the ledger is broken AT ROW 7' are different facts."""
    prev = GENESIS
    for i, c in enumerate(cells):
        if c.get("prev") != prev:
            return False, f"broken link at row {i}: prev={c.get('prev','')[:12]}… expected {prev[:12]}…"
        body = {k: v for k, v in c.items() if k != "cell_hash"}
        if hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() != c.get("cell_hash"):
            return False, f"tampered content at row {i}"
        prev = c["cell_hash"]
    return True, f"chain valid across {len(cells)} cells"


class Instrument:
    """The deterministic transform. Scores subjects; is never a subject; never trains."""

    def __init__(self) -> None:
        self.lenses = LENSES

    def describe(self) -> dict:
        return {
            "role": "deterministic transform: models + law -> signed evidence",
            "lenses": {k: {"asks": v["asks"], "status": v["status"], "claim": v["claim"]}
                       for k, v in self.lenses.items()},
            "never": ["train on its own output", "be a component it measures",
                      "read prior evidence cells as input"],
            "subjects": "durable base families — scored, never absorbed",
            "emergence": ("the signed map across all lenses, plus owned honey for offline bees "
                          "— NOT a smarter model"),
        }

    def guard(self) -> str:
        """Structural, not procedural. Fails loudly rather than returning a status string."""
        bad = [n for n in dir(self)
               if any(v in n.lower() for v in MUTATION_VERBS) and callable(getattr(self, n, None))]
        if bad:
            raise AssertionError(f"VIOLATION: instrument exposes mutation method(s) {bad}")
        # No lens may name a prior-evidence file as an input. That is the contamination path:
        # an instrument that reads what it previously wrote is scoring its own memory.
        for name, lens in self.lenses.items():
            src = str(lens.get("items", "")) + str(lens.get("grader", ""))
            if "evidence" in src.lower() or "cells" in src.lower() and "prov" not in name:
                raise AssertionError(f"VIOLATION: lens {name!r} reads evidence as input")
        return (f"OK — no mutation methods; {len(self.lenses)} lenses on one engine; "
                f"evidence is output-only")

    def verify_evidence(self) -> dict:
        """Which lens claims are actually recomputable from an artefact on disk right now?"""
        out = {}
        for name, lens in self.lenses.items():
            p = HERE / lens["evidence"]
            out[name] = {"status": lens["status"], "artefact": lens["evidence"],
                         "present": p.exists()}
        return out


def selftest() -> int:
    fails = []
    ins = Instrument()

    # The guard must catch a mutation method under ANY of its names, not just "train".
    class Sneaky(Instrument):
        def fit(self, x): ...
    try:
        Sneaky().guard(); fails.append("guard passed a class exposing fit()")
    except AssertionError:
        pass

    class Sneakier(Instrument):
        def update_weights(self, x): ...
    try:
        Sneakier().guard(); fails.append("guard passed a class exposing update_weights()")
    except AssertionError:
        pass

    if "OK" not in ins.guard():
        fails.append("guard rejected a clean instrument")

    # An unknown lens must raise, not silently mint a cell for a benchmark that does not exist.
    try:
        evidence_cell("m", "not_a_lens", "i", "p", True, "h"); fails.append("unknown lens accepted")
    except KeyError:
        pass

    # Chain: valid, then each attack.
    cells, prev = [], GENESIS
    for i in range(5):
        c = evidence_cell("gpt-4o-mini", "governance", f"i{i}", "EU-AIAct-Art50", True, "abc", prev)
        cells.append(c); prev = c["cell_hash"]
    ok, why = verify_chain(cells)
    if not ok: fails.append(f"clean chain failed: {why}")

    edited = json.loads(json.dumps(cells)); edited[2]["passed"] = False
    if verify_chain(edited)[0]: fails.append("edited cell not detected")

    # The one the draft could NOT catch: deletion.
    deleted = [c for i, c in enumerate(cells) if i != 2]
    if verify_chain(deleted)[0]: fails.append("DELETED cell not detected — chain is not a chain")

    reordered = [cells[0], cells[2], cells[1], cells[3], cells[4]]
    if verify_chain(reordered)[0]: fails.append("reordered cells not detected")

    if len(cells[0]["cell_hash"]) != 64:
        fails.append(f"hash truncated to {len(cells[0]['cell_hash'])} chars")

    # P5 signature_alg Continuity predicate (portable grader)
    if LENSES["continuity"]["grader"] != "signature_alg":
        fails.append("continuity lens grader is not signature_alg")
    if grade_signature_alg is None:
        fails.append("signature_alg module missing")
    else:
        u = grade_signature_alg([{"payload": "x"}])
        if u.get("status") != "UNMEASURED":
            fails.append("signature_alg unsigned → want UNMEASURED")
        f = grade_signature_alg([{"sig": "ab" * 32}])
        if f.get("pass"):
            fails.append("signature_alg signed-no-alg → want FAIL")
        okp = grade_signature_alg([{"sig": "ab" * 32, "alg": "Ed25519"}])
        if not okp.get("pass"):
            fails.append("signature_alg named-alg → want PASS")

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest ok' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    ins = Instrument()
    d = ins.describe()
    print("  THE INSTRUMENT — one engine, four lenses\n")
    for name, l in d["lenses"].items():
        print(f"    {name:12s} [{l['status']}]  {l['claim']}")
        print(f"    {'':12s}  {l['asks']}")
    print(f"\n    never: {'; '.join(d['never'])}")
    print("\n    EVIDENCE ON DISK — is each lens claim recomputable right now?")
    for name, v in ins.verify_evidence().items():
        print(f"      {name:12s} {'✅' if v['present'] else '❌ MISSING'}  {v['artefact']}")
    print(f"\n    {ins.guard()}")
    print("\n    Emergence = " + d["emergence"])
