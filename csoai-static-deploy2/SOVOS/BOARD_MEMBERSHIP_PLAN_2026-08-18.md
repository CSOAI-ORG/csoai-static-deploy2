# BOARD MEMBERSHIP PLAN — v1 (built 18 Aug 2026 by JEEVES)

**Doctrine (AGENTS.md board doctrine + dossier §5):** authority compounds from being in the
room. Contribute measurement methodology (neutral/technical), gain early signal, convert
co-members into warm intros, ship mapping packs. **Firewall:** never lobby for certification
powers, never pre-brief a vendor client, never take a seat that conflicts with measurement
neutrality.

## Current board assets
| Body | Status | Value |
|---|---|---|
| C2PA Contributor Member (LF) | ✅ signed (docusign 7C9592DB) | Adobe/MS/BBC/Sony/Google = co-members → warm-intro pool |
| BSI ART/1 (UK mirror ISO/IEC SC 42, £0) | ⏳ owner-gated | EU AI Act harmonised standards feed — BSI connection-readiness walkthrough at SOVOS/CONNECTION_READINESS_AUDIT_CAI_BSI_DEEP_2026-08-19.md (NOT yet a submitted application; the previously-cited BSI_ART1_SEAT_2026-08-15.md pack does not exist) |

## Agent-doable applications (4) — this plan

### 1. OpenSSF — model-signing (LF)
- What: join OpenSSF (Linux Foundation) working groups; contribute model-signing methodology.
- Angle: we sign Ed25519/COSE ML-DSA-65 cards — our primitive fits their supply-chain mandate.
- Step: apply for membership + join sigstore/model-signing WG. Application drafted below.

### 2. LF x402 Foundation
- What: the x402 payment-protocol foundation (open payments for AI).
- Angle: we build x402 metered flows (£0.0001/call pricing) — a reference implementer.
- Step: membership application + reference-implementation contribution.

### 3. OWASP AI/MCP
- What: OWASP AI Exchange + MCP security project.
- Angle: our 63-item adversarial corpus + MCP conformance boards are exactly their testing gap.
- Step: join as contributor member; submit care_battery + MCP scoring as a project asset.

### 4. AI Verify Foundation (IMDA)
- What: Singapore's AI Verify testing framework (global).
- Angle: our 13-axis GSPC registry maps 1:1 to AI Verify's testing categories; Singapore alignment
  sourcing from the canonical framework at _evacuation/runpod-bundles/20260822-frameworks-drum/frameworks/singapore-model-ai-governance-framework-for-agentic-ai.md
  (NOTE: the previously-cited council-os/SINGAPORE_AI_VERIFY_PACK.md does not exist — no alignment pack authored yet).
- Step: foundation membership + alignment submission.

## Application drafts (one paragraph each, ready to send)

### OpenSSF membership (draft)
> CSOAI Ltd (UK 16939677) applies to join OpenSSF. We are a neutral AI-governance measurement
> body: we publish signed, recompute-able measurement cards (Ed25519 / COSE ML-DSA-65 / OSCAL)
> for AI model behaviour across 13 GSPC axes. We offer our model-signing methodology and
> adversarial corpus (63 items, deterministic grading) as a contribution to the sigstore and
> model-signing working groups. We ask for nothing in return beyond a seat at the table.

### LF x402 membership (draft)
> CSOAI Ltd applies to join the LF x402 Foundation as a reference implementer. We price
> AI-governance attestation calls at £0.0001 via x402 metered payments and can contribute a
> reference implementation + measurement-fairness use case. Neutrality firewall: we implement
> the protocol, never gate it.

### OWASP AI/MCP (draft)
> CSOAI Ltd offers its deterministic adversarial corpus (63-item care battery, 15-dim GovBench
> grader, 13-axis GSPC registry) to the OWASP AI Exchange and MCP security projects as testing
> assets under OGL-UK-3.0. Contribution of a conformance board over 531 MCP servers, signed
> and recompute-able.

### AI Verify Foundation (draft)
> CSOAI Ltd applies for AI Verify Foundation membership. Our 13-axis GSPC measurement registry
> (13 axes × 19 models, 12 Aug 2026 stamp, signed cards) is directly compatible with AI
> Verify's testing categories. Singapore alignment pack not yet authored (no SINGAPORE_AI_VERIFY_PACK.md on disk). We seek membership to
> align measurement methodology and share signed-card verification tooling.

## Firewall checklist (every application)
- [ ] No certification-power lobbying
- [ ] No vendor-client pre-briefing
- [ ] No seat conflicting with measurement neutrality
- [ ] Language lock: measure, sign, re-attest (never "certification body")

*Filed: JEEVES, 18 Aug 2026. Next: Nick GO on sending; OpenSSF/OWASP may have self-serve forms — verify live before send (external comms = owner gate).*

---

## ANNEX A — C2PA "Inside-Out" Contribution Strategy (aligned 18 Aug 2026)

Source: deep-research pack (C2PA Working-Group Landscape, Aug 2026). Verified against our
actual standing: **we are already a C2PA Contributor Member (docusign 7C9592DB)** — so this
is about converting membership into standing via contributions, NOT joining.

### The honest picture
- C2PA: ~6,000+ members/affiliates, ~839 on TWG list, 11-member Steering Committee
  (Adobe/Amazon/BBC/Google/Meta/MS/OpenAI/Publicis/Sony/TikTok/Truepic). Every technical
  group is Adobe-chaired/co-chaired. Invitations are real participation, NOT credential.
