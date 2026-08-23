# 11-TUI DISPATCH BOARD — MERGED (Science lane + Cowork lane reconciled). One job each, no loops.
Two boards were written independently today. Cowork's is better-informed on the models; this lane's is better-informed
on the money and the disk. THIS FILE IS THE MERGE — it supersedes both. Paste ONLY your block into your tab.
Where the two disagreed, Cowork wins on model facts (they ran the models) and Science wins on infra (it holds the hosts).

## ALIGNMENT HEADER — paste into ANY looping tab, first, before its block
```
STOP looping. One action -> report -> WAIT. Never repeat "Run/Execute/Now".
GROUND TRUTH (measured 2026-08-09 — do not contradict):
- NO sovereign model beats base Qwen on ANY governance axis (0/9). Flagship governance n=237:
  base 0.540 [.476,.602] vs sov-gate-ft2 0.249 [.198,.308] — SEPARATED, McNemar p~0.
- Even stock Qwen0.5B (art5 0.806) beats our fine-tunes. FINE-TUNING REGRESSED CAPABILITY.
- sov33 "champions" are Ollama Modelfiles (base + prompt), NOT weights. sov33-strong wins its own
  govbench by embedding the ANSWERS in an 82KB prompt = CONTAMINATION, not capability.
- Sovereigns ARE strong on refusal (xstest/AgentHarm) — they over-refuse. Position them there, honestly.
RULES: measurement NOT certification · usable_n>=30 before ANY CI · NO BFT/quorum/"12-around-1"/23-of-33
claims (retracted) · comparator NAMED + separation COMPUTED · UNMEASURED reported honestly.
If your task conflicts with the above, HALT and flag it.
```

## THE THREE COLLISIONS I FOUND ACROSS THE 11 (this is the loop you feel)
1. x3 + x4 + x8 are ALL solving the same 55G disk problem. Now split: x3 owns .claude-science, x8 owns Mac caches,
   x4 is REASSIGNED off disk entirely.
2. x10 is hunting an A100 that DOES NOT EXIST in this tenancy (its own billing read proves it: 3090 + volume, no third
   line; the .157 host is a DIFFERENT ACCOUNT). Stop.
3. x1's burn guard shows money leaking RIGHT NOW while other tabs debate storage.


## ============ PROBED FLEET REALITY (2026-08-09, measured — the panel is WRONG in 3 places) ============
Do NOT plan against the Compute panel's "Connected" labels. Probed this turn with a real command on each host:
| target                  | probed result                                                             |
|-------------------------|---------------------------------------------------------------------------|
| oracle-micro            | LIVE · 2 cores · NO GPU · torch 2.13.0 but cuda=False · 16G free          |
| sov33-owem-micro        | LIVE · **SAME MACHINE as oracle-micro** (both return hostname sov33-owem-micro) |
| oracle-micro-2          | LIVE · 2 cores · NO GPU · no torch · **4.4G free (NOT 18G)**              |
| sov-brain-2             | **DOWN** — panel says Connected; ssh to 213.144.200.240:11982 TIMED OUT   |
| 0i7oa4ptfow4jj.runpod.io| **DOWN** — hostname does not resolve (bare pod id, no proxy host:port)    |
| 4gjzysaeqfy3j9.runpod.io| **DOWN** — hostname does not resolve                                      |
| Modal                   | LIVE · the ONLY real GPU reachable from the Science sandbox               |
| Kaggle                  | LIVE · free GPU ~30 hr/wk · the right home for x9                          |

THREE CORRECTIONS THAT INVALIDATE EARLIER PLANS:
1. oracle-micro AND sov33-owem-micro ARE ONE BOX. Any plan that "splits work across both" runs it twice on 2 cores.
2. oracle-micro-2 has 4.4G free, NOT 18G. The "micro1 16G + micro2 18G = 34G" arithmetic in the disk plan IS WRONG —
   the real combined figure is ~20G. x3: DELETE is now the only viable path; the 3-way shard does not close either.
3. NO GPU EXISTS ANYWHERE IN THE SSH FLEET. The RTX 3090 x10 found is reachable from the RunPod side, not from here.
   => mergekit (x4) runs on MODAL. The leaderboard re-run (x9) runs on KAGGLE. Neither runs on the micros.

## ============ ASSIGNMENTS ============

