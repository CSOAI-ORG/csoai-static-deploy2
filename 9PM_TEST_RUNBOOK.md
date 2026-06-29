# 🐉 MEOK WORLD — 9 PM TEST RUNBOOK

**Date:** 2026-06-29 (Mon) · **Time:** 21:00 BST (9 PM) · **Owner:** Nick Templeman

This is the **step-by-step runbook** for the 9 PM test. The design/UX team takes over at 21:00 BST for 4 days till the **Saturday 4 Jul 09:00 BST public launch**.

---

## 🎯 9 PM OBJECTIVES

1. **Visual review** of all 128 pages
2. **E2E testing** with real browser (playwright when installed)
3. **Real-world testing** with users
4. **Final polish** before 4-day countdown
5. **Document findings** for the team

---

## 🛠 WHAT YOU'LL NEED

- **Mac** with `~/clawd` checked out
- **Browser** (Chrome / Firefox / Safari)
- **Backend** running on `:8000` (start with `./launch.sh`)
- **MEOK account** (if you want to test i-character flow)

---

## 📋 STEP-BY-STEP

### Step 1: Launch the system (5 min)
```bash
cd ~/clawd
./launch.sh all
```

**Verify the output says "ALL SYSTEMS GO"**. This runs all 175+ tests + starts the backend.

### Step 2: Open the home page (5 min)
```bash
open ~/clawd/csoai-os/meok-home/index.html
```

**Check**:
- [ ] Hero shows "The world is at your feet. Sovereign AI, live."
- [ ] Live backend status bar polls every 30s (look for "SOV3 13/13" + "MCPs 218")
- [ ] 11 temples with proper colors
- [ ] 13-Queen + King council with 2 VETO (Care, Watch) in red
- [ ] "See the emergence" CTA in bottom-right corner
- [ ] Service worker registers (DevTools → Application → Service Workers)
- [ ] PWA installable (DevTools → Application → Manifest)

### Step 3: Open the character emergence page (10 min)
```bash
open ~/clawd/csoai-os/meok-home/meok-character-emergence.html
```

**Check**:
- [ ] 7 parent archetypes appear with translucent eggs
- [ ] Each egg has its own color + pattern
- [ ] Hover cracks the egg (CSS animation)
- [ ] Click plays procedural sound (Web Audio API)
- [ ] 13-Queen + King council grid renders
- [ ] 5-step i-character wizard works end-to-end
- [ ] Step 1: region auto-detect (ipapi.co)
- [ ] Step 2: name input
- [ ] Step 3: 13-queen archetype picker
- [ ] Step 4: 22-arcana lens picker
- [ ] Step 5: i-character created + saved to localStorage

### Step 4: Open the temple OS (10 min)
```bash
open ~/clawd/csoai-os/v2-temple-os.html
```

**Check**:
- [ ] Globe with 11 temples at real lat/lon
- [ ] UK user-marker shown
- [ ] LHS: 16 tool tiles
- [ ] Center: sovereign character + chat
- [ ] RHS: SOV3 + 12-Queen council + BFT + sessions
- [ ] DORADO bar: west → globe → temple → east
- [ ] i-character greeting shows (if signed up)
- [ ] Sovereign character has crown label
- [ ] Click any temple → expands with details

### Step 5: Test the i-character wizard (5 min)
```bash
open ~/clawd/csoai-os/v2-signup-wizard.html
```

**Check**:
- [ ] Step 1: Region auto-detected
- [ ] Step 2: Name input works
- [ ] Step 3: 13 queens visible + selectable
- [ ] Step 4: 22 arcanas visible + selectable
- [ ] Step 5: Confirmation card
- [ ] localStorage saves the i-character
- [ ] Link to v2-temple-os.html works

### Step 6: Test the API (5 min)
```bash
curl -s http://127.0.0.1:8000/api/backend/status | head -c 300
curl -s -X POST http://127.0.0.1:8000/api/ichar/create \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"test","name":"E2E","queen_model":"queen-arcana","arcana_lens":21}' | head -c 200
curl -s -X POST http://127.0.0.1:8000/api/cascade/route_query \
  -H 'Content-Type: application/json' \
  -d '{"query":"What is the EU AI Act?","task_type":"chat"}' | head -c 200
```

