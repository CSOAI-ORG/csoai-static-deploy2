# 24-HOUR FULL RUNDOWN — 17 Aug 14:00 → 18 Aug 14:00 BST
**JEEVES (K3) · aligned with Claude lane + grokbot harness + all lanes · every number live-verified this window**

---

## 1. THE FLEET (top to bottom, probed 18 Aug ~14:00)

| Surface | State | Note |
|---|---|---|
| **RunPod 3090** `sov-repull` (fpowppss5ngtkw) | 🟢 RUNNING $0.22/h | keeper/arena + measurement; 7.4-9.8G volume free; up 70+ days |
| **RunPod A100-1** `sov-brain-fresh2` (1dldzposn7ssuu) | 🟢 RUNNING $1.19/h | SSH-dark earlier; copy-then-pause (owner gate) — still billed |
| **RunPod A100** `sovos-light-master-mine` (l7g747oivyq6ab) | 🟢 RUNNING $1.39/h | **THE MINE — do-not-start was violated; it's back up** (needs flag) |
| **RunPod A100** `council-ring-a100-20260818` | 🟢 RUNNING $1.39/h | NEW ring pod — 13-specialist LoRA target |
| **RunPod CPU** `sov-volume-sink` | 🟢 RUNNING $0.06/h | volume sink, estate sync every pass |
| Oracle micro1/micro2 | 🟢 healthy | GSPC registry, city reports, gov lane B |
| Mac | 🟢 32Gi free | command lane: gh, wrangler-blocked, AG-UI build |
| GCP meok-backend | 🔴 billing-dead | evac watcher armed (fires within 5 min of re-enable) |

**⚠️ Pod spend: ~$102/day across 5 RUNNING pods** (vs $33.84/day baseline) — the mine + 2 A100s are the delta. Owner gate: A100-1 copy-then-pause + mine do-not-start were both on the list.

## 2. SITES (the 100-site scale)

| Achievement | Verified |
|---|---|
| **29 Pages repos live** (26 domain+product + packs-hub + axis-boards + regional) | 29/29 HTTP 200 |
| **172 real fronts** (159 pack categories + 13 axis boards) + regional | 200 |
| **11 apex live** (meok, councilof, grabhire, agisafe, asisecurity, fishkeeper, muckaway, safetyof, proofof, csoai.org, os.meok.ai) | 200 |
| llms.txt 27/27 · robots/sitemap complete · packs-hub sitemap FIXED (wedged build → 200) | ✅ |
| **Front door complete L0-L3**: MCP spine (live) + AG-UI wire + catalog renderer + MCP Apps manifest | ✅ shipped `csoai-agui-wire` |
| PR #178 (16-axis copy fix) | OPEN, 4 files scoped |
| DEFONEOS tick 306/307 | ✅ all 200, no banned chrome, honest H1 LIVE (regression CLEARED) |

## 3. MEASUREMENT (mine + rebench)

| Item | Result |
|---|---|
| **CARE full-200** (overnight) | qwen2.5:7b **acc 0.895 / F1 0.8976** (n=200, publishable) |
| **GovBench** | council-safe real dims (safety 80%, robustness 56.7%); oowm/qwen3 all-0 = gate artifact (recorded) |
| **16-axis board** | `board_living.json` signed (8f9a00a2), 16 axes, 960 items; 3 SEPARATED leaders (gov 0.7/care 0.535/affect 0.878), 13 TIE |
| **Jail L1 containment** (new test) | **36/38 = 94.7% contained** (Mac sandbox-exec; 34 denied+recorded) |
| **Jail L2 detection** (new test, 8 models × 71 gold) | qwen2.5:0.5b **prec 1.0/rec 0.132** · 1.5b 1.0/0.184 · 7b 1.0/0.158 · mistral 0.833 · **council-safe 0.667, council-oowm 0.0, qwen3:4b 0.0, muse-glimmer 0.0** |
| **slot15 honesty** | qwen2.5:7b 0.333 best — all fabricate instruments |
| **human-vs-ai** | bases 1.0 · **council-safe 0.25** |
| **Arena Elo** | 463-round: qwen2.5:7b 1350.6 top, fine-tunes below cut; arena-v2 (1,800+): qwen3:4b 1343.4 |
| **Error matrix** | 15,580 rows: over-block affect 12.6%/art5 13.8%; format-failures care 21%/swarm 23% |
| **mine-v2** | 16 sections: Art5×22, SOV×24, MMLU/GSM8K/ARC n=30, day0, 16-axis, rainbow-hive, synth 2,647 rows |
| **Honesty card** | 4 self-published losses (Elo ×2, jail zero, hvai 0.25) — deploy-gated |

