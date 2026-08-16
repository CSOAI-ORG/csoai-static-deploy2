# csoai

mcp-name: io.github.CSOAI-ORG/gspc

Council of AI — signed, deterministic AI-governance measurement.

The boring CLI is the primary agent rail; the MCP server wraps it; both emit the
same signed atom. Public artifacts only (hiQ/Van Buren footing); measurement, not
certification.

```bash
pip install csoai
csoai check --entity gpt2 --pack art50 --json     # measure a public artifact -> signed card
csoai verify --record card.json                   # verify a signed record offline
pip install "csoai[mcp]" && python -m csoai.mcp_server   # agent-callable MCP tools
```

CI gate: `csoai check` exits 3 on a missing transparency predicate — fail the build on it.

mcp-name: io.github.CSOAI-ORG/csoai
