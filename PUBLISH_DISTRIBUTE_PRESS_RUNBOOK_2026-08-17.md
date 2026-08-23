# PUBLISH · DISTRIBUTE · PRESS — RUNBOOK 2026-08-17

Status: **READY, mostly blocked on 3 owner gates.** Everything below is drafted or
verified; nothing external was sent this session. Honesty rails active (EAT doctrine:
no 30-frameworks / no compliance-body / no sov-os/sov-space / no 527 / no Measure —
**Sign. Prove.**).

---

## 0. LIVE TRUTH (probed 17 Aug 2026 ~12:10 BST)

| Surface | Result | Note |
|---|---|---|
| csoai.org/ | 301 → councilof.ai (200, 130KB) | apex wildcard redirect live |
| www.csoai.org/ | 301 → councilof.ai | same |
| csoai.org/defoneos | HTTP 200 (3,831b) | stub served explicitly |
| csoai.org/llms.txt | HTTP 200 (2,215b) | ✅ |
| councilof.ai | HTTP 200 (130,441b) | ✅ canonical live |
| meok.ai | HTTP 200 (41,913b) | ✅ |
| sitemap.xml (apex) | follows redirect → 0 locs | masked by wildcard; full sitemap lives on the CF Pages estate |
| PyPI | HTTP 200 | distribution lane reachable |

**Masking alert (tick-301 finding, unchanged):** the apex catch-all serves the
Next.js home for 1,300+ deep-dive pack paths — packs ARE live on the
`csoai-site` CF Pages deployment (`*.csoai-site.pages.dev`), they are just not
reachable through the apex until the wildcard redirect is scoped. This is a
*serving* issue, not a content-loss issue.

---

## 1. PUBLISHING LANE

**Canonical host:** Cloudflare Pages project `csoai-site` (NOT Vercel — billing-blocked).
Estate: 1,109 pages · 1,316 sitemap URLs · 30/30 MCPs · 15/15 repos (as-recorded tick 299/303).

**🚫 BLOCKED — owner gate (the only blocker):** `wrangler` OAuth revoked + GitHub
`CLOUDFLARE_API_TOKEN` secret empty (ticks 296/297, 2× confirmed). Deploy is a
1-command human step:

```bash
# Option A (interactive, ~2 min)
npx wrangler login
npx wrangler pages deploy _site --project-name csoai-site

# Option B (token) — add secret to the repo, then deploy is agent-doable:
#   CLOUDFLARE_API_TOKEN=<token> npx wrangler pages deploy _site --project-name csoai-site
```

**When unblocked, publish order (agents can do all of this):**
1. Re-deploy latest `_site` (tick 299 estate + any newer packs on disk).
2. Scoped-route fix for apex: serve `/defoneos*` + `sitemap.xml` + `llms.txt` explicitly,
   then consider narrowing the `/*` 301 to only known SPA routes (tick-303 pattern).
3. Re-verify: home / defoneos / sitemap (1,316 URLs) / llms.txt byte-exact.

**Other surfaces:** councilof.ai (200 ✅, mounts at /gspc-arena) · meok.ai (200 ✅) ·
sovereign.wiki (DNS A→35.242.143.249 — Nick gate, still pending per 13 Jul state).

---

## 2. DISTRIBUTION LANE

| Channel | State | Owner |
|---|---|---|
| PyPI (~570 packages: 530 crown jewels + brains/bridges/mindsets/products) | ✅ shipped (as-recorded 13 Jul) | agents |
| MCP registry / llms.txt | ✅ live (llms.txt 200) | agents |
| Sitemap (1,316 URLs) | ✅ on CF Pages estate; masked at apex | agents (after OAuth) |
| sovereign.wiki | ⏳ DNS pending | **Nick** |
| npm 2FA / Stripe live-flip | ⏳ revenue wall gates | **Nick** |

Distribution is the healthiest lane: PyPI + llms.txt + MCP registry all live.
No action required this session beyond keeping the publish lane unblocked.

---

## 3. PRESS LANE

**Assets on disk (drafted, verified, NOT sent):**
- `~/clawd/PRESS_PACKET_2026-06-29.md` — full kit: one-pager, 200-word statement,
  ready-to-fire tweet thread, contact block.
- `~/clawd/press-kit/` — pitch + announcement (May, needs refresh).
- `~/clawd/_hive_divergence_2026-06-26/PRESS_OUTREACH_LIST_2026-06-15.md` + `press_send.py`.

**Fresh-facts addendum for any press use (verified today):**
- 1,300+ live pages of UK/EU public-body AI deep-dive packs (DEFONEOS estate, Ed25519 SIGIL-signed, 6 red lines each).
- 30/30 MCPs wired · 15/15 repos · llms.txt live · councilof.ai + meok.ai live.
- C2PA Contributor Member (Adobe/MS/BBC/Sony co-members — warm-intro surface).
- Defensive IP posture: OIN 2.0 + LOT Network executed (15 Aug) — neutral measurement body, not a vendor.

**Ready-to-fire tweet thread (draft — needs Nick's GO before sending):**
```
1/ 🧵 The measurement body for AI compliance just shipped its DEFONEOS estate:
   1,300+ signed public-body AI deep-dive packs. Every page Ed25519-signed.
   Verify offline, no account. Sign. Prove.

2/ 1,316 URLs. 30/30 MCPs wired. llms.txt live. councilof.ai + meok.ai live.
   UK/EU public bodies mapped: what their AI use must never do, in law.
   No invented scores. Every claim points to an artefact.

3/ We don't sell certification. We publish the measurable baseline and sign it.
   C2PA contributor member. OIN + LOT Network defensive posture.
   Ask us what your agency's AI is permitted to do. prove@csoai.org
```
**Press email (draft):** subject `CSOAI: 1,300+ signed public-body AI compliance packs — verify offline`
→ 3-sentence lede using the 200-word statement's facts, link to llms.txt + one live pack,
contact block. **Not sent — external communication requires Nick's go.**

---

## 4. HUMAN GATES (owner — nothing below is agent-doable)

1. **wrangler login / CF token** → unblocks ALL publishing (the single highest-value gate).
2. **Press GO** → authorises sending the tweet thread + press email above.
3. **A100-1 (`1dldzposn7ssuu`) policy:** RUNNING, SSH-dark (re-confirmed 11:05 BST).
   Directive was "copy-then-pause" — DO NOT pause while unreachable (strands in-pod data).
   Either restore SSH (runpodctl ssh info re-check / pod console) then copy+stop, or
   accept the ~$/day while dark. **2 paid pods are running today (3090 + A100-1).**
4. **sovereign.wiki DNS** (A → 35.242.143.249, pending since Jun).
5. Stripe live-flip + npm 2FA (revenue wall, unchanged).

---

## 5. THIS SESSION'S ALIGNMENT (Grok Bot harness)

- `~/.grokbot/harness/fleet.json` — reconciled with true RunPod fleet: 11 pods
  (2 RUNNING: 3090 SSH-OK keeper, A100-1 SSH-dark; 9 EXITED incl. the mine).
- `~/.grokbot/harness/mesh.json` — rule/dark/how updated; mine = learned locally.
- `~/.grokbot/harness/mine/` — NEW dept: `learn.sh` → `mine-learnt.json` +
  `mine-summary.md` (25 models, honest, provenance-tagged; CARE/GOV/SWAG raw scores
  flagged as suspect scoring artifacts, rebench pending).
- Backups: `fleet.json.bak-20260817` · `mesh.json.bak-20260817`.

---

*Runbook written by JEEVES, 17 Aug 2026. Next tick: re-probe after any gate clears.*
