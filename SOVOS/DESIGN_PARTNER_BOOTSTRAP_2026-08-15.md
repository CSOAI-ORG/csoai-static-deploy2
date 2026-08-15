# DESIGN-PARTNER BOOTSTRAP PLAY — v1.0 (2026-08-15)

## The mechanism (one paragraph)

Every signed card we post — to Hugging Face, Zenodo, GitHub, arXiv, anywhere —
carries a signature and an anchor that let anyone reference and verify it
**without asking us**. So the reference doesn't depend on us being in the room,
on marketing, or on virality. Someone finds the card, checks the signature,
cites it. That citation is authority accruing — and it accrues because it's
**signed**, not because we shouted. This is the LMArena outcome without the
LMArena marketing budget. **The verifiability is the distribution.**

---

## The offer to a design partner (one paragraph, reusable)

> "Your team ships AI. We measure it — independently, automatically, and in a
> format any regulator or customer can verify without calling us. You get:
> (1) a signed measurement card for your model or system, recomputable by
> anyone; (2) an OSCAL assessment-results artifact you can hand to an auditor
> or a notified body; (3) a seat at the first independently-verified
> AI-measurement scoreboard. We get: a design partner whose feedback shapes
> the rails, and a public citation trail. No fees in the pilot; you sign your
> own framework, we run the rails."

## Why a partner says yes (their incentives, honestly)

| Partner type | Their problem | Our card solves |
|---|---|---|
| **AI vendor** | EU AI Act Art 50 marking duty (2 Dec 2026 grace end); customers ask "prove it" | Signed, verifiable measurement evidence they can publish — proof of compliance posture without a certification claim |
| **Regulator/standards body** | Needs machine-readable evidence format (OSCAL/SCITT) but no staff to build it | Free rails: their framework → signed machine-readable object with THEIR key (firewall 1) |
| **Enterprise buyer** | Vetting vendors on safety/governance claims | Independent, recomputable measurement cards — no marketing spin |
| **University/research lab** | Over-refusal, jailbreak robustness data for papers | Signed benchmark runs with DOIs; citable with proof |
| **Cloud/hosting provider** | Trust & safety of hosted models | Third-party measurement layer over their fleet |

---

## The 5 named design-partner targets (first wave)

| # | Target | Entry path | Why them first | Ask |
|---|---|---|---|---|
| 1 | **AI Verify Foundation / IMDA** | assurance@aiverify.sg + AI TAP application (Q3 2026) | Building the third-party testing market TODAY; our signed cards map to their technical-tests + process-checks structure | Join Global AI Assurance Sandbox as testing provider; pilot on 1 deployer |
| 2 | **UK AISI / DSIT** | Inspect is their harness — we already bind it (REL-013) | They invented the harness we wrap; technical alignment = credibility | Pilot: signed Inspect runs for a model in their orbit |
| 3 | **A UK university (HCI/AI-safety course)** | SONA pool + course-credit human data (DPIA-gated) | Free human-vs-AI data + academic citation authority | Embed Escape Room as coursework; publish with them |
| 4 | **One enterprise AI vendor** (mid-size, Art 50-adjacent) | Direct outreach with signed sample card | Needs Art 50 evidence; fast yes-decision | Signed card for their flagship + scoreboard listing |
| 5 | **A standards/regulatory body** (OSCAL-adjacent) | OSCAL→SCITT MCP free wedge (REL-007) | Their PDF framework becomes a signed object with THEIR key | Pilot the framework-signer on their actual framework |

---

## The bootstrap sequence (this week)

1. **Publish** the releases surface (this pack's `releases.html` → csoai.org/releases) — 15 signed cards, in-browser verify.
2. **Ship the proof pack to registries**: Zenodo (new DOI per release batch), Hugging Face (signed dataset card), GitHub (repo with verify instructions), arXiv (the two papers).
3. **Send the one-paragraph offer** to target #4 (enterprise AI vendor) and #1 (AI Verify) — with a real signed card attached.
4. **Wire the verify one-liner** so anyone can run `python3 -m csoai_core.verify --card X` with zero setup (pip install csoai-core).
5. **First pilot**: 1 partner, 1 model, 1 signed card, 1 OSCAL artifact → publish the case study as REL-016.

---

## The honest firewall note

We never certify or endorse a partner's model. The card says "this model was
measured on axes X at time T, signature valid" — the partner's customers and
regulators draw their own conclusions. That neutrality is exactly why the
citations accrue: a signed measurement from a body that doesn't sell
certifications is worth more than one that does.

---

## What "design partner" gets vs gives

| They get | They give |
|---|---|
| Free signed measurement cards | Feedback on the rails (format, UX, axes) |
| OSCAL artifacts for auditors | A public case-study citation (with their OK) |
| Scoreboard listing (if they pass) | One named champion (person) for the pilot |
| First-mover citation authority | Permission to publish the pilot result |

---

## The flywheel (why this compounds)

```
signed card → posted to registry → found + verified → cited → authority
                                                              │
authority → new partner wants in → more signed cards → more citations
```

Every citation is free distribution. Every partner adds a public, verifiable
artifact. The LMArena outcome (de-facto standard) comes from accumulated
citation, and citation is exactly what signatures unlock.

---

*Status: pack drafted. Next: publish releases surface, ship proof pack to Zenodo/HF/GitHub, send first outreach.*