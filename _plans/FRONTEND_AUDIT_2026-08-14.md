# Front-end audit — 2026-08-14

Page-by-page audit of all 444 tracked root `*.html` pages (excluding `_site/` build output).
Rule applied: **removal = archive, never delete**. Archived pages moved with `git mv` to
`_archive/2026-08-14/<original path>`. `check_counters.py` passes after all changes.

## Counts

| Bucket | Count |
|---|---|
| KEEP | 395 (315 defoneos deep-dive packs + 80 other pages) |
| UPGRADE | 9 |
| ARCHIVE | 40 |
| **Total audited** | **444** |

## Firewall breaches found (highest priority)

1. **ceasai.html — ARCHIVED.** Claimed "CEASAI · Accredited Certification" and "Certified
   Engineer for AI Safety & Implementation — three levels of professional AI-governance
   certification under CSOAI". Direct contradiction of certification.html ("neither
   accredited nor applying"). A measurement body never certifies.
2. **index.html — BREACH, NOT TOUCHED (main-lane property).** Asserts the retracted BFT
   claim as fact: badge "✓ BFT-33 quorum 23/33" (line 46) and "Byzantine Fault Tolerant.
   Quorum 23/33." (line 75), plus "BFT-33" (line 88). Retracted 2026-07-29
   (`_alignment/QUORUM_RETRACTION_2026-07-29.md`). Also links MASTER_TAKEOVER.html (now
   archived) twice. **The main lane must scrub these.**
3. **sov3-whitepaper.html — FIXED INLINE.** Listed "BFT-33 quorum" as a standing invariant
   and said "certified institutions". Reworded to the designed-33-council retraction
   phrasing and "measured institutions".
4. **scorecard.html — FIXED INLINE.** Sold a "Certification — 'SOV Protocol Compliant'
   badge — $5K / cert" product tier. Reworded to a signed measured-run record,
   "a measurement, not a certification".
5. **series-a-deck.html + series-a-data-room.html — FIXED INLINE.** Echoed the
   "Certification $5K" tier; reworded to match the scorecard fix.
6. **a2a-swarm.html — FIXED INLINE.** Demo prose had CouncilOf "issue a compliance
   certificate" (£50/certificate). Reworded to "signed audit receipt". The internal JS
   message-type string `issue_certificate` remains (visible only in the demo's raw JSON
   log) — cosmetic, flagged under UPGRADE-optional.
7. **MASTER_TAKEOVER.html — ARCHIVED.** "100/100 doctrine" self-grade, "BFT-33 council"
   as fact, plus an internal revenue plan (Stripe links, cold-email checklist) on the
   public surface.
8. **defoneos-seal.html — ARCHIVED.** Described a "sovereign AI governance credential…
   issued only after a 23-of-33 quorum… ratifies the run" — credential-issuance framing
   from the hash-theater era.

