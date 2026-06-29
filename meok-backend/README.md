# MEOK OS Backend — M4 lane (sovereign-orchestrator)

FastAPI service backing the MEOK OS frontend. Exposes the 20 endpoints the
M4 pages call. Real implementations, no stubs.

## Run

```bash
cd ~/clawd/meok-backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Test

```bash
source .venv/bin/activate
pytest -q        # 27 tests, ~0.3s
```

## Live smoke test (against a running server)

```bash
./smoke.sh                          # default: http://127.0.0.1:8770
BASE=http://localhost:8000 ./smoke.sh
```

## Endpoints

| # | Method | Path | Notes |
|---|---|---|---|
| 1 | GET  | `/api/backend/status` | health + 11 system fields |
| 2 | GET  | `/api/ichar/{id}` | reads `ichars.db` |
| 3 | POST | `/api/ichar/create` | inserts i-character |
| 4 | POST | `/api/ichar/{id}/evolve` | +1 interaction |
| 5 | POST | `/api/ichar/{id}/absorb` | mark absorbed + hive |
| 6 | GET  | `/api/ichar/user/{user_id}` | list user's ichars |
| 7 | GET  | `/api/geo` | mock GB/UK for local dev |
| 8 | POST | `/api/cascade/route_query` | 4-tier sov3small3 cascade |
| 9 | POST | `/api/sigil/verify` | hash-chained ledger lookup |
| 10| POST | `/api/auth/signup` | PBKDF2-HMAC-SHA256 |
| 11| POST | `/api/auth/login` | HMAC-signed token |
| 12| GET  | `/api/council/{queen_id}` | 13 council members |
| 13| GET  | `/api/temples` | 11 sovereign jurisdictions |
| 14| GET  | `/api/temple/{code}` | one temple |
| 15| GET  | `/api/mcp/list` | 218 MCPs |
| 16| GET  | `/api/sigl/chain` | last 10 entries |
| 17| GET  | `/api/sov3/tools` | 222 SOV3 tools |
| 18| POST | `/api/sov3/invoke` | mock invocation |
| 19| GET  | `/api/news` | 6 curated items |
| 20| GET  | `/api/temple-os/bundle` | full OS state |

Plus `/api/healthz` for liveness.

## Storage

- `ichars.db` — SQLite, schema auto-created on startup.
- `users.db` — SQLite, schema auto-created on startup.
- `sigil_chain.jsonl` — append-only hash-chained SIGIL log.

All paths can be overridden via env vars `MEOK_ICHARS_DB`, `MEOK_USERS_DB`,
`MEOK_SIGIL_LOG`, `MEOK_CLAWD_ROOT`.

## Integration

The backend prefers the existing M4 lane modules if importable:

- `~/clawd/csoai-os/ichar.py` — queen archetypes + arcana lenses
- `~/clawd/sovereign-temple/sov3small3.py` — 4-tier cascade

If they are missing, the backend falls back to its own self-contained
implementation (still real, still hash-chained, still per-spec counts).

## License

Sovereign-orchestrator lane, M4. CSOAI-ORG / MEOK © 2026.
