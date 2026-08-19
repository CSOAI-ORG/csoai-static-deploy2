# arXiv Paper Draft — The Gap Map and the Signed Measurement Instrument
**Council of AI (CSOAI Ltd, UK 16939677) · 19 Aug 2026 · ready for the 27 Aug endorsement gate**

> ⚠️ OWNER/COUNSEL GATE — do not submit until: (1) the over-block cost figures are confirmed as
> *modeled from measured inputs*, not observed market outcomes; (2) the word "benchmark/index" is
> cleared against IOSCO/EU-BMR scope if the paper is later tied to a commercial signal; (3) no
> "certified/compliant" language anywhere; (4) the arXiv endorsement ticks land (27 Aug — Nick's
> clock). Zenodo DOI 10.5281/zenodo.21991105 already mints the corpus, so the paper is
> citable even if the arXiv channel slips.

---

## Title (proposed)

**The Gap Map: Zero of 417 Statutory Provisions Are Covered by Public AI-Governance Benchmarks, and a Signed Instrument That Can Measure the Gap**

## Authors

Council of AI (CSOAI Ltd, UK 16939677) — measurement body; no individual author names on the
preprint (neutrality + firewall; add co-authors by name only after the naming ruling, 11 Sep).

## Abstract (draft)

AI-governance claims today are largely self-reported or ungrounded: a model card may assert
safety with no verifiable method, and a compliance claim can outlive the regulation it rests on.
We quantify the measurement gap itself. Across **417 frozen statutory provisions** from six EU
regulations (EU AI Act 2024/1689: 126, GDPR 2016/679: 99, Cyber Resilience Act 2024/2847: 71,
DORA 2022/2554: 64, NIS2 2022/2555: 46, CSRD 2022/2464: 11), we evaluate 13 public benchmark
frameworks against a provision × axis × mode grid of **3,336 cells**: **zero cells are fully
covered** by any public benchmark, 16 are partially covered, and **3,320 are absent**. The
corpus is sha256-anchored and open (DOI 10.5281/zenodo.21991105); the crosswalk is public and
re-computable.

We then present the instrument that measures against that gap: **GSPC**, an open measurement
framework with three properties current benchmarks lack. **(1) Deterministic grading** — no
judge model; every item is scored by exact rule, so results are reproducible bit-for-bit.
**(2) A first-class UNMEASURED state** — items a system refuses or answers uninterpretably are
reported as UNMEASURED, never silently coerced to zero, so the score cannot flatter a system by
counting non-answers as failures or successes. **(3) Grounded legal claims** — every statutory
citation is checked against an exact registry, and an answer that cites a non-existent or
mis-attributed article cannot pass as verified. Results are **Ed25519-signed** measurement
credentials and independently re-computable offline with only the published public key.

Using the instrument we measure 13 of 14 quotable axes on our own fleet (n≥30 signed cells,
jail axis honest-empty until a gold bank completes), and quantify **over-refusal as a business
cost**: modeled from measured over-block rates at 100,000 requests/month, an all-refusal
baseline carries a **$67.5k/month** false-refusal cost while a composed model achieves the same
refusal rate and zero harmful leakage at **$28.9k/month — a 57% reduction** (modeled, not
observed P&L). We further show the measurement resists Goodharting: improvement is gated on a
held-out probe split the model never trains on.

**Two demand-side motivations frame why the gap matters now.** First, the Ninth Circuit's
4 Aug 2026 decision in *Amazon v. Perplexity* makes **consent checkpoints the evidentiary
safe harbour** for web-interaction claims — the proof-of-consent burden is now a measurable,
recordable behaviour, and an instrument that signs evidence of it is directly load-bearing.
Second, the UK AISI's incident reporting cadence has made **demand for independently verified
behavioural evidence** concrete: incident response needs a measurement of what a system did,
not a vendor's assertion of what it is.

We release the harness, the frozen probe banks, the corpus anchor, and the signed result
cards, so any party can re-compute and verify every number in this paper. **This is
measurement, not certification.**

