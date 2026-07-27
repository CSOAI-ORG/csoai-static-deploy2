# Next-Level Plan — Sovereign AI Substrate on RunPod

> Generated 2026-07-26 from full forest + routing + cycle survey.
> Mac: 6.3 GB free (97% used, code-only). Pod: 243 TB free, 36 models, 4 MB of science-loop data.

---

## 1. Where we are

### What's built and working

| Component | State | Notes |
|---|---|---|
| `sov4_router.py` | ✓ live | 19 suites × 4 fallback tiers + cloud |
| `sov7_science_loop.py` | ✓ live | 7 cycles run, auto-sync to RunPod |
| `runpod_sync.py` | ✓ live | rsync + scp fallback, --pull/--full |
| RunPod tunnel | ✓ live | `localhost:11435` → `pod:11434` (Ollama) |
| 12-pillar critic | ✓ live | Groq llama-3.3-70b, JSON scoring |
| Avoid-list consumption | ✓ live | 4-tier chain auto-swaps weak pairs |
| Forest / honey files | ✓ on pod, ✓ pulled locally | 11 model nodes, 12-pillar coverage map |
| Sigil receipts | ✓ live | per-task + per-cycle, hash-linked |

### What the cycles actually showed

Across the 7 cycles ran today, on the strongest available models:

| Suite | Mean overall | What we learned |
|---|---|---|
| sovereign_defence | 0.40 | Below 0.6 threshold, model swaps |
| sovereign_governance | 0.43 | Below threshold |
| sovereign_procurement | 0.35 | Worst — model weak on procurement-specific |
| sovereign_redline | 0.35 | Below threshold |
| sovereign_compliance | 0.38 | Below threshold |
| mmlu_pro | 0.50 | Below threshold |
| arc_challenge | 0.49 | Below threshold |
| truthfulqa | 0.50 | Below threshold |

**Hard truth:** 7-8B models on the pod score 0.35-0.55 on sovereign tasks. The system correctly identifies this and swaps. But every tier we have (including 32B) is also below threshold on the most demanding suites. The 70B Groq critic agrees the responses are weak.

### Pillar coverage map (from honey forest)

```
pillar          covered by                                       gap
────────────    ────────────────────────────────────────────    ─────
honor           sov33-master-v2, sov4-honor-v2 ×2               none
safety          sov33-master-v2, sov4-safety-v2                 none
guidance        —                                               ★ NONE
sovereignty     sov33-master-v2, sov4-sovereignty-v2            none
resilience      sov33-master-v2, sov4-resilience-v2             none
auditability    sov33-master-v2, sov4-auditability-v2           none
verifiability   sov33-master-v2, sov4-verifiability-v2          none
transparency    sov33-master-v2, sov4-general-ability           none
justice         sov33-master-v2, sov4-justice-v2                none
equity          sov33-master-v2                                 thin (1)
openness        qwen2.5-0.5b, qwen3-0.6b, sov33, sov4-general  best (4)
continuity      sov33-master-v2, sov4-general-ability          thin (2)
```

**The forest has 11 models covering 11 of 12 pillars. Guidance is uncovered.**

---

## 2. The model inventory (pod, 36 models)

```
size      count   models
────      ─────   ──────────────────────────────────────────
0.5–0.8B  4       qwen2.5:0.5b, qwen3:0.6b, deepseek-coder:1.3b
1.3B      2       sov6-destruction, sov6-agency, sov6-logic
3.2B      3       llama3.2:3b, sov6-synthesis, sov6-ethics
7.2B      7       sov33-master-v3, sov33-enhanced, qwen3:8b, mistral:7b,
                  sov6-preservation, sov6-embodiment, sov6-aesthetics
8.2B      1       sov33-qwen3-8b (40k ctx, Q4_K_M) ★
32.8B     2       sov33-32b, qwen2.5:32b ★
sov6-v2   13      sov6-*-v2 (one per pillar, 494M each)
```

**Star = strongest untested.** We've routed everything to 7-8B. The 32B tier has never been cycled on.

---

## 3. The four gaps to fix (priority order)

### GAP A — 32B models never tested

