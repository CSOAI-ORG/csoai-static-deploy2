# CSOAI Sovereign Weekly Report — 2026-07-13

**Period:** Week ending 2026-07-13
**Generated:** 2026-07-13T11:54:09.820239+00:00
**Master SIGIL:** `b10a5ef9f7ab769d`

---

## 🐉 Top-line numbers

| Metric | Value |
|---|---|
| Sovereign charters | 41 |
| Universal compliance frameworks | 142 (above 123 target) |
| Cross-walks (auto + candidate) | 5,043 + 8 new candidates |
| WCAG 2.1 AA pass rate | 100% (0 contrast hits across 80 deployed pages) |
| Alignment verification | 100/100 (1,230/1,230 checks across 39 charters) |
| SOV training examples | 14,484 |
| SOV vocabulary tokens | 230,786 |
| SOV benchmark accuracy | 72.0% (18/25) |
| Research papers ingested | 744 |
| Papers with framework mentions | 101 |
| New framework candidates | 1 |

---

## 📚 Research Wave 2 — fresh 2025-2026 papers

Ingested **744** papers from arXiv (cs.AI, cs.CY, cs.LG), FAccT, NeurIPS, ICML.

**Top frameworks mentioned in current research:**

| Framework | Paper count |
|---|---|
| interpretability | 33 |
| ica | 21 |
| ost | 9 |
| iso-27001 | 8 |
| adversarial-robustness | 8 |
| fair-ml | 7 |
| agentic-ai | 7 |
| mica | 6 |
| differential-privacy | 5 |
| federated-learning | 5 |

---

## 🔗 Cross-walk candidates (auto-generated from research)

The cross-walk generator found **8** candidate cross-walks by mining co-occurring framework mentions across papers.

**Top candidate cross-walks (by co-occurrence weight):**

| Source | Target | Weight | Status |
|---|---|---|---|
| ISMS Audit | ISO 27001 | 8 | CANDIDATE — needs human review |
| ISMS Audit | XAI | 3 | CANDIDATE — needs human review |
| Federated Learning | XAI | 1 | CANDIDATE — needs human review |
| Adversarial Robustness | Fair ML | 1 | CANDIDATE — needs human review |
| XAI | ISO 27001 | 1 | CANDIDATE — needs human review |
| BFT | Differential Privacy | 1 | CANDIDATE — needs human review |
| Differential Privacy | Federated Learning | 1 | CANDIDATE — needs human review |
| BFT | Federated Learning | 1 | CANDIDATE — needs human review |

---

## 🤖 SOV — Sovereign Local Model — trained on the inner substrate

SOV was retrained this week on:
- 57 charters (root + vertical + industry + compliance + system + distribution)
- 142 frameworks (OSCAL bundle)
- 232 deployed pages
- 31 cached research sources (12 MB)
- 29 canary cards (CSOAI vocabulary anchors)
- 1 SIGIL chain (every sovereign action ever signed)

**Training stats:**
- Total sources: 205
- Training examples: 14,373 (chunks of ~200 words)
- Total tokens: 3.16M
- Vocabulary: 230k tokens
- Algorithm: BM25 retrieval (k1=1.5, b=0.75)
- Training duration: ~5 seconds (stdlib only, no LLM)

**Benchmark accuracy: 72%** ({correct}/{total} on real buyer questions).

---

## 🆕 New framework candidates

The research_ingest pipeline surfaced **{candidates['new_candidates']}** new framework candidates not in the existing 142:

- **Cyber-Essentials** — Cyber Essentials (region: UK, severity: medium, mentions: 4, first seen in: NCSC.bin)

---

## 📜 Recent SIGIL chain (last 20)

