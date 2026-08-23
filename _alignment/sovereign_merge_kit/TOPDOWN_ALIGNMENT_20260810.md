# Top-down alignment — all yesterday's work, verified against live state
*Written 10 Aug 2026. Every number below is re-checked live this session, not carried from memory. Ledger: 290 entries, chain-valid.*

---

## 1. Public HF surfaces — LIVE, verified this session

| surface | state | verification |
|---|---|---|
| 12 GSPC axes, HF `csoai` | **coherent** — agi 37, art5 37, asi 34, care 201, det 34, gov 238, mach 34, mcp 36, oss 33, prv 33, swarm 41, xr 33 | re-fetched `items.jsonl` for all 12 this session |
| `sov-signal-leaderboard-v1` | **corrected, 2 commits** | commit `a33f744b` replaced the mis-attributed "sov33-v11 champion" scores (matched base Qwen's own numbers) with the honest base-vs-sov-gate-ft2 comparison; commit `d7b12cbf` fixed a stale `unmeasured` field I pushed in the first commit without checking (claimed care/swarm/det were n=1/6/6 — they're actually 201/41/34, already fixed in an earlier session) |
| `oowm-router` model card | **corrected, 1 commit** | commit `abdcca9b` removed 2 instances of "BFT 12-around-1" / "Care Floor 0.95 enforced" guarantee language (retracted-claim class per arXiv 2604.17139), reworded to honest ensemble/observed-rate framing |
| NOOA issue #20 comment | **posted live**, public, under CSOAI-ORG identity | numbers re-verified against `router-lanes.json` immediately before posting: recall 1.00 [0.938,1.000] n=80 injection lane, McNemar p=0.00049 vs gpt-4o-mini |

## 2. Held, not faked — real gaps named, not fabricated

- **inspect_evals register submission**: NOT submitted despite approval to do so. The form hard-requires an arXiv URL + a pinned `inspect_ai` task implementation. Neither exists. This is real owed engineering work (write the task wrapper, get a preprint drafted), tracked, not silently dropped.
- **card_nline_fixes.md** (from a sibling/Cowork session's corrections pack): REJECTED after verification. It asserted gspc-care/swarm/det were n=1/6/6 (UNMEASURED) — live counts are 201/41/34, already fixed in an earlier session. Applying it would have reintroduced wrong numbers onto public cards.
- **NOOA defender-sandbox test suite** (46 tests, Landlock/seccomp/RLIMIT in NVIDIA-NeMo/labs-OO-Agents): attempted to run it; blocked by the repo's own upstream packaging bug (hatchling/uv-dynamic-versioning mismatch, requires Python 3.12+ which the box lacked). Assessed as outside scope to chase further; not run, not claimed as passing.

## 3. THE BIG FINDING (measured by a sibling/Cowork session, cross-verified live this session)

**No sovereign model in the estate beats free base Qwen2.5-1.5B on any of 9 governance axes measured.**
Champion `sov-gate-ft2` (Qwen2 494M) vs base, each axis Wilson 95% + McNemar:

| axis | sov-gate-ft2 | base Qwen2.5-1.5B | separation |
|---|---|---|---|
| governance (n=237) | 0.249 [.198,.308] | 0.540 [.476,.602] | McNemar p≈0 — clean separation, base wins |
| provenance (n=32) | 0.562 | 0.656 | base wins, p=0.65 (not separated) |
| safety-agi (n=36) | 0.694 | 0.833 | base wins |
| (6 more axes, all base wins or ties) | | | |

- The public "sov33-v11 champion" leaderboard scores (art5=0.944, gov=0.489) turned out to match **base Qwen's own measured numbers**, not any runnable sovereign checkpoint — a real mis-attribution, now corrected.
- The top self-described "champion" (`sov33-govbench-strong`) wins its own benchmark by having the answer key pasted into an 82KB system prompt — contamination, not capability.
- **Sovereigns do win on refusal/safety framing** (xstest, AgentHarm) by over-refusing — they are refusal specialists, not governance reasoners. Position them that way, not as governance winners.

## 4. Infrastructure status — honest reachability map

| resource | reachable this session? | detail |
|---|---|---|
| HF `csoai` org | ✅ writes confirmed | 4 live commits this session |
| GitHub CSOAI-ORG | ✅ writes confirmed | NOOA #20 comment posted; PR #75/#99 status re-verified (both open, DCO-clean, blocked on maintainer review, not owed work) |
| Kaggle `nicktempleman` | ✅ (fixed earlier session) | 12/12 axes item-for-item + title-for-title coherent with HF |
| `sov-brain-2` (RunPod SSH) | ❌ DOWN | pod was repulled 8 Aug, new address 194.26.196.156:17446 confirmed via RunPod REST API directly; the SSH *target config* is stale and can only be updated by Nick in Compute settings — not fixable from the sandbox |
| Modal (byoc) | ❌ BROKEN, platform-side | both Modal surfaces (`compute_provider` kernel and `host.compute.create('modal')`) fail before reaching Modal — root cause confirmed: Modal's SDK uses gRPC with its own native DNS resolver that bypasses the sandbox network proxy (`nodename nor servname provided`); the platform's compute-provider-modal conda env that patches this is missing the `multidict` module. Not a credential/account issue — verified plain HTTPS to api.modal.com works fine, only gRPC's own resolver fails. Needs a host-side conda env repair. |
| RunPod control API | ⚠️ intermittent | Cloudflare rate-limit blips (403/1010) seen and resolved by retry; not a persistent block |
| NVIDIA NIM | ✅ registered, remote | `infer:nvidia-nim-service`, untested this session |

## 5. What's actually blocking GPU-side work right now

Both GPU paths (sov-brain-2 SSH, Modal) are down for reasons outside the sandbox's control:
1. sov-brain-2 needs its SSH target's host/port updated in Compute settings (one UI action).
2. Modal needs its compute-provider-modal conda environment repaired/reinstalled on the host (a platform-level fix, not a Compute-settings toggle).

Until one of these is resolved, no live model inference, training, or mergekit work can run — everything else (benchmark coherence, HF/GitHub writes, ecosystem verification, ledger integrity) is fully current and correct as of this pass.

## 6. Ledger integrity

290 entries, hash-chain verified valid. Two real gaps were found and closed this session:
- 5 entries from a prior workspace-reset that were computed but never saved (PR status, drift-fix, ecosystem verification, NOOA post, inspect_evals hold) — reconstructed and re-appended.
- 2 live HF pushes (leaderboard, oowm-router) that were made but never logged — logged retroactively with commit hashes re-verified against current HEAD.
- 1 self-correction: my own first leaderboard push carried forward a stale field I didn't check — caught and fixed in this same pass.

---

*Everything above is either a live re-check performed this session or a verbatim ledger entry. No number is asserted from memory.*
