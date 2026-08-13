# Legal Clocks Register — 2026-08-13 (first run of the never-opened register)

**Doctrine (Part CD/CB):** the register re-runs monthly; no new threads until a run closes more than it opens. This is run #1 — it opens the register itself.

## Verified this run

| Clock | Status | Evidence (verified 2026-08-13) |
|---|---|---|
| **TLS certs ×5** | ✅ LOW RISK — auto-renew class | csoai.org expires 2026-11-08 · councilof.ai 2026-10-30 · meok.ai 2026-10-29 · proofof.ai 2026-10-30 · safetyof.ai 2026-11-03. All issuer **Google Trust Services WE1** = Cloudflare-managed edge certs, auto-renewed ~30 days out. Residual risk: registrar billing lapse or CF account issue — see watches below. |
| **Companies House — CSOAI Ltd (16939677)** | ✅ ACTIVE, no urgent clock | Incorporated 2 Jan 2026, private limited, model articles, GBP 1 capital. Only filing on record: NEWINC. **Confirmation statement: first due by ~16 Jan 2027** (12-month review period ends 1 Jan 2027 + 14 days). **First accounts: ARD defaults to 31 Jan 2027, due by 2 Oct 2027** (21-month first-accounts rule). Nothing due in 2026. |
| **proofof.ai domain** | ✅ bleed closed | Domain serves a 470-byte meta-refresh redirect to councilof.ai; zero SOV4/sovereign strings (live-verified 2026-08-13). The owner-gate item from Part AX–CK is effectively resolved; formal "archive/kill" decision remains Nick's, but there is nothing left to scrub. |

## Not verifiable without browser session (queued for webbridge)

| Clock | What to check | Where |
|---|---|---|
| **ICO registration** | Is CSOAI Ltd (or Nicholas Templeman) on the data-protection register? Handling user data (signups, Stripe) without ICO registration is a fee/fine exposure. | ico.org.uk register search — JS-driven, curl blind |
| **UK IPO trademarks** | "Council of AI", "GSPC" — any conflicting registrations; decide file-or-monitor. Trademarks have opposition windows — a clock you can't pause. | trademarks.ipo.gov.uk |
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
