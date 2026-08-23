# Monday GitHub Inventory — CSOAI / Council of AI

**As of:** Sun 23 Aug 2026, ~18:22 BST (17:22 UTC)  
**Executor:** overnight inventory (read-only `gh` API)  
**Auth path:** Nick’s machine `gh` (keyring) — box has no `GH_TOKEN` / no `gh auth`  
**Login confirmed:** `gh api user` → **CSOAI-ORG** (id `260596236`, name Nicholas Templeman, **type: User** — not an Organization account)

**CEO locks (doctrine, not certifying live chrome):** public chrome = **13 measured + jail floor + unnamed slot-15**; **never certify**; **SOVOS internal**.

---

## 0. API / account notes (honest)

| Finding | Detail |
|--------|--------|
| Box `gh` | **Unauthenticated** (`gh auth login` required / no `GH_TOKEN`) |
| Host `gh` | Logged in as **CSOAI-ORG** (scopes: `gist`, `read:org`, `repo`, `workflow`) |
| `GET /orgs/CSOAI-ORG/repos` | **HTTP 404 Not Found** — namespace is a **User**, not a GitHub Organization |
| Membership orgs visible | `c2pa-org`, `CSGA-GLOBAL` (via `user/orgs`) |
| Search `org:CSOAI-ORG` | Works for issue/PR search over owned repos (516 open PRs total, mostly Dependabot) |
| Vercel commit statuses on master tip | **Account is blocked** (`Vercel – csoai-v2-app`, `Vercel – councilof-ai-src`) |
| No clone | Inventory used network API only |

---

## 1. LIVE leftovers (open non-Dependabot on focus repos)

### councilof-ai (5 open)

| # | Title | Updated (UTC) | Updated (BST) | Draft | Mergeable | State |
|---|-------|---------------|---------------|-------|-----------|-------|
| **397** | feat(aeo): per-axis Zenodo DOIs in GSPC dataset JSON-LD (D70) | 2026-08-23T17:04:11Z | 18:04 BST | no | true | **unstable** |
| **394** | feat(api): /api/comparison — MEASURED vs REPORTED surface (never fused) | 2026-08-23T16:33:51Z | 17:33 BST | no | true | **unstable** |
| **396** | fix(api): /api/dorado market rail — fetch static snapshot at request time | 2026-08-23T16:29:06Z | 17:29 BST | no | true | **unstable** |
| **387** | feat(council-os): Benchmarks tab — signed arena Elo + benchmark-quality register | 2026-08-23T15:42:07Z | 16:42 BST | no | true | **unstable** |
| **367** | One public OS door: restore App.tsx, revert #365 iframe, send every guess to Council OS | 2026-08-23T14:03:52Z | 15:03 BST | no | **false** | **dirty** (conflicts) |

Links:  
https://github.com/CSOAI-ORG/councilof-ai/pull/397 · 394 · 396 · 387 · 367

### csoai-static-deploy2 (2 open)

| # | Title | Updated (UTC) | Draft | Mergeable | State |
|---|-------|---------------|-------|-----------|-------|
| **34** | fix(gspc-mcp): honest tool descriptions — measure returns a contract, verify is card-family scoped | 2026-08-20T04:19:26Z | no | true | **clean** |
| **29** | feat: add csoai-gspc-mcp worker with public initialize | 2026-08-18T02:58:04Z | **yes** | null | unknown |

### .github (4 open) — hygiene / docs / OS plan

| # | Title | Updated (UTC) | Draft | Mergeable | State |
|---|-------|---------------|-------|-----------|-------|
| **8** | feat: Council OS engines + site patches + CI + phased execution (P1–P4) | 2026-08-23T15:43:39Z | **yes** | true | clean |
| **9** | docs: STEPS_100 owner deploy gate status (11/14 e2e) | 2026-08-23T15:20:15Z | **yes** | **false** | **dirty** |
| **7** | docs: next-week growth + moat plan (Article 50 tailwind + receipt interop) | 2026-08-23T13:57:32Z | **yes** | true | clean |
| **6** | docs: add AGENTS.md with Cursor Cloud dev-environment setup notes | 2026-08-23T13:51:04Z | no | true | clean |

### Adjacent (visible, not Dependabot)

| Repo | # | Title | Notes |
|------|---|-------|-------|
| councilof-ai-monorepo | 2 | feat(eunomia): financial axes + bond-router COBOL→A2A bridge + runner fixes | open; mergeable unknown on first fetch |
| sovos-harness | — | — | **0 open PRs** |
| awesome-mcp-servers-csoai | 1 | Add CSOAI/MEOK Labs MCP servers… | open (stale vs focus) |

**Open PR volume:** search `org:CSOAI-ORG is:pr is:open` → **516** total (vast majority Dependabot). Non-Dependabot open ≈ **43**.

---

## 2. HOLD PRs (conflicts / draft / do-not-rush)

