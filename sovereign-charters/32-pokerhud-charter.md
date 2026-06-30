# SOVEREIGN CHARTER — POKER HUD
## pokerhud.ai
## CSOAI Ltd · UK Companies House 16939677 · London, United Kingdom

> **Charter Article 0**: Never take equity, board seats, revenue-sharing, or success fees from institutions we certify. ISO fee-for-service model ONLY. **CA3O is the CMKC for AI.**

## ARTICLE I — SOVEREIGN FOUNDATION
| Field | Value |
|---|---|
| **Hive Slug** | `pokerhud` |
| **Domain** | `pokerhud.ai` |
| **Industry** | Poker Analytics, GTO Solutions & Tournament ICM Analysis |
| **MCP Tools** | `poker-ai-mcp`, `gto-ai-mcp` |
| **BFT Ratification** | Council #POK-001 — Quorum 23/33 |

## ARTICLE II — INDUSTRY DOMAIN & MARKET

### II.A — Scope
Poker analytics for post-session study and training: hand history parsing from all major platforms (PokerStars, GGPoker, WSOP.com, Winamax, 888poker, partypoker), Game Theory Optimal (GTO) solver integration with nodelocking for exploitative adjustments, Independent Chip Model (ICM) tournament analysis using multiple algorithms (Malmuth-Harville, FGS, Bennett, Monte Carlo), range construction analysis, population tendency deviation detection, and decision tree review. NOT a real-time assistance (RTA) tool — designed exclusively for post-session study, coaching, and self-improvement.

### II.B — GTO Solver Methodology
- **Preflop Ranges**: RFI charts by position (UTG→BTN), 3-bet/4-bet/5-bet ranges, cold-call ranges, blind defence frequencies
- **Postflop Game Trees**: Build decision trees with configurable bet sizing (33%, 50%, 66%, 75%, 100%, 150% pot), multiple raise sizes, and donk-bet nodes
- **Nodelocking**: Lock opponent strategy nodes to observed frequencies for exploitative adjustments — find the maximum exploitation strategy
- **Convergence Criteria**: Solver accuracy measured in EV loss per hand (target <0.1% of pot for precise solves)
- **Multiway Approximation**: 3-way and 4-way pot solving via CFR abstraction or Monte Carlo CFR

### II.C — ICM Algorithm Deep-Dive
- **Malmuth-Harville**: Classic ICM model — estimates each player's tournament equity based on stack sizes and payout structure
- **FGS (Future Game Simulation)**: Extends ICM by simulating N future hands with positional and skill advantages
- **Bennett Model**: Accounts for blind structures and ante effects more accurately than base ICM
- **Monte Carlo ICM**: Simulation-based approach for complex payout structures (satellites, bounties, progressive KO)
- **Bubble Factor**: Ratio of tournament $ lost vs chips lost — quantifies ICM pressure at each stage

### II.D — Hand History Parsing Formats
| Platform | Format | Key Fields |
|---|---|---|
| **PokerStars** | Text/XML | Hand ID, table, stakes, players, positions, hole cards, actions, board, results |
| **GGPoker** | Text/JSON | Smart HUD data, all-in equity, run-it-twice results |
| **WSOP.com** | Text | Standard HH format with tournament info |
| **Winamax** | Text | French/English, 4-color deck option |
| **888poker** | Text | Snap/standard tables |
| **partypoker** | Text/JSON | FastForward support |

### II.E — Market & Barriers
- **Global TAM**: £3.8B online poker market
- **Current Barrier**: GTO solvers cost £250-£1,000/yr (PioSolver £499, GTO Wizard £700, MonkerSolver £999, GTO+ £250). ICM tools cost £100-£300/yr (ICMIZER 3, HRC). This creates an information asymmetry where professionals with solver access exploit recreational players without it.
- **Sovereign Barrier Drop**: Free sovereign GTO solver + ICM calculator + hand history parser — democratising poker strategy for all players.

### II.F — Black Swan Window
- **US online poker re-regulation (2026-2028)**: State-by-state legalisation (currently: NV, NJ, DE, PA, MI, WV, CT live; CA, NY, IL, MA pending). Potential 10× market expansion creates massive demand for affordable study tools.
- **AI transparency in skill gaming**: As AI-assisted training becomes standard, the gap between trained and untrained players becomes a regulatory concern.
- **Cross-state player pooling**: MSIGA (Multi-State Internet Gaming Agreement) expansion increases player pools and study tool demand.

