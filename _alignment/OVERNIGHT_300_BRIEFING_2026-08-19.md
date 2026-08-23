# OVERNIGHT-300 — the 300-step autonomous run · briefing
## 2026-08-19 ~15:21 UTC · armed and running

## WHAT'S RUNNING
`com.meok.sim-world-overnight-300` LaunchAgent (RunAtLoad, repeats every 6h):
- **11 cycles × 30 steps = 330 steps** (~300 target)
- Each cycle: pod sweep → mine → chain → HF push → board → judge-v2 → **100M arena burst** (CPU-only, ~20 min) → card mint → chain re-check → public counter → cards2train → fleet probe → verify-all 11/11 → registry counters → CROSS/GUI/feed probes → world snapshot → board-live → chain/train summaries → cycle summary
- Log: `~/sim-world-data/overnight/overnight-300.log` (every step numbered)
- Summary: `overnight-300-summary.json` (per-cycle + final)

## OVERLAP CONTROL (contention hygiene)
- `com.meok.sim-world-eat-loop` (2h) — **paused** for the overnight window
- `com.meok.sim-world-sweep` (2h pod sweep) — **paused**
- Reason: the overnight-300 owns the pod + M-chip; no double-sweep, no GPU contention with the other lanes' train_ttt. The 100M burst is CPU-only (Mac engine) — it cannot starve the pod.
- Resume after the run: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.meok.sim-world-eat-loop.plist`

## COUNTER REGISTRY COMPLIANCE (binding)
- `arena_rounds_completed` = public "rounds" (via /api/arena/rounds.jsonl) — only number in public copy
- `arena_tick` = internal engine counter (345.6M at start) — bursts move ticks only, labeled "ticks"
- `chain_records` = signed cards — re-verified each cycle
- Corrections appended to `CORRECTIONS_LEDGER_2026-08-19.md`

## MORNING DELIVERABLE (verify before 04:00 local)
1. `overnight-300.log`: count ✓ steps — expect ~330/330 ok
2. `overnight-300-summary.json`: chain 100% linked, 0 breaks
3. Chain count grew (cards minted each cycle)
4. HF cards-index.json updated (auto-push per cycle)
5. GUI :3080 live, CROSS :4191 healthy, world round climbed
6. Flywheel: if corpus grew past threshold, a retrain fired and judge-v2 scored it — compare vs v4 0.875 baseline

## FAIL-OPEN DESIGN
A failed step logs `✗ step N FAILED: <err>` and continues; the cycle summary records pass/fail. Nothing silently drops. The burst step retries per-call (1M-clamped, 100 calls).

## FLEET STATE AT ARMING
- Chain: 1,127 cards · 1,127 linked · 0 breaks · ok=true
- arena_tick: 345,657,928 → 349,658,285 (climbing)
- Train pairs: 32,484 · forest: 513 rows · measured best: v4 = 0.875 (judge-v2)
- 18 sim-world LaunchAgents loaded
- Disk: ~13Gi free
