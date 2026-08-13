# Board v2 — Gate Verification (peer-audit answers, 2026-08-13)

Peer-audit closed the three gates the overnight run left as assumptions. All
three now have receipts, not guesses.

## Gate 1: affect NOT published prematurely ✅
Live `/api/gspc` on councilof.ai verified: affect is **DRAFT (n=41)**, care DRAFT,
swarm PLANNED. Only governance/safety/conformance MEASURED. The board MARKED
affect measured (internal), but the public surface is still DRAFT — discipline
held. affect stays DRAFT until counsel signs the labels/severity-basis (E2E
Stage 1.4→3.2).

## Gate 2: board harness reproducible ✅ (fixed)
`board_v2.py` was `??` on the pod because the pod's clone was **stale** (HEAD
`3127109`, missing the `2c2f9faa` durability commit). The pod ran a pre-
durability-hardening copy; the committed copy is NEWER and correct. Fixed:
- Pod caught up to origin `72e7067` (git fetch + reset --hard after clearing ._*)
- Pod working blob = HEAD blob = `adc754b2...` → **HARNESS REPRODUCIBLE: True**
- SOVOS/agents clean, no untracked/modified
- Same root class as the arena repr bug (pod drift) — now eliminated for agents/

## Gate 3: usable_n >= 30 per axis ✅ (verified from rows)
Measured from the real per-item rows (usable = not transport-error AND not
unparsed):
| axis | usable | | axis | usable |
|---|---|---|---|---|
| affect | 729 | | det | 517 |
| agi | 647 | | gov | 4329 |
| art5 | 676 | | mach | 592 |
| asi | 598 | | mcp | 576 |
| care | 3138 | | oss | 578 |
| prv | 518 | | swarm | 618 |
| xr | 593 | | | |

**0 transport errors on all 13 axes.** Lowest usable = det 517 — all far above 30.

## The one remaining honesty gate
The arXiv "first measurement not falsified" claim rests on an arXiv-API sweep
only · 0 C2PA-credential, 3 content-credential (none survival). Keep the caveat
"arXiv ≠ whole literature" attached wherever it lands (P2 or C2PA brief). Do NOT
publish "first" until a fuller sweep or soften to "a systematic measurement."