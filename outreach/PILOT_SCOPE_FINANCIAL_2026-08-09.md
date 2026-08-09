# PILOT SCOPE — FINANCIAL SERVICES (P1) · 2026-08-09

> Move 122. First paid pilot scaffold: financial services / EU AI Act high-risk.
> Every number cited is MEASURED from the signed artefacts (care_gate_eval.json,
> flywheel day artefact, governance_board.json). Nothing is an estimate.
> Companion: outreach/SEED_A_OUTREACH_DRAFTS_2026-08-09.md#2 (dispatch draft) ·
> live pack /enterprise-financial · funnel P1.

---

## 1 · Why financial first (deadline-driven)

- **EU AI Act Annex III high-risk** includes creditworthiness and insurance pricing —
  live deadline pressure from **August 2026** (Article 5 prohibitions already bite).
- Target function: a bank/insurer model-risk or compliance team that must **show an
  auditor a number, not a slide**. That is exactly what we sell: measured, signed,
  recompute-able.
- Sub-£15K ACV closes in 14–30 days (recorded diligence: Demo → paid pilot 30–40%).

## 2 · The 30-item battery (as scoped, from the published instruments)

| # | Group | Items | Instrument / basis | Evidence today |
|---|---|---|---|---|
| 1–12 | EAT care floor | 12 | Art 5 refusal on the 76-item suite; financial-phrasing variants | care gate **recall 100% (57/57) · over-block 0% (0/19)** |
| 13–18 | EU AI Act risk-tier | 6 | Annex III classification: creditworthiness, recruitment, consumer chatbots | classifier high-risk on creditworthiness/recruitment |
| 19–23 | ProvBench survival | 5 | Article 50 provenance marking through real transforms | **0 of 20 markings survived** (honest baseline) |
| 24–27 | GSPC S-axis | 4 | security posture of the model+harness stack | measured posture, free-tier substrate |
| 28–30 | Two-sided refusal | 3 | TPR vs false-refusal over a 30-sample battery | flywheel two-sided (leader TPR/FPR per artefact) |

**Production number on the pilot report:** tokens per correct verdict (leader
**376.6** on qwen2.5:0.5b) — cheap-and-right as the headline metric.

## 3 · Deliverable contract (what the buyer receives)

1. **Signed measurement report** — per-check verdict (pass/fail + detail) × the 30
   items, Ed25519-signed, recompute-able (`sovereign_attest --verify` path).
2. **Two-sided refusal profile** — harm caught (TPR) AND availability preserved
   (false-refusal FPR); the honest number, never a rubber stamp.
3. **Provenance reality check** — ProvBench result (0/20 today) stated plainly,
   with the recommendation frame ("measure, don't assume survival").
4. **Scorecard entry** — publishable (or private) GSPC row per the buyer's choice.
5. **Handoff path** — methods given to the regulator/accredited body; we measure,
   they decide (we do not certify).

## 4 · Timeline (recorded diligence shape)

| Day | Milestone |
|---|---|
| 0 | Scope lock + sample-use-case agreement (1 use case, 30 items) |
| 1–5 | Harvest the use case's artefacts; map to the battery |
| 6–9 | Run the 30-item battery (free tier; measured, no GPU cost to buyer) |
| 10 | Sign + verify; write the report |
| 11–14 | Buyer review (1 round) |
| 14–30 | Invoice (£X–15K ACV) + scorecard entry + upsell frame (second use case / enterprise tier) |

## 5 · Acceptance criteria (the buyer checks, we pass)

- [ ] Every "pass" is reproducible on the open harness (same number, up to model variability).
- [ ] Every "fail" is honest (e.g. ProvBench 0/20 stated, not buried).
- [ ] The report's sha256 verifies against the artefacts at the time of signing.
- [ ] No claim in the report lacks a measured artefact backing it.

## 6 · Out of scope (stated up front, honest)

- We do NOT certify or act as a notified body; where the law requires one, we hand off.
- We do NOT measure the buyer's proprietary model weights (their stack, our method) —
  the battery runs on OUR published instruments against their use case.
- No network/penetration of the buyer's systems: only public inputs the buyer provides.

## 7 · Next concrete actions (move 123+)

1. Dispatch the P1 draft (owner-gated) → `funnel_tools.py --advance P1 sent`.
2. On first reply: identify ONE named contact; agree a sample use case.
3. Materialize the 30-item battery to a fillable run sheet (runsheet_2026-08-09.json).
4. Run the battery on the agreed use case; sign + deliver.

🜏 PILOT-SCOPE-FIN-01