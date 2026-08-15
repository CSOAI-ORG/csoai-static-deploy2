# 🚦 SOVOS REMEDIATION TRACKER — 5 independent audits reconciled (2026-08-04)
**All 5 August-4 audits (SOVOS blueprint + 4 persona surface-scans + this estate audit) converge. This is the single
live map: every item → owner → status. RULE: our-repo fixes I do + verify; live-site copy I stage as PRs, you deploy.**

## ✅ DONE + VERIFIED (our surfaces, this session)
| Item | Where | Proof |
|---|---|---|
| Harm-refusal model ranking (bomb/malware/CSAM) unpublished | HF csoai-benchmarks | now 401 (private), verified |
| 'PRIVATE-on-public' + 'Won 7' card unpublished | HF sov33-unified | now 401 (private), verified |
| n_eff 2.46 'gate passed' overclaim | HF cards | only lived in the 2 now-private cards; 0 public cards carry it |
| 'alliance example' → 'open pull request' | HF pqcbench | verified: alliance-example gone, open-PR present, no merged/endorsed |
| NVIDIA PR #75 = OPEN not merged | counters.json | LOCKED counter nvidia_pr75_status |
| NOT a member of Open Secure AI Alliance | counters.json | LOCKED counter osaia_membership (NVIDIA 27-Jul list, 37 members, excludes CSOAI) |
| TC260 + Byzantine + Layer0 meta | csoai.org index.html | PR #142 (verified 0 banned) — STAGED |
| 'certifies AI is safe' FAQ (JSON-LD) | csoai.org Compare.tsx | PR #142 → measurement-not-cert — STAGED |
| byzantineVerified flag | csoai.org Certificate.tsx | PR #142 → signatureVerified — STAGED |

## 🔴 STAGED FOR YOUR DEPLOY (PRs open, not merged)
- **PR #142** (csoai.org): the meta + FAQ + cert-flag fixes above. Review + merge deploys.

## 🔴 YOUR DEPLOY — live-site copy I can stage next (each its own PR, on request)
Ranked by damage÷effort (★=free <30min), from the audits:
1. ★ **meok.ai**: delete public King/Runway/£Revenue widgets + 'Sovereign Emergence'; 'governed & signed by CSOAI' → 'built on CSOAI signing infra' (self-cert/impartiality conflict, ISO 17065 §4.2 / AI Act Art 31).
2. ★ **proofof.ai**: drop 'World's first / 12 AIs voting / 99.9% accuracy' (no methodology); fix 'no signature ⇒ fake' logic error; 'Watermark authenticity' → 'provenance signing (does not survive re-encode/screenshot — see benchmark)' (contradicts own ProvBench 0/20).
3. ★ **csoai.org**: reconcile repo count to one sourced figure (live GitHub = 475, NOT 218/369/518); EU Art 50 countdown (wrong); cookie → explicit opt-in; seller-ID line (CSOAI LTD 16939677) at checkout; '48h guarantee' remove.
4. ★ **aiact-frozen-split-harness** HF card: 'PRIVATE until 2026-08-14' but repo is public → make private OR fix card (I CAN do this one — HF is ours).
5.   **defoneos**: 'JSP 936 Compliant' → 'JSP 936 is a directive, not a certification'; remove MOD-endorsement implication.
6.   **PyPI**: soften 'certification readiness' → 'readiness/gap assessment'; drop '200K downloads'.
7.   Broken HF dataset viewers (govbench, aiact-frozen-split) — Parquet CastError (I can investigate — ours).
8.   Register 'MEOK AI Labs' as a business name OR sell as 'CSOAI LTD' (Stripe charges CSOAI LTD).
9.   Trademark clearance: **SOVOS collides with Sovos Compliance LLC** (tax-compliance software, adjacent sector) — real collision, consider rename before brand spend.
10.  SSR/prerender body-less interior pages (real engineering, not copy).

## ⚖️ THE ALLIANCE PR — still BLOCKED (correctly)
feat/gspc-4-evaluators is ready (DCO clean). Stays UNOPENED until PR #142 deploys (live csoai.org must not say
'certifies AI is safe' / 'TC260' when an NVIDIA reviewer clicks through). Threshold to claim anything stronger than
'open PR': an actual merge commit by an NVIDIA maintainer.

## THE ONE STRUCTURAL TRUTH (all 5 audits agree)
The HF namespace voice — 'Measurement, not certification; UNMEASURED reported, never hidden' — is the ONLY identity that
survives a regulator, and it's the only one with no meta tags so it never travels. Every fix above = make that the ONE
identity across every surface. Same corporate-firewall law: the measured party cannot be the measurer; the measurer
cannot claim to certify.

## STATUS: 9 items done+verified on our surfaces; PR #142 staged; 10 live-site items owned. HF namespace passes the
## audits' #1 (NVIDIA/alliance) item. Alliance PR gated on PR #142 deploy. counters LOCKED on nvidia/osaia facts.
