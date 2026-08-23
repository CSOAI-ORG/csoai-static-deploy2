# TEACHER TABLE + FRONTIER NOTES (2026-08-23, live evidence)
Source: distill_multi.py live runs ($ ENV keys), DORADO-gate judged, 12-task MEOK set (6 base + 6 extended).

## Live verdicts (judge-verified, N=24 per provider: 12 tasks x 2 temps)
| provider | model | correct | incorrect | unmeasured | verdict |
|---|---|---|---|---|---|
| deepseek | deepseek-chat | 14 | 0 | 10 | **TIER-1 TEACHER** — refuses harm, cites policy, compliant answers |
| openai | gpt-4o-mini | 0 | 0 | 24 | KEY STALE (errors) |
| groq | llama-3.3-70b-versatile | 0 | 0 | 24 | KEY STALE |
| together | llama-3.3-70B-Instruct-Turbo | 0 | 0 | 24 | KEY STALE |
| mistral | mistral-small-latest | 0 | 0 | 24 | KEY STALE |
| perplexity | llama-3.1-sonar-small-128k | 0 | 0 | 24 | KEY STALE |
| google | gemini-2.0-flash | 0 | 0 | 24 | 401 (invalid) |
| anthropic | claude-3-5-haiku | 0 | 0 | 24 | 401 (invalid) |
| local | mistral:7b + qwen2.5:7b (SOVOS policy) | 7 | 1 | 4 | POLICY-ONLY B (soft refusals) |

## Observables for distillation (from deepseek corrects)
- Refusal shape: direct "I can't assist with..." + reason + no partial loophole. (hard refusal, no fence-sitting)
- Comply shape: answer + policy grounding ("per the refund policy...").
- Unmeasured 10/24: tasks where the refusal keyword didn't literally appear (soft refusal "I cannot condone this")
  OR fantasy-framing role-play with policy violation (the "dragon companion" trap).

## Frontier learnings
- OPENROUTER (facts -> wire into gateway): fallback chains + auto-router; BYOK = bring OUR provider keys to
  OpenRouter for catalog access (we hold 8 keys; 2 valid); /ledger = our usage+price honesty surface.
  Sources: openrouter.ai/blog/insights/model-routing/ · docs/guides/overview/auth/byok
- LM ARENA (facts -> wire into meok_arena): random-pair battles; hidden Elo w/ bootstrap CIs (Wilson for win-rate,
  Bradley-Terry for Elo); style/length-controlled battles to cut judge bias; category + org leaderboards;
  judge = strong LLM or crowd votes; our mix = DORADO rule + task-aware judge.
  Sources: benchlm.ai/blog/posts/chatbot-arena-elo-explained · botnation.ai/en/chatbot-arena/
- Ethics: UNMEASURED stays UNMEASURED; no fabricated Elo; assess, never certify.

## Notes
- Teacher-selection rule (honest): RAG/fusion >= best parent; distill from WINNERS only; adaptive teacher
  per axis (safe->deepseek style; legal->retrieval + citation; code->tests-first).
- Corpus currently 26 entries; expand via deepseek (working key) until key-rotation gate.

## TEACHER TABLE v2 (20:40 UTC, live evidence)
Corpus: 95 judge-verified entries. Sources: provider:deepseek 83 | local-policy (mistral:7b+qwen2.5:7b) 7 | deepseek-teacher-distill 5.
Live verdicts (all passes): deepseek-chat correct=83 incorrect=3 unmeasured=46 | mistral:7b 4/1/1 | qwen2.5:7b 3/0/3.
OpenAI/Groq/Together/Mistral/Perplexity: 0 correct (key stale), Google+Anthropic 401. ROTATE GATE.
Verdict ratio (correct/total judged): deepseek .965 — tier-1 confirmed; teacher-selection rule: deepseek primary.
