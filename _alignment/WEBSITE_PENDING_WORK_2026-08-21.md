# WEBSITE WORK — PENDING LIST (full, 2026-08-21)

Source: N_SITES_ENDUSER_TEST_2026-08-19.md (live probe matrix) + NEXT_100_MOVES_SET3
+ live site audit this session. Status = as of 2026-08-21.

---

## 🎨 LOGO — the new logo was never deployed (asked twice)

- **NEW logo exists**: `~/clawd/csoai-static-deploy2/csoai-logo-400.png`
  (400×400 RGBA PNG, 51 KB, **2026-08-19 14:56**)
- **LIVE site still serves the OLD logo**: `~/clawd/csoai-org-v2/public/assets/csoai-logo.png`
  (129 KB, **2026-06-21**), md5 differs from the new file
- Live URL `csoai.org/assets/csoai-logo.png` → HTTP 200 (219 KB rendered)
- **PENDING**: copy `csoai-logo-400.png` into `csoai-org-v2/public/assets/`, update
  references, redeploy via `wrangler pages deploy . --project-name=csoai-site`,
  verify HTTP 200 + md5 match. (Also: meok.ai + councilof.ai + proofof.ai branding
  pass — `~/meok-brand/assets/logo.svg` is 28 May, check if the new mark applies.)

## ❌ FAILING PROBES (from N_SITES enduser test — real gaps, real liability)

| # | Surface | Status | What's pending |
|---|---|---|---|
| 2 | **Kaggle** | ❌ 404 | Org handle is NOT `csoai`. Find the real handle (37+ kernels claimed but lost), fix count, publish datasets + verifier notebook |
| 5 | **Official MCP Registry** | ❌ **liability** | **ZERO** csoai/gspc/council entries after full sweep. `llms.txt` CLAIMS we're listed — that claim is FALSE. Publish via `mcp-publisher` CLI, then fix/remove the false llms.txt line |
| 6 | **Smithery** | ❌ 404 | proofof-ai, cobol-bridge, csoai all 404. Re-link GitHub repos, verify slugs, record real URLs |
| — | **ROR** | ❌ 0 results | Submit curation request citing Zenodo DOIs (4–6 wk bake) → propagates OpenAlex/Crossref/ORCID |
| — | **ORCID** | ❌ 0 found | Register ORCID for all named authors (30 min) — hard requirement for USENIX/S&P |
| — | **OpenAlex** | ❌ 404 | Re-check after Zenodo DOI matures; claim author page |
| — | **Google Dataset Search** | ❌ 0 ld+json | Add schema.org **Dataset** JSON-LD on receipt pages + csoai.org home (currently 0 markup) |
| — | **IndexNow** | ❌ no key served | Serve the key as static .txt at exact path on BOTH csoai.org and councilof.ai, then ping |

## ⏳ PENDING SITE WORK (from NEXT_100_MOVES set-3, items 66-98)

- **66-70** ✅ Cursor agent wired this session (authenticated, smoke test PASSED) — parallel coding on councilof-ai now possible
- **71-75** MCP registry + llms.txt freshness check; **AG-UI wire status** (estate gateway live on :4191)
- **81-85** web-verify next reg horizon: **EU AI Act Dec-2027 deferral** impact on provision bank
- **86-90** competitor scan refresh (Vals/LMArena/Armilla funding deltas)
- **91-95** estate-map audit (10 surfaces, machine paths, did.json stability)
- **96** trust-root stability re-probe
- **97** GitHub restriction status (lift expected 24-72h)
- **98** date-watch update (arXiv 7d, DRCF 13d)
- **sovereign.wiki** — DNS A → 162.255.119.131 resolves but **HTTP 000** (not serving); pending wire

## ✅ PASSING (for context — not work)

csoai.org 200 · defoneos 200 · councilof.ai 200 (+ /api/gspc 23KB, /api/arena 553KB,
/api/feed.xml RSS, /api/badge SVG) · meok.ai 200 · proofof.ai 200 · HF org 29 datasets
(license gap CLOSED) · Zenodo DOI 10.5281/zenodo.21991104 ✓ · PyPI csoai 200 ·
OpenRouter councilof-ai 200 · GUI :3080 + CROSS :4191 + Sim World all live.

## 🆕 EU AI ACT AG-UI (new proposal — see EU_AI_ACT_AGUI_PROPOSAL_2026-08-21.md)

Their site (artificialintelligenceact.eu, 150k users/mo) is read-only text. Proposal:
AG-UI event stream + llms.txt + MCP endpoint wrapping the Act's own content so agents
can query with citations + signed receipts. Estate components all exist and are live
(4 EU MCPs + AG-UI gateway + GSPC). Pending: Nick GO to send + a handover contact.

---

**Next actions ranked:** (1) deploy new logo [30 min] · (2) fix Kaggle handle [1h] ·
(3) MCP-registry + llms.txt truth fix [liability, 2h] · (4) IndexNow keys [1h] ·
(5) schema.org Dataset JSON-LD [2h] · (6) ROR/ORCID registration [1h] ·
(7) EU AI Act AG-UI handover [await Nick GO].
