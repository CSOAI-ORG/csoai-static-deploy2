# PROVENANCE Axis — Competitor & Peer Learning

**CSOAI · GSPC PROVENANCE axis (signed evidence · content authenticity · watermarking · verifiable records)**
**Prepared:** research-only, no accounts, no submissions. **Honesty rule:** every claim below traces to a cited source; where a claim could not be independently confirmed it is flagged, not asserted.

---

## Scope note

The brief named **12** targets ("top 10" + two extras). All 12 are covered here: 10 are the "core" competitors/peers, and 2 (DigiCert, EU AI Act Art. 50) are adjacent anchors — the CA/trust-list authority and the regulatory driver, respectively. The 12 rows are numbered 1–12; **#1–#10 are the headline ten**.

---

## 1. Competitor table (12 rows)

| # | Competitor | Category | What it does (one line) | Software shape | ONE thing CSOAI could adopt |
|---|---|---|---|---|---|
| 1 | **C2PA / Content Credentials** | Open media-provenance standard | Open spec that cryptographically binds a manifest (who/what/when/edits) to media; Content Credentials is the consumer + SDK layer | Spec 2.x + `c2pa-rs` (Rust) / c2pa-js / Python / C++; CAWG trust list; "Verify" site | A **provenance-timeline renderer**: turn a raw h3k card into a human-readable who→what→when chain, with a **trust-list** of recognized signers |
| 2 | **Truepic** | Secure camera / capture-time authenticity | Camera SDK that signs photos/video at the moment of capture (C2PA-compliant), tamper-evident | Lens SDK (mobile), Vision (enterprise); C2PA co-founder/member | **Sign at source, not retroactively** — bind the receipt at the measurement instant |
| 3 | **Sigstore** | Software-supply-chain signing | Keyless signing via OIDC identity → short-lived cert → transparency log (Rekor) | `cosign` / `fulcio` / `rekor`; Linux Foundation, OSS | **Keyless identity + transparency-log inclusion** for low-friction signing UX |
| 4 | **SCITT (IETF)** | Standards for supply-chain transparency | IETF arch for a Transparency Service: signed *Statements* registered in an append-only Merkle ledger, receipts prove inclusion | `draft-ietf-scitt-architecture` (v19+); COSE/Merkle (RFC 9162) | Align our **receipt schema toward SCITT Signed Statements** for standards interop |
| 5 | **OpenTimestamps** | Trustless timestamping | Proves content *existed before time T* by anchoring a Merkle root into Bitcoin — no trusted third party | `opentimestamps-client` (Python); calendar servers + Bitcoin anchor | **Bitcoin time-anchor** on cards → "existed before T" without trusting us |
| 6 | **vaara (vaaraio/vaara)** | AI-governance evidence layer | Gates every AI tool call against policy, writes a hash-chained, Ed25519-signed record an auditor verifies offline | Python CLI + MCP proxy; AGPL-3.0; IETF `draft-sirkkavaara-vaara-receipt`; SLSA L3 | The **"Resin" single-file offline verifier** + the six-lens `verify-bundle` + explicit "what a pass does NOT establish" |
| 7 | **PipeLab (Pipelock)** | Independent mediator receipts | A **mediator outside the agent trust boundary** signs Ed25519 receipts for each adjudicated HTTP/MCP/WS action | Pipelock proxy; verifiers in Go/TS/Rust/Python; public conformance corpus; exit codes 0/1/2/64 | **Self vs independent attestation** labeling + a public conformance corpus + exit-code CLI verifier |
| 8 | **signet-auth (Prismer-AI)** | Agent tool-call receipts | Signs every MCP `tools/call` (Ed25519 + hash chain), co-signs responses, delegation chains, policy attestation | Rust core, Python, 6 npm pkgs incl. `@signet-auth/mcp`; Apache-2.0/MIT; live browser demo | **MCP-native signing** (drop-in `signet proxy`) + bilateral co-signing + delegation chains |
| 9 | **OpenAI provenance** | Model-output provenance | Embeds C2PA Content Credentials in DALL·E / gpt-image-1 outputs + a detection classifier (~98% on DALL·E 3) | C2PA manifest in API images; classifier; Azure Content Credentials | **Provenance at generation time** + a "is this CSOAI-generated?" detector |
| 10 | **SynthID (Google DeepMind)** | Statistical watermarking | Imperceptible watermark + detector across text / image / audio / video; survives metadata stripping | DeepMind model + SynthID Detector; text watermarking in Responsible GenAI Toolkit | **Watermark as lossy-but-robust fallback** when crypto metadata is stripped |
| 11 | **DigiCert** | CA / document signing | Document Signing certs + Document Trust Manager; Adobe Approved Trust List (AATL) + eIDAS trust lists | Document Trust Manager (DigiCert ONE); AATL/eIDAS membership | Publish a **CSOAI trust list** (approved signer keys) + **revocation check** on every verify |
| 12 | **EU AI Act Art. 50** | Regulation (marking) | Obliges providers to mark AI-generated synthetic content machine-readably; GPAI Code of Practice on transparency | Art. 50(1)(2)(4) + final transparency Code of Practice | Position receipts as **Art. 50 compliance evidence**; map each check to the clause |