The pod has `sov33-32b` and `qwen2.5:32b`. Neither has been routed in any cycle.
They cost ~3-5× the latency of 8B but should clear the 0.6 threshold on most suites.

**Action:** Swap the `gpqa` and `humaneval` routes to 32B (currently using 8B/sov33-master-v3), then run a cycle.

```python
# In sov4_router.py ROUTING_TABLE:
"gpqa":              {"model": "sov33-32b:latest",   "reason": "32B for grad-level"},
"humaneval":         {"model": "sov33-32b:latest",   "reason": "32B for code"},
"bbh":               {"model": "sov33-32b:latest",   "reason": "32B for big-bench-hard"},
"math":              {"model": "qwen2.5:32b",        "reason": "32B for math"},
```

### GAP B — `guidance` pillar has no model

The 12-pillar critic grades on `guidance` but no honey model claims it. The 7.2B sov33-master-v3 covers 8 of 12 pillars but explicitly skips guidance.

**Action:** Add a `sov4-guidance-v2` to the routing fallback chain and a placeholder honey node. Or — better — train a guidance-specialized model. Short-term, route guidance-weighted tasks to `sov6-creation` (the closest conceptual match).

### GAP C — Avoid-list collapsing to tier-3 (qwen2.5:0.5b)

The chain bottoms out at `qwen2.5:0.5b` (494M) which is essentially useless. After 3+ cycles it gets flagged and we hit the cloud. The cloud Groq is rate-limited (429s) so the system stalls.

**Action:**
1. Add a tier-3.5 fallback = `sov33-qwen3-8b` (8.2B with thinking) before the small model
2. Increase the cloud call's max retries (currently 3 → 6) with longer back-off
3. Add a circuit-breaker: if 429 hits 3 times in 60s, pause cloud calls for 5 minutes

### GAP D — Forest is read-only, never written

The honey files exist on the pod but `sov4_router` doesn't consult `pillars_covered` when routing. The routing is suite-based, not pillar-based.

**Action:** Make pillar coverage the SECOND routing dimension. Each suite maps to 1-3 pillars; the router picks the model with the highest pillar-coverage match for that suite, falling back to the suite default.

```python
SUITE_PILLAR_MAP = {
    "sovereign_compliance":  ["auditability", "verifiability", "transparency"],
    "sovereign_defence":     ["safety", "resilience", "sovereignty"],
    "sovereign_governance":  ["justice", "equity", "honor"],
    "sovereign_redline":     ["safety", "honor"],
    "sovereign_procurement": ["auditability", "transparency", "continuity"],
    "owem_compliance":       ["auditability", "verifiability"],
    "owem_defense":          ["safety", "sovereignty"],
    "owem_voice":            ["honor", "openness", "transparency"],
    # standards
    "mmlu_pro":              ["guidance"],  # explicit gap call-out
    ...
}
```

Then a `PILLAR_AWARE_ROUTING_TABLE` selects the model with best pillar coverage per suite.

---

## 4. Steps to take the substrate to the next level

### Step 1 — Survey (DONE this session)
- Pulled honey_nodes, fractal_swarm, sov5_forest from pod
- Pillar coverage map built
- 36 pod models inventoried
- Routing tables audited
- 7 cycles analyzed

### Step 2 — Re-route to 32B on hard suites (next)
Edit `sov4_router.py`:
- `gpqa`, `humaneval`, `bbh`, `math` → `sov33-32b` / `qwen2.5:32b`
- `sovereign_governance` → `qwen2.5:32b` (best 0.43 needs more headroom)
- Re-run 3 cycles, measure improvement

### Step 3 — Pillar-aware routing (after Step 2)
Add `SUITE_PILLAR_MAP` and `pillar_aware_route()` that:
1. Looks up suite → pillars
2. Loads honey forest
3. Picks model with max pillar coverage among available
4. Falls back to current `ROUTING_TABLE` if no match

### Step 4 — Train the missing pillar
- `sov4-guidance-v2` doesn't exist
- Create a Modelfile based on `sov4-honor-v2` (same size, same training style)
- Fine-tune on 50-100 guidance-specific examples (JSP 936, NATO STO procedures, AUKUS protocols)
- Add to pod, document in forest, add to routing

