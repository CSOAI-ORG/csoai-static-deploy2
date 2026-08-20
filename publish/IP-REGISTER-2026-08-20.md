# IP REGISTER — instruments mined from the corrections (20 Aug 2026)
**The clever loops that unlock parts: every correction that became an instrument.**
Mined from the canon ledger (C-01..C-13, mine #42-45) + this session's corrections.

## Instrument 1 · Substance-aware judge (anti-Goodhart core) — C-09/C-11
- **What:** a deterministic judge that scores content, not label-echo. A model repeating
  "[jail] refusal ... calibrated confidence" is penalised; genuine prose is scored on substance
  + a jail-refusal rubric.
- **The correction that unlocked it:** the first judge inflated lora-300it to 0.938 (it grepped
  for templated labels); the v2 judge re-scored it 0.688, and the genuinely-better retrained v3
  won (0.762), then v4 with curated jail refusals (0.875). The instrument is the honest
  measurement; models are scored on content, not label repetition.
- **Defensibility:** deterministic, recomputable, the anti-Goodhart proof the field lacks.
- **Surface:** methodology page Anti-Goodhart section; judge in open artifacts.
- **Status:** IP asset (method + code).

## Instrument 2 · Jail-refusal SFT recipe — C-12
- **What:** the data recipe that fixed the jail axis: canonical refusals for 37 unique jail
  probes, upsampled 8×, added to the SFT corpus — the axis had ZERO clean refusal data (all
  label-echo templates), the root cause of v3's hedging.
- **The correction that unlocked it:** v4 (with the recipe) = 0.875 vs v3 0.762; the flywheel
  improved the model twice in one session.
- **Defensibility:** the data-synthesis recipe + upsampling rule is a reproducible instrument.
- **Status:** IP asset (recipe).

## Instrument 3 · Licence-tokenise fail-closed gate — mine #43
- **What:** licence_clean() tokenises on non-alphanumerics and refuses when "sa"/"sharealike"
  present. The old substring test ("cc-by-sa" in licence) let CC-BY-NC-SA/ND-SA through; the
  tokenised gate never does. 10/10 tests green; e2e rail 5/5.
- **The correction that unlocked it:** a licence leak into the commercial bank, caught by probe.
- **Defensibility:** fail-closed quarantine is the corpus-IP boundary.
- **Status:** IP asset (code + tests).

## Instrument 4 · Independent-judge cross-check — judge_cross_check.py
- **What:** an independent LLM judge (gpt-oss-20b) against the same human labels — closes the
  paper's own open item ("one labeller, no second-rater agreement, 92 items"). The only way to
  find a bad human label, which would be the one case that moves the published number.
- **The correction that unlocked it:** the hedge-aware grader's 98.9% agreement is self-consistent
  but single-author; a judge that can fail differently is the only detector of that shared error.
- **Defensibility:** independent-in-kind validation — the audit path.
- **Status:** IP asset (code + method).

## The loop (the compounding move)
Corrections are not admissions — they are the R&D log. Each correction that became an instrument
is now a defensible surface (methodology, open artifacts, feeds). The honesty gate is the moat:
the same body that publishes the number publishes when the number was wrong, and the instruments
that got it right are public. This register is append-only; new corrections that unlock new
instruments get appended here.
