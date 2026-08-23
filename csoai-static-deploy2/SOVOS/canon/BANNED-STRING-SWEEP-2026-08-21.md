# BANNED-STRING PRE-AUDIT — OCCURRENCE INVENTORY (step 008)

Date: 2026-08-21 · lane: DSH/JEEVES (measurement only, NO prod deploys) · handoff to LANE for P0-2 purge.

Scope: deployable HTML surface in `csoai-static-deploy2` (root `*.html` + `_site/*.html`, 652 files),
noise excluded (training_data / forest / benchmark-results / .backups). Tool = harness ripgrep (authoritative).

## 1. Correction triggers (#51–#56) — CLEAN in public HTML
| String | Files | Verdict |
|---|---|---|
| "Meta declined" | 0 | clean |
| "unlaunched" | 0 | clean |
| "95,000" | 0 | clean |
| "SB 315" | 0 | clean |
| "OpenHands-CLI" | 0 | clean |
| "MirrorCode" | 0 | clean |
| "draft era" | 0 | clean |

The stale "Meta declined" lives only in the frozen canon `SOVOS/canon/SOVOS-MASTER-PART-A.md`
(L3301 C6) — superseded by `CORRECTIONS-51-56-2026-08-21.md`, not on the public surface.

## 2. Killed-claim hits — VIOLATIONS (hand to LANE)
| String | Files | Evidence |
|---|---|---|
| "33 live" / "33-agent" / "BFT as fact" | 2 + ~20 | `defoneos-cnic-pillar-2-proposal.html:218` "Nick's 33-agent BFT council is at 12/33 live" (+ `_site/` copy); 20 defoneos-* pages carry "33-voter/33-agent" as present-tense fact |
| "CA3O is the CMMC for AI — independent third-party accreditation" | ~10 core marketing pages | `finance.html:51`, `government.html:51`, `launch.html:68`, `vote.html:165`, `energy.html:51`, `education.html:51`, `healthcare.html:51`, `press-release.html:15,42`, `launch-kit.html:108`, `bft-configurator.html:164` (+ `_site/` copies) |

The recurring quote also carries "institutions we **certify**" + "**ISO** fee-for-service model ONLY" —
three banned-grammar violations in one reusable footer block. This is the single highest-value purge target:
a shared quote component, not 10 independent edits.

## 3. Honest negations — KEEP (NOT violations)
- **UKAS (14 hits / 7 files):** "DEFONEOS-SEAL not yet UKAS-accredited", "we don't have UKAS accreditation yet",
  "pursuing accreditation by Q4 2026" — correct honest disclosure, keep.
- **accreditation (108 hits):** predominantly "accreditation pending", "no completed accreditation claimed",
  "not a replacement for … primary accreditation", and the `defoneos-mod-delivery-accreditation` document title.
  Correct, keep. (Reconcile only the CA3O quote block above.)

## 4. Grammar check
- "13 measured of 14" — not in local HTML; lives on the live board `GET councilof.ai/api/gspc`. Do not contradict.
- "measurement, not certification" — not found verbatim in local HTML (case/comma variants). Confirm the
  required negation phrase is present on the live home surface as part of P0-2.

## Handoff
P0-2 purge = LANE (deploy-gated: branch → PR → Claude merges → GHA). Recommended first commit:
replace the shared "CA3O is the CMMC for AI … accreditation … certify … ISO fee-for-service" footer block
with the canonical grammar: "verified measurement credential — measurement, not certification."
Sweep log archived here; not deployed.
