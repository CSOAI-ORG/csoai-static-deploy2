# THE CATAPULT — MASTER DOC (Session consolidation, 2026-08-14)

**Thesis:** We are the neutral, cryptographically-verifiable measurement layer the
regulated AI economy consumes. Regulators regulate. We measure. Fix-loop/NGOs fix.
We sign. The signal aggregates. Everyone else proves *who* an agent is — we prove
*whether it behaves as claimed*. That behaviour-attestation slot is empty, and ours.

## PART 1 — PROVEN TONIGHT (the two blocking gaps, closed)

1. ✅ External verifier LIVE — Cloudflare Worker verifies Ed25519 cards with no
   secret. JS canonicalization proven byte-identical to Python.
   `https://csoai-attest-verify.nicholastempleman.workers.dev` — "verify without
   trusting us" is a live URL.
2. ✅ Signing-issuance leg wired — real card through MeasureService → MinIO →
   content_id recomputed off-box and matched. Bucket: 3 objects.
3. ✅ Correctness gate — GROUNDED / UNGROUNDED / UNKNOWN; ungrounded can't sign.
   Enforced at the emit choke point (measure_api self_test 6/6).
4. ✅ GSPC-as-A2A-skill — routes through real Ed25519 MeasureService; issues a
   *measurement credential*, never a certificate (refused the "issue_certificate"
   firewall breach).
5. ✅ BFT council rejected a promotion and corrected its own f=1-with-3-voters
   error (needs 4). Doctrine working.
6. ✅ attestation_registry.py fixed the silent signal bug (council_signal was
   averaging via `except: pass`). Now real ConstituentScores from GSPC, crosswalk,
   bridges, cards → SOV signal. 6/6.
7. ✅ Master verify pod-side: 7/7 wires PASS, exit 0 (A100).

## PART 2 — LOCKED ARCHITECTURE DECISIONS

8. **Layer protocol, NOT mono-repo.** Neutral spine stays clean; every vertical
   consumes it across a firewall.
9. **Three J-Spaces** (each ~3KB into SOV space):
   - J-Space 1 = Adoption (Anthropic/OpenAI/Google economic indices)
   - J-Space 2 = Capability/Governance-policy (OECD.AI, Stanford HAI)
   - J-Space 3 = Behaviour (our GSPC)
10. **Connect indices as READ sources — never absorb and re-sign as ours.** We sign
    the *binding*: "these models, this adoption context, this governance score,
    drift-free as of this date." The signal of all signals = the signed relationship.
11. **SOV signal = signed measurement across ALL labs**, not soft signal for one.
    Anthropic built the adoption layer; consume it, don't rebuild it.
12. **SOV space / UE5 = PROOF SURFACE** (visual), NOT a security boundary. Shop
    window, never "secure" render.

## PART 3 — CONNECT (open-source, don't rebuild)

13. did:web identity root (Ed25519 + ML-DSA-65 keys) — closes signer-identity gap.
14. SCITT / DataTrails receipt per card — tamper-evident issuance. (Flag: SCRAPI
    draft, DataTrails Preview.)
15. Upgrade ai-bom-mcp → CycloneDX ML-BOM 1.7 + SPDX 3.0 AI Profile.
16. Upgrade meok-watermark-attest-mcp → C2PA 2.x before the marking cliff.
17. Adopt OpenSSF Model Signing; wire garak + PyRIT into the injection scanner.
18. Replace "OTS Bitcoin" overclaim with RFC-3161 / OpenTimestamps (DONE in-lane —
    timestamping.py, calendar_commit state, btc_anchored never claimed unverified).

## PART 4 — SYNTHESIZE (existing assets, ranked)

19. #1 **Regulation-drift-triggered re-attestation** — corpus-watch drift →
    crosswalk re-map → flag stale cards. LIVING COMPLIANCE. Built (drift_
    re_attestation.py, 18/18).
20. AI-BOM + signed measurement bundle ("provenance + behaviour") for high-risk AI.
21. Measured governance score as insurance-underwriting INPUT (feed, not policy).
22. Self-instrumentation: engine emits SIGNED telemetry about its own operation
    (cards issued, axes run, drift) — NOT self-awareness claims.

## PART 5 — THE THREE DIAMONDS (buyers with deadlines)

23. **Diamond 3 — AI liability insurance underwriting. SHORTEST LINE TO MONEY.**
    Munich Re aiSure, Armilla+Lloyd's, AIUC-1 (score→premium). They already pay.
24. **Diamond 1 — Post-quantum migration attestation. LIVE URGENCY.** ML-DSA-65
    (FIPS 204); NIST deprecates RSA/ECC post-2030. Signed equivalence attestation.
25. **Diamond 2 — EU AI Act high-risk. ⚠️ DATE FLAG.** Estate brief says high-risk
    obligations **2 Aug 2027**; catapult draft says **2 Dec 2027** (Digital
    Omnibus Reg 2026/1744). BOTH confirm 2027 (longer runway — don't lead).
    Exact day UNVERIFIED (web tools down 2026-08-14) — verify before quoting.
    Article 50 marking: 2 Aug / 2 Dec 2026 (near-term cliff — watermark plays).
26. **Bonus — A2A signed-agent-card slot** (150+ orgs, Linux Foundation, v1.0).
    Fill before anyone else.

## PART 6 — OWNER-GATED (only Nick)

27. Rotate leaked npm token (confirmed live).
28. Resolve `affect` — reverted to DRAFT/UNMEASURED (confirmed lane flip). Stays
    until ~Sep 11 + your one word.
29. arXiv 7946050 two ticks — EXPIRES AUG 27 (only hard clock). Fix affiliation typo.
30. Signer trust-root membership (CA / C2PA list) — owner + cost gate.
31. Counsel: ICO £40; "Council of AI" TM £170; FTO; severity-basis sign-off ~Sep 11.
32. UK AI Growth Lab GO/NO-GO before Sep 27 — only live UK gov window.
33. Squat bare npm `csoai` (404); claim Kaggle `/csoai` (404); delist 7–11 sov-*
    HF models.
34. k3 / jv-wave8 force-rewind verdict — restore or deliberate?

## PART 7 — FIREWALL (non-negotiable)

35. Never "certify"/"compliant"/"board-grade"/notified body/legal advice/market
    prediction. Measured ≠ certified. Feed the notified body; never impersonate.
36. CobolBridge stays dark and firewalled — mine the 49GB moat, never merge its
    client/certify/Stripe code. Verify migrations, never do them.
37. Never say "index" publicly until IOSCO/UK-BMR legally scoped.
38. Drop soft-signal MARKET prediction from the brand entirely.
39. Sandboxes = measurement instrument (taken-escape), NOT hosting security
    boundary. Private key lives ONLY on the A100. "Monitored containment, not
    provable isolation."

## PART 8 — THE THROUGH-LINE

Distance to money was never more building. Tonight closed the two gaps that
mattered. What's left to first invoice: **publish the 19/19 over-refusal anchor,
resolve affect with one word, point Diamond 3 at an underwriter.**

Status legend: ✅ done · 🟡 built/live · 🔴 owner-gated · ⚠️ flag
