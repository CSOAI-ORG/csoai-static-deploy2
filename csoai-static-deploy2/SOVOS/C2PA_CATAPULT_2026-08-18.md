# C2PA CATAPULT — LAUNCH PLAN — 2026-08-18

**Premise:** CSOAI is now a C2PA Contributor member with a live onboarding wave
(GitHub org + Slack + conformance-administrators team + 9 TF invites). The Conformance
Program is **declarative YAML rubrics evaluated by a Python `json_formula` engine** —
that is CSOAI's measurement-methodology lane, and the spec is at **2.4** (text support
live). Catapult = contribute neutral measurement → early signal → co-member intros.

## PHASE 1 — ONBOARD COMPLETE (this week, no gate)
1. ✅ Mailbox wired (keystone → nicholas@csoai.org, 6,938 msgs, himalaya configured)
2. ⏳ **Accept GitHub invite** → unlocks `twg-meetings`, `the_way_we_work`, `conformance-administrators` (2 private repos)
3. ⏳ **LFX profile** → https://openprofile.dev (meeting invites, votes, attendance badges)
4. ⏳ **Groups.io** → Main + TWG subgroups (Conformance, Agentic, AI/ML, Text, Watermark priority)
5. ⏳ **Slack** → ccpaworld.slack.com

## PHASE 2 — FIRST CONTRIBUTION (the wedge PR)
- **GSPC→C2PA mapping pack** (built: `SOVOS/c2pa-catapult/gspc-c2pa-mapping.json` — 16 axes mapped to rubrics/vocabulary)
- **PR #1 to `c2pa-org/conformance-public`**: a governance-rubric expression pack (neutral, technical, no certification claims)
- PR #2: signed-card corpus → `public-testfiles` (CSOAI 3KB h3k cards as C2PA test vectors)

## PHASE 3 — TASK FORCE PRESENCE (Aug 20+) — per GW.3 firewall
- **Priority TFs (concentrate 4, ignore rest): Conformance · Watermarking · Threats & Harms · AI/ML (+CAWG identity tracking).**
- ZKP / Ledgers / Agentic: UNVERIFIED as chartered groups — research threads only, NEVER cited externally as memberships.
- 30/60/90 sequence: EasyCLA (CLA) → 2–3 well-scoped issues → ONE merged contribution per priority TF → one open-source conformance/measurement tool.
- Endorsement language lock: may say "contributes to the C2PA TWG / [TF]"; NEVER "C2PA-certified", "partner", "endorsed", "official provider".
- Standing earned via merged code/test-vectors/spec sections (12–24 months), NOT attendance.
- **TWG Meeting #2: Special Topics** — Thu Aug 20, 11:00 (Zoom LFX 99579049307)
- **Conformance TF** — join + volunteer measurement-methodology workstream
- **Agentic TF** — pitch: agentic-provenance rubric using CSOAI's signed-card format
- **AI/ML TF** — attested system environment ↔ DEFONEOS signed attestation
- **ZKP TF** — Wed Aug 26, 13:00 (Zoom LFX 94495920909)

## PHASE 4 — PRODUCT (the catapult ship)
- **`c2pa-rubric-measure` MCP** — wraps the C2PA rubric evaluator (json_formula): input manifest → rubrics → verdict. CSOAI's measurement body inside the conformance program.
- Wire the 7 existing C2PA/Art.50 MCPs to spec 2.4 (June intel said 2.1 — refresh).
- Mapping pack → public page (csoai.org) once rubrics land: "CSOAI measures C2PA conformance, neutrally."

## FIREWALL (board doctrine — binding)
- Contribute measurement only; never lobby for certification powers
- Never pre-brief a vendor client; never take a seat conflicting with neutrality
- All GSPC scores stay quotable-with-CI; no invented numbers, no cert claims

## OPEN DECISION
- **SSL.com** (C2PA certificate vendor, 2 follow-ups): keep-active (feed requirements) or close. Nick.

---
*Canonical: `SOVOS/C2PA_ONBOARDING_2026-08-18.md` + this plan + `gspc-c2pa-mapping.json`.*

## 18 Aug 04:55 addendum — CONFORMANCE PROGRAM ALREADY IN MOTION
- **Generator Product legal agreement SIGNED** (Aug 4, per Conformance Admin email ID 6518).
- **Intake Form PENDING** (Google Form link in that email) — Nick completes this week.
- This flips the SSL.com decision: **own-certificate route primary** (conformant generator + own claim-signing cert, Publisher: CSOAI).
- SSL.com reply v2 drafted (SSL_COM_REPLY_DRAFT_v2_2026-08-18.md) — re-asks the 5 unanswered questions against the own-cert path.
- Next: intake form → evaluation → Conformance Letter → CSR → SSL validation → cert.
