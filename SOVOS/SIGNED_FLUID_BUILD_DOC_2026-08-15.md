# SIGNED-FLUID BUILD DOCUMENT — v1.0 (2026-08-15)

## Council of AI / CSOAI LTD (UK 16939677) — the build spec for the AI-economy fabric

**Status: READY TO BUILD** — one document, four blocks of work, all mechanisms verified.

---

## PART 0 — WHAT THIS IS

Three mechanisms, run separately, because running them together is where the confusion creeps in:

1. **OMS as the front door** — every model entering the estate gets licence-recorded, checked for upstream
   signature, then signed by us as custodian (weights + config + tokenizer as one unit) → **one digest**.
   From then on the model is not "Hy3" — it is a pinned artifact. The catapult: cheap, one pip install,
   converts every downstream number from a claim into something bound to a fact.
2. **The harness merge** — `sovos_chain.py` already runs router → clan council → gate chain. What changes:
   the router dispatches to **digests rather than model names**. Same code path, one field swapped.
3. **The paired J-Space records (the real invention)** — run the same benchmark item TWICE: once through
   the signing spine, once bypassing it. Both write J-Space records with a shared pair ID. Signed vs
   unsigned becomes a controlled variable, not two products. Every arena cell (AI-vs-AI, human-vs-AI,
   swarm-vs-swarm) inherits the pairing automatically because it sits **upstream of the cell**. One
   execution yields: axis score + signing overhead + cell comparison, all commensurable on one digest.

The overhead number (cost of signing) is **publishable and nobody has it**. That is the honest wedge.

---

## PART 1 — ESTATE MINE (verified 15 Aug 2026, 06:45 UTC)

### What already exists (binding, not building)

| Component | Location | Status | Evidence |
|---|---|---|---|
| BOM builder + signer | `SOVOS/packages/sovos-city/src/sovos_city/bom_signer.py` | **LIVE** | `build_minimal_bom()`, `sign_bom()`, `self_test()` all present |
| OMS model-signing integration | `SOVOS/agents/oms_sign.py` | **LIVE** | commit `d62560ae` — signed card + paired records verified |
| Chain / harness | `SOVOS/packages/sovos-chain` | **LIVE** | 15/15 tests |
| J-Space | `sovos-jspace-hyperbolic/pipeline/move` | **LIVE** | path hook fix committed `4f7a3e4f` |
| Arena + real league | `sovos-arena`, `sovos-league` | **LIVE** | 48 real matches → Glicko-2 |
| Honey strata (behaviour data) | `forest/honey_all_producers.jsonl` | **LIVE** | **4,896 rows** — the asset — **0% signed** |
| Board measurements | `SOVOS/boards-v2-2026-08-12/` (13 axes, 19 models) | **LIVE** | G4 gate PASS, quotable n≥30 |
| Axis-14 (jail) | `sandbox_escape_bench.py` | **MEASURED** | 30+30 gold bank, 1.0/1.0 |
| Monorepo migration | `registry/migration-state.json` | **IN FLIGHT** | 10/55 migrated (arena, city, glass, harvest, league, chain, gprobe, invariants, fisher-rao, signal-index) |
| Oracle free mesh | micro1+micro2 city report + verify health | **LIVE** | 05:00 UTC daily, £0 |
| K3 serverless | `sov6-kimi-k3-2tb` (FlashBoot + 2TB vol) | **LIVE** | pay-per-inference |
| OpenPatent.ai readiness | `ip_readiness.py` → `/v1/readiness` | **LIVE** | CF Pages |
| IP posture | OIN 2.0 + LOT executed + 42-comp inventory | **CLOSED** | committed |
| verify_record | csoai_pkg (sibling lane) + GSPC MCP worker | **LIVE** | 5/5 tests |
| GSPC MCP endpoint | `https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp` | **LIVE** | `measure` + `verify` tools |

### The gap this document closes (verified by count, not assumption)

```
Honey rows:     4,896
Signed rows:        0   ← 0% of the compounding asset is provable
```

Everything else can wait. **This is the first build item.** Until the honey routes through the signing
spine as a card type it is a valuable pile, not a provable asset. Signed makes it sellable and citable.
Unsigned, a buyer takes your word.

---

## PART 2 — THE FIREWALL DOCTRINE (the line this whole build holds)

**Measure or build — the neutrality survives only one of them.**

- ✅ **Generate and sign the data** — publish datasets, stay neutral, sell signed cards. This is the business.
- ❌ **Merge that data into a rival flagship model** — training a competitive model on the honey is where
  the auditor problem bites. Same data, two very different positions.

Consequences already wired in:
- The estate's honest finding (AGENTS.md v49.2 lane log): *"base Qwen2.5-0.5B still beats every sovereign
  fine-tune on 8/9 measured governance axes (only path: base model + statute retrieval, NOT weight-merge
  of weak specialists)."* — **the data says the merge path doesn't even work yet**; the firewall is not
  just principle, it's the measured result.