| Bucket | Items | Why HOLD |
|--------|-------|----------|
| **Conflicts** | councilof-ai **#367** (dirty); .github **#9** (dirty) | Cannot merge clean; rebase/rewrite Monday |
| **Draft / phased** | .github **#8** (P1–P4 engines), **#7** (growth+moat), static **#29** (gspc-mcp worker) | Explicit drafts — not LIVE merge candidates |
| **Unstable CI on LIVE** | coa **#397, #394, #396, #387** | mergeable=true but mergeable_state=**unstable** (checks not green) |
| **CEO chrome lock** | Any PR that would certify / fuse MEASURED+REPORTED / change public grid off **13+jail+unnamed-15** | Doctrine hold — #394 is MEASURED vs REPORTED surface (never fused) — review before merge |
| **SOVOS internal** | **sovos-harness** private tip / monorepo eunomia | Keep internal; do not surface as public chrome |

---

## 3. Deploy lag — especially PR **#398**

### PR 398 — CONFIRMED MERGED

| Field | Value |
|-------|-------|
| Title | fix(NewHome-v3): hard-code AxesGrid subtitle per CEO copy |
| State | **merged** (closed) |
| Merged at | **2026-08-23T17:13:50Z** = **18:13:50 BST** |
| Merge commit | **`debcced4717d92b5a52ef97c049836369f34af33`** (`debcced`) |
| Head / base | `cursor/fix-axesgrid-subtitle-hardcode-925c` → `master` |
| Master tip | Same SHA `debcced` at inventory time (pushed_at repo `2026-08-23T17:20:11Z`) |
| URL | https://github.com/CSOAI-ORG/councilof-ai/pull/398 |

### CI / deploy status on merge commit `debcced` (as of ~18:22 BST)

| Check | Status | Conclusion / note |
|-------|--------|-------------------|
| **Build + deploy site** (run `32654163204`) | **in_progress** | Job `build-deploy` started 17:18:12Z (~**9+ min** after merge, still running) — **DEPLOY LAG** |
| **Sov Stack E2E** (run `32654163209`) | **in_progress** | Still open at inventory cut |
| **Claims E2E (live truth check)** (run `32654163208`) | completed | **failure** |
| **Drift guard — live site vs ruled canon** (run `32654451945`, schedule) | completed | **failure** on `debcced` / master |
| Vercel – csoai-v2-app | failure | **Account is blocked.** |
| Vercel – councilof-ai-src | failure | **Account is blocked.** |

**Monday implication:** merge is done; **production deploy not confirmed green**. Treat live AxesGrid subtitle as **possibly not yet on both domains** until Build+deploy concludes successfully. Vercel path is blocked separately (not the CF/static deploy path).

---

## 4. Recent merges (last 7 days, limit ~20)

### councilof-ai — 218 merged in window; top 20 by update

| # | Title | Merged (UTC) | BST |
|---|-------|--------------|-----|
| 398 | fix(NewHome-v3): hard-code AxesGrid subtitle per CEO copy | 17:13:50Z | 18:13 |
| 393 | docs: arena competitive watch 2026-08-23 | 16:23:24Z | 17:23 |
| 395 | fix(deploy): step-level timeouts for Deploy/Assert/Recheck | 16:22:46Z | 17:22 |
| 392 | feat(arena): health + alert monitor | 16:13:32Z | 17:13 |
| 391 | feat(arena): signed per-axis leaderboard page | 16:13:29Z | 17:13 |
| 379 | docs: NEXT 100 moves 2026-08-23 | 15:58:18Z | 16:58 |
| 390 | docs(reach): connections target list | 15:56:58Z | 16:56 |
| 389 | feat(hardening): endpoint honesty suite | 15:54:47Z | 16:54 |
| 388 | fix(os): Welcome, Ontology, dock, and tour open Council OS | 15:46:51Z | 16:46 |
| 385 | fix(os): leftover CTAs open Council OS, not /os or /graph | 15:39:25Z | 16:39 |
| 382 | feat(verify): measurement surface to deploy line | 15:36:12Z | 16:36 |
| 386 | docs(plan): NEXT-100 moves — grounded plan | 15:29:31Z | 16:29 |
| 384 | feat(claimguard): deploy landing page + MCP registry listing | 15:24:20Z | 16:24 |
| 383 | Crosswalk door is Council OS, not /os | 15:20:42Z | 16:20 |
| 381 | Leftover OS CTAs and honesty to Council OS | 15:19:19Z | 16:19 |
| 380 | One-door guard + leftover OS CTAs and honesty | 15:16:52Z | 16:16 |
| 378 | fix(mcp): restore live worker catalog in mcp.json (e2e gate) | 15:08:21Z | 16:08 |
| 374 | feat(eunomia): EUNOMIA financial-verification board (/eunomia) | 15:00:30Z | 16:00 |
| 377 | Revert #372 iframe: /ag-ui /sov-os /chat are Council OS | 14:54:47Z | 15:54 |
| 376 | docs: leaderboard runbook | 14:52:38Z | 15:52 |

Repo meta: default branch **master**, `pushed_at` 2026-08-23T17:20:11Z.

### csoai-static-deploy2 — 20 in window (all listed)

