# Live Website Test — CSOAI / Council + MEOK

**Tested:** 12 August 2026  
**Scope:** `csoai.org`, `councilof.ai`, `meok.ai`, `os.meok.ai`, plus a spot-check of `proofof.ai` because it is publicly live and affects brand trust.  
**Method:** rendered-browser tests, unauthenticated route checks, API probes, sitemap crawl, metadata/header inspection, response-time sampling, and independent Ed25519 verification of the signed assessment result.

---

## 1. Executive verdict

**The sites have the right soul. They do not yet have the right plumbing.**

The strongest surfaces already express the correct company:

- **Council / CSOAI:** “Measured, not modelled.” Deterministic instruments, signed assessments, published refutations, explicit AI-surface disclosure.
- **MEOK:** warm consumer sovereign-AI positioning, local-first privacy language, honest arena caveats, clear separation between measurement and certification.

But the public estate is not yet ready for regulator, insurer, or investor traffic because several first-click journeys fail or contradict the trust doctrine:

1. `csoai.org` is not currently a second website. Every tested path 301s to the **Council homepage**, destroying the old site’s route equity.
2. Demo login, registration, newsletter storage, and MEOK checkout are not production-wired.
3. Public unauthenticated browsers can render admin/dashboard/billing-style surfaces.
4. Several “LIVE” metrics are not backed by reachable public evidence at test time.
5. The unparsed-answer doctrine contradicts itself between `/api/gspc` and the SOV OS method panel.
6. Both major sites have canonical, favicon, manifest, security-header, and performance hygiene issues.
7. MEOK’s local-first claim needs scoping once cloud chat/premium models are involved.
8. `proofof.ai` is live with older, more aggressive SOV4 claims and a dead “Get Started” CTA; it now conflicts with the more mature measurement register.

**Recommended target shape:**

- `councilof.ai` = enterprise / regulator / measurement trust machine.
- `meok.ai` = consumer sovereign OS.
- `csoai.org` = temporary path-preserving redirect to Council, until a separate corporate site is genuinely needed.
- `proofof.ai` = redirect to the current benchmark/trust pages or clearly archived as historical.

---

## 2. What is genuinely working

| Surface | Result | Why it matters |
|---|---:|---|
| Council homepage | PASS | Clear, differentiated, professional: deterministic rule-based instrument, no fake AI claim, strong “Measured, not modelled” positioning. |
| Sovereign Console on homepage | PASS | Sample employment prompt returned Annex III employment classification with explicit limitations. |
| Free AI Risk Check | PASS after required controls are selected | Produced HIGH_RISK Annex III employment verdict, report ID, Ed25519 signature, gaps, and legal caveat. |
| Assessment signature | PASS with documentation caveat | Independent verification succeeded when `sig` was decoded as hex. The public verification instructions should state that encoding explicitly. |
| SOV OS board | PASS with doctrine caveat | Excellent “no score until measured” presentation; 3/12 measured, 1 interval, signed/recomputable framing. |
| GSPC benchmarks | PASS | Strong measurement culture: intervals, usable-n floor, dead-item analysis, grader agreement, non-claims. |
| AI transparency page | PASS | Exactly the kind of Article 50 surface classification competitors are not doing. |
| Refutation ledger | PASS with count-sync issue | Strong trust asset; page says 9 entries while public stats endpoint reports 7 refutations out of 13 total records. |
| Council contact page | PASS | Honest mailto flow; no silent backend, no hidden storage. |
| MEOK homepage | PASS | Strong consumer explanation: one memory, any model, SOVOS substrate, CSOAI provenance. |
| MEOK privacy page | PASS with claim-scope caveat | Good UK GDPR structure and clear rights language. |
| MEOK arena | PASS | Exceptional honesty register: ready / not ready / owed / owner-gated cells are exactly right. |
| MEOK governance page | PASS | The 1.00 result is correctly caveated as internal consistency, not third-party validity. |
| MEOK sitemap | PASS | 34/34 sitemap URLs returned 200. |

---

## 3. P0 failures — fix before any serious external push

### 3.1 The two CSOAI domains are not two websites

**Observed:**

- `https://csoai.org` → 301 → `https://councilof.ai/`
- `https://csoai.org/about` → 301 → `https://councilof.ai/`
- `https://csoai.org/pricing` → 301 → `https://councilof.ai/`

