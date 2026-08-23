# PUBLICATION LAUNCH KIT — 2026-08-22 (mass growth)

Draft for the mass-growth publication. EVERYTHING here is backed by the signed evidence
(`SOVOS/evidence/`), so each piece links to a stranger-verifiable artifact.

## 1. THE HOOK (headline)
> **We measured the frontier — and you can verify every result without trusting us.**

## 2. LANDING PAGE COPY (verify surface)
# CSOAI — the independent measurement body
The AI industry's self-reported scores are unsigned. We measured frontier base models + our own
sovereign models on 16 governance axes, on a **clean sequential protocol**, and made **every result
cryptographically verifiable** — Ed25519-signed on a signing node (key never leaves), confirmable
in-browser or with one command.

**Measurement, not certification.** We never take money from the scored. Buyer/insurer/regulator-pays
only.
[Verify the evidence] [Read the methodology]

## 3. THE THREE FINDINGS (citable, spreadable)
1. **Retrieved knowledge beats trained knowledge** — RAG context lifts governance scores by **+34–38
   points** (confound-free, measured on 4 base models).
2. **At the same size, base beats our own fine-tunes** — base qwen2.5:0.5b (32.6) > sov33-v7 (19.8) >
   sov33-evolved (11.4). The flaw is **merge-not-train**, not size.
3. **The crowd is verifiable** — the whole result is one Ed25519 signature anyone can check.

## 4. PER-CHANNEL POSTS (ready)
- **X/LinkedIn (short):** "Every AI lab's scores are self-reported and unsigned. We measured the
  frontier on a clean protocol — retrieved knowledge beats trained by +34–38pts, and base models beat
  our own fine-tunes. Every result is Ed25519-verifiable without trusting us. Measurement, not
  certification. → /verify"
- **HN (technical):** "We built a stranger-verifiable eval body. Showed retrieved>>trained (+34–38) and
  base>fine-tune on governance axes. All results Ed25519-signed, key on signing node, verify in-browser
  (WebCrypto). Tooling on GitHub."
- **r/MachineLearning + r/artificial:** the findings + the verification link.

## 5. DEPLOY STEPS (Claude/GHA — the firing key)
Push `SOVOS/evidence/verify.html` + `signed/*.json` + `verify_signature.py` + this kit to the site
repo → `wrangler pages deploy` (councilof.ai) → live `/verify`. Publish the pubkey `bWbk52E47J6EkY4+pu0Hh/B1l1175AZoZsDEBr0EfWA=` in the page.

## 6. ARXIV ABSTRACT (measurement methodology)
> **Verifiable Governance Measurement: clean sequential evaluation shows retrieved knowledge beats
> trained knowledge, and base models outrank their own fine-tunes**
> We present a measurement methodology for AI governance that fixes two confounds degrading
> leaderboard trust: (1) grader/refusal sensitivity — the keyword grader under-credits refusal and
> persona-narrow answering; (2) contention — shared-GPU batch eviction inflates spurious failures. On
> a sequential, evict-first protocol we measure RAG-context lift of +34–38 points across four base
> models, and show that at fixed size a base model (qwen2.5-0.5b, 32.6) outperforms its own sovereign
> fine-tunes (sov33-v7 19.8, sov33-evolved 11.4) — evidence that weight-merging weak specialists
> dilutes rather than improves the base. Every result is Ed25519-signed on a signing node (key never
> leaves), making the evaluation independently verifiable without trust in the publisher. Measurement,
> not certification.

## 7. TIMELY REGULATORY HOOKS (cite us)
- Art 50 live (Aug 2) · Illinois SB 315 (audits Jan 2028) · EN 18286 uncited · Vietnam Decree 142.
- Position: a buyer-side, COI-screened, signed-artifact measurement body is what these mandates require.