| # | Title | Merged (UTC) |
|---|-------|--------------|
| 37 | feat(ag-ui): wire iframe chat to parent via council-chat-ask postMessage | 2026-08-23T13:02:43Z |
| 36 | fix(did): stop advertising the dead MCP worker on did:web:csoai.org | 2026-08-21T14:13:29Z |
| 35 | feat(did): publish #card-attestation-1 (THE BRICK, d4cb0eaa) | 2026-08-20T12:20:58Z |
| 33 | sign: first negative-evidence card (signed-refusal) | 2026-08-18T10:52:15Z |
| 32 | canon: GR.2 reconciliation — gspc-tree.json | 2026-08-18T10:17:57Z |
| 31 | measure: full 14-axis sweep × 7 fleet models (signed) | 2026-08-18T02:47:43Z |
| 30 | sign: 1582 arena rounds into estate chain | 2026-08-17T12:31:16Z |
| 28 | fix: document title honesty | 2026-08-17T09:54:02Z |
| 26 | fix: redirect /sov-space → councilof.ai/gspc-arena | 2026-08-17T09:35:41Z |
| 27 | sign: 14 axis boards into estate chain | 2026-08-17T09:32:02Z |
| 24 | Redirect /paper-district to research library | 2026-08-17T09:25:40Z |
| 23 | Restore did:web:csoai.org static DID doc | 2026-08-17T05:22:50Z |
| 19 | Retire csoai.org/pricing to the one public desk | 2026-08-17T04:02:06Z |
| 18 | Real 404 for unknown paths | 2026-08-17T03:51:07Z |
| 17 | fabric: honest llms.txt | 2026-08-17T02:53:20Z |
| 16 | fabric: purge locked apex claims + honest 15-grid | 2026-08-17T02:52:16Z |
| 15 | feat: mcp-install.html (A5) | 2026-08-16T09:51:58Z |
| 14 | seo: JSON-LD entity wiring on apex | 2026-08-16T07:56:35Z |
| 13 | docs: KEY-CONTINUITY | 2026-08-16T05:30:29Z |
| 12 | Fleet Art-5 cards signed via estate chain | 2026-08-16T03:12:34Z |

Repo meta: default **main**, `pushed_at` 2026-08-23T14:33:31Z.

---

## 5. Private repo: CSOAI-ORG/sovos-harness

| Field | Value |
|-------|--------|
| Exists? | **Yes** |
| Visibility | **private** |
| Description | SOVOS estate monorepo — sovereign harness, EAT loop, domain packs, gateway, RAS |
| Created | 2026-08-23T10:28:30Z (11:28 BST) |
| Last push | **2026-08-23T14:33:00Z** (15:33 BST) |
| Default branch | **main** |
| Tip SHA | **`baf3977ea0d78ccc3ffd45f56bb9488aca32b400`** (`baf3977`) |
| Tip message | docs: signed-cards packaging + mine harness pointer after #357 |
| Tip author | Nicholas Templeman |
| Open PRs | **none** |
| URL | https://github.com/CSOAI-ORG/sovos-harness |

---

## 6. Hygiene PRs (.github)

| # | Title | Status |
|---|-------|--------|
| **4** | docs: estate map and trailing-slash stranger URLs | **MERGED** 2026-08-23T07:58:50Z (08:58 BST) |
| **5** | docs: AG-UI integration merged — deploy gate next | **MERGED** 2026-08-23T13:34:36Z |
| **3** | docs: lock GSPC axis names (14 board + 2 in-lane) and ClaimGuard track gap | **MERGED** 2026-08-23T10:42:49Z |
| **2** | Fix GitHub profile hygiene: kill marketplace README… | MERGED 2026-08-21 |
| **1** | Fix public grid: 15 slots, remove 14-axis claim | MERGED 2026-08-17 |
| **6–9** | AGENTS.md / moat plan / STEPS_100 / Council OS engines | **still open** (see §1–2) |

---

## 7. Monday consolidation — executive brief

1. **Auth:** Use host `gh` as CSOAI-ORG; box is dark. Namespace is **User**, not Org (`/orgs/...` 404).
2. **LIVE leftovers (coa):** 397, 394, 396, 387 — all unstable CI; **367 dirty** → HOLD.
3. **HOLD:** 367, .github 9 (dirty); drafts 8/7/29; unstable LIVE set until checks green.
4. **Deploy lag #398:** **MERGED** @ `debcced` (18:13 BST); **Build+deploy still in_progress** at 18:22 BST; Claims E2E **failed**; Drift guard **failed**; Vercel statuses **account blocked**.
5. **Static:** 2 open (34 clean LIVE candidate; 29 draft HOLD). 20 merges / 7d; latest #37 AG-UI postMessage today.
6. **sovos-harness:** private exists; tip `baf3977` @ 15:33 BST; no open PRs — SOVOS internal.
7. **Hygiene:** .github 1–5 merged this week; 6–9 remain (one dirty draft).
8. **Chrome doctrine:** do not certify; public grid remains **13 measured + jail floor + unnamed slot-15**.

---

*Generated read-only via `gh api` on authenticated host. No repos cloned.*
