# The Master Brand — Single Source of Truth (2026-08-15)

> This is the TOP of the alignment cascade. Every surface below (domains, orgs,
> profiles, repos, packages, datasets) MUST render this identity verbatim.
> Nothing above the leaves. Nothing below the brand.

## 1. The brand (one line)
> **Council of AI** — we measure AI systems against the rules that govern them,
> sign the result (Ed25519), and publish what we cannot yet measure.
> **Measurement, not certification.**

## 2. The fixed form (copy-paste for every surface)
| Field | Canonical value |
|---|---|
| Brand name | **Council of AI** |
| Legal entity | **CSOAI Ltd** |
| Registration | **UK 16939677** |
| One-liner | "Independent AI-governance measurement. We measure, sign, and publish — measurement, not certification." |
| Canonical site | **https://www.csoai.org** (apex), **https://councilof.ai** (marketing) |
| Live MCP | `https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp` |
| Contact | nicholas@csoai.org |
| Signature axes | 13 GSPC: governance, safety, provenance, continuity, conformance, openness, machinery, care, cross-reality, detector-interop, art5-safeguard, swarm, affect |

## 3. What the brand is NOT
- NOT "Council for the **Safety** of AI" (dead brand — retire on every surface)
- NOT a certifier / accreditation body
- NOT "CSOAI" alone as the public selling name (CSOAI Ltd is the legal co, Council of AI is the brand)
- NOT "SOVOS/SOV-*/sov6/MEOK" as public-facing brand (internal engine codenames — never public surface)

## 4. The cascade order (apply top-down strictly)
```
1  MASTER BRAND (this file)
   ↓
2  APEX DOMAIN   csoai.org  →  must be the measurement home (<title>Council of AI…)
   ↓
3  MARKETING     councilof.ai  →  "Council of AI" title/footer
   ↓
4  ORGS          GitHub CSOAI-ORG · HF org "csoai"  →  name + description = brand
   ↓
5  PROFILES      GitHub profile bio/company · HF org bio · Kaggle bio  →  brand one-liner
   ↓
6  REPOS         descriptions + topics + pinned set  →  brand-aligned, crown jewels front
   ↓
7  PACKAGES/DATA PyPI · HF datasets · Kaggle banks  →  link back to the brand
```
Rule: if a lower layer conflicts with a higher layer, the HIGHER layer wins. Fix upward, never let a leaf diverge the brand.