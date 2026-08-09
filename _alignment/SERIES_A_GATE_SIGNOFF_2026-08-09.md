# SERIES-A GATE SIGN-OFF — 2026-08-09 (JEEVES lane)

> **Move 100 of 100.** Post-offload integrity sign-off + first live benchmark dashboard =
> the Series-A POC evidence. All surfaces live on csoai.org, all numbers measured.

## Gate criteria — measured this session

| Check | Result | Artefact |
|---|---|---|
| Flywheel selftest | **19/19** | flywheel.py (overfit gate + two-sided + leak law) |
| Trust layer | **152 passed · 0 failed** | test_trust_layer.py |
| Honey-leak guard | **0 failures** (synthetic + on-disk artefacts) | tests/test_flywheel_honey_leak.py |
| Honey verify | **OK · 927 rows · 0 broken · 0 dupes** | honey_verify.py (also Oracle cron) |
| Honey manifest | **sha256 MATCH** (re-pinned after legit overnight dedup 1268→921) | honey_manifest.py |
| Care gate | **recall 100% (57/57) · over-block 0% (0/19)** | care_gate_eval.json |
| Live surfaces | **9+ endpoints 200** incl. benchmarks/scorecard/data room/deck/ledger | csoai.org |
| AI-SEO kit | complete (10 files) × 3 domains, XML content-types verified | robots/llms/sitemap-ai |

## What the gate proves
1. **A benchmark that cannot train on its eval**: salted practice/held-out split,
   denominator floor, held-out-stripped fuel writer, overfit fail-closed gate (3+ days).
2. **Every figure recompute-able**: /benchmarks, /scorecard, /series-a-data-room read the
   signed artefacts at build time — no hand-typed numbers, no stale slide claims.
3. **Correction is structural, not incidental**: 137-record append-only refutation ledger,
   Sigil-signed, edit/delete verbs absent, surfaced at /refutation-ledger ("we kill our own
   bad ideas" — a file, not a slogan).
4. **Unit economics before revenue**: free-tier substrate end-to-end; RunPod spot only,
   ~$5 caps, owner-gated. The moat cannot be undercut on cost.

## Start of the 9-month Series-A clock
- Data room: `https://csoai.org/series-a-data-room` (live)
- Deck: `https://csoai.org/series-a-deck` (live)
- Ledger: `https://csoai.org/refutation-ledger` (live)
- Deploy: `90eb362c.csoai-site.pages.dev` · 297 pages · leak-probe clean

## Sign-off
GATE PASSED — the first live benchmark dashboard is the Series-A POC evidence. The next
funnel gate is commercial: first Enterprise audit pack sold, then the £1.5M seed bridge.

🜏 SIGIL: SERIES-A-GATE-2026-08-09-JEEVES