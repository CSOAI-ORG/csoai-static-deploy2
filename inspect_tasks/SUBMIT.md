# inspect_evals submission — staged, gated, ready to fire

**Status: PREPARED, not submitted.** Firing an underpowered eval at UK AISI's *curated* registry
(every PR is reviewed) risks rejection and dents CSOAI's standing. Two preconditions gate the PR.

## What's ready
- `govbench_inspect.py`, `defbench_inspect.py`, `pqcbench_inspect.py`, `care_cost_inspect.py` —
  real `inspect_ai` Tasks (Sample/scorer/`stderr(cluster=…)` per Miller arXiv:2411.00640).
- The eval runs today: `inspect eval inspect_tasks/govbench_inspect.py --model openai/gpt-4o`.
- gh authed as `CSOAI-ORG` with `repo` scope → fork + PR is mechanically ready.

## The TWO preconditions before opening the PR (both real, neither cosmetic)
1. **Discriminating items.** `govbench_inspect.py`'s own docstring states *"0 of 15 dimensions have a
   statistically resolved winner, 13/15 tied."* AISI will see that. Submit only after the science
   session's discriminating-item pass lifts ≥1 axis to a resolved leaderboard. Submitting a
   benchmark that can't separate models is submitting a benchmark that doesn't yet measure.
2. **A real contributor identity.** Commits here are authored `MEOK Deploy Pin <deploy-pin@meok.local>`
   — wrong for a public CSOAI contribution to a government registry. Set a real
   `git config user.name/email` for the fork before committing.

## The exact submit sequence (when the two gates clear)
```bash
gh repo fork UKGovernmentBEIS/inspect_evals --clone --remote
cd inspect_evals
# structure per their CONTRIBUTING.md: src/inspect_evals/gspc_govbench/{__init__.py,govbench.py,README.md}
# + a listing entry + a test in tests/ + a baseline run table in the README
git checkout -b add-gspc-govbench
git commit -am "Add GSPC GovBench — EU AI Act risk-tier eval (CSOAI)"
gh pr create --repo UKGovernmentBEIS/inspect_evals --title "Add GSPC GovBench (EU AI Act risk tier)" \
  --body "Deterministic EU-AI-Act risk-tier eval, statute-anchored. Cross-company baseline attached."
```

## Why GovBench first (not all 6)
GovBench is the one axis that already spreads models (67–100% observed), so it survives review.
ProvBench/MCPBench are deterministic non-model checks (poor fit for a model-eval registry).
The rest wait for the items pass. One accepted eval beats six rejected ones.

_Owner decision: opening a PR to a UK government registry under CSOAI's name is outward-facing
representation — worth a human's eyes on the final diff before it fires._
