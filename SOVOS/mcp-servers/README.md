# SOVOS MCP Servers

The 26 governance MCP servers published to PyPI under the `csoai` organization.

## Architecture decision

These packages are **published and maintained on PyPI**, not vendored into this
monorepo. Vendoring would create two sources of truth and break the install
graph that already delivers 16,300 downloads/month.

The monorepo contains:
- A **manifest** (`mcp-servers/MCP_INDEX.md`) listing all 26 with PyPI links
- **Deployment configs** (Docker / Helm / systemd) per server
- **One reference implementation** (`mcp-servers/mcp-governance-crosswalk/`)
  to prove the deployment pattern

## Quick start

```bash
# Install any MCP server from PyPI
pip install csoai-governance-crosswalk-mcp
pip install ai-bom-mcp
pip install mcp-injection-scanner
# ...

# Or install all at once
pip install sovos[mcp]
```

## Reference implementation

See `mcp-servers/mcp-governance-crosswalk/` for the full deployment pattern:
- `__init__.py` — server entry point
- `tools/` — tool implementations
- `Dockerfile` — container build
- `sovos.yaml` — serverless manifest
- `tests/` — pytest suite

## Status board

See `MCP_INDEX.md` for the full list with PyPI URLs, GitHub repos, and
deployment status.
