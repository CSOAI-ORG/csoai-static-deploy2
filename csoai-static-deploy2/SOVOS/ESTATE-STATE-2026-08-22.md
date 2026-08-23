# STATE OF THE ESTATE — what's DONE vs NOT (2026-08-22)

**Source of truth = `SOVOS/canon/SOVOS-MASTER-PART-A.md` (3,975 lines) + `PART-B.md` (1,546 lines).**
The canon IS the last 3 weeks of distilled knowledge. Anything new must point at it, not parallel it.

## 1. WHAT THE CANON ALREADY OWNS (do NOT redo)
| Topic | Canon location |
|---|---|
| Corrections ledger (already +3 → +19) | PART-A CO.1 / PART-B HA.5 |
| Crown jewels | PART-B GV.1 |
| Threats / the moat (4-direction scale) | PART-B GV.2 / HA.2 |
| AG-UI wired as agent→user wire | PART-B GW.5 |
| AIUC-1 (insurer wedge) | PART-B |
| Cross-jurisdiction crosswalk | PART-B (41 hits) |
| Watermark / Art 50 | PART-B (15 hits) |
| Signed receipts / measurement-not-certification | PART-A CO.2, inspect-receipts |
| SB 315 / EN 18286 / KI-MIG / Decree 142 | PART-A CO, PART-B |
| Front-door stack decision | PART-B GU (globe pattern) |
| Killer Axis-3↔4 (C2PA/SIGIL) | PART-A CV-11 |
| Refusal-tolerance / abstention | PART-A (C14, CV) |

## 2. GENUINELY NEW (my play-300 only — fold into canon, keep)
- **measurement-card media type** (`application/agent-measurement+json`)
- **rate-cap convention v0.1** (velocity multi-window)
- **independence ledger v1**
- **referee-capture monitor v1**

The OTHER ~26 play-300 files are reflective of the canon → mark as SYNTHESIS/point-to-canon, not new.
**Deprecate the parallel stack; fold the 4 new specs into the canon as an addendum.**

## 3. NOT-DONE — the real work (actions, not docs)
| Item | Type | Gate |
|---|---|---|
| Inject `COUNCIL_SIGN_KEY` → stranger-verifiable receipts | OWNER | NICK/POD |
| prod deploy (CA3O footer fix, 97-file `11439` re-point, P0-2 purge) | OWNER | Claude→GHA |
| Move `sov33-unified` (3.2B q4 llama) → 3090 + measure | LANE | RunPod SSH transfer |
| Rebuild `sov33-evolved` full prompt + `council-oowm` | LANE | pod-level |
| **Persistent sequential-measurement protocol** (one model per load + evict) | LANE | — (I proved it works) |
| Populate empty `gaps-*.md` every session (the root cause of redoing) | ALL | — |
| Mine the unreadable `intel/*` session logs (filesystem deadlock) | SYS | fs fix |

## 4. WHY WE KEEP REDOING (root cause)
- `intel/session-*.md` = **filesystem deadlock** ("Resource deadlock avoided") → unreadable history.
- `intel/gaps-2026-08.md` = **EMPTY** → completed/gap work isn't recorded, so agents redo it.
- Canon is authoritative but nobody cross-checks new work against it before generating.

## 5. RULE (binds, to stop duplication)
Before creating a strategy doc: `grep -liE <topic> SOVOS/canon/SOVOS-MASTER-PART-*.md`.
If it exists → **extend the canon**, don't write a new file. If genuinely new → add to canon as an
addendum. No more parallel stacks.
