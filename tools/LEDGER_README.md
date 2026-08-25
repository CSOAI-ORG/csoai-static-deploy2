# COORDINATION LEDGER — the living single-source-of-truth (2026-08-25)

**Purpose:** one structured file the whole team (JEEVES / Claude / Cursor / K3 / fleet)
reads + appends to, so outreach, connections, accounts, and moves are **mapped + tracked
in the same place** — never duplicated, never orphaned. This is the "living database"
everyone works against.

**File:** `COORDINATION_LEDGER.json` (root of csoai-site-main) + `tools/ledger.py`.

## How to use (dedup-aware, no secrets)
```bash
# list everything
python3 tools/ledger.py list
# add or update an entry (dedup on key; ==canonical key==, not free text)
python3 tools/ledger.py add '{"key":"outreach:chipzen-x402","type":"outreach","target":"chipzen/x402","status":"ready_to_send","owner":"OWNER_nick"}'
# move a status + note
python3 tools/ledger.py set '{"key":"outreach:chipzen-x402","status":"sent","note":"owner sent 2026-08-25"}'
```

## The rules (do not break)
- **Dedup on `key`** = `slug(type:target)`. Never create a duplicate of an existing key — update it.
- **NEVER store a password / API key / private key / secret.** Accounts list *fields + status + frames* only.
- **Append-only + honest**: outreach status is `sent` ONLY when actually sent; a decline/await is its own status.
- **Owner gates**: status=`gated_owner`, owner=`OWNER_nick`. I can prepare; the owner executes (credentials never in chat).
- **Walls**: measurement not certification (JI.4) · attestation = opinion/measurement, never a token/ownership/claim · R8 regulators free forever · no mass email, one-to-one PR only.

## Who + where
- Repo: `csoai-static-deploy2` branch `aligned-front-20260817`, file `COORDINATION_LEDGER.json`.
- Mirror to `~/.clawdbot/shared-knowledge/` so all agents read the same state.
- Backstop the 300-move plan: `NEXT_300_MOVES_2026-08-25.md`. Live state: `JEEVES-CURSOR-HANDOFF-2026-08-25.md`.
