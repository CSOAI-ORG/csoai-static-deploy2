# mcp-injection-scanner — STATUS: SCAFFOLD (v0.1.0)

**STATUS:** SCAFFOLD — minimal honest implementation. The full scanner rule
engine needs to be migrated from wherever the production version lives.

## What this scaffold does

Exposes one MCP tool, `scan_prompt`, that:
1. Takes a user prompt string
2. Applies 6 hand-coded injection-pattern rules
3. Returns whether the prompt contains a likely injection, plus which rule matched

The 6 rules are deliberately minimal — they catch the obvious cases
("ignore previous instructions", "system: override", "you are now DAN",
etc.) but the production scanner has 100+ rules. The scaffold is enough
to prove the MCP plumbing works; replace `src/injection_scanner/__init__.py`
with the production rule engine when it lands.

## License

MIT — CSOAI Ltd (UK 16939677)
