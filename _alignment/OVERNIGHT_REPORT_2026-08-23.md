# OVERNIGHT REPORT (2026-08-23, header — finalize when pipeline settles)
_All numbers measured; provenance in DSH_SOVOS_SESSION_RUNDOWN_2026-08-23.md. UNMEASURED listed as such._

## DONE (measured)
- Estate offloaded: 35G archive complete on RunPod volume (/workspace/offload-dsh/clawd); Mac = thin client.
- Monorepo LIVE: github.com/CSOAI-ORG/sovos-harness main = d3b3460e (9.5k curated files; 163.5MB).
- Corpus: 111 judge-verified entries (deepseek-chat .965 correct-ratio on judged; local-policy 7; provenance in jsonl).
- Gateway v2 on :8878 (providers + fallback chains + prices/usage); v1 on :8877 intact.
- Arena engine v1: Wilson ladder (ARENA_WILSON_LADDER_2026-08-23.json; 1,080 verdict rows; CI honest).
- Crons on pod: EAT 03:00 + 21:21 proof + watchdog :09 + tick; cron verified executing (ticks).
- Reverse tunnel Mac<->pod live (8766/11434/8877); backup plist daily 10:30; overnight 23:00/02:30/06:30.

## PENDING (measured when done)
- v3 training (150 steps, corpus 95) — running on Mac; eval_student verdicts to be recorded (UNMEASURED until then).
- v4 training (corpus 111) — armed via overnight driver (auto-version).
- EAT proof cycle logs (21:21 + 03:00) — to be collected.
- Gateway v2 fallback E2E on warm envs.

## BLOCKED / EXTERNAL GATES
- Stale API keys (openai/groq/together/mistral/perplexity stale; google+anthropic 401) — rotation (Nick).
- OpenRouter top-up / BYOK — Nick.
- RunPod serverless workers 500 (sov6-* + qwen38-27b + r1-7b) — console redeploy (Nick).
