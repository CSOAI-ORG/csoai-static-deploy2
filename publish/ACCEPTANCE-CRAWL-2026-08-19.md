# ACCEPTANCE CRAWL — 19 Aug 2026 (move 6 + move 74, weekly battery)

**Verdict: SOFT-404 CONFIRMED ON csoai.org → councilof.ai CHAIN — root cause is a ZONE-LEVEL 308 wildcard, NOT an edge-cache artifact and NOT a regression in the `_site` build.**

## What was tested (fresh fetches, cache-busted `?x=$(date +%s)`, 19 Aug 03:32 UTC)

| Probe | Result |
|---|---|
| `csoai.org/zzz-nope` (no query) | `308` → `Location: https://councilof.ai/zzz-nope` |
| `csoai.org/zzz-nope?x=…` | `308` → `Location: https://councilof.ai/zzz-nope?x=…` |
| `csoai.org/` root | `308` → `https://councilof.ai/` |
| `csoai.org/gspc-scoreboard.html` | `308` → `https://councilof.ai/gspc-scoreboard.html` |
| `www.csoai.org/*` | `308` → `https://councilof.ai/:splat` (www CNAMEs to csoai-site.pages.dev but the 308 fires first) |
| `councilof.ai/zzz-nope` | `200` — 11,242 B Vite SPA shell, `<title>CSOAI — the independent measurement body for AI` (soft-404) |
| `councilof.ai/gspc-scoreboard` | `200` — real page ("Council Scoreboard — 13 axes × 19 models") |
| `councilof.ai/benchmarks` | `200` — real page ("GSPC Benchmarks — CSOAI measurement instrument") |
| `49ac2784-d596-…csoai-site.pages.dev/zzz-nope` | `404` — CORRECT (my build's real 404, "Not found — Council of AI") |

## Root cause (verified at the API level)

1. **The `csoai.org` zone is NOT in this Cloudflare account.** `GET /zones?name=csoai.org` → status `moved` (zone deleted/transferred out; modified 2026-08-18T17:11:22Z). Its name servers at the registrar are `dns1/2.registrar-servers.com` (Namecheap), apex A records point at Cloudflare anycast IPs (`172.66.44.153` / `172.66.47.103`).
2. A **zone-level wildcard redirect `/* → https://councilof.ai/:splat 308`** answers every csoai.org hostname (apex AND www) before any Pages project can serve. It is NOT in `_redirects` (the repo file has no wildcard — it was deliberately removed 2026-08-12 as an SEO/AEO hazard; the deployed `_redirects` matches).
3. `councilof.ai` is the **councilof-ai Vite SPA** (`wrangler.jsonc` name `csoai`, `pages_build_output_dir: ./dist/client`, `/* /index.html 200` catch-all in `public/_redirects`) — so **every unknown path answers 200 with the SPA shell** (soft-404).
4. The Pages project `csoai-site` has custom domain `csoai.org` attached, but the zone-level 308 pre-empts it. The `www.csoai.org` CNAME → `csoai-site.pages.dev` is also pre-empted.

## Verdict

- **NOT an edge-cache staleness issue.** Cache-busted fetches behave identically to plain fetches.
- **NOT a regression in the `_site` build.** The latest deployment (`49ac2784`) serves the correct 404 and all real pages on the Pages domain.
- The **csoai.org custom domain currently funnels EVERY path (including unknown ones) into the councilof.ai SPA shell**, which answers 200 for all of them. This is exactly the hazard the 2026-08-12 `_redirects` note documented ("456 pack URLs were funnelling into an unrelated shell page").
- Where the wildcard lives is outside this account's control: the `csoai.org` zone is `moved` out (owner: the account that now holds it — likely Nick's other Cloudflare account or the councilof-ai lane). Only that owner can remove/scope the zone-level rule.

## Actions

- [ ] **OWNER (Nick):** find which Cloudflare account now holds `csoai.org` and decide: (a) remove the zone-level wildcard so csoai.org serves the Pages project again (recommended — restores real 404s + the signed board), or (b) keep the wholesale consolidation and instead fix councilof.ai's soft-404 (`/* /index.html 200` → real 404 handling in the councilof-ai repo).
- [ ] **councilof-ai lane:** if (b), add a true 404 (SPA route + status) so unknown paths stop returning 200.
- [ ] This lane: keep `csoai-site` Pages deployment as the canonical static build (real 404 verified); re-run the battery weekly; re-check after the owner decision.

## Evidence

- DNS: `dig csoai.org NS` → `dns1/2.registrar-servers.com`; `dig www.csoai.org CNAME` → `csoai-site.pages.dev`.
- API: zone `544bbc7ffd86343598a5f69056aaf5ac` status `moved`; Pages project `csoai-site` latest deployment `49ac2784-d596-4856-8cbc-8e77c8222b62`.
- Live chain: `csoai.org/zzz-nope` → `308 https://councilof.ai/zzz-nope` → `200` shell (11,242 B).
