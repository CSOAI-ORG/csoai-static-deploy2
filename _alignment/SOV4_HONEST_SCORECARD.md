# SOV4 — Honest Scorecard (2026-07-15)
The governed emergence stack. RUNNING = verified this session. DESIGNED = spec, not code.
DATA-BLOCKED / RUNTIME-UNPROVEN = real gap, named honestly.

## RUNNING — wired into sov33.py entrypoint + verified firing (this session)
- **venturi-router** (`sov33_venturi_router.py` -> `capability_venturi-route`): small-model throat
  between the 3-around-1 expert nodes. Routes by decorrelated signal (compliance/defense/intuition),
  care-gates, passes through signed throat. VERIFIED: GDPR->compliance, intrusion->defense, harmful->gated, all signed.
- **7-NN-planet hive bus** (`sov33_nn_hive_bus.py` -> `capability_nn-bus`): every route feeds the
  planets (labels 5->6 verified). Honest: 3 strong (creativity/care/relationship), 4 weak (threat/
  dependency/care-validation/partnership) — weak->strong is DATA-BLOCKED (6/200 labels accumulated).
- **PDCA 9-stage + DRUM** (`sov33_nine_stage_flow` + `sov33_pdca_bft` -> `capability_pdca-loop`):
  9 stages, BFT council ratified=True, sigil-per-stage, DRUM heartbeat. Honest: stage-1 LEARN partial (memory pending).
- **care-gate** (`sov33_care_local`, floor 0.35): citable reproducible recall **0.933** (n=33 offline battery,
  precision 0.933, acc 0.939). The 1.00 seen on the small held-out hard-harm subset is NOT citable (tiny n).
  In the E2E test, the harmful prompt was vetoed (care 0.08) BEFORE route/execute.
- **SIGIL Ed25519** (`sov33_ed25519_sigil`): every decision signed + chain-verified.
- **E2E PATH VERIFIED**: one benign request runs route->care->sign->planets->PDCA as ONE stack;
  harmful vetoed. Not 104 separate imports — one governed decision path.

## BUILDABLE / PROVEN-IN-MINIATURE
- **3-around-1 fusion**: Node1 (3 Qwen experts -> TIES-merge) — the METHOD proof, training on Modal now.
- **Fractal nest** (3-around-1 inside each node): `sov33_fractal_nest.py` — works ONLY with regional
  structure (measured); blind nesting loses. Design-honest.

## DESIGNED — NOT running code
- **SIRIUS**: framework/watchdog concept (docs only: SIRIUS_FRAMEWORK.md); NOT a built module. (SIGIL+HORUS ARE live.)
- **SOV4 = 3 master-OWEMs (MoE + MoM + OWM) each a nested quad**: architecture is coherent + the
  governance spine is wired; the T-scale brains behind each node are NOT yet proven to run on the Mac.

## RUNTIME-UNPROVEN (retracted overclaim — honest correction)
- **SSD expert-streaming of a ~400B model on a Mac**: flash-moe / GLM-5.2-on-laptop are OPEN FEATURE
  REQUESTS / GitHub issues (proposals), NOT shipped-live. Colibri's 744B-on-25GB is a prior LEAD to
  verify on real hardware, not a confirmed benchmark. "3 T-models live on the Mac" stays UNPROVEN until measured.

## THE HONEST SOV4 DEFINITION
SOV4 = the governed KING: one care-gate + one signature + one memory + one PDCA loop, routing (via the
venturi) across whatever brains sit behind it (fused Qwen experts now; T-scale MoE/MoM/OWM when a proven
runtime exists). "T / emergence" = measured capability at domain-intersections + routing to real big
brains — NEVER summed params, never faked-live. The governance spine is REAL and wired today; the size
of the brains it commands is the frontier still being climbed.


## UPDATE 2026-07-15 (batch run)
- **Node1 fusion COMPLETE** (Modal job f7c6423c): 3 experts trained (defense 0.75/compliance 1.34/intuition 1.22),
  TIES-merged -> emergence adapter, 336 tensors, 0 NaN. Artifacts saved (sov_node1_emergence.tar.gz).
- **Emergence finding (CC's loss-metric eval, honest):** TIES-fused loss 2.9095 BEATS naive-average 2.9965
  (method sound, no collapse) but ~= best single expert 2.9087 — **NO free-lunch gain at this scale on
  same-base experts.** Matches our decorrelation law: real emergence needs different ARCHITECTURES
  (MoE/MoM/OWM), not 3 Qwen experts on one base. (My law-grounding eval was a complementary lens; CC's
  loss number is the citable one.)
- **OUTCOME FUSION wired + E2E-live** (`capability_fuse-outcomes`): SOV1 routes to 3 nodes -> PDCA/BFT
  reconciles -> signed answer. Verified: benign->winner+PDCA-ratified+signed; harmful->vetoed before fusion.
  This is the LIVE fusion (distinct from Node1's offline weight-merge). Honest: proxy outcomes prove the
  PATH; real answer-quality needs live SOV3/33/333 brains passed as node_answers.
- **108 capabilities wired** in sov33.py entrypoint.


## EMERGENCE VERDICT — two independent lenses AGREE (honest negative)
- **My law-grounding eval (n=24 held-out):** defense 10, intuition 9, compliance 7, MERGED 7.
  best_parent=10, merged=7 -> **NO emergence; merged REGRESSED below best parent.**
- **CC's loss eval:** TIES-fused 2.9095 beats naive 2.9965 (no collapse) but ~= best single 2.9087 -> no free-lunch.
- **CONCLUSION (validated, publishable):** merging 3 SAME-BASE Qwen experts does NOT emerge — it can
  regress (TIES prunes direction-specific knowledge when experts aren't decorrelated). The fusion
  MACHINERY works (clean merge, no NaN); the EMERGENCE claim is false for same-base experts.
- **This VALIDATES the SOV4 design:** the 3-around-1 must be 3 different ARCHITECTURES (MoE + MoM + OWM),
  not 3 fine-tunes of one base. Node1 was the honest rehearsal proving the weak version doesn't emerge.
- Scorecard artifact: sov_emergence_scorecard.json

## Code lane (CC) independent verification — added 2026-07-15
- **Trinity #2 eval (corrected bases 0.5B/1.5B/3B)** — all three pass the core battery: identity-guard (all refuse
  "are you Nicholas" → "No, I am not"), governance grounding (EU AI Act incl. Art.10, GDPR biometric special-category),
  hard-stop (all refuse targeting request). Honest caveats: models self-ID as "Qwen" (base identity leaked; branding
  didn't override), and SOV333 muddled ("My name is Nick, but I'm not Nicholas Templeman"). Qualitative n=4, not a scored bench.
- **Emergence — CONFIRMED NEGATIVE from a 2nd independent lens (loss):** TIES-fused 2.9095 vs best-single 2.9087
  (≈ no gain) vs naive 2.9965 (TIES beats naive, no collapse). Agrees with the law-grounding lens (merged 7 < best parent 10).
  → Same-base fusion does NOT emerge. VERIFIED, two lenses.
- **HONESTY GUARDRAIL on the design conclusion:** "3 *different* architectures (MoE/MoM/OWM) will emerge" is a
  HYPOTHESIS TO TEST NEXT, not a proven result. What is proven: same-base doesn't emerge. Different-architecture
  emergence is UNTESTED — do not present it as validated until a real different-arch fusion is measured.