## Structure

1. **Introduction** — the claim-to-evidence gap; the demand side (Ninth Circuit safe harbour;
   AISI incident cadence; insurance and procurement needing verifiable behaviour).
2. **The Gap Map** — 417-provision corpus construction (CELEX-keyed, frozen, hash-anchored);
   the 13-framework × 4-axis × 2-mode grid; counting rule (COVERED/PARTIAL/ABSENT); the
   result: 0 / 16 / 3,320; honest scoping (46.1% unclassified residual stated; the absolute-zero
   claim is scoped against COMPL-AI / Bench-2-CoP partial findings).
3. **The Instrument (GSPC)** — deterministic grading (exact-rule, no judge model);
   UNMEASURED as first-class; grounded legal citations; Ed25519 signed cards
   (id = sha256 of canonical body; signature = Ed25519(id); prev links the chain); offline
   verification with the public key only.
4. **Measured Results** — 13 of 14 quotable axes on our fleet (n≥30 cells, CIs); human
   baselines from published external cohorts (MMLU expert ~89.8%, GPQA diamond PhD ~81%,
   ARC-AGI human ~85% — signed cells); the jail axis reported honest-empty until n≥30
   signed cells exist.
5. **Over-refusal as a business cost** — modeled from measured over-block rates; the $67.5k
   vs $28.9k/month comparison; honest hedge: modeled, not observed.
6. **Anti-Goodhart discipline** — held-out probe split; leak-free self-test (19/19);
   fuel law (practice set public, reply_head practice-only).
7. **Demand-side framing** — Ninth Circuit consent checkpoints; AISI incident cadence;
   the insurer pitch (30 Sep) and Article 50 retrofit (2 Dec) as applied consumers.
8. **Reproducibility** — corpus anchor, crosswalk, boards, cards, key: everything public.

## Explicitly REMOVED (do not reintroduce)

- The "33-member Byzantine-Fault-Tolerant safety council" and "22/33 supermajority" framing.
  Measured effective independence is n_eff ≈ 1.21 of 3 nominal legs — the council is **not**
  BFT; a voting-independence claim would be a known-false statement.
- Any "certificate / certified / guarantees compliance" language. Cards are signed
  **measurements** — say "measured", never "certified".
- Internal codenames (SOV3/SOV33, DEFONEOS, OOWM, SOVOS, EAT) and any sov-* engine/product
  names — public names only: Council of AI / CSOAI, GSPC, MEOK.
- Unscoped absolute-zero claims about *all* benchmarks ever — the gap is scoped to the 13
  frameworks and 417 provisions in the frozen corpus.

## Honest hedges to keep in the paper

- The $67.5k / $28.9k figures are **modeled** from measured over-block rates, not observed P&L.
- "Composed model" gains attribute to deterministic layers; per-dimension routing and statute
  retrieval were measured and did **not** beat a single good model — report that, it
  strengthens credibility.
- The jail axis is honest-empty until n≥30 signed cells; the 13-of-14 framing is quotable
  *because* the empty axis is reported, not hidden.
- External re-compute witness (an academic/AISI-style re-runner co-signing a sample) is the
  single most credibility-additive step — recruit one before or just after submission.

## Submission checklist (27 Aug gate)

- [ ] arXiv endorsement ticks secured (Nick)
- [ ] Counsel clears "benchmark/index" wording vs IOSCO/EU-BMR (11 Sep package can be
      before-or-after; do not block on it — the paper says "measurement instrument",
      not "index")
- [ ] Over-block cost figures confirmed as modeled-from-measured (this lane)
- [ ] No cert/compliance language anywhere (final grep: certify|certified|compliant|guarantee)
- [ ] Zenodo DOI cross-linked (10.5281/zenodo.21991105 — corpus; 10.5281/zenodo.21973003 —
      methodology citation in AGENTS.md)
- [ ] Signed card chain + public key path included in the reproducibility appendix