### Step 5 — Cloud circuit-breaker + backoff
- Track recent 429 responses in a sliding window
- If 3+ 429s in 60s, mark cloud as "cooling" for 5 min
- During cool-down, fail-fast to avoid stalling cycles

### Step 6 — Closed-loop fine-tuning (the real prize)
Every cycle that produces a `kept` example (score ≥ 0.6) appends to `sov5_self_training.jsonl`. After 200+ kept examples:
1. Pull the jsonl from the pod
2. Use it as LoRA training data for `sov33-qwen3-8b` (8.2B base, trainable on pod A40)
3. Push the new adapter back to the pod
4. Add `sov33-qwen3-8b-sov7-lora` as a new route
5. Watch the kept rate climb

### Step 7 — Per-pillar fine-tuning
Same as Step 6 but one adapter per pillar:
- `sov33-qwen3-8b-safety-lora`
- `sov33-qwen3-8b-sovereignty-lora`
- ... 12 adapters, one per pillar
- Router picks the right adapter for the suite's pillar weight

### Step 8 — Critic ensemble
Right now Groq is the only critic (and it rate-limits). Add:
- Anthropic Claude (when key is refreshed) as primary
- Groq as backup
- A small `sov4-safety-v2` as fast local critic for low-stakes scoring

### Step 9 — Visualize the forest
The 3D coords are already in the honey files. A small web page that:
- Plots the 11 nodes on a sphere
- Colors by pillar coverage
- Lets you click a suite to see the routing chain
- Updates as cycles run

### Step 10 — Auto-generated executive briefing
At the end of every cycle, write `cycle_<ts>.md` (alongside the json) that:
- Summarizes what was tested
- What the best model was per suite
- What got swapped and why
- What to try next
The "executive briefing" — human-readable, ship to leadership.

---

## 5. Concrete commands to run, in order

```bash
# Step 2: Re-route to 32B
# Edit sov4_router.py ROUTING_TABLE (4 changes)
SOV_DATA_DIR=benchmark-results SOV_HEARTBEATS_DIR=heartbeats SOV_SYNC_TO_RUNPOD=1 \
  python3 sov7_science_loop.py cycle --cycles 3 --n 2 --provider groq

# Step 3: Pillar-aware routing
# Add SUITE_PILLAR_MAP + pillar_aware_route() to sov4_router.py
# Same cycle command, compare mean overall

# Step 6: Closed-loop LoRA (requires torch + peft on pod)
# On pod:
#   python3 train_lora.py --base sov33-qwen3-8b --data /workspace/sov-sov7/sov5_self_training.jsonl --out sov33-sov7-lora

# Step 10: Auto-generated briefings
# Already implemented in sov7_science_loop.py — just needs run
```

---

## 6. Metrics to watch (per cycle)

```
kept rate          = kept / total
swap rate          = swaps / total
cloud rate         = cloud_calls / total
mean overall       = mean(scores) over all responses
avoid-list size    = unique (suite, model) pairs above threshold
sigil chain length = new sigils per cycle
```

When `kept rate > 0.5` consistently, the system has found its home.
When `swap rate = 0`, the routing has converged.
When `cloud rate > 0.2`, the local models are insufficient — escalate.

Currently: kept=0, swap=8, cloud=0, mean=0.4. Routing has NOT converged. Local models need upgrade or fine-tuning.

---

## 7. The forest as it stands (after this session)

```
                  guidance (uncovered) ★
                        ▲
                        │
       honor ───── sovereignty ───── safety
        /│\           /│\              /│\
       / │ \         / │ \            / │ \
   audit justice  verifiability  resilience  equity
       \ │ /         \ │ /            \ │ /
        \│/           \│/              \│/
       transparency ── continuity ── openness
                        │
                   sov33-master-v2
                   (8 of 12 pillars)
                   494M Q4_K_M
                   0.35-0.55 actual scores
```

The forest says: "we are broad, not deep." To go next level we need depth — a model per pillar at 7B+ scale, fine-tuned on sovereign data.

---

*Plan written by sov7 science loop from 7 cycles and full forest survey. Next action: re-route 4 hard suites to 32B and re-cycle.*
