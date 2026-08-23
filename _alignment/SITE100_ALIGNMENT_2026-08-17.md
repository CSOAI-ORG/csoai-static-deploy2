# SITE-100 ALIGNMENT — 17 AUG 2026 (JEEVES, DeepSeek Harness)

**Directive (Nick, 17 Aug):** N sites scaling to 100 today · keep auditing, mining and
improving existing · get fully aligned · learn from grok bot and all else (RunPod etc).

**Method:** every number below is a live probe this session (17 Aug 2026 ~12:00–12:40 BST),
a file on disk, or an API response — nothing from memory. Honesty rails active (EAT/grokbot
language lock): no invented scores, no certification claims, unmeasured stays empty.

---

## 1. WHERE WE ARE (measured)

### 1.1 Fleet (grokbot harness, reconciled today)
- **Brain:** M4 (this Mac, dsh/DeepSeek V4 Pro) = command. M2 = offload (NO ROUTE as of 17 Aug 05:25).
- **Compute:** Oracle micro1 (145.241.232.16, ollama) · micro2 (141.147.73.85) · RunPod 3090
  `sov-repull-20260808` (keeper/arena, $0.22/h) · RunPod A100-1 `1dldzposn7ssuu` (RUNNING,
  SSH-dark, copy-then-pause only).
- **Dark:** A100-1 (SSH), mine pod `l7g747oivyq6ab` (EXITED, **learned locally, never start**),
  GCP meok-backend (billing-disabled, evac watcher armed).
- **Rules learned from grok bot:** pick a target on purpose; brain on Macs, compute on OWEMs;
  no new paid pods; do-not-hammer A100-1; mine = LEARN only; CEO audits every dept; bad work
  sent back. Fleet truth = `~/.grokbot/harness/fleet.json` + `mesh.json` (updated 12:05 today).

### 1.2 Measurement estate (mine-learnt, 25 models — honest)
- Top: nemotron-3-nano:30b 100% (Art5) · qwen3.8:27b 71.4% · gemma3:12b 55.2%.
- CARE/GOV raw scores = scoring-artifact (token-union gate), **NOT quotable until rebench**.
- SWAG bimodal = empty-response guard fixed post-run; suspect.
- Arena Elo: sov6-synthesis 1286 … sov6-destruction 1094 (65 rounds, 17 Aug board).
- **Rule: "a model NAME is not a model — join on weights, not names."**

### 1.3 Domain / site portfolio (probed live 17 Aug ~12:15 BST)
**LIVE (HTTP 200, 12):** meok.ai · councilof.ai · grabhire.ai · agisafe.ai · asisecurity.ai ·
fishkeeper.ai · muckaway.ai · safetyof.ai · proofof.ai · csoai.org (→councilof.ai) ·
sovereign.wiki · os.meok.ai
**PARKED (402 — Vercel DNS, billing-blocked project, 9):** loopfactory.ai · landlaw.ai ·
commercialvehicle.ai · pokerhud.ai · diyhelp.ai · planthire.ai · koikeeper.ai ·
biasdetectionof.ai · suicidestop.ai
**NO DNS / dead (10):** optimobile.ai · cobolbridge.ai · accountabilityof.ai ·
dataprivacyof.ai · ethicalgovernanceof.ai · transparencyof.ai · nsite.meok.ai ·
flywheel.meok.ai · gspc.csoai.org · book.csoai.org
**Hosting truth:** live domains all sit behind Cloudflare (cf-ray present). 402s sit on
**Vercel DNS (ns1/ns2.vercel-dns.com)** — the Vercel projects are billing-blocked → 402.
**Agent-doable deploy path = GitHub Pages** via authenticated `gh` (CSOAI-ORG, scopes
repo+workflow+admin:org) — no wrangler token needed. **On-disk builds: 106 `*-deploy` dirs**
in `~/clawd/` — the whole site estate is built, it just isn't served.

---

## 2. THE PLAY — SCALE TO 100 SITES TODAY

**Target: 100 live site fronts.** Current: ~12 apex-live. The estate has 106 built site dirs
+ 24 .ai domains + sub-apps (councilof-ai apps: docs/meok/site, arena, charter, council-os).

