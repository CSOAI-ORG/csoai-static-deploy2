# Council of AI — Position + Consolidated Plan
## 2026-08-16 · JEEVES lane · aligned with K3 EU-1/EU-2 inspection board

---

## 1. The positioning paragraph

Council of AI (CSOAI Ltd, UK 16939677) is a measurement body that creates a market
it does not participate in. We measure how AI systems behave against frozen,
published benchmarks across 13 governance axes and issue the result as a 3KB signed
measurement credential — Ed25519-signed, timestamp-anchored, anyone can verify
without asking us. We do not fix the AI. We do not consult on remediation. We
measure who is best at fixing, publish it, and the market routes itself. Whoever
tops the board gets the work — which means our incentive is to rank accurately,
because if the top-ranked fixer does bad work, the board is worthless. That is
a self-correcting loop. No referral fees, no equity in fixers, no ownership of
remediation shops. Published methodology, ranked whether they like it or not.
That is the discipline that survives counsel and an outside room.

---

## 2. The market-rail architecture

### Tier 1 — Measure (CSOAI earns here)
- Signed card per AI system per axis: accuracy, n, 95% CI, Ed25519 sig, timestamp
- £199/mo re-attest, £500–£5K enterprise measurement runs
- Re-attest loop: measure monthly, issue delta cards — the recurring engine

### Tier 2 — Verify (free, forever)
- Client-side WebCrypto recomputation — runs in the user's browser
- No account, no login, no server. Zero marginal cost.
- Every verification IS distribution. Every verifier is a lead.

### Tier 3 — Rank fixers (CSOAI publishes, does not profit)
- Directory of independent remediation providers who USE the cards
- Criteria: can read a card, can map it to a fix plan, use the public verify endpoint
- No CSOAI ownership, no referral fees, no revenue share
- The routing rule is mechanical: "the top-ranked model on each axis, whichever it is"
- Twenty independent shops needing cards to start work = measurement becomes the standard by adoption, not permission

### The money-flow rule (the whole test)
Never take a fee, a kickback, or equity from a ranked fixer. No payment either
direction. Fixers ranked whether they like it or not. This is the line that makes
it survive counsel and survive an outside room.

---

## 3. Owner-gated items

| # | Item | Gate | Deadline/note |
|---|------|------|---------------|
| **G1** | **arXiv endorser forward G6Y9SY** | 🟡 Nick | **HARD: Aug 27, 12 days** |
| G2 | Stripe live keys → keystone sync-vercel | 🟡 Nick | Blocks checkout 500s; first £ blocked |
| G3 | npm 2FA + SMITHERY | 🟡 Nick | Blocks distribution revenue |
| G4 | CF AI-bot-block toggle (councilof.ai zone) | 🟡 Nick | EO-1 — one click in dashboard |
| G5 | THE ONE NAMING RULING — 23+ public SOV URLs + nav + titles | 🔴 Nick | Blocks N4 apex purge + B7 sweep |
| G6 | GSPC leader vs honest harness reconciliation (F17) | 🔴 Nick | Credibility-critical |
| G7 | Two-signer public attribution ruling | 🟡 Nick | Which key signs what |
| G8 | gdrive reconnect + A100-1 console reboot | 🟡 Nick | Estate resilience |
| G9 | LOT Network membership confirmation | 🟡 Nick | Badge pending→confirmed |
| G10 | BSI ART/1 seat (UK mirror of ISO/IEC SC 42) | 🟡 Nick | Pack at SOVOS/BSI_ART1_SEAT_2026-08-15.md |
| G11 | C2PA badge gate on meok.ai | 🟡 Nick | C2PA contrib member CONFIRMED (docusign 7C9592DB); badge on councilof.ai live |

---

## 4. Counsel agenda — 11th session

