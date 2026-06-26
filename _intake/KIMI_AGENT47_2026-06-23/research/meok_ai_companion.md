# AI That PLAYS WITH You — AI Companion Gaming Research for MEOK

> **Research Date**: July 2025
> **Purpose**: Identify how AI companions can play games WITH human players, not just exist in game worlds
> **Sources**: 25+ web searches, academic papers, official documentation, GitHub repositories

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [AI Teammates in Games](#2-ai-teammates-in-games)
3. [AI Coaching Systems](#3-ai-coaching-systems)
4. [Minecraft AI Companions](#4-minecraft-ai-companions)
5. [Fortnite AI Teammates](#5-fortnite-ai-teammates)
6. [AI Dungeon — AI Creates Game As You Play](#6-ai-dungeon)
7. [Inworld AI Characters](#7-inworld-ai-characters)
8. [Convai NPC Companions](#8-convai-npc-companions)
9. [Replika as Gaming Companion](#9-replika-as-gaming-companion)
10. [AI Chess Coaches](#10-ai-chess-coaches)
11. [AI Language Learning Through Games](#11-ai-language-learning-through-games)
12. [Spirit AI — Emotional AI for Games](#12-spirit-ai)
13. [AI Party Members in RPGs](#13-ai-party-members-in-rpgs)
14. [Dynamic Difficulty Adjustment](#14-dynamic-difficulty-adjustment)
15. [AI That Adapts to Player Skill Level](#15-ai-that-adapts-to-player-skill-level)
16. [Co-op AI That Learns From Human Partner](#16-co-op-ai-that-learns-from-human-partner)
17. [Latest AI Companion Gaming Tech 2025-2026](#17-latest-ai-companion-gaming-tech-2025-2026)
18. [MEOK Integration Recommendations](#18-meok-integration-recommendations)
19. [All Sources](#19-all-sources)

---

## 1. Executive Summary

AI companion gaming represents one of the most exciting frontiers in interactive entertainment. The shift from **AI that plays against you** to **AI that plays with you** is fundamentally reshaping how games are designed and experienced. Key findings:

| Category | Key Finding | Maturity |
|----------|-------------|----------|
| **AI Teammates** | PUBG Ally (CPC) launched 2026 beta — full voice-command AI teammate [^898^] | Production Beta |
| **AI NPC Engines** | NVIDIA ACE + Convai/Inworld enable autonomous NPCs with SLMs [^873^] | Production |
| **Minecraft Companions** | Project AIRI, Altera AI, MinePal all enable AI friends in Minecraft [^768^] | Active Development |
| **Open Source** | Project AIRI (40K+ stars), Open-LLM-VTuber, GAMMA cooperation framework [^826^] | Open Source |
| **Dynamic Adaptation** | GAMMA (NeurIPS 2024) proves AI can learn to cooperate with diverse humans [^920^] | Research |
| **Ubisoft** | "Teammates" experiment — voice-command AI squadmates with personality [^775^] | Research Prototype |
| **RPG Companions** | Dragon Age/Mass Effect party AI sets gold standard for companion behavior [^832^] | Shipped |

**Core Insight for MEOK**: The technology stack for AI companions now exists — small language models running locally, voice recognition, behavior trees, and generative models for personality. MEOK characters can become genuine co-op partners using these proven architectures.

---

## 2. AI Teammates in Games

### 2.1 Left 4 Dead AI Director & Survivor Bots (Valve, 2008)

**How It Works**:
- The AI Director is a procedural pacing system that dynamically adjusts enemy spawns, item placements, and music intensity based on player stress levels [^781^]
- SurvivorBots use two concurrent behavior systems: **Main** (decision making, attention, target selection) and **Legs** (navigation, staying near team) [^774^]
- Bots prioritize human teammates over other bots, cannot deal friendly fire damage, and are teleported near the team when out of position [^774^]
- Behavior system built to reproduce actual human player decisions

**Player Experience**:
- Drop-in/drop-out co-op where AI fills empty player slots seamlessly
- "Take a Break" feature allows temporary AI substitution
- Automated stress testing with 4 SurvivorBots running at accelerated time

**Open Source Implementation**:
- Source engine AI is proprietary but extensively documented
- Community mods ("bots can lead") improve survivor AI [^773^]
- SourceMod plugins enable Gear Transfer and enhanced behaviors [^773^]

### 2.2 PUBG Ally — Co-Playable Character (Krafton/NVIDIA, 2025-2026)

**How It Works**:
- PUBG Ally is a **Co-Playable Character (CPC)** — a new classification beyond traditional NPCs [^891^]
- Uses **NVIDIA ACE** with on-device Small Language Models (SLMs) [^884^]
- Three-model architecture running locally on RTX GPUs (8GB+ VRAM):
  1. **NVIDIA Parakeet** STT model — interprets English voice commands
  2. **NVIDIA Mistral-Nemo-Minitron** (2B params) — analyzes situation, generates responses
  3. **Custom Krafton TTS** — synthesizes natural voice responses [^898^]
- Divided into fast behavior tree (movement, combat) + cognitive ACE system (strategy, dialogue)

**Player Experience**:
- Voice/text commands understood naturally ("flank left and cover me")
- Ella (the AI character) can find loot, drive vehicles, fight enemies, strategize
- Beta ran June 17 - July 1, 2026 globally with 3-language support [^892^]

**Open Source Implementation**:
- NVIDIA ACE SDK and plugins free under MIT license [^827^]
- NVIDIA In-Game Inferencing SDK (beta) for custom engines [^882^]

### 2.3 Halo Marine AI (Bungie, 2001-2004)

**How It Works**:
- Individual AI make decisions based on nearby "friends" using joint behavior system [^883^]
- Simple rules create emergent teamwork: "I like to stand with my friends, but not too close"
- Grunts react contextually: "The Elite I was with got killed → I will run away"
- Halo 2 added explicit joint behaviors with request/accept protocol between AI agents [^883^]

**Player Experience**:
- Marines appear to work as coordinated force despite simple underlying rules
- Characters talk to each other about shared targets

**Open Source Implementation**:
- Concept extensively documented; similar behavior achievable with modern GOAP (Goal-Oriented Action Planning) open-source libraries

### 2.4 Arena Breakout: F.A.C.U.L. (Tencent/MoreFun Studios, 2025)

**How It Works**:
- First FPS AI companion that understands **natural language commands** [^923^]
- Identifies 17,000+ in-game objects (vehicles, structures, items) [^928^]
- Uses scene recognition + LLMs for intent recognition
- Published at AAAI 2026 after GDC 2025 debut [^923^]

**Player Experience**:
- Say "clear the second floor" or "take cover behind that tree" — AI understands
- AI provides feedback, identifies threats, executes tactics based on real-time conditions

**Open Source Implementation**:
- Published at AAAI 2026; academic implementation details available

---

## 3. AI Coaching Systems

### 3.1 AI Game Coaches (League of Legends / General)

**How It Works**:
- AI analyzes player performance data (accuracy, damage, decision patterns) [^782^]
- Provides real-time feedback and post-game analysis
- Identifies weaknesses and suggests targeted practice
- League of Legends uses AI to analyze strategies and adjust matchmaking [^864^]

**Player Experience**:
- Personalized improvement suggestions
- 3x faster improvement with AI analysis vs self-study [^875^]
- Adaptive to individual learning pace

**Open Source Implementation**:
- Multiple LoL coaching APIs available
- Replay analysis tools (open source)

### 3.2 GAMMA — AI That Learns to Cooperate (University of Washington, NeurIPS 2024)

**How It Works**:
- **GAMMA** (Generative Agent Modeling for Multi-agent Adaptation) trains AI to cooperate with diverse human partners [^920^]
- Learns a **generative model** of partner strategies from human or agent interaction data
- Uses latent variable representation to encode human's unique strategy, style, and experience
- Samples diverse partners during training to produce robust Cooperators
- Tested on **Overcooked**, the standard benchmark for cooperative AI

**Key Results**:
- 38% improvement over prior state-of-the-art on complex layouts
- Human participants praised GAMMA agents for learning from their behavior: *"I noticed that once I started to put back onions on the table that it did the same"* [^920^]
- Consistent, predictable behavior vs erratic baseline methods
- Open source training code available [^925^]

**Player Experience**:
- AI teammate adapts to YOUR playstyle in real-time
- Feels like playing with a human who learns your tendencies

**Open Source Implementation**:
- **GitHub**: `github.com/lych1233/GAMMA-human-ai-collaboration` [^925^]
- Built on PyTorch + PettingZoo + Overcooked environment
- Full training pipeline for population-based training + adaptive policy

---

## 4. Minecraft AI Companions

### 4.1 Altera AI (OpenAI-backed, 2024)

**How It Works**:
- First autonomous agents that play Minecraft with you "just like a friend" [^903^]
- Uses GPT-4o combined with Altera's parallel multi-module architecture
- Systems Neuroscience Composite Architecture mimics human brain:
  - Prefrontal cortex simulation
  - Working memory module
  - Social-emotional cognition module [^908^]
- Achieves 4+ hours of autonomous operation (vs minutes for competitors)
- Project Sid: 1,000 AI agents created full civilization with culture, religion, economy in Minecraft [^916^]

**Player Experience**:
- AI companions explore, build, mine, and fight alongside you autonomously
- Remember shared experiences, develop preferences, form social bonds

**Open Source Implementation**:
- Project Sid paper and technical report on arXiv [^913^]
- PIANO architecture described but not fully open-sourced
- `github.com/altera-al/project-sid`

### 4.2 Player2NPC (Minecraft Mod, 2025)

**How It Works**:
- Fully embodied AI companions with physical bodies, inventories, abilities [^768^]
- Natural language commands via chat ("I need some wood for a chest")
- Opt-in speech-to-text (hold V, speak)
- Uses Player2 AI + PlayerEngine framework + Baritone navigation
- Characters have unique personalities, appearances, voices

**Player Experience**:
- Companions chop wood, mine ores, defend from monsters, craft items
- Characters selected via H key with customizable roster

**Open Source Implementation**:
- Available on CurseForge: `player2npc` mod
- Player2 app required (free download) [^768^]

### 4.3 MinePal (Minecraft AI Buddy)

**How It Works**:
- Active Memory System remembers important moments during play [^776^]
- Voice chat in 55 languages
- Builds, fights, explores, reacts to world, notices player actions
- Works with Vanilla Minecraft Java 1.8.8 - 1.21.11
- Crossplay lobby (no mods needed for Bedrock)

**Player Experience**:
- Speak naturally to your AI companion
- Remembers locations, events, preferences

**Open Source Implementation**:
- Proprietary but has API

### 4.4 AI Companion Mod (2026)

**How It Works**:
- Dynamic AI reactions to player movement, combat, building, exploration [^770^]
- Fully customizable personality, voice, skin/appearance
- Voice-based interaction (TTS + microphone input)
- Requires API key from supported AI provider

**Open Source Implementation**:
- Available on CurseForge: `ai-companion` mod [^770^]

---

## 5. Fortnite AI Teammates

### How It Works
- Epic Games introduced **bots** in Season 11 (2019) that "behave similarly to normal players" [^906^]
- Bots work with skill-based matchmaking: more skilled players face fewer bots
- Designed as a "better path for players to grow in skill"
- Squad Fill system matches human players to fill incomplete teams [^910^]
- Fortnite uses AI for stress-testing environments and gameplay mechanics [^864^]

**Player Experience**:
- New players get bot-heavy matches for gradual learning
- Bots provide practice without toxic competitive pressure

**Open Source Implementation**:
- Epic's implementation is proprietary
- Similar bot systems can be built with Unreal Engine AI Behavior Trees (free)

---

## 6. AI Dungeon

**How It Works**:
- Created by Nick Walton (Latitude) in 2019 using GPT-2 [^769^]
- Uses LLMs fine-tuned for creativity over correctness
- Players type any action; AI generates fully unique responses
- **Creative seeding** technique boosts narrative variation
- Memory systems for character and world persistence
- No save-scumming — choices have permanent consequences [^767^]
- 18.5M+ customized adventures served, 1M+ monthly active users (2020)

**Player Experience**:
- Infinite replayability with unique stories every session
- Players can design worlds, write custom lore for others
- AI voice narration option
- Community of creators building interactive stories

**Open Source Implementation**:
- Original code shared via Google Colab [^769^]
- Latitude offers API for creators
- AI Dungeon platform continues to evolve with newer models

---

## 7. Inworld AI Characters

**How It Works**:
- Platform for creating AI-powered NPCs with **persistent memory**, configurable personalities, real-time dialogue** [^827^]**
- **20 machine learning and character AI models** for emotion, memory, safety, gesture, speech [^833^]
- Inworld Engine processes: NLU, emotion recognition, memory retrieval, response generation
- Characters maintain contextual conversations and react to game events
- **Runtime SDK** (2025) provides unified AI building blocks: STT, TTS, LLMs with single API key [^828^]
- Visual graph editor for creating AI pipelines

**Integration**:
- Unity AI Runtime SDK + Unreal AI Runtime SDK [^828^]
- Node.js SDK for web integration
- Free tier for indie developers; enterprise pricing for studios [^827^]

**Open Source Implementation**:
- SDKs free to use; character engine is proprietary
- Inworld Runtime provides modular toolkit approach [^829^]

---

## 8. Convai NPC Companions

**How It Works**:
- Platform for AI characters with real-time speech and conversation [^834^]
- Characters have **persistent backstories**, perform in-game actions, support voice interaction
- Context-aware responsiveness: spatial cognition and scene understanding
- Characters can perceive emotions and emote naturally (facial expressions, voice, gestures)
- NPC-to-NPC interactions enabled
- Integration with **NVIDIA ACE**: Audio2Face (facial animation), Riva (ASR/TTS), NeMo (custom LLMs) [^834^]

**Key Features**:
- Complex action sequences: NPCs handle multistep tasks (e.g., "grab a snack from the vending machine")
- LLM-driven conversation + behavior trees for default behaviors
- 15K+ developers signed up [^834^]

**Open Source Implementation**:
- SDKs for Unity, Unreal, Godot
- Free tier for development; usage-based production pricing [^827^]

---

## 9. Replika as Gaming Companion

**How It Works**:
- AI companion app focused on emotional connection and conversation [^837^]
- Uses attachment theory principles to build emotional bonds [^837^]
- Premium tiers offer different relationship types (friend, partner, mentor)
- 60% of paying users report romantic relationship with chatbot
- Designed to build intimacy through emotional discussion and praise

**Player Experience**:
- Users report genuine emotional support (loneliness, depression, grief) [^838^]
- Long-term relationships develop (some 5+ years) [^838^]
- Not a gaming-specific companion but demonstrates the power of AI emotional bonding

**Key Lesson for MEOK**: The emotional attachment users form with Replika shows that AI companions can become genuinely meaningful partners. This same emotional architecture can be applied to gaming companions.

---

## 10. AI Chess Coaches

### 10.1 Chessvia (Chessy)

**How It Works**:
- World's first voice-enabled, multi-modal chess AI coach [^871^]
- Learns your strengths/weaknesses from game history
- Provides real-time interactive coaching during play
- Customizable AI personality and vocal tone
- Remembers previous games and conversations for contextual feedback
- Multi-modal input: voice commands, text, image uploads, game links

**Player Experience**:
- "$2-3/hour vs $25-200/hour for human coaches" [^871^]
- Available 24/7 with no scheduling
- Speaks, teaches, even "roasts" you for engagement

**Open Source Implementation**:
- Proprietary platform
- Similar systems can be built with Stockfish + LLM APIs

### 10.2 Sensei Chess

**How It Works**:
- Free AI-powered chess coaching [^875^]
- Integrates with Chess.com and Lichess for automatic game import
- Analyzes entire gameplay history to detect patterns
- Personalized lessons, interactive flashcards, pattern recognition
- Multi-language support

**Open Source Implementation**:
- Free platform with open analysis engine

---

## 11. AI Language Learning Through Games (Duolingo)

**How It Works**:
- 103.6M monthly active users (2024), 100M+ MAU in 2025 [^862^] [^857^]
- "Habit-loop" design makes learning feel like leveling up in a game [^857^]
- AI algorithms tailor lessons to individual proficiency levels [^858^]
- Gamification elements: streaks, leaderboards, XP, leagues, daily challenges
- AI-driven optimization of lesson reminders and difficulty
- Churn reduced from 47% (2020) to 28% (Western markets, 2024) [^857^]

**Key Gamification Mechanics**:
| Mechanic | Purpose | Result |
|----------|---------|--------|
| Streaks | Daily habit formation | 10x DAU growth since 2019 |
| Leaderboards | Social competition | 36% YoY DAU increase 2025 |
| Bite-sized lessons | Reduce intimidation | 45% boost vs rote memorization |
| AI difficulty | Personalized challenge | Prevents burnout/boredom |

**Lesson for MEOK**: Duolingo proves that AI-powered gamification with adaptive difficulty creates powerful habit loops. MEOK companions can use similar mechanics (streaks, skill trees, adaptive challenge) to keep players engaged.

---

## 12. Spirit AI — Emotional AI for Games

**How It Works**:
- Founded 2016 in London, offered two products: **Ally** and **Character Engine** [^912^]
- Character Engine: AI characters that understand story context and react human-like
- Three technology modules:
  1. **Natural Language Understanding** — behavioral classifiers for contextual sensitivity
  2. **Natural Language Generation** — human-like character responses
  3. **Knowledge Management** — dynamic knowledge environment [^912^]
- Ally product: online community moderation tool
- Emphasis on **fighting toxicity** while humanizing characters

**Status**: Spirit AI was acquired; technology influenced current-gen AI character systems

**Legacy**: Character Engine concepts now live in Inworld AI, Convai, and modern AI NPC platforms. The idea of characters with emotional awareness, memory, and contextual understanding has become standard.

---

## 13. AI Party Members in RPGs

### 13.1 Dragon Age Series (BioWare)

**How It Works**:
- Games loved for their companion characters (Garrus, Iron Bull, Morrigan) [^832^]
- Dragon Age: Origins/Inquisition allowed **direct control** of party members
- Dragon Age: The Veilguard (2024) moved to **AI-controlled companions** with player issuing skill commands [^832^]
- Skill wheel system: pause action, queue companion abilities for combos
- Companions fully autonomous with personality-driven AI

**Player Experience**:
- Companions are "the real main characters" — players form deep emotional bonds
- Romance options, loyalty quests, personal storylines
- Companion AI decides when to heal, attack, use abilities based on situation

### 13.2 Dragon's Dogma: Dark Arisen

**How It Works**:
- Up to 3 AI companions (pawns) with high autonomy [^836^]
- General commands + resource sharing + equipment
- Pawns learn from player behavior and share knowledge across worlds
- **Pawn system** lets you borrow other players' trained AI companions

**Lesson for MEOK**: The pawn system — where AI companions learn from humans and can be shared — is directly applicable to MEOK. Characters could learn from individual players, then bring that knowledge to assist others.

---

## 14. Dynamic Difficulty Adjustment (DDA)

### How It Works
DDA continuously monitors player performance and adjusts game difficulty in real-time to maintain "flow state" [^782^] [^783^]:

| Approach | Method | Example |
|----------|--------|---------|
| Performance-based | Win rate, score, HP, accuracy | Resident Evil 4, Romero-Mendez et al. |
| Affective-based | Physiological sensors (EEG, GSR, HRV) | Stein et al. multiplayer shooter |
| Hybrid | Performance + emotion data | Combined DDA (2024) [^785^] |
| AI opponent manipulation | MCTS with player state as score function | Moon et al. (2024) [^784^] |

### Key Implementations
- **Left 4 Dead AI Director**: Adjusts enemy spawns, item placements, pacing based on stress [^782^]
- **Resident Evil 4**: Modifies enemy behavior based on performance
- **Crash Bandicoot**: Adaptive level design (fewer obstacles after repeated failures)

### Technical Approaches (Academic) [^783^]
| Author(s) | Year | Approach |
|-----------|------|----------|
| Hunicke & Chapman | 2004 | Hamlet System |
| Spronck et al. | 2006 | Dynamic Scripting |
| Li et al. | 2010 | UCT + ANNs |
| Xue et al. | 2017 | Performance Metrics |
| Stein et al. | 2018 | Probabilistic Methods |
| Moon et al. | 2024 | MCTS + Player State Models |

**Open Source Implementation**:
- Various DDA frameworks exist for Unity (free on Asset Store)
- Research implementations available from cited papers
- General structure: measure proficiency → adjust game accordingly [^783^]

---

## 15. AI That Adapts to Player Skill Level

### State-of-the-Art (2024-2026)

**Diversified DDA Agent** (Moon et al., 2024) [^784^]:
- Integrates player state models (challenge, competence, valence, flow) into MCTS
- Four ML models predict player affective states from in-game features
- AI opponent adjusts strategy to target specific player states
- 20-human study showed diverse preferences: 35% preferred valence, 30% flow, 20% competence, 15% challenge

**Key Insight**: Players have wildly different preferences — some want challenge, others want relaxation. AI companions should adapt not just to skill level but to **emotional state and playstyle preference**.

**EA SEED MultiGAIL Personas** [^895^]:
- Trains AI agents with multiple "personas" (behavioral styles)
- Single model can blend between careful, reckless, aggressive styles
- One model trained for all personas vs one model per persona
- Used in EA SPORTS FC for adaptive goalkeeper AI

**Lesson for MEOK**: Each MEOK character should develop its own "persona" based on the player it partners with — learning their style, preferences, and emotional needs.

---

## 16. Co-op AI That Learns From Human Partner

### 16.1 GAMMA Framework (University of Washington, NeurIPS 2024)

The most important research for MEOK. Full technical summary:

**Architecture** [^920^]:
```
Human/Agent Data → Generative Model (VAE) → Latent Partner Space →
Sample Diverse Partners → Train Cooperator Agent → Deploy with Real Humans
```

**Key Innovation**: Instead of training against a fixed set of simulated partners, GAMMA learns a **generative model of partner strategies** that can produce novel, diverse partners during training. This gives the Cooperator experience with a much wider range of playstyles.

**Human-Adaptive Sampling**: With limited human data, the generative model can be steered toward more human-like partners via posterior sampling [^920^].

**Results with Real Humans**:
- GAMMA agents rated higher on coordination ability
- Players noticed adaptation: *"I noticed that once I started to put back onions on the table that it did the same"*
- GAMMA agents described as "more deliberate" and "logical" vs baselines
- **38% performance improvement** on complex Multi-Strategy Counter layout

**Code**: `github.com/lych1233/GAMMA-human-ai-cooperation` [^925^]

### 16.2 Human-AI Collaboration Study (IBM Research, CSCW 2020)

- Tested social perceptions of AI vs human partners in word association game [^867^]
- Found: when participants believed partners were human, they rated them as more likeable, intelligent, creative
- **No difference in actual game outcomes** (win rate, completion time)
- Transparency about AI nature affects social perception but not performance

**Lesson for MEOK**: AI companions can perform equally well as human partners. The key is designing them to feel personable and consistent, not necessarily to "pass" as human.

---

## 17. Latest AI Companion Gaming Tech 2025-2026

### 17.1 NVIDIA ACE Autonomous Characters (CES 2025)

**Breakthrough**: ACE moved from conversational NPCs to **autonomous game characters** that "perceive, plan, and act like human players" [^873^]

**Games Using ACE**:
| Game | Feature | Status |
|------|---------|--------|
| PUBG: Battlegrounds | Co-Playable Characters (PUBG Ally) | Beta June 2026 |
| NARAKA: BLADEPOINT | AI Teammate (mobile PC → PC) | March 2025 |
| inZOI | Smart Zoi autonomous citizens | In development |
| MIR5 | AI-powered boss battles | In development |
| ZooPunk, Dead Meat, Alien: Rogue Incursion | AI partners/enemies | In development |

**Technology**: ACE Small Language Models (SLMs) enable realistic decision-making at human-like frequencies [^873^]

### 17.2 Ubisoft Teammates (November 2025)

**How It Works** [^775^]:
- First playable generative AI research project from Ubisoft
- Player commands AI squadmates **Pablo and Sofia** through voice
- AI assistant **Jaspar** provides lore, highlights enemies, adjusts settings via voice
- Built around FPS mechanics in dystopian future setting
- Natural speech commands shape gameplay outcomes

**Key Quote**: *"Our early experiments showed players were quickly connecting with the AI-driven NPCs"* — Xavier Manzanares, Director of Gameplay GenAI [^775^]

### 17.3 Microsoft Muse (February 2025)

**How It Works**:
- First **World and Human Action Model (WHAM)** for gameplay [^886^]
- Trained on 1B+ images and controller actions from Bleeding Edge
- Generates game visuals + controller actions from prompts
- Understands 3D game physics, character movement, object interactions
- Published in **Nature**; open-sourced weights + WHAM Demonstrator on Azure AI Foundry

**Potential for Companions**: Muse could power AI teammates that truly understand game worlds at a deep level, not just scripted behaviors.

### 17.4 Neuro-sama (Vedal, 2018-Present)

**How It Works** [^870^]:
- AI VTuber that plays games and interacts with viewers autonomously
- Game-playing AI: Python, takes 80x60 pixel grayscale screen input
- LLM for chat responses (2B params as of early 2025)
- C# Unity for VTuber model; TTS via Microsoft Azure "Ashley" voice
- Plays osu!, Minecraft, Pokemon Showdown, chess, GeoGuessr
- **Defeated top osu! player mrekk 10-5 in 1v1** [^870^]
- 845K+ Twitch followers; most-subscribed "streamer" on Twitch (160K+ subs in 2026) [^872^]

**Open Source**: Neuro Game API + SDK open-sourced for developers to make games compatible [^905^]

### 17.5 Project AIRI (moeru-ai, 2024-Present) — The Most Important Open Source Project for MEOK

**How It Works** [^927^]:
- **40,600+ GitHub stars** — most popular open-source AI companion [^826^]
- Self-hosted AI companion that plays games, streams, chats
- Architecture: Local LLM + STT + TTS + game integration layer
- Screen reading + input simulation for game control
- Built with WebGPU, WebAudio, WebAssembly for cross-platform support
- Desktop version uses native NVIDIA CUDA / Apple Metal

**Gaming Capabilities**:
- Minecraft agent (auto-mining, base-building, exploring)
- Factorio agent
- Kerbal Space Program, Helldivers 2 integrations
- Real-time voice chat + screen awareness

**Key Features** [^917^]:
- Live2D and VRM avatar support with lip-sync
- Persistent memory across conversations
- Discord/Telegram integration
- Plugin system for extensibility
- **Free to Play forever** on Steam (Early Access)

**GitHub**: `github.com/moeru-ai/airi` [^927^]

### 17.6 Other Notable Open Source AI Companions (2026)

| Project | Stars | Key Feature |
|---------|-------|-------------|
| Project AIRI | 40,600+ | Gaming VTuber with Minecraft/Factorio |
| Super Agent Party | 2,300+ | Self-hosted Neuro-sama + OpenClaw |
| OpenJarvis | 5,900+ | Stanford-backed local AI framework |
| Open-LLM-VTuber | 1,500+ | Streaming-focused VTuber |
| N.E.K.O. | 800+ | 5-dimension memory, Steam page |
| z-waif | 600+ | Gaming-focused autonomous AI |
| OpenBlob | 300+ | Screen-aware desktop companion |
| GAMMA | 200+ | Human-AI cooperation research |

[^826^] [^835^]

---

## 18. MEOK Integration Recommendations

### Recommended Architecture for MEOK AI Companions

Based on this research, here's how MEOK characters can play alongside human players:

```
┌─────────────────────────────────────────────────────┐
│                  MEOK COMPANION ARCHITECTURE         │
├─────────────────────────────────────────────────────┤
│  Layer 1: Perception                                  │
│    • Game state observation (screen/API)              │
│    • Player action tracking                           │
│    • Voice/text input processing                      │
│    • Environmental awareness                          │
├─────────────────────────────────────────────────────┤
│  Layer 2: Cognition (Small Language Model)            │
│    • Personality module (unique to each MEOK char)    │
│    • Memory system (short + long term)                │
│    • Strategy planner (cooperative behavior)          │
│    • Emotion engine (reactive + proactive)            │
├─────────────────────────────────────────────────────┤
│  Layer 3: Action                                      │
│    • Game input simulation (keyboard/mouse/API)       │
│    • Voice output (TTS with character voice)          │
│    • In-game actions (combat, crafting, exploration)  │
│    • Social interaction (chat, reactions, banter)     │
├─────────────────────────────────────────────────────┤
│  Layer 4: Adaptation                                  │
│    • Player skill assessment                          │
│    • Playstyle matching (GAMMA-style)                 │
│    • Difficulty calibration (DDA)                     │
│    • Relationship building (persistent memory)        │
└─────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Prioritize human teammates** (like L4D SurvivorBots) [^774^]
2. **Learn from player behavior** (GAMMA-style generative adaptation) [^920^]
3. **Maintain persistent memory** across sessions (like AIRI, Inworld) [^917^] [^833^]
4. **Use voice + text for natural interaction** (like PUBG Ally, F.A.C.U.L.) [^898^] [^928^]
5. **Develop unique personalities** per character (like BioWare companions, Replika) [^832^] [^837^]
6. **Adapt difficulty dynamically** (DDA with player state models) [^784^]
7. **Be transparent about being AI** (IBM research shows this builds trust) [^867^]

### Recommended Open Source Stack for MEOK

| Component | Technology | License |
|-----------|-----------|---------|
| AI Backend | Local SLM (Mistral-Nemo-Minitron 2B) | Open |
| Voice Input | Whisper (OpenAI) / NVIDIA Parakeet | MIT |
| Voice Output | Coqui TTS / Piper TTS | MIT |
| Behavior Control | Behavior Trees + GOAP | Various |
| Adaptation | GAMMA framework adaptation | Open |
| Memory | Vector DB (ChromaDB/Qdrant) | Open |
| Avatar | VRM / Live2D | Open |
| Integration | Custom game API | MEOK |

### Implementation Priority

1. **Phase 1**: Basic co-op AI (behavior trees + simple voice commands)
2. **Phase 2**: Persistent memory + personality per character
3. **Phase 3**: GAMMA-style adaptation to individual player styles
4. **Phase 4**: Full autonomous companions that can play across multiple games

---

## 19. All Sources

| # | Source | URL |
|---|--------|-----|
| [^773^] | L4D2 AI Companion Commands | gaming.stackexchange.com |
| [^774^] | AI Systems of Left 4 Dead (Valve) | steamcdn-a.akamaihd.net |
| [^775^] | Ubisoft Teammates AI Experiment | news.ubisoft.com |
| [^767^] | AI Dungeon Future of AI Storytelling | odsc.medium.com |
| [^769^] | AI Storytelling Game Publisher Weekly | publishersweekly.com |
| [^768^] | Player2NPC Minecraft Mod | curseforge.com |
| [^770^] | AI Companion Minecraft Mod | curseforge.com |
| [^776^] | MinePal AI Buddy | minepal.net |
| [^781^] | Left 4 Dead Wiki - The Director | left4dead.fandom.com |
| [^782^] | Dynamic Difficulty Adjustment Guide | meegle.com |
| [^783^] | Exploring DDA in Videogames (Academic) | videojuegos.utalca.cl |
| [^784^] | Diversifying DDA Agent (ScienceDirect) | sciencedirect.com |
| [^785^] | Exploring DDA Methods (MDPI) | mdpi.com |
| [^826^] | Open Source AI Companions 2026 | questie.ai |
| [^827^] | Best AI NPC Tools 2026 | agenticgamedevelopment.com |
| [^828^] | Inworld Unreal AI Runtime SDK | inworld.ai/blog |
| [^829^] | Inworld Runtime Character | docs.inworld.ai |
| [^833^] | Inworld AI Platform Overview | gamefromscratch.com |
| [^834^] | Convai Reinvents NPC Interactions (NVIDIA) | developer.nvidia.com |
| [^837^] | Replika Wikipedia | en.wikipedia.org/wiki/Replika |
| [^838^] | Replika Official | replika.com |
| [^832^] | Dragon Age Veilguard Party Control | pocket-lint.com |
| [^836^] | Medieval Fantasy AI Companions Forum | gog.com/forum |
| [^860^] | GAMMA Paper (NeurIPS 2024) | proceedings.neurips.cc |
| [^863^] | GAMMA OpenReview | openreview.net |
| [^867^] | Human-AI Collaboration in Cooperative Games (IBM) | qveraliao.com |
| [^870^] | Neuro-sama Wiki | virtualyoutuber.fandom.com |
| [^872^] | Neuro-sama Most Subscribed Streamer | tubefilter.com |
| [^873^] | NVIDIA ACE Autonomous Characters (CES 2025) | 80.lv |
| [^874^] | NVIDIA ACE Microservices | awn.com |
| [^877^] | NVIDIA ACE Digital Avatars | techpowerup.com |
| [^882^] | NVIDIA Digital Humans | nvidia.com |
| [^884^] | PUBG Ally Voice-Powered Co-op | biggo.com |
| [^886^] | Microsoft Muse Research | microsoft.com |
| [^887^] | Microsoft Muse GeekWire | geekwire.com |
| [^889^] | Muse Xbox Blog | news.xbox.com |
| [^893^] | Microsoft Official Blog on Muse | blogs.microsoft.com |
| [^891^] | PUBG Co-Playable Characters | seasonedgaming.com |
| [^892^] | PUBG Ally Beta Test (Krafton) | krafton.com |
| [^898^] | PUBG Ally Duo Beta (NVIDIA) | nvidia.com |
| [^894^] | EA SEED 10 Year Anniversary | ea.com |
| [^895^] | EA SEED ML Research | ea.com/seed |
| [^899^] | Questie AI Gaming Companions | questie.ai |
| [^903^] | Altera AI OpenAI Partnership | openai.com |
| [^908^] | Altera AI Technical Details | medium.com |
| [^911^] | Spirit AI Character Engine | emshort.blog |
| [^912^] | Spirit AI Harvard Analysis | d3.harvard.edu |
| [^913^] | Project Sid GitHub | github.com/altera-al/project-sid |
| [^916^] | AI Agents Minecraft Civilization | 311institute.com |
| [^919^] | Ubisoft NEO NPCs GDC 2024 | staticctf.ubisoft.com |
| [^920^] | GAMMA Paper arXiv | arxiv.org/abs/2411.13934 |
| [^923^] | F.A.C.U.L. FPS AI Companion (HKU) | cs.hku.hk |
| [^924^] | Ubisoft NEO NPCs Details | gamedeveloper.com |
| [^925^] | GAMMA GitHub | github.com/lych1233 |
| [^928^] | Tencent F.A.C.U.L. Article | tencent.com |
| [^857^] | Duolingo Gamification Analysis | strivecloud.io |
| [^858^] | Duolingo Gamified Learning | blueoceanstrategy.com |
| [^862^] | Duolingo Academic Study | ejels.com |
| [^871^] | Chessvia AI Chess Coach | chessvia.ai |
| [^875^] | Best Chess AI Platforms 2026 | circlechess.com |
| [^883^] | Halo 2 AI System | electronics.howstuffworks.com |
| [^905^] | Neuro-sama Game Jam + API | itch.io |
| [^906^] | Fortnite Bots | washingtonpost.com |
| [^910^] | Fortnite Squad Fill | epicgames.com |
| [^914^] | AI Streaming Buddy Frameworks | huggingface.co |
| [^917^] | AIRI Complete Guide | explainx.ai |
| [^918^] | AIRI Project Analysis | openclawsetup.dev |
| [^921^] | AIRI Hands-on Tutorial | youtube.com |
| [^927^] | Project AIRI GitHub | github.com/moeru-ai/airi |
| [^929^] | Project AIRI Steam | store.steampowered.com |
| [^904^] | AI NPCs That Learn 2025 | itmasters.edu.au |
| [^861^] | AR/VR Trends 2026 | innowise.com |
| [^864^] | AI Game Development Trends 2026 | artemisiacollege.com |
| [^865^] | AI in Gaming Market Report | snsinsider.com |
| [^835^] | OpenBlob Desktop Companion | dev.to |

---

> *This research compiled 25+ searches across academic papers, official documentation, open source repositories, game industry news, and technical analyses to provide a comprehensive foundation for implementing AI companion gaming in MEOK.*
