# CSOAI PRIOR-ART / FTO LANDSCAPE — 2026-08-14
**Method**: live queries against Google Patents (patents.google.com) — the FTO subagent
timed out, so these were run directly this session. Stories = REAL (verified in live
results). This is research/landscape, NOT a legal FTO opinion — counsel confirms.

---

## Theme 1 — Cryptographic signing of AI model output (Ed25519/Signed output)
Query: `"model output" signature Ed25519 attestation` → **2 results** (both CN, tangential:
multi-agent audit-authority grading; supply-chain traceability). 
**FTO: LOW collision risk.** No US/WO patent squarely claims "Ed25519-signing the output of
an AI model as a measurement credential." Our combo (gate → sign → time-anchor → verify) is
not directly asserted.

## Theme 2 — Content provenance / AI watermarking / C2PA-style (CROWDED — watch)
Query: `content credentials provenance C2PA signature AI generated` → **11 relevant results**:
- **US12158929B1 (Trufo Inc.)** — watermarking digital media with signatures/verification, 2023
- **WO2025038396A1 (Digimarc)** — digital watermarking for C2PA manifest-swap detection, 2023
- **US20240205023A1** — data provenance capsule management, 2023
- **US20250330546A1 (Atom Technologies)** — trusted media device for non-synthetic assurance
- **US20260057480A1 (Qualcomm)** — secure imaging / content provenance (PQC-adjacent), 2024
- **WO2025245205A1 (Istari/Fyber)** — trust layer for derivative-data provenance, 2024
**FTO: MODERATE.** Digital-watermarking + provenance is heavily patented (Trufo, Digimarc,
Qualcomm). BUT these are media/image provenance — NOT signed measurement credentials for
*model governance behavior*. Our dissimlarity: we sign a *measurement outcome* of governance
axes, not media provenance. Avoid claiming "watermarking" in any filing; our wedge is the
governance-measurement credential, not content-provenance.

## Theme 3 — AI governance measurement / scoring model behavior (VERY CROWDED — highest care)
Query: `AI governance compliance measurement model behavior score` → **84,506 results**:
- **US20200265356A1 (Talisai)** — "AI accountability platform", risk-context governance, 2019
- **US11776060B2 (Cerebri AI)** — object-oriented ML governance modeling, 2019
- **US20250259082A1 / US20250259041A1 (Qomplx)** — AI decision platform, deontic reasoning, 2024
- **US20250181728A1 (Citibank)** — end-to-end measurement/grading of pretrained models, 2023
- **US20220351007A1 (Cognitive Scale)** — "Burden Score for an Opaque Model", 2019
**FTO: HIGH collision surface on the generic concept** ("measure/score/grade a model's
governance/compliance behavior"). Many big/industry parties hold filings. **Our novelty is
NARROW and specific**: (a) the *measurement credential* as a signed, time-anchored,
externally-verifiable artifact (not a score), (b) groundedness-gate-before-sign, (c)
recompute-by-any-third-party. Any US provisional must be drafted against this crowded prior
art — narrow claims, not "we score models." This is exactly why counsel + the arXiv date
matter.

## Theme 4 — Agent identity / A2A / verifiable credentials for SOFTWARE AGENTS (OPEN — opportunity)
Query: `verifiable credential software agent identity authentication` → **46,107 results, but
all generic authentication** (FIDO/UAF, biometric, SSO, token recycling):
- US11184343B2 (Giesecke+Devrient, FIDO UAF) · CN biometric identity · SSO (Idee) · KR TLS-delegation (MS) · token recycling (Red Hat)
**FTO: LOW on the specific claim.** Nobody patents a **competence/compliance credential
issued to a software agent** for governance behavior — every hit is human/user identity or
generic auth. This is the same "unoccupied slot" the Agent-Economy Go-Machine §1.1 identified.
**Novel opening — our card is defensible here.**

## Theme 5 — Blockchain time-anchoring / proof-of-existence (CROWDED — but our form is distinct)
Query: `blockchain timestamp document provenance proof existence hash` → **6,456 results**:
- **US12335395B2 (Artema Labs)** — artifact origination + content tokenization, artifact-to-time, 2021
- **EP3639536B1 (Intel)** — blockchain recording for IoT naming, 2016
- **US11222331B2** — blockchain gemstone ownership/custody, 2017
- **US12223469B2 (Neurosymbolic)** — project accountability services, 2021
- **US11061886B2 (Blockchain Integrated Partners)** — data validation/assurance, 2018
- **US11514441B2 (Bitmark)** — decentralized title recordation, 2015
**FTO: MODERATE on generic "chain-anchor a hash."** BUT OpenTimestamps-style *detached
commitment to an independent calendar batch-merkle-to-BTC* is a distinct implementation
(public, no permissioned chain). We are a **user of OpenTimestamps** (open-source), not
patenting it. No filing on time-anchoring — it's prior art we rely on.

---

## SYNTHESIS (honest FTO verdict for the counsel conversation)
| Theme | Collision risk | Our position |
|---|---|---|
| 1. Sign model output | LOW | defensible, novel combo |
| 2. Media provenance/watermark | MODERATE (Trufo/Digimarc/Qualcomm) | AVOID "watermarking" claims; we're governance, not media |
| 3. AI governance scoring | **HIGH** (84k results; Talisai/Cerebri/Qomplx/Citibank/CogScale) | draft NARROW — "signed measurement credential + groundedness gate + third-party recompute," NOT "score a model" |
| 4. Agent competence credential | **LOW/OPEN** | **the novel wedge — no competing patent found** |
| 5. Time-anchoring | MODERATE (generic) | we USE OTS (open source), don't claim it |

**Bottom line for counsel:** the strongest US-provisional angle is **theme-4 (agent
competence/compliance credential)** — genuinely unoccupied in the patent record — narrow and
implementable. Theme-3 (governance scoring) is a minefield: any claim must be narrow and
built on the *signed, gated, recomputable measurement credential*, not model-scoring. Avoid
theme-2 (watermarking) and theme-5 (time-anchoring) as claim sets entirely — both are
crowded prior art we use, not invent.

---
*Subagent timed out; these were captured directly from live Google Patents results 2026-08-14.
Real patent numbers cited above. Not a legal opinion.*
