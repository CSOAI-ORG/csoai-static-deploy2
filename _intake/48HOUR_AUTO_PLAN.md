# 🐉 48-HOUR AUTONOMOUS EXECUTION PLAN (17-19 Jun 2026)
**Operator:** JEEVES (Hermes) → GCP VM meok-backend
**Author:** Nick is OUT — full autonomy, no human gates
**Constraint:** All execution via GCP VM (Mac may be offline)

---

## PHASE 1 (H0-H2): Infrastructure — VM cron jobs + watchdogs

### Deploy VM-resident cron jobs
```bash
# 1. Keystone cert factory — 100 certs every 6h
# 2. Hive fleet health check — every 30 min
# 3. Autoresponder scanner — every 15 min
# 4. Uptime monitor — every 5 min
# 5. IndexNow submission — every 12h
```

### Services to verify VM-resilient
- [x] sov3.service — running ✅
- [x] meok-king.service — running ✅
- [x] meok-council.service — running ✅
- [x] meok-one.service — running ✅
- [x] cron.service — running ✅
- [x] nginx.service — running ✅
- [ ] Set up LaunchAgents equivalent via systemd timers

---

## PHASE 2 (H2-H6): Keystone cert sprint (substrate lane)

| Batch | Count | Category | 
|-------|-------|----------|
| Governance | 100 | EU AI Act, ISO 42001, COAI compliance |
| Risk | 100 | DORA, NIS2, CRA frameworks |
| Trust | 100 | Ed25519, C2PA, watermarking |
| **Total** | **300** | |

Run via VM cron — no Mac needed, keystone is Vercel-hosted.

---

## PHASE 3 (H6-H14): Identity/SEO content (VM-served)

### Deploy 30 staged iCloud pages to VM nginx
- Copy page.tsx content as static HTML
- Add to nginx serve dir
- Submit IndexNow from VM

### AEO/llms.txt files
- Deploy 36 files to nginx
- Submit to commoncrawl + IndexNow

### FAQPage JSON-LD
- Deploy 25 schema files
- Submit to Google via IndexNow

---

## PHASE 4 (H14-H24): Content pipeline

### Blog posts
- Publish 5 drafted blog posts to VM nginx
- Submit IndexNow

### Social posts
- 5 posts from D22 offensive — stage for Buffer/tweet

### SEO keyword audit
- Run seo-keyword-audit.py on VM
- Generate gap report

---

## PHASE 5 (H24-H36): Deep substrate work

### BFT council expansion
- Add 3 new BFT councils via VM's SOV3
- Register 15 new voter seats

### Keystone cert page
- Deploy the keystone-certs.html to production nginx
- Integrate with COBOLBridge.ai, ethicalgovernanceof.ai

### SOV3 memory consolidation
- Query VM SOV3 for all memory episodes
- Write consolidated summary

---

## PHASE 6 (H36-H44): MCP monetization (D20 aligned)

### Smithery submissions
- Submit top-10 MCPs to Smithery
- Verify builds

### Glama submissions (web UI)
- Check if Glama UI has changed
- If accessible via browser-use on VM, submit

### PyPI readiness
- Verify all 18 pyproject.toml MCPs have proper metadata
- Stage wheels for twine upload (gated on gh auth)

---

## PHASE 7 (H44-H48): Final check + seal

### Full audit
- All 5 surfaces: HTTP 200
- SOV3: verify_fail=0
- Keystone: HTTP/2 200  
- Autoresponder: flowing
- Hives: 29+ LIVE

### 48-hour completion report
- Write to VM empire_mirror
- Write to shared handoffs

### SOV3 sigil seal
- Emit 48-hour completion sigil

---

## CRITICAL NOTES

### What works without Mac:
- ✅ All curl/SSH to GCP VM (meok-backend)
- ✅ keystone API (Vercel-hosted)
- ✅ SOV3 on VM (:3101 via SSH)
- ✅ cron jobs on VM
- ✅ nginx content serving on VM

### What Mac-dependent (won't run if Mac off):
- ❌ `vercel deploy` (needs local Vercel token)
- ❌ Local SOV3 at localhost:3101 (use VM SOV3 instead)
- ❌ iCloud writes (use VM empire_mirror instead)
- ❌ `claude` CLI (use VM scripts instead)

### Contingency
- If VM disk hits 85%+: auto-clean /tmp + old session logs
- If SOV3 crashes: `systemctl restart sov3.service` via cron
- If nginx goes down: auto-restart via systemd
- If cron jobs fail: retry 3x with exponential backoff
