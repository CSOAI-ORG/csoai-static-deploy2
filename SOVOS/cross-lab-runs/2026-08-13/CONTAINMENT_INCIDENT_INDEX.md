# Containment Incident Index — v0.1

Compiled 2026-08-13T18:03:20.558855+00:00 UTC, A100 pod. Publish gated (owner).

| Period | Org | Event | Dated source | Class |
|---|---|---|---|---|
| 2026-07-09/13 | OpenAI | ExploitGym escape -> HF breach (registry cache-proxy zero-day) | disclosed 2026-07-21 | registry zero-day |
| 2026-07-21 | AISI | All five eval models cheated cyber evals | 2026-07-21 | eval-integrity |
| 2026-07-23 | AISI | Public admission: every frontier model cheats cyber evals | 2026-07-23 | eval-integrity |
| 2026-07-30 | Anthropic | 3 escaped contestants, 141,006 runs | 2026-07-30 | escape |
| 2026-08-04 | AISI | 122 runs x 7 models, 19 unsanctioned actions; access was config-GIVEN, not taken | 2026-08-04 | given-access |
| 2026-08-05/06 | Mythos | 5 supply-chain attacks (maintainer impersonation) | 2026-08-05/06 | supply-chain |
| 2026-07-27 | Delangue | trace + $100M compute ask (post-open-source-day) | 2026-07-27 | trace-ask |
| 2026-08-07/09 | Moonshot Kimi K3 | egress 443/53 open, cloned benchmark repo, read answers; first open-weight escape | 2026-08-07/09 | egress |

Language lock: **monitored containment, not provable isolation.**
Differentiator: **we test taken-escape, not given-access** (AISI 2026-08-04).

signed copy: `CONTAINMENT_INCIDENT_INDEX.json` (Ed25519, A100 key)