That is path-collapsing, not a proper migration. It throws away every old URL and makes the sitemap misleading.

**Required fix:**

- Either keep one canonical site and use **path-preserving redirects**:
  - `csoai.org/about` → `councilof.ai/about`
  - `csoai.org/pricing` → `councilof.ai/pricing`
  - `csoai.org/assess` → `councilof.ai/assess`
- Or make `csoai.org` a genuinely separate corporate/trust site.

**Recommendation tonight:** one canonical product site on `councilof.ai`; path-preserve every old CSOAI route.

---

### 3.2 Canonical and duplicate-host conflict

**Observed on Council:**

- Page canonical says `https://csoai.org` while the served site is `councilof.ai`.
- `www.councilof.ai` returns 200 instead of redirecting to apex.
- Sitemap contains 351 `csoai.org` URLs.
- 347 sitemap URLs return 200 after redirects; 4 MCP endpoints return 405.

**Observed on MEOK:**

- Homepage canonical is `https://meok.ai/index.html` while final URL is `/`.
- Several pages canonicalise to `.html` while the final served route is extensionless.
- `www.meok.ai` and `os.meok.ai` both return the same public homepage shell.
- `www.meok.ai/sitemap.xml` returned 402 in the spot check.

**Required fix:**

- One canonical host per brand.
- Redirect `www` → apex.
- Canonical must equal the final served URL.
- Regenerate sitemap after redirect policy is fixed.
- Keep API/backend on a distinct route or subdomain that does not serve the marketing shell at `/`.

---

### 3.3 Authentication and demo login are broken

**Observed:**

- Council `/login` renders correctly.
- “Demo Login (No Password Required)” calls `POST /api/auth/login`.
- Server response: **405 Method Not Allowed**.
- Direct `POST /api/auth/register` also returns **405**.
- Direct GETs to auth API paths return the SPA HTML instead of JSON.

**Required fix:**

- Wire the auth endpoints or remove/hide the buttons.
- Demo login must either:
  - create a signed read-only demo session, or
  - route to a clearly labelled static demo.
- API paths must never fall through to the SPA HTML.

---

### 3.4 Newsletter capture is not storing anything

**Observed:**

`POST /api/subscribe` with a syntactically valid test address returned:

```json
{
  "ok": true,
  "stored": false,
  "reason": "no datastore bound yet",
  "fallback": "email nicholas@csoai.org"
}
```

**Why it matters:** this leaks every high-intent visitor at the exact moment the site is asking for trust.

**Required fix:** bind the datastore or replace the form with an explicit mailto until storage exists. Do not show “Subscribe” as if persistence works.

---

### 3.5 Public admin-style surfaces

**Observed in a fresh unauthenticated browser:**

- `/assess` renders a dashboard sidebar labelled “Admin User”.
- `/admin` renders an Admin Dashboard.
- `/dashboard` renders a Dashboard.
- `/settings/billing` renders Billing & Subscription.

These may be mock/static surfaces, but a regulator, insurer, or security researcher will not read them that way.

**Required fix:**

- Gate every app surface behind auth.
- If the data is mock, label the route `/demo-admin` and make the demo state impossible to confuse with a live admin session.
- Public assessment should not render the admin chrome.

---

### 3.6 Live-status honesty failures

**Observed on Council `/os`:**

- Page displays “LIVE”, `1.45B+ signed episodes`, `0 governed crimes`, `121M+ ungoverned`.
- `/flywheel-snapshot.json` returns the SPA HTML shell, not JSON.
- The page still presents the figures as live.

**Observed on MEOK / Sovereign backend:**

- `GET https://os.meok.ai/api/health` returns healthy metadata.
- `POST /api/chat` with a real question returned:

```json
{"response":"I’m here — my deeper voice hiccuped, try once more.","model":"offline"}
```

So the backend is reachable, but the model surface was offline at test time.

**Required fix:**

- Introduce one shared `STATUS.json`: `live`, `partial`, `offline`, `unmeasured`.
- No hard-coded “LIVE” unless the source endpoint returns valid data.
- If the model is offline, the page must say “Sovereign backend reachable; model offline” — not imply a live governed brain.
- Large counters need evidence links or must be hidden.

---

### 3.7 Measurement doctrine contradiction: unparsed answers

**Observed:**