1. **Measurement/fix separation doctrine** — confirm the no-fee, no-equity, no-ownership structure survives outside scrutiny. Published methodology. Arm's-length ranking. Separate beneficial ownership of any fix entity.
2. **Unsolicited-measurement policy** (Moody's structural borrowing) — if we measure an AI system without the provider's consent and publish the card, what's the liability? Held as counsel question.
3. **Analyst-commercial separation** (Moody's borrowing) — structural firebreak between the measurement analysts and any commercial team. Held as counsel question; draft commitment ready.
4. **Human-vs-AI axis** — scope: are we measuring human decision-makers the same way we measure AI? What does the board show? Counsel to advise on GDPR/employment-law implications.
5. **GSPC leader reconciliation** (F17) — measurement body cannot publish a leader its harness no longer reproduces. Options: annotate as documented experiment, or correct the public API. Counsel to advise on regulatory/reputational risk of leaving uncorrected.
6. **DEFONEOS hard stops refresh** — confirm kinetic-targeting/personal-surveillance red lines are current. No new compartments.

---

## 5. Build lane — today's wave

### Deployed / verified live
| Item | State |
|------|-------|
| csoai.org → 301 → councilof.ai | ✅ Live. Apex + www + all subpaths (except /mcp) redirect 301. MCP endpoint preserved. |
| B2: "30 frameworks" → "13 frameworks" public lock | ✅ Fixed in canonCounters + committed |
| N9: nav flex-nowrap CSS (vertical-letter collapse bug) | ✅ Fixed in Header.tsx + committed |
| C2PA/OIN/LOT membership badges on councilof.ai | ✅ EnterpriseTrust — C2PA + OIN confirmed; LOT "application submitted" (honest) |
| N2: canonical /gspc-scoreboard route | ✅ 62KB signed table in client/public + deploy list + sitemap + nav link |
| Sigil brand-gate: 6 pages cleaned | ✅ Display text replaced with "signed record/attestation" |
| CEASAI brand-gate: eu-ai-act-urgency | ✅ Replaced with "CSOAI Ltd" |
| Brand-gate exclusions: ai-transparency/authority/badges | ✅ Audit pages exempted (legitimate route/code-example rendering) |

### Pushing now (CI running — master ea3f9a5)
- **NewHome-v3 preview** at /home-v3 — 7-section restructured homepage: scroll hero, 4-buyer cards, 13-axis grid, 7 industries, arena strip, 6-blog strip, 3-upsell CTAs, FAQ AEO schema. Full white/green brand. Live route `/home-v3` — NOT yet swapped for `/` (awaiting review).
- All above fixes flow through the same deploy pipeline. CI running as of 08:20 UTC.

### Queued (lane-executable, next push)
| N-item | Task | Effort |
|--------|------|--------|
| N3 | Real 404s — kill SPA catch-all for /api/* (serve 404 JSON) | Medium |
| N8 | Fix "undefined servers live" JS hole in sov-space arena | Small |
| N11 | csoai.org/.well-known/mcp.json content-type → application/json | Fixed by redirect? Verify |
| — | Remediation-partners directory page | Small (one page, declares the architecture) |
| — | Swap / route to NewHomeV3 after review | 1 line |
| M1 | Playwright gate suite on 3090 pod | Written, awaiting pod run |

### RunPod posture
**Additive, never purge.** Current fleet:
- 3090 (194.26.196.156:12853) — hosts csoai-static-deploy2 dev workspace
- A100-main (1dldzposn7ssuu) — /workspace/jeeves-exec runtime
- Oracle micro1 + micro2 — sov33-owem / fleet lanes
- Mac = terminal only (disk critical). All dev/compute on pods.

Nothing is deleted. New workstreams get new pods.

---

## 6. Gated list (K3 board items blocked on owner action)

| B# | Item | Owner gate |
|----|------|------------|
| B1 | csoai.org apex breaches | ✅ FIXED (redirect) |
| B2 | "30 frameworks" on homepage | ✅ FIXED (13) |
| B3 | GSPC API leader vs harness | 🔴 G6 above |
| B4 | CF robots contradiction | 🟡 G4 above |
| B5 | paper-district dark + www 402 | 🟢 Lane-executable (restore from remote) |
| B6 | Soft-404 catch-alls | 🟢 N3 above |
| B7 | 23+ SOV URLs | 🔴 G5 above |
| B14 | gdrive dead + A100 dead + micro2 97% | 🟡 G8 above |
| B15 | No H1 in raw HTML key routes | 🟢 Prerender fix (N10) |
| B16 | Two-signer attribution | 🟡 G7 above |

---

## 7. Standing red lines (unchanged)

- Care floor 0.95 — never autonomously publish, send, or spend
- Measurement credentials, never certification
- UNMEASURED cells shown honestly — never zero
- No fee, kickback, or equity from ranked fixers
- No fabricated architecture specifics — every number traces to a signed artefact
- Mac = terminal only. All heavy work on RunPod/Oracle pods. Additive, never delete.
- DEFONEOS hard stops (kinetic, surveillance, DAIC/AUKUS claims, defonos.io)
- OIN scope check mandatory before any patent filing
- Internal engine codenames (SOV3, JEEVES, Hermes, Liquid-KAN, etc.) NEVER on public surfaces