- Frozen-to-fluid / GNN → simulation → ASI-evolve is the **champion-model direction**. It stays on the
  build side only for sovereign internal simulation, never as a publicly-competing flagship trained on
  published honey.

**The moat is not the signature on the model.** OMS is a public standard; anyone can sign the same
weights tomorrow. Signing produces custody, not exclusivity. The moat is **the measurement bound to the
digest** — the signed benchmark-against-benchmark corpus that only we run. That distinction is the whole
business.

---

## PART 3 — THE FLYWHEEL (why this compounds)

```
15-axis benchmark (nobody else runs it)
        │
        ▼
behaviour data (humans + AI + swarms, every cell)
        │
        ▼
PAIRED signed/unsigned J-Space records   ← 3rd mechanism, upstream of every cell
        │
        ▼
honey strata (trained + signed versions)
        │
        ▼
simulations / cross-synthesis (GNN/NN → 3KB cards)
        │
        ▼
ASI-evolve loop closes back into new probes
        │
        ▼
repeat — each pass adds a signed stratum nobody else has
```

"Not only are we testing humans against the fifteen-axis benchmarks no one else is doing — we're also,
at the same time, training the models, and simulating / cross-synthesizing all of this data." — the
compound effect is the product.

---

## PART 4 — RESEARCH + TODAY'S MARKET (15 Aug 2026)

### Standards layer (all current, adopt-not-build)
- **OMS (OpenSSF Model Signing)** — v1.0 shipped 4 Apr 2025, spec June 2025, Sigstore Bundle Format,
  PKI-agnostic (keyless OIDC OR bare keys OR self-signed). NVIDIA signs NGC models since Mar 2025.
  **Our posture: key-based PKI, not keyless OIDC** — a neutrality-dependent body must not delegate the
  root of trust to a single commercial IdP (Google/GitHub). Anchor in **SCITT (RFC 9943, June 2026)** +
  **RFC 3161** timestamps + own Rekor instance.
- **W3C VC 2.0** (7 Recommendations, 15 May 2025) — machine-verifiable credential wrapper when a third
  party needs credential exchange.
- **C2PA** — for media artifacts the arena generates.

### The fork manifesto (attached compass artifact) says:
- **Crown jewel: `UKGovernmentBEIS/inspect_ai` (MIT)** — the UK AISI's own harness. Binding the signing
  spine into its **`Scorer`** makes a UK company selling measurement into UK/EU regulators speak the
  regulator's native dialect. Threshold: if AISI pivots away from Inspect/licence, fall back to
  `lm-evaluation-harness` (MIT, backs the HF Open LLM Leaderboard).
- Game/simulation layer: `ai-town` (MIT) shell + `AgentSociety v2` (Apache-2.0) experimental backbone
  + `meltingpot` (Apache-2.0) adversarial mechanics. **Trap to avoid:** `generative_agents` art assets
  are a paid itch.io pack — code only.
- RLHF: `OpenRLHF` (PPO/GRPO/DAPO, 70B+) / `trl`; **keep `safe-rlhf` datasets out** (CC-BY-NC).
- Annotation: `argilla` + `distilabel`; seed `hh-rlhf` (MIT).
- Sandbox: **gVisor / Firecracker, never bare Docker**; **safetensors-only, reject pickle** (arbitrary
  code execution); hash-verify every file against the OMS manifest before load.
- **EU AI Act Art 10**: bind annotator-pool metadata into the signed card — compliance becomes a feature.

### Consent (the human arena)
- Estate audit: **ZERO hits** for IRB / participant / human-subject across the whole tree (re-checked
  this session). Consent is **void** — nothing to inherit.
- **EDPB Guidelines 1/2026 (16 Apr 2026)** + **UK GDPR Art 35**: a DPIA is almost always required for
  AI-enabled research. CSOAI LTD = data controller. EDPB harmonised DPIA template (14 Apr 2026) is the
  scaffold.
- **Prolific**: pseudonymous IDs, PII prohibited without written approval, fraud rate <0.1%, video-
  liveness makes pure-AI participation infeasible. **Precedent:** RealityTest ran 503 UK-representative
  participants at £12/hr — a directly citable design template.

### Today's market (BBC, 11–15 Aug 2026 — verified live this session)
- **Nvidia + Wall Street: $500bn AI-infrastructure raise** (Apollo, BlackRock, Blackstone, Brookfield,
  Goldman Sachs, KKR) — *"compute has become a scarce, mission-critical asset class."* $1tn+ already
  spent by tech majors in 3 years. **Implication:** as compute becomes an under-written asset class,
  the measurement/assurance layer over what runs on that compute becomes bankable. That is our wedge.
