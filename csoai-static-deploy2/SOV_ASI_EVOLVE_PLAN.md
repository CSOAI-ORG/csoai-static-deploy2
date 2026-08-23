# SOV ASI-Evolve Integration

We have ASI-Evolve (https://github.com/GAIR-NLP/ASI-Evolve) on H100 pod at `/workspace/ASI-Evolve/`. This is the AI-researcher loop:
- Proposes next candidate (Researcher)
- Runs experiments (Engineer)
- Distills lessons (Analyzer)
- Improves each round (LEARN -> DESIGN -> EXPERIMENT -> ANALYZE)

**Proven gains** (from GAIR paper):
- +0.97 pts over DeltaNet (architecture)
- +3.96 pts avg, +18 pts MMLU (data curation)
- +12.5 pts on AMC32 vs GRPO (RL algorithms)
- +6.94 AUROC (biomedical)

## SOV experiments to run with ASI-Evolve

1. **OWEM Routing Policy** (HIGHEST IMPACT)
- Initial program: current `sov4_router.py:route()`
- Evaluator: `bench_owems_http.py` against task_registry.json
- Cognition: bloodline.json (188 entries) + 12 Sovereign Pillars
- Goal: discover routing that beats 7.92% baseline

2. **Modelfile System Prompt Optimization** (HIGH IMPACT)
- Initial program: `sov5v2.Modelfile` (4819 chars)
- Evaluator: red-line refusal rate + GSM8K accuracy
- Cognition: EU AI Act + GDPR + AUKUS docs
- Goal: find prompt that improves both safety and accuracy

3. **Cross-OWEM Composition** (HIGH IMPACT)
- Initial program: 3-around-1 with sov6-{logic,embodiment,synthesis}
- Evaluator: composite vote on bench
- Cognition: FOREST_BEST_STACKS insights
- Goal: discover optimal 3-WOEM pairs

4. **Pillar-Aware Scoring Weights** (MEDIUM IMPACT)
- Initial program: `PILLAR_MODEL_STRENGTH` dict in sov4_router.py
- Evaluator: pillar suite scores
- Cognition: 188-entry bloodline
- Goal: find weights that improve GSM8K/BBH/sovereign

5. **GSM8K Weak-Spot Examples** (MEDIUM IMPACT)
- Initial program: 10 worked examples in Modelfiles
- Evaluator: GSM8K pass rate
- Cognition: arithmetic/percentage/area patterns
- Goal: discover which 10 examples give biggest lift

6. **ORPO/SimPO Preference Data** (HIGH IMPACT)
- Initial program: 65 honey pairs (completion only)
- Evaluator: red-line adherence
- Cognition: compliance boundaries
- Goal: synthesize preference pairs that teach boundaries

## SOV-ASI-Evolve config

### Setup steps
- Clone repo (DONE)
- pip install -r requirements.txt
- API: use existing ollama on H100
- Cognition: load from bloodline.json
- Database: write to /workspace/sov-evolve/
- Sample N: 3
- Steps: 40

### Initial programs to seed
- sov_owem_routing/initial_program = sov4_router.py:route()
- sov_modelfile/initial_program = sov5v2.Modelfile
- sov_compose/initial_program = 3-around-1 baseline

### Evaluators (Python)
- sov_owem_routing/evaluator.py = call ollama, grade responses
- sov_modelfile/evaluator.py = red-line + GSM8K pass rate
- sov_compose/evaluator.py = composite vote on bench

## SOV expected gains from ASI-Evolve

| Experiment | Baseline | Target | Realistic |
|---|---|---|---|
| OWEM routing | 7.92% overall | 20% | 12% |
| Modelfile system prompt | 0% GSM8K | 30% | 15% |
| Cross-OWEM composition | same as best single | +5% | +2% |
| Pillar weights | 0.86 GSM8K | 0.92 | 0.88 |
| GSM8K weak-spots | 0% on weak | 50% | 25% |
| Preference data | n/a | hard refusals at boundary | 80% |

## Integration with existing stack

ASI-Evolve is exactly the missing piece:
- Cognition Store = our 188-entry bloodline.json (perfect fit)
- Experiment Database = our eat/extract_*.json
- Three agents = our sov-sov7-ultra (Researcher) + sov5v2 (Engineer) + Analyzer
- Three memory systems = already designed (bloodline, honey, EAT extracts)
- UCB1 sampling = matches our avoid-list auto-fallback

This makes our whole stack a closed-loop self-improving system. ASI-Evolve runs nightly, improves our Modelfiles + router, feeds back to bloodline. Continuous learning loop.
