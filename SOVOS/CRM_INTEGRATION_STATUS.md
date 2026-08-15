# Twenty CRM — integration status (2026-08-15)

## What's live

- Twenty server running on A100 :3000 — `HTTP 200 /healthz` ✅
- PostgreSQL database `twenty_crm` created, migrations applied ✅
- GraphQL endpoint responds (schema introspection OK) ✅
- Watchdog armed (cron */5 restarts server/worker/Postgres/Redis if down) ✅
- `csoai_crm.py` — CRO-seat API client written, tested connectivity ✅
- Repo: `/runpod/corp-services/twenty` on persistent volume ✅

## What blocks the CRM objects

Twenty mints its CRM objects (companies/people/notes) only after the
**first-run workspace wizard** — a UI step that creates the tenant + custom
objects. Until then, standard queries (`{ companies }`) return "Unknown type".

**Owner step (5 min):** open http://<A100-pod>:3000 in a browser, complete the
workspace-creation wizard, then the CRO seat client can create/query companies:

```bash
cd /workspace/jeeves-exec && python3 SOVOS/agents/csoai_crm.py --list
python3 SOVOS/agents/csoai_crm.py --create-company "Adobe Inc." --domain adobe.com
```

## The wiring (once wizard done)
- `csoai_board.cro_harness` (why the stub exists):
  `add_prospect` → `csoai_crm.py --create-company <name>`
- Pipeline stages map to Twenty opportunities; every CRM action signed
  (board ledger), firewall-linted (no paid-placement language)

## Alternative if wizard is slow
Twenty also exposes a REST-ish setup endpoint; the canonical path is the UI
wizard. If we can't reach the pod's :3000 from a browser (SSH tunnel), open:
`ssh -L 3000:localhost:3000 root@104.255.9.187 -p 11703` then browse
`http://localhost:3000`.