- Spec: 2.3 published Jan 2026 (live-video, text manifests); 2.4 in progress; ISO/DIS 22144
  fast-track (NOT yet published — never claim "C2PA is ISO"). JPEG Trust ISO/IEC 21617-1:2025
  is published and C2PA-based — distinct fact.
- Adoption at ecosystem scale: Pixel (Assurance Level 2), OpenAI SynthID+C2PA (May 2026),
  Google Search/Chrome verify (I/O 2026), TikTok 3B labeled (Jul 2026), EU AI Act Art.50
  live 2 Aug 2026 — major tailwind.

### PRIORITISE 4 task forces (of our 11 listed — 3 unverifiable)
| TF | Verified | Fit | Our existing asset → contribution |
|---|---|---|---|
| **Conformance** | ✅ whitepaper | HIGHEST | GSPC "externally recomputable measurement" IS conformance doctrine. Ship: open-source recomputable validator/test harness + `public-testfiles` vectors + conformance gap reports |
| **Watermarking** | ✅ Digimarc co-chair | HIGH | Our watermarking axis. Ship: soft-binding algorithm PR + adversarial-survivability robustness benchmark methodology |
| **Threats & Harms** | ✅ whitepaper | HIGH | Our adversarial-robustness + safety axes. Ship: threat annex "how provenance/watermarks fail under attack" + measurable rubric |
| **AI/ML** | ✅ whitepaper | HIGH | Our ai-disclosure/human-vs-AI baselines + 15-dim GovBench. Ship: measurable criteria for `ai-disclosure` / `digitalSourceType` (we have c2pa_sign.py + gspc-c2pa-mapping.json) |
| CAWG identity (DIF) | ✅ (moved to DIF Mar 2025) | STRONG ADJACENT | identity/attribution assertions — light tracking |

### DEPRIORITISE (of our 11)
- **ZKP TF — NOT VERIFIED** as chartered (research interest only) → engage as research, never claim a seat.
- **Ledgers TF — NOT VERIFIED** (C2PA core explicitly no-DLT) → deprioritise.
- **Agentic TF — NOT VERIFIED** (agents handled via digitalSourceType/ingredients) → watch; overlaps IETF agentproto.
- Audio/Live Video/UX/Text → confirmed but low/medium fit; polite deprioritise unless a specific asset appears.

### The firewall (critical — JDF Trademark Policy)
- MAY say: "contributor to / participant in the C2PA TWG"; "contributes to the [Conformance/…] task force"; "member of the C2PA TWG"; "contributed [specific PR/issue/tool]".
- MUST NOT say: "C2PA-certified/approved", "partner", "endorsed by C2PA", "official measurement provider", or logo implying sponsorship. No "GSPC is C2PA conformant" unless a product passes the actual Conformance Program (separate, evidence-based).
- Route all investor/marketing copy through the approved-language list.

### 30/60/90 sequence
- **Days 0–30:** sign corporate C2PA CLA via EasyCLA (free, distinct from dues); join Slack + twg@; attend TWG + 4 chosen TF calls read-only; open 2–3 well-scoped issues on github.com/c2pa-org (specifications, conformance-public); publish one honest blog post (approved language only). No press release implying endorsement.
- **Days 31–60:** land ≥1 merged uncontroversial contribution per priority TF (test vectors / algorithm PR / editorial spec fix); circulate a draft white-paper annex (Threats & Harms or AI/ML).
- **Days 61–90:** ship one open-source reference component (our recomputable conformance/measurement tool — c2pa_sign.py + gspc-c2pa-mapping.json are the seed) and offer a TF-call demo; open co-authorship conversation; draft first IETF agentproto internet-draft on signed agent-session measurement.
- **Escalate:** ≥1 merged contribution per TF + one adopted tool by day 90 → co-chair candidacy + dues-paying membership. Stall → narrow 4→2 (Conformance + one). agentproto WG chartered → elevate IETF to co-equal.

### IETF agentproto (genuine second catapult)
- BoF at IETF 126 Vienna (23 Jul 2026); framework work by Rosenberg/Jennings; layered over WIMSE/OAuth + DAWN + MoQ/QUIC. Early enough that a well-scoped draft on **signed, recomputable measurement/attestation of agent sessions** could stake territory. 2–3 yr RFC timeline; rough consensus; Nick's voice only per owner gates.

### Assets already built (ship these)
- `SOVOS/c2pa-catapult/gspc-c2pa-mapping.json` — 16 GSPC axes → C2PA conformance rubrics + spec 2.4 vocabulary
- `SOVOS/c2pa-catapult/asset-rubric-governance-v0.1-spec2.4.yml` — rubric expression pack
- `kimi-regen/c2pa_sign.py` + `c2pa_manifest.py` — Ed25519 C2PA manifest signer (ai-disclosure + org.csoai.provenance assertions)
- `benchmark-results/c2pa_selftest.json` — valid (unsigned) selftest manifest
- `bin/c2pa_synthid_detector.py` — SynthID detection (Google adoption angle)

### Next concrete step (agent-doable, in-bounds)
Verify live: does our C2PA membership grant GitHub org access + twg@ list already? Check
c2pa-org CLA status + EasyCLA signature; prepare the 2–3 well-scoped issues and the
`public-testfiles` vector submission for Conformance TF.
