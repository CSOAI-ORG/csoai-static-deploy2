# MASTER FRAMEWORK — the substrate that evolves and keeps-if-better
## OAI Master Framework · v1.4 · 2026-08-20 · FRAMEWORKS DRUM knowledge pack

> **Adopted from:** the COAI architecture session (whiteboard + session summary), mined as one
> object, grounded by the deep-mine corpus map, then **validated against the literature**
> (`docs/RESEARCH_VALIDATION.md`, 2026-08-20). v1.2 applied the validation's surgical
> corrections: 9-step loop → 5 MAPE-K stages; complementarity reframed as task-allocation;
> the 90/10 router speced as a frozen conformal-threshold predicate; mergekit reduced to the
> evolutionary loop (weight arithmetic does not transfer); promote-gate made
> contamination-resistant with significance testing. **v1.3: every [BET] carries its strongest
> disconfirming evidence inline (adversarial-evidence rule, binding). v1.4 (this version,
> Claude alignment): the market-leg/Dorado doctrine with its three boundaries — composed never
> fused, licensed source before assertion, never a trading signal — plus the live-verified
> trust-root state and the did:web reconcile + DSH-key plan.**
>
> **Naming discipline (binding):** codenames in [brackets] are INTERNAL-ONLY and must never
> reach a public surface — [OOWM], [SOV3], [MEOK-internal], [Dorado]. Public grammar only:
> "measurement, not certification", "13 measured of 14", "verified measurement credential".
> This doc is showable only because the internal names are quarantined here.
>
> **Evidence discipline (binding):** every claim below is tagged [BET] (an architectural
> wager, stated as such), [BUILT] (real code/data exists), or [GAP] (named, not yet real).
> **Adversarial-evidence rule (binding, v1.3):** every [BET] must state its strongest
> disconfirming evidence inline — the best documented result against the wager — and explain
> what survives it. A bet without its counter-evidence is not a bet, it is an assertion.
> The estate's credibility rests on never smuggling a [BET] in as a [BUILT].

## 0. The one-sentence thesis

Build the benchmark-and-promote machinery once, at the substrate level, and every downstream
product (compliance, gaming, the agent harness) inherits improvements automatically — because
CSOAI and [MEOK] share one backend. [BET]

**Strongest evidence against this bet (carried here, not hidden):** the substrate is only
~40% built, and the ~200 marketplace *-ai-mcp repos are one factory + templated stubs, not N
products — inheritance from a substrate that is mostly scaffolding inherits scaffolding. The
55/55 migrated packages and the signed-receipts core are real [BUILT]; the rest of the target
shape (packages/gspc, packages/regwatch, registry/mcp-catalogue, charter/) is [GAP]. What
survives it: "finish + wire + dedupe" is the plan of record, not greenfield — the bet is
conditional on completing the substrate first, and the dedupe list (§6) is the concrete first
pass.

The bet underneath it: durable capability gains come from blending human cross-domain judgment
with AI processing, not AI scaling alone — and the frontier labs are under-investing in the
hybrid. [BET — not a finding; the strongest evidence against this bet is carried in §1, and
the surviving form is allocation, not blending.] The honest evidence position: no model
weights exist in the estate; every "consciousness/AGI/sovereign model" is markdown or a toy
classifier (per the 2026-08-20 inventory). So this framework is an architecture for
compounding measured improvements, not a claim to have built AGI. That distinction is the
whole credibility of a body that measures others.

## 1. The core complementarity — reframed as task-allocation, not blending

What each side actually contributes:

| Human brings | AI brings |
|---|---|
| Ambient cross-domain pattern recognition (rhymes noticed across weeks, unprompted) | Speed processing inside human-defined frames |
| Felt sense of drift — when something stops fitting the long-arc vision | Structured synthesis on demand |
| The selection function — what is worth attention at all | Execution without fatigue |
| Judgment under ambiguity with real stakes | Breadth of recall |

