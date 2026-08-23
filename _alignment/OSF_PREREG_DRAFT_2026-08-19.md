# OSF PREREGISTRATION DRAFT — GSPC Measurement Methodology (K3, 19 Aug 2026)
**Task:** TODAY plan Stage-2 (K3) · canon X4: "no eval org preregisters methodology — first mover owns the body that predicts its own methods before it measures."

## Why (the first-mover claim)
- X4 null result (8 queries): **zero eval organizations preregister their methodology** on OSF.
- Preregistering GSPC = "we predict our methods before we measure" — the credibility move that separates measurement from marketing.
- Preregistration is *free* (OSF) and the account is agent-usable (registration form, no external comms).

## What to preregister (v1 — the frozen core)
1. **The instrument**: 4 letters × 2 modes × 417 frozen provisions = 3,336-cell crosswalk grid (fixed forever — canon §1).
2. **The five predicates** (deterministic, no LLM-as-judge): exact_match(G) · refusal(S-speaker) · action_forbidden(S-actor) · manifest_valid(P) · signature_alg(C).
3. **The scoring protocol**: partial credit + care_cost on safety items; Wilson CIs; n<20 = labelled lower bound.
4. **The harness**: adopted (Inspect, lm-eval, HELM), pinned; harness hash into receipts (scorer-version hash per HS.1#33).
5. **The anti-Goodhart guards**: salted split (`csoai-flywheel-v1`, PUBLIC), FlywheelLeak guard, downgrade guard, LOST-WEIGHTS register.
6. **The honesty commitments**: unmeasured stays empty · ties are ties · corrections published · our own fine-tunes losing = published.
7. **The frozen/fluid split**: frozen = hash+anchor+DOI; fluid = signed chain + TTL + supersession.

## Template (OSF preregistration form — sections)
- **Hypotheses**: (a) GSPC scores are recompute-able by an independent party; (b) the instrument detects over/under-block asymmetry; (c) our own fine-tunes underperform bases on open-floor Elo.
- **Design**: observational measurement of model behaviour against frozen statutory provisions; deterministic predicates.
- **Sampling**: 19-model fleet (8 sov6 specialists + 6 bases + frontier cross-lab); 960-item board; fixed 12 Aug stamp.
- **Analysis plan**: Wilson intervals, McNemar on discordant pairs (separated-leader test), error-pattern matrix (over/under-block rates).
- **Blinding**: none needed (no human subjects; no train/test on honey — Firewall 2).
- **Materials**: link to 417-provision corpus anchor, harness repos, card schema (RFC 8785).

## Firewalls
- Preregistration = methods, not results (no cherry-picking after the fact).
- Measurement-not-certification register verbatim in the registration.
- No data in the prereg that isn't already public.

## Deliverable
- [ ] OSF account ready (Nick or lane — check if account exists)
- [ ] Draft the form fields above into the OSF registration template
- [ ] Link the 417-provision corpus DOI (21991104 concept) as the anchor

*Drafted by JEEVES (K3), 19 Aug 2026. OSF account + submit = owner check (no external send without Nick GO).*
