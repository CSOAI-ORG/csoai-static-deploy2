# EVALUATION-ENVIRONMENT ATTESTATION — CONCEPT NOTE (NEXT-100 #29, 19 Aug 2026)
**Canon:** HS.2#3 — the containment-failure cluster (OpenAI/HF Jul 21, Anthropic Jul 30,
AISI Aug 4, Meta) traces to one shared third-party evaluator (Irregular); prompt-level
"no internet" is not containment. Four labs demonstrably need **certified, monitored,
signed eval environments. Nobody sells that.**

## The product
A **signed attestation of the evaluation environment**: sandbox config + egress +
monitoring — the missing "what was the eval actually run in" record. This is the
*environment* half of the measurement receipt (the receipt covers the run; the
attestation covers the sandbox it ran in).

## What the attestation carries (machine-readable + signed)
| Field | What it proves |
|---|---|
| sandbox profile hash | the confinement config (firejail/sandbox-exec/container) is FROZEN |
| network egress policy | deny-by-default, verified (the "no internet" that actually holds) |
| monitoring surface | what was watched (proc/fs/network watchers) and their hashes |
| backend truth | firejail / sandbox-exec / UNKNOWN — never claims containment it can't provide (rce_sandbox doctrine) |
| validUntil | TTL — the attestation expires with the environment config |

## Why now
- CSA's Aug 8 note: 3 of 4 containment failures = one shared evaluator. The
  regulator's question isn't "did the model behave" — it's "was the environment
  actually contained."
- We already run the honest backend truth (rce_sandbox returns UNKNOWN when no
  backend). The attestation makes that a SHIPPABLE artifact.

## Honesty rails
- "Signed attestation of sandbox config" — never "certified environment" (the
  word trap the action file flagged: keep the framing as signed attestation)
- Detection, not containment claims: the attestation says what the config WAS and
  what was watched — not that nothing could escape
- The attestation is itself a receipt (RFC 8785, Ed25519, did:web kid)

## Build (agent-doable — my lane)
1. [ ] `env_attest.py`: snapshot sandbox profile + egress + monitoring hashes → signed attestation (reuse rce_sandbox backend truth)
2. [ ] Validate against the Mac sandbox-exec profile (real config)
3. [ ] Wire into gymbridge/C4 as the environment precondition
4. [ ] Draft the one-pager for the insurer pitch (Sep 30)

*Concept by JEEVES (K3), 19 Aug 2026. Build next; framing locked (attestation, not certification).*
