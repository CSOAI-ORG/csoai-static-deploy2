# VALS PROOF-POINT — the wedge, demonstrated (Opening 1, done)
**2026-08-19 · JEEVES · Live signed card on the pod · the artifact Vals cannot produce**

---

## What was built
`vals_proof_point.py` — produces a **signed, recomputable measurement card** for one GSPC axis: model identity + weights digest · axis + frozen anchors · full per-item transcripts + raw outputs · deterministic score (temp=0, exact-label predicate) · **Ed25519 signature over canonical JSON** · funding-wall statement.

## Live artifact (verified on the pod)
`/workspace/arena-24x7/proof/proof_card_1787134564.json`

| Field | Value |
|---|---|
| axis / model | gov / qwen3:4b |
| score | 0.25 (1/4) — honest: 2 UNMEASURED, 1 UNKNOWN, 1 YES |
| publisher | Council of AI (CSOAI Ltd, UK 16939677) |
| funding | no money from any graded party (EZ firewall) |
| verification | **PASS — recomputable, tamper-evident** |

## The wedge (why this beats the incumbent)
**Vals AI publishes a bare web dashboard** (verified: zero signing/attestation anywhere in their stack — docs, exports, Valkyrie harness, model pages). **We publish a signed card anyone can recompute without trusting us.**

The honest UNMEASURED handling is itself the differentiator: Vals' private sets are black boxes ("private" doing the work "verifiable" should do); our card publishes every transcript + the recompute path.

## The 90-day move (Openings 1+2+3, now queued)
1. **Signed-verification wall** — list every Vals score without a signed card (next build)
2. **Funding-wall charter** — publish the zero-to-graded-party attestation
3. **CorpFin retirement release** — re-measure Vals' retired benchmark openly

## SIGIL
`vals-proof-point-2026-08-19-jeeves`
