# defoneos-sign-mcp

**The sovereign assurance layer, as an MCP.** Any Claude agent — Claude Science, Claude Code, a custom agent — hands over an output and gets back a **signed, offline-verifiable DEFONEOS artifact**. The receipt verifies at [defoneos.vercel.app/verify.html](https://defoneos.vercel.app/verify.html) with **no server** — same Ed25519 scheme as the DEFONEOS dome's SIGIL ledger.

DEFONEOS doesn't live *inside* anyone's app. It's the thing the ecosystem calls **into** to make a result auditable, reproducible, and independently checkable. This is that seam.

## Why
The biggest labs now ship "auditable / reproducible" AI outputs (e.g. Claude Science attaches the code + environment + history that made a result). DEFONEOS goes one axis further: the artifact is **cryptographically signed and verifiable without trusting the vendor's server**. This MCP puts that primitive one tool-call away for any agent.

## Tools
| tool | does |
|---|---|
| `defoneos_sign` | wrap `{output, kind, subject, method, inputs}` in signed provenance → receipt (Ed25519). Records method ("how it was made"), input sources, a SHA-256 of the exact output, and the care-floor. |
| `defoneos_verify` | verify a receipt offline (tamper-evident); optionally re-bind the original output to its signed hash. |
| `defoneos_public_key` | the sovereign public key + fingerprint (trust-on-first-use / pin it). |

## Run
```bash
node server.js          # MCP stdio server
npm test                # 12/12 sign→verify→tamper→content-rebind
```
Add to an MCP host (Claude Desktop / Claude Code) config:
```json
{ "mcpServers": { "defoneos-sign": { "command": "node", "args": ["/path/to/defoneos-sign-mcp/server.js"] } } }
```

## What a receipt looks like
```json
{ "defoneos_signed_contact": {
    "message": { "i":0, "ts":"…", "action":"artifact:finding", "detail":"{…method,inputs,output_sha256,care_floor…}", "prev":"" },
    "signature_ed25519": "…128 hex…",
    "public_key_ed25519": "…64 hex…",
    "fingerprint": "SOV:XXXX-XXXX-…" } }
```
Drop it into `verify.html` (paste, file-drop, or `?receipt=<base64url>`), or verify with any Ed25519 library:
recompute `utf8(JSON.stringify(message))`, then Ed25519-verify `signature_ed25519` with `public_key_ed25519`.

## Guarantees & honest scope
- **Ed25519 (RFC 8032)**, raw message sign — cross-library verified (Node `crypto` ↔ `@noble/ed25519` in the browser verifier).
- **Sovereign key** persists at `~/.defoneos/sign.key` (0600); nothing is sent anywhere.
- **Care-floor recorded** in every envelope + a hard-stop note: signed for **assurance only** — no kinetic/surveillance tasking (a Layer-0 hard stop). This MCP signs; it does not act.
- It attests *that an output was produced and by what method*; it does **not** validate the output is scientifically correct. Provenance ≠ truth — that stays with the researcher.

CSOAI Ltd (UK 16939677) · MIT + CC0.
