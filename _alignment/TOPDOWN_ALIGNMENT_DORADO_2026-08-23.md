# TOP-DOWN ALIGNMENT + FULL PLAN — DORADO measurement body (live pull)

Date: session-verified, not memory. Every number below is read from the live repo /
pods this session.

## 1. Fleet status (online / offline)

| Surface | Host | State | Role |
|---|---|---|---|
| **3090** | `sov-brain-2` (01d43fdfaa57) | ✅ ONLINE · GPU 43% · disk 41% | the live measurement producer (EAT batch) |
| **Oracle micro1** | `sov33-owem-micro` | ✅ ONLINE · disk 81% | backup / evac target |
| **Oracle micro2** | `sov33-owem-micro2` | ✅ ONLINE · disk 36% | backup / evac target |
| **A100** | `sovos-light-a100` (38.128.232.57) | 🔴 UNREACHABLE (offline) | other-lane; down this session |
| **redblue-pod** | 194.14.47.19 | 🔴 UNREACHABLE | other-lane; down |

**The Mac is terminal-only; all measurement runs on the 3090 pod.**

## 2. DORADO repo state (the canonical source of truth)

- Commit: `4a79084` (28+ commits this build).
- Board: content-addressed, append-only; grows live on the pod.
- All suites green: battery, personas, elo, schema, banned-strings.
- CI green on every commit; GitHub Pages live (board, leaderboard, verify, discovery).

## 3. Sprint (Day-1, SPRINT-300-3DAY) — aligned against the repo

**Already DONE in the working repo:**
- 001 naming adopted (DORADO) · 014 licenses (Apache-2.0 + CSL-1.0) · 015 governance
  (donation clause) · 021 measurement-card schema · 022 run-manifest/harness-hash ·
  023 replay-merkle (schema) · 024 13-of-14 grammar · 025 provision-map (crosswalk) ·
  028/030 schema CI · 031-038 RFC draft (kramdown skeleton + COSE_Sign1 alg-19 +
  security + IANA) · 040 README verify-in-60s · 019 signing pod (Ed25519, identity-gate).

**DONE this session (achievable, non-owner-blocked):**
- 002 measurement evidence pack · 009 canon grammar locked
- 010 + 016 **banned-string lint + purge** (caught + fixed a real `llms.txt` leak)
- 040 README verify-in-60s path pointed at a **self-consistent** verify trio
  (fixed the stale-example wart — card/receipt/anchor were inconsistent across rounds)

**OWNER-BLOCKED (only Nick can do — never faked):**
- 001 naming tap (CIVOLA/DORADO adopted; final name is Nick's) · 006 IH P0 authorization ·
  011 cibola.dev/getcibola.com domains (~£15) · 012 UKIPO trademark (~£170) ·
  020 did:web on a real domain
- **Provision the real `#card-attestation-1` pod key** → production-signed cards
  (identity gate auto-recognizes it; zero code change).

**Pod-GPU-bound (infra, not code):**
- a completed live pairwise (12 inference calls exceed a bounded window on the
  contended shared GPU) — machinery proven; needs a quiet/dedicated window.

## 4. Full plan — everything needed today (ranked, agent-executable first)

1. **Run pods** — EAT batch on 3090 across all 6 domains (IN PROGRESS this session;
   board grows live). ✅
2. **Banned-string purge + CI lint** on public surfaces. ✅ (caught real leak)
3. **README verify-in-60s** → self-consistent trio. ✅
4. **Sync the grown board + telemetry** from pod → repo (the authoritative record). ⏳
5. **Frontier-model EAT** on a quiet window = the last measurement benchmark gap. ⏳
6. **Owner-gated (Nick):** real signing key + domain + did:web + trademark.

## 5. Doctrine (holds on every surface)

- Measurement, never certification — register verbatim on every card.
- One-signer identity gate — a non-published key never claims the production identity.
- Join on weights/evidence, not names — measured-evidence subject digest.
- Neutrality — a vendor buys data, never a score.
