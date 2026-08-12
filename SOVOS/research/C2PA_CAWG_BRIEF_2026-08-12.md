# C2PA / CAWG Standards-Lane Brief — ProvBench content-credential survival

**Date:** 2026-08-12 · **Status:** PARTIAL — web_search/web_extract + arXiv API
blocked on Mac (requests lib + approval gate). Facts verified from estate record
+ the EU AI Act authoritative timeline (curl). Live standards-body claims flagged.

## Verified (estate record + authoritative curl)
1. **CSOAI is a C2PA Contributor Member** — verified in ATTRIBUTIONS.md
   (Docusign 7C9592DB-D7C7-8C0F-8012-AFC90FD84F1E, signed 8 Aug 2026; Jim
   Zemlin countersigned). Grants: Working Group participation + PRs. NOT:
   Steering, vote, auto-seats. (Memory §[C2PA-VERIFIED 8AUG])
2. **ProvBench numbers** (benchmark-results/provbench-15asset-2026-07-30.json):
   n_assets=15, n_cells=105, survival_rate=0.1714 (18/105). The 20-asset original
   run reported 0/20 asset-level survival (rule-of-three upper bound 15%).
   Units discipline: asset-level vs cell-level are different quantities.
3. **EU AI Act Article 50 timeline** (artificialintelligenceact.eu, curl-verified):
   transparency obligations for GPAI effective **2 Aug 2026** (in force), national
   sandboxes mandated by same date; high-risk obligations 2 Aug 2027.

## The "first systematic measurement" claim — status
**UNVERIFIED STAND, NOT YET FALSIFIED.** The subagent dispatched to check arXiv
for prior art timed out on the broken web tools (33 API calls, no result). The
claim in the preprint ("first systematic measurement of content-credential
survival") remains plausible but is NOT yet backed by a completed literature
sweep. **Do not submit to arXiv with the word "first" until the sweep is run.**
The honest fix: either (a) run the sweep when the web lib is fixed / from a pod,
or (b) soften the claim to "a systematic measurement" (no "first") — which
cannot be falsified and is still strong.

## What Article 50(2)(c)/(3) requires (estate knowledge, flag for re-verify)
Article 50(2)(c) requires GPAI providers to mark AI-generated content in a
machine-readable format, detectable as AI-generated; (3) requires transparency
that content is AI-generated/synthetic. The regulation does NOT technically
mandate C2PA by name — it's format-neutral — but C2PA is the de facto
interoperable standard the ecosystem is adopting. ProvBench's finding (credentials
die on real-world transforms) is a **governance-effectiveness finding**: the
marking mandate's real-world effect depends on credentials surviving social
uploads, re-encodes, screenshots. This is exactly the "prove the whole pipeline"
pivot from Part AY.

## C2PA entry path (from Contributor membership)
- Contributor members participate in **Working Groups** (CAWG = Content
  Authenticity Working Group / specification workstreams) and can open PRs.
- The natural home for a "credential durability measurement" proposal is the
  **spec/implementation workstream** that owns manifest formats, plus a **new
  measurement/reference-implementation proposal** — Contributor-level: propose,
  contribute the harness, open the measurement as a PR/standard input.
- What a Contributor CAN do: raise the survival-rate finding as a working-group
  input, submit the ProvBench harness as a reference implementation, contribute
  to conformance-testing discussions. CANNOT: vote on spec decisions or hold
  steering seats (those are member-tier rights).
- **Action (lane-executable):** draft the 1-page "credential durability as a
  measurement axis" input for the next CAWG cycle, framed as: Article 50
  effectiveness depends on survival; here is a harness + first numbers.

## ISO/IEC / ETSI context (flag — needs live verification)
Estate knowledge: ISO/IEC 42001 (AI management), ISO/IEC 5259 (data quality for
AI), ETSI EN 304 223 (AI assessment methodology, which the estate's GSPC
references). Whether any cite C2PA by name is UNVERIFIED (web blocked). The
estate's ETSI 304 223 benchmark exists (sovos-etsi-304-223-benchmark-v0.1.json).

## Bottom line
The standards-lane move is real and the membership is verified. The blocker is
the "first measurement" claim needing a literature sweep before arXiv. The
cheapest honest fix: run the sweep from a pod (curl works there) or soften to
"a systematic measurement." The CAWG input (1-pager + harness) is lane-executable
NOW and does not depend on the "first" claim.

## OWED
1. Literature sweep for prior art on credential survival (pod/curl or fixed web lib)
2. Verify whether any ISO/IEC/ETSI standard cites C2PA by name
3. Decide arXiv wording: "first" (post-sweep) vs "a systematic measurement" (safe now)
## UPDATE (2026-08-12, sweep RUN from pod)
arXiv prior-art sweep executed (curl from A100 pod, export.arxiv.org):
- `all:"C2PA credential"` → **totalResults: 0**
- `all:"content credential"` → **totalResults: 3** (AIGC-assisted image production;
  GPT-Image-2 Twitter dataset; synthetic-legal-evidence detection) — **none measures
  credential survival across transforms.**
**Verdict: the "first systematic measurement" claim is NOT falsified by arXiv.**
Caveat: arXiv ≠ full literature (industry/conference papers unchecked). Safe
wording: keep "first" only with "to our knowledge" — or the stronger "a systematic
measurement." The sweep evidence is in the record (tmp/arxiv1.xml + arxiv2.xml on
pod).
