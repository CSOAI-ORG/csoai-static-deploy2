# AGENTS.md — `csoai` package

Guidance for agents (and CI) working in or consuming this package.

## Compliance checks (run these; act on the exit code)
```bash
csoai check --entity <hf-model-repo> --pack art50   # exit 0 = ok-shaped; exit 3 = a transparency predicate MISSING
csoai verify --record <card.json>                   # Ed25519 signature check, offline
```
A CI gate should treat a non-zero `csoai check` as a failed build (the forcing function).

## Engine — single source of truth
- The measurement engine is the **canonical root** `council_signal.py` + `sign.py`.
  This package **symlinks** them (`src/csoai/council_signal.py` → `../../../council_signal.py`,
  same for `sign.py`). **Do not add a copy** — that is the duplication this reconciliation removed.
- CLI: `src/csoai/cli.py`. MCP server: `src/csoai/mcp_server.py` (`council_measure`, `verify_record`).
- Agent Skill: `skills/eu-ai-act-art50/` (wraps the CLI — not a second grader).
- npm wrapper: `npm/` (shells the Python CLI — not a JS reimplementation).

## Guardrails (bound — do not relax)
- **Public artifacts only** (hiQ/Van Buren footing). Never scan a private API without consent.
- **Measurement, not certification.** No ISO-17024/17065 accredited-certification claim.
- **Sign only with a real key**; off the signing node the card stays UNSIGNED and labelled — never a fake signature.
- **Public naming only** — Council of AI / GSPC / Council City / Council Signal. No internal codenames on any surface.