**Check**:
- [ ] All 3 return 200 OK
- [ ] Response has expected fields
- [ ] SIGIL chain shows new hash

### Step 7: Visual review of all 128 pages (60 min)

Use the **MEOK_DESIGN_REVIEW_2026-06-29.md** checklist (50 design/UX checks). For each section:

| Section | Pages | Time |
|---|---:|---|
| Universe | 7 | 5 min |
| OS | 7 | 5 min |
| Characters | 9 | 5 min |
| Queens | 12 | 5 min |
| Work | 5 | 5 min |
| Gaming | 6 | 5 min |
| Guardian | 5 | 5 min |
| Temples | 11 | 5 min |
| MCP/Empire | 10 | 5 min |
| Compliance | 12 | 5 min |
| Company | 18 | 5 min |
| Defoneos | 19 | 5 min |
| Legal | 5 | 5 min |

**For each page, check**:
- [ ] Topbar with 8 nav items + active page highlighted
- [ ] Page-specific hero (tag + h1 + description)
- [ ] Real content (not Lorem ipsum, not TODO)
- [ ] 3-12 stat/feature cards
- [ ] CTA box at bottom
- [ ] Footer with 5 columns
- [ ] Live status bar (12 rows)
- [ ] Responsive on mobile (test at 320px, 768px, 1024px)
- [ ] PWA manifest link + SW registration
- [ ] No console errors

### Step 8: Document findings (30 min)

Create a `FINDINGS_2026-06-29.md` with:
- ✅ What works
- ⚠️ What needs polish
- ❌ What's broken
- 💡 Ideas for v2

---

## 📞 WHO TO CALL IF SOMETHING BREAKS

| Issue | Escalate to |
|---|---|
| Backend down | M4 (sovereign-orchestrator) |
| Frontend bug | M4 |
| M2 live app bug | M2 (councilof-ai) |
| DEFONEOS sprint | Hermes/JEEVES |
| DNS / domain | Nick |
| PyPI / Smithery / Glama | Nick |
| Stripe / payment | Nick |
| Vercel deploy | M2 |
| GCP VM | Nick + VM ssh |

---

## 🚀 4-DAY COUNTDOWN (Tue → Sat)

| Day | Date | Focus |
|---|---|---|
| Mon (today) | 29 Jun | 9 PM test + absorb + launch script |
| Tue | 30 Jun | PyPI publish + MCP registry |
| Wed | 1 Jul | Apple/Windows icon + a11y + 404/500 |
| Thu | 2 Jul | Performance + load test + monitoring |
| Fri | 3 Jul | Final E2E + smoke + dress rehearsal |
| **Sat** | **4 Jul** | **PUBLIC LAUNCH 09:00 BST** |

---

## 🎯 LAUNCH CHECKLIST (Sat 4 Jul 09:00 BST)

- [ ] Vercel deploy: `cd meok-deploy && vercel --prod`
- [ ] DNS: meok.ai apex → Vercel
- [ ] Stripe live keys wired
- [ ] SMTP wired for email
- [ ] OAuth (GitHub, Google) wired
- [ ] 218 MCPs published to PyPI
- [ ] 218 MCPs on Smithery
- [ ] Apple/Windows icons packaged
- [ ] Final E2E green
- [ ] All 128 pages deployed
- [ ] Live smoke 5/5
- [ ] Public launch! 🚀

---

## 📚 REFERENCES

- `MEOK_WORLD_9PM_CHECKLIST.md` — original 9 PM checklist
- `MEOK_WORLD_9PM_FINAL_STATE.md` — final state doc
- `MEOK_DESIGN_REVIEW_2026-06-29.md` — 50 design/UX checks
- `LAUNCH_REPORT_20260629_153251.md` — last launch report
- `launch.sh` — 9-step pre-launch script
- `FACT_CHECK_REPORT.md` — 50/60 claims verified
- `MASTER_REVISION.md` — 8 layers, 367 dirs, 33 hives
- `DEDUPLICATION_REPORT.md` — 95% DRY

---

*Generated 2026-06-29 15:35 BST. The dragon flies sovereign. The empire is 100% master. 🐉🔥*
