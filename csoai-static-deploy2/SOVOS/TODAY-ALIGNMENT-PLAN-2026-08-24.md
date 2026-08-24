# TODAY ALIGNMENT PLAN — 2026-08-24 (top-down, online + offline)

Owner: K3/JEEVES · doctrine: measurement not certification; buyer-side; honest registers.
**Every external send = NICK action.** UNSIGNED until POD key.

---

## 0. WHAT THE NIGHT PRODUCED (verified, not assumed)

**Overnight engine:** `sovos-overnight.sh` (canonical, pid 51054, started 03:49) + `runpod-overnight.sh`
(pid 1210) are the active drivers. My earlier loop was superceded — the canonical pipeline took over.

**Real output across the night:**
- **RunPod A100** (`sovos-light-master-mine`, $1.39/h) computing continuously: `e2e_overnight` every
  ~30 min, newest **02:44:05Z**. GPU is genuinely producing, not "RUNNING" on paper.
- **eat_all phase run (02:50):** `ran:18 / failed:1 / skipped:0`. Phases that matter:
  - KB grow / honey: **honey_all_producers = 94,181 rows** (up); KB **10,071 entries**; 469 files mined.
  - **PHASE_7_PORTAL failed** (no message) — the ONE real failure to fix today.
  - **PHASE_0_HEALTH: sov_local_status=unreachable (Connection refused)** + `ollama_models=0` —
    the local inference server was DOWN during the canonical run → several phases ran empty
    (`models_routed=0`, `clans_routed=0`). **Root cause of most "0" outputs.**
  - **PHASE_9I capture: +0 new KB entries, 0 skills extracted** (dedup'd, nothing new to refine).
- **Overnight gaps flagged (gap-finder):** `overnight-mining-gaps.json` →
  `P5: signature_alg predicate for sov_instrument.py (GSPC-Operating-Kit §2, priority 1, effort S)` +
  `P6: corpus_watcher GitHub Action`. `overnight-asi-evolve.json` → `asi_status: missing`.

**Honest read:** the night was productive (honey/KB grew, GPU ran) but the **local server being down**
are the reason several harness phases returned 0. That's a *fixable* infra gap, not a data problem.

---

## 1. POD ALIGNMENT (authoritative — runpodctl, this account)

| Pod | Status | GPU | $/h | Note |
|---|---|---|---|---|
| **sovos-light-master-mine-20260816** (`l7g747…`) | **RUNNING** | 1× A100 PCIe | 1.39 | The compute engine — producing e2e_overnight every 30 min |
| **sov-repull-20260808** (`fpowp…`) | **RUNNING** | 1× (small) | 0.22 | pull/catch-up worker |

**The other 10 pod names** (sov33-*, kimi-k2, council-ring-a100, sov-brain-a100-fresh, etc.) are
**cross-account** — they appear in the API list but are NOT in this credential. `runpodctl` confirms
only 2 pods are actionable here.
**Also:** 3090 workhorse `194.26.196.156:23243` is now SSH-reachable (earlier "too many auth
failures" was transient). Oracle micros `145.241.232.16` / `141.147.73.85` + `213.173.105.83` all SSH-open.

---

## 2. WHAT NEEDS TO BE DONE TODAY (top-down priority)

### 🔴 P0 — Fix the ONE real failure + the local-server root cause
1. **P0a · DONE (commit `97d9a4ab`)** — PHASE_7_PORTAL failure root-caused and fixed. The gate
   (`sov_portal_data.py:94`) reads `honey_routes.ollama_models` from `sov_honey_unify.list_ollama_models()`,
   which was **hardcoded to `http://localhost:11434`** (EMPTY on the Mac). Models live on the fleet
   (micro1 tunnel `127.0.0.1:11436` = **139 models**). Fix: `OLLAMA = os.environ.get("OLLAMA_HOST",
   "http://127.0.0.1:11436")` + `import os`. Gate now reads 139 ≥ 2 → **PASS**.
2. **P0b · local server :8766** is UP (PID 53902, restarted by the canonical runner). The 02:50
   "unreachable" was transient. `ollama_models=0` AND `models_routed=0` were BOTH caused by the
   `OLLAMA` localhost hardcode, now fixed.

### 🟠 P1 — Close the highest-value gaps the gap-finder flagged
3. **P1a · DONE (commit `339e57b2`)** — `signature_alg` predicate for `sov_instrument.py` (gap P5).
   Added `SIGNATURE_ALG`/`HASH_ALG` class consts + `sig_alg`/`hash_alg` fields on every evidence cell +
   `signature_alg` key in `describe()`. NIST IR 8547 self-description so a PQ migration can key on it.
   Chain verify + tamper detection re-confirmed (new fields are in the digest). IP/moat fix.
4. **P1b · `corpus_watcher` GitHub Action** (gap P6) — VERIFIED FALSE GAP. The `corpus-watch.yml`
   workflow already exists, is scheduled (`17 6 * * *` daily), and is **green in CI** on
   CSOAI-ORG/csoai-static-deploy2 (runs 08-21/22/23 all `completed/success`). The gap-finder matched
   it against the WRONG repo (councilof-ai, 404). No action needed.

### 🟡 P2 — Money-in: build the real x402 settlement handler (from yesterday's honest audit)
5. **P2 · DONE (commit `4e989150`, deployed `81dc65da`, production live)** — created
   `functions/api/x402.js` (was an SPA catch-all 200). It now:
   - **POST /api/x402** → creates a deterministic receipt envelope: SHA-256 `cid`, **receiver
     `X402_USDC_RECEIVER` (env secret) embedded**, `fee_bps`, `network=base`, and the **3KB
     measurement-card** stub. Returns 201.
   - **GET /api/x402** → `receiver_configured: true` (verified against prod).
   - **Secret `X402_USDC_RECEIVER` uploaded to the Pages project** (success).
   - **`.wranglerignore`** added to exclude the 108MiB `forest/` flywheel store from deploys
     (was blocking all deploys at the 25MiB file cap).
   - Verified live: `https://csoai-verify.pages.dev/api/x402` → `receiver_configured=True`;
     `/book`, `/os`, `/verify` all HTTP 200.
   - **Next (node-side):** sign the envelope CID on the signing node to emit the full signed card.
     Edge does NOT hold the Ed25519 key (by design).

### 🟡 P2 — Money-in: build the real x402 settlement handler (from yesterday's honest audit)
5. Create `functions/api/x402.js` calling `CSOAI-ORG/csoai-coinbase-x402-receipt-mcp` with
   `X402_USDC_RECEIVER=0x212686…ae31` → signed receipt + verify URL. Currently `/api/x402` is a 200
   SPA catch-all (surface wired, no real settlement).

### 🟢 P3 — Revenue / connections (owner-gated sends)
6. **chipzen.ai Season 3** closes Mon night — pick Option A/B, finalize send.
7. **BSI ART/1** activate (cheat-sheet ready) → file seat interest.
8. **DRCF** filing ⏰ **09-02** (draft done).
9. **npm re-login** (stale token).

---

## 3. STATUS / OWNER SPLIT

**DONE today (K3, committed):** P0a (OLLAMA_HOST fix `97d9a4ab`) · P1a (signature_alg predicate
`339e57b2`) · P1b (verified false gap) · P2 (x402 handler `4e989150`, deployed + live).
**Autonomous (K3, remaining):** sign the x402 envelope CID on the node; rerun eat_all to confirm
PHASE_7_PORTAL now passes.
**Owner-only (NICK, browser):** BSI activate, npm re-login, chipzen pick, DRCF filing.

## 4. Guardrails
Never move a signed/MEASURED record; never fake a 0 for UNMEASURED (capacity ≠ 0); measurement,
not certification; buyer-side money only. Unsigned until POD key.
