# Sovereign Town — Privacy & Data Policy

**Effective date:** 2026-06-22

## Core principle: aggregate-only, synthetic, no PII

Sovereign Town is a governed-vs-ungoverned agent-world **simulation**. All data it
publishes are synthetic, aggregate, and deliberately stripped of individual
identities, real firms, or real transactions.

## What we do not collect or store

- No real customer, citizen, or transaction data.
- No personally identifiable information (PII).
- No real company names, addresses, or beneficial-owner records.
- No biometric, health, financial-account, or location data about real people.

## What we do use

- **Public, open-licence datasets** (e.g. OGL-UK government open data) are
  downloaded, aggregated, and converted into simulation pressure signals.
- **Agent personas** are fictional archetypes generated for research purposes.
- **Simulation episodes** are hash-chained and signed, but contain only
  synthetic agent states and actions.

## Public outputs

Public pages (`proofof-site/sovereign-town/`) display only:

- Aggregate fleet status (hive counts, episode totals, governed/ungoverned crime
  counts).
- Signed run manifests (run ID, policy, scenario, aggregate metrics).
- Experiment reports with synthetic treatment/control comparisons.

No raw ledger entries, no agent identities, and no individual decisions are
published.

## Ed25519 signatures and transparency

Every signed manifest links to a public Ed25519 key (`town_pub.key`) and can be
verified offline with `verify_chain.py`. This is a transparency mechanism, not a
surveillance mechanism.

## Contact / disclosure

If you believe a public output contains real PII or other sensitive data, please
open an issue or contact the operator directly. Do not post sensitive details in
public channels.
