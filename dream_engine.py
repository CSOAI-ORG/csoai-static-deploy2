#!/usr/bin/env python3
"""dream_engine.py — stage the JEPA world-model bet. Shape the honey, pre-register the test. NO training.

    python3 dream_engine.py --stage      # build the corrective dataset + write the pre-registration

WHAT THIS IS, AND WHAT IT REFUSES TO BE
The SOVOS GOAL doc names a "Dream Engine — JEPA-style future prediction, trains while you sleep." The
honest, buildable version is a CORRECTIVE OPERATOR trained on the estate's own honey to reduce a
MEASURED drift — e.g. qwen3's systematic under-call of EU AI Act risk (LIMITED→MINIMAL ×44). Not "a
model that tops all benchmarks" (measured dead five times); a small operator that, run over run, gets
measurably better against dated law — or is retired.

This file does two honest things and stops:
  1. STAGE — shape honey rows into a corrective dataset (context → correct label; the drift is the
     documented hard negative). It refuses to build from nothing (empty = fatal).
  2. PRE-REGISTER — write the measurement contract BEFORE any training exists: the hypothesis, the
     metric, the n, the significance AND sign test, and the exit criterion. This is the estate rule
     that an earlier verdict line broke by printing "beats" for a negative delta.

It does NOT train. Training is GPU + owner gated. Two hard barriers apply at the training edge, not
here: (1) the corrective test MUST run on the PRIVATE held-out split, never the trained rows —
contamination is the defect that produced the 63% train-on-test result; (2) no capability is claimed
until it is measured at n>=30 with a CI clear of zero. A staged dataset is real; a trained operator is
not, so this file will not pretend to have one.
"""
import argparse, glob, json, os, sys, collections

SIG = os.path.expanduser("~/clawd/_alignment/SOV_SIGNAL")
OUT = os.path.expanduser("~/clawd/_alignment/dream")
PREREG = os.path.expanduser("~/clawd/_alignment/DREAM_ENGINE_PREREG.md")


def stage():
    rows = []
    for f in sorted(glob.glob(f"{SIG}/*.jsonl")):
        rows += [json.loads(l) for l in open(f, errors="ignore") if l.strip()]
    honey = [r for r in rows if r.get("outcome") == "wrong"]
    if not honey:
        sys.exit("NO HONEY: 0 wrong rows in SOV_SIGNAL. Measure first — a Dream Engine trained on "
                 "nothing is the emptiest false success of all.")
    by_axis = collections.Counter(r["axis"] for r in honey)
    os.makedirs(OUT, exist_ok=True)
    ds = f"{OUT}/dream_dataset.jsonl"
    with open(ds, "w") as f:
        for r in honey:
            # corrective example: given the item, the target is the measured-correct label; the model's
            # own drift is recorded as the hard negative it must stop choosing.
            f.write(json.dumps({"context": r.get("item", ""), "axis": r["axis"],
                                "target": r["gold"], "hard_negative": r.get("pred"),
                                "anchor": r.get("anchor"), "source_model": r.get("model")}) + "\n")
    print(f"staged {len(honey)} corrective examples → {ds}")
    for ax, n in by_axis.most_common():
        print(f"  {ax:<12} {n} examples")
    print("\n  NOTE: axes the board marks DEAD (no cross-model discrimination) still carry a real,\n"
          "  correctable single-model drift — but any claim of improvement MUST be measured on the\n"
          "  PRIVATE held-out split, never these trained rows.")
    write_prereg(len(honey), dict(by_axis))
    print(f"\n  pre-registration written → {PREREG}")
    print("  Dream Engine: STAGED. Training is GPU+owner gated. No operator exists yet; none is claimed.")


def write_prereg(n, by_axis):
    dominant = max(by_axis, key=by_axis.get) if by_axis else "—"
    open(PREREG, "w").write(f"""# Dream Engine — pre-registration (written BEFORE any training)

**Status: STAGED, not trained.** This contract is fixed before the operator exists so the result cannot
be rationalised after the fact.

## Hypothesis
A small operator fine-tuned on {n} honey rows (this model's measured errors against dated, anchored
labels) reduces its dominant measured drift — currently **{dominant}** — on **held-out** items, without
degrading the axes it already handles.

## Data
- Train: `~/clawd/_alignment/dream/dream_dataset.jsonl` ({n} corrective examples: context → correct
  label, with the model's own wrong answer as the hard negative).
- Test: the **PRIVATE held-out split** of each GSPC bank (never uploaded, never trained on). If a theme
  appears in training, the whole theme leaves the test set (theme-level contamination barrier).

## Metric & decision rule
- Primary: accuracy on the held-out split, per axis, base operator vs corrected operator.
- Decision: improvement is claimed **only if** the paired delta's 95% CI is **clear of zero AND positive
  in sign** (an earlier verdict printed "beats" for a −9.16 delta by testing only CI-excludes-zero).
- Gate: no interval, and no win, reported below **usable_n ≥ 30** — including ours.

## Kill criterion
If the corrected operator does not beat base on any axis at n≥30 with a CI clear of zero, the operator
is **retired**, not re-rolled. "Tops all benchmarks" is not a hypothesis this can confirm; "gets
measurably better on a specific axis" is.

## Compute
I-JEPA / LeWorldModel-class training needs funded A100s (paper: 632M params ≈ 16×A100 / 72h). Owner
decision required before spend. Until then this stays staged: dataset + this contract, no training.

*Measurement, not certification. Nothing here is legal advice. — csoai.org*
""")


def main():
    ap = argparse.ArgumentParser(description="Dream Engine — stage + pre-register, never train here")
    ap.add_argument("--stage", action="store_true")
    a = ap.parse_args()
    if a.stage: stage()
    else:
        print("Dream Engine — the honest JEPA bet.\n  --stage  shape honey + write the pre-registration.\n"
              "  Training is GPU+owner gated and is not in this file. No operator is claimed until measured.")


if __name__ == "__main__":
    main()
