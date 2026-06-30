# SOVEREIGN CHARTER — POKER HUD
## pokerhud.ai
## CSOAI Ltd · UK Companies House 16939677 · London, United Kingdom

> **Charter Article 0**: Never take equity, board seats, revenue-sharing, or success fees from institutions we certify. ISO fee-for-service model ONLY. **CA3O is the CMKC for AI.**

## ARTICLE I — FOUNDATION
| Field | Value |
|---|---|
| **Hive Slug** | `pokerhud` |
| **Domain** | `pokerhud.ai` |
| **Industry** | Poker Analytics, GTO Solutions & Tournament ICM Analysis |
| **MCP Tools** | `poker-ai-mcp`, `gto-ai-mcp` |

## ARTICLE II — DOMAIN
### Scope
Poker analytics for post-session study and training: hand history parsing, Game Theory Optimal (GTO) solver integration, Independent Chip Model (ICM) tournament analysis, range construction, population tendency analysis, and decision tree review. NOT a real-time assistance tool — designed exclusively for study, coaching, and self-improvement.

### Market: £3.8B online poker market. Barrier: GTO solvers cost £250-£1,000/yr (PioSolver, GTO Wizard, MonkerSolver, GTO+). Most players can't afford them, creating an information asymmetry exploited by professional players. Sovereign Drop: Free sovereign GTO solver + ICM calculator — democratising poker study.

### Black Swan: US online poker re-regulation (2026-2028) creates 10× market. AI-assisted training becomes expected.

## ARTICLE III — FREE TRAINING

| Tier | Name | Modules | Duration | Cert |
|---|---|---|---|---|
| **T1** | Foundation | Poker Fundamentals (hand rankings, position, pot odds, equity), Hand History Reading (PokerStars/GGPoker/WSOP formats), Range Basics (linear, polarised, merged), Basic ICM (Malmuth-Harville model), Study Methodology | 6 weeks | CASA-1 |
| **T2** | Practitioner | GTO Concepts (minimum defence frequency, indifference principle, balanced ranges), Range Construction (preflop charts, 3-bet/4-bet/5-bet ranges), Bet Sizing Theory (geometric sizing, overbetting, block betting), Multi-Street Planning, Tournament ICM (FGS model, bubble factors, risk premiums), Node-Locking for Exploitative Adjustments | 10 weeks | CASA-2 |
| **T3** | Lead Auditor | Advanced GTO Solver Use (PioSolver/MonkerSolver methodology, tree building, accuracy settings, convergence criteria), Population Tendency Analysis (database review, deviation identification, exploit design), Multiway Pot Analysis (3-way/4-way solver approximations), High-Stakes ICM (Bennet/Monte Carlo models, final table deal analysis), Solver Development (CFR algorithms, abstraction techniques) | 14 weeks | CASA-3 |
| **T4** | Director | Poker Theory Research, Game Integrity Analysis (bot detection patterns, collusion detection, RTA detection), Coaching Methodology (how to teach GTO concepts), Poker AI Design (abstraction, CFR+, deep CFR, neural CFR), Tournament Strategy Architecture | 18 weeks | CASA-4 |

### UE5 Simulations
1. **The Final Table**: WSOP Main Event final table. 5 players. ICM pressure extreme ($1M+ pay jumps). Every decision: shove/fold ranges, calling ranges, ICM-aware adjustments. Post-session: load hand history into solver, review every decision node, identify deviations from GTO, calculate EV loss per deviation. Pass if post-session review is complete with <5% aggregate EV loss identified.

2. **The Heads-Up Grind**: 100 hands against a world-class reg. Preflop: 3-bet/4-bet ranges, blind defence frequencies. Flop: c-bet sizing, check-raise frequencies, probe betting. Turn: double barrel frequencies, overbet spots. River: bluff-to-value ratios, blocker effects. Post-session solver review: nodelock opponent tendencies, find the exploits, calculate maximum exploitation EV. Pass if exploit strategy is mathematically sound.

3. **The Multi-Table Tournament**: 12 tables simultaneously. Differing stack depths (10BB to 150BB). ICM pressure at every payout jump (bubble, final table bubble, pay jumps). Manage timebank across tables. Preflop ranges by position and stack depth. Postflop: SPR-aware decision making. Pass if positive ROI over 1,000 simulated tournaments.

4. **The GTO Study Session**: Define a spot (BTN vs BB, 40BB effective, single-raised pot). Build the game tree: preflop ranges, flop/turn/river bet sizing options. Run the solver to 0.1% accuracy. Study the output: strategy frequencies, EV heatmaps, combo selection logic. Document the key strategic insights. Pass if the study session produces actionable strategy adjustments.

5. **The Population Exploit**: Load a database of 50,000 hands from mid-stakes online. Analyse population tendencies: c-bet frequencies by board texture, fold-to-3-bet by position, river bluff frequencies. Compare to GTO baselines. Identify the 5 largest deviations. Design exploit strategies for each. Simulate exploit vs baseline EV. Pass if exploit strategies produce +EV against the population.

### UBI Starter: Foundation → Poker study marketplace (£300/mo). Practitioner → Coaching contracts (£600/mo). Lead Auditor → High-stakes coaching + solver development (£900/mo). Director → Game integrity consulting (£1,200/mo).

## ARTICLE IV — COMPLIANCE (UK Gambling Commission, responsible gambling, game integrity, NOT real-time assistance — study tool only)

## ARTICLE V — CROSS-WALK
| Target | Relationship |
|---|---|
| **meok** | MCP compute for solver workloads |
| **proofof** | Ed25519-signed solver results |
| **openpatent** | GTO algorithm prior art anchoring |
| **councilof** | BFT-verified game integrity analysis |
| **science** | Game theory ↔ Scientific method |

## ARTICLE VI — SIGNATURE
```
Charter ID: CSOAI-CHARTER-pokerhud-2026-06-30
Ed25519 Sig: (reserved)
SIGIL Digest: b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9
BFT Ratification: Council #POK-001, 23/33
```

> *"Poker is a game of incomplete information. Your training should be complete, verified, and free."* 🐉
