# SOVOS_CHAIN KV BINDING ATTACH — OWNER ONE-PAGER (2026-08-25)
# JEEVES lane → owner. ONE dashboard action turns /api/attest `chained:false` → true.

## Why
`/api/attest` mints a signed chain card and links it to the previous head via KV.
Without the binding it returns `chained:false` (signed, but not persisted across
invocations). Attaching SOVOS_CHAIN makes the ledger durable — every attestation
chains to the last, `/api/chain` walks the real persistent ledger, and the register
rollup counts real chained cards. This is the LAST gate to a fully persistent,
stranger-verifiable enforcement ledger.

## What (exact steps — Cloudflare Dashboard, ~2 minutes)
1. Cloudflare Dashboard → your account (Nicholastempleman@gmail.com / 52092e4dad74b51759a2f748c8cf2528).
2. **Workers & Pages** → **csoai-gspc** (the project, NOT csoai-site).
3. **Settings** → **Functions** → scroll to **KV namespace bindings** → **Add binding**.
4. **Variable name:** `SOVOS_CHAIN`
5. **KV namespace:** select the existing namespace **SOVOS_CHAIN** (id `b4eb1252766040d68bf6b10e6470ab57`).
   (It already exists — create nothing new.)
6. **Save.** Cloudflare redeploys; the binding is live for all future invocations.

## Verify (after attach)
```bash
curl -s -X POST https://csoai-gspc.pages.dev/api/attest \
  -H 'content-type: application/json' \
  -d '{"sector":"bond","subject":"chain test","text":"regulated, KYC, privacy, atomic"}'
# expect: "chained": true  (was false)
curl -s 'https://csoai-gspc.pages.dev/api/chain?n=5'
# expect: cards[] with prev links — the persistent ledger
```

## NOTE — why it's dashboard-only (verified twice)
`wrangler pages` has NO KV-binding subcommand (only `deploy`/`deployment`/`project`).
The existing `[[kv_namespaces]]` block in `wrangler.toml` belongs to the **Workers**
`csoai-site` deploy (`pages_build_output_dir = "_site"`), NOT the `csoai-gspc`
**Pages** project. There is no CLI path to attach a KV binding to a Pages project;
it is dashboard-only. I cannot do this from code — it is genuinely owner-gated.

## Other namespaces (already exist, wired in wrangler.toml) — do NOT touch
SOV_TOWN_STATE · SOV_OPENTTD_STATE · SOV_ARENA_STATE · EAT_OWEM · SOV_CRDT_STATE · VERIFY_COUNTER · WEBHOOKS.
