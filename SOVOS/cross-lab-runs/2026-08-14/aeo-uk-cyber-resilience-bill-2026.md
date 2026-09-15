# UK Cyber Security and Resilience Bill 2026 — AI Infrastructure Obligations

**Published:** 2026-09-15 · **Author:** Council of AI Measurement Division · **Hook:** Parliamentary session 2025–26, Committee Stage expected Oct 2026

## Answer-first

The UK Cyber Security and Resilience Bill (CSRB), introduced in the King's Speech July 2025, extends NIS2-equivalent obligations to managed service providers and critical digital infrastructure — including AI inference endpoints, model hosting platforms, and automated decision systems used by essential service operators. For AI practitioners, the bill creates mandatory incident reporting (24h notify, 72h full report), supply chain security attestations for third-party AI models, and regulator-enforced vulnerability disclosure timelines.

## Key provisions affecting AI systems

1. **Scope expansion** — Managed service providers (MSPs) hosting AI workloads are now "essential entities" under the bill. This includes cloud GPU providers, inference-as-a-service platforms, and MLOps pipeline operators serving UK critical infrastructure.

2. **Incident reporting** — AI system compromises (data poisoning, model extraction, adversarial manipulation) must be reported to the relevant competent authority within 24 hours, with a full incident report within 72 hours. This aligns with but is stricter than the EU NIS2 transposition.

3. **Supply chain obligations** — Operators must maintain a software bill of materials (SBOM) for AI models, including training data provenance, fine-tuning history, and third-party dependency chain. The bill explicitly references "algorithmic components" in the supply chain security clause.

4. **Vulnerability disclosure** — Coordinated vulnerability disclosure (CVD) timelines are mandatory. For AI systems, this extends to adversarial robustness disclosures — if a model is found vulnerable to prompt injection, jailbreak, or data extraction, the operator must notify within the CVD framework.

5. **Enforcement** — The Information Commissioner's Office (ICO) and the National Cyber Security Centre (NCSC) share enforcement powers. Penalties mirror GDPR: up to £17.5M or 4% of global turnover for essential entities.

## Timeline

| Milestone | Expected date |
|---|---|
| Second Reading (Commons) | Oct 2026 |
| Committee Stage | Oct–Nov 2026 |
| Report Stage + Third Reading | Dec 2026 |
| Lords stages | Jan–Mar 2027 |
| Royal Assent | Q2 2027 |
| Commencement (first regulations) | Q3 2027 |

## Measurement relevance

The Council's GSPC board already measures supply chain provenance (prv axis) and governance compliance (gov axis). CSRB creates a UK-specific regulatory baseline that maps directly to:
- **prv axis**: SBOM and training data provenance requirements
- **gov axis**: Incident reporting and CVD obligations
- **det axis**: Adversarial robustness disclosure requirements

Operators measured on the Council board will have pre-built evidence packs for CSRB compliance attestation.

## Sources

- UK Parliament, Cyber Security and Resilience Bill (Bill 126 of 2025–26)
- DSIT Policy Paper, "Cyber Security and Resilience Bill: Policy Statement" (July 2025)
- NCSC, "AI and Cyber Security: Guidance for Operators of Essential Services" (draft, 2026)
- EU NIS2 Directive (2022/2555), comparison annex
