# EXTERNAL AUDIT RECONCILIATION — 2026-08-13

**Source:** `Downloads/compass_artifact_wf-7fc60525...md` (external top-down audit of the
CSOAI public estate, dated 13 Aug 2026) — received, read, and reconciled against
**direct raw-endpoint probes** performed by this lane.

## Method
The audit's own caveat was load-bearing: *"UNVERIFIED items are null search results,
not confirmed 404s — re-probe the raw endpoints."* We re-probed every contested item
against the live endpoints. Where the audit said UNVERIFIED and the endpoint says
otherwise, the endpoint wins.

## Reconciliation table (direct probes vs audit)

| Surface | Audit verdict | Our direct probe (2026-08-13) | Final |
|---|---|---|---|
| PyPI `csoai` | UNVERIFIED | `pypi.org/pypi/csoai/json` → **0.1.2 live**, author "Council of AI (CSOAI LTD, UK 16939677)"; installed from public index into fresh venv → exit 0 | **REAL — audit wrong** |
| npm `@meok-labs/csoai` | UNVERIFIED + "scope is @meok-ai not @meok-labs" | `registry.npmjs.org/@meok-labs%2Fcsoai` → **HTTP 200**, latest 0.1.0; `@meok-ai/csoai` → **404** | **REAL at @meok-labs — audit's scope claim wrong** |
| npm bare `csoai` | unclaimed squat risk | **404** | **Audit right — squat exposure open** |
| MCP registry `io.github.CSOAI-ORG/csoai` | UNVERIFIED | 404 on documented paths; versioned API also unreachable this pass | **UNVERIFIED (unchanged)** — do not cite as live |
| `meek-3-and-sov3-connection-mcp` (PyPI) | leaked SOV3/sovereign strings (HIGH) | **HTTP 200, v1.0.0, org-owned** (author MEOK AI Labs <nicholas@csoai.org>, homepage csoai.org); tarball inspected → **77 banned-string hits** incl. server.py, pyproject, PKG-INFO; payload includes "SOV3³", "33-hive BFT", "341 MCPs", "DEF ONE OS", severed-brand gate | **CONFIRMED — liability #1 REAL** |
| arXiv 2603.14011 "Sovereign-OS" | NOT estate work (USC/UMD) | Not re-probed (web tools flaky); audit's evidence is credible | **Accepted — never cite as ours** |
| EU AI Act "verbatim article count" | Factually wrong; Reg 2024/1689 = **113 Articles** / 180 recitals / 13 chapters | Not re-counted this pass; audit's statutory count is authoritative | **Accepted — canonical count is 113** |
| csoai.org apex | REAL, title "CSOAI — the measurement body" | **200**; our naming-clean deploy live (Council / Council City 3D / Council OS) | **REAL** |

## What this lane does NEXT (already in motion / done)
1. **Launch note** (committed `db2dd664`) already flags MCP registry as UNCONFIRMED — audit agrees.
2. **`verify_record` open-standard lane** — audit's #1 power move. We already ship the
   first agent-callable Ed25519 signed-record verifier; the *next* step (Rekor-v2 /
   SCITT-SCRAPI / in-toto wrappers, RFC 9942/9943 now stable) is queued — NOT yet built.
3. **Cross-lane flag (owner-gated):** `meek-3-and-sov3-connection-mcp` v1.0.0 on PyPI
   must be **yanked or scrubbed** by the `mcp-marketplace` lane + TM counsel sign-off
   (SOVOS US Reg #6876686 proximity). Evidence pack: 77 hits, file list, tarball at
   `/tmp/leak/pkg.tar.gz` on the pod. Not touched by this lane (cross-lane rule).

## Owner-gated (unchanged)
HF token revoke (`…XBeI`) · npm token rotation (`npm_UXkQ…`) · counsel: TM proximity +
certification-language gate · bare `csoai` npm/PyPI claim decision.
