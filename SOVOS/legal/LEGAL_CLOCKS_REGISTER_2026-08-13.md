# Legal Clocks Register — 2026-08-13 (first run of the never-opened register)

**Doctrine (Part CD/CB):** the register re-runs monthly; no new threads until a run closes more than it opens. This is run #1 — it opens the register itself.

## Verified this run

| Clock | Status | Evidence (verified 2026-08-13) |
|---|---|---|
| **TLS certs ×5** | ✅ LOW RISK — auto-renew class | csoai.org expires 2026-11-08 · councilof.ai 2026-10-30 · meok.ai 2026-10-29 · proofof.ai 2026-10-30 · safetyof.ai 2026-11-03. All issuer **Google Trust Services WE1** = Cloudflare-managed edge certs, auto-renewed ~30 days out. Residual risk: registrar billing lapse or CF account issue — see watches below. |
| **Companies House — CSOAI Ltd (16939677)** | ✅ ACTIVE, no urgent clock | Incorporated 2 Jan 2026, private limited, model articles, GBP 1 capital. Only filing on record: NEWINC. **Confirmation statement: first due by ~16 Jan 2027** (12-month review period ends 1 Jan 2027 + 14 days). **First accounts: ARD defaults to 31 Jan 2027, due by 2 Oct 2027** (21-month first-accounts rule). Nothing due in 2026. |
| **proofof.ai domain** | ✅ bleed closed | Domain serves a 470-byte meta-refresh redirect to councilof.ai; zero SOV4/sovereign strings (live-verified 2026-08-13). The owner-gate item from Part AX–CK is effectively resolved; formal "archive/kill" decision remains Nick's, but there is nothing left to scrub. |

## Verified this run — browser pass (2026-08-13 ~07:10, webbridge, Nick's sessions)

| Clock | Status | Evidence (verified live 2026-08-13) |
|---|---|---|
| **ICO registration** | 🔴 **GAP — not registered** | ICO register searched under both "Council for the Safety of Artificial Intelligence" and "CSOAI" → *"There are no entries that match your search criteria"* (both). If CSOAI Ltd processes personal data (waitlist/signup emails count), the UK data-protection fee (from £40/yr) is almost certainly owed — registration is a legal requirement, not optional. **Action: register at ico.org.uk before any personal-data collection is publicly claimed; ~15 min online.** |
| **UK IPO — "Council of AI"** | ✅ CLEAR | Zero UK marks matching "Council of AI" (Similar search) and zero for "Council for the Safety of Artificial Intelligence". The rename target is registrable. **Action: file ~£170/1 class (cl 9/42) before public launch locks the name; opposition windows make waiting the expensive option.** |
| **UK IPO — "GSPC"** | ⚠️ OCCUPIED, classes clear | 20 marks match "GSPC". Live Registered: UK00003193446 (cl 16,35,36,40,41 · filed 2016), UK00003407104 (cl 35 · 2019), UK00003413505 (cl 35,36,43 · 2019). **Class 9/42 "GSPC" marks are EXPIRED (2006 filings)** — software/scientific classes appear unoccupied among live marks seen (7 of 20 reviewed; remaining 13 = page-2, next run). GSPC usable in cl 9/42 with a clearance opinion; "Council of AI" is the cleaner mark. |

## Not verifiable without browser session (queued for webbridge)

| Clock | What to check | Where |
|---|---|---|
| **Registrar billing** | Which registrar holds the 5 domains, auto-renew on/off, card validity | registrar account (webbridge) |
| **Stripe catalogue audit** | £1/£9/£29 ladder live in public READMEs (X4) vs Stripe products — mismatch = billing disputes | dashboard.stripe.com |
| **PyPI/npm token security** | eu-ai-act-compliance-mcp 1.8.15 + meok-attestation-verify 1.0.4 (X3: installable code carrying £199/mo attestation + proofof.ai verify endpoint claims) | pypi.org/npmjs.com account pages |

## Open watches (no action needed yet, re-check next run)

- **Cert renewal verification:** confirm each domain's cert actually renews inside the auto window (~2 Oct 2026 onward). One check per domain per month.
- **Registrar expiry dates:** cert ≠ domain. Domain registration expiry dates not yet pulled — do at next run (or webbridge pass).
- **Dead-man's switch:** monitoring for Nick-inaccessible scenarios — never opened; design owed (N-register).
- **Bus factor = 1:** failure-domain doctrine never applied to the human layer — all infra logins, keystone, and accounts route through one person. Documented as the estate's largest unmitigated single point of failure.
- **HF bank backups outside HF:** banks are on HF + MinIO (boards) but the HF→MinIO bank-level mirror is partial — complete it (affects K3 disposition too).

## Next run: 2026-09-13 (monthly). Close-more-than-open rule applies from run #2.

---

## Delta — EU AI Act dates verified against Digital Omnibus (2026-08-13, two independent web searches, consistent)

The Omnibus Regulation (EU) 2026/1744 entered into force 27 Jul 2026 and moved several AI Act clocks. Verified positions, now canonical for planning:

| Provision | Date | Status |
|---|---|---|
| **Art 50 transparency obligations** | **2 Aug 2026** | 🔴 **LIVE NOW — enforceable.** Any public genAI artifact must carry AI-disclosure per Art 50; our own pages/papers/banks are in scope. |
| **Art 50(2) marking grace** (genAI systems placed on market before 2 Aug 2026) + **new Art 5(1)(ba)(bb)** NCII/CSAM prohibitions | **2 Dec 2026** | ~16-week runway from 2026-08-13. This is the playbook's Phase-4 horizon. |
| **Art 57 national regulatory sandboxes** (member states must establish) | **2 Aug 2027** | ⚠️ CORRECTION: any line saying "states owe a sandbox in 2026" is stale — Omnibus moved it to Aug 2027. |
| **Annex III high-risk obligations** | **2 Dec 2027** | Post-Omnibus date. |
| **Annex I product-embedded AI** | **2 Aug 2028** | Post-Omnibus date. |
| Notified-body designation (Art 43(3)) | 28 Jan 2028 | |
| Machinery Regulation (EU) 2023/1230 | 20 Jan 2027 | Sectoral, unchanged — relevant to `mach`/embodied axis. |

**Planning consequences:** (1) Art 50 compliance is not a future item — it binds today; the Art 50 evidence pack is the correct flagship. (2) The 2 Dec 2026 marking window is the real near-term deadline for the public artifact estate. (3) Sandbox-window language in the flywheel playbook §2 confirmed accurate post-verification; sandbox timing is 2027, not 2026.

*Verified by kimi lane via live web search 2026-08-13; sources consistent across two independent queries. Dated addition, not a silent edit.*