No survivors of the quarantined counters (the framework-count and signed-agent-count
phrases in check_counters.py's UNEVIDENCED list) or lorem ipsum were found in tracked
root pages. `python3 check_counters.py` → PASS before and after.

## ARCHIVE (40 pages → `_archive/2026-08-14/`)

| Page | Reason |
|---|---|
| MASTER_TAKEOVER.html | Internal ops dashboard on public surface; 100/100 self-grade; BFT-33 as fact; Stripe/revenue checklist |
| EXEC/EXEC_DASHBOARD.html | Internal exec pipeline dashboard ("Full Speed Ahead") leaking into public |
| master.html | Near-empty jargon stub ("SOV33 OWEM Hub", sigil_digest chain); no content |
| sovereign.html | Near-empty stub; "OWEM swarm", sigil jargon; links only to other stubs |
| defoneos.html | Stale stub — claims "21 packs" (there are 315); superseded by defoneos-index.html; nav has "Master" twice |
| defoneos-owem-rfq.html | Dead product stub: "Open Warfare Emergence Matrix" RFQ; nav is "Master" ×3 |
| defoneos-article-50.html | Stub with expired countdown to 2 Aug 2026; superseded by article-50.html + tools/article50-passport.html |
| defoneos-seal.html | Credential issued by "23-of-33 quorum" council — certification-adjacent hash theater |
| defoneos-cost-reduction-manifesto.html | Unmeasured "90% savings vs Palantir/Anduril" marketing manifesto; broken nav ("Master" ×5) |
| ceasai.html | "Accredited Certification" claim — firewall breach (see above) |
| charter-portal.html | "41 charters orbiting a BFT Council of 33 agents" 3D theater; BFT presented as real |
| birth.html | Internal substrate experiment ("Mode 0 · Birth · J-space coordinate") |
| bus-portal.html | Internal StateBus (water/milk/honey) visualization; needs a Redis backend |
| experiments.html | MEOK OS internal A/B dashboard; MEOK branding breaches the CSOAI/MEOK boundary |
| pulse.html | MEOK OS "live heartbeat" dashboard with BFT weight cells; internal telemetry |
| sovereign-os.html | MEOK-branded "Council OS — 5 Worlds" page; MEOK content must not live under CSOAI |
| sov7_synthesis_dashboard.html | Internal training-pipeline dashboard ("bloodline fusion") |
| sov7_visual_synthesis.html | Same family — internal synthesis visuals |
| sov7_synthesis/_sov7/sov7_master_dashboard.html | Same family; contains BFT-era content |
| sov-5d-engine.html | SOV-Space experiment (UE5 representation) — internal world-model viewer |
| sov-city-3d.html | SOV-Space experiment — governance-city toy |
| sov-fluid-viewer.html | SOV-Space experiment — "living visual reasoning memory" |
| sov-globe-portal.html | SOV-Space experiment — globe & records viewer |
| sov-infinite-zoom.html | SOV-Space experiment — zoom canvas |
| sov-local-viewer.html | SOV-Space experiment — local renderer |
| sov-portal.html | SOV-Space experiment — end-user console mock |
| sov-space-vwm.html | SOV-Space experiment — VWM visual KB |
| sov-suburb-3d.html | SOV-Space experiment — OpenTTD substrate viewer |
| sov-sync-proof.html | SOV-Space experiment — sync demo |
| sov-three-eyes.html | SOV-Space experiment — IWM/OWM/VWM substrate |
| sov-time-canvas.html | SOV-Space experiment — spacetime canvas |
| sov_space_visual.html | "The Soul of Sovereign AI" — internal visual essay |
| portal/index.html | SOV-Space portal shell — internal |
| globe3d.html | Cesium "Photorealistic Governance Earth (beta)" demo — beta toy, no measurement content |
| uncertainty-shader.html | WebGL pixel-shader experiment |
| arena-build/arena-hub.html | Superseded older build copy of arena-hub.html (pre sov34→Council-34 rename, no canonical) |
| SOVOS/published/sovereign-wiki/index.html | Byte-identical duplicate of sovereign-wiki/index.html |
| fca-financial-conduct-supervision-ai-deep-dive-pack.html | Orphaned root-named duplicate of the defoneos- pack family (0 inbound links) |
| ofgem-energy-regulation-ai-deep-dive-pack.html | Orphaned root-named duplicate (defoneos-ofgem-… is the linked one) |
| ofwat-water-regulation-ai-deep-dive-pack.html | Orphaned root-named duplicate (defoneos-ofwat-… is the linked one) |

## UPGRADE (9 pages)

| Page | Fix needed |
|---|---|
| index.html | (main lane — DO NOT TOUCH order respected) Scrub retracted BFT-33/quorum-23/33 claims; remove 2 links to archived MASTER_TAKEOVER.html |
| alphabet.html | Good honest tool; rewrite internal "Drum Spine / tick" vocabulary into public register |
| scorecard.html | Cert tier fixed inline; remaining: soften "the Moody's of AI" positioning line; paid Pro/Enterprise tiers sit oddly with the open-source doctrine — owner call |
| a2a-swarm.html | Prose fixed inline; optionally rename JS message type `issue_certificate` → `issue_receipt` (visible in demo's raw JSON log) |
| arenas.html | Near-duplicate purpose with arena-hub.html (both are arena boards) — consolidate or cross-link with distinct roles |
| tools/charter-network.html | Remove "SIGIL-anchored… EU AI Act compliant" boilerplate meta; state the data source for the force graph; footer links to archived master.html |
| tools/compliance-heatmap.html | Same boilerplate; "Global coverage" heat map needs a visible data-source/date line; footer links to archived pages |
| tools/bft-council.html | Content already carries the retraction ("fault tolerance is NOT claimed — n_eff 1.21 of 3"), but the *filename* still says "bft" — rename with redirect when nav is next touched |
| tools/bft-vote-log.html | Same filename problem; content is "Designed 33-Agent Council" (compliant) |

## KEEP (395 pages)

**defoneos deep-dive pack family — 315 pages KEEP** (`defoneos-*-deep-dive-pack.html`, plus
the three pack-style pages `defoneos-drinking-water-inspectorate.html`,
`defoneos-gangmasters-labour-abuse-authority.html`,
`defoneos-information-commissioner-regulatory-sandbox.html` and the hub
`defoneos-index.html`). Sampled (CMA, FCA, Ofgem, Ofwat packs opened in full): uniform
generated design, professional dark theme, "measurement, not certification" meta, indexed
from defoneos-index.html — this is the live AEO discovery surface, deliberately excluded
from the counter gate. Judged as a family after sampling; not opened one-by-one.

Other KEEP pages (all opened or head-inspected; on-message, honest register):

| Page | Note |
|---|---|
| _templates/HEAD-AI-SEO-AEO-GEO.html | Generator template, not a public page |
| about.html, faq.html, docs.html, products.html, services.html, pricing.html, privacy.html, terms.html | Core 2026-css pages |
| certification.html | The honest "we do NOT certify" boundary page — keep exactly as is |
| article-43.html, article-50.html, article-50-evidence-pack.html, ai-act-summary.html | EU AI Act cluster |
| eu-ai-act.html + eu-ai-act/{compliance,high-risk,risk,summary}.html | EU AI Act cluster |
| cra.html, crosswalk.html, compare.html | Statute/measurement pages |
| benchmarks.html, govbench.html, govbench_leaderboard.html, provbench.html, recompute.html | Benchmark surfaces (leaderboard is notably honest: "author's own models lose to the base they wrap") |
| gspc.html + 15 gspc-* axis/score pages | GSPC suite (gspc-scoreboard "13 axes × 19 models" = models measured, not the quarantined signed-agent-count phrase) |
| blog.html + 5 blog-* posts | Journal, honest register |
| enterprise-{financial,healthcare,public}.html | Pilot audit packs |
| audit.html, seal.html, gate.html, drift-feed.html, refutation-ledger.html, polarity-map.html | Evidence surfaces (polarity-map states the BFT retraction correctly) |
| research.html, research-transparency.html, founder.html, council.html | Org pages |
| scorecard.html, series-a-deck.html, series-a-data-room.html | After inline fixes above |
| sov3-model-card.html, sov3-system-card.html, sov3-whitepaper.html | Cards + whitepaper (after inline fix) |
| sovos.html | "Tour master" — honest (every figure carries n and interval) |
| sovereign-wiki/index.html | Wiki hub (duplicate copy archived) |
| arena-hub.html, arenas.html | Arena boards (see UPGRADE consolidation note) |
| oowm-demo.html, cpo-calculator.html, injection-scanner.html, a2a-swarm.html, alphabet.html | Free browser tools |
| tools/index.html + tools/{article50-passport,bft-council,bft-vote-log,charter-network,compliance-heatmap}.html | Tools (see UPGRADE rows; tools/index has 8 links to archived experiments — below) |
| chrome-extension/popup.html | Part of the real extension bundle (manifest.json + background.js) — moving it would break the package; not a nav surface |
| index.html | DO NOT TOUCH order — but carries the BFT breach; see firewall section |

## Broken links to archived pages (for the main lane to fix in one pass)

**Totals: 900 link instances across 179 pages.** ~85% are generated footer/CTA boilerplate
inside the defoneos packs. Full machine-readable scan preserved in this audit's session;
regenerate with a grep for the 40 archived filenames.

Aggregate by target (fix suggestion in brackets):

| Archived target | Inbound links | Suggested rewrite |
|---|---|---|
| defoneos-owem-rfq.html | 165 (mostly pack boilerplate) | drop the CTA, or → /tools/article50-passport.html |
| master.html | 159 (pack + core-page navs) | → /index.html |
| defoneos-article-50.html | 148 (pack boilerplate) | → /article-50.html |
| defoneos.html | 135 (pack boilerplate + about.html) | → /defoneos-index.html |
| sovereign.html | 8 | → /sovos.html or drop |
| sov-globe-portal.html | 3 (faq, products, tools/index) | drop |
| defoneos-seal.html | 2 (seal.html) | → /seal.html self-content or drop |
| MASTER_TAKEOVER.html | 2 (index.html) | drop — main lane |
| charter-portal, globe3d, sov-5d-engine, sov-city-3d, sov-portal, sov-space-vwm, sov-suburb-3d | 1 each (tools/index.html) | remove the "3D/visual" card block from tools/index |
| defoneos-cost-reduction-manifesto.html | 1 | drop |

Non-pack pages carrying broken links (exact rows):

```
about.html            -> defoneos.html (2)
audit.html            -> defoneos-article-50.html (1), defoneos-owem-rfq.html (1), master.html (3)
chrome-extension/popup.html -> defoneos-article-50.html (1), master.html (1)
council.html          -> master.html (1), sovereign.html (1)
docs.html             -> master.html (1), sovereign.html (1)
faq.html              -> master.html (1), sov-globe-portal.html (1), sovereign.html (1)
founder.html          -> master.html (1)
gate.html             -> defoneos.html (1), master.html (1), sovereign.html (1)
govbench.html         -> master.html (1)
index.html            -> MASTER_TAKEOVER.html (2)   [main lane]
pricing.html          -> master.html (1), sovereign.html (1)
products.html         -> master.html (1), sov-globe-portal.html (1), sovereign.html (1)
seal.html             -> defoneos-seal.html (2)
sovereign-wiki/index.html -> defoneos.html (1), master.html (1), sovereign.html (1)
tools/article50-passport.html -> defoneos-article-50.html (1), defoneos-owem-rfq.html (2), master.html (3), sovereign.html (1)
tools/bft-council.html    -> defoneos-article-50.html (1), defoneos-owem-rfq.html (1), master.html (2)
tools/bft-vote-log.html   -> defoneos-article-50.html (1), defoneos-owem-rfq.html (1), master.html (2)
tools/charter-network.html -> defoneos-article-50.html (1), defoneos-owem-rfq.html (1), master.html (2)
tools/compliance-heatmap.html -> defoneos-article-50.html (1), defoneos-owem-rfq.html (1), master.html (2)
tools/index.html      -> charter-portal.html, globe3d.html, sov-5d-engine.html, sov-city-3d.html,
                         sov-globe-portal.html, sov-portal.html, sov-space-vwm.html, sov-suburb-3d.html (1 each)
```

The remaining ~150 pages with broken links are all defoneos packs whose generated
footer/CTA strip points at the four archived stubs — fixable with one scripted pass over
`defoneos-*.html` (the pack body content itself needs no edits).

## Ambiguities left in place (honest notes)

- **index.html** carries the worst live firewall breach (BFT as fact) — out of my lane by
  instruction; flagged, not fixed.
- **chrome-extension/popup.html** left despite SOV33 branding because it is a functional
  extension bundle file, not a nav page.
- **tools/charter-network.html / tools/compliance-heatmap.html** kept although I could not
  verify the provenance of the data they render; flagged under UPGRADE rather than
  archived because they are curated on tools/index.html and carry no retracted claims.
- **Paid tiers** on scorecard/pricing/series-a pages conflict with the "open source, not
  SaaS" doctrine but describe audits/services rather than SaaS gates — owner call, left.
- **defoneos packs** judged as a family from a 4-pack sample + uniform generator metadata,
  not 315 individual openings.
- **_site/** untouched (regenerated by build_site.py); it still contains stale copies of
  archived pages until the next build.
