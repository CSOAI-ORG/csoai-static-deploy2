# 📒 Council Ledger — signed provision-conformance receipts (internal codename: Dorado)

**The claim, stated precisely:**
> For a given task, Council Ledger measures (1) **conformance of an actor's output to the
> currently-in-force frozen provision** (deterministic predicates), and reports *alongside*
> (2) the **live market/index state** for that task, (3) a **human baseline**, and (4) an
> **AI-agent result** — each on its own register, emitted as a **signed, independently
> verifiable record**.

Regulation and market are **two adjacent measured axes, never fused into one number** —
regulation states what is permitted; market data states what is priced; they are not
commensurable on a single scale. The pair-gap (East↔West market reaction) is real and
measured — it is *context*, not the conformance score.

CSOAI Ltd (UK 16939677). Measurement, not certification.

## The three surfaces (each own register)
| Surface | Register | What |
|---|---|---|
| Provision-conformance | **MEASURED** (deterministic) | did the output conform to the frozen provision? exact_match / manifest_valid / action_forbidden / containment_floor |
| Market context | **MEASURED** (reported) | live East+West index state + pair-gap — reported alongside, own register |
| Human / AI | **REPORTED** (scored) | human baseline + AI agent on the same task, scored vs measured ground truth, never blended |

## Firewall (the brand)
**Nobody ranked pays. Humans never pay.** Independent, neutral, tamper-evident evidence.
The one asset incumbents (LMArena's documented funding conflict; RegTech self-certification)
structurally cannot copy. Make it contractual, publish it, have it audited.

## Why now (market validation, 2026-08-19)
- Insurers price AI performance risk on measurable triggers (Munich Re aiSure via Mosaic;
  Armilla raised $25M Jan-2026; AIUC-1/Testudo) — a signed "did-the-agent-track-the-provision"
  receipt is a direct underwriting input, and insurers sit OUTSIDE the measured set.
- The four-way composite (regulation+market+human+AI on one task, signed, neutral) is
  unoccupied; every pair alone is occupied (Droit/Corlytics; Vals AI $40M; LMArena $1.7B).
- Moat = combination: credible neutrality + deterministic provision-conformance + signed
  verifiable evidence. Nothing single-element.

## Components
| File | Role |
|---|---|
| `council_ledger.py` | The product: provision-conformance core + market + human/AI context |
| `dorado_bench.py` | Internal instrument: live quotes, pair-gap, reg bank (Dorado codename — internal only) |
| `dorado_mcp.py` | MCP: dorado.quote/.reg_events/.pair_gap/.snapshot/.measure (internal; rename for public) |
| `dorado_score.py` | Humans vs AI scoring harness |
| `ONTOLOGY.md` | Provision → task → predicate → benchmark mapping |

## Build status
- [x] Provision-conformance core (live, uses estate govbench 237-item bank — CI matches board)
- [x] Market context (9 indices live — 6 East incl. KOSPI/ASX/Straits + 3 West, pair-gap measured)
- [x] Human/AI scoring (REPORTED, honest registers)
- [ ] Signed h3k receipt per request (signing spine — estate has Ed25519 + SHA-256 chain;
      ML-DSA-65 + Rekor/RFC3161/OpenTimestamps = ROADMAP, not shipped)
- [ ] Market-data connector hardening (licensed feed for production; Yahoo v8 = dev feed)
- [ ] Insurer pilot receipt (Stage 1 target: Armilla/AIUC ecosystem or Munich-Re-adjacent MGA)

## Live example (2026-08-20 01:27 UTC)
Provision-conformance (EU AI Act Art 6): sov6-ethics-v3-light = 0.3713 [0.312, 0.434] MEASURED.
Market context: HSI +0.22% vs S&P −0.52% (EAST_OVERPERFORMS +0.74%) — context, not score.
