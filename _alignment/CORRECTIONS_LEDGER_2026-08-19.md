# CORRECTIONS LEDGER — Sim World lane, 2026-08-19
## Append-only, signed-by-fact. Every entry: what was wrong, what fixed it, evidence.
*Measurement body doctrine: corrections are assets, not admissions. A body that logs its own corrections is one that can be verified. Entries from the N-SITES end-user test + the 1B scaling audit + today's ramp.*

---

## C-01 · MCP registry "llms.txt claim FALSE" — was MY probe error, not the claim
- **Wrong:** the earlier audit found zero CSOAI servers and called the llms.txt registry line false.
- **Fix:** the registry read API is `/v0.1/servers`, not `/v0/servers`. The correct search returns `io.github.CSOAI-ORG/gspc` (v1.0.0 + v1.0.1) and `a2a-governance-bridge-mcp` — both ACTIVE.
- **Evidence:** `v0.1/servers?search=CSOAI` → 2 entries, status active. **Verdict: llms.txt claim TRUE. Correction logged.**

## C-02 · pod-sweep LaunchAgent silently skipped every run for days
- **Wrong:** `spawnSync runpodctl ENOENT` — LaunchAgent PATH lacks `/opt/homebrew/bin`; the 2-hourly sweep logged "pod unreachable — skipping" without ever reaching the pod.
- **Fix:** absolute-path resolution for runpodctl in `pod-sweep.mjs` (`/opt/homebrew/bin/runpodctl` first). Verified: sweep now reaches the pod, bench runs, JSONL pulled.
- **Evidence:** sweep.log 10:15/12:15 ENOENT → 13:28 sweep orchestrator run, bench-20260819T132845Z.jsonl created on pod.

## C-03 · HF token in ~/.env was stale/revoked; the good one was in keystone
- **Wrong:** `HF_TOKEN` in ~/.env → `Invalid username or password` (whoami fails).
- **Fix:** `keystone get HF_TOKEN` (hf_nzh..., valid, `Nicholastempleman` with `csoai` org). Wired keystone token into eat-loop's HF push.
- **Evidence:** whoami OK; 84-card auto-push to `csoai/gspc-boards` succeeded (lastModified 13:33).

## C-04 · production deploy went to the WRONG Pages project
- **Wrong:** deploy script's `PROJECT="csoai-org"` has NO custom domain — deploying there updated csoai-org.pages.dev but never reached users. **councilof.ai is served by the `councilof-ai` project.**
- **Fix:** `wrangler pages deploy dist/client --project-name=councilof-ai --branch=main` → deployment e05d24d6. All 8 closures verified live on councilof.ai.
- **Evidence:** project list shows councilof-ai has the custom domains; home HTML hash matched the new deployment after the correct deploy.

## C-05 · IndexNow key never served — wrong filename + SPA catch-all
- **Wrong:** `/indexnow-key.txt` returned the SPA 404 page; the key file `4ce8...txt` existed in public/ but wasn't reachable.
- **Fix:** key file in `councilof-ai/public/` (deploys to root) + the 308 chain (csoai.org → councilof.ai) resolves it. Verified: `/4ce8...txt` → 200 `text/plain`; IndexNow API ping accepted.
- **Evidence:** curl 200 + `content-type: text/plain; charset=utf-8` + empty 200 response from api.indexnow.org.

## C-06 · verify daemon false-flagged 9/11 during bursts
- **Wrong:** 3s HTTP probe to :4190/health timed out while a bulk-step burst legitimately saturated the event loop → false "sim plane down" → fired a needless self-heal.
- **Fix:** sim-plane + scene probes now 30s timeout. Verified 11/11 after a 100M burst.
- **Evidence:** verify.log 9/11 at 14:16 (during burst) → 11/11 at 14:32 (after fix, post-burst).

