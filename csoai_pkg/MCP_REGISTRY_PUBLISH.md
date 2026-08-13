# Publishing csoai to the MCP registry

`server.json` is the registry manifest (validated). Publishing needs owner GitHub auth
(like npm's 2FA) — I can't do the interactive login. One-time steps:

```bash
# 1. install the publisher CLI
brew install mcp-publisher   # or: go install github.com/modelcontextprotocol/registry/cmd/mcp-publisher@latest

# 2. authenticate (proves ownership of the io.github.CSOAI-ORG namespace)
mcp-publisher login github   # opens a device-code flow in the browser

# 3. publish (from csoai_pkg/)
mcp-publisher publish         # reads ./server.json
```

After this, agents discover `io.github.CSOAI-ORG/csoai` via the MCP registry →
github.com/mcp curation → aggregators mirror. The server itself is already live on
pypi: `uvx --from 'csoai[mcp]' csoai-mcp` runs council_measure + verify_record.