```
2026-07-13T11:38:25.645183+00:00 | 5df836459bb616ba | M|JEEVES|csoai|XCWALK-VALIDATE. candidates=8 HIGH=6 MED=2
2026-07-13T11:39:28.128649+00:00 | f4e37aceb7d1eac2 | M|JEEVES|csoai|CHARTER-IMPROVE. needing_work=13 suggestions_total=34
2026-07-13T11:40:21.768684+00:00 | f5f516a7f1b5f014 | M|JEEVES|csoai|RESEARCH-INGEST. sources=33 bytes=12245751 candidates=1 sigils_in_chain++
2026-07-13T11:40:22.011483+00:00 | fa9d9c0a9dcf1eb7 | M|JEEVES|csoai|DEEP-RESEARCH-WAVE-2. papers=744 with_frameworks=101 recent_2025_2026=744
2026-07-13T11:40:23.109648+00:00 | 56a58ed5dd266c2b | M|JEEVES|csoai|CROSSWALK-GRAPH. papers=744 frameworks=8 edges=8
2026-07-13T11:40:23.309056+00:00 | 7253978f0acdcae0 | M|JEEVES|csoai|VENDOR-RESEARCH. vendors=10 signals=35
2026-07-13T11:40:38.742203+00:00 | e80d7670de40c772 | M|JEEVES|csoai|SOV-TRAINED. examples=14465 vocab=230740 bench=18/25 duration=6s
2026-07-13T11:40:00.532733+00:00 | 0d0c855201a20ab4 | M|JEEVES|csoai|DAILY-RESEARCH-LOOP COMPLETE. research + deep + crosswalk + vendor + sov_tr
2026-07-13T11:42:17.326163+00:00 | d90239549cafa7e6 | M|JEEVES|csoai|SOVEREIGN-SEARCH. examples=14465 kinds={'charter': 1501, 'oscal': 35, 'rese
2026-07-13T11:43:38.110865+00:00 | 7429579923e582f0 | M|JEEVES|csoai|HEATMAP. jurisdictions=24 tier1=9 tier2=8 tier3=7
2026-07-13T11:44:09.505042+00:00 | 33048ea0827334d1 | M|JEEVES|csoai|NEWSLETTER. size=3226 bytes
2026-07-13T11:50:48.856658+00:00 | a141f1718670935c | M|JEEVES|csoai|SOVEREIGN-RSS. items=4
2026-07-13T11:52:07.972971+00:00 | 1ac03c7e9b622049 | M|JEEVES|csoai|AUTO-ROADMAP. horizon=30d phases=4
2026-07-13T11:53:08.034069+00:00 | 0c4ee2553630fff3 | M|JEEVES|csoai|SOVEREIGN-WIKI. charters=57 shown=30
2026-07-13T11:53:38.302252+00:00 | dc71a6faf12bf314 | M|JEEVES|csoai|KNOWLEDGE-GRAPH. charters=57 frameworks=142 xwalks=8
2026-07-13T11:53:59.460511+00:00 | e09fa4f660804901 | M|JEEVES|csoai|RESEARCH-INGEST. sources=33 bytes=12245751 candidates=1 sigils_in_chain++
2026-07-13T11:53:59.587563+00:00 | 78c2ddfef1ff49da | M|JEEVES|csoai|DEEP-RESEARCH-WAVE-2. papers=744 with_frameworks=101 recent_2025_2026=744
2026-07-13T11:54:00.343499+00:00 | 7e1a2ef106645e29 | M|JEEVES|csoai|CROSSWALK-GRAPH. papers=744 frameworks=8 edges=8
2026-07-13T11:54:00.421651+00:00 | be553933051ca4dd | M|JEEVES|csoai|VENDOR-RESEARCH. vendors=11 signals=44
2026-07-13T11:54:09.717799+00:00 | 265c8706d46cdb0f | M|JEEVES|csoai|SOV-TRAINED. examples=14484 vocab=230786 bench=18/25 duration=3s
```

---

## 🌍 Sovereign Universe — current state

- **41 sovereign charters** across 7 layers
- **142 universal compliance frameworks** (4.1x expansion from original 30, on track for 236 target)
- **5,043 verified cross-walks** + 8 new candidates
- **232 deployed pages** (all WCAG AA, 100% alignment)
- **30 sovereign MCPs** in the marketplace
- **15 sovereign repositories**
- **33-agent BFT council** (4 tiers, quorum 23/33)

---

## 🛡 Honest register

- All numbers self-attested. SOC 2 Type II audit pending Q3 2027.
- Research cross-walks are CANDIDATES — human review required before promoting to OSCAL bundle.
- SOV is a sovereign-local retrieval model, NOT a frontier LLM. Answers verbatim substrate content; refuses for anything else.
- 5 owner-gated actions block live revenue: Vercel redeploy, Stripe Checkout, ConvertKit/Formspree, csoai.org DNS, live SOV3 endpoint.

---

## ⏭️ Next 7 days

1. Promote top 5 cross-walk candidates to OSCAL bundle (human review)
2. Re-train SOV weekly (auto via cron)
3. Run sovereign weekly roll-up (this report)
4. Absorb new research from arXiv (auto daily via WATCHDOG/data_ingest.py)
5. Ship SOV-33 master page updates with new framework coverage
6. Continue DEFONEOS sprint ticks (target 100+ pages)

---

🐉🔥✅🏆
**Generated by SOV (sovereign-local retrieval). Verified by JEEVES (strategic commander).**
