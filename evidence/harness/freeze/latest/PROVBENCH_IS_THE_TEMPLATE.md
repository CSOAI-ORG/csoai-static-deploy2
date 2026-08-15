# ProvBench already does everything the MISSING_REGISTER says is missing

Mined every canon artifact for "does the number resolve to the things it counts". Most did not.
**ProvBench does — and then does five more things nothing else in the estate does.**

The improvement this session was reaching for does not need inventing. It exists in-house, in
one benchmark, and was never propagated.

---

## What ProvBench has, measured from `provbench-n20.json`

| property | ProvBench | GovBench (before today) |
|---|---|---|
| **Pre-registered predictions** | **110 predictions, 110 cells, 0 disagreements** | none |
| **Confidence interval per cell** | every cell carries `ci` | none — Gap 1 |
| **UNMEASURED as a distinct outcome** | `unmeasured` field per cell, with the actual exception recorded | added today |
| **Environment provenance** | sdk version, TSA, signing alg, trust anchor | added today (grader hash) |
| **Explicit caveats** | 8, and they argue *against* the result | none |
| **Alternative statistics reconciled** | rule-of-three 0.15 vs Wilson one-sided 0.119, both published | none |

The canonical: `k=0, n_assets=20, rule_of_three_upper=0.15, wilson_one_sided_upper=0.119`.

---

## The caveats are the tell

These are not disclaimers. They are arguments against the estate's own headline:

> *"A surviving signature proves PROVENANCE, NOT CORRECTNESS."*

> *"Our certificate chains to a PRIVATE ROOT CA that is NOT on the C2PA trust list."*

> *"sidecar_oracle is the MOST FAVOURABLE assumption available — the harness hands the detached
> manifest straight to the verifier."*

> *"Transforms are applied by Pillow. A different re-encoder (libvips, ImageMagick, a phone ISP,
> a CDN) may behave differently."*

And the UNMEASURED entry is a real exception, not a placeholder:
`format_convert_heic: TransformUnavailable: no HEIF encoder: KeyError: 'HEIF'`

A benchmark that publishes "our trust anchor is not trusted" and "we gave ourselves the most
favourable assumption" is doing the thing the rest of the estate has been failing at all day.

---

## Why this matters more than any fix I made today

Every defect found this session — fabricated zeros, four grader bugs, missing intervals, no
control arm, a number that doesn't resolve to its things — is **already solved in this file**.
The estate did not have a methodology problem. It had a **propagation** problem: its best
practice lived in one benchmark and never became the house standard.

That reframes the MISSING_REGISTER. Gaps 1, 2, 5 and 6 are not research tasks. They are
**port ProvBench's structure to the other five axes**:

1. **Pre-register predictions** before any run. ProvBench got 110/110 right, which is itself
   evidence the instrument is understood — and a disagreement would have been the most
   valuable output available.
2. **CI on every cell**, not just the headline.
3. **UNMEASURED carries its exception text**, so the reason survives.
4. **Environment block** on every result.
5. **Caveats that argue against your own finding**, published with it.
6. **Reconcile alternative statistics** rather than picking the flattering one.

---

## The one thing ProvBench lacks

A **control arm**. It measures survival of markings under transforms, where a control is less
natural — but "an unmarked asset subjected to the same transforms" would establish the
false-positive floor. Worth adding when it is next re-run.

---

## Recommendation

Make `provbench-n20.json` the **schema of record** for every axis. The six-axis e2e harness
built today already carries CI, UNMEASURED, control arm and a fingerprint; adding
pre-registration and a caveats block would bring it to ProvBench's standard.

Then the estate's claim stops being "we measure rigorously" as an assertion and becomes a
**format** — one another party can inspect, reproduce, and check the caveats of.