**The strongest evidence against this bet (carried here, not hidden):** the largest
meta-analysis of human–AI teaming to date — Vaccaro, Almaatouq & Malone, *Nature Human
Behaviour* 8:2293–2303, 2024 (arXiv 2405.06087; 106 studies, 370 effect sizes) — found that
on average, **human–AI combinations performed significantly worse than the best of humans or
AI alone** (Hedges' g = −0.23; 95% CI −0.39 to −0.07). The losses concentrated in
**decision-making** tasks; the gains concentrated in **content-creation** (g = 0.64). The
critical asymmetry: **when the human alone outperformed the AI, combining produced gains —
when the AI outperformed the human, combining produced losses.** The failure mechanism is
over-reliance / automation bias and redundancy without a clear division of labour. There was
no human–AI synergy on average.

**What survives it (the sharpening, not a retreat):** this does not kill the bet — it
sharpens it into the version the architecture already implements. The meta-analysis says
*blending is not generically superior*; it does not say *allocation is worthless*. The
defensible design is exactly what this framework builds: **route each task to the stronger
agent, and combine only where the human is the stronger agent or the task is
generative/ambiguous.** Do not blend on decision tasks where AI alone is stronger — the
evidence says that loses. **The 90/10 router (§4) is the corrected thesis in code**: its
frozen conformal predicate is the allocation mechanism, and its escalate-to-human arm is the
one place the literature says combining wins. A bet stated alongside its best evidence-against
is harder to attack than one that merely tags itself [BET]. [BET — evidence-informed; the
disconfirming evidence above is the ledger entry for this wager]

## 2. The engine — a MAPE-K loop with an audit-and-promote stage

The whiteboard and the session summary are the same 9-step cycle:

```
learn/train → check → plan → do → act → check → audit → improve → brand/visual/quality
```

Read plainly, that is PDCA + an audit-and-promote stage bolted on — the mergekit
"keep-if-better" idea. Same object, both ends.

**The validation's correction — collapse to 5 canonical MAPE-K stages** (Monitor-Analyze-
Plan-Execute-Knowledge, the canonical self-adaptive control model; IBM 2003-05; SEAMS 2015):

1. **Monitor** — continuously ingest/mine the corpus and codebase (documents, code, patterns,
   visual records); compute measurable features. (Visual/structural pattern detection over the
   signed-card corpus is the third signal layer here — [BET / partial [BUILT]].)
2. **Analyze** — run the deterministic router (§4) to classify each finding 90%-case
   (auto-proceed) or 10%-case (escalate/explore). **Subsumes the two CHECK stages and the
   separate AUDIT stage** — the promote-gate lives at the boundary to Execute.
3. **Plan** — 90%-cases: auto-generate and queue the obvious next task; 10%-cases: escalate to
   a human judgment call OR fan out into parallel candidate exploration (spawn N, keep the
   best). Time-compression (years→days→hours) is the execution MODE of Plan→Execute here —
   parallel fan-out, not a stage.
4. **Execute** — run the task; for merge/combine candidates, benchmark against the frozen
   baseline and promote only if it beats baseline with statistical significance (§5).
5. **Knowledge (residue capture)** — write every candidate, its provenance, evaluation result,
   and lineage to the append-only, signed archive (the "copy-and-improve" residue). [GAP →
   BUILD — the archive is Stage-1 work.]

**Cut from the substrate loop (validation, binding):** BRAND/VISUAL/QUALITY is genuine scope
creep — a downstream *output* concern, not a control-loop stage; folding it in risks
Goodharting on aesthetics. It becomes a downstream consumer.

## 3. ASI Evolve — mergekit at the knowledge & code layer [BET, with a [BUILT] substrate]

Model mergekit blends weights → benchmarks → keeps if better. **The validation's correction:
weight-space arithmetic does NOT transfer to knowledge/code** — you cannot SLERP two functions
or average two documents. Knowledge artifacts and code do not share the continuous geometry of
weight tensors; merging requires shared base initialization and architecture, and fails via
parameter interference and merging collapse.

