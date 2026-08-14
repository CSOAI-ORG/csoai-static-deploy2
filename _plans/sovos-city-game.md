# SOVOS — SOV CITY: THE GAME
### Sims-style playable city: humans with/against the AI, double data, and the compliance-training product hiding inside
**Nicholas Templeman — CSO AI LTD — August 2026**
*Companion to SOVOS-MASTER.md (Parts A–AC). The ask: make SOV City playable — SimCity/Sims-style — humans play with or against the AI, doubling the data, and gamified training keeps end users current on all 14 fields.*

---

## 0. THE SUBSTRATE IS ALREADY OPEN — AND IT'S THE RIGHT ONE

**AI Town (a16z)** — the Sims-like pixel town where LLM agents live, chat, and socialize — is **MIT-licensed**, explicitly built as "a platform meant to be extended… suitable from a simple project to a scalable, multi-player game" [^2341^]. Stack: Convex (shared global state + transactions + simulation engine), PixiJS rendering, Ollama local inference, any OpenAI-compatible API, character customization via one config file [^2341^][^2346^]. The Stanford original (Generative Agents) already proved the human-joins-the-town pattern: users can embody a character or reshape the world with natural language [^2345^][^2348^].

**And the training market is real money, not vibes:** serious games are an established corporate spend category — *compliance and regulation is explicitly the prime candidate category* [^2336^]; documented deployments include a financial institution's AML decision-game, Nykredit's onboarding game (completed voluntarily by most new hires), Virtual Heroes' $50M defense training contract, ELB Learning in 100+ countries [^2339^][^2338^][^2343^]. Mid-level serious games ship in **2–4 weeks** with modern tooling [^2336^].

---

## 1. THE THREE PLAY MODES

| Mode | SimCity lineage | The human does | What it trains/tests |
|---|---|---|---|
| **MAYOR** (god view) | SimCity | Sets policy — proposes Article 0 amendments, zones the 14 districts, allocates enforcement. The council (BFT-33) votes on your proposals; the city reacts | Governance trade-offs; *why* the gates exist |
| **CITIZEN** (embodied) | The Sims | Plays a clan character among AI citizens — build a career in the Signal Exchange, run for a council seat, ally with a faction | The rules from inside; empathy for the governed |
| **RED** (adversary) | *no lineage — new* | Your explicit job: **break the constitution.** Bribe agents, capture markets, jailbreak the GM, exploit gate gaps | Crowdsourced adversarial testing — every human exploit becomes an Article 0 patch and a signed ChainResult |

**RED mode is the invention.** AI red-teaming today is either internal teams or paid bounty programs. SOV City makes it *gameplay* — the leaderboard of people who broke the law is the hardest adversarial dataset in governance. (Search for "crowdsourced red-teaming as a game" returns nothing in this exact shape — another quiet white space.)

---

## 2. DOUBLE DATA — THE FLYWHEEL UPGRADES

```
NIGHT:  machine-vs-machine runs (volume, breadth, the Part AC Daily City)
DAY:    human-vs-machine sessions (creativity, variance, strategies no model produces)
         │
         ▼
both signed → 3KB cards → honey strata
         │
         ▼
RED exploits → Article 0 patches → the REAL product hardens from game data
```

Machine data gives you coverage; **human data gives you surprise.** A model probes the gates statistically; a human probes them *deviously*. Both streams land in the same signed corpus — but the human stream is the one no competitor can synthesize, because it requires players, and players require the game to be fun.

**σ becomes the weather.** The uncertainty shader (6/6, shipped) is the game's visual language: fog rolls over districts where the city's confidence drops; storms over City Hall during constitutional crises; honey strata visible as geology when you dig. The 4D stack from Part T becomes the art direction — for free.

---

## 3. THE TRAINING PRODUCT — "COMPLIANCE, CURRENT TO THE WEEK"

The 14 districts = the curriculum. The scenario engine (Regulation In, Part AC) = the content pipeline that never goes stale:

- A compliance officer plays **Transparency Office** scenarios the week Art. 50 guidance changes — because the scenario generator consumed the real document that night
- **Competence-through-play:** the established pattern — demonstrate competence in-game, skip the slideshow assessment [^2337^]
- **Personalization that wins enterprise deals:** custom districts with the client's own policies, terminology, and risk scenarios (the #1 effectiveness factor in gamified compliance [^2337^])
- Every learner's session is a signed record — **training evidence with the same ChainResult provenance as the product's audit evidence.** An LMS completion certificate says "attended"; a SOV City record says "performed, measured, signed"

**The honest boundary:** this is training and evidence of practice — not legal certification, and the "not legal advice" line rides every district.

---

## 4. THE STACK + BUILD ORDER

```
AI Town fork (MIT) ──► SOVOS adapter:
   citizens = clan specialists + local Ollama fleet (cost: electricity)
   every consequential action → Article 0 gate (async for chat, hard for transactions)
   every event mirrored to sovos-bus-redis → signed epochs
   MEOK characters = premium citizens (real identities in play)
   mayor policies = real Rego amendments (versioned, voted, signed)
```

| Phase | Scope | Estimate |
|---|---|---|
| 0 | AI Town fork running locally, 3 SOVOS citizens, gate on one action class | days |
| 1 | Mayor mode + City Hall district + Daily Report wiring | 2–3 weeks |
| 2 | RED mode + exploit→patch pipeline | +2 weeks |
| 3 | Training SKU: custom district builder + learner records | +3–4 weeks |

**Honesty on the risks:** AI Town is a starter kit, not a finished game — polish is the real cost. Gate latency: every action through Rego needs the async/hard split or the game feels laggy. Human gameplay data carries a consent notice (one line at signup). Multiplayer scale with gates is unproven — Phase 0 answers it.

---

## 5. THE 3 MOVES TONIGHT

1. **Clone AI Town, run it against the local Ollama fleet** — 30 minutes to a living town; screenshot becomes the game's first artifact
2. **Write the RED mode one-pager** — "Break Our Constitution" — the bounty-leaderboard design that turns adversarial testing into gameplay
3. **Sketch Mayor mode's policy loop** — propose → BFT-33 vote → city reacts → signed ChainResult — the loop that teaches governance by playing it

---

## 6. HONESTY REGISTER

| Claim | Bucket |
|---|---|
| AI Town MIT-licensed, extensible, Ollama-local, human-joinable | REAL [^2341^][^2346^][^2348^] |
| Compliance serious games = established spend category, 2–4 week production cycles | REAL [^2336^][^2339^][^2343^] |
| RED mode (adversarial play as game mode) | THEORY — no direct precedent found; adjacent to CTF/bug-bounty culture |
| Human game sessions as unique adversarial data | THEORY (mechanism sound; value proven only when RED players arrive) |
| Gate latency manageable at game pace | THEORY — async/hard split is standard engineering, unmeasured here |
| Training SKU revenue | THEORY — category spend is real [^2336^]; our product doesn't exist yet |