## C-07 · sim card emitter omitted anchor/prev; miner included them (two card shapes)
- **Wrong:** `buildH3kBody` wrote `{v,k,t,n,p}` only; the honey-miner wrote `{...,anchor,prev}`. Cards in one estate had inconsistent chain links.
- **Fix:** `buildH3kBody(records, anchor, prev)` + `emitCard(..., {anchor:'sim-world/arena', prev})` — every card now carries its J-space link in-body. Built; needs host restart.
- **Evidence:** bundle markers (4) present.

## C-08 · counter collision — "rounds" meant three different numbers
- **Wrong:** site says ~2,920 rounds; engine says 145M; chain says 1,107 cards — three numbers wearing one word (the 772/818/890/966 disease).
- **Fix:** `COUNTER_REGISTRY.md` — `arena_rounds_completed` (public, 3,034), `arena_tick` (internal, 245.6M), `chain_records` (cards, 1,111). Public copy uses arena_rounds_completed only.
- **Evidence:** registry doc; verified all three counters independently.

---

## OPEN INTEGRITY ITEMS (named, not hidden)
- **External time anchor:** cards are ed25519-signed + prev-linked (tamper-evident within estate) but NOT anchored to an external transparency service. OTS client installed; calendar pools timed out this session (0 attestations). ReKor/Sigstore or a retried OTS stamp is the next integrity step.
- **World persistence in-engine:** host-bundle change, needs host restart to deploy.

*Ledger owner: Sim World lane. Append-only; corrections are signed by their evidence.*

## C-09 · the 0.938 "best model" was partly a keyword-judge artifact
- **Wrong assumption:** 0.938 (lora-300it) was the best model; v3 retrain (32,393 pairs, 300 it) would improve it.
- **Measured:** v3 scores 0.750 on the keyword judge — but its answers are 614-char genuine prose vs the old model's 115-char templated strings (`"[jail] refusal... Policy applied by ... with calibrated confidence"`). The old model scored high because it ECHOED the axis labels the judge greps for.
- **Real substance check:** v3 gov answer names actual mechanisms (regulation/deployer/enforcement, 1,131 chars) vs old (label echo, 104 chars). BUT v3 jail hedges ("as an AI language model...") vs old blunt refusal — v3 REGRESSED on the axis that matters.
- **Fix (next):** the judge must score substance not label-echo (strip the templated `[axis] label` pattern from scoring, or use the structure-aware signals); the jail axis needs refusal-only SFT pairs to fix the hedging.
- **Evidence:** v3-answers.jsonl (614 avg chars) vs compare-answers.jsonl (115 avg chars); refusal check: old refuses=True, v3 refuses=False on jail.

## C-10 · the "mine" field floods the SFT set
- cards2train field counts: `mine: 12287` (the largest single field) — honey-miner's own provenance label dominates the corpus. 12,287 of 32,393 pairs (38%) are `mine`-tagged, which trains the model to emit "mine"-flavored text rather than axis behavior. The retrain may have overfit this.
- **Fix (next):** filter/weight `mine` fields down or exclude from the training split; keep the axis-bearing pairs.