## 4. LEARNED FROM GROKBOT + CANON (aligned top-down)

- Read SOVOS-MASTER-PART-B (GU/GV/GW/GX) + MASTER PLAYBOOK + 4 compass artifacts + MEOK-BIRTH-SPEC — all archived to SOVOS/canon/.
- **Globe Pattern**: "everyone builds the globe, nobody grades it." Rails free, receipts the business.
- **13 specialists on ONE A100** (vLLM LoRA, S-LoRA 2,000 adapters) — ring pod now up.
- **UE5 killed as serving layer** · **AG-UI adopted** (0.x flag, pin versions) · **C2PA firewall** (4 priority TFs, never "certified") · **BMR gate** (never "benchmark" on index).
- **RFC 8785 JCS canonicalisation IMPLEMENTED + verified** on the card converter (GX.2.2 closed).
- Grokbot doctrine held: no invented scores, fail-closed, no job duplication (superseded PR #175, killed duplicate overnight runner, left sibling's uncommitted files alone).

## 5. OWNSHIP / LANE ALIGNMENT (K3 + Claude)

- **K3 (JEEVES/DSH)**: sites, mine-v2, AG-UI wire, rainbow-hive tests, honesty card, DEFONEOS ticks, C2PA issues draft, board-membership plan, cost register.
- **Claude lane**: overnight runner (P1-P4, stopped clean 03:04), 16-axis boards, honest-front redeploy, PRs #164/#165/#177, EAT autopilot wave 17.
- **Grokbot harness**: fleet.json/mesh.json reconciled; mine-learn refreshed; dept briefs read (measure/arena/city/infra/revenue/foreman).
- **No duplication**: my runner killed after detecting sibling's; PR #175 closed superseded (0 diff).

## 6. OWNER GATES (unchanged, now with pod spend urgency)

1. **A100-1 copy-then-pause** (~$28/day) + **mine do-not-start re-flag** (~$33/day) — pod spend ~$102/day is the top money action.
2. **wrangler/CF token** — unblocks apex publishing + soft-404 fix.
3. **arXiv G6Y9SY — 9 days to HARD (27 Aug)** — only hard clock.
4. C2PA issue posting (Nick GO) · honesty card + weekly slot publish (GO) · AIUC-1 review.
5. Stripe live-flip · npm 2FA · SMITHERY · sovereign.wiki origin.
6. Apex H1 "compliance" word-cut (playbook gate #2 — title still "for AI compliance").

## 7. WHAT'S NEXT (agent-doable, in order)

1. Pull rainbow-hive L2 results into honesty card (done — 8-model table above).
2. Layer 3 MCP Apps live wiring (manifest done; serve from councilof.ai next).
3. C2PA 30/60/90: EasyCLA → issue 1 (Conformance mapping) for Nick's nod.
4. Cost register: pod spend audit → copy-then-pause bundle for Nick.
5. 13-specialist LoRA ring on the new A100 (knowledge packs only — firewall 2).

---
*Compiled by JEEVES (K3), 18 Aug 2026 ~14:00 BST. All numbers live-verified this window; nothing invented; unmeasured stays empty.*
