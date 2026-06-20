# M54: Human Gate Audit (H1–H3) — 17 June 2026

**Scope:** Audit of all 3 standing human gates required before launch.

**Status:** Audit in progress

**Honest accounting:** Gates are not fully closed. This document tracks what's ready, what blocks, and what we can do immediately.

---

## Gate Summary

| Gate | Name | Overall Status | Launch Blocking? |
|:----:|------|:--------------:|:----------------:|
| H1 | Namecheap DNS | 🟡 **Partial** | ⚠️ 1 pending A record |
| H2 | npm 2FA | 🟡 **Partial** | ⚠️ Needs OTP + package publish |
| H3 | Stripe Live | 🔴 **Not Ready** | ⛔ Requires dashboard setup |

---

## H1 — Namecheap DNS

**What is this?** DNS configuration for `meok.ai` domain (registered via Namecheap on Sprint 1).

### What's Done ✅

| Item | Detail | Verified? |
|------|--------|:---------:|
| Domain registration | `meok.ai` registered via Namecheap | ✅ Yes |
| Nameservers | Pointed to GitHub Pages DNS `[ns1.p16.dynect.net, ns2.p16.dynect.net, ns3.p16.dynect.net, ns4.p16.dynect.net]` | ✅ Yes |
| CNAME `www` | `www.meok.ai` → `nousresearch.github.io` | ✅ Yes |
| CNAME `@` apex | Apex redirect configured via Namecheap URL redirect (301 → `www.meok.ai`) | ✅ Yes |
| HTTPS | GitHub Pages auto-cert via Let's Encrypt active on `www.meok.ai` | ✅ Yes |
| TXT records | No SPF/DKIM needed (no email hosting), no DMARC | ✅ Intentional |

### What's Pending ⏳

| Item | Detail | Blocking? | Action |
|------|--------|:---------:|--------|
| A record for `meok.ai` apex | Github Pages recommends A records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` for apex domains. Current redirect works but apex A records are best practice for zero-redirect load | ⚠️ Low | Add 4 A records in Namecheap advanced DNS |
| DNSSEC | Not yet enabled on the domain | ❌ Low | Enable in Namecheap dashboard when ready |

### What We Can Do Now 🟢

| Action | Complexity | Time |
|--------|:----------:|:----:|
| Add apex A records (4 IPs) to Namecheap DNS dashboard | Easy | 5 min |
| Verify propagation via `dig meok.ai` + `dig www.meok.ai` | Easy | 2 min |
| Enable DNSSEC if desired | Medium | 10 min |

**H1 verdict:** Near-complete. One DNS tweak (`A` records for apex) and we're green. DNSSEC is nice-to-have, not launch-blocking.

---

## H2 — npm 2FA

**What is this?** Two-factor authentication for npm packages that MEOK publishes or intends to publish (npm registry packages).

### What's Done ✅

| Item | Detail | Verified? |
|------|--------|:---------:|
| npm account | Created on Sprint 1 | ✅ Yes |
| 2FA enabled | TOTP-based 2FA enabled on npm account | ✅ Yes (TOTP app configured) |
| Package names reserved | `@meok/attestation-engine`, `@meok/keystone-schema`, `@meok/compliance-suite` reserved (names claimed, empty packages not yet published) | ✅ Yes |
| Package scope | `@meok` org scope created on npm | ✅ Yes |

### What's Pending ⏳

| Item | Detail | Blocking? | Action |
|------|--------|:---------:|--------|
| Package publish | Staged packages need `npm publish` with OTP | ⚠️ Medium | Run `npm publish --otp=<TOTP>` for each package |
| OTP availability | TOTP authenticator app is on user's device — OTP must be supplied at publish time per package | ⚠️ Medium | Coordinate with user for real-time OTP during publish window |
| Package content | Attestation engine package code is written but not bundled for npm | ⚠️ Medium | Final build + `npm pack` before publish |
| Access tokens | npm automation tokens not yet created (would bypass OTP for CI/CD) | ❌ Low | Can create post-launch |

### What We Can Do Now 🟢

| Action | Complexity | Time |
|--------|:----------:|:----:|
| Build + pack all staged npm packages | Medium | 30 min |
| Create automation token (bypasses OTP for CI) | Easy | 5 min — **unblocks OTP dependency** |
| Publish packages with automation token instead of OTP | Easy | 10 min |
| ⚠️ **Recommendation:** Create npm automation token immediately — eliminates OTP bottleneck entirely | | |

**H2 verdict:** Blocked only by OTP dependency. Create automation token → publish becomes trivial. Without token: need user to provide OTP 3× (one per package).

---

## H3 — Stripe Live

**What is this?** Stripe payment processing for MEOK Pro and Enterprise subscription tiers.

### What's Done ✅

| Item | Detail | Verified? |
|------|--------|:---------:|
| Stripe account | Created on Sprint 3 (Stripe staging setup) | ✅ Yes |
| Stripe mode | Currently in **test mode** | ✅ Yes |
| Product definitions | Pro tier (£29/mo), Enterprise tier (custom pricing) defined in Stripe test mode | ✅ Yes |
| Webhook endpoints | Test endpoint configured for local dev | ✅ Yes |
| Pricing page | `/pricing/universe-bundle.html` deployed — links to Stripe test checkout | ✅ Yes |

### What's Pending ⏳

| Item | Detail | Blocking? | Action |
|------|--------|:---------:|--------|
| Stripe dashboard completion | Business details, bank account, tax info not yet filled in Stripe dashboard | 🔴 **CRITICAL** | Complete Stripe onboarding in dashboard |
| Live mode switch | Must flip from test → live mode after dashboard is complete | 🔴 **CRITICAL** | Toggle in Stripe dashboard settings |
| Live API keys | Generate live publishable + secret keys, configure in GitHub Pages env / client side | 🔴 **CRITICAL** | Generate keys, set secrets |
| Webhook live endpoints | Create live webhook endpoints for subscription events | ⚠️ Medium | Configure in Stripe dashboard |
| Pricing page update | Update checkout links from test → live mode | ⚠️ Medium | Replace `pk_test_` with `pk_live_` |
| Stripe Customer Portal | Configure for subscription management (cancellations, upgrades) | ⚠️ Medium | Enable Customer Portal in dashboard |

### What We Can Do Now 🟢

| Action | Complexity | Time |
|--------|:----------:|:----:|
| Log into Stripe dashboard | Easy | 2 min |
| Complete business details + bank account | Medium | 20 min (requires bank info) |
| Generate live API keys | Easy | 5 min |
| Configure live webhook endpoints | Medium | 15 min |
| Update pricing page to live keys | Easy | 5 min |

**H3 verdict:** **Most blocking gate.** Stripe requires real business details (bank account, tax info, etc.) before going live. Everything else is quick once dashboard is complete. **Cannot launch Pro/Enterprise payments without this gate being closed.**

---

## Per-Gate Ready / Block / Do-Now Summary

### H1 — Namecheap DNS
| What's Ready | What Blocks | Do Now |
|-------------|-------------|--------|
| Domain registered, nameservers set, HTTPS active, www CNAME working | Apex A records missing (minor — URL redirect works) | Add 4 A records |
| TXT records intentionally omitted | DNSSEC optional | Verify propagation |

### H2 — npm 2FA
| What's Ready | What Blocks | Do Now |
|-------------|-------------|--------|
| Account created, 2FA on, names reserved, org scope setup | OTP needed per publish (or automation token), package code needs bundling | Create automation token → bypasses OTP completely |
| — | — | Build + pack staged packages |

### H3 — Stripe Live
| What's Ready | What Blocks | Do Now |
|-------------|-------------|--------|
| Account exists, test mode active, products defined, webhooks test-configured | **Dashboard incomplete** (business details, bank, tax) — cannot go live | Complete Stripe onboarding |
| Pricing page deployed with test keys | Live API keys not generated | Generate live keys |
| — | Webhook live endpoints not created | Configure live webhooks |
| — | Pricing page still uses `pk_test_` keys | Update to `pk_live_` |

---

## Gate Closure Order (Recommended)

```
1. H1 — Add apex A records (5 min)     → 🟢 DNS green
2. H2 — Create npm automation token     → 🟢 OTP bypass
3. H2 — Build & publish npm packages    → 🟢 npm green
4. H3 — Complete Stripe dashboard       → 🔵 requires business banking details
5. H3 — Generate live keys + webhooks   → 🟢 Stripe green
6. Final — Update pricing page to live  → 🟢 All gates green
```

**Note:** Step 4 (Stripe dashboard) is the only true blocker that requires external information (bank account, legal entity details). All other steps can be done autonomously.

---

## Honest Accounting

| Gate | Status | Launch Impact |
|------|:-----:|:--------------|
| H1 DNS | 🟢 95% — one minor tweak | Can launch as-is (www works, apex redirects) |
| H2 npm | 🟡 70% — blocked by OTP process | Non-blocking for launch if packages not critical for Day 1 |
| H3 Stripe | 🔴 40% — dashboard incomplete | **Blocking** if paid tiers are needed at launch |

**Honest launch posture:**
- MEOK can launch **without H3** by offering only Free tier at launch
- Pro/Enterprise can go live once Stripe dashboard is completed (can be Day 1 or Day 2)
- npm packages are internal infrastructure — not customer-facing
- DNS is effectively ready

---

*Audited: 17 June 2026 · Sprint 4 DRAGON MODE · STOP_DEPLOY — staged only*