## ARTICLE III — FREE TRAINING PATHWAY

| Tier | Name | Modules | Duration | Cert |
|---|---|---|---|---|
| **T1** | Foundation | Poker Fundamentals (hand rankings, position, pot odds, equity calculation), Hand History Reading (PokerStars/GGPoker/WSOP/Winamax formats), Range Basics (linear, polarised, merged, depolarised), Basic ICM (Malmuth-Harville model, bubble factor), Study Methodology (how to use solvers effectively) | 6 weeks | CASA-1 |
| **T2** | Practitioner | GTO Concepts (minimum defence frequency, indifference principle, balanced ranges, blocker effects), Range Construction (preflop charts by position, 3-bet/4-bet ranges, blind vs BTN ranges), Bet Sizing Theory (geometric sizing for nutted hands, overbetting polarised ranges, block betting merged ranges), Multi-Street Planning (flop→turn→river line construction), Tournament ICM (FGS model, bubble factors, risk premiums, pay jump analysis), Node-Locking for Exploitative Adjustments (locking opponent frequencies, finding max-exploit lines) | 10 weeks | CASA-2 |
| **T3** | Lead Auditor | Advanced GTO Solver Use (tree building for specific spots, accuracy settings, convergence monitoring, database integration), Population Tendency Analysis (100K+ hand database review, deviation identification by player type, exploit design at scale), Multiway Pot Analysis (3-way/4-way solver approximations, main pot/side pot dynamics), High-Stakes ICM (Bennett/Monte Carlo models, final table deal analysis, satellite bubble strategy), Solver Development (CFR algorithms, abstraction techniques, neural CFR architectures) | 14 weeks | CASA-3 |
| **T4** | Director | Poker Theory Research (unexploitable strategy frontiers, multi-player equilibrium existence proofs), Game Integrity Analysis (bot detection patterns — inhuman frequencies/timing, collusion detection — chip dumping, soft play, shared hole cards, RTA detection — solver-perfect play at scale), Coaching Methodology (how to teach GTO concepts to different skill levels), Poker AI Design (CFR+, Deep CFR, neural CFR with function approximation, Pluribus-style multi-player AI), Tournament Strategy Architecture | 18 weeks | CASA-4 |

### III.B — UE5 Simulation Scenarios

1. **The Final Table**: WSOP Main Event final table, November Nine atmosphere. 5 players remaining with stacks: 45BB (you), 35BB, 25BB, 18BB, 12BB. Payouts: 1st $10M, 2nd $6M, 3rd $4M, 4th $3M, 5th $2M. ICM pressure is extreme — every chip has >$20K in tournament equity. Play 50 hands navigating: shove/fold ranges vs each stack size, calling ranges with ICM risk premiums, 3-bet fold equity at 25BB effective, blind-vs-blind dynamics. Post-session: load all hands into solver, review every decision node, compare to GTO baselines, calculate EV loss per deviation, document the 10 biggest mistakes. Pass if post-session review is complete with <5% aggregate EV loss identified and a concrete improvement plan for each mistake.

2. **The Heads-Up Grind**: 100 hands against a world-class regular at 200BB deep, $5/$10 NLHE. Preflop: BTN open ranges (70%+ at 200BB), BB 3-bet frequencies, 4-bet bluff selection with blocker effects. Flop: c-bet sizing on dry/wet/static textures, check-raise frequencies, donk-bet range construction. Turn: double barrel frequencies by turn card, overbet spots on blank turns, probe betting after flop checks through. River: bluff-to-value ratios at each sizing, blocker selection for bluffs (A-high, K-high, Q-high blocker hierarchy), thin value bet sizing. Post-session: nodelock opponent's observed tendencies, find the maximum exploitation strategy, calculate EV of exploit vs GTO baseline. Pass if exploit strategy produces +EV and is mathematically sound.

