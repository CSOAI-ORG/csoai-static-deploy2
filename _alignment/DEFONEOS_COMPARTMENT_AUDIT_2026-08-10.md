# DEFONEOS Compartment Audit — Top-Down Drift (2026-08-10)

**Doctrine reference:** `~/clawd/MEOK_DEFONEOS_ALIGNMENT_2026-06-27.md` v2.0 / v2.1 (27-28 Jun 2026).
**Audit date:** 2026-08-10 (JEEVES, K3 lane, DEFONEOS compartment doctrine reload per session-start mandate).
**Status:** HONEST FINDING, not a bug. Resolution is owner-gated (constitutional amendment).

---

## Executive summary

The doctrine says **3 compartments**, with 2 active + 1 legacy:
- `meok-defoneos` (BUILDS — 15 defence-AI MCPs + geospatial = 16)
- `csoai-defoneos` (CERTIFIES — 33-agent BFT council + DEFONEOS-SEAL)
- `dagon` (LEGACY NDA-only — never public, never linked)

The consumer-facing brand umbrella is `DEFONEOS` — that's what the buyer sees.

**What the disk actually has (20 packages):**

| Prefix | Count | Doctrinal status | PyPI status (sampled) |
|---|---|---|---|
| `meok-defoneos-*` | 2 | ✅ required (build compartment) | live |
| `csoai-defoneos-*` | 6 | ✅ required (certify compartment) | live |
| `defoneos-*` (bare) | 11 | ⚠️ **DOCTRINAL DRIFT** — not in v2.0/v2.1 doctrine | live |
| `agentic-threat-defense-mcp` | 1 | ⚠️ **out of scope** — generic cyber, not DEFONEOS compartment | live |
| **TOTAL** | **20** | | |

---

## Detailed inventory

### Compartment-clean packages (8)

**`meok-defoneos-*` (build compartment, on disk = 2 of 16 doctrinal):**
- `meok-defoneos-mcp` (`mcp-marketplace/meok-defoneos-mcp/`)
- `meok-defoneos-geospatial-intel-mcp` (`mcp-marketplace/meok-defoneos-geospatial-intel-mcp/`)

**`csoai-defoneos-*` (certify compartment, on disk = 6):**
- `csoai-defoneos-mcp`
- `csoai-defoneos-digitaltwin-mcp`
- `csoai-defoneos-isr-mcp`
- `csoai-defoneos-medevac-mcp`
- `csoai-defoneos-ospd-mcp`
- `csoai-defoneos-swarm-mcp`

### Doctrinal-drift packages (11 bare `defoneos-*`)

These all reference the DEFONEOS brand internally (verified via README grep) but use the bare prefix without the build/certify suffix. All are live on PyPI.

| Package | Functional area | Apparent compartment |
|---|---|---|
| `defoneos-mcp` | umbrella aggregator | uncertained — likely umbrella product surface |
| `defoneos-compliance-mcp` | compliance wrapper | likely certify (csoai-defoneos family) |
| `defoneos-cesium-mcp` | geospatial visualisation | likely build (meok-defoneos family) |
| `defoneos-cyber-mcp` | cyber | uncertained |
| `defoneos-counterdrone-mcp` | counter-UAS | likely build (meok-defoneos family) |
| `defoneos-isr-mcp` | ISR | likely build (meok-defoneos family) |
| `defoneos-jsp936-mcp` | JSP 936 ethics wrapper | likely certify (csoai-defoneos family) |
| `defoneos-medevac-mcp` | medevac | likely build (meok-defoneos family) |
| `defoneos-ospd-mcp` | OSPD | likely build (meok-defoneos family) |
| `defoneos-swarm-mcp` | swarm coordination | likely build (meok-defoneos family) |
| `defoneos-tak-mcp` | TAK integration | likely build (meok-defoneos family) |

Each needs an explicit compartment assignment, then either a PyPI-side rename (breaks installers) OR a doctrinal amendment recognising the bare-`defoneos-*` family as the **umbrella brand surface** distinct from internal compartment names.

### Out-of-compartment package (1)

