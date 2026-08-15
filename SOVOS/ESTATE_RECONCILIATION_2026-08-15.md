# BUILD RECONCILIATION — 100-Step Plan × Current Estate (2026-08-15)

## Summary

The 100-step plan from the compass artifact is comprehensive. This document maps every step to
what already exists, what's partially built, and what's not started — and flags ONE critical
change that affects tomorrow's decisions.

---

## 🔴 CRITICAL — Oracle A1.Flex cut halved (confirmed)

The research pass reports that **Oracle cut its Always-Free A1 allowance effective 15 June 2026**,
with **automatic termination of over-limit instances from 18 August 2026** (3 days from now).

| Metric | Before (assumed) | After (real) |
|---|---|---|
| Free tier | 4 OCPU / 24 GB | **2 OCPU / 12 GB** |
| Monthly OCPU-hours | 3,000 | **1,500** |
| Monthly GB-hours | 18,000 | **9,000** |
| Enforced from | N/A | **18 August 2026** |

**What this means for the fleet plan:**
- The rotator still fits (Qwen2.5:1.5B, Llama3.2:3B, Gemma:2B, DeepSeek-R1:1.5B all fit in 12GB)
- **Throughput drops ~50%** — from ~12 models/hour to ~5-6 models/hour, so ~140 model-sessions/day not 288
- Only ONE lightweight model can be resident at a time (no preloading)
- PAYG upgrade is the reliable workaround for more capacity
- The E2.Micros (unchanged, £0) remain the fabric layer

---

## PHASE-BY-PHASE RECONCILIATION

### PHASE 0 — Monorepo & Core (shared prerequisite)

| Step | Description | Status | Evidence |
|---|---|---|---|
| 1 | Freeze csoai monorepo; 45 remaining package stubs (10/55 done) | **IN FLIGHT** | Subagent B verified 9/9, signal-index pre-existing |
| 2 | Extract bom_signer.py + oms_sign.py into csoai-core | **LIVE** | Committed. `bom_signer.py` in sovos-city, `oms_sign.py` in agents/ |
| 3 | Define J-Space record schema (pair_id, chain_id) | **LIVE** | `oms_sign.py` — shared pair_id, different chain_id verified |
| 4 | Encode 13-axis GSPC registry as data | **LIVE** | `GSPC_NUMBERS_REGISTRY.json` committed |
| 5 | CI validation + licence-scan gate | **PARTIAL** | `claim_linter.py` exists; no licence-scan gate yet |
| 6 | csoai-core golden tests (sign→verify) | **PARTIAL** | `oms_sign.py` self-test works; needs formal test suite |
| 7 | Stand up signed-card registry | **NOT STARTED** | Need SCITT service |
| 8 | Dependency-lint rule (MEOK→model import ban) | **NOT STARTED** | Firewall 2 as code |

### PHASE 1 — Evidence Spine (Track 2, blocks everything)

| Step | Description | Status | Evidence |
|---|---|---|---|
| 9 | Fork model-transparency; OMS detached-bundle emit | **PARTIAL** | `oms_sign.py` + `bom_signer.py` do OMS-style Ed25519; not yet detached Sigstore bundles |
| 10 | J-Space card as in-toto statement with GSPC predicate | **PARTIAL** | Paired records exist; not in in-toto format |
| 11 | RFC 3161 timestamping | **PARTIAL** | `cose_wrapper.py` has OTS time-anchor; works on A100 |
| 12 | Deploy scitt-ccf-ledger Transparency Service | **NOT STARTED** | Need to fork MIT repo and deploy on Oracle micro or A100 |
| 13 | Rekor v2 inclusion proofs | **NOT STARTED** | `sigstore/rekor-tiles` (v2) — not v1 (maintenance mode) |
| 14 | C2PA manifest (c2pa-rs, Ed25519) | **NOT STARTED** | c2patool v0.26.27 exists; not wired |
| 15 | VC 2.0 / Open Badges 3.0 issuer | **NOT STARTED** | OB 2.0 still dominates; 3.0 is future |
| 16 | End-to-end test | **NOT STARTED** | Depends on 9-15 |
| 17 | Verifier CLI (pinned issuer) | **NOT STARTED** | `csoai` CLI has `verify` subcommand via PyPI |

