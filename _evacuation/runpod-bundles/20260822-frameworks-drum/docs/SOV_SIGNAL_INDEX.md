# SOV SIGNAL — and what the drum index actually is (the honest answer)
## 2026-08-22 · FRAMEWORKS DRUM · doctrine note

> **Question answered:** "this is SOV SIGNAL, code name our index?"
> **Answer:** they are TWO different indexes that compose. The drum is the
> **reference/metadata index**; SOV SIGNAL is the **measured trust gauge**. Conflating them
> is exactly the kind of overclaim the estate's measurement doctrine exists to prevent.

## 1. The two indexes (not the same object)

| | FRAMEWORKS DRUM (this pack) | SOV SIGNAL (the trust gauge) |
|---|---|---|
| What it is | The **reference / metadata index** — the universe of frameworks, charters, regulations, articles + the estate's registry, sorted and queryable | A **measured trust gauge** — Fisher-Rao distance from the permitted manifold ≡ Merton/KMV distance-to-default |
| What it measures | *What exists* (a 608-item catalogue; kind, issuer, region, binding, effective, sources) | *How far from the permitted manifold* a subject sits — a scalar/vector, the "trust gauge" |
| Kind | Categorical / descriptive | Quantitative / risk |
| Customers | Machine clients (MCP/A2A), agents, compliance ground-truth | Insurers (parametric triggers), enterprises (EU AI Act evidence), agent markets (risk oracle) |
| Output | catalog.json, cards, feeds | a distance number + EDF-equivalent empirical curve |
| Earned how | Mined + sourced (each item carries a source URL / estate path) | **Measured** (signed chain verdicts, benchmark results, held-out eval) |

**The composition (why they're related yet distinct):**
- The drum is the **schema + labels** the gauge is computed over. It tells you *what to measure*:
  the axes, the instruments, the sectors (space, xAI, Tesla), the binding/effective states.
- SOV SIGNAL is the **gauge** that measures a subject *against* that universe + the permitted
  manifold defined by the charters/frameworks in the drum.
- The NN/GNN models (0.592 MLP / 0.742 GNN, kind-classification) train ON the drum to learn
  **features** (issuer/region/knowledge-graph structure) — those features are the substrate a
  SOV SIGNAL-style gauge can consume. The models are not the gauge; they're its feature layer.

## 2. Where the drum maps into the SOV SIGNAL architecture (master doc v1.4)

```
                 FRAMEWORKS DRUM  (reference index)
                 ── catalog.json · cards · feeds · graph
                            │  (what exists, sourced)
                            ▼
   [feature layer]  NN/GNN on the graph  →  features per item / per subject
                            │  (measured, 0.742 GNN — promote-gated)
                            ▼
   GSPC 14-slot axes  +  permitted manifold (charter/framework predicates)
                            │
                            ▼
   SOV SIGNAL  =  Fisher-Rao distance from the permitted manifold   ──►  the gauge
                            │                                (≡ distance-to-default)
                            ▼
   DORADO pair-gap (East↔West regulation vs market)   ·   EAT 7-box   ·   insurance trigger
```

- **Drum → feature layer:** the graph (issuer/region edges) + the NN/GNN models produce learned
  features. **This is the piece that is genuinely ours and measurable.**
- **Feature layer → SOV SIGNAL:** the gauge needs the permitted manifold + a distance. The
  GSPC axes registry + charter/framework predicates define the manifold; the distance is the
  measurement. SOV SIGNAL is the *gauge* that produces the number (the DORADO/SOV SIGNAL docs
  in the estate already specify the mathematics).
- **The honest line:** the drum is *the index SOV SIGNAL is computed over*, not SOV SIGNAL
  itself. Claiming "the drum IS SOV SIGNAL" would be like claiming a telescope is the
  measurement of a star. The drum is the instrument's catalogue; SOV SIGNAL is the reading.

## 3. The wiring path (what makes them compose)

1. **Drum → features** (done this week): catalog graph + GNN/MLP (0.742/0.592).
2. **Drum → axes** (next): map the drum's sectors/kinds onto the GSPC 14-slot registry
   (the 14-slot axis canon) — so each measured item lands on an axis the gauge measures.
3. **Axes → manifold → gauge** ([LANE]/[GATE]): the permitted manifold = the binding charters +
   frameworks in the drum; the distance = SOV SIGNAL. This is the mature measurement layer the
   engine lanes already spec (Fisher-Rao, Merton/KMV).

## 4. Doctrine rule (binding)

- The drum's catalog is a **reference index** — it describes; it does not measure trust.
- SOV SIGNAL is a **measured gauge** — it scores; it does not catalogue.
- Any surface or doc that presents the drum as "the SOV SIGNAL index" must carry the
  distinction: the drum is the *reference index* the measured gauge is computed over.
- The GNN/MLP numbers are **model benchmarks on a catalogue-classification task**, not trust
  measurements. Presenting 0.742 as a "trust score" would be an overclaim.
