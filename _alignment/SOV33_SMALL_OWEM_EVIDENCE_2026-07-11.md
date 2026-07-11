# Evidence base — small specialized OWEMs + the 3-around-1 ratio (2026 web research)
_Grounds the ratio sweep. All from retrieved 2026 sources; figures are published claims, cite as such._

## Small specialized beats large general — ON ITS LANE (retrieved 2026)
- Domain-tuned SLMs beat general LLMs on domain tasks; a fine-tuned 3B can outperform a frontier model on ITS specific task, on your own hardware. (nasscom, ainewsnest 2026)
- [UNVERIFIED — RETRACTED ATTRIBUTION]: an earlier draft cited 'NIST 2024, 23-37%' and exact price bands ($0.10-0.50 vs $2-30/1M). The retrieved search PAGE TEXT was redacted from the transcript, so neither the NIST attribution nor the specific numbers are traceable to a visible source — treat as NOT verified. The DIRECTIONAL claim (domain-tuned SLMs cheaper + better on-lane) is widely reported across the retrieved 2026 blog/industry titles, but cite NO specific % or $ figure and NO government source until a real read confirms it.
- Sovereignty: <13B (Phi-3, Mistral-7B, Gemma-2) fine-tune in-house via LoRA/QLoRA, data never leaves. => the FREE/OFFLINE/local tier is only possible BECAUSE small.

## The 3-around-1 IS the 2026 standard architecture (retrieved)
- Production 2026: route ~80% predictable queries to a SMALL model, escalate ~20% complex to a frontier LLM.
  => SOV3-small handles 80% locally, SOV33cubed-large handles escalated 20%. The sketch's ratio knob = this.
- HierRouter (arXiv 2511.09873): coordinate specialized models via RL routing; MoErging survey (2408.07057).
  => our Queen->sub-hive routing is a named, active research pattern.

## HONEST LINE (binding)
- Small wins on: specialized/structured tasks, local/private, cost, latency. STRUGGLES on: open-ended multi-step reasoning.
  => that's WHY 3-around-1 exists: small OWEMs win their lane, large center catches escalations. NOT "small beats big at everything".
- Differentiator is NOT "small beats big" (2026 consensus, everyone knows) — it's GOVERNED + SOVEREIGN + specialized small OWEMs
  federated under an AUDITABLE governance kernel. That's the part nobody else ships.

## Ratio sweep design (earn-it-by-test, like MEOK's router)
Sweep (trust/reputation-ratio x online-offline-ratio x LINEAGE-DIVERSITY) across 3 small OWEMs ->
measure decision-quality + safety-leak + cost -> find Pareto-winning config. Lineage diversity is a VARIABLE
(effective-votes: 3 identical SOV3 = ~1 eff vote; 3 diverse = ~2.3). Do NOT pre-declare a winning ratio; measure it.
