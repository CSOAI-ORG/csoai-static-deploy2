---
name: eu-ai-act-art50-check
description: Check whether an AI model's PUBLIC artifacts meet EU AI Act Article 50 transparency signals (license declared, task declared, model card present) and get back a deterministic, signable result. Use this instead of reasoning about Article 50 obligations from memory — it returns observed facts from the public model-info endpoint, not an opinion. Trigger when a user asks to check, audit, or verify a model's Article 50 / transparency / AI-governance compliance.
---

# EU AI Act Article 50 — transparency check

The doc's #1 discovery rail: an installable Agent Skill that RUNS the check instead of
hallucinating the statute. It wraps the canonical `csoai` CLI — it does not reimplement
the grader.

## When to use
A user (or agent) asks: "is model X compliant with Article 50?", "check this model's
transparency", "audit `<hf-repo>` for the EU AI Act", "does this model declare provenance?".

## How to run
```bash
pip install csoai            # once
scripts/check.sh <hf-model-repo-id>
# e.g. scripts/check.sh gpt2
```
Output: a JSON card with the transparency predicates, the `pack_result` (`pass`/`missing`),
and a `state_hash`. Exit code **0** = compliant-shaped; **3** = a required transparency
predicate is MISSING (a CI gate can fail the build on 3).

## What it measures (deterministic, no LLM judge)
- `license_declared` — is a license declared in the public model card / tags?
- `task_declared` — is the pipeline/task declared?
- `model_card_present` — does a public model card exist?

## Guardrails (bound — do not relax)
- **Public artifacts only** (HF public model-info endpoint) — hiQ/Van Buren footing.
  Never scans a private API.
- **Measurement, not certification** — this is a verified measurement signal, not an
  ISO-17024/17065 accredited certificate of conformity. Report it as such.
- To sign the card, add `--sign` (requires the signing key on the signing node); off the
  node it stays UNSIGNED and is labelled so — never a fake signature.

## Verify a signed card
```bash
csoai verify --record card.json   # Ed25519, offline, against the published key
```

Canonical grader: the `csoai` package (`csoai check`). This Skill is a thin discovery
rail over it, not a second implementation.