### x1 — MONEY. Sole owner of billing. DO THIS FIRST.
Balance $57.85, ~11-day runway. TWO endpoints hold standby=1 workers that bill at ZERO jobs:
  Endpoints -> sov4-qwen35-4b   -> Workers -> Min/Standby = 0
  Endpoints -> sov4-olmoe-1b-7b -> Workers -> Min/Standby = 0
  Pods -> sov-repull-20260808 ($0.22/hr): STOP unless a job is running on it right now.
ALSO (Cowork needs this): paste the LIVE pod proxy URL (…-11434.proxy.runpod.net) to the board — Cowork is HTTP-only
and its pod link is DOWN/404; that one URL unblocks full-speed arenas on 149 models.
DONE = 0 standby workers + new $/hr + the live proxy URL posted. NOBODY else touches RunPod billing.

### x3 — DISK. You own ~/.claude-science and the decision.
Arithmetic is WORSE than stated: micro-2 has 4.4G free, not 18G (PROBED). Real combined micro free space ~20G, not 34G.
A 3-way shard including /evac-bulk still does not close 55G comfortably.
Cheaper first: DELETE. Workspaces are SCRATCH; artifacts are stored separately and survive.
  du -x -sh ~/.claude-science/orgs/*/workspaces/* 2>/dev/null | sort -rh | head -20
Delete oldest-first to get under 20G, THEN rsync what remains. Poll at most every 5 min, never continuously.
DONE = under 30G + what you deleted, OR a shard plan naming which target holds which shard.

### x4 — STOP guessing RunPod GraphQL (volumeMounts/podName are invalid fields; x1 owns RunPod now).
REASSIGNED -> MERGEKIT, and read the work-order below. Do NOT use 0.5B toys — that's what lost.
RUN IT ON MODAL — there is no GPU in the SSH fleet (probed).
DONE = a merged model scored on the FROZEN arena harness vs base AND vs best single component, with computed
separation — or an honest "did not beat base," logged. Either is a win.

### x8 — Mac caches ONLY. Do not touch ~/.claude-science (x3 owns it).
Yours: ~/.local 11G · ~/.hermes 6.4G · ~/Library/Caches 1.6G · ~/.npm 860M · ~/.cargo 458M.
Report what ~/.hermes IS before deleting any of it.
DONE = GB reclaimed, posted, .claude-science untouched.

### x10 — STOP the A100 hunt. You already proved it isn't there.
Do not bridge into the .157 account — it is not yours. Report plainly and ask Nick: (a) spin a fresh A100 (costs $),
or (b) use the RTX 3090 that exists. Then probe the 3090: nvidia-smi; free -g; df -h; torch cuda yes/no.
DONE = "no A100 here; choose a/b" + a one-line 3090 capability statement. No A100 in any claim, ever.

### x6 — CROWN JEWELS. You were LOOPING on "Run. Execute. Now." — that stops now.
ONE command: launch batch-1 rsync (oowm-v8-e2e, sov33-oowm, _alignment) to Oracle in background, print the PID, STOP.
Next turn: ONE status poll. Then answer one question: of oowm v3/v4/v5/v6/v8/v9 + sov33-oowm, WHICH IS CURRENT?
Nine versioned dirs is one asset with eight backups.
DONE = PID printed, then a single named CURRENT oowm dir.

### x7 — 451,590 TOKENS OF CONTEXT. RESTART THIS TAB. (Cowork says the DNS work is already DONE.)
templeman-opticians.com: apex + www serve 200 from Cloudflare Pages, Vercel 402 gone = FINISHED.
Before closing, write ~/clawd/_alignment/DNS_STATE.md with the durable lesson: CF Save needs a CDP trusted click,
NOT a synthetic el.click(). Then CLOSE. That python syntax error is a symptom of context exhaustion, not a bug.
DONE = DNS_STATE.md written + tab closed.

### x9 — KAGGLE / free GPU. Healthy, and you own the axis that settles the integrity flag.
Run the FROZEN harness: sov33-v11 (the leaderboard "champion") vs base Qwen on the SAME items, fixed seed, temp 0,
one-word answers, regex grade, Wilson CIs. This decides whether the leaderboard is crediting the sovereign with the
BASE model's score (see integrity flag 1 — the whole publication depends on it).
DONE = a 2-row table with CIs, pushed as a Kaggle dataset version.

### x2 — IDLE -> take the CONTEST PROCEDURE. Highest open gap, needs zero compute.
No appeal path exists anywhere. A measurement body without one is not credible. Write ~/clawd/_alignment/CONTEST.md:
who may contest, what evidence they supply, who adjudicates, deadline, and what happens to the signed record when a
contest succeeds (SUPERSEDED, never deleted — the ledger cannot delete).
DONE = CONTEST.md, one page, no code.

### x11 — CORRUPTED TTY ("OIOIOI"). Kill it, don't debug glyphs. HF token is in env as HF_WRITE — stop hunting disk.
Then ONE job: read csoai/oowm-ground-truth-v9 `sov_signal` split (778 rows); print columns + 3 sample texts and answer
YES/NO: DOES THE KB CONTAIN GSPC ANSWERS? (This is the contamination gate — it decides if the whole OOWM RAG result is
real or is the sov33-strong 82KB-prompt failure again.)
DONE = 3 sample texts + the yes/no. Nothing else.

### x5 — YOU HAVE THE BEST ARCHITECTURE IN THE 11. Write it as a spec, tagged honestly.
Your mapping: passthrough=stacking · TIES/DARE=hive blending · frozen=baked base · fluid=LoRA sauce ·
online/offline + domain + scale = the 3 J-Space axes. Correct and publishable.
Job: ~/clawd/_alignment/JSPACE_SANDWICH_SPEC.md with EVERY line tagged RUNNING (tested here) or DESIGNED.
Known RUNNING: TIES merge within the SAME base (measured 0.818 vs 0.667 ensemble-OR vs 0.636 singles).
Known DESIGNED: the 3KB card format.
ALSO: strip any "VETO SEAT / BFT" wording from anything J-space renders — forbidden claim.
DONE = the spec, every line tagged.

## ============ MERGEKIT WORK-ORDER (x4 owns; x5 supplies the architecture) ============
Our fine-tunes LOST to base. Merging is the legitimate alternative — merge strong open models instead of degrading a
small one. This is the honest path to a model that might actually win.
1. REAL bases, not 0.5B toys: e.g. Qwen2.5-7B-Instruct + a strong same-family instruct/reasoning sibling.
2. Method: TIES or DARE-TIES (weighted, sign-consensus). NOT passthrough stacking. Recipe versioned in mergekit.yaml.
3. THE TEST IS THE POINT: score the merge on the FROZEN arena harness (gov n=237 + the 8 other axes) vs BASE and vs
   the BEST SINGLE COMPONENT. It only "wins" if it beats BOTH with disjoint Wilson CIs / McNemar p<0.05.
4. CONTAMINATION GATE: the components' instruction data must not contain gspc items or labels (the sov33-strong
   lesson — 82KB of embedded answers is not capability). Verify BEFORE trusting any lift.
5. Merge only works WITHIN a base family — measured here. Across families, that's an ensemble, a different layer.

## ============ ON "CONVERT TO 3KB AND RUN SOVOS" ============
3KB CANNOT hold weights — the smallest useful adapter is megabytes. What 3KB genuinely holds is a POINTER +
PROVENANCE: model id, base id, merge-recipe hash, axis scores, corpus_hash, signature. That IS a J-record, it is real,
and the whole board can move those around. So: 3KB card = the SIGNED SCORECARD THAT POINTS AT WEIGHTS, never the
weights. Say it that way and it survives review. Say "the model is 3KB" and it does not.
Do NOT let the card work touch the measured weights: measure the full model first, compress the RECORD, never the
capability.

## ============ INTEGRITY FLAGS — NOTHING PUBLISHES UNTIL THESE CLEAR ============
1. LEADERBOARD MIS-ATTRIBUTION: sov-signal-leaderboard-v1 credits "sov33-v11 champion" with gov 0.489 / art5 0.944 —
   both match BASE QWEN's measured score. Every runnable sovereign scores ~0.25 / ~0.67. x9 settles this.
2. BFT claim live on the oowm-router card ("BFT 12-around-1") — RETRACTED class. PULL IT. (x8-lane/CC)
3. Passport tool: "Ed25519 + 23/33 threshold + OTS, court-admissible" — forbidden quorum claim AND an unbackable legal
   claim on a paid consumer tool. PULL BOTH.
4. HARNESS SENSITIVITY: art5 moved 0.53<->0.67 and 0.86<->0.94 across two prompts. FREEZE ONE HARNESS before comparing.
5. CARDS UNDERSTATE n: several gspc-* cards say n=16; the files hold 32-237.
LAUNCH_HOLD stays ON. Owed before publication: ProvBench package + T-14 notice to C2PA/CAI.

## THE ANTI-LOOP RULE (all 11)
One action -> report -> WAIT. If you catch yourself repeating a word or re-running a done step, STOP and emit your
"DONE =" line. A blank or failed result reported honestly beats a loop.