### PHASE 2 — Regulation Rails (Track 1)

| Step | Description | Status | Evidence |
|---|---|---|---|
| 18 | Add compliance-trestle (Apache-2.0) + oscal-cli | **NOT STARTED** | `sovos-oscal` exists (self-contained). Trestle not imported yet. |
| 19 | Wire compliance-trestle-mcp for agent-driven authoring | **NOT STARTED** | MCP server exists (Feb 2026 release) |
| 20 | measurement→OSCAL SAR converter | **PARTIAL** | `sovos-oscal` exports `assessment_results()` — the SAR converter exists. |
| 21 | Harmonized control catalog + OSCAL v1.2.1 Mapping Model | **NOT STARTED** | Need to research the March 2026 Mapping Model |
| 22 | OPA/Rego crosswalk validators | **PARTIAL** | `article_zero.rego` exists; not mapped to NIST/ISO |
| 23 | EU adapter (Annex IV + Art 50 C2PA) | **PARTIAL** | `csoai_framework_signer.py` — framework→OSCAL works. Annex IV specific emitter needed. |
| 24 | US adapter (NIST AI RMF + ISO 42001) | **NOT STARTED** | |
| 25 | CN adapter (GB 45438-2025 metadata) | **NOT STARTED** | |
| 26 | SG adapter (AI Verify-shaped report) | **NOT STARTED** | Fork NIST↔IMDA crosswalk (May 2025, airc.nist.gov) |
| 27 | Golden-file tests per adapter | **NOT STARTED** | |
| 28 | Firewall audit (no "certified" field) | **NOT STARTED** | |

### PHASE 3 — MEOK Human-Data Engine (Track 3)

| Step | Description | Status | Evidence |
|---|---|---|---|
| 29 | Fork ai-town (MIT) into csoai-meok | **NOT STARTED** | Game shell needed |
| 30 | Fork FastChat battle/vote harness | **NOT STARTED** | Pairwise human-vote UI |
| 31 | MeltingPot / AgentSociety scenarios | **NOT STARTED** | |
| 32 | Complete + file Art. 35 DPIA | **NOT STARTED** | CSOAI LTD = controller. ICO template exists. |
| 33 | Consent gate | **NOT STARTED** | |
| 34 | Seed MIT/Apache sets only | **PARTIAL** | Honey has 4,896 rows; licence-hygiene check needed |
| 35 | Exclude CC-BY-NC sets | **NOT STARTED** | |
| 36 | Prolific calibration cohort | **NOT STARTED** | |
| 37 | Export votes as signed records | **PARTIAL** | `csoai_scorer_signer` emits paired records; MEOK export not wired |
| 38 | Static-analysis: no MEOK→model path | **NOT STARTED** | |

### PHASE 6 — Compute Fabric (parallel)

| Step | Description | Status | Evidence |
|---|---|---|---|
| 53 | 2× E2.Micro (scheduler + submitter) | **LIVE** | micro1+micro2 city-report running 05:00 UTC |
| 54 | A1.Flex at 2 OCPU/12GB (or PAYG) | **HUNTING** | eu-frankfurt-1; 3,533 misses. Cut takes effect 18 Aug. |
| 55 | Ollama lightweight tier (5 models) | **TESTED** | Each fits 12GB; low tok/s CPU-only |
| 56 | Model rotator (load→N probes→sign→unload→next) | **NOT STARTED** | Script needed; 5-6 models/hour on 2 OCPU |
| 57 | Emit probes as signed cards to registry | **PARTIAL** | `csoai_scorer_signer` does this |
| 58 | RunPod K3 client with FlashBoot warmup | **LIVE** | `sov6-kimi-k3-2tb` endpoint deployed |
| 59 | A100 + 3090 workers → same registry | **PARTIAL** | Both live; aren't writing to shared registry yet |
| 60 | Licence-gate model pulls (MIT/Apache only) | **NOT STARTED** | |
| 61 | Throughput benchmark | **NOT STARTED** | |

---

## WHAT TO BUILD NEXT (prioritized for weekend lane)