**What DOES transfer is the higher-level evolutionary loop** — hunt structurally-similar
patterns → generate combinations/variants → benchmark against a fixed evaluator → keep only if
it beats baseline. This is exactly how the systems that actually work run (AlphaEvolve
arXiv 2506.13131: 4×4 matmul 49→48, 23-32% kernel speedups; FunSearch *Nature* 2023; Darwin
Gödel Machine arXiv 2505.22954: SWE-bench 20%→50%; STOP arXiv 2310.02304). For code the
analogues are genetic improvement / program repair / superoptimization; for knowledge they are
corpus curation, coreset selection, distillation — where data quality beats algorithm
(arXiv 2606.25488, 2411.18674).

**Estate [BUILT] touchpoints:** GovBench (12-axis, real eval code), the 13 GSPC axes, the
held-out batteries; the fix_loop.py "measured-failure → real fix → held-out gate →
promote-if-generalised" (+2.5 held-out proven) is a working instance at the model-tuning layer;
the multi-agent evolve machinery (this session's PRs) is a worked example of the 10%-case fan-out.

**Binding preconditions (validation):** the loop only works where the evaluator is cheap,
fast, and trustworthy — start in one narrow verifier-rich domain (a code module with strong
tests). Every serious system hit the documented failure modes; the safeguards table in
`docs/RESEARCH_VALIDATION.md` (reward hacking, contamination, rise-and-collapse,
evaluator-becomes-target, diversity collapse, automation bias) is binding day-one design, not
afterthought. The estate's existing doctrine — deterministic predicates, no training on
benchmarks, corrections ledger, signed provenance — is unusually well-matched to what the
literature prescribes.

**The strongest evidence against this bet (carried here, not hidden):** every demonstrated
success of self-improving evolution (AlphaEvolve, FunSearch, Darwin Gödel Machine) is
domain-narrow — it works only where the automated evaluator is cheap, fast, and trustworthy
(games, kernels, cap-sets, code with strong tests). Where the evaluator is weak or gameable —
most real-world knowledge work — the loop Goodharts: a large reward-hacking study found 73.8%
of Kernel-Bench optimizations showed proxy gains without real gains (proxy–reality gap widening
from 26.4% to 57.8% over 10→100 steps); naive self-training on competitive programming rose
then collapsed (pass@1 25→81→~0 by step 200, KL/EWC constraints did not prevent it);
SWE-bench Verified carries ~33% solution leakage and OpenAI has retired it. Cost is not
trivial: one 80-iteration DGM run ≈ $22k of API spend. **What survives it:** the failure modes
are documented and the estate's doctrine — deterministic predicates, no training on
benchmarks, corrections ledger, signed provenance, frozen contamination-resistant eval — is the
safeguard set the literature prescribes. The bet survives in its sharpened form: *keep-if-
better works where the evaluator is trustworthy, and we build the evaluator before we build
the loop.*

## 4. The deterministic 90/10 router — the frozen conformal-threshold predicate

The scoring function that routes each finding to the 90%-case (auto-proceed) or 10%-case
(escalate/explore) was the crown-jewel gap. **The validation closes it with a concrete,
doctrine-compliant build spec:**

1. Build a calibration set of past findings with known correct outcomes (never
   arena/benchmark data).
2. Define a computable nonconformity score `s(x)` — e.g., decorrelated ensemble-member
   disagreement, `1 − max softmax`, or distance-to-calibration-distribution.
3. Compute `q̂` = the ⌈(n+1)(1−α)⌉-th smallest calibration score for target auto-proceed error
   α (split conformal prediction, Vovk et al. 2005; Angelopoulos & Bates arXiv 2107.07511);
   **freeze it.**
4. Route: `s(x) ≤ q̂ → auto-proceed`; `s(x) > q̂ → escalate or explore`.
5. Guarantee: `Pr[auto-proceed AND wrong] ≤ α`, distribution-free, under exchangeability.
   Use Conformal Risk Control (arXiv 2208.02814) to bound a cost-weighted loss instead of raw
   error rate. Recalibrate on a controlled, signed schedule (never continuously).

**This is a pure threshold comparison on a measurable quantity — no LLM judges a model.**
[GAP → BUILD; Stage 1.] The ensemble feeding the score must be genuinely decorrelated
(different data slices/seeds/architectures) — shared-base members collapse into the same loss
basin and give little uncertainty benefit (arXiv 2202.06985, 2302.00704, 2210.09184).

## 5. The promote-gate protocol (minimum credible)

"Promoted because it measurably beat baseline" requires more than a single benchmark number
(validation §Key Findings 4):

1. **Frozen, private, contamination-resistant held-out eval set** — canary strings,
   password-protected, never trained on (OpenAI's own recommendation after SWE-bench leakage
   ~33%, arXiv 2410.06992/2507.11059); temporal held-out (SWE-rebench arXiv 2505.20411,
   SWE-bench-Live arXiv 2505.23419) because public benchmarks overstate by 20–50%.
2. **Regression pack:** zero regressions on P0 known-good cases (hard gate).
3. **Statistical significance** vs. an equal-sized baseline cohort, with sequential/anytime-
   valid tests for early stopping (arXiv 2210.08589).
4. **Shadow → graded canary** (1%→5%→20%→50%→100%) with automated rollback triggers.
5. Only then promote permanently, writing to the Knowledge archive with signed provenance and
   a "measured-current-state" record — **never "certified"**.

## 6. The substrate — the monorepo already exists; finish and wire it [BUILT ~40%]

NOT greenfield. `/Users/nicholas/clawd/councilof-ai-monorepo` (org mirror councilof-ai-monorepo)
already has apps/ charter/ evidence/ ops/ packages/ registry/ research/ with **55 csoai-*
packages** migrated ("55/55") — drum-verified 2026-08-20. `SIGNED_RECEIPTS_CONSOLIDATION_SPEC`
(2026-08-20) names inspect-receipts canonical (RFC 8785, e2e 5/5) and lists the 5 dups. Plan of
record = finish + wire this, not start.

**Real target shape:** `apps/site/` (fold in the master SPA + 33 signed /api handlers) ·
`packages/receipts/` (ONE signed-receipt core; delete 4 dup copies) · `packages/core/`
(canon.json + ruling loader + drift-guard) · `packages/crosswalk/` (13-framework × 52-article,
single impl — 3 today → 1) · `packages/gspc/` (14-slot axes registry + board harness +
separation gate) · `packages/frameworks/` (FRAMEWORK_GROUND_TRUTH — verified-to-primary-source,
the credibility engine) · `packages/regwatch/` (corpus-watch detector + reg-watch-state) ·
`registry/{mcp,a2a,did}/` (ONE mcp-catalogue.json — kills the 819/890/966 count drift —
+ agent-cards + trust root) · `charter/` (52-article charter single canonical, constitution,
rulings, corrections, firewall) · `frameworks-corpus/` (EU AI Act 417 frozen provisions) ·
`evidence/` (append-only signed boards/receipts/ledgers).

**Drum ↔ monorepo:** the drum (`master-harness/knowledge/frameworks-drum/`) is the living
catalog/intake layer (555 items, MCP-served); `packages/frameworks` is the
verified-to-primary-source ground truth. Both are needed; the drum feeds the ground-truth work.

**Stays SEPARATE (mine-don't-merge):** the 18 Layer-0 bridge verticals
(cobol/cics/as400/fix/iso8583/hl7-fhir/scada…) and the *-ai-mcp verticals — they depend on
packages/receipts+core, never absorbed. [MEOK] hosting/model repos stay out entirely — CSOAI
measures, [MEOK] hosts; never host a model under the CSOAI monorepo.

**Top dedupes:** signed-receipt ×5 → one · MCP-count drift (843 dirs / 207 repos / ~200
marketplace → one registry) · crosswalk ×3 · 52-article charter ×4 · corpus-watch ×2 ·
Article-50 ×5 · retired-deploy shadow copies (csoai-static-deploy2 / kimi-regen / csoai-org-v2
/ csoai-platform) → quarantine + harvest + retire.

**Honest vaporware line:** the ~200 marketplace *-ai-mcp repos are 1 factory + N templated
stubs, not N products — do NOT fold on their names. Layer-0 "100/100 A+++++" is self-graded —
keep the real bridge code, strip the grade. Banned strings (sovereign/SOV<n>/CEASAI/byzantine/
BFT) are pervasive in donor material and MUST move to an internal-only tree (the
Dorado-in-cross.ts pattern); monorepo CI must inherit the drift-guard + brand-gate so a donor
can't reintroduce them.

## 7. Honest evidence ledger (so the doc can't be weaponised against us)

**Working note (2026-08-21, dual-walk discipline — operationalizes the audit stage, not a
charter amendment):** every consequential artifact gets a forward walker (builder) and a
backward walker (prover). The backward walk re-derives content ids and re-verifies signature
labels on a cadence — the estate checks its own homework in public (TEA×EAT; the mesh
`dualwalk` daemon covers signed boards; the drum's walker is `archive/dualwalk.py`, running in
the standing check + overnight). A signed artifact that fails its backward walk is an anomaly
logged loud, never silently repaired.

**[BUILT] real:** GovBench + 13 GSPC axes + held-out batteries · signed-receipts core (19/19
tests) · did:web:csoai.org trust root · the reg-deadline feed · fix_loop.py's measured
promote-if-generalised · the multi-agent evolve machinery · the framework-validation research
(`docs/RESEARCH_VALIDATION.md`) with its primary citations · the drum itself (555-item living
catalog, MCP/A2A/llms.txt wired).

**[BET] wagers (stated, not hidden, each carrying its strongest disconfirming evidence
inline — v1.3 adversarial-evidence rule):** human+AI complementarity → durable capability
gains (disconfirming: Vaccaro meta-analysis g = −0.23; surviving form: allocation, not
blending — §1) · evolve-and-keep-if-better at the knowledge/code layer (disconfirming:
domain-narrow successes + reward hacking 73.8% + rise-and-collapse; surviving form: evaluator
first — §3) · the substrate-inheritance thesis (disconfirming: ~40% built, ~200 stubs;
surviving form: finish+wire+dedupe first — §0).

**[GAP] not yet real:** the 90/10 conformal router (spec'd §4 — build is Stage 1) · the
durable Knowledge/residue archive · the visual/structural pattern detector over the card
corpus · a unified /evolve loop · the promote-gate eval set + canary (Stage 2). **No model
weights exist — full stop.**

## 8. Better wiring — concrete next moves (from the validation's stages)

**Stage 1 (build now — weeks):**
1. Implement the 90/10 router as a **frozen conformal-threshold predicate** over a small
   decorrelated ensemble's disagreement score; α = 1–5% auto-proceed error budget; measure
   realized coverage before trusting it. If realized error exceeds α on a fresh held-out
   slice, recalibrate or lower α.
2. Stand up the **Knowledge archive** (append-only, signed, lineage-tracked) as the
   residue/copy-and-improve substrate, reusing the Ed25519/did:web rail.
3. Collapse the loop to the **5 MAPE-K stages**; cut BRAND/VISUAL/QUALITY to a downstream
   consumer.

**Stage 2 (the promote-gate — weeks to months):**
4. Build the frozen, private, contamination-resistant eval set + regression pack +
   statistical-significance gating; wire in the UK AISI Inspect eval-receipt package already run.
5. Shadow → canary with automated rollback (any P0 regression or canary metric below the noise
   floor auto-rolls back).
6. Apply mergekit-for-knowledge/code ONLY as the evolutionary loop in one narrow verifier-rich
   domain.

**Stage 3 (scale carefully — months):**
7. Expand autonomy only after the promote-gate catches injected regressions in a red-team drill.
8. Route decision-making/high-stakes ambiguity to humans; scale/synthesis/tireless execution
   to AI. Budget realistically (~$22k/run at DGM scale); days-to-hours is real only for narrow
   verifier-rich tasks.

## 9. The market leg — [Dorado] doctrine (three boundaries, binding)

The evolved measurement data — the MAPE-K **Knowledge** archive — feeds the divergence layer
(internal codename [Dorado]): regulation × measured-AI × human-baseline composed against a
live market/index signal. Today the layer composes **regulation × measured-AI ×
human-baseline**; the **market/index leg is the genuine missing 4th**, honestly flagged
`NOT_PRESENT`. Composing measured AI-governance divergence against a live market signal is a
real differentiator — nobody measures regulation × AI-behaviour × human × market together —
that is the east-west spread. But three boundaries bind, and the third is non-negotiable:

1. **Composed, never fused.** Regulation and a bond price are not commensurable. The market
   leg is a **REPORTED context leg** — reported alongside, never blended into one number
   (the divergence layer's own doctrine). No single "score" mixing a governance distance and
   a market move.
2. **Licensed source before assertion.** The market leg needs a real licensed data source
   before it is asserted. It stays `NOT_PRESENT` until then, honestly — no Yahoo-ticker
   shortcut dressed as a data product.
3. **Never a trading signal or investment product.** Reporting governance-vs-market divergence
   as *context* is fine and valuable. Presenting it as a signal to trade on would be
   personalized financial advice — a hard line that is never built toward. **The divergence
   layer measures and reports; it does not advise or signal.** Keep it that way and it is a
   moat; cross it and it is a liability. This boundary is enforced in product design, not just
   wording.

## The real blockers (verified by drum live checks 2026-08-20 — NOT GCP)

1. **did:web split-brain (small, real):** apex csoai.org serves site-release-1 +
   estate-chain-1 + board-attestation-1; mirror councilof.ai serves those three **plus
   card-attestation-1** (live check: apex 3 keys, mirror 4) — the machine-contract split-brain
   guard trips on the mismatch. **Reconcile plan (one PR):** add `card-attestation-1` to the
   apex copy AND add the DSH key — **`o32UOkcsCnpSd5u-GALIWDTrpVY1ibxirnIWJrObb-w`, ready to
   publish as `did:web:csoai.org#dsh`** (env wired to the new seed; the `council_sign` CLI
   returned no JSON on that subcommand — a CLI-shape quirk to debug, not a key problem). The
   reconcile + #dsh PR is proposed; it fires on the deploy lane's go (deploy-lock on
   councilof-ai respected).
2. **estate-chain-1 private half stranded on the dead GCP VM:** don't recover — regenerate
   (F1 pattern) for anything that needs it. Public feeds move to the live board-attestation key.
3. **No key-continuity charter:** a monorepo whose value is a signing key needs succession as a
   first-class charter/doc.

---

*v1.4 — whiteboard + session summary, grounded by the deep-mine corpus map, corrected by the
literature validation, hardened by the adversarial-evidence rule (every [BET] states its
strongest disconfirming evidence inline), and aligned with the Claude lane: the [Dorado]
market-leg doctrine (three boundaries — composed never fused, licensed before assertion, never
a trading signal), the live-verified trust-root state, and the did:web reconcile + #dsh plan.
The 90/10 router — the crown-jewel gap — has a concrete, doctrine-compliant build spec (frozen
conformal predicate). The monorepo is ~40% already built (councilof-ai-monorepo, 55 packages);
the job is finish+wire+dedupe, and the real signing blocker is a small did:web split-brain,
not GCP. Next: Stage 1 (conformal router, Knowledge archive, MAPE-K collapse) becomes the
build queue.*
