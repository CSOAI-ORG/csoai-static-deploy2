# AGENTS.md — Council of AI (csoai-static-deploy2)

Operating rules for automated agents and human contributors working in this repo.

## Identity
This repo is the **Council of AI** (CSOAI Ltd, UK 16939677) static + Worker estate. It
ships a neutral AI-governance measurement body: frozen benchmark harnesses, GSPC
measurement axes, Ed25519-signed + time-anchored measurement credentials, and an
external verifier. Everything measured is recompute-able by any third party.

## Register discipline (bind — every contribution)
Tag claims so readers can trust them:
- **REAL** = verified/live · **DEMO** = works with demo data · **THEORY** = unverified ·
  **GATED** = owner/counsel/keys.
- We issue **measurement credentials, never certifications**. Never claim compliance,
  accreditation, "board-grade," or authority we do not hold.
- **Missing cells are `UNMEASURED`, never zero.** Every public number carries its
  confidence interval + caveats.
- Do not reference internal engine codenames (SOVOS, SOV-*, sov6, and related) on any
  public surface. Public names: Council of AI, GSPC, DEFONEOS surfaces only.

## MCP / distribution
- Live GSPC MCP endpoint (streamable HTTP): `https://csoai.org/mcp`
  — tools `measure` + `verify`. Free to verify, metered to issue.
- Registry entry: `registry/server.json` → `io.github.CSOAI-ORG/gspc`.
- Worker source lives in `workers/csoai-gspc-mcp/`. Deploy with `npx wrangler deploy`
  from that directory. Keep `measurement-not-certification` wording intact.

## Build
- `python3 build_site.py` assembles static `_site` from page sources. Do not edit `_site`
  by hand — regenerate.
- Deploy static to Cloudflare Pages: `npx wrangler pages deploy _site --project-name csoai-site`.
- Stage/commit by name only. Never `git add -A` (multi-lane repo — can sweep another
  lane's files). After commit, verify with `git show --stat <commit>`.

## Guardrails
- Never exfiltrate private data. Corrupting or destructive operations require explicit
  confirmation. When architecture is ambiguous (>3 files), propose a plan before editing.