---

## 2. Per-competitor detail (what · flow · docs · software · adopt)

### 1. C2PA / Content Credentials

- **What:** Open technical standard (Coalition for Content Provenance and Authenticity, governed under the Linux Foundation / Joint Development Foundation) that cryptographically binds a **manifest** — who created content, with what tool, when, and what edits — directly to media assets (image/video/audio/doc). "Content Credentials" is the consumer-facing brand + the open-source SDK/tooling (Adobe, Microsoft, Google, BBC, Sony are co-members). CSOAI is a C2PA Contributor Member (per workspace records).
- **User flow:** Creator signs in to an app (e.g. Photoshop, or camera firmware) → content is captured/edited with a manifest attached and signed → published with credentials → a viewer (Content Credentials "Verify" site, or a browser/OS surface) inspects the manifest and renders the provenance chain; the viewer checks the signature against a **trust list** (CAWG identity/trust anchors).
- **Docs/onboarding:** c2pa.org spec + `c2pa-rs` README, opensource.contentauthenticity.org (Rust SDK + CAWG identity docs), developer guides ("C2PA for Developers").
- **Software shape:** Rust library `c2pa-rs`, c2pa-js, Python, C++; reference `c2patool` CLI; Verify/Inspect web UIs; trust list distribution via CAWG.
- **Adopt:** the **manifest-as-timeline** renderer and the **trust-list** concept — our AG UI Provenance window should render a 3KB h3k card as a readable who→what→when→edits chain, and show *which recognized signer (trust list) vouched for it*, not just "signature valid."
- **Sources:** [c2pa.org / C2PA spec + developer guide](https://c2pa.ai/for-developers), [CAWG identity assertion (opensource.contentauthenticity.org)](https://opensource.contentauthenticity.org/docs/rust-sdk/docs/cawg-identity/), [C2PA-W3C-08202024 (membership/governance)](https://lists.w3.org/Archives/Public/www-archive/2024Aug/att-0001/C2PA-W3C-08202024.pdf).

### 2. Truepic

- **What:** Commercial secure-camera / "camera-native authenticity" company (C2PA co-founder). Its Lens SDK captures cryptographically-signed, tamper-evident photos/video at the moment of capture — binding location, time, device, and edit history — and Truepic Vision is the enterprise verification product. TIME Best Inventions 2022 for the authenticating camera SDK.
- **User flow:** App vendor integrates Lens SDK → user photographs through the SDK → image is signed + provenance-encoded at capture → later inspection verifies the image is unaltered and shows capture metadata.
- **Docs/onboarding:** developer.truepic.com (SDK), truepic.com blog/product pages.
- **Software shape:** Mobile SDK (Lens), enterprise SaaS (Vision), C2PA-compliant credential output.
- **Adopt:** **provenance at the point of creation.** For CSOAI: the receipt must be bound the instant a benchmark record / duel / card is produced (which our `sim_emit_card` already does at emission), and the Provenance window should emphasize *capture-time vs post-hoc* signing — a record signed at the measurement moment carries materially more weight.
- **Sources:** [Truepic — authenticating camera SDK](https://www.truepic.com/blog/truepics-technology-provides-authenticity-and-content-verification-via-tamper-evident-imagery), [TIME Best Inventions 2022 (Truepic SDK)](https://www.globenewswire.com/de/news-release/2022/11/10/2553559/0/en/Truepic-s-Authenticating-Camera-SDK-Recognized-by-TIME-s-Best-Inventions-2022.html).
- **⚠️ Not verified:** Truepic's current ownership/corporate status (post-2023). Deliberately omitted rather than guessed.

### 3. Sigstore

- **What:** Linux Foundation open-source project for signing software artifacts "keylessly": a developer proves identity via OIDC (GitHub/Google/etc.), Fulcio issues a **short-lived** certificate, the artifact is signed (cosign), and a **Rekor** transparency log records the signing event so anyone can later prove *who signed what and when*.
- **User flow:** `cosign sign` → OIDC token → Fulcio cert → signature + Rekor log entry → `cosign verify` checks signature + log inclusion offline/online.
- **Docs/onboarding:** docs.sigstore.dev; blog.sigstore.dev; quickstart is a handful of CLI commands.
- **Software shape:** Go CLIs (`cosign`, `fulcio`, `rekor`), server components, tlog (Merkle) + CT-style inclusion/consistency proofs.
- **Adopt:** **keyless identity + transparency log.** Our `did:web:csoai.org` trust root already approximates Sigstore's "identity is the key, not a long-lived secret." Copy the *low-friction* signing UX and the *inclusion + consistency proof* so a card can be verified without a pre-distributed key.
- **Sources:** [What is Sigstore / keyless signing](https://safeguard.sh/resources/blog/what-is-sigstore), [cosign GitHub (sign/verify/OCI/in-toto)](https://github.com/api-evangelist/cosign).

### 4. SCITT (IETF)

- **What:** "Supply Chain Integrity, Transparency, and Trust" — an IETF working group specifying an open **Transparency Service** for software/firmware/artifact supply chains. Issuers submit **Signed Statements** (claims); the service registers them in an append-only Merkle ledger and returns a **receipt** proving inclusion; verifiers check statements against the receipt without trusting the issuer.
- **User flow:** Issuer → submit Signed Statement → Transparency Service → receipt; Verifier → fetch statement + receipt → verify inclusion + consistency against the service's published state.
- **Docs/onboarding:** datatracker.ietf.org (`draft-ietf-scitt-architecture`, v19 at time of writing); COSE/Merkle building blocks (RFC 9162).
- **Software shape:** Spec + Internet-Drafts (architecture, profiles like VeritasChain VCP for algorithmic trading); implementations by ecosystem (e.g. peac/SCITT-composition, Microsoft/Ledger-backed).
- **Adopt:** **align our receipt format toward SCITT "Transparent Statement + receipt"** so a CSOAI card is a first-class SCITT statement (claim + signed inclusion receipt), maximizing standards interop rather than a bespoke envelope.
- **Sources:** [draft-ietf-scitt-architecture-19 (Transparency Service)](https://datatracker.ietf.org/doc/draft-ietf-scitt-architecture/19/), [SCITT-VCP profile (algorithmic trading audit trails)](https://datatracker.ietf.org/doc/html/draft-kamimura-scitt-vcp-02).

### 5. OpenTimestamps

- **What:** Peter Todd's trustless proof that *content existed before time T*, with **no trusted third party**. A file's hash is aggregated into a Merkle tree; the tree root is committed into the **Bitcoin** blockchain (via calendar servers); the resulting `.ots` proof can be verified forever against the public chain.
- **User flow:** `ots stamp file.ots` → wait for calendar aggregation + Bitcoin confirmation → `ots upgrade` (attach the Bitcoin block anchor) → `ots verify` at any later date.
- **Docs/onboarding:** opentimestamps.org; GitHub `opentimestamps-client` README; PyPI package.
- **Software shape:** Python `opentimestamps-client` CLI/library; calendar servers; Bitcoin as the anchor; Rust/Dart ports exist.
- **Adopt:** **time-anchor cards to Bitcoin** (or a timestamp authority) so "this card existed before T" is provable without trusting CSOAI's own clock — directly strengthens the "time-anchor" we already carry in signed cards.
- **Sources:** [opentimestamps-client GitHub](https://github.com/opentimestamps/opentimestamps-client), [opentimestamps-client PyPI](https://pypi.org/project/opentimestamps-client/).

### 6. vaara (vaaraio/vaara) — *closest architectural peer to CSOAI*

- **What:** Open-source "evidence layer for AI governance." Gates every AI agent tool call against your policy (allow/block/escalate, risk-scored) and writes a **hash-chained, tamper-evident execution record** an auditor verifies **offline, without trusting the operator**. Ed25519-signed (DSSE pre-auth encoding), `did:web` key identity, binds to **TPM 2.0 / SEV-SNP** hardware root when present, optional opt-in transparency log. AGPL-3.0.
- **User flow:** `pip install vaara` → decorate governed functions (`@vaara.govern`) or drive `InterceptionPipeline` directly → decisions + calls + outcomes land in `~/.vaara/trail/audit.db` → `vaara trail export` to sign for third-party proof → any outsider verifies via `vaara verify-bundle evidence-bundle.json`.
- **Docs/onboarding:** GitHub README + `docs/verifying-evidence.md`, `docs/standards.md`, `docs/conformance-profile.md`; a **46-suite public conformance page** (vaara.io/conformance.html) where third parties post check results; a HuggingFace Space; Zenodo DOI.
- **Software shape:** Python CLI + MCP proxy + server; npm `@vaara/client`; Homebrew/macOS menu-bar; SLSA Build Level 3 provenance; IETF `draft-sirkkavaara-vaara-receipt`; `SEP-2828` execution-record format.
- **The six-lens `verify-bundle`** (this is the killer feature): **Identity** (did:web) → **Signature** (Ed25519) → **Back-link** (binds to request + prior chain head) → **Inclusion** (in transparency log) → **Consistency** (log append-only) → **Revocation** (key/receipt not revoked). `ok` only if a signature is *actually established* — "present in a log but never checked" does NOT pass.
- **The "Resin"** (vaara.io/verify.html): a **single HTML file, no build, no deps** — paste a receipt, it recomputes the digest and checks Ed25519 with WebCrypto **in-browser; the receipt never leaves the tab; works offline.** Crucially, it *explicitly states what a passing check does NOT establish* (key ownership, statement truth, wall-clock time, whole-history).
- **Adopt (highest-value pick):** copy the **Resin** and the **six-lens verifier + honesty list** into the AG UI Provenance window. "Verify anything, client-side, offline, and say exactly what the green check does *not* prove."
- **Sources:** [vaara README (vaaraio/vaara)](https://github.com/vaaraio/vaara), [verifying-evidence.md](https://github.com/vaaraio/vaara/blob/main/docs/verifying-evidence.md), [standards.md](https://github.com/vaaraio/vaara/blob/main/docs/standards.md), [Vaara Receipt Internet-Draft](https://datatracker.ietf.org/doc/draft-sirkkavaara-vaara-receipt/).

### 7. PipeLab (Pipelock) — *the "independent attestation" peer*

- **What:** "Agent Action Receipts — signed evidence for what an AI agent did." A **mediator outside the agent trust boundary** (a proxy on the agent's HTTP/MCP/WebSocket path) records each adjudicated action and signs it, so verification does not depend on the agent's own (rewritable) logs. Explicit thesis: **independent attestation vs self-attestation**.
- **User flow:** Put Pipelock on the agent's network/MCP path → enable flight recorder + mediator signing key → each mediated action becomes an Ed25519-signed, hash-chained receipt (`evidence.jsonl`) → bundle into an "Audit Packet v0" → a third party verifies with a pinned public key + a standalone verifier (no vendor dashboard).
- **Docs/onboarding:** pipelab.org/learn ("Agent Action Receipts", "What did my agent do", "Action Receipt Spec"); **public conformance corpus** (golden/malicious/edge fixtures) + copy-paste walkthroughs.
- **Software shape:** Pipelock proxy; verifiers in **Go, TypeScript, Rust, Python** (`pipelock verify-receipt`, `pipelock-verifier`, …); JSON Schema `audit-packet-v0.schema.json`; receipt = `{action_record, Ed25519 sig over SHA-256(canonical-JSON), signer_key}` with `chain_prev_hash` linkage; **exit codes 0 accept / 1 reject / 2 verifier error / 64 usage error**.
- **Adopt:** (a) label every Provenance record **self-attested vs independently-attested**; (b) publish a **public conformance corpus** for our card format so outsiders can prove *their* verifier works before trusting it; (c) ship a **standalone exit-code CLI verifier** (`csoai verify-card` → 0/1/2/64) that imports no vendor code.
- **Sources:** [Agent Action Receipts (PipeLab)](https://pipelab.org/learn/agent-action-receipts/), [Mediator receipts — independent attestation](https://pipelab.org/blog/independent-attestation-mediator-receipts/).

### 8. signet-auth (Prismer-AI) — *the MCP-native peer*

- **What:** "Cryptographic receipts for every AI agent tool call — signed, hash-chained, offline-verifiable, provider-independent." Each agent gets an Ed25519 identity; every `tools/call` is signed, appended to a hash chain, verifiable offline or *before execution* (execution boundary), with **bilateral co-signing** of responses.
- **User flow:** `signet proxy --target <cmd> --key <name>` drops in front of **any MCP server** (no agent/server code changes) → signs every `tools/call` → optional policy engine blocks/records → local append-only audit log + dashboard; a **live browser demo** (signet-auth.vercel.app) lets you sign a tool call, tamper a field, and watch verification fail.
- **Docs/onboarding:** GitHub README (v0.10), `docs/guides/mcp-integration.md`, `docs/COMPLIANCE.md` (maps to SOC 2 CC7.2, ISO 27001 A.8.15, **EU AI Act Art. 12**, NIST AI RMF), YouTube walkthroughs.
- **Software shape:** Rust `signet-core`, Python `signet-auth`, 6 npm packages (`@signet-auth/core`, `@signet-auth/mcp`, `@signet-auth/mcp-server`, `@signet-auth/mcp-tools`, `@signet-auth/node`, `@signet-auth/vercel-ai`); Apache-2.0/MIT. Features: `trace_id`/`parent_receipt_id` causal chaining, **delegation chains** (who authorized, what scope), **PolicyAttestation** embedded in receipt.
- **Adopt:** **MCP-native receipt signing** — wrap our AG tool calls with a `signet`-style proxy so every `tools/call` gets a receipt; add **delegation chains** ("who authorized this action, under what scope") and **bilateral co-signing** (both agent and server sign).
- **Sources:** [signet README (Prismer-AI/signet)](https://github.com/Prismer-AI/signet), [signet-core (crates.io)](https://crates.io/crates/signet-core), [@signet-auth/core (npm)](https://www.npmjs.com/package/@signet-auth/core).

### 9. OpenAI provenance (C2PA-based)

- **What:** OpenAI (a C2PA steering-committee member) embeds **C2PA Content Credentials** metadata into images generated by **DALL·E / ChatGPT**, and the `gpt-image-1` API emits C2PA manifests; Azure OpenAI exposes "Content Credentials." OpenAI also ships an **image-detection classifier** (reported ~98% accurate on DALL·E 3 at launch, May 2024) to identify its own generations, and participates in SynthID watermarking for some outputs.
- **User flow:** Generate an image → the artifact carries C2PA metadata (and/or SynthID watermark) → any C2PA verifier (or OpenAI's classifier) checks "was this made by OpenAI / has it been altered."
- **Docs/onboarding:** OpenAI Help Center ("C2PA in ChatGPT Images", "Provenance signals (Content Credentials, SynthID)"); Azure AI docs "Content Credentials."
- **Software shape:** C2PA manifest in API responses; classifier; Azure Content Credentials for Azure OpenAI.
- **Adopt:** **provenance at generation time** (not bolted on) + a **"is this CSOAI-generated?" detector** surfaced in the Provenance window — users can both *read* our receipt and *ask* "did a CSOAI measurement produce this?"
- **Sources:** [C2PA in ChatGPT Images (OpenAI Help)](https://help.openai.com/en/articles/8912793-c2pa-in-chatgpt-images), [Provenance signals — Content Credentials + SynthID (OpenAI Help)](https://help.openai.com/en/articles/8912793-provenance-signals-content-credentials-synthid-in-openai-generated-content), [Azure OpenAI Content Credentials](https://learn.microsoft.com/azure/ai-services/openai/concepts/content-credentials).

### 10. SynthID (Google DeepMind)

- **What:** Google DeepMind's **imperceptible statistical watermarking** + detection for AI-generated content, spanning **text** (token-level watermarking of LLM output), **image**, **audio** (SoundStream/Lyria), and **video** (Veo). The watermark is embedded in the generation process itself, so it survives when C2PA-style metadata is stripped; a "SynthID Detector" scans for it.
- **User flow:** Generate content with watermark enabled → later run the SynthID scanner/detector → a confidence score reports "likely/possibly/not watermarked" (statistical, not cryptographic proof).
- **Docs/onboarding:** deepmind.google/synthid; Google AI for Developers "Responsible Generative AI Toolkit" (SynthID text watermarking, open-sourced); SynthID Detector launched 2025.
- **Software shape:** DeepMind model capability; SynthID Detector; open-source text-watermarking in the Responsible GenAI Toolkit.
- **Adopt:** treat watermark as a **lossy-but-robust fallback channel** alongside our cryptographic receipts: the receipt is the *proof*, SynthID-style watermarking is the *resilient hint* when metadata is stripped. **Honesty note for our UI:** label watermark results as *statistical/confidence*, never "verified."
- **Sources:** [SynthID (DeepMind)](https://deepmind.google/models/synthid/), [SynthID text watermarking (Google AI for Developers)](https://ai.google.dev/responsible/docs/safeguards/synthid), [Google SynthID Detector (The Verge)](https://www.theverge.com/news/672013/google-synthid-detector-ai-generated-content-watermark-i-o-2025).

### 11. DigiCert (document signing / CA anchor)

- **What:** Certificate authority providing **document signing certificates** and **Document Trust Manager**; DigiCert certificates are on the **Adobe Approved Trust List (AATL)** and **eIDAS** trust lists, so PDFs signed with them are automatically trusted/validated in Acrobat and EU-compliant contexts.
- **User flow:** Provision a signing cert → sign a document (Adobe/Acrobat, or API) → the document carries a signature that validates against a widely-trusted CA root + AATL/eIDAS list.
- **Docs/onboarding:** digicert.com/document-trust-manager, knowledge.digicert.com (AATL integration), datasheets.
- **Software shape:** Document Trust Manager (DigiCert ONE), API/SaaS, hardware-backed key options.
- **Adopt:** the **trust-list + revocation** discipline — publish a **CSOAI Approved Signer list** (mirroring AATL/eIDAS), and make **revocation status** a first-class check in every card verification (not just "signature valid").
- **Sources:** [DigiCert Document Trust Manager — Adobe](https://www.digicert.com/document-trust-manager/adobe), [DigiCert + Adobe Approved Trust List (KB)](https://knowledge.digicert.com/solution/digicert-and-adobe-approved-trust-list).

### 12. EU AI Act Article 50 (marking / regulatory anchor)

- **What:** Legal obligations (not a tool). Article 50 requires **machine-readable marking** of AI-generated *synthetic* content (Art. 50(2)) and *disclosure* for deepfakes (Art. 50(4)); providers of general-purpose AI must mark outputs per Art. 50(1). A **final Code of Practice on transparency of AI-generated content** (GPAI, under Art. 53) specifies how (metadata, watermarking, and their interplay with C2PA). Effective 2 Aug 2026 (transparency rules).
- **User flow:** Provider → embed machine-readable provenance/watermark at generation → downstream detects/discloses → regulators/auditors verify compliance.
- **Docs/onboarding:** EU AI Act text (Art. 50), European Commission draft guidelines + final transparency Code of Practice; practitioner analyses (Freshfields, Dastra).
- **Software shape:** N/A (law) — realized via C2PA/metadata/watermark implementations; Anthropic is adding watermarks to Claude output to meet these rules (per cited coverage).
- **Adopt:** position CSOAI receipts as **Article 50 compliance evidence** (machine-readable marking + traceability), and in the Provenance window **map each check to the governing clause** ("this receipt satisfies Art. 50(2) machine-readable marking") so a regulator sees the compliance linkage directly.
- **Sources:** [Freshfields — final Code of Practice on transparency (EU AI Act Unpacked #33)](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-33-the-final-code-of-practice-on-transparency-of-ai-generate-102n4yx), [Dastra — AI Act transparency rules, 2 Aug 2026](https://www.dastra.eu/en/blog/ai-act-transparency-rules-what-changes-august-2-2026/60164), [Anthropic watermarks for EU transparency (news)](https://azertag.az/en/xeber/anthropic_to_embed_hidden_watermarks_in_claude_ai_content_to_meet_new_eu_transparency_rules-4361501).

---

## 3. What CSOAI should adopt — 5 concrete improvements for the AG UI Provenance chat window

> These are prioritized for *our* stack: Ed25519 receipt spine, 3KB signed h3k cards, `did:web:csoai.org` trust root, RFC-8785 canonical-JSON, time-anchored cards. Each improvement names the **tool to embed** and the **flow to copy**.

### (1) Verify-anything input — a client-side, offline, self-describing verifier
**Copy:** vaara's "Resin" (single HTML, WebCrypto, paste → digest → Ed25519 check, nothing leaves the tab, works offline) + PipeLab's exit-code discipline + signet's live "tamper a field, watch it fail" demo.
**Tool to embed:** a paste/upload box that auto-detects the format — h3k card, vaara/SCITT receipt, C2PA manifest, PGP/SSH/Ed25519 signature, OpenTimestamps `.ots`, SynthID report — and verifies **in-browser** with WebCrypto (no server round-trip for the crypto check).
**Flow to copy:** paste → auto-detect → verify → render a **per-check pass table** (not a single boolean), with exit-code semantics (0 accept / 1 reject / 2 verifier error / 64 usage error).
**Adoptable "honesty" flourish:** always print, verbatim, *what a green check does NOT establish* (key ownership, statement truth, wall-clock time, whole-history) — this is the single most trust-building, differentiating behavior we saw.

### (2) Watermark / authenticity checks as first-class tools
**Copy:** Content Credentials "Verify" site (upload media → see the provenance chain + trust list) + SynthID Detector + OpenAI classifier + OpenTimestamps verify.
**Tool to embed:** in the Provenance window, expose four tools: **C2PA manifest check** (render who/what/when/edits + trust-list membership), **SynthID-style watermark scan** (confidence: likely/possibly/not — labeled *statistical*), **"is this CSOAI-generated?"** detector, and **OpenTimestamps verify** (prove "existed before T" against Bitcoin).
**Flow to copy:** one prompt — *"check this image/card"* — fans out to all applicable checks and returns a single, clearly-labeled verdict panel (crypto proof vs statistical hint kept visually separate, never conflated).

### (3) Receipt queries + set-level audit summary (not just single-card verify)
**Copy:** vaara's six-lens `verify-bundle` (Identity → Signature → Back-link → Inclusion → Consistency → Revocation) and `audit-summary`; PipeLab's chained `evidence.jsonl` + "Audit Packet" bundle.
**Tool to embed:** `csoai verify-bundle` and `csoai audit-summary` behind natural-language queries — *"verify all cards from hive `meok` in the last 24h"*, *"show any record signed but missing an outcome"*, *"is the transparency log still append-only?"*.
**Flow to copy:** set-level verification with a **per-lens pass count** and gap detection (duplicate records, authorized-but-no-outcome, executed-but-no-result), mirroring vaara's `verify-records` set-level forms.

### (4) Transparency-log inclusion + consistency, plus a public conformance corpus
**Copy:** Sigstore Rekor (keyless OIDC identity + Merkle transparency log) + SCITT (transparent statement + receipt) + PipeLab's public conformance corpus + vaara's public conformance page (third parties post their own verdicts, rows hash-chained).
**Tool to embed:** (a) an append-only **CSOAI transparency log** where every card gets an inclusion + consistency proof; (b) a **public conformance corpus** (golden/malicious/edge fixtures) so any outsider can prove *their* verifier works before trusting it on our cards; (c) a **standalone, dependency-light verifier** that imports no vendor code (like vaara's checker: `cryptography` + `rfc8785` only).
**Flow to copy:** "verify without trusting the producer" — the Provenance window links to the corpus and the standalone checker, so the answer to "why should I trust CSOAI?" is "don't — run the verifier yourself."

### (5) Attestation-trust labeling + policy/authorization binding + regulatory mapping
**Copy:** PipeLab's **self vs independent attestation** distinction; signet's **delegation chains** + **PolicyAttestation** + bilateral co-signing; vaara's **did:web identity** + TPM/SEV hardware binding; EU AI Act **Art. 50 clause mapping**.
**Tool to embed:** every record in the Provenance window is tagged **`self-attested` vs `independently-attested`**, carries a **policy hash** and **delegation chain** ("who authorized, under what scope"), and — where hardware is present — a **TPM 2.0 / SEV-SNP binding** indicator.
**Flow to copy:** the verify panel maps each check to a governing clause (*"satisfies EU AI Act Art. 50(2) machine-readable marking / Art. 12 record-keeping"*), so a regulator reads the compliance linkage directly instead of being handed raw bytes.

---

## 4. One-line synthesis for the AG UI Provenance window

> **"Verify anything, offline, in-browser; report *per-check* passes with exit-code semantics; label self- vs independent-attestation; state exactly what a pass does *not* prove; time-anchor to Bitcoin; expose a trust list + revocation; and map every check to EU AI Act Art. 50."**

---

## Honesty & verification log

- **Directly verified from primary source (curl/GitHub raw):** vaara README + verifying-evidence.md; signet README; PipeLab agent-action-receipts page (schema-org + body).
- **Verified via cited web sources (search):** C2PA spec/CAWG, Truepic SDK, Sigstore, SCITT draft, OpenTimestamps, OpenAI C2PA/classifier, SynthID, DigiCert AATL/Document Trust Manager, EU AI Act Art. 50 + Code of Practice.
- **Flagged, not asserted:** Truepic post-2023 corporate status (ownership/acquisition) — omitted as unverified.
- **Scope:** research only. No accounts created, no submissions made, no external writes.