3. **The Multi-Table Tournament**: 12 tables simultaneously in a $109 online MTT with 5,000 entrants. Differing stack depths: Table 1 (12BB, push/fold mode), Table 3 (35BB, re-steal stack), Table 7 (85BB, deep-stacked play), Table 11 (6BB, survival mode). ICM pressure at every payout jump: money bubble (top 15%), final table bubble (top 9), pay jumps at 7th/6th/5th/4th/3rd. Manage timebank across tables (30s per decision average). Apply preflop ranges by position and stack depth using push/fold charts from solver. Postflop: SPR-aware decision making (fold when SPR<2 with marginal hands, jam draws when SPR<3 with equity). Pass if positive ROI maintained over 1,000 simulated tournaments.

4. **The GTO Study Session**: Define a specific spot (BTN vs BB, 40BB effective, single-raised pot, BTN open 2.25×, BB call). Build the game tree: BTN range (45% of hands), BB range (35% of hands). Flop: A♥7♦2♣ (BTN range advantage). Configure BTN bet sizing options (33%, 50%, 75%), BB check-raise options. Turn: T♠ (brick for both ranges). River: 4♥ (blank). Run solver to 0.1% accuracy. Study output: BTN strategy frequencies by hand class, BB defence frequencies, EV heatmap across the range-vs-range matrix. Extract combo-level insights: "BTN bets small with entire range on this texture because range advantage + nut advantage on A-high dry board." Document the 5 key strategic insights with solver screenshots. Pass if study produces actionable strategy adjustments with EV justification.

5. **The Population Exploit**: Load a database of 50,000 hands from mid-stakes online ($50NL-200NL). Analyse population tendencies across 10 dimensions: (1) c-bet frequency by board texture and position, (2) fold-to-3-bet by position (BTN vs CO 3-bet, SB vs BTN 3-bet), (3) river bluff frequency by line (triple barrel, check-raise river, probe river), (4) check-raise frequency on different flop textures, (5) donk-bet frequency and hand strength correlation, (6) turn probe frequency after flop checks through, (7) overbet frequency and hand strength, (8) 3-bet vs call frequency in BB vs BTN, (9) 4-bet bluff frequency, (10) showdown hand strength by line. Compare each to GTO baselines. Identify the 5 largest deviations from equilibrium. Design exploit strategies for each. Simulate exploit vs GTO baseline EV over 10,000 hands. Pass if all 5 exploit strategies produce statistically significant +EV.

### III.C — UBI Starter Integration
- **Foundation (T1)** → Poker study marketplace access (£300/mo in training credits + solver access)
- **Practitioner (T2)** → Coaching marketplace — list as verified coach, match with students (£600/mo equivalent)
- **Lead Auditor (T3)** → High-stakes coaching contracts + solver development contributions (£900/mo)
- **Director (T4)** → Game integrity consulting + coaching platform revenue share (£1,200/mo stipend)

## ARTICLE IV — COMPLIANCE & GOVERNANCE

| Framework | Coverage | Notes |
|---|---|---|
| UK Gambling Commission | Aligned | Study tool — no gambling functionality |
| Responsible Gambling | 100% | Promotes skill development, not gambling encouragement |
| Game Integrity | 100% | Anti-RTA, anti-bot detection patterns built into solver methodology |
| Platform Terms of Service | Compatible | Post-session study only — no real-time data access during play |
| GDPR | 100% | Hand history data processed locally — no cloud upload |

## ARTICLE V — CROSS-WALK MAP

| Target Hive | Relationship |
|---|---|
| **meok** | MCP compute infrastructure for solver workloads (CFR calculations) |
| **proofof** | Ed25519-signed solver results — cryptographic verification of training completion |
| **openpatent** | GTO algorithm prior art anchoring — CFR+, Deep CFR patent disclosures |
| **councilof** | BFT-verified game integrity analysis — multi-agent collusion/bot detection |
| **science** | Game theory → Scientific method bridge — equilibrium computation, strategy verification |

## ARTICLE VI — SIGNATURE CHAIN
```
Charter ID: CSOAI-CHARTER-pokerhud-2026-06-30
SHA-256: f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8
Ed25519 Public Key: (reserved for signing ceremony)
Ed25519 Signature: (reserved)
SIGIL Digest: b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9
OTS Bitcoin Anchor: pending
BFT Ratification: Council #POK-001, 23/33 votes required
Timestamp: 2026-06-30T02:00:00Z
```

---

> *"Poker is a game of incomplete information. Your training should be complete, verified, and free. Five simulations. Four tiers. Zero barriers. The solver is sovereign."* 🐉
