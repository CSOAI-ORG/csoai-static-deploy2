# CANNONBALL DRAFTS — STAGE 2 (2026-08-19)
**JEEVES · K3 lane · coordinate-first, one genuine contribution per upstream · all ready to send**

---

## C1 — proofbundle coordinate-first comment (Inspect issue #4413)
**Target:** UK AISI Inspect repo issue #4413 (open since Jul 3 — "signed eval receipts" ask, unanswered)
**Who:** proofbundle (2-star single-maintainer MIT project) authored it; CSOAI-ORG commented today

**The draft comment (coordinate-first, merge > format war):**
> Thanks for opening this — it's exactly the right ask. We're building the same thing from the governance side (CSOAI — Council of AI): Ed25519-signed eval receipts with did:web identity binding, supersession/correction chains, per-sample evidence, offline verification, and an appeals path. proofbundle's crypto+prereg + our identity+standing covers the full stack.
>
> Proposal: one common receipt envelope instead of two. Schema sketch: `{schema, model_digest, harness, items[], score, ci, signature, did, anchor}` — signed over RFC 8785-canonical JSON, Rekor+TSA anchored, offline-verifiable. Happy to draft the merged schema as a PR against whichever repo you prefer. The measurement layer is the point — nobody with standing signs eval results yet.

**Why:** merge of efforts > format war at 2 stars vs 0. Common envelope = the receipt format wins by authorship.

## C2 — Terminal-Bench 3.0 contact note
**Target:** tbench.ai (74-task set, 4 days old, publishes cheating audits — receipt-friendly venue)
**Draft:**
> Hi Terminal-Bench team — we run deterministic, signed evaluation predicates (13 of 14 GSPC axes, Ed25519 receipts, honest UNMEASURED). Your cheating-audit posture matches our anti-BenchJack doctrine. Would you accept a signed-run-format contribution — receipts that attach to each scored submission (hash of run config + per-item transcripts + predicate output)? Happy to draft the PR.

**Why:** receipt-friendly young venue; their integrity focus is our register.

## C3 — Appia membership brief (for Nick)
**The one-pager:**
- **What:** Appia Foundation (JDF) — conformity-evidence specs forming NOW; first-mover window
- **Cost:** JDF membership mechanics (voting seat = paid; contributor = free)
- **Scope (firewall-safe):** evidence-format contribution only, never certification (HO.1 holds)
- **The play:** their charter says they "will not conduct conformity assessments" — the executor's chair is empty; we are the measurer
- **Decision:** contributor tier now (free), voting seat only if the evidence-format leadership justifies it

## C4 — EEE (Every Eval Ever) schema-compat sketch
**The receipt as an EEE provenance block:**
- EEE DB: 22,235 models / 2,273 benchmarks, Inspect/lm-eval/HELM converters exist
- **Our move:** emit receipts with an `eee_provenance` field — schema-compat so EEE's DB can ingest our signed results without a new converter
- **Draft field:** `"eee": {"model": "<id>", "benchmark": "<id>", "result": <score>, "provenance_hash": "<sha256 of run config>"}`
- **Why:** our receipts become the *only signed rows* in the largest eval DB on earth

## SIGIL
`cannonball-drafts-c1-c4-2026-08-19-jeeves`
