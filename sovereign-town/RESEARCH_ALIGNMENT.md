# Sovereign Town — Research Alignment Matrix

This map connects the public CSOAI research vision to the files that implement
each piece in the current `sovereign-town` repository.

| Research concept | Status | Implementation |
|---|---|---|
| Governed-vs-ungoverned agent world | ✅ Live | `p0_aqua/sim.py`, `p0_aqua/town_sim_live.py` |
| 28 autonomous hives | ✅ Live | `p0_aqua/passports/`, `p0_aqua/characters.json`, `p0_aqua/hive_pack.py` |
| Ed25519-signed episodes & manifests | ✅ Live | `p0_aqua/sign_lib.py`, `p0_aqua/agent_passport.py`, `p0_aqua/verify_chain.py` |
| Real-world data moats | ✅ Live | `p0_aqua/data_moat.py`, `psc_moat.py`, `finance_moat.py`, etc. |
| BFT council vote | ✅ Live | `p0_aqua/policy_lab.py`, `p0_aqua/dashboard_server.py` `/api/council/vote` |
| Cross-terminal SOV3 bridge | ✅ Live | `p0_aqua/sov3_bridge.py`, `/api/sov3/*` |
| Policy Lab regulatory A/B | ✅ Live | `p0_aqua/policy_lab.py`, `p0_aqua/regulation_parser.py`, `experiments/` |
| Aethelgard Finance Hive contract | ✅ Live | `p0_aqua/aethelgard_finance_hive.json`, `/api/hive/aethelgard` |
| FreeLLMAPI agent chat bridge | ✅ Live | `/agent/chat` proxy in `dashboard_server.py` |
| Public static regulator views | ✅ Live | `proofof-site/sovereign-town/experiments/` |
| 47-agent real-character sim | 🔄 Planned | Research-only; current simulation runs 140 procedural agents |
| Frontier-model “Dragon Mode” arm | 🔄 Planned | Architecture reserved; not yet wired to live inference |

## Notes

- The **140-agent procedural town** is the production research engine. It
  generates signed data 24/7 and drives the Policy Lab.
- The **47-agent real-character town** is a planned product narrative aligned
  with `meok-ai/ui`. It will reuse the same policies, manifests, and verifier.
- Older `sovereign-temple*` repositories are source primitives and runtime
  experiments; `sovereign-town` is the canonical, reproducible engine.