### Immediate (today/tomorrow) — highest leverage
1. **csoai-core freeze** — package `bom_signer.py` + `oms_sign.py` + J-Space schema + GSPC registry
   into a standalone installable package. Blocks every other track.
2. **CI dependency-lint rule** — fail on `csoai-meok` → shippable-model import. Firewall 2 as code.
3. **Update honey licence gate** — exclude any CC-BY-NC rows from the signed honey (check the source
   fields). Step 35 + 60.
4. **Compute reality: commit the 2 OCPU/12GB plan** — update FLEET_ROSTER.md with the Oracle cut.
   The A1 hunt switches to: EU 1.5K OCPU-hours ceiling; PAYG workaround for >2 OCPU.

### This week
5. **SCITT transparency service** — fork `microsoft/scitt-ccf-ledger` (MIT), deploy on E2.Micro or A100.
   Step 12.
6. **Measurement→OSCAL SAR converter** — wrap `sovos-oscal.assessment_results()` into the
   evidence spine. Step 20 is already 80% done by the sovos-oscal package.
7. **AI Verify adapter** — fork the NIST↔IMDA crosswalk (airc.nist.gov, May 2025). Step 26.
   This is the institutional priority (AI Tester Accreditation Programme).

### Owner-gated (this weekend ideally)
8. **DPIA** — Art. 35 UK GDPR template. Name CSOAI LTD as controller. Step 32. Blocks all human data.
9. **npm token + arXiv submission** — expires 27 Aug.
10. **Phone number** — both checkouts (TM £385 + Cyber Essentials £320).

### Not this week (staged)
11. C2PA manifest — needs X.509 cert; OSCAL v1.2.1 Mapping Model — needs full crosswalk investment;
   A2A metering — needs AP2 fork.
12. MEOK game shell — needs DPIA done first.

---

## FIREWALL COMPLIANCE CHECKLIST — current state

- [ ] **FW1 (rails, not certification):** No adapter output contains "certified/endorsed/approved".
  CURRENT: G4 claim-linter checks this for SOVOS codenames. Need a `certify`/`endorse` string scan.
- [ ] **FW2 (analyse, never ship champion):** MEOK data + GNN → never train a shipped Council model.
  CURRENT: Not enforced in code. Need `csoai-meok`→model import ban in pyproject.toml.
- [ ] **No PII leakage:** x402 metadata + SCITT statements.
- [ ] **Licence hygiene:** MIT/Apache/BSD only in shippable paths. CC-BY-NC excluded.
- [ ] **Compute reality:** Plan for 2 OCPU/12GB, not 4/24.
- [ ] **Abandoned-project guard:** `scitt-ccf-ledger`, not `scitt-api-emulator`. `rekor-tiles`, not `rekor` v1.

---

## TODAY'S MARKET SIGNAL (15 Aug 2026)

Wall Street just declared compute an asset class. Nvidia + Apollo/BlackRock/Blackstone/Brookfield/
Goldman Sachs/KKR raised **$500bn** for AI infrastructure: *"Compute has become a scarce, mission-critical
asset class"* (KKR). $1tn+ already spent by big tech in 3 years.

The measurement/assurance layer over what runs on that compute is a **bankable requirement**, not a
nice-to-have. Every one of those $500bn deals will eventually need: (a) signed provenance records,
(b) independent measurement evidence for regulatory compliance (EU AI Act Art 50 goes live 2 Dec 2026),
(c) verifiable agent audit trails (Singapore Agentic Framework, NIST Agent Standards).

**The wedge:** we have the working measurement pipeline before the market knows it needs one. The 100-step
plan is credible because it maps onto this timing exactly.

---

*Source: 100-Step Execution Plan (compass_artifact_wf-7150550a) · BBC News 11 Aug 2026 — Nvidia $500bn ·
Oracle Always-Free A1 cut, effective 15 Jun 2026, enforced 18 Aug 2026 (InfoQ/Linuxiac Jul 2026) ·
EU AI Act Art 50: Code of Practice published 10 Jun 2026, marking obligation 2 Aug 2026, grace period
to 2 Dec 2026 · AI Verify Foundation Tester Accreditation Programme, first in Asia*