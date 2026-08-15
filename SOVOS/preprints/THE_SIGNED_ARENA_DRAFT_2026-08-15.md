# The Signed Arena: Closed-Door Human-vs-AI Measurement

**Working title · Council of AI (CSOAI Ltd, UK 16939677) · draft v0.1 · 2026-08-15**
**Status: DRAFT for arXiv (owner-gated submission) · HELM-grade honesty rails**

---

## Abstract (draft)

The measurement of AI systems has bifurcated: deterministic benchmark
harnesses score models against fixed item banks, while a handful of
one-shot academic studies time human professionals against AI assistance.
Neither gives the market a *continuously-running, multi-domain, signed*
comparison of human and machine capability. This paper reports the
architecture and first results of the Signed Arena: a closed-door
measurement instrument in which human judgements and model outputs flow
through the *same* item bank, the *same* deterministic scorer, and the
*same* Ed25519-signing rails. We describe the bridge that lets a
human-supplied answer occupy the exact slot a model solver would occupy in
an Inspect-style pipeline, the deterministic gold (never a model judge),
and the paired signed/unsigned record format that makes every row
recompute-able by any third party. We connect the design to the METR RCT
(arXiv:2507.09089) — the strongest existing evidence that human-vs-AI
comparison is both contested and high-stakes — and position the arena as
the operational form of that study: a continuously-running experiment
instead of a snapshot.

**Claims made:** an architecture exists, runs, and produces signed
records. **Claims not made:** any certification, accreditation, or
"better than" ranking — the ruler is the instrument; results speak.

## 1. The gap

- **Frozen benchmarks** (GSPC boards, HELM, lm-eval) measure model vs gold.
- **One-shot studies** (METR devs, BCG consultants, MIT writing, call-centre
  RCT, MLE-bench vs Kaggle) measure human vs model on a single task class.
- **Missing:** a general, continuously-running, multi-domain instrument
  with timing + quality scoring across settings, producing signed output.

The arena closes exactly that gap: **same items, same scorer, both
species, signed**.

## 2. Architecture

```
        item bank (GSPC axes)
         ├── model solver  ──┐
         └── human solver ───┤  (empirica/oTree session, existing bridges)
                             ▼
                deterministic judge (exact-label gold;
                no model judges another)
                             ▼
        paired signed | unsigned records (Ed25519 spine,
        time-anchored, recompute-able)
```

Key modules (all in this repo, all self-tested):

| Module | What it does | Proof |
|---|---|---|
| `human_solver_bridge.py` | Human answer in the same slot as a model solver | 10/10 demo items, honest acc 0.80 |
| `csoai_scorer_signer.py` | Paired signed/unsigned Score emission | EAT-1, real Inspect |
| `grok_escape_gold.py` | Frontier model through the sandbox gold bank | precision 1.0 / recall 0.25 (n=11) |
| `daily_index.py` | One signed closing-cross value per day | 57.36 → 57.49 index |

## 3. Why signed matters (the honest thesis)

A measurement nobody can recompute is an anecdote. Every arena row is a
signed card: content digest, Ed25519 signature, time anchor, link to the
item and the gold. A human row and a model row have identical shape except
the `source` field — so downstream consumers can verify *both* with the
same public verifier. That's the difference between a leaderboard and an
instrument.

## 4. Relation to METR (the citation anchor)

METR's (2507.09089)-randomized trial found experienced open-source
developers were **19% slower** with AI while believing they were 20% faster.
That perception gap is the best evidence that human-vs-AI comparison is
both contested and consequential. This arena operationalizes the method:
publish methodology, run continuously, sign every row, report the deltas.
Where METR ran one trial, the arena runs every day.

## 5. Honest limitations

- Human-pass sample sizes are gated by cost (Prolific ~£12/hr); n<30
  cells are UNMEASURED by policy.
- Human-subjects data => DPIA is the controller record (drafted); Prolific
  is an independent controller.
- The static detector is regex-primitive-grade; paraphrase obfuscation
  may beat it (the gate's false-negative surface is an axis of study, not
  a hidden fix).
- No certification claim anywhere: "verified measurement credential" only.

## 6. Forkables & license compliance

- Empirica (Apache-2.0) for real-time multi-participant human side.
- oTree (MIT) for Python multiplayer; MIT confirmed from LICENSE file.
- Inspect AI (MIT) as the task/grading frame.
- Prolific as the human supply (paid, gated).

## 7. Next steps (owner-gated)

1. Owner approves Prolific spend (~£400-500).
2. Empirica seat on a host (Oracle micro or pod).
3. First 100-participant gold run -> n=100 per axis, Cohen's κ gate.
4. Signed cards enter the public register + the error statistics.

---

*Draft. For the record: this is measurement infrastructure disclosed
honestly, not a claim of user-consensus superiority, certified accuracy, or
market rank. arXiv submission requires owner endorsement (expires 27 Aug).*