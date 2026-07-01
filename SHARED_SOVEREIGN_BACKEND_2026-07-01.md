# THE shared Sovereign backend — one brain for MEOK, CSOAI & DEFONEOS (2026-07-01)

Nick's ask: "we want the SAME sovereign backend for meok, csoai and defoneos." Done — here it is,
live and CORS-open on `os.meok.ai`, aligned to DEFONEOS/JEEVES's existing contract so all three
surfaces converge without a rewrite.

## The shared contract (already how DEFONEOS's sov3-llm-brain.js works)
Every surface exposes two globals; ONE brain drives them all:
- `window.getScreenContext()` → what the Sovereign SEES (`{surface, space, open_windows, active_layers,
  last_inspected_node, selected_node, doctrine, brain, care_floor}`). ✅ MEOK OS now exposes this,
  same shape as DEFONEOS's cop.html.
- `window.sovereignOSCommands` → what the Sovereign can DO (open_app, set_space, explain_node,
  observe_focus, govern, fly_to, sign, validate_bridge, utter). ✅ MEOK OS now exposes this.

## The shared backend (os.meok.ai/api/* — all CORS `*`)
| Endpoint | Does | Status |
|---|---|---|
| **`/api/orchestrate`** | the BRAIN: `{message, context}` → `{say, actions:[{command,args}]}` (Groq; Claude when credited) | ✅ 20/20 E2E |
| `/api/sign` · `/api/verify` | **Ed25519** sign a governed action / verify offline (the SIGIL moat) | ✅ |
| `/api/bridge` | validate/parse real legacy msgs (IBAN/ISO20022/HL7/ISO8583/SWIFT) | ✅ |
| `/api/govern` | industry → real frameworks + bridges | ✅ |
| `/api/nodes` | canonical sovereign node graph (12 hubs, status, links) | ✅ |
| `/api/chat` · `/api/knowledge` · `/api/tools` · `/api/media` · `/api/badge` · `/api/avatar` | council brain · live world knowledge · tool router · CC media · authority badges · character | ✅ |

## How each surface adopts it
- **MEOK OS** — ✅ already: dock routes NL → `/api/orchestrate` → speaks + runs `sovereignOSCommands`.
- **DEFONEOS (cop.html / JEEVES)** — point the brain + tools at the shared backend:
  ```js
  window.SOV3_BRAIN_ENDPOINT = 'https://os.meok.ai/api';   // orchestrate/chat
  // and call the shared sovereign tools directly:
  //   POST /api/sign  /api/verify  /api/bridge  /api/govern  |  GET /api/nodes
  ```
  JEEVES's `sov3-llm-brain.js` already reads `getScreenContext()` + invokes `sovereignOSCommands` —
  identical contract. Two options: (a) keep its OpenAI-streaming brain, adopt the shared **tools**
  (`/api/sign|verify|bridge|govern|nodes`); or (b) switch its brain to `/api/orchestrate`
  (`{say, actions}` — one adapter in `askBrain()`). Either way the sovereign **services are one**.
- **CSOAI** — same globals + same endpoints.

## SIGIL alignment (the moat, unified)
- Shared signer = `/api/sign` (Ed25519, seed-stable via `SIGIL_SEED`; owner sets the real sovereign
  King seed once → identical signatures across all three). Verify offline anywhere with `/api/verify`.
- DEFONEOS adds **PQC ML-DSA-65** on top — fold that into `/api/sign` as a second signature field
  when ready (Ed25519 stays the interop baseline all three verify).

## One honest note
`/api/orchestrate` returns `{say, actions}` (simple, model-agnostic, reliable). JEEVES's bridge
speaks OpenAI `/chat/completions` streaming + `tool_calls`. To make os.meok.ai a *drop-in* for that
bridge unchanged, add an OpenAI-compat streaming shim later; for now the `{say, actions}` contract is
the clean shared standard and DEFONEOS needs a ~10-line adapter. The **tools** (sign/verify/bridge/
govern/nodes) are already 100% shared, today.

— M4
