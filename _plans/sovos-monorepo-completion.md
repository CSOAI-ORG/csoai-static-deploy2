# SOVOS — THE MONOREPO COMPLETION MAP
### Everything outside the wall, what to absorb, what to reference, what to reconcile

*Compiled August 11, 2026. Sources: live estate sweep this session (GitHub CSOAI-ORG, councilof.ai, meok.ai, csoai.org, PyPI/Smithery/glama/MCP-registry presence) + all engagement logs. Verdict tiers per item: ABSORB (bring inside SOVOS/) / REFERENCE (manifest entry, stays published) / RECONCILE (claim drift to fix) / OWNER (Nick-gated).*

---

## 0. THE ESTATE, AS MEASURED TONIGHT (bigger than the briefs said)

- **GitHub CSOAI-ORG: 568 repositories** [github.com/csoai-org]. Every prior count undercounted (50+ → 152 → 568). Founder: Nicholas Templeman, Yorkshire, UK Companies House 16939677.
- **The MCP fleet is published and distributed**: PyPI (`pip install`/`uvx`), Smithery, the official MCP registry, glama, claudeskills directories. Named, verified tonight: `csoai-governance-crosswalk-mcp` (**30-framework crosswalk — billed as the only one**), `iso-42001-ai-mcp` (**billed as the only ISO 42001 MCP globally**), `nist-rmf-ai-mcp`, `bft-progress-council-mcp`, `meok-eu-aigc-icon-mcp` (Article 50 icon), `education-ai-mcp`, `image-metadata-ai-mcp`, `meok-ai-reflection-mcp` (extracted from SOV3). **MEOK Governance Suite: 38 governance MCPs** — EU AI Act, DORA, NIS2, CRA, GDPR, ISO 42001, FDA SaMD, MDR, Basel, MiFID II, MiCA, COPPA.
- **councilof.ai is already a deterministic compliance console**: *417 frozen statutory provisions, four lenses, zero models in the verdict path*, 30 frameworks crosswalked, Ed25519-signed offline-verifiable proofs, GovBench 193 items. **And it already carries the public honesty ledger** — the 33-agents retraction is published on the page itself. That retraction ledger is a trust asset; keep it forever.
- **meok.ai is live and deep**: v0.9 sovereign release, 7 archetypes / 27 named characters / 6 growth stages, Ed25519 key-claim flow, Merkle-anchored memory ledger, C2PA Contributor badge, GSPC arena link ("twelve greenfield axes, measured live"), /verify readers on both domains, MEOK GO + /world 3D + /ar surfaces, Stripe buy ladder (£1/£9/£29 — same link the x402 gate uses ✅ consistent).
- **Domain constellation**: councilof.ai, csoai.org, meok.ai, safetyof.ai, cobolbridge.ai (legacy modernization — a whole second business line).
- **Thin spots**: Kaggle profile not publicly discoverable (provebench tasks exist but Kaggle-side presence is opaque); **no HuggingFace presence found** — sov33/sov-safety-v1 are not publicly indexed anywhere (consistent with the "sov33-v9 weights not on pod" problem).

---

## 1. ABSORB — what must come inside the wall

