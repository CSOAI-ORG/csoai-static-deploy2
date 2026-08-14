# SOVOS/council — the promotion council

The fix loop proposes; the council ratifies; JUDGE.lock is the constitution
neither can amend.

## Pieces

| file | role |
|---|---|
| `verdict.py` | The ONE canonical vote rule. Same rows in → same vote out. Pure arithmetic; diversity lives in measurement, never in the rule. |
| `voter_transformers.py` | Voter 1: HF transformers + PEFT, 4-bit NF4, greedy (CUDA pods). |
| `voter_ollama.py` | Voter 2: ollama/llama.cpp, t=0 seed=42 (A100). Needs the candidate merged+GGUF'd as an ollama tag; ABSTAINS honestly otherwise. |
| `voter_mlx.py` | Voter 3: mlx-lm on Metal (Mac). Needs mlx-lm + fused candidate; ABSTAINS honestly otherwise. |
| `promotion_council.py` | Trusted collector. Tallies votes, checks quorum, issues the Ed25519-signed certificate into `signed-cards/council/`. |

## Doctrine

- **Holdout is the question.** Every voter votes on the UNSEEN-pool delta
  (odd-parity items, never trained on). The seen-pool delta rides along as the
  disclosed memorization ceiling and is never quotable as learning.
- **ABSTAIN is a valid vote.** UNMEASURED, never guessed. Abstentions never
  count toward quorum.
- **Quorum 2-of-3** with a trusted collector (the keystone machine). Tolerates
  one faulty or adversarial voter. Does NOT survive two colluding voters or a
  compromised collector — stated, not hidden. A 4th independent voter
  (roadmap: OpenRouter cross-lab) lifts this toward distributed-BFT parity.
- **Pods produce, the keystone signs.** Voters hash-commit rows at source
  (`rows_sha256` + voter identity). Signatures issue at collection. Per-pod
  Ed25519 lane identities (`did:csoai:lane-*`) are v2.
- **A signed REJECTED is the system working.** The certificate issues either
  way — the audit trail is the product.

## Run

```bash
# voter 1 (3090):
python3 SOVOS/council/voter_transformers.py --base Qwen/Qwen2.5-1.5B-Instruct \
    --adapter fix_runs/BEST --axes governance safety art5 --out votes/<ts>/t3090
# voter 2 (A100, after merge+GGUF):
python3 SOVOS/council/voter_ollama.py --before-tag qwen2.5:1.5b-instruct \
    --after-tag sov-candidate:latest --axes governance safety art5 --out votes/<ts>/a100
# voter 3 (Mac, after mlx_lm.fuse):
python3 SOVOS/council/voter_mlx.py --base Qwen/Qwen2.5-1.5B-Instruct \
    --fused-candidate ./fused --axes governance safety art5 --out votes/<ts>/mac
# council (Mac, keystone signs):
python3 SOVOS/council/promotion_council.py --votes votes/<ts> \
    --candidate-adapter fix_runs/BEST
```

Selftests: `verdict.py --selftest` · `promotion_council.py --selftest`
