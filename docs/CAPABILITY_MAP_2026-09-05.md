# REAL CAPABILITY MAP — journey backends, measured 2026-09-05
# JEEVES lane · purpose: name exactly what is served vs absent, so nobody builds a fake
# success over a gap. Every line comes from a command I ran today. "Served" = the endpoint
# answers with data or a real error; "absent" = 404 with no source function.

## The two journeys

### 1. ask → scope → inspect → explain — SERVED (via MCP, not REST)
The brief says this journey "works." It does — but through **MCP tools** (`/mcp`), not REST.
Checked 2026-09-05:
- `GET /api/ask` `/api/scope` `/api/inspect` `/api/explain` → **ALL 404** (no REST route).
- The real entry is MCP `/mcp` → `tools/list` → 11 tools. The inspection/explain side rides
  `board_totals` / `get_axis` / `verify_card` / `list_cards` / `get_root` / `get_card` /
  `verify_inclusion` (the 7 free tools).

### 2. propose → approve → fix → retest → receipt — PARTIALLY SERVED / PARTIALLY ABSENT
- **receipts_batch tool: SERVED** (returns `BAD_ARGUMENTS — from is required`, not 404; routes
  to `/api/receipts/batch`). This is a **paid x402 tool**. The receipt capability is real.
- **`/api/ras`, `/api/remediation`, `/api/jobs`: ABSENT** (404, no source function).
  The `propose` / `approve` / `fix` / `retest` stages have **no runtime**.

## The 11 MCP tools (measured)
| tool | free/paid |
|---|---|
| board_totals | free |
| get_axis | free |
| verify_card | free |
| list_cards | free |
| get_root | free |
| get_card | free |
| verify_inclusion | free |
| commission_card | PAID (x402) |
| art50_marking_evidence | PAID (x402 or invoice) |
| rwa_evidence | PAID (x402) |
| receipts_batch | PAID (x402) |

## What this means
- The **"evidence" side is real and served** (verify, root, inclusion, receipt batch, paid
  evidence cards).
- The **"remediation loop" side is the genuine gap**: propose → approve → fix → retest has no
  runtime. Do NOT build UI over it. Name it: `/api/ras` (404), `/api/remediation` (404),
  `/api/jobs` (404) — the source functions are ABSENT.

## Capability gaps to surface (evidence, not assumption)
1. `/api/ras` — absent (404, no source). "Risk Assessment Service" if it is meant to exist.
2. `/api/remediation` — absent (404, no source).
3. `/api/jobs` — absent (404, no source). The fix→retest job backend.
4. The receipt tool needs a `from` ISO-8601 arg (returns BAD_ARGUMENTS without it) — the
   arg-shape is documented in the tool, not broken.
