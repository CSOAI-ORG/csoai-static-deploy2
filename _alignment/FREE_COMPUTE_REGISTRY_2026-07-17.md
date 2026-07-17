# FREE COMPUTE REGISTRY — verified 2026-07-17 (CC lane, 3 parallel sweeps)

**~70 catalogued. ~30 genuinely usable.** Every entry marked ✅ works / ⚠️ caveat / ❌ dead-or-gated.
Not padded to 100 — a dead link costs a wasted morning. This is what *actually* works.

## 🏆 THE HEADLINE — apply this week
**[UKRI AIRR Rapid Access](https://www.ukri.org/opportunity/isambard-ai-and-dawn-airr-supercomputers-rapid-access-route/)
— 20,000 GH200 GPU hours, FREE.** Eligibility: **UK-registered SME with a Companies House number.** No VC, no
academic affiliation, no equity. Open rolling, ~2 weeks, light-touch. **CSOAI Ltd qualifies exactly.**
This single item outvalues every hyperscaler credit tier combined. 3-month use window is the only constraint.

## 1. FREE GPU FOR TRAINING (LoRA/QLoRA 7B–14B)
| Platform | Real allowance | Card? | 7-14B? |
|---|---|---|---|
| ✅ **Kaggle** | **30 GPU-hr/WEEK**, T4×2 or P100, 9–12h sessions, background exec | No | **Best free option** |
| ✅ **Modal** | **$30/mo recurring** ≈ 12h A100-80GB / 51h T4 | No | **Yes — our proven substrate** |
| ✅ **Lightning** | 15 credits/mo = 10h A100-40GB (⚠️ "80 free hrs" is T4-only marketing) | No | Yes, 4h session cap |
| ⚠️ **Colab** | T4, ~12h session, **quota unpublished** | No | 7B yes, 14B marginal |
| ⚠️ **Intel Tiber** | free Gaudi2/Max JupyterLab, **no card** | **No** | Maybe (Optimum-Habana, not CUDA) |
| ⚠️ **Beam** | $30/mo claimed (**UNVERIFIED** — page now shows only Team $89) | Likely no | Yes if real |
| ⚠️ **TPU Research Cloud** | free TPU v4/v5 by application; **VM+storage billed to you** | GCP acct | Awkward (JAX/xla) |
| ❌ **SageMaker Studio Lab** | **CLOSING to new customers 30 Jul 2026** | No | Don't build on it |
| ❌ **Saturn Cloud** | **free tier appears GONE** (listicles are stale) | — | No |
| ❌ **Paperspace** | free = M4000 8GB Maxwell (decoy); usable GPUs need paid plan | — | No |
| ❌ **RunPod** | **no free tier** — bonus needs $10 deposit; "$500 free" is affiliate bait | Yes | No |
| ❌ **Cerebrium** | "Hobby Free" = free *platform fee*, **compute billed** | Yes | No |
| ❌ **Banana.dev** | **DEAD** (shut 31 Mar 2024) | — | — |
| ❌ Deepnote / Datalore / Replit / JarvisLabs / Replicate / Baseten / fal | no free GPU for arbitrary QLoRA | — | No |

## 2. FREE INFERENCE APIs — the 100B+ question
| Provider | Free allowance | Biggest free model | Card? |
|---|---|---|---|
| 🎯 **Groq** | 30 RPM / 1K RPD / 200K TPD | **gpt-oss-120B ✅ VERIFIED WORKING** (+llama-4-scout MoE, qwen3.6) | **No** |
| ✅ **NVIDIA NIM** | ~40 RPM | **DeepSeek-R1 671B, GLM-5 744B** | No (**phone verify** — likely our 403 fix!) |
| ✅ **OpenRouter** | 50 RPD (→1K with one-time $10) | **Nemotron 3 Ultra 550B** | No |
| ⚠️ **Cerebras** | **5 RPM** / 1M TPD (docs contradict every blog) | gpt-oss-120B | No |
| ⚠️ **Mistral** | 2 RPM / ~1B tok/mo | Mistral Large 3 | No |
| ⚠️ **Cloudflare Workers AI** | 10K neurons/day | Nemotron 120B | No |
| ⚠️ **Google AI Studio** | Flash ~1500 RPD | Gemini Flash (strong aggregator despite closed params) | No |
| ❌ **SambaNova** | **20 req/DAY** — useless for MoA | DeepSeek-V3.1 671B | No |
| ❌ **Cohere** | **non-commercial only** | Command A 111B | No |
| ❌ **Chutes** (free tier killed Mar 2026) · **Anyscale** (dead 2024) · **Together** (no real free tier) · **Fireworks/DeepInfra/Hyperbolic/Novita** (card/trial only) |

**⚠️ Stale-info warning:** the popular `free-llm-api-resources` GitHub list is WRONG in places (still shows
Llama-405B on OpenRouter, 30 RPM on Cerebras). Treat as discovery index, not truth.

## 3. CLOUD TIERS + CREDITS — what a bootstrapped UK founder ACTUALLY gets
| Program | Amount | Verdict |
|---|---|---|
| 🎯 **UKRI AIRR Rapid** | **20,000 GH200 hrs** | ✅ **APPLY — UK SME, no VC needed** |
| ✅ **AWS Activate Founders** | **$5,000** | bootstrapped is the *qualifying* condition |
| ✅ **Microsoft Founders Hub** | $1K → **$5,000** | self-serve, solo founders OK |
| ✅ **Google for Startups** | **$2,000** | bootstrapped tier |
| ✅ **NVIDIA Inception** | free + $10K DLI + **partner credits (Nebius AI Lift)** | no equity/fee — real route to 5 figures |
| ✅ **Modal Startups** | up to **$25,000** | no VC referral needed |
| ✅ **Intel Liftoff** | Tiber credits (amount UNVERIFIED) | no equity |
| ✅ **Oracle Free Tier** | ⚠️ **A1 ARM halved 4→2 OCPU Jun 2026** (our box is AMD micro — unaffected) | still best always-on free |
| ✅ **GitHub Codespaces** 120 core-hrs/mo · **Render** 750 hrs/mo (only surviving PaaS free tier) · **HF Pro $9/mo → 25min/day H200** |
| ❌ **VC-GATED — do NOT chase:** AWS Portfolio ($100–200K), Google $20–350K tiers, Oracle for Startups ($100K), MS $150K, CoreWeave (US-only?) — **all require a VC/accelerator on the cap table** |
| ❌ **AIRR Innovator** (50–150K GPU-hrs) — closed 16 Jan 2026; watch next cycle |
| ⚠️ **EuroHPC AI Factories** — UK eligibility **UNVERIFIED/contested**; worth one email to their helpdesk |

**Honest ceiling:** bootstrapped hyperscaler credits ≈ **$12K total**, not six figures. Anyone quoting $350K is selling something.
**Free tiers are contracting:** Fly, Railway, Gitpod Classic, Chutes, Anyscale all killed theirs; AWS swapped 12-months-free for 6-month expiring credits.

## The stack that actually works today (£0)
**Train:** Kaggle (30h/wk) + Modal ($30/mo) — stack monthly, no cards.
**Serve/infer:** Groq (gpt-oss-120B **free, verified**) + NVIDIA NIM (671B, once phone-verified).
**Always-on:** Oracle free VM (our `sovereign-hermes`).
**Next-level:** apply to UKRI AIRR → 20,000 GH200 hrs.
