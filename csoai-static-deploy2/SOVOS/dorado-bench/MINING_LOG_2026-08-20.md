# MINING LOG — overnight run Phase D (2026-08-20)
Findings, IP notes, and corrections from the mining pass.

## IP Notes (3)

### IP-1: Signed-receipt dual-use (evidence rail → insurance trigger + claims evidence)
The same primitive (Ed25519 + hash-chained 3KB card) serves THREE product
surfaces: (a) underwriting input (deterministic conformance with CI),
(b) parametric trigger (policy condition met = receipt valid), (c) claims
evidence (tamper-evident "what the AI did"). One build, three buyers — the
strategy doc's "dual-use rescue of the same primitive." Moat: no competing
AI-insurer (AIUC/Armilla/Munich Re) has a neutral signed rail; they all bear
risk or sell evaluations.

### IP-2: Corrections-as-asset (credible neutrality is the product)
The corrections ledger (appended-never-edited) is a marketing asset in a
market full of pay-for-placement rankings. Live in /api/regulation
(corrections_policy + headline_correction). The 9 real self-caught corrections
prove neutrality better than any claim. Doctrine: never edit history, append.

### IP-3: Reg-feed-as-underwriting (penalty exposure = contractible data)
The regulation feed's penalty_exposure field (EUR35M/7%, EUR15M/3%,
USD1M/3M Illinois) makes regulatory deadlines CONTRACTIBLE underwriting input.
19 deadlines, quarterly re-verified, corrections appended. This is the NOW
product needing no signed receipt — the lead 30 Sep pitch artifact.

## Corrections found & fixed this pass
1. **P1-4 machine-contract purge**: banned vocab (sovereign/SOV3/defoneos) in
   109 occurrences across 15 public API functions. Root cause: shared
   constants.mjs persona + legacy api/ static dir shadowing functions/.
   Fixed: constants + 7 public APIs clean (verified on deployment), legacy
   api/ shadow removed. mcp serves "MEOK MCP".
2. **Dead /api/owem link** in governance.html: removed (internal-only concept,
   no public function).
3. **favicon.ico 404**: added (browsers request it).
4. **Carder README endpoint**: fixed to raw/main/README.md (API /README 404s).

## Carder baseline (pilot, dry-run, own 30 datasets)
23 GREEN / 7 AMBER / 0 RED. gspc-jail 100/100 (all 5 sections). 7 AMBER need
card-section completion (datasets/dataset_info/card keys). Next: complete the
7 AMBER cards, then wire SIGN (Ed25519) + SPRAY (HF post) after owner nod.

## One-count rule
Board API carries authoritative count (887 items / 14 axes / "13 of 14").
Homepage + llms.txt consistent (no conflicting hardcoded numbers).