- **"Why tech bosses keep sharing their manifestos about AI"** (Zuckerberg the latest) — positioning
  war is live; the demand for independent, signed measurement is exactly the void.
- **Tokenomics debate** ("Why making AI pay is tricky") — the payment layer for AI is unresolved; a
  signed, metered card format is a natural unit of exchange.
- **Amazon training on Twitch content (opt-out)** — provenance/training-data rights are front-page.
  Proves the market pain for signed, consented training data.

---

## PART 5 — THE BUILD PLAN (four blocks)

### ✅ BLOCK A — WEEKEND LANE WORK (agent-doable, no gates)
1. **Sign the honey.** Add a `card_type` + Ed25519 signature column/stratum to
   `forest/honey_all_producers.jsonl` (4,896 rows) using `bom_signer.sign_bom()` — make the pile provable.
   Verify: re-count signed% → target 100% by end of weekend.
2. **Wire `oms_sign.py` into every board/arena run.** `board_v2.py`, `cross_lab_city.py`,
   `axis14_city.py`, arena loop: emit a paired signed/unsigned record per cell (pair_id = digest of
   cell content; mechanism already built and verified in `oms_sign.py`).
3. **`inspect_ai` fork** — clone `UKGovernmentBEIS/inspect_ai`, bind the spine into the `Scorer` so
   scorer output is an OMS-signed card. (Crown jewel, MIT.)
4. **Key-based OMS adoption** — `pip install model-signing`; configure key-based PKI (not keyless);
   self-test signing a known model manifest; document the key ceremony in `SOVOS/keys/`.
5. **Migration continues** — run `migrate_one_package.py --all-pending` batch #2 (45 pending).
6. **Estate-wide consent sweep (re-run)** — confirm still zero IRB/participant references post-migration.

### 🗓️ BLOCK B — TWO-WEEK WORK
7. **SCITT (RFC 9943) transparency anchor** — publish signed measurement cards to a SCITT statement
   log; adoption path: own Rekor + RFC 3161 timestamps; measure the signing-overhead number (the
   publishable nobody-has-it metric).
8. **DPIA** — complete using EDPB template; CSOAI LTD as controller; file for the human arena design.
9. **Human arena pilot** — Prolific-scope a 100-participant gold run (RealityTest as template,
   £12/hr), 15-axis human-vs-AI cells, all paired signed/unsigned.
10. **`ai-town` + `AgentSociety v2` + `meltingpot` forks** — instrument agentsociety experiment
    manifests + replay logs for signed/unsigned replay; strip `generative_agents` only as reference.
11. **Scoreboard v2** — `gspc-scoreboard.html` gains the signed/unsigned column + overhead cell.

### 🔐 BLOCK C — OWNER-GATED
12. **npm token** (expires 27 Aug — top of list) + **arXiv endorsement** (tick, expires 27 Aug).
13. **Stripe live flip** + checkout fix (revenue wall).
14. **Human-arena PII/prolific approvals** — any deviation from no-PII needs written Prolific sign-off.
15. **DSRB diplomatic entry** — via UK delegation / DSIT as **Probity Assurance Provider** (never
    portal-builder); NATO DIANA 2027 cohort via Janus Allies — needs owner steer + intro.
16. **HF token revoke** + `meek-3-and-sov3-connection-mcp` PyPI yank/scrub (cross-lane liability).

### ⛔ BLOCK D — DO-NOT-SHIP (firewall)
17. **No rival flagship trained on published honey.** Measure or build; one survives.
18. **No keyless OIDC for public-facing signing** (roots trust in a commercial IdP — kills neutrality).
19. **No `safe-rlhf` datasets, no `generative_agents` art, no pickle deserialization, no bare Docker
    for untrusted model code.**
20. **No "only ones with signed open-source models" claim** — false; anyone can sign. The moat is
    measurement bound to digest, and that's the only defensible copy.

---

## PART 6 — ONE-PARAGRAPH PITCH (for the record)

CSOAI runs the only 15-axis signed measurement bench — humans, AIs and swarms, every cell measured
twice (signed/unsigned, one digest). The behaviour data that spills out of those runs is itself the
asset: consented, licence-recorded, signed, saleable as cards, and citable with proof. We adopt OMS as
the front door (key-based, SCITT-anchored), fork the UK AISI's own harness so regulators read our
numbers in their native dialect, and publish every number with its confidence interval — because a
neutral, audit-grade measurement body is the missing layer of the AI economy that $500bn of Wall Street
compute financing just declared it needs.

---

*Companion artifacts:* `SOVOS/agents/oms_sign.py` (mechanism, committed `d62560ae`) · `bom_signer.py` ·
`SOVOS/FLEET_ROSTER.md` · `SOVOS/GSPC_NUMBERS_REGISTRY.json` · fork manifest (attached compass artifact)