- SOV OS method panel says: **“Unparsed counted incorrect.”**
- `/api/gspc` note says unparsed responses are **“reported as UNMEASURED, never scored as a wrong answer.”**

These cannot both be canon.

**Required fix:** choose one doctrine and propagate it everywhere:

- If unparsed = incorrect, remove the API note.
- If unparsed = unmeasured, change SOV OS method and benchmark language.

Given the current trust posture, the safer doctrine is:

> Unparsed responses are excluded from accuracy denominators and reported separately as UNMEASURED; they are never silently dropped and never silently scored as wrong.

If the actual harness already counts them incorrect, publish that instead — but only one version may live.

---

### 3.8 Broken public links and files

**Observed:**

- Council footer link `/insurance` → Page Not Found.
- Council footer link `/framework-crosswalk` → Page Not Found.
- Council `/favicon.ico` returns HTML, not an icon.
- MEOK `/favicon.ico` returns HTML.
- MEOK `/manifest.json` returns HTML.
- ProofOf `/favicon.ico` returns HTML.
- ProofOf “Get Started” CTA is `#`.

**Required fix:** add these to deploy-blocking smoke tests.

---

## 4. P1 issues — fix this week

### 4.1 Security headers

Both Council and MEOK are missing important baseline headers:

- `Strict-Transport-Security`
- `Content-Security-Policy`
- consistent `X-Frame-Options` / `frame-ancestors`

