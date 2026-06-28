# Why sovereign MCPs are the developer experience you've been waiting for

**For:** Backend and AI engineers building agent systems.
**TL;DR:** The MCP protocol is HTTP + JSON. Every sovereign MCP returns Ed25519-signed JSON with a proofof.ai verify URL. No proprietary SDKs. No vendor lock-in. Just `pip install` and `from meok_sovereign_passport import create_passport`.

**The DX wins:**

1. **pip install** — every sovereign MCP is a standard Python package
2. **from meok_sovereign_X import Y** — clean Pythonic API
3. **Ed25519 by default** — every tool output is signed with a verify URL
4. **MCP-compatible** — run as a stdio MCP server: `python -m meok_sovereign_passport`
5. **Tested** — 10-20 pytest cases per MCP, all passing in <0.2 sec
6. **MIT-licensed** — copy, modify, ship. No legal review.

**The 4-line sovereign agent:**

```python
from meok_sovereign_passport import create_passport, evaluate_intent
from meok_sovereign_receipt import create_receipt
from meok_sovereign_governance import policy_evaluate

passport = create_passport("trader-bot", "trader", ["payments"], care_floor_validated=True, bft_council_id="c1")
decision = evaluate_intent(passport, "send_payment", "/api", agent_level="senior", care_floor_validated=True)
receipt = create_receipt({"event": "decision", "verdict": decision["verdict"]})
assert decision["verdict"] == "allow"
print(decision["verify_url"])  # https://proofof.ai/passport/...
```

**Run an MCP server (3 lines):**

```python
from mcp.server.fastmcp import FastMCP
from meok_sovereign_passport import register_mcp_tools
mcp = FastMCP("meok-passport")
register_mcp_tools(mcp)
mcp.run()
```

**The dev pitch (60 seconds):**

"12 MIT-licensed sovereign MCPs. pip install. Pythonic API. Ed25519-signed output. MCP-compatible. 167 tests in 1.5 seconds. The hardest part of your agent is the trust primitive — we hand it to you in 4 lines."

[GitHub: github.com/CSOAI-ORG]

---

**#1 line for dev due diligence:** "MIT-licensed. pip install. 4-line API. Ed25519 by default. MCP-compatible. 167 tests in 1.5 sec."
