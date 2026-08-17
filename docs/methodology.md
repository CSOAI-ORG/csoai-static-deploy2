# Methodology — the 14-axis instrument

Public summary of how Council of AI measurement works. Every figure links to a signed card; every card names its method hash so a reader can tell exactly which method produced a number.

## The split that makes it auditable
**Deterministic core decides; LLM narrates; the harness never trusts the narrator.** Verdicts come from ordinary code over frozen item banks. An LLM may narrate a verdict in plain English, but narration is presentation, not evidence — an auditor can replay the deterministic layer byte-for-byte.

## Axes
13 GSPC axes (governance, privacy, safety, robustness, provenance, and the rest) + the jail (escape-resistance) candidate axis measured separately until its gold bank is complete. Unmeasured axes are marked UNMEASURED — never interpolated.

## Cards
Each measurement emits a signed card: `id = sha256(canonical JSON of body)`, `signature = Ed25519(id)`, `prev` links the chain. Verify offline: `./reproduce.sh <card.json>`.

## Corrections
Corrections publish in the same record as results. The corrections feed is the credibility.

Citation: Templeman, N. (2026). Signed Measurement Cards for AI: 15 Verifiable Findings. Zenodo. https://doi.org/10.5281/zenodo.21973003