- `agentic-threat-defense-mcp` — generic cyber MCP, not in the DEFONEOS doctrinal hierarchy. Either belongs in the meok-defoneos build family (rename) or in the broader meok-os empire (separate brand).

---

## Why this matters

Doctrine line 64: **"NEVER mix meok-defoneos, csoai-defoneos, and dagon assets in the same code/IP."**
Doctrine line 66: **"ALWAYS use the consumer name for the buyer: DEFONEOS (umbrella), meok-defoneos (the build), csoai-defoneos (the certify), DEFONEOS-SEAL (the signed credential)."**

If the bare `defoneos-*` packages contain build-code mixed with cert-code (or vice-versa), they violate line 64. If they contain pure build OR pure cert code, they should be renamed per line 66. Either way, **the doctrine doesn't currently account for them**.

---

## Resolution paths (all owner-gated)

### Path A — Rename the 11 packages to `meok-defoneos-*` or `csoai-defoneos-*`
- Pro: fully compliant with doctrine line 66.
- Con: breaks every installer; requires PyPI-side deprecation + new publication + a migration window of ≥6 months.
- Con: violates doctrine line 152 ("Public PRs that reference MoD / HMG / ITAR / AUKUS → MUST be cleared by the csoai-defoneos council vote (quorum 23/33) before publication").

### Path B — Doctrinal amendment: recognise `defoneos-*` as a 3rd published family
- Pro: zero breakage, zero installer migration.
- Pro: matches the actual consumer-facing language ("DEFONEOS" is the umbrella brand).
- Con: requires amendment v3.0 with PBFT-MoE Council consultation (per doctrine line "Authority").
- Con: needs to define the relationship between the bare `defoneos-*` family and the meok-defoneos / csoai-defoneos internal compartments (parent? parallel? umbrella?).

### Path C — Do nothing; document drift; defer
- Pro: zero risk.
- Con: drift accumulates; every new meok-defoneos or csoai-defoneos package makes the bare-defoneos family look more like an orphan.

---

## My recommendation (JEEVES, K3 lane)

**Path B is the right move.** The doctrine was written when there were only 16 packages; reality has 20, and the bare-`defoneos-*` family is functioning as the *published umbrella surface* while the meok-defoneos / csoai-defoneos split is functioning as the *internal compartment model*. That's actually a clean separation — buyers see "DEFONEOS", internal staff see meok/csoai.

The amendment should:
1. Acknowledge the bare `defoneos-*` family as the *consumer-facing umbrella product surface* (not a compartment).
2. Define the relationship: `defoneos-*` packages import from `meok-defoneos-*` (build) and `csoai-defoneos-*` (certify) but never the other way around.
3. Define the migration path for `agentic-threat-defense-mcp` (out-of-compartment) — either rename to `meok-defoneos-agentic-threat-defense-mcp` or move to the meok-os cyber family.

But this is a constitutional edit and I will **NOT autonomously amend v2.0**. Surfacing to Nick.

---

## Operational posture (for the next sibling tick or session)

1. Do NOT rename any bare `defoneos-*` package without consulting this audit.
2. Do NOT reference the bare `defoneos-*` family in PRs to upstream projects (e.g. NVIDIA-ACE) without owner sign-off.
3. Do NOT deploy any new `defoneos-*` package without first assigning it a compartment (meok-defoneos for build, csoai-defoneos for certify) OR explicitly adding it to the bare `defoneos-*` umbrella family with a constitutional note.
4. The DEFONEOS hard stops (lines 109-117 of doctrine) remain in force: NO kinetic-targeting patterns, NO personal-surveillance patterns, NO "AUKUS partnership" claim without signed letter, NO DEFONEOS-SEAL without 33-agent BFT vote, NO DSEI booth without UK-prime pilot letter, NO `defonos.io` domain, NO mixing of compartments.

---

**Filed:** `~/clawd/_alignment/DEFONEOS_COMPARTMENT_AUDIT_2026-08-10.md`
**Authority:** JEEVES, K3 lane, top-down doctrinal reload per session-start mandate.
**Action requested:** Nick to authorise Path B (constitutional amendment v3.0) or Path A (gradual rename) or Path C (acknowledge drift, defer).