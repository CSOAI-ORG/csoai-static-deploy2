# ONE-MAN-CORPORATION OS — Deployment Architecture & Install Plan (2026-08-15)

## Compute placement decisions (binding)

| Harness | Where | Why not A100 |
|---|---|---|
| **csoai_board (CEO router)** | Oracle micros + K3 burst | API-call agent — uses OpenRouter/frontier for reasoning, needs no GPU. The existing micros are already running cron. |
| **Twenty CRM** | A100 /runpod volume (Docker) | Lightweight (Node + PostgreSQL, ~1GB). Installed on the persistent volume while the A100 is running; easy to move to a £5 VPS later. |
| **ERPNext** | A100 /runpod volume (Docker) | Heavier (Frappe + MariaDB + Redis + Nginx, ~4GB). Same rationale — persistent volume, easy migration. |
| **n8n** | A100 /runpod volume (Docker) | 200k★ workflow automation — connects MCP fleet to press/sales pipelines. |
| **Twenty + ERPNext data** | /runpod/sovos-corp-data | Survives pod restarts. If the pod is replaced, the volume is reattached. |

**Total storage on /runpod: ~84G free. Twenty + ERPNext + n8n: ~8GB.** No impact on measurement work.

## Install order

1. **Docker + Docker Compose** (on A100) — needed for everything
2. **Twenty CRM** (lightest, fastest win) — csoai_board CRO seat wires to it
3. **n8n** (workflow automation) — connects board actions to real execution
4. **ERPNext** (heaviest — needs Frappe bench) — CFO seat wires to it

## ✅ ACTUAL RESULTS (2026-08-15)

**Docker verdict: BLOCKED on the RunPod pod.** The sandbox forbids nested
mounts (`operation not permitted` on overlayfs, vfs, AND `unshare`). Docker
nested-in-container is not viable on this pod. **GO NATIVE instead** — this
is the correct pattern for container pods anyway (lighter, no nesting).

**Twenty CRM: ✅ LIVE at http://localhost:3000 (HTTP 200).**

- Postgres 14.23 + Redis + Node 24.19 installed natively
- `twenty_crm` database created (user `twenty`)
- repo cloned to `/runpod/corp-services/twenty`
- `yarn install --immutable` (yarn 4.13.0, Node ^24.5 required)
- `nx build twenty-server` + `nx run twenty-server:database:init:prod` — all
  migrations applied
- Server + worker running: `Nest application successfully started`
- **Watchdog armed**: `/usr/local/bin/corp-services-start.sh` (cron */5)
  restarts server/worker/Postgres/Redis if they die

**Auto-start commands:**
```bash
cd /runpod/corp-services/twenty
yarn nx run twenty-server:start:prod    # server :3000
yarn nx run twenty-server:worker:prod   # worker
```
**Login:** first-run signup at http://<pod-ip>:3000 (create the workspace)

## Twenty CRM install

```yaml
# docker-compose.twenty.yml
services:
  twenty:
    image: twentycrm/twenty:latest
    ports: ["3000:3000"]
    environment:
      APP_SECRET: "${TWENTY_SECRET}"
      PG_DATABASE_URL: "postgres://twenty:${PG_PASS}@postgres:5432/default"
    volumes:
      - twenty-data:/data
    depends_on: [postgres]
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: twenty
      POSTGRES_PASSWORD: "${PG_PASS}"
      POSTGRES_DB: twenty_crm
    volumes:
      - pg-data:/var/lib/postgresql/data
```

## ERPNext install (via Frappe Docker)

```yaml
# docker-compose.erpnext.yml (simplified — easy:init for full setup)
services:
  mariadb:
    image: mariadb:10.6
    volumes: [mariadb-data:/var/lib/mysql]
  redis:
    image: redis:7
  frappe:
    image: frappe/erpnext:v15.25.1
    ports: ["8080:80"]
    volumes: [erpnext-data:/home/frappe]
    depends_on: [mariadb, redis]
```

## csoai_board → harness wiring (to build after installs)

Each CEO seat's stub code (already working — 6/6 tests pass) needs a real
endpoint client. The pattern:

```python
# CFO seat — from stub to real ERPNext client
@register_harness("CFO")
def cfo_harness(intent, payload):
    if intent == "open_invoice":
        # ERPNext API call
        resp = requests.post("http://localhost:8080/api/resource/Sales Invoice",
            json={"customer": payload["client"], "total": payload["amount"]},
            headers={"Authorization": f"token {ERPNext_API_KEY}:{ERPNext_SECRET}"})
        return {"seat": "CFO", "status": "posted" if resp.ok else "failed",
                "invoice_id": resp.json().get("data", {}).get("name")}
    ...
```

## The 3-pilot plan (this week, £0 compute)

Day 1: Docker on A100 + Twenty CRM (CRO seat goes from stub to real)
Day 2: n8n + press workflow wiring (CMO seat)
Day 3: ERPNext base install + CFO seat wiring
Day 4: All 3 wired end-to-end through csoai_board

## Migration from A100 (when revenue comes)

The data lives on /runpod volume, which is portable. When we have revenue:
→ Move Twenty + ERPNext to a £5–10/mo VPS (Hetzner, OVH, Digital Ocean)
→ The router + CEO agents stay on the Oracle micros (they're API-call agents)
→ GPU fleet stays GPU fleet

---

*Status: architecture documented, csoai_board harness tested (6/6 PASS).
Next: install docker on A100, then Twenty CRM.*