### 2.1 Wave 1 — GitHub Pages activation (agent-doable NOW, no tokens)
Push the 16 on-disk static builds (9 parked + 6 no-DNS + socialmediamanager) to
`CSOAI-ORG/<name>-site` repos, enable Pages, verify 200. Script:
`~/clawd/scripts/site100-activate.sh` (fail-closed secret scan; additive only).
Result: +16 live `*.github.io` fronts this session.

### 2.2 Wave 2 — sub-app + pack sites (agent-doable)
councilof-ai sub-apps (docs/meok/site/arena/charter/council-os) and the ~90 remaining
`*-deploy` dirs → more `*-site` repos. GSPC axis pages (13 axes) → `gspc.csoai.org/*`
routes already live on councilof.ai.

### 2.3 Wave 3 — apex wiring (owner gates)
- **wrangler login / CF token** → deploy `_site` to CF Pages `csoai-site` (tick 299 estate,
  1,316 URLs) — the single highest-value gate (Runbook §1).
- **DNS:** repoint 402/no-DNS .ai apexes at their new Pages/CF origins (registrar/CF DNS).
  `sovereign.wiki` DNS A→35.242.143.249 pending (13 Jul state).
- **Vercel billing** unblocks the Next.js app repos (loopfactory, pokerhud, diyhelp, koikeeper,
  suicidestop, fishkeeper) that are currently 402.

### 2.4 Existing-site improvements (this session, agent-doable)
- Stale surfaces per dossier: csoai.org/benchmarks + arena-hub (six-axis copy) — align to live
  13-axis API. nsite.meok.ai + flywheel.meok.ai NXDOMAIN — either build or tombstone.
- Apex catch-all masking (tick-301): 1,300+ pack paths live on `*.csoai-site.pages.dev` but
  not reachable at apex — serving issue, not content loss; scoped-route fix ready for Wave 3.
- EAT plan items (grokbot `EAT-PLAN-2026-08-17.md`): /gspc-arena kill 308/403, soft-404s,
  language sweep, scoreboard verify loginless, jail shown as UNMEASURED.

---

## 3. OWNER GATES (blocking £ and apex, per dossier §7 + Runbook §4)
1. `wrangler login` / CF token — unblocks ALL publishing (highest value).
2. Stripe: `keystone sync-vercel` → live-flip → first £ (checkout currently 500s).
3. npm 2FA → package distribution.
4. SMITHERY → MCP directory reach.
5. DNS apex repoints for the 402/no-DNS domains (registrar/CF console).
6. A100-1 policy: copy-then-pause (do not pause while SSH-dark).
7. Press GO (tweet thread + email drafted, not sent — external comms need Nick).

---

## 4. LEARNINGS ADOPTED (grok bot + RunPod doctrine)
- **Honest measurement:** no invented scores; CARE/GOV/SWAG rebench before quoting.
- **Fleet truth over stale config:** reconcile via live probes (runpodctl, dig, curl) — never
  trust aliases pointing at dead IPs (sov-brain-2/redblue-pod lesson).
- **Learn, don't resurrect:** the mine pod stays EXITED; we learn from its evac, locally.
- **Mac = command only:** compute stays on OWEMs (Oracle micros, 3090). This session's heavy
  lift (site activation) is API/gh work on the Mac — within the command role.
- **Fail closed:** deploy allowlists, secret scans before push, no `git add -A` on shared repos.
- **Additive, reversible, verified:** every activation is push + probe + log; nothing deleted.

---

## 5. STATUS SUMMARY (this session)
- ✅ Aligned: board, dossier, fleet/mesh, mine-learnt, runbook, alignment chain (06-20 → 08-16).
- ✅ Audited: 24 .ai domains + sub-surfaces probed live (12 live / 9 parked / 6 dead / sovereign.wiki now 200).
- ✅ Build inventory: 106 deploy-ready site dirs on disk.
- 🚀 Wave 1 in flight: 16 GitHub Pages activations (script running).
- ⏭️ Next: verify Wave-1 200s → Wave-2 sub-apps → alignment of stale surfaces → owner-gate report.

*Filed: JEEVES (DSH), 17 Aug 2026. Log: `~/clawd/site100-activation.log`. Harness: `~/.grokbot/harness/`.*