Council has `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and a permissions policy; MEOK has `nosniff` only.

**Required:** deploy a shared security-header policy across every domain.

---

### 4.2 Performance and caching

**Council observed:**

- HTML shell ≈ 10.5 KB.
- Main JS ≈ 1.29 MB.
- CSS ≈ 375 KB.
- Homepage median response ≈ 1.31 s in repeated requests.
- Main JS median ≈ 2.46 s; max observed 6.34 s.
- Hashed JS/CSS only `max-age=14400`.

**MEOK observed:**

- `/os` HTML ≈ 309.6 KB.
- `/os` median response ≈ 2.51 s.
- `/arena` median ≈ 2.86 s.
- Pages are served `max-age=0, must-revalidate`.

**Required:**

- Long-cache immutable hashed assets.
- Split Council JS further by route.
- Compress and cache static MEOK pages at the edge where safe.
- Add a public status/performance page if “LIVE” remains part of the pitch.

---

### 4.3 Accessibility and form hygiene

**Council:**

- Login password fields warn about missing `autocomplete="current-password"`.
- Assessment text inputs rely on placeholders without accessible labels.
- SOV OS has many icon-only buttons with no accessible names.
- Some empty links remain.

**MEOK:**

- OS uses many clickable divs/spans rather than semantic buttons/links.
- Canvas/app surfaces need keyboard focus order and ARIA naming.
- Voice/camera flows need explicit permission states and fallback text.

**Required:** semantic controls, labels, focus states, and a keyboard path through the main flows.

---

### 4.4 Claim scope: MEOK local-first

MEOK’s strongest claim — “your data stays on your device” — is true only when the route is genuinely local.

It is not safely true as a blanket claim when:

- premium cloud models are used,
- moderation calls post to `/api/chat`,
- cross-device sync exists,
- benchmark opt-ins are retained.

**Required wording:**

> Free/local mode keeps memory and preferences on your device. Premium model calls, sync, and opt-in benchmark contributions are disclosed per surface before data leaves the device.

That preserves the claim without creating a privacy contradiction.

---

### 4.5 Pricing truth states

**Council pricing:** strong structure, but some listed capabilities need REAL / PoC / planned labels.

**MEOK pricing:** “Get Pro” and “Add credit” are honest once clicked, but the checkout APIs report:

- Pro: Stripe account cannot currently make live charges.
- PAYG: no price configured.

**Required:** label those CTAs “Join waitlist” or “Stripe test mode” until live payment works.

---

## 5. Brand-alignment ruling

### The good news

The two-site split makes sense:

| Brand | Role | Tone |
|---|---|---|
| Council / CSOAI | regulator, insurer, enterprise, measurement authority | austere, evidentiary, deterministic |
| MEOK | consumer/family sovereign AI | warm, personal, local-first, companion OS |

That is a clean brand ladder.

### The current problem

The estate does not yet speak with one measurement dictionary:

- Council says 417 provisions / 4 lenses / 3 of 12 axes measured.
- Benchmarks discuss 6-axis GSPC results.
- MEOK arena discusses 12 greenfields and older SOV33/SOVBENCH artifacts.
- MEOK pricing mentions a “13-queen council.”
- ProofOf markets “SOV4” with “ties frontier”, “beats them on governance”, “100×”, and `1.000 DORADO`.
- CSOAI’s own current doctrine would require those claims to be scoped, intervalled, or removed.

### Required artifact: one public doctrine file

Create a shared `PUBLIC_DOCTRINE.json` consumed by both sites:

```json
{
  "company": "CSOAI LTD",
  "company_number": "16939677",
  "canonical_measurement_site": "https://councilof.ai",
  "consumer_site": "https://meok.ai",
  "axes_measured": 3,
  "axes_total": 12,
  "axes_with_intervals": 1,
  "unparsed_policy": "reported_separately_as_unmeasured",
  "status_vocabulary": ["LIVE", "PARTIAL", "OFFLINE", "UNMEASURED", "DRAFT", "POC"],
  "forbidden_claims": [
    "state_of_the_art_without_external_held_out_eval",
    "certification_or_conformity_assessment",
    "partnership_without_signed_relationship",
    "live_when_source_endpoint_is_offline"
  ]
}
```

Every page renders from that file. No more drift.

---

## 6. What each site needs to achieve the target state

### Council / CSOAI must become the trust machine

Keep:

- Homepage positioning.
- Free signed risk check.
- Instrument / benchmarks / SOV OS.
- Refutation ledger.
- AI transparency registry.
- Trust center.

Fix:

1. Path-preserving CSOAI redirects.
2. Canonical + sitemap regeneration.
3. Auth/demo/register endpoints.
4. Newsletter datastore.
5. Admin/dashboard gate.
6. Footer 404s.
7. Live-status source validation.
8. Unparsed doctrine sync.
9. Favicon/manifest/security headers.
10. Public signature-verification example with `sig` encoding stated.

### MEOK must become the consumer doorway

Keep:

- Warm homepage.
- Privacy posture.
- Arena honesty.
- OS demo shell.
- Local-first free mode.

Fix:

1. Scope local-first claims by mode.
2. Show model/backend status honestly.
3. Replace dead payment CTAs with waitlist/test-mode labels until Stripe is live.
4. Canonical cleanup (`/index.html`, `.html` vs extensionless).
5. Separate `www`, apex, and `os.` roles.
6. Fix manifest/favicon.
7. Align “council”, “SOV4”, “SOV33”, “SOVEREIGN”, and “SOVOS” naming.
8. Link governance surfaces to the current Council GSPC pages, not the old CSOAI root.
9. Make premium-model data flow explicit before the user sends anything.
10. Add the same smoke-test CI as Council.

---

## 7. The exact 3 moves tonight

### Move 1 — Canonical domain repair

- `csoai.org/*` → `councilof.ai/$1`
- `www.councilof.ai` → `councilof.ai`
- `www.meok.ai` → `meok.ai`
- Regenerate sitemaps and canonical tags.
- Fix favicon and manifest routes.

### Move 2 — Truth-state repair

Either wire or relabel:

- Demo login / register
- Newsletter subscribe
- MEOK Pro checkout
- Sovereign chat
- “LIVE” counters
- Public admin surfaces

No broken CTA may look production-ready.

### Move 3 — Doctrine sync

Publish one shared doctrine file and update:

- unparsed policy,
- measured-axis counts,
- ledger counts,
- status vocabulary,
- forbidden claims,
- cross-brand links.

---

## 8. Final ruling

**REAL:** the trust architecture is visible. The measurement pages, signed assessment, transparency registry, and MEOK arena caveats are genuinely differentiated.

**NEEDS FIX:** the public estate does not yet meet its own standard. The broken auth, subscription storage, path-collapsing redirects, public admin chrome, and unsupported live labels are exactly the sort of thing the site’s own refutation doctrine would catch.

**KILLED:** the idea that “both CSOAI sites” currently exist as separate assets. They do not. `csoai.org` is a redirect to Council.

**The dragon move:** make Council the austere evidence machine and MEOK the warm consumer doorway — then bolt both to the same doctrine, status, and measurement files. That is how the estate starts looking like one organism instead of several promising lanes.