| # | Asset | Where it lives now | Why it belongs inside |
|---|---|---|---|
| 1 | **The 38-MCP Governance Suite source** | Separate CSOAI-ORG repos | These ARE the RAS product surface (Part O). Monorepo them as `SOVOS/packages/mcp-governance/*` or a single `sovos-governance-mcp` meta-package. The crosswalk MCP + ISO 42001 MCP + NIST RMF MCP are the law-monorepo's v0 — *the crosswalk existed as a product before it existed as a plan* (again). |
| 2 | **The 417-provision statute dataset + 4-lens console engine** | councilof.ai site code | This is the deterministic compliance engine — the law corpus v0 that predates the CELLAR plan. Absorb as `sovos-statute-db` + expose through the chain. CELLAR then *extends* it rather than starting it. |
| 3 | **The remaining 41/47 api/*.js** | top-level, unabsorbed | Finish the Part R tranche. |
| 4 | **sov-os Rust crate (incl. ue5-bridge)** | confirmed on disk in Part G, not in the 37 | Mode 3 + UE5 depend on it. Absorb alongside sovos-hive as the second Rust citizen. |
| 5 | **DEFONEOS regulator packs (tick 258+, phase 246)** | sibling lane, same branch | Converging with RAS territory (Part P.4 flag). Absorb the packs as `SOVOS/deploy/regulator-packs/` with honest STATUS labels. |
| 6 | **Strategy/status docs** (STATUS.md series, BRIEF_AUDIT, REAL_MEASUREMENT, INVENTORY, HONEST_MINE) | SOVOS/ root (partially in) | Keep — but add the VERIFIED-header rule (Part M) to every one that will ever leave the building. |
| 7 | **This engagement's research corpus** (master, atlas, hunt, portfolio, market, RAS, endgame — the documents you're reading) | orchestrator sandbox `/mnt/agents/output/` | Export into `SOVOS/docs/strategy/` so the monorepo contains its own reasoning. A repo that contains its own strategy is a sovereign repo. |
| 8 | **UncutGem repo** | pending verification since earlier phases | Verify, then absorb or kill — close the item either way. |
| 9 | **A100 bring-up + spec6 harness** | done ✅ (Part Q) | — |
| 10 | **m2-deployment-kit** | done ✅ (Part R) | — |

## 2. REFERENCE — published artifacts, manifest not absorption

- **The 500+ non-governance MCP repos**: do NOT absorb 568 repos. Create `SOVOS/registry/fleet-manifest.json` — every published MCP with name, PyPI version, registry URL, axis coverage, and last-verified date. The monorepo *indexes* the fleet; the fleet stays published. This manifest doubles as the public "fleet page" data source — one number, one definition (see §3).
- **PyPI/Smithery/registry listings**: referenced in the manifest; republish automation later.
- **csoai_leads.db (2,363 leads / 570,698 rows)**: business data — does NOT belong in the monorepo. Encrypted backup + a `data/` pointer note only. Customer data in a code repo is a GDPR-own-goal; we're the privacy people.
- **Kaggle benchmarks**: provebench package absorbed ✅; Kaggle-side profile/datasets stay hosted there — referenced in manifest.

## 3. RECONCILE — claim drift across the estate (fix before the exposure phase)

| Claim | Where | Conflict | Canonical ruling |
|---|---|---|---|
| "300+ MCP servers" / "207 MCP servers" / "81-MCP fleet" / "38 governance MCPs" / "568 repositories" | various readmes, csoai.org/about, buy ladders, GitHub | Five numbers for one fleet | **One public number with one definition**: "N MCP servers published to the official registry" (countable, verifiable), with repos-count stated separately as engineering surface. Update all surfaces from the fleet-manifest. |
| "33 Witness Council" (meok.ai) vs 33 ratified seats / 3 live processes vs "19 signed agents" (councilof.ai) | meok.ai, councilof.ai | Three council numbers | Canonical precision ruling stands: **33 ratified seats, 3 live processes**. meok.ai "33 Witness Council" → "33 ratified seats". councilof.ai's "19 signed agents" → reconcile or footnote. The site's own retraction ledger sets the standard — extend it. |
| "Twelve greenfield axes, measured live" | meok.ai | ✅ NOW TRUE (arena 9/9, Wilson CIs) | Keep. First marketing claim with a test suite attached. |
| "world's first sovereign AI OS" (meok.ai/go) | meok.ai | Superlative | Defensible-position framing: "the sovereign AI OS with a published measurement substrate" — superlatives invite challenge; measured claims invite verification. |
| Kaggle/HF absence | — | The models the arena references aren't publicly indexed | **HuggingFace model cards for sov-safety-v1 (+ sov33 when weights are located/retrained) with arena scores attached** — the RAS credibility loop runs through HF. This is a distribution gap, not a code gap. |

## 4. OWNER-GATED (Nick, not code)

- **sov33-v9 weights**: locate or retrain — the model artifact itself is the one piece of the empire with no known address.
- **Mamba-3 / ITQ3_S installs** (owner-gated from Part G-δ2).
- **Oracle fleet auth** (Week-1 P0 from the estate audit — still open).
- **Vercel billing / Stripe / OpenRouter / x402 pay_to** (carried from Part K/Q).
- **Kaggle profile + HF org setup** — accounts exist? claim the namespaces, publish the cards.

## 5. THE COMPLETION ORDER

1. **Fleet manifest** (days) — one JSON, one canonical number, feeds every public surface. Ends the five-numbers problem permanently.
2. **Governance 38-pack absorb** (~1 week) — the RAS product surface comes home; crosswalk/ISO/NIST MCPs become law-monorepo v0.
3. **Statute-DB absorb** (~1 week) — 417 provisions + lens engine as `sovos-statute-db`; CELLAR pipeline extends it.
4. **Remaining api tranche + sov-os Rust** (~1 week).
5. **Strategy docs export + VERIFIED headers** (days).
6. **HF model cards + Kaggle profile** (days, owner-assisted) — arena scores on the cards.
7. **DEFONEOS packs absorb with STATUS labels** — after the lane sync (Part P.4).
8. **UncutGem verdict** — close the oldest open item.

*Completion map compiled August 11, 2026. The headline: the estate sweep found the RAS product surface, the compliance console, and the crosswalk engine already built and published — the monorepo's job is not to create them but to gather them, number them honestly, and point the chain at them. 568 repos outside, 37 packages inside, one manifest to rule the count.*
