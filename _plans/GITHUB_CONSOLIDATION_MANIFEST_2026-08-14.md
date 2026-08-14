# GitHub Consolidation Manifest — CSOAI-ORG

**Date:** 2026-08-14
**Scope:** `gh repo list CSOAI-ORG` (300 repos) + `CSGA-GLOBAL` (2 repos, both already archived). No other `meok*` org exists (the authenticated account belongs to `CSGA-GLOBAL` only; MEOK lives as a naming prefix *inside* CSOAI-ORG, not a separate org).
**Nature:** AUDIT + PLAN. Nothing here has been deleted, archived, or edited. This is a manifest the owner acts on.

---

## Summary

**302 repos total** (300 in CSOAI-ORG + 2 in CSGA-GLOBAL).

| Bucket | Count | What it is |
|---|---:|---|
| **SPINE** | 11 | The ONE neutral measurement/sign/verify/drift core + its measurement packages |
| **SITE / DEPLOY** | 18 | Front-end, org sites, distribution surfaces, per-domain hive configs |
| **CONSUMER** | 246 | Verticals that *consume* the spine but must stay SEPARATE (bridges, generic MEOK utility/compliance MCPs, A2A substrate, client sites) |
| **ARCHIVE-CANDIDATE** | 27 | Stale / empty / third-party forks / superseded / near-duplicate |

