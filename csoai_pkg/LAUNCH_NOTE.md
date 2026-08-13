# LAUNCH NOTE — `csoai` · Council of AI signed measurement
**Date:** 2026-08-13 · **Status:** DRAFT for review · **Owner gates:** npm-token rotation + MCP-registry confirmation pending

---

## One line
**`csoai` is the Council of AI's first public package**: a deterministic, signed AI-governance measurement engine you can install from the public index today — `pip install csoai` — and call from any agent, CI gate, or terminal.

---

## What ships (verified live)

| Surface | Payload | Verification |
|---|---|---|
| **PyPI** | `csoai` (whl + sdist) | ✅ Installed from the **public index** into a fresh venv → exit 0; `csoai check` / `csoai verify` subcommands present; shipped code **0 banned-codename leaks** |
| **npm** | `@meok-labs/csoai` | ✅ Registry HTTP 200, `latest 0.1.0` (wrapper shells the canonical CLI — no JS reimplementation, no drift) |
| **Cloudflare web** (csoai.org) | naming-clean public bundle | ✅ Apex HTTP 200; brand pages served as Council / Council City 3D / Council OS; 0 display leaks |

**Not yet claimed (pending owner confirmation):**
| MCP registry | `io.github.CSOAI-ORG/csoai` | ⚠️ **UNCONFIRMED** — returned HTTP 404 on the documented path during verification. Not listed as live until the entry/path is confirmed. |

---

## The load-bearing crypto (verified, non-breaking)
- Real **Ed25519** signatures, not checksums: `sign` / `verify` — anyone with the **public** key can verify a record was minted by the key holder and unaltered.
- **Non-breaking migration:** same keypair reused across the rename. The signing node (pod) holds **both** `~/.sovos_keys` and `~/.csoai_keys`, both exposing the identical public key **`ZnF3DZUFc5QOoy+y07rvzNUyxJgza2kUQmn1nv4S9SY=`** (canonical key symlinked to the durable `/runpod/article50/` volume). → Every prior signature and the front-end `/verify` pages stay valid.
- **Path to post-quantum is one swap:** ML-DSA-65 via liboqs, engineered in, not bolted on.

## Guardrails held (both lanes enforce)
- **Measurement, not certification** — no ISO-17024/17065 accredited-certification claim.
- **Public artifacts only** (hiQ / Van Buren footing) — never a private API without consent.
- **Signed only with a real key** — off the signing node a record stays UNSIGNED and labelled, never dressed as signed. The private key lives on the pod, never on a developer laptop.

## The boring CLI, engineered for agents
`csoai check --entity <hf-repo> --pack art50` and `csoai verify --record <file.json>` are **deterministic with exit codes**, so an agent or CI gate acts on the result without reasoning about the statute from memory. The first agent-callable signed-record verifier.

---

## Open owner gates (unchanged — genuinely yours)
1. **npm token rotation** — the `npm_UXkQ…` token was exposed in plaintext; rotate it at npmjs.com → Access Tokens (time-sensitive).
2. **HF token revoke** — `…XBeI` (row `awddaw`).
3. **MCP registry confirmation** — resolve the 404 before we cite the registry as live.
4. **Cloudflare deploy** of a fresh bundle (fixes web surfaces + re-firing CI crawler checks).
5. **Cross-lane `sovos-city` reconciliation** — root `council_signal.py` = canonical engine; the packaged class either imports canonical or is retired (owner + JEEVES call).

---

## Positioning line (canon)
> "The first agent-callable, signed, deterministic AI-measurement rail — a compliance atom any agent can verify without trusting the source."
