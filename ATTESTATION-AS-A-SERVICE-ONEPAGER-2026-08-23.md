# ATTESTATION-AS-A-SERVICE — REVENUE ONE-PAGER (2026-08-23)

**Product:** "Verified measurement credential" — signed, independently verifiable AI-governance
measurement evidence. The buy-side (insurers / regulators / deployers) purchases **attestation**, not a
certification stamp. Measurement, not certification.

## Why now (the buy-side window)
| Hook | Date | What the buyer needs |
|---|---|---|
| Illinois SB 315 | audits from **2028-01-01** | annual independent third-party frontier audit — a COI-screened, signed-artifact body is the statute's shape |
| EU AI Act Art 50 | **live 2 Aug 2026** | signed evidence of disclosure/marking (binary, machine-checkable) |
| EN 18286 / Art 17 | uncited (OJEU pending) | conformity-preparation evidence-scoring |
| Vietnam Decree 142 | Mar/Sep 2027 | mandatory 3rd-party certification evidence (banking/health) |

The buy-side has **no signed, independent, re-measurable evidence object** today. That's the gap.

## What we sell (the attestation)
1. **Signed receipt** — Ed25519 on a signing node (key never leaves; `did:web:csoai.org` trust root).
   Canonical body → `signature{sig, body_sha256, pubkey}` → anyone verifies offline.
2. **Live verify URL** — `https://csoai-verify.pages.dev/verify` (browser WebCrypto, zero trust).
3. **Methodology** — clean sequential measurement (refusal-tolerant, evict-first); the base-beats-finetune
   + RAG findings as measured evidence.
4. **Independence** — buyer/insurer/regulator-pays ONLY; never the scored; no issuer-pays (Moody's trap).

## The proof (already live + signed)
- 15 Ed25519-signed artifacts + `evidence-index.json` (pubkey `bWbk52E47J6EkY4+pu0H…`).
- Clean measurement: mistral 67.3 / llama3 66.6 / qwen2.5:7b 63.3 / 1.5b 60.5 (RAG, confound-free).
- Base > our fine-tunes at same size (merge-not-train is the flaw).

## Revenue model (the play's bands; buyer-side only)
| Service | Band |
|---|---|
| Document review / evidence scoring | €8–20k |
| Conformity-preparation scoring | €25–80k |
| Surveillance / re-check | €5–15k / yr |
| Per-receipt attestation / API | entry-priced |

## Buyers (first wave)
1. **Insurers** — Mosaic × Munich Re (Art 50 receipt pilot, `INSURER_PILOT_v2`); underwriting-measurement
   (Eticas×Armilla precedent: up to 20% premium reduction).
2. **Regulators** — SB 315 audit-pack, Art 50 evidence, EU Art 85 complaints, AI Office CoP.
3. **Deployers with live Art 50(1) chatbot-disclosure exposure** — fixed-fee 5-day engagement.

## Doctrine (binds)
- **Measurement, not certification.** Never a conformity certificate (Art 28 void). Stay evidence/scoring side of Art 43.
- **Never the scored.** No lab sponsors, no private best-of-N, no paid placement. Grants never >50% revenue.
- **Buyer-side.** Issuer-pays is the Moody's trap.

## Status
Signed + verifiable (see evidence estate). Step-1 GTM asset for the SB 315 / Art 50 buy-side.