> Some repos legitimately sit at a bucket boundary (e.g. `csoai-static-deploy2` is the spine's own publish surface). Each such call is noted inline. Counts assign every repo to exactly one bucket; archive-candidates are drawn out of whichever functional bucket they came from and listed once, in ARCHIVE.

**The headline finding is not the count — it is the firewall.** 32 repos publish a self-awarded grade (`100/100 A+++++ · world-leading`), and at least one MCP (`ai-self-audit-mcp`) ships an "EU AI Act — Compliant" badge and a `get_certificate` tool that emits "signed certificates" of compliance. That is certification language on a body whose entire legitimacy depends on being *measurement, not certification*. Fix the firewall before touching the sprawl.

---

## SPINE — the one measurement core + its measurement packages

These are neutral: they measure, sign, freeze, and preserve evidence. They contain **no client, no fix, no payment path**. Nothing with a billing or remediation attachment may be folded in here.

| Repo | Last push | Why SPINE |
|---|---|---|
| `sovos-core` | 2026-08-10 | SOVOS measurement OS — GSPC four-axis scoring over ETSI EN 304 223, local-first. The engine. |
| `csoai-dashboard` | 2026-08-13 | Published measurement surface — "frozen harnesses, signed results, recompute-able evidence." |
| `corpus-watch` | 2026-08-14 | Regulatory **drift** detection — daily hash watcher over EU AI Act (CELLAR)/UK statute; fail-closed (UNKNOWN never reported as unchanged). |
| `gspc-harness` | 2026-08-05 | GSPC governance evals as runnable Inspect harnesses — the frozen benchmark harness. |
| `govbench` | 2026-08-05 | GovBench measurement harness (the canonical "measure with GovBench" tool). |
| `csoai-governance-crosswalk-mcp` | 2026-06-27 | The named 13-framework × 52-article crosswalk (NIST AI RMF ↔ ISO 42001 ↔ EU AI Act ↔ …). |
| `ai-bom-mcp` | 2026-06-26 | AI Bill of Materials (CycloneDX/SPDX), EU AI Act Art.11 — evidence artifact generator. |
| `agent-prompt-injection-firewall-mcp` | 2026-08-08 | Injection scanner — the "injection-scanner" measurement package. |
| `model-scoreboard-mcp` | 2026-06-26 | Model leaderboard + evidence-based routing (measurement, not routing-for-sale). |
| `sovereign-oowm` | 2026-08-09 | OOWM substrate feeding the measurement core. |
| `csoai-static-deploy2` | 2026-08-14 | *Boundary:* the spine's own static publish surface (500+ gov pages). Lives with the spine but is the deploy artifact of it — see SITE note. |

**Firewall note inside the spine:** `csoai-governance-crosswalk-mcp` is the master crosswalk; `dora-nis2-crosswalk-mcp` and `nist-iso42001-crosswalk-mcp` are subsets of it (see Duplicates). `ai-self-audit-mcp` looks spine-shaped ("self-measuring") but currently emits certificates — it is quarantined in CONSUMER + flagged as a breach until de-certified.

---

## SITE / DEPLOY

Front-ends, org sites, distribution/CDN surfaces, and the per-domain hive config repos.

| Repo | Last push | Why this bucket |
|---|---|---|
| `councilof-ai` | 2026-08-14 | **Canonical public site** (councilof.ai) — the firewall-honest one ("independent measurement instrument… not a notified body"). |
| `csoai-static-deploy2` | 2026-08-14 | Static deploy substrate (also the spine's publish surface). |
| `csoai-org` | 2026-08-12 | Org website — description still advertises "CEASAI certification" (see FIREWALL). |
| `csoai-org-v2` | 2026-06-29 | Superseded site — "certificate authority" framing (see FIREWALL + Duplicates). |
| `csoai-global` | 2026-06-27 | **Already archived** — empty legacy site. |
| `csoai-mcp-dist` | 2026-08-09 | MCP distribution (jsDelivr/unpkg-mirrored) — deploy infra. |
| `mcp-servers` | 2026-08-08 | "MEOK MCP Marketplace" HTML — deploy/catalogue surface. |
| `meok-governance-smithery` | 2026-08-08 | Smithery distribution surface. |
| `meok-compliance-gateway` | 2026-08-08 | Streamable-HTTP/container build surface for MEOK MCPs. |
| `haulage-deploy` | 2026-08-05 | Consumer-brand SaaS front-end (haulage.app) — deploy of a CONSUMER vertical, kept off the spine. |
| `meok-attestation-api` | 2026-08-05 | Attestation API surface (haulage.app). |
| `asisecurity-hive` | 2026-08-08 | Per-domain GENE/A2A/MCP wiring config. |
| `optimobile-hive` | 2026-07-17 | Per-domain hive config. |
| `meok-compliance-gateway-hive` | 2026-06-19 | Per-domain hive config. |
| `socialmediamananger-hive` | 2026-06-19 | Per-domain hive config (note misspelling in the domain). |
| `commercialvehicle-hive` | 2026-06-19 | Per-domain hive config. |
| `cobolbridge-hive` | 2026-06-19 | Per-domain hive config for the CobolBridge vertical. |
| `openpatent-hive` | 2026-06-21 | Per-domain hive config (empty desc — archive candidate). |

---

## CONSUMER — verticals that consume the spine, kept SEPARATE

**246 repos.** These are the sprawl, but the firewall rule is absolute: **none may be folded into the SPINE.** They carry client relationships, remediation ("get compliant"), payment (Stripe/x402), or domain-vertical logic — folding any of them into the neutral core poisons its neutrality. Listed by family (full enumeration would be 246 rows; the families are what the owner collapses).

| Family | Count | Examples | Why CONSUMER |
|---|---:|---|---|
| Protocol bridges (`*-bridge-mcp`) | 22 | `cobol-bridge-mcp`, `sap-bridge-mcp`, `iso20022-bridge-mcp`, `fix-bridge-mcp`, `hl7-fhir-bridge-mcp` | CobolBridge & family — verticals that translate an enterprise protocol *into* governance. Consume the spine; never part of it. |
| Generic MEOK utility MCPs (`*-ai-mcp`) | ~105 | `churn-predictor-ai-mcp`, `resume-parser-ai-mcp`, `crypto-tracker-ai-mcp`, `weather-ai-mcp`, `recipe-finder-ai-mcp`, `pet-care-ai-mcp`, `fishkeeper-ai-mcp` | Off-the-shelf SaaS-utility MCPs. Zero governance-spine content. Pure consumer catalogue. |
| Compliance-regime MCPs | ~55 | `gdpr-compliance-ai-mcp`, `hipaa-compliance-mcp`, `dora-compliance-mcp`, `nis2-compliance-mcp`, `pci-dss-mcp`, `soc2-compliance-ai-mcp`, `fda-samd-mcp` | Per-regime tools. Many carry the `100/100 A+++++` puffery and/or Stripe billing → monetized consumer, not neutral measurement. |
| A2A substrate (`agent-*-mcp`) | 19 | `agent-orchestrator-mcp`, `agent-audit-logger-mcp`, `agent-x402-paywall-mcp`, `agent-handoff-certified-mcp` | Agent-to-agent plumbing + paywalls. Consumer infra. |
| Payment / commerce MCPs | ~10 | `meok-x402-wrap-mcp`, `stripe-billing-mcp`, `meok-stripe-acp-checkout-mcp`, `meok-coinbase-x402-receipt-mcp`, `meok-governance-engine-mcp` (Stripe) | Money paths — must stay out of the neutral core by definition. |
| Watermark / C2PA MCPs | 6 | `c2pa-watermark-mcp`, `watermarking-authenticity-mcp`, `meok-c2pa-durable-mcp` | Art.50 watermarking tools (heavy internal overlap — see Duplicates). |
| Domain verticals / demos | ~15 | `defoneos`, `defoneos-com`, `sov3-beat-demo`, `sov3-arch-demo`, `sov3-live-demo`, `muckaway-ai-mcp`, `planthire-ai-mcp`, `haulage-uk-compliance-mcp` | Defence, waste, plant-hire, haulage verticals. |
| Client / family sites | ~8 | `networknick-mallett-roofing`, `networknick-wcr-grab-hire`, `networknick-dmt-car-transport`, `templeman-opticians-site`, `aksteelservices`, `optimobileai`, `optimobile-practice-hub` | Real client and family-business sites. Absolutely never spine. |
| Curated `awesome-*` lists | 6 | `awesome-eu-ai-act`, `awesome-compliance-csoai`, `awesome-legaltech` | Marketing/SEO lists (see Duplicates). |
| Misc research / private | ~5 | `clawd-workspace` (priv), `meok-one` (priv), `sov-os` (priv), `sov-tv` (priv), `openchronicle-mcp` | Private workspaces & research lanes. |

---

## FIREWALL BREACHES — highest priority for the owner

Language that presents CSOAI/MEOK as a **certifier, accreditor, or self-graded authority** rather than an independent measurement instrument. This is legal/IOSCO exposure (a measurement body must not certify or self-award grades). Fix these before any consolidation.

### Top 5 (act first)

1. **`ai-self-audit-mcp`** — the most dangerous. README ships an **`EU AI Act — Compliant`** badge, describes agents auditing "their own EU AI Act compliance in real time **with signed certificates**", exposes a **`get_certificate`** tool, and markets **"Need help getting compliant?"**. This is compliance-certification-as-a-service under the CSOAI name. De-certify: rename outputs to "measurement record / signed evidence", drop the "Compliant" badge and the `get_certificate` verb.

2. **`csoai-org`** — public description advertises **"CEASAI certification"** and "Byzantine Council". (Its README *has* been corrected — it now reads "Not a certifier… an independent measurement instrument" — but the repo description the world sees still sells certification. Description/README mismatch: fix the description.)

3. **`csoai-org-v2`** — describes itself as a **"certificate authority"**. Positions CSOAI as an accreditation/CA body. Superseded by `councilof-ai` anyway → retire (see Duplicates), and never revive the CA framing.

4. **The `100/100 A+++++ · world-leading` fleet (32 repos)** — a **self-awarded grade** published as fact across the estate (e.g. `cobol-bridge-mcp`, `eu-ai-act-compliance-mcp`, `csoai-governance-crosswalk-mcp`, every `*-bridge-mcp`, `mica-crypto-mcp`, `ll144-bias-audit-mcp`, `sbom-cyclonedx-mcp`). "100/100 A+++++", "bleeding edge", "world-leading" are an index/score the org grants itself. Strip all 32 to neutral, falsifiable descriptions. This is one search-and-replace but it touches a third of the estate.

5. **`agent-handoff-certified-mcp`** — the repo **name** carries "certified" and markets "certified" A2A handoffs. Rename to `agent-handoff-signed-mcp` (it is signed provenance, not certification).

### Secondary (measurement-framed but watch the wording)

- `csoai-dashboard` — "the measurement body for AI compliance." "Measurement body" is defensible; "**the** … body" edges toward accreditation-authority. Prefer "an independent measurement harness."
- `gspc-harness`, `sov5v2` — use "**benchmark(s)**". Framed as evals (lower risk), but "benchmark" is an IOSCO-loaded term; prefer "governance evals / measurement harness".
- `iso-42001-ai-mcp` — description promises AIMS "**certification**"; reframe as "certification-*readiness* assessment".
- `watermarking-authenticity-mcp` / `agent-content-watermark-mcp` — "authenticity"/"certified content" framing; keep to "provenance signal", not proof of authenticity.

---

## Collapse these duplicates

Concrete near-duplicate groups the owner should merge/retire. **Keep-one** is named in each.

1. **CSOAI org sites (5 → 1 + 1 deploy).** `csoai-org`, `csoai-org-v2`, `csoai-global` (already archived), `councilof-ai`, `csoai-static-deploy2`.
   **Keep:** `councilof-ai` (canonical, firewall-honest) as the site; `csoai-static-deploy2` as its static build. **Retire:** `csoai-org`, `csoai-org-v2`, `csoai-global`.

2. **Watermark / C2PA MCPs (6 → 1–2).** `c2pa-watermark-mcp`, `meok-c2pa-durable-mcp`, `watermarking-authenticity-mcp`, `meok-watermark-attest-mcp`, `agent-content-watermark-mcp`, `meok-eu-aigc-icon-mcp` — all Art.50 watermarking/provenance.
   **Keep:** `meok-c2pa-durable-mcp` (most current C2PA 2.2). Fold the rest in; keep `meok-eu-aigc-icon-mcp` only if the EU AIGC icon emitter is genuinely distinct.

3. **RAG / knowledge / vector MCPs (3 → 1).** `rag-knowledge-graph-mcp`, `rag-knowledge-mcp`, `vector-knowledge-graph-mcp` — same hybrid-retrieval capability three times.
   **Keep:** `rag-knowledge-graph-mcp`. Retire the other two.

### Also collapse (secondary)

4. **`awesome-*` lists (6 → 3).** Two are literal EU AI Act twins: `awesome-eu-ai-act` + `awesome-eu-ai-act-genaigurus` → keep `awesome-eu-ai-act`. Keep `awesome-legaltech` and `awesome-foundation-model-leaderboards` if distinct; fold `awesome-compliance-csoai` / `awesome-mcp-servers-csoai` into the survivors.
5. **UK AI Act MCPs (2 → 1).** `uk-ai-act-mcp` + `uk-ai-bill-compliance-mcp` are the same UK AI Bill tool → keep one.
6. **AML MCP + misnamed twin (2 → 1).** `aml-ai-mcp` and `yaml-ai-mcp` **share the identical 6AMLD/UK-MLR/FinCEN description** — `yaml-ai-mcp` is a mislabeled AML duplicate (its name implies a YAML tool). Retire/rename `yaml-ai-mcp`.
7. **Crosswalk subsets (3 → fold into spine master).** `dora-nis2-crosswalk-mcp` and `nist-iso42001-crosswalk-mcp` are slices of `csoai-governance-crosswalk-mcp` — fold into the master crosswalk package.
8. **SOV3 demo sites (3 → 1).** `sov3-beat-demo`, `sov3-arch-demo`, `sov3-live-demo` — three DEFONEOS demo pages → keep one showcase.

---

## ARCHIVE-CANDIDATE

Flagged only — do not archive from this task.

**Already archived (3):** `geolocation-ai-mcp`, `consciousness-engine-mcp`, `csoai-global`.

**Third-party forks (5):** `OpenHands`, `langfuse`, `inspect_evals`, `labs-OO-Agents` (NVIDIA OO-Agents), `agent-zero` — upstream projects, no CSOAI value-add visible; archive or delete.

**Empty description + stale >30d (superseded/abandoned):** `meok-saas`, `meok-town-view`, `meok-sovereign-stack`, `sovereign-flywheel-proof`, `sigil-proofs`, `supply-chain-mcp`, `openpatent-hive`, `sovereign-temple`, `flywheel-nsite` (empty desc), `csoai-governance` (empty desc), `proofof-ai-mcp` (empty), `care-membrane-mcp` (empty), `regulatory-webhook-mcp` (empty), `trust-chain-mcp` (empty), `credential-manager-mcp` (empty), `oscal-generator-mcp` (empty).

**Superseded by firewall/dup decisions:** `csoai-org`, `csoai-org-v2` (→ `councilof-ai`), `yaml-ai-mcp` (dup of `aml-ai-mcp`).

**CSGA-GLOBAL (2, both already archived):** `COBOLBRIDGE`, `COBOLBRIDGEAI` — legacy private CobolBridge repos; consolidate the CobolBridge story onto `cobol-bridge-mcp` + `cobolbridge-hive` in CSOAI-ORG.

> Empty-description repos flagged above should be spot-checked before archiving — a couple may hold live wiring despite a blank description. This manifest flags; the owner verifies then acts.

---

## The one spine — statement

**`sovos-core` is the single neutral spine** — the GSPC measurement/sign/verify engine. It measures, signs (Ed25519), freezes to statute, and preserves evidence; it decides nothing and certifies nothing.

**Belongs INSIDE / beside the spine (measurement packages):** `csoai-dashboard` (published surface), `corpus-watch` (drift), `gspc-harness` + `govbench` (harnesses), `csoai-governance-crosswalk-mcp` (the crosswalk — absorbing the DORA×NIS2 and NIST×ISO subsets), `ai-bom-mcp`, `agent-prompt-injection-firewall-mcp`, `model-scoreboard-mcp`, and `csoai-static-deploy2` as its publish artifact.

**Must stay SEPARATE consumers (never folded in):** every `*-bridge-mcp` (CobolBridge & family), every generic `*-ai-mcp`, every per-regime compliance MCP, the `agent-*` A2A substrate, all payment/commerce MCPs (`stripe-*`, `*-x402-*`), the domain verticals (DEFONEOS, haulage, waste, plant-hire), and all client/family sites. These consume the spine's signed measurements; giving any of them a seat *inside* the neutral core would make CSOAI both the measurer and an interested party — the exact conflict the firewall exists to prevent.

**Measurement, not certification.** CSOAI measures, signs, and preserves the evidence; regulators and accredited bodies decide. Every "certified / certificate / Compliant / 100/100 / world-leading" string in the estate contradicts that and is a bug to fix, not a feature to keep.