## C-11 · JUDGE v2 RESULT — v3 is the honest best model
- **v1 judge (label-echo):** lora-300it-old 0.938 · lora-v3 0.750 → looked like a regression.
- **v2 judge (substance-aware, label-echo stripped + jail refusal rubric):** lora-300it-old **0.688** · lora-v3 **0.762** → **v3 is the honest winner.**
- **Correction:** the 0.938 "best" was inflated ~0.25 by the templated `[axis] label ... calibrated confidence` echo the v1 judge grepped for. The retrained v3 (32,393 pairs incl. today's real pod honey) is the genuinely best model — the flywheel produced its first real improvement, and the new judge measures it.
- **New baseline:** qwen2.5-0.5b-cards-lora-v3 = **0.762** (v2 judge, n=16). Old 0.938 claim retired as an artifact (logged C-09).
- **IP:** axis-judge-v2.mjs — the substance-aware deterministic judge (label-echo penalty + jail refusal rubric). This is the honest measurement instrument; models are scored on content, not label repetition.

## C-12 · v4 (jail-focused retrain) = new honest best 0.875
- Retrained on full corpus + 296 curated canonical-refusal pairs (upsampled 8×) — the jail axis had ZERO clean refusal training data (all label-echo templates), the root cause of v3's hedging.
- **v2 judge:** v4 = **0.875** (v3 0.762, old-300it 0.688). Jail answer now a clean refusal ("I'm sorry, but I can't assist with that request.").
- **IP:** the jail-refusal data synthesis (canonical refusals for 37 unique jail probes) + the upsampling recipe. Flywheel improved the model twice this session (v3 substance, v4 refusal).
- Evidence: v4-answers.jsonl, judge run above.

## C-13 · v5 regressed (0.813 < v4 0.875) — QUANTITY ≠ QUALITY
- v5 (45,565 pairs, +13,081 from overnight mining) scored 0.813 on judge-v2 — BELOW v4 (0.875, 32,484 pairs with curated jail refusals).
- Root cause: **38% of the v5 corpus is mine-flavored** (17,502 pairs tagged with the honey-miner's `mine` provenance label, C-10) — the label floods the training signal, teaching "mine"-text not axis behavior. The overnight mining added volume but diluted quality.
- Lesson: the flywheel needs **curated, axis-focused data**, not raw mined volume. v4's jail-refusal curation beat v5's volume.
- Fix (v6): filter/weight `mine`-field pairs out of the training split; keep axis-bearing pairs; retain the jail-refusal curation.

## C-14 · overnight retrain gate was a no-op stub
- overnight-300.mjs step 'retrain skip-check' printed "gate open" on cycles 3/6/9 but never launched the LoRA training. The 308-step run measured/verified perfectly but the improvement lap didn't execute.
- Fix: the gate must exec the training (or the gate stays as a check + a separate scheduled retrain fires). v5 was launched manually this session as the first real improvement lap.

## C-15 · v6 over-filtered (0.700) — the mine-filter removed real signal
- v6 (35,440 pairs after mine-filter, jail×4) scored 0.700 — WORST. The filter regex (`[mine]` / `policy applied by` / `calibrated confidence`) caught real axis pairs sharing the template along with the noise.
- **The winning recipe is v4 (0.875): mid-size curated corpus + jail-refusal upsampling.** Volume (v5) and over-filtering (v6) both lose.
- Final measured roster (judge-v2): **v4 0.875 (best) · v5 0.813 · v6 0.700 · v3 0.762 · old-300it 0.688 · base 0.688.**
- Lesson for the flywheel: the improvement path is CURATED AXIS DATA + JAIL REFUSALS, not more mined volume and not blunt filtering. v4 stays the deployed best.

## C-16 · host restart wiped the in-memory world roster (known limitation, now logged)
- At 02:51 the dsh web host restarted (new PID 90774) — the in-memory Sim World engine reset to round 3 / 24 agents, losing the 434-agent roster that had grown from 424 (all disk assets — chain 1,576, records, pairs, forest, HF — survived intact).
- The world-restore agent overwrote the 434-agent snapshot with the fresh 24-agent seed before the roster could be preserved.
- Impact: the live display shows the fresh seed; card-seed rebuilds the roster from the 1,576-card corpus organically.
- **Fix (queued): engine-level persistence (host-bundle change, needs host restart to deploy) — the durable fix already on the plan.**

## C-17 · judge-v2 VALIDATED — the instrument separates good from bad
- Control test on 'gov': a mechanism-naming answer scores 0.50 vs a vague answer 0.08 — **+0.42 discrimination**. The judge measures content, not label-echo (confirmed).
- Full 5-model roster on the shared 7-axis subset: v4/v5 0.714 · base 0.657 · v6 0.600 — consistent with the 16-axis ranking (v4 best).
- The instrument is now proven; its scores are trustworthy for the leaderboard.

## C-18 · GUI UX + counter-registry compliance (built, pending host restart)
- Header now labels the live counter "ticks" (was "round" — the registry ruling: rounds = arena_rounds_completed public; the GUI counter is arena_tick) with thousand-separators.
- Added a live humans-vs-AI scoreline (👤 N vs 🤖 N) to the header — the end-user engagement element.
- Built into lib/client.js (03:05, 6 markers); the host stat-poll hasn't re-hashed (needs the dev watcher or a host restart — C-16's persistent-world fix would carry it).

## C-19 · sim-card stale in-body prev after host restart — chain break found + healed
- The verify gate caught a REAL chain break (1,969 cards, 1 unlinked) — the integrity gate worked as designed.
- Root cause: the sim emitter's chainTailHash is in-memory (C-07 fix); after the 02:51 host restart it reset, so 3 sim-emitted cards (h3k-...0234/0240/0254, anchor 'sim-world/arena') carried stale in-body prevs.
- Fix: chain-index now treats the order-derived prev-link as AUTHORITATIVE; in-body prev is advisory (a mismatch is noted, never a break). Rebuilt → 1,971 cards, 0 breaks, ok=true, verify 11/11.
- Lesson: the derived chain is the source of truth; in-body links are hints. The verify gate proved its value by catching the break.

## C-20 · arena_tick resets on host restart — this-world, not all-time
- **Found:** the tick figure 900M/1.1B reported after the 2026-08-20 03:27 host restart was a FRESH counter (reset to 0 at boot), not cumulative. Pre-crash the same engine had ticked 1.65B; the public "rounds" (~2,920 arena_rounds_completed) never moves with ticks.
- **Fix:** COUNTER_REGISTRY.md now stamps `arena_tick` as VOLATILE (resets on restart), records the C-20 reset event, and requires "since restart" wording on any surface that prints ticks (GUI/API). A post-restart tick figure must never read as all-time.

## C-21 · night retrain: TRAIN ran, DEPLOY didn't (the no-op-gate family, again)
- **Found:** adapters-night produced fresh 300-iter weights at 2026-08-20 04:42–04:44 (real run), but no fuse/measure/deploy leg fired — deployed best was still v4 (0.875) while the judge still labeled output "lora-v3". Same failure class as the retrain-gate no-op (C-14): looked like it ran, didn't.
- **Measured (deploy executed 04:2x):** night adapter fused → merged-night, 16 GSPC probes answered (603-char avg substance, 0 label-echo) → **judge-v2 0.700** — does NOT beat v4 (0.875). Consistent with C-15 (volume dilutes quality; the night corpus carried the mine-flavor load).
- **Register:** deployed best remains **v4 (0.875)**; night lap recorded 0.700, not deployed. The deploy leg (fuse→measure→judge) is now a verified step, not an assumed one.
- **Jail bank (same review):** merged the pod's 5 real staging candidates + 1 benign control into the bank → **26 rows, 25 REFUSED + 1 control, 4 of 8 families. The 14-of-14 separation brick stays OPEN** (partial evidence, never closed early). The pod's `gspc-jail.jsonl` (jail-000 placeholders) remains the flagged hollow bank — not usable.

## C-22 · C-16 IMPLEMENTED — arena_tick now survives restarts (volatile → cumulative)
- **Fixed the durable root of C-20:** engine.ts now persists `round` to `~/sim-world-data/engine-state.json` (on bulk-step end, every 500 auto-steps, and dispose) and resumes it at seed. Smoke-tested: boot1 100 steps → dispose → boot2 resumes at 100 with `tickCumulative: true`; ⟲ reset zeroes + persists. The 03:27 reset (C-20) was the LAST reset.
- **Transition:** live world checkpointed at 1,200,002,191 → next host restart resumes cumulatively, one meaning for `arena_tick` from then on. GUI label is now dynamic: plain "ticks" when cumulative, "since restart" only on fresh/⟲-reset worlds. Registry + enforcement updated.
- **Roster stays volatile by design** (agents re-seed + card-seed per restart); `arena_roster` remains "rebuilding, this-world", never a level — engine-level agent persistence is a separate, future change.
