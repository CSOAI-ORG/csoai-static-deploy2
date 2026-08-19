# Install — Council of AI GSPC (measurement over MCP)

The Council of AI GSPC measurement server. Deterministic governance-measurement over MCP:
13 measured of 14 GSPC axes, Ed25519-signed measurement cards, offline verification,
UNMEASURED reported never hidden. **Measurement, not certification.**

## Remote server (recommended — no local install)

Add to your MCP client:

```json
{
  "mcpServers": {
    "csoai-gspc": {
      "type": "http",
      "url": "https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp"
    }
  }
}
```

## Local (from source)

```bash
git clone https://github.com/CSOAI-ORG/csoai-static-deploy2
cd csoai-static-deploy2
# the MCP server ships in the repo (functions/api + gspc-mcp spec)
```

## What you get

- **measure** — run a subject through GSPC axes → signed measurement card
- **verify** — check a card offline (sha256 canonical body + Ed25519, public key only)
- **board** — the live axis register (13 of 14 quotable; UNMEASURED stays unmeasured)
- **lookup** — deterministic covered-query answers from the signed corpus (no model in path)

## Verify everything

`id = sha256(json.dumps(body, sort_keys=True, separators=(",",":"), ensure_ascii=False))`
· `signature = Ed25519(id)` · `prev` links the chain. Verify offline with the published key.

Official MCP Registry: `io.github.CSOAI-ORG/gspc` · Methodology DOI 10.5281/zenodo.21991104
