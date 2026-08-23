# MASTER PLAN 2026-08-22 — SORT MAC → OFFLOAD TO RUNPOD/ORACLE → TRUE MEASUREMENT BODY E2E
### JEEVES lane · top-down alignment · full sweep · next-300-move spine

> Objective: **empty the Mac** (work → RunPod/Oracle RAG volumes), **drive the frameworks-drum to a
> TRUE measurement body E2E**, **take every estate surface to production-ready 100/100 A++++**,
> and run the **EAT loop** (mine → improve → research → test → audit → improve).

---

## ⚠️ URGENT STATE (verified)
- **Mac disk: 98% full, ~4.8Gi free** (`/System/Volumes/Data`). It cannot run training/inference.
- **RunPod RAG volumes (offload targets):** `k3-weights-2tb` (2TB) · `sovos-merge-800` (800GB) ·
  `sov-models` (300GB) · `sov-artifacts` (200GB) · `sov-workspace-mtl4` (200GB). **Plenty of space.**
- RunPod API + Oracle OCI creds verified. `sov-repull` pod RUNNING.
- Drum bundle already staged: `_evacuation/runpod-bundles/20260822-frameworks-drum/`.

---

## PHASE 0 — SORT THE MAC (move work OFF, don't delete)
Priority = move the big, regenerable + work artifacts to RunPod/Oracle, in this order:
1. **`~/.ollama` (5.5G)** — model weights → `sov-models` volume (300GB). *(Confirm no Mac-only inference needed.)*
2. **`~/.npm` (1.6G)** + HuggingFace cache — re-downloadable; `npm cache clean --force` + HF cache prune.
3. **`clawd/.git` (3.3G) + `csoai-static-deploy2/.git` (1.1G)** — bundle+push the active repos to `k3-weights-2tb` / `sovos-merge-800`, then `git gc` (only AFTER offload, to avoid repack-at-98%).
4. **Drum + FLEET artifacts** → `sov-artifacts` (200GB) / `k3-weights-2tb`.
5. **`~/Library` caches (app support, podman, etc.)** — prune only the clearly-regenerable.
> RULE: never delete a sibling-lane artifact mid-flight; never purge `~/.cache/uv` (kimi-code runs from it);
> never purge without owner OK on an estate asset.

**Offload mechanism:** attach a network volume to a cheap CPU pod (`sov-artifacts`/`sovos-merge-800`),
SSH in, `rsync -a` the staging dirs off the Mac. Keep the Mac as a thin terminal (browser/mail/CI),
matching the "Mac = terminal" doctrine. Verify with `df` after each leg; log each transfer.

---

## PHASE 1 — FRAMEWORKS-DRUM → TRUE MEASUREMENT BODY (the 5 gaps, from the audit)
The drum is a world-class **reference index** but NOT a measurement body (0/612 items signed).
Close in priority order:
1. **SIGN/CHAIN/ANCHOR (the trust product)** — ship the **#dsh Ed25519 rail**; sign the catalog manifest,
   scorecard, board, model cards (EAT boxes 3/4/5). This is THE gating gap. `[GATE #dsh]`
2. **Trusted-router score** — realized error 0.3684 > α=0.05 across 3 honest negatives. Try a
   **calibrated/majority-confidence or retrieval-grounded** score; only flip `trusted:true` ≤ α.
   Or accept honest human-gated routing. `[LANE]`
3. **SOV SIGNAL measured gauge** (real, not mock) — feature-layer → manifold → measured gauge → sign.
4. **Deterministic-vs-predictive boundary** — state explicitly: drum predicts document attributes;
   GSPC layer measures model behavior deterministically. Both signed.
5. **Monorepo substrate** — one registry (`registry/mcp-catalogue.json`), harvest shadow copies
   (`csoai-static-deploy2`/`kimi-regen`/`csoai-org-v2`/`csoai-platform`), kill count drift (819/890/966).
6. **Independence firewall test** — prove "measure, never fix/certify" + offline third-party verify of a signed card.

---

## PHASE 2 — PRODUCTION-READY 100/100 A++++ (estate-wide)
- **All gates green** (drift-guard, test, e2e, scorecard) — verify daily; auto-redeploy on thin (already landed).
- **Signing at rest** — every published surface carries an Ed25519-signed, offline-verifiable credential.
- **Real EAT 7-box**: measured→CI'd→signed→chained→anchored→boarded→mirrored.
- **Contamination guards** — canary strings, frozen held-out evals, no-train-on-evals (CI-enforced).
- **Independent-host mirroring** — board/catalog mirrored to ≥2 hosts (RunPod + CF + Oracle).

---

## PHASE 3 — THE EAT LOOP (continuous, cadence)
Mine → index → graph → train → feature-layer → verify → publish, every night; verify every 15 min,
signed every fold. **Standard:** keep-if-better on significance; publish honest negative results;
corrections ledger appended-never-deleted.

---

## NEXT-300-MOVE SPINE (consolidated)
Fold the drum's `NEXT_100_MOVES` sets 1/2/3 + my 5 gap-closers + the offload + production-readiness into
one executable queue. Tag every move `[DONE]`/`[GATE]`/`[LANE]`/`[SELF]` with evidence. Re-number at each
completion (the drum's move-100 discipline).
