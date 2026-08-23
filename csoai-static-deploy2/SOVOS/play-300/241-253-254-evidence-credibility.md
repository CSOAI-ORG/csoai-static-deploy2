# 241 / 253 / 254 — EVIDENCE & CREDIBILITY DRAFTS (Movement 8)

Date: 2026-08-21 · lane: K3 (prereg/memo) / POD+LANE (signed cards) · stack legitimacy assets (D10 §6).

## 241 — OSF preregistration (measurement methodology)
Pre-commit: hypotheses, instruments, scoring, exclusions → OSF DOI.
Signed-methodology page: every method doc hash-anchored + POD-signed.

## 243–245 — First signed measurement cards (👑 POD+LANE)
COSE_Sign1 alg -19 · iss = independent evaluator · sub = measured subject (the inversion).
Card = score vector + CI + suite digest + environment commitment + replay Merkle root + method +
timestamps. Public verify endpoint (one URL, offline-verifiable, cosign-bundle pattern).
**Gate: ≥1 card stranger-verifiable (REAL: zero signed score attestations, H9/D01 §5).**
→ BLOCKED on POD key injection (owner-gated). The sim h3k card (ed25519) already proves the pipeline.

## 253 — ICLR abstract (signed measurement cards + arena fairness)
Contribution: first buyer-side, offline-verifiable signed score attestation + a velocity-cap
fairness methodology. Feeds step 126/252.

## 254 — in-toto predicate memo
Pipeline stages (build→run→score→leaderboard) as signed DSSE links — predicate schema (D02 §2).

## Non-endorsement (binds)
15 CFR 200.113-style disclaimer on every card: measurement, not approval. Incident-report
transparency policy (AISI Aug 6 self-report = model). Correction-receipt runbook (supersession chain).

## Status
Drafts v0.1. OSF/ICLR submission = external (NICK/Claude). Signed cards = POD-key-gated.
UNSIGNED until POD key.
