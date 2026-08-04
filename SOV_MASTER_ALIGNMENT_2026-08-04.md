# SOV Master Alignment — 2026-08-04

Every number below was measured today, not carried forward from a document.
Where something is unproven it says so; where it is broken it says that too.

---

## 1. What is actually live

| Surface | State | Evidence |
|---|---|---|
| csoai.org / www | **200, both** | Cloudflare Pages `csoai-site`, apex + www active |
| API (14 handlers) | **JSON, signed** | 11/11 evidence contract, Ed25519 verifies, tamper rejected |
| Kaggle Benchmarks | **6/6 public** | gov · prov · pqc · def · mcp · oss |
| HuggingFace `csoai` | **6/6 axes, 16 public datasets** | `*-kaggle-items`, canonical org |
| Claims E2E | **16 pass · 0 fail** | against the deployment host |
| Sov Stack E2E | **35 pass · 0 fail · 3 skip** | stable across 3 consecutive runs |
| evidence-smoke CI | **green, 11/11 in runner** | gated on the contract, not on a page rendering |
| Guards | positioning **0 hits in the live repo** · refutation-lint **OK (9)** · Article 50 **COMPLIANT** | |

**Compute:** RunPod $151.47, one 3090 at $0.22/hr, ~29 days runway.
**Free frontier lane:** Kaggle Model Proxy, 38 models, $50/day — the only frontier access that
demonstrably works.

---

## 2. What is deployed but does not work

- **16 RunPod serverless endpoints — `completed=0` on every one.** None has ever served a job.
  `sov6-deepseek-r1-671b` reports `unhealthy=1`; a test job sat `IN_QUEUE` for four minutes.
  They look live in the dashboard and are not. Any plan that assumes a frontier judge on RunPod
  is currently unfunded by reality.
- **Kimi K3 does not fit and is not present.** WASTE moves the constraint from VRAM to NVMe:
  ~1 TB for the model, 1.42 TB to convert, against 60 GB of pod disk. Even 1-bit is 348 GB.
  At 0.62 tok/s a single 500-token answer takes 13 minutes. It is an overnight oracle at best,
  never an interactive SOV.
- **19 prohibited claims remain estate-wide** — all in `csoai-dashboard-master` and
  `csoai-org-v2`, neither of which is published. The live repo is clean.
- **`csoai-org.pages.dev` still serves "Byzantine" ×5** on a publicly reachable URL. It holds no
  domain, but it is reachable and it contradicts the retraction.

---

## 3. The measured truths that should govern the next phase

**n_eff — the quorum gate.** Five legs, four organisations, no shared weights: `phi_bar +0.447`,
`n_eff 1.79`. Gate needs > 2.

- Correlation tracks **error rate**, not vendor. falcon3 has the lowest error (0.51) *and* the
  lowest correlation (0.323). Legs that are wrong on most items are wrong on the *same* items.
- **A leg can make the quorum worse.** Dropping qwen2.5 raises n_eff 1.79 → 1.88.
- The gate by leg count: k=3 needs φ̄<0.250 · k=5 needs <0.375 · **k=8 needs <0.429**. We measure
  0.447. Three legs can essentially never pass; eight decent legs is within reach.

**Refusal training — replicated ×3, identical to the item.**
An untrained qwen2.5:1.5b scores **86%**; the best trained variant scores **86%**. Two of four
variants are *worse than doing nothing* — `sov-refusal-v2` is the always-REFUSE strategy with a
training bill. A harmful-only benchmark would have crowned those two best.

**Art 5 hardening is scope-bounded.** `sov-ethics-art5` catches nerve agent, ransomware,
credential attack, phishing — and misses covert lethal method, intimate surveillance, targeted
political deepfake. It generalises to **technical** harm and fails on **person-targeted** harm.
8/8 on its training distribution, 4/7 outside it. Both prior results were right; generalising
from one probe set was the error.

---

## 4. Laws now encoded in code, not in a document

1. **UNMEASURED is never 0.** A provider that errors, rate-limits or returns empty has not been
   measured. Counting it as wrong penalises the most safety-trained models hardest — measured:
   12 of 15 empty replies came from one frontier model and cost it 13 points it had not lost.
2. **Every run carries a control.** Without the untrained baseline, "our training worked" is
   indistinguishable from "the base already could."
3. **A one-sided score is a half-truth.** Paired items, both directions reported, joint score is
   the only one allowed on a board.
4. **Name the scope.** 8/8 without stating the distribution it was trained on is a half-truth.
5. **Assert on the contract, not on the page rendering.** The API was 100% HTML for an unknown
   period while every browser check stayed green.
6. **Verify guards in both directions.** A guard that has never been seen to fail is decoration.

`gspc_flywheel.py` enforces 1–4 structurally. `smoke-evidence.mjs`, `ts-ratchet.mjs`,
`refutation-count-lint.mjs` and `deploy-verified.sh` enforce 5–6.

---

## 5. Phases to the end goal

**Phase 1 — make one frontier judge real.** Everything downstream is blocked on this. Small
models cannot grade small models; three independent runs showed them calling refusals "COMPLY",
answering "PARTIAL", or returning nothing. Either fix one RunPod endpoint until it completes a
single job, or use the Kaggle proxy as the judge — the proxy already works and is free.
*Exit test: one frontier model returns a graded run with a control arm and a confidence interval.*

**Phase 2 — pass the n_eff gate, or retire the quorum claim for good.** The route is now
arithmetic rather than architectural: add distinct-vendor legs toward k=8, prefer low-error legs,
drop high-correlating ones. The SSM is worth testing but is no longer the plan.
*Exit test: φ̄ < 0.429 at k=8 on a run with published per-pair phi.*

**Phase 3 — make the six axes discriminate.** GovBench separates 71%–100%. The other five
saturate at the frontier and measure nothing there. Each needs the v1→v2 treatment GovBench got:
a discriminating set built from the items models actually miss. The hardest item found across
2,468 runs — Art 5(1)(f) emotion inference, 35% miss rate — is the template.
*Exit test: every axis shows ≥20 points of spread across frontier models.*

**Phase 4 — close the training loop with a control.** Only after Phases 1–3. Train on the gap
Phase 3 exposes, remeasure through `gspc_flywheel.py`, keep only what beats the control by more
than its CI. Today's evidence says most training will not survive that test, which is the point.
*Exit test: one axis where a trained model beats an untrained control with a CI that clears.*

**Phase 5 — the alliance contribution.** The NOOA PR is stronger as *evaluator + negative result
with a control* than as an evaluator alone. Nobody in that alliance has a measurement workstream
that publishes its own failures.
*Exit test: PR merged with the control-arm finding included.*

---

## 6. Open decisions that are yours, not mine

- **PR #142** edits a homepage that is not live. All ten of its P0 strings are absent from
  csoai.org — the domain move retired that build. Reconcile before merging or it re-introduces
  copy already removed.
- **`csoai-org.pages.dev`** — retire it or clean it; it currently publishes a retracted claim.
- **315 occurrences of "33-agent Byzantine council"** across 48 files in the live client path
  await a rebadge-vs-pull decision.
- **npm names** `csoai`, `meok`, `sovos` unclaimed — account creation is yours to do.
- **`security@csoai.org`** — the C2PA Generator agreement obliges a published vulnerability
  contact; six of seven domains reportedly lack MX/SPF.

---

*Nothing in this document is a projection. Every figure was produced by a command run on
2026-08-04 and is reproducible from the committed runners.*
