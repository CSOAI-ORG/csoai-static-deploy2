# MEOK Universe — AI Integration Platform Research

> **Research Date**: July 2025  
> **Purpose**: Enable "anyone can add their own AI" to the MEOK Universe game world.  
> **Coverage**: 20 platform categories, 15+ independent searches, API availability, pricing, UE5 integration, and open-source alternatives.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Inworld AI](#2-inworld-ai)
3. [Convai](#3-convai)
4. [Charisma AI](#4-charisma-ai)
5. [Character.AI API](#5-characterai-api)
6. [OpenAI GPTs / GPT Store](#6-openai-gpts--gpt-store)
7. [OpenRouter API](#7-openrouter-api)
8. [Local LLM Integration (Ollama, LM Studio)](#8-local-llm-integration-ollama-lm-studio)
9. [AI Agent Marketplace Platforms](#9-ai-agent-marketplace-platforms)
10. [Modding Framework for AI NPCs](#10-modding-framework-for-ai-npcs)
11. [Skyrim/Fallout AI Modding Community](#11-skyrimfallout-ai-modding-community)
12. [Minecraft AI Agent Mods (MineDojo)](#12-minecraft-ai-agent-mods-minedojo)
13. [AI NPC Plugin Architecture for UE5](#13-ai-npc-plugin-architecture-for-ue5)
14. [LLM-as-NPC Runtime for Games](#14-llm-as-npc-runtime-for-games)
15. [RAG System for Game NPCs (Persistent Memory)](#15-rag-system-for-game-npcs-persistent-memory)
16. [Voice Synthesis for Game NPCs (ElevenLabs, Coqui)](#16-voice-synthesis-for-game-npcs-elevenlabs-coqui)
17. [Emotion/Personality System for AI Characters](#17-emotionpersonality-system-for-ai-characters)
18. [AI Character SDK for Game Developers](#18-ai-character-sdk-for-game-developers)
19. [Anyone Can Create AI NPC — Platform Comparison](#19-anyone-can-create-ai-npc--platform-comparison)
20. [AI Avatar Creation Tools (Open Source)](#20-ai-avatar-creation-tools-open-source)
21. [Multi-Tenant AI Agent Platform Architecture](#21-multi-tenant-ai-agent-platform-architecture)
22. [Strategic Recommendations for MEOK Universe](#22-strategic-recommendations-for-meok-universe)

---

## 1. Executive Summary

The AI NPC integration landscape for games has matured rapidly since 2023. Multiple viable paths now exist for letting users add custom AI characters to a game world:

| Category | Leaders | Open-Source Alternative | Key Decision Factor |
|----------|---------|------------------------|---------------------|
| Commercial AI NPC Platforms | Inworld AI, Convai, Charisma AI | None direct | Cost scales with MAU; best for games with revenue |
| Custom GPT / Character AI | OpenAI GPTs, Character.AI | None direct | Content moderation; no full API access |
| Multi-Model Gateway | OpenRouter, Poe API | LiteLLM | Single API key, 315+ models, pay-per-token |
| Local LLM Runtime | Ollama, LM Studio | llama.cpp (Runtime Local LLM) | Zero cloud cost; requires GPU |
| UE5 Plugin Ecosystem | NVIDIA ACE, Convai, Runtime Local LLM | Ollama UE Plugin, Cactus AI | Plugin-based, Blueprint-friendly |
| Voice Synthesis | ElevenLabs | Coqui TTS, Piper TTS | ElevenLabs = best quality; Coqui = free |
| Persistent Memory | Custom RAG + Vector DB | Chroma, Qdrant, pgvector | Essential for NPCs that remember |
| Multi-Agent Orchestration | CrewAI, LangGraph, AutoGen | All open source | CrewAI easiest; LangGraph most powerful |

**Bottom Line for MEOK Universe**: A hybrid architecture using OpenRouter for cloud LLM access + local LLM fallback + RAG memory + ElevenLabs/Coqui for voice + CrewAI for multi-agent orchestration provides the most flexible "anyone can add AI" platform.

---

## 2. Inworld AI

### Overview
Inworld AI is a developer platform for creating AI-powered virtual characters. It provides a unified runtime for speech-to-text (STT), LLM inference, and text-to-speech (TTS), targeting real-time game and simulation use cases. [^146^][^154^]

### Key Features
- **Unified AI Runtime SDK**: Covers STT, LLMs, and TTS in a single SDK for Unreal Engine and Unity [^193^]
- **Visual Graph Editor**: Create AI pipelines (e.g., speech-to-speech) with a visual node editor [^193^]
- **Pre-built Templates**: Ready-to-use templates for AI NPCs and chatbots [^193^]
- **Hundreds of Models**: Access 150+ models with a single API key [^228^]
- **NPC Awareness**: Characters can be aware of in-game events, locations, time, and items [^197^]
- **Persistent Memory**: Vector database-backed conversation history [^234^]
- **Multi-NPC Conversations**: NPCs can talk to each other (radiant dialogue) [^197^]
- **VR Support**: Full integration for Unity OpenXR and Unreal SteamVR [^227^]

### API & SDK
- **SDKs**: Unity, Unreal Engine, Node.js [^228^]
- **API Type**: REST API for TTS and character interaction
- **Integration**: Unity Package Manager (`inworld-unity-sdk`) or GitHub clone for Unreal (`inworld-unreal-sdk`) [^227^]
- **Authentication**: API key-based
- **Platform Support**: Unity, Unreal, Web, VR/AR [^227^]

### Pricing
| Plan | Price | Features |
|------|-------|----------|
| Free/Hobbyist | $0 | Limited API interactions (200-5,000/month) [^213^] |
| Starter/Pro | $10-$25/month | 600-3,000 API calls/month, unlimited characters [^213^] |
| Launch/Enterprise | Custom | Tailored pricing based on DAU, revenue share possible [^213^] |
| TTS (each::labs) | $10/million chars (Max), $5/million (Mini) | Consumption-based billing [^146^] |

**Note**: Inworld's official pricing page has been reported as broken/outdated; third-party sources provide the above estimates [^213^].

### UE5 Integration
- Native Unreal Engine SDK via GitHub [^227^]
- Visual graph editor for building AI pipelines in UE5 [^193^]
- Blueprint and C++ support [^180^]

### Open-Source Alternative
- No direct open-source equivalent. Closest: **Runtime Local LLM** (UE5 plugin) + **Ollama** for local inference + **Coqui TTS** for voice [^188^][^184^]

---

## 3. Convai

### Overview
Convai is a creator-first AI character creation tool specifically built for games and virtual worlds. It provides REST APIs for programmatic character management and integrates deeply with Unreal Engine and Unity. [^148^][^153^]

### Key Features
- **Character Crafting APIs**: Create, update, and manage AI characters programmatically [^153^]
- **Knowledge Bank API**: Upload books, manuals, or learning modules to character knowledge [^153^]
- **Narrative Design API**: Create branching scenarios, training simulations, and dynamic interactions [^153^]
- **Voice & Language**: Configurable voices, 20+ languages supported [^157^]
- **3D Avatar Support**: Works with MetaHumans, Reallusion, Ready Player Me, custom avatars [^148^]
- **Facial Animation**: NeuroSync-powered facial animation and lip-sync component (`BP_ConvaiFaceSync`) [^157^]
- **NPC-to-NPC Conversations**: Multiple AI characters can converse with each other [^234^]
- **Real-time Updates**: Push new content, voices, and abilities to live characters [^153^]

### API & SDK
- **API Type**: RESTful Core APIs [^148^]
- **SDKs**: Unreal Engine (FAB plugin), Unity, Web, Mobile [^153^]
- **Components**: `BP_ConvaiChatbot` (AI logic, memory, LLM) + `BP_ConvaiFaceSync` (facial animation) [^157^]
- **Documentation**: docs.convai.com with API reference and Google Colab notebook tutorials [^148^]
- **Authentication**: API key-based

### Pricing
Convai uses tiered pricing. Specific public pricing details are limited, but the platform offers:
- Free tier for experimentation
- Usage-based paid tiers
- Per-minute cloud pricing model [^234^]

### UE5 Integration
- **Step 1**: Install Convai plugin from FAB Store [^157^]
- **Step 2**: Add `BP_ConvaiChatbot` component to avatar for AI logic [^157^]
- **Step 3**: Add `BP_ConvaiFaceSync` component for facial animation [^157^]
- **Step 4**: Connect Character ID from Convai Dashboard to the Blueprint [^157^]
- **Step 5**: Add `BP_ConvaiPlayer` to player pawn for voice interaction UI [^157^]
- Push-to-talk and hands-free voice modes supported [^157^]

### Open-Source Alternative
- **Ollama + Runtime Local LLM plugin + 3D avatar system**. Convai's key differentiator is its integrated NeuroSync facial animation, which would need manual integration with open-source tools.

---

## 4. Charisma AI

### Overview
Charisma.ai is a narrative-focused AI platform for creating story-driven interactive experiences. Unlike Inworld/Convai which focus on sandbox NPCs, Charisma specializes in narrative control with a unique "Emotion Engine." [^147^][^149^]

### Key Features
- **Blended AI**: Visual node-based story graph combined with generative AI for natural language responses [^147^]
- **Emotion Engine**: 12 distinct feelings for emotionally intelligent character responses [^147^]
- **Character Memory**: Characters recall details from past conversations [^147^]
- **Analytics**: Built-in analytics for tracking player engagement [^149^]
- **Plug'n'Play Modules**: Ready-made Unity and Unreal Engine modules [^147^][^152^]
- **Proprietary LLMs**: Uses its own trained language models (not GPT-4) [^149^]

### API & SDK
- **SDKs**: Unity SDK, Unreal Engine SDK, Web SDK [^147^]
- **Integration**: Plug'n'Play modules for Unity and Unreal [^152^]
- **Platform**: Web, mobile, VR, game engines

### Pricing
| Plan | Price | Features |
|------|-------|----------|
| Free Starter | Free (1-month Pro trial) | Limited features [^150^] |
| Pro | Pay-as-you-go: $5 per 50,000 credits (~200 experience minutes) | Story collaborators, script flow tools, AI voice, generative AI [^147^][^152^] |
| Enterprise | Custom (one-off dev fee + monthly) | Everything in Pro + premium voices, admin tools, templates, account manager [^152^] |

### Open-Source Alternative
- **LangGraph + custom narrative state machine + local LLM**. Charisma's blended approach (scripted + generative) can be replicated with a graph-based workflow engine.

---

## 5. Character.AI API

### Overview
Character.AI is a consumer-focused platform for creating and chatting with AI characters. It popularized the concept of AI personas but does NOT offer an official developer API. [^155^][^156^]

### API Status
- **Official API**: ❌ **Does not exist** as of 2026 [^156^]
- **Unofficial API**: Community wrapper `node-character.ai` exists but requires session token extraction from browser LocalStorage [^155^]
- **Platform Focus**: B2C consumer chat, NOT developer/game integration [^156^]

### Workaround Approaches
Since no official API exists, developers must build custom character AI using:

| Approach | Pros | Cons |
|----------|------|------|
| Build with GPT-4/Claude via API | Powerful, flexible, full API access | Requires development effort [^156^] |
| Build with open-source models | Full control, no content filters | Requires GPU infrastructure [^156^] |
| Use unofficial wrapper | Quick to try | Brittle, violates ToS [^155^] |

### Pricing
- Consumer platform: Freemium with $9.99/month subscription [^147^]
- No developer pricing (no API)

### Verdict for MEOK Universe
**Not suitable**. Character.AI has no developer API and is not designed for game integration. It serves as a reference for what end-user character creation looks like, not as an integration platform.

---

## 6. OpenAI GPTs / GPT Store

### Overview
OpenAI GPTs allow anyone to create custom versions of ChatGPT with specific instructions, knowledge, and actions. Launched November 2023. [^151^]

### Key Features
- **No-code builder**: Create GPTs via ChatGPT interface without coding [^197^]
- **Custom Instructions**: Define personality, behavior, and constraints
- **Knowledge Files**: Upload documents for RAG-based knowledge retrieval
- **Actions**: Connect to external APIs via OpenAPI schemas
- **GPT Store**: Publish GPTs for discovery by ChatGPT users [^197^]
- **Monetization**: Revenue-sharing program in development (based on engagement) [^197^]

### API for Developers
- GPTs themselves do NOT have a direct programmatic API
- However, **OpenAI Assistants API** provides similar functionality programmatically
- **Chat Completions API** with system prompts enables custom character behavior
- Models: GPT-4.5, GPT-4o, GPT-3.5-turbo [^158^]

### Pricing
| Tier | Price | Notes |
|------|-------|-------|
| ChatGPT Plus | $20/month | Access to GPTs |
| ChatGPT Team | $25/user/month | Team workspace |
| ChatGPT Enterprise | Custom | Enterprise features |
| API (GPT-4o) | $5/million input tokens, $15/million output tokens | Pay-per-use [^187^] |
| API (GPT-4o-mini) | $0.15/million input, $0.60/million output | Cheapest option |

### UE5 Integration
- No direct UE5 plugin from OpenAI
- Developers use HTTP requests to OpenAI API via Blueprint or C++
- Third-party plugins (Runtime AI Chatbot Integrator) provide Blueprint nodes [^187^]

### Open-Source Alternative
- **Ollama + local models (Llama 3, Mistral)** provides GPT-like functionality locally [^184^]
- **OpenRouter** provides access to GPT models and 315+ others via single API [^187^]

---

## 7. OpenRouter API

### Overview
OpenRouter is a unified API gateway that provides access to 315+ AI models from every major provider through a single, OpenAI-compatible API endpoint. [^187^][^196^]

### Key Features
- **315+ Models, One API Key**: Claude, GPT, Gemini, DeepSeek, Llama, Grok, and hundreds more [^187^]
- **OpenAI-Compatible API**: Drop-in replacement — just change base URL and API key [^187^]
- **Model Flexibility**: Switch models by changing one parameter, no code changes needed [^187^]
- **Free Models Available**: Dozens of free models with rate limits (20 req/min, 200 req/day) [^187^]
- **Usage Dashboard**: Track spending per model and per API key [^187^]
- **Pay-Per-Token**: No monthly fees, no minimum spend [^187^]

### API & Integration
```python
# Python example - OpenAI SDK compatible
import openai
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="$OPENROUTER_API_KEY",
)
response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Pricing
- **Billing**: Credit-based system, add credits via credit card or crypto [^187^]
- **Free Tier**: Free models at 20 req/min, 200 req/day [^187^]
- **Popular Models**: Pass-through pricing at or near direct API cost [^187^]
- **Example**: Claude Sonnet 4.5 at $3/$15 per million tokens (same as direct) [^187^]
- **Monthly Estimates**: Hobby $0-10, Light $10-50, Medium $50-300, Heavy $300+ [^187^]

### UE5 Integration
- Use via HTTP requests in Blueprint/C++
- Compatible with any plugin that uses OpenAI-compatible API (Runtime AI Chatbot Integrator, etc.)

### Open-Source Alternative
- **LiteLLM Proxy**: Self-hosted multi-model gateway with identical functionality, 90% cost reduction for multi-tenant setups [^190^]

---

## 8. Local LLM Integration (Ollama, LM Studio)

### Overview
Running LLMs locally eliminates cloud costs, latency, and dependency on external services. Critical for offline gameplay and data privacy.

### Ollama
- **What**: Open-source tool for running LLMs locally [^184^]
- **Supported Models**: Llama 3, Mistral, Gemma, Phi, Qwen, DeepSeek-R1, and 100+ more [^187^]
- **API**: REST API at `http://localhost:11434` [^184^]
- **Installation**: Download from ollama.com, run `ollama pull <model>` [^184^]
- **GPU**: Optional but recommended; falls back to CPU/RAM [^192^]

### LM Studio
- **What**: Desktop app for discovering, downloading, and running local LLMs
- **GUI-based**: No command line needed
- **Built-in Server**: Local OpenAI-compatible API server
- **Use Case**: Great for non-technical users and testing

### UE5 Integration
| Plugin | Features | Link |
|--------|----------|------|
| **Unreal Ollama Plugin** | Async Blueprint nodes, C++, text gen, chat, multimodal | GitHub: `MuddyTerrain/unreal-ollama` [^184^] |
| **Runtime Local LLM** | GGUF support, streaming, Windows/Mac/Linux/Android/iOS/Quest | FAB marketplace [^188^] |
| **Runtime AI Chatbot Integrator** | Ollama + Grok integration, streaming mode | FAB tutorial [^187^] |
| **Cactus AI Framework** | Local LLM + VLM + TTS, Blueprint exposed, UE5.6+ | GitHub: `cactus-compute/cactus` [^190^] |

### AI People — Real-World Example
AI People is the first game to implement AI NPCs powered by local LLM. Players can run the entire game offline with local LLM, local Speech Recognition, and optional TTS. Requires minimum 12GB GPU VRAM (8GB for LLM, 1-2GB for speech recognition). [^194^]

### Pricing
- **Ollama**: Free (open source)
- **LM Studio**: Free (desktop app)
- **Models**: Free (open source weights)
- **Hardware Cost**: GPU with 8GB+ VRAM recommended

### Open-Source Alternative
- Ollama itself IS the open-source alternative to cloud APIs
- **llama.cpp**: Core inference engine that powers most local LLM tools

---

## 9. AI Agent Marketplace Platforms

### Overview
AI agent marketplaces are platforms where developers publish and users discover/purchase AI agents. Think "App Store for AI agents." The market is projected to reach $50B by 2030. [^181^]

### Leading Marketplaces

| Platform | Type | Key Feature | Monetization |
|----------|------|-------------|--------------|
| **GPT Store** | Consumer | Custom GPTs for ChatGPT users | Revenue share (in development) [^197^] |
| **Poe** | Multi-model | Create bots on top of GPT/Claude/Gemini | $20/user earnings, price per message [^231^] |
| **Agent.ai** | Professional | LinkedIn for AI agents | Business use cases [^181^] |
| **Agentman** | No-code | Create/buy/sell AI agents without coding | Buy/sell marketplace [^181^] |
| **MindStudio** | No-code | Pixel-perfect interactive frontends | Anyone can create [^195^] |
| **Oracle AI Agent Marketplace** | Enterprise | Partner-built agent templates for Fusion Apps | Subscription fee [^189^] |
| **OpenAgents** | Open source | Native MCP + A2A protocol support | Free/open source [^211^] |

### Pricing
- **GPT Store**: Free to publish; no direct creator payments yet [^197^]
- **Poe**: Free tier 3,000 points/day; $4.99-$249.99/month subscriptions [^225^][^232^]
- **MindStudio**: Free tier available [^195^]
- **Agentman**: Not publicly disclosed [^181^]

### UE5 Integration
- None of these marketplaces offer direct UE5 integration
- Bots/agents are typically HTTP API-based; integrate via REST calls
- **OpenAgents** with native MCP/A2A protocols may offer the most game-friendly integration path [^211^]

### Open-Source Alternative
- **OpenAgents**: Open-source framework with native MCP and A2A protocols, network-based agent communities [^211^]
- **Build your own marketplace**: Using multi-tenant AI agent architecture (see Section 21)

---

## 10. Modding Framework for AI NPCs

### Overview
The AI NPC modding scene has exploded across multiple games, creating a blueprint for user-generated AI content.

### Key Technologies Used by Mods
- **LLM Integration**: OpenAI API, OpenRouter, local models (Ollama) [^197^]
- **Speech-to-Text**: Whisper, Windows Speech Recognition [^183^]
- **Text-to-Speech**: ElevenLabs, Coqui TTS, built-in TTS [^183^]
- **Memory Systems**: Vector databases for conversation history [^241^]
- **Game Integration**: SKSE (Skyrim), F4SE (Fallout), BepInEx, MelonLoader [^197^]

### Mod Architecture Pattern
1. Game mod DLL injects into game runtime
2. Intercepts NPC dialogue triggers
3. Sends player speech (via STT) or text to LLM
4. LLM generates response with character context + memory
5. TTS converts response to speech audio
6. Lip-sync/facial animation plays in-game

### Open-Source Frameworks
- **MelonLoader**: Universal mod loader for Unity games
- **BepInEx**: Plugin framework for Unity/.NET games
- **SKSE/F4SE**: Script extenders for Bethesda games
- **Harmony**: Runtime method patching library for C#

---

## 11. Skyrim/Fallout AI Modding Community

### Overview
The Skyrim modding community has become the proving ground for AI NPCs, with multiple active projects demonstrating what's possible.

### Key Mods

#### Mantella (30,000+ downloads) [^196^][^197^]
- **Features**: Talk to EVERY NPC in real-time, 3,000+ NPCs with unique backgrounds
- **Memory**: NPCs remember previous conversations
- **Awareness**: Knows in-game events, location, time, items
- **Actions**: NPCs can become followers, attack, share inventory
- **Vision**: Can "see" what the player sees (for vision models)
- **Radiant Dialogue**: NPCs start conversations with each other
- **Languages**: 20+ languages
- **Models**: Supports local, OpenRouter, and OpenAI LLMs [^197^]
- **Latest Version**: 0.14 (April 2026) — Advanced actions, nearby NPC tracking, combat awareness, vanilla dialogue awareness [^183^]

#### Herika (25,000+ downloads) [^196^]
- Started as a tool to summarize Skyrim books
- Evolved into a full AI follower/companion
- Uses OpenAI API (costs money per dialogue line) [^196^]
- Free option requires running LLM locally (resource-intensive) [^196^]

#### Other AI NPC Mods
- **Hogwarts Legacy**: AI companion mods [^196^]
- **Cyberpunk 2077**: AI NPC interaction mods [^196^]
- **Garry's Mod**: AI character mods [^196^]
- **Stardew Valley**: AI chatty companions [^196^]
- **Fallout 4**: Mantella has a dedicated Nexus page [^197^]

### Technical Architecture (Mantella)
- **Game Plugin**: SKSE plugin hooks into dialogue system
- **Python Backend**: Handles LLM communication, memory, context
- **STT**: Whisper or Windows Speech Recognition
- **TTS**: ElevenLabs, Coqui, or other TTS services
- **Memory**: File-based + LLM context window
- **Configuration**: In-game UI for settings [^183^]

### Lessons for MEOK Universe
1. **NPC memory is essential** — players love when NPCs remember past conversations [^197^]
2. **NPC-to-NPC dialogue creates emergent storytelling** [^183^]
3. **Vision capabilities** (NPCs "seeing" the game world) add immersion [^197^]
4. **In-game event awareness** makes NPCs feel alive [^183^]
5. **Free vs. paid model tension** — charging for AI usage is a barrier for mod users [^196^]
6. **Local LLM support** is critical for cost-sensitive users [^197^]

---

## 12. Minecraft AI Agent Mods (MineDojo)

### Overview
MineDojo is a framework for building open-ended embodied agents in Minecraft, featuring thousands of tasks and internet-scale multimodal knowledge. [^198^]

### Key Features
- **Simulation Suite**: Thousands of diverse open-ended tasks [^198^]
- **Knowledge Base**: Minecraft videos, tutorials, wiki pages, forum discussions [^198^]
- **Agent Architecture**: Leverages pre-trained video-language models as learned reward functions [^198^]
- **Generalist Agents**: Solves tasks specified in free-form language without manually designed rewards [^198^]
- **Open Source**: Full simulation suite, knowledge bases, algorithms, and pre-trained models [^198^]

### Technical Details
- **Authors**: NVIDIA, Caltech, Stanford, Columbia, SJTU, UT Austin [^198^]
- **Website**: https://minedojo.org
- **License**: Open source (all code, models, data released)

### Other Minecraft AI Projects
- **Minecraft GPT mods**: Various mods that integrate LLMs for NPC dialogue
- **Bot agents**: Frameworks for autonomous Minecraft agents using LLM reasoning

### Relevance to MEOK Universe
MineDojo demonstrates how a sandbox game can serve as a platform for AI agent research. The pattern of "game world + LLM agent + task specification" is directly applicable to MEOK Universe's "anyone can add AI" vision.

---

## 13. AI NPC Plugin Architecture for UE5

### Overview
Unreal Engine 5 has multiple plugin options for AI NPCs, from commercial SDKs to open-source local LLM plugins.

### Plugin Ecosystem

| Plugin | Type | Features | Cost |
|--------|------|----------|------|
| **NVIDIA ACE UE5 Plugins** | Official (NVIDIA) | ASR, SLM, TTS, Audio2Face, Blueprint + C++ | Free SDK + cloud usage [^180^] |
| **Convai FAB Plugin** | Commercial | Full AI character system, facial sync, voice | Per-minute pricing [^157^] |
| **Inworld AI Runtime SDK** | Commercial | Unified STT+LLM+TTS, visual graph editor | Usage-based [^193^] |
| **Runtime Local LLM** | Open source | Local GGUF models, streaming, all platforms | Free [^188^] |
| **Unreal Ollama Plugin** | Open source | Async Blueprint nodes, C++, multimodal | Free [^184^] |
| **Cactus AI Framework** | Open source | Local LLM+VLM+TTS, Blueprint, UE5.6+ | Free [^190^] |

### NVIDIA ACE UE5 Plugins (2026) [^180^]
Three pillars:
1. **Automatic Speech Recognition (ASR)**: nemo-conformer-ctc-120m + 7 additional languages
2. **Small Language Models (SLM)**: Local GGUF support, Qwen 3.5 4B included, low-latency text generation
3. **Text-to-Speech (TTS)**: Chatterbox Turbo 350M TTS model with example voices
- **Benefits**: Local, RTX-optimized, no cloud latency, predictable costs
- **Integration**: Blueprint and C++ examples, sample levels

### Architecture Pattern for MEOK Universe
```
UE5 Game Project
├── AI NPC Plugin (one of above)
│   ├── STT Component (speech input)
│   ├── LLM Component (brain/inference)
│   ├── TTS Component (voice output)
│   └── Facial Animation Component
├── Memory System (RAG + Vector DB)
│   ├── Conversation History
│   ├── Character Knowledge
│   └── World State
├── Character Registry
│   ├── User-created characters
│   ├── Official characters
│   └── Community characters
└── API Gateway
    ├── OpenRouter (cloud models)
    ├── Local LLM (offline)
    └── Voice Service (ElevenLabs/Coqui)
```

---

## 14. LLM-as-NPC Runtime for Games

### Overview
The concept of using LLMs as the runtime "brain" for NPCs has matured from experimentation to production-ready systems.

### Runtime Approaches

| Approach | Latency | Cost | Quality | Best For |
|----------|---------|------|---------|----------|
| **Cloud API (OpenAI/Claude)** | 200-800ms | Pay-per-token | Highest | Premium NPCs |
| **Cloud Gateway (OpenRouter)** | 300-1000ms | Pay-per-token | High | Multi-model flexibility |
| **Local LLM (Ollama, 7B)** | 50-300ms | Hardware only | Good | Offline, low-cost |
| **Local SLM (NVIDIA ACE, 4B)** | 10-100ms | Hardware only | Good | Real-time, low-latency |
| **Hybrid (local + cloud)** | Variable | Optimized | Best overall | Production games |

### NVIDIA ACE Game Agent SDK [^180^]
- **Local inference**: On-device AI companions with RTX optimization
- **Complete pipeline**: ASR → LLM → TTS → Facial animation
- **Latency target**: <300ms total response time for natural conversations [^234^]
- **No cloud costs**: All processing on local GPU/NPU

### Production Considerations
- **Response time budget**: <300ms feels natural, >1s feels sluggish [^234^]
- **Token streaming**: Stream response chunks for perceived responsiveness
- **Context management**: Trim conversation history to fit model context window
- **Fallback strategies**: If LLM fails, fall back to scripted dialogue
- **Rate limiting**: Prevent abuse in multiplayer settings

### Open-Source Solutions
- **Runtime Local LLM** (UE5): Full local inference pipeline [^188^]
- **NVIDIA ACE**: Free SDK, local inference [^180^]
- **Cactus AI**: Mobile-optimized local inference [^190^]

---

## 15. RAG System for Game NPCs (Persistent Memory)

### Overview
Retrieval-Augmented Generation (RAG) is essential for NPCs that remember past conversations, know game lore, and maintain persistent relationships with players.

### Why RAG Matters for NPCs
- **Long-term memory**: Without RAG, NPCs only remember what's in the LLM context window (~4K-128K tokens) [^241^]
- **Memory dilution**: Context gets lost after ~20 rounds of dialogue [^241^]
- **Knowledge base**: Characters need access to world lore, their backstory, game events
- **Personalization**: Each player has a unique relationship history

### RAG Architecture for Game NPCs
```
Player Input
    │
    ▼
[Query Embedding] ──→ [Vector Database]
                           │
    ┌──────────────────────┘
    ▼
[Retrieve Relevant Memories]
    │ (past conversations, lore, events)
    ▼
[Build Context Window] ←── [Character Prompt] ←── [World State]
    │
    ▼
[LLM generates response]
    │
    ▼
[Store to Vector DB] ──→ [Future Retrieval]
```

### Vector Database Options
| Database | Type | Best For |
|----------|------|----------|
| **Chroma** | Open source | Simple projects, local deployment |
| **Qdrant** | Open source | Production, filtering, hybrid search |
| **pgvector** | PostgreSQL extension | Existing Postgres users |
| **Pinecone** | Managed cloud | Scale without ops |
| **Weaviate** | Open source + cloud | Multi-modal data |

### Memory Types for NPCs
1. **Episodic Memory**: Specific past conversations with the player [^240^]
2. **Semantic Memory**: Facts about the world, lore, character knowledge [^240^]
3. **Procedural Memory**: How the character behaves, their personality
4. **Working Memory**: Current conversation context

### Implementation Approaches
- **Custom RAG**: LangChain/LlamaIndex + vector DB + custom retrieval logic
- **MindStudio**: No-code agent builder with persistent memory [^240^]
- **Inworld/Convai**: Built-in memory systems (commercial)

### Open-Source Stack
- **LlamaIndex**: RAG-native developer experience [^209^]
- **LangChain + Chroma**: Popular combination with Python integration
- **Sentence Transformers**: Generate embeddings locally

---

## 16. Voice Synthesis for Game NPCs (ElevenLabs, Coqui)

### Overview
Text-to-speech (TTS) is critical for immersive AI NPCs. Two dominant approaches: commercial cloud APIs (highest quality) vs. open-source local models (free but variable quality).

### ElevenLabs
**The commercial gold standard for AI voice synthesis.**

| Plan | Price | Characters/Month | Key Features |
|------|-------|-----------------|--------------|
| Free | $0 | 10K multilingual / 20K Flash | No commercial use, 128kbps [^186^] |
| Starter | $5 | 30K / 60K | Commercial license, instant voice clone [^186^] |
| Creator | $11/mo ($22 before discount) | 100K / 200K | 1 Pro voice clone, 192kbps [^186^] |
| Pro | $99/mo | 500K / 1M | 44.1kHz PCM output, 192kbps [^186^] |
| Scale | $330/mo | 2M / 4M | 3 seats, team collaboration [^186^] |
| Business | $1,320/mo | 11M / 22M | 10 Pro clones, low-latency TTS [^186^] |
| Enterprise | Custom | Custom | Custom terms, SLAs, SSO, HIPAA [^186^] |

**Key Features**:
- Voice cloning (instant + professional)
- 29 languages
- Low-latency model for real-time conversation
- API access at all paid tiers
- Sound effects and music generation (newer features)
- **Startup Grants**: 12 months free with 33M characters for eligible startups [^188^]

### Coqui TTS
**The leading open-source TTS toolkit.** [^212^]

| Aspect | Detail |
|--------|--------|
| License | MPL 2.0 |
| Languages | 1,100+ languages |
| Voice Cloning | XTTS v2 with 17 languages, <200ms streaming latency |
| Training | Fine-tune models in any language |
| Installation | `pip install coqui-tts` |
| Voice Conversion | OpenVoice, kNN-VC, FreeVC models |

**Python Example**:
```python
from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(text="Hello!", speaker_wav="reference.wav", language="en", file_path="output.wav")
```

**Trade-offs vs. ElevenLabs**:
- Coqui is free but requires self-hosting and GPU
- Voice quality is good but not as natural as ElevenLabs [^214^]
- XTTS underlying model is partially open (community fork maintained at `idiap/coqui-ai-TTS`)

### Other Open-Source TTS Options
- **Piper TTS**: Lightweight, fast, designed for embedded/local use
- **Mimic 3**: Mycroft's neural TTS, privacy-focused
- **Tortoise TTS**: High-quality but slow

### Recommendation for MEOK Universe
- **Premium tier**: ElevenLabs API for highest quality
- **Free/Standard tier**: Coqui TTS running locally
- **Hybrid**: ElevenLabs for important characters, Coqui for background NPCs

---

## 17. Emotion/Personality System for AI Characters

### Overview
Emotion and personality systems make AI characters feel believable and distinct rather than generic chatbots.

### Emotion Engine Approaches

#### 1. Charisma AI Emotion Engine [^147^]
- **12 distinct feelings** for nuanced emotional responses
- Emotions affect character dialogue, facial expressions, and behavior
- Visual story graph maps emotional arcs

#### 2. Inworld AI Character Brain [^146^]
- Personality traits drive behavior
- Emotional state affects responses
- Contextual awareness (location, time, events)

#### 3. NVIDIA ACE Emotional Animation [^234^]
- **Audio2Face**: Maps emotional tone in voice to facial muscle movements in real-time
- Anger → furrowed brows, surprise → widened eyes
- Automatic, no manual animation needed

#### 4. Custom Implementation
```python
class EmotionEngine:
    emotions = {
        'joy': 0.0, 'sadness': 0.0, 'anger': 0.0,
        'fear': 0.0, 'surprise': 0.0, 'disgust': 0.0,
        'trust': 0.0, 'anticipation': 0.0, 'love': 0.0,
        'curiosity': 0.0, 'boredom': 0.0, 'confusion': 0.0
    }
    
    personality = {
        'openness': 0.7,
        'conscientiousness': 0.5,
        'extraversion': 0.8,
        'agreeableness': 0.6,
        'neuroticism': 0.3
    }
    
    def update_emotion(self, event, intensity):
        # Event affects emotional state
        # Personality modifies emotional response
        pass
```

### Personality Frameworks
- **OCEAN/Big Five**: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- **MBTI**: Myers-Briggs types for simpler systems
- **Custom trait systems**: Game-specific personality axes

### Integration with LLM
Personality is injected via **system prompts**:
```
You are {name}, a {personality_type} character.
Personality traits: {traits}
Current emotional state: {emotions}
Speaking style: {style}
Backstory: {backstory}
Always stay in character. Respond according to your emotional state.
```

### Open-Source Tools
- **PersonalityForge**: Open-source chatbot personality system
- **Custom emotion trees**: Implement as state machines in game code
- **Sentis/ONNX models**: Run emotion classification locally in Unity

---

## 18. AI Character SDK for Game Developers

### Overview
Multiple SDKs exist for integrating AI characters into games, ranging from commercial all-in-one solutions to open-source component libraries.

### SDK Comparison

| SDK | UE5 | Unity | Local | Cloud | Voice | Memory | Price |
|-----|-----|-------|-------|-------|-------|--------|-------|
| **Inworld AI** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | Usage-based |
| **Convai** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | Per-minute |
| **Charisma AI** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | Pay-as-you-go |
| **NVIDIA ACE** | ✅ | ✅ | ✅ | Hybrid | ✅ | ✅ | Free SDK |
| **Cactus AI** | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | Free |
| **Runtime Local LLM** | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | Free |

### Key SDK Components Needed
1. **Character Definition**: Name, personality, backstory, voice
2. **LLM Integration**: Cloud API or local inference
3. **Memory System**: Conversation history, knowledge base
4. **STT**: Speech recognition for voice input
5. **TTS**: Voice synthesis for spoken responses
6. **Animation**: Lip-sync, facial expressions, gestures
7. **Action System**: NPCs can perform in-game actions
8. **Vision**: NPCs can "see" and react to the game world

### Open-Source SDK Stack for MEOK Universe
```
Component              Open-Source Option
─────────────────────────────────────────────
LLM Runtime            Ollama / llama.cpp
STT                    Whisper (OpenAI) / faster-whisper
TTS                    Coqui TTS / Piper
Animation              Oculus Lipsync / Rhubarb
Memory                 Chroma / Qdrant + LangChain
Character Config       JSON/YAML + custom editor
Multi-Agent            CrewAI / OpenAgents
```

---

## 19. Anyone Can Create AI NPC — Platform Comparison

### Overview
The "anyone can create AI" vision requires a platform that supports both no-code creation (for casual users) and API/SDK access (for advanced users).

### Platform Comparison Matrix

| Platform | No-Code | API | Game Integration | Self-Host | User-Created NPCs |
|----------|---------|-----|------------------|-----------|-------------------|
| **Inworld AI** | Studio UI | ✅ SDK | UE5, Unity | ❌ | ✅ |
| **Convai** | Dashboard | ✅ REST | UE5, Unity | ❌ | ✅ |
| **Charisma AI** | Story graph | ✅ SDK | UE5, Unity | ❌ | ✅ |
| **GPT Store** | Web UI | ❌ | ❌ | ❌ | ✅ (ChatGPT only) |
| **Poe** | Web UI | ✅ API | ❌ | ❌ | ✅ |
| **MindStudio** | Visual builder | ✅ SDK | ❌ | ❌ | ✅ |
| **OpenAgents** | Studio UI | ✅ Code | Partial | ✅ | ✅ |
| **Custom Build** | Custom UI | Full | Full | ✅ | ✅ |

### Key Insight: The "App Store" Model
For MEOK Universe to enable "anyone can add their AI," the platform needs:

1. **Creator Portal**: Web-based tool for defining characters (personality, voice, knowledge)
2. **Template System**: Pre-built character templates users can customize
3. **Asset Upload**: Users upload backstory documents, voice samples, images
4. **Approval/Moderation**: Content review before characters go live
5. **Discovery/Marketplace**: Browse and rate community-created NPCs
6. **Revenue Sharing**: If creators charge for their NPCs, platform takes a cut

### Existing Models for Creator Economy
- **GPT Store**: Free to create, no creator payments yet [^197^]
- **Poe**: Creators earn up to $20 per user they bring in, can set price per message [^231^]
- **Oracle AI Agent Marketplace**: Enterprise partner-built templates [^189^]

---

## 20. AI Avatar Creation Tools (Open Source)

### Overview
AI characters need visual representation. These tools enable avatar creation for game NPCs.

### Tools

#### Ready Player Me [^192^]
- **Type**: Cross-platform avatar system
- **Features**: Customizable avatars from selfies, extensive asset library
- **SDKs**: Android, iOS, Unity, Unreal Engine, WebGL, React
- **Developer Studio**: Set up Avatar Creator, custom designs, AI content tools
- **Monetization**: Sell avatars and skins with payment integration
- **Pricing**: Free tier available; paid for premium features
- **Open Source**: SDKs are open source

#### Inworld AI Avatar Integration
- Works with MetaHumans (Unreal), Ready Player Me, Reallusion [^148^]
- Full 3D avatar support with lip-sync and facial animation

#### Convai Avatar Support
- MetaHumans, Ready Player Me, Reallusion, custom 3D avatars [^148^]
- NeuroSync facial animation integration

#### Open-Source Avatar Tools
- **MakeHuman**: Free humanoid character creator
- **MB-Lab**: Blender addon for realistic human characters
- **Avaturn**: AI-generated 3D avatars from photos
- **Meshy AI**: Text-to-3D character generation

---

## 21. Multi-Tenant AI Agent Platform Architecture

### Overview
For MEOK Universe to host thousands of user-created AI characters, a multi-tenant architecture is required to isolate data, manage costs, and scale efficiently.

### Why Multi-Tenancy Matters [^189^]
- **Cost**: 60-70% infrastructure cost reduction vs. single-tenant [^191^]
- **Scalability**: Horizontal scaling across all tenants
- **Management**: Centralized updates and monitoring
- **Risk**: One tenant's runaway agent can't burn the entire OpenAI budget [^190^]

### Three Deployment Patterns [^190^]

| Pattern | Isolation | Cost | Best For |
|---------|-----------|------|----------|
| **Silo** | Dedicated everything per tenant | Very high | Enterprise (banks, healthcare) |
| **Pool** | Shared with tenant filters | Optimized | Most SaaS products (start here) |
| **Bridge** | Hybrid (Pool for SMB, Silo for Enterprise) | Balanced | B2B SaaS with multiple tiers |

### Core Technical Pillars [^189^]
1. **Context Isolation**: Every prompt tagged with `tenant_id`
2. **Access Control**: JWT tokens with tenant identification
3. **Central Orchestrator**: Rate limiting, load balancing per tenant

### Security Requirements [^190^][^193^]
- **Data Isolation**: Vector database namespaces per tenant
- **Compute Isolation**: Per-tenant resource quotas
- **Cost Isolation**: Per-tenant usage tracking and budget caps
- **Memory Isolation**: Separate conversation history, RAG indices per tenant
- **Audit Logging**: Every agent action traced with tenant ID

### Architecture for MEOK Universe
```
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                           │
│         (Auth, Rate Limit, Tenant Routing)               │
└─────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  Tenant A  │  │  Tenant B  │  │  Tenant C  │
    │ (User NPCs)│  │ (User NPCs)│  │ (User NPCs)│
    ├────────────┤  ├────────────┤  ├────────────┤
    │ • NPC 1    │  │ • NPC 4    │  │ • NPC 7    │
    │ • NPC 2    │  │ • NPC 5    │  │ • NPC 8    │
    │ • NPC 3    │  │ • NPC 6    │  │ • NPC 9    │
    │            │  │            │  │            │
    │ Vector DB  │  │ Vector DB  │  │ Vector DB  │
    │ (isolated) │  │ (isolated) │  │ (isolated) │
    └────────────┘  └────────────┘  └────────────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
    ┌──────────────────────────────────────────────────┐
    │              LLM Proxy (LiteLLM)                  │
    │   ┌──────────────────────────────────────────┐    │
    │   │ Organizations → Teams → Users → Keys    │    │
    │   │ Budget caps cascade down the chain       │    │
    │   └──────────────────────────────────────────┘    │
    └──────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  Cloud LLM │  │  Local LLM │  │  Voice Svc │
    │ (OpenRouter)│  │  (Ollama)  │  │(ElevenLabs)│
    └────────────┘  └────────────┘  └────────────┘
```

### Framework Limitations [^190^]
- **LangGraph**: No native multi-tenant primitives
- **CrewAI**: No native tenant boundaries
- **AutoGen**: No multi-tenant support
- **LiteLLM**: Only handles LLM layer; rest is on you

### Open-Source Multi-Tenant Platform [^195^]
A fully open-sourced multi-tenant AI agent platform exists with:
- **Docker isolation**: Per-user container isolation
- **SIWE auth**: Sign-In with Ethereum
- **Markdown agent definitions**: `.md` files with YAML frontmatter
- **x402 gateway**: Agent-to-agent payments on Base blockchain

---

## 22. Strategic Recommendations for MEOK Universe

### Recommended Architecture

Based on this research, MEOK Universe should implement a **hybrid, multi-tenant AI platform**:

#### Tier 1: Cloud-Powered Premium NPCs
- **LLM**: OpenRouter gateway (single API, 315+ models) [^187^]
- **Voice**: ElevenLabs API (highest quality TTS) [^186^]
- **Memory**: Per-tenant vector database (Qdrant or pgvector) [^240^]
- **Latency**: 200-500ms acceptable for premium experience

#### Tier 2: Local LLM NPCs
- **LLM**: Ollama + Unreal Ollama Plugin [^184^]
- **Voice**: Coqui TTS (locally hosted) [^212^]
- **Memory**: Local SQLite + embeddings
- **Requirement**: 8GB+ GPU VRAM

#### Tier 3: On-Device (Mobile/Quest)
- **LLM**: NVIDIA ACE small language models (4B params) [^180^]
- **Voice**: Chatterbox Turbo 350M TTS [^180^]
- **Processing**: Fully local, zero cloud cost

### Creator Platform
1. **No-code Character Creator**: Web UI for defining personality, uploading knowledge, selecting voice
2. **Template Library**: Pre-built archetypes (merchant, quest-giver, companion, etc.)
3. **Community Marketplace**: Browse, rate, and install user-created NPCs
4. **Revenue Model**: Free tier (basic NPCs) + Premium tier (advanced features, voice cloning)
5. **Moderation**: Content review pipeline for community submissions

### Technology Stack
| Component | Primary | Fallback |
|-----------|---------|----------|
| LLM Gateway | OpenRouter | Ollama local |
| TTS | ElevenLabs | Coqui TTS |
| STT | Whisper API | Whisper local |
| Memory | Qdrant vector DB | SQLite + embeddings |
| Multi-Agent | CrewAI | Custom orchestration |
| Avatars | Ready Player Me | Custom 3D models |
| UE5 Plugin | NVIDIA ACE + Custom | Runtime Local LLM |
| Auth | JWT + tenant_id | SIWE (blockchain) |

### Cost Model (Per 1,000 Active NPCs)
| Component | Cloud Cost | Local Cost |
|-----------|-----------|------------|
| LLM (light usage) | $50-150/month | GPU electricity only |
| TTS (ElevenLabs Pro) | $99/month | Free (Coqui) |
| Vector DB | $20-50/month | Free (local) |
| Total per 1K NPCs | ~$170-300/month | ~$0 (hardware already owned) |

### Implementation Priority
1. **Phase 1**: OpenRouter + basic STT/TTS + conversation memory
2. **Phase 2**: RAG system + persistent NPC knowledge
3. **Phase 3**: Creator portal + community marketplace
4. **Phase 4**: Local LLM support + mobile/Quest optimization
5. **Phase 5**: Multi-agent interactions (NPC-to-NPC) + emergent storytelling

---

## Sources

- [^146^] each::labs — Inworld AI Provider: https://www.eachlabs.ai/inworld
- [^147^] Skywork.ai — Charisma.ai Deep Dive: https://skywork.ai/skypage/en/Charisma.ai-A-Deep-Dive
- [^148^] Convai — Core APIs Tutorial: https://www.youtube.com/watch?v=vwBzaQP0Bl4
- [^149^] The Decoder — Charisma AI: https://the-decoder.com/charisma-ai
- [^150^] AI Dex — Charisma.ai Tool: https://www.img2046.com/aidex/tool/charisma-ai
- [^151^] Wikipedia — OpenAI: https://en.wikipedia.org/wiki/OpenAI
- [^152^] Charisma.ai — Pricing: https://charisma.ai/pricing
- [^153^] Convai — Character Crafting APIs Blog: https://convai.com/blog/build-control-empower-ai-characters-programmatically
- [^154^] Inworld AI X/Twitter: https://x.com/inworld_ai
- [^155^] GitHub — node-character.ai: https://github.com/RichardDorian/node-character.ai
- [^156^] CrazyRouter — Character AI API Guide: https://crazyrouter.com/en/blog/character-ai-api-guide
- [^157^] Convai — Quick Setup Guide UE: https://convai.com/blog/quick-setup-guide-conversational-ai-unreal-engine-convai-fab-plugin
- [^158^] APIYi — AI Model API Documentation: https://docs.apiyi.com/en/resources
- [^180^] NVIDIA Developer Blog — ACE UE5 Plugins: https://developer.nvidia.com/blog/build-on-device-ai-companions
- [^181^] Fast.io — Top AI Agent Marketplaces: https://fast.io/resources/top-ai-agent-marketplaces
- [^183^] Yahoo Tech — Skyrim AI Mod Overhaul: https://tech.yahoo.com/gaming/articles/skyrim-mod-makes-npcs-ai
- [^184^] GitHub — Unreal Ollama Plugin: https://github.com/MuddyTerrain/unreal-ollama
- [^186^] FlexPrice — ElevenLabs Pricing: https://flexprice.io/blog/elevenlabs-pricing-breakdown
- [^187^] Epic Games Dev — Ollama AI Integration UE: https://dev.epicgames.com/community/learning/tutorials/X7KV
- [^188^] Epic Games Dev — Runtime Local LLM Plugin: https://dev.epicgames.com/community/learning/tutorials/M45X
- [^189^] Oracle — AI Agent Marketplace: https://blogs.oracle.com/fusioninsider/introducing-ai-agent-marketplace
- [^190^] Build MVP Fast — Multi-Tenant AI Architecture: https://www.buildmvpfast.com/blog/multi-tenant-ai-agent-architecture
- [^191^] EsferaSoft — Cloud Architecture Multi-Tenant AI SaaS: https://www.esferasoft.com/blog/cloud-architecture-for-multi-tenant-ai-saas-platforms
- [^192^] AI Axio — Ready Player Me: https://aiaxio.com/tools/ai/ready-player-me
- [^193^] Inworld AI Blog — Unreal AI Runtime SDK: https://inworld.ai/blog/introducing-unreal-ai-runtime-sdk
- [^194^] Marek Rosa Blog — AI People Local LLM: https://blog.marekrosa.org/2024/12/ai-people-now-with-local-llm
- [^195^] Dev.to — Multi-Tenant AI Agent Platform Open Source: https://dev.to/agentbot/how-we-built-a-multi-tenant-ai-agent-platform
- [^196^] The Verge — Modders AI Companions: https://www.theverge.com/2024/10/17/24268007/modders-ai-companions-stardew-valley-skyrim
- [^197^] Nexus Mods — Mantella: https://www.nexusmods.com/skyrimspecialedition/mods/98631
- [^198^] NeurIPS — MineDojo Paper: https://papers.nips.cc/paper_files/paper/2022
- [^209^] Cordum — AI Agent Frameworks Comparison: https://cordum.io/blog/ai-agent-frameworks-comparison
- [^211^] OpenAgents — Framework Comparison: https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared
- [^212^] GitHub — Coqui TTS: https://github.com/idiap/coqui-ai-TTS
- [^213^] eesel.ai — Inworld AI Pricing Guide: https://www.eesel.ai/blog/inworld-ai-pricing
- [^214^] Reddit — Self-hosted TTS Review: https://www.reddit.com/r/selfhosted/comments/17oabw3
- [^225^] Poe Help Center — Pricing FAQ: https://help.poe.com/hc/en-us/articles/19945140063636
- [^227^] WebSim — VR Integration Guide Inworld AI: https://vr-integration-guide-inworld-ai--luminousbreeze53797175.on.websim.com
- [^228^] each::labs — Inworld SDK Documentation: https://www.eachlabs.ai/inworld
- [^229^] Meta Developers — Unity Inference Engine: https://developers.meta.com/horizon/documentation/unity/unity-pca-sentis
- [^231^] Voiceflow — Poe AI Features: https://www.voiceflow.com/blog/poe-ai
- [^232^] SeaArt — Poe AI Deep Dive: https://www.seaart.ai/blog/poe-ai
- [^233^] Poe Blog — Transparent Pricing: https://poe.com/blog/introducing-transparent-usd-pricing-and-api-tool-calling
- [^234^] Antier Studios — NVIDIA ACE: https://studio.antier.com/blogs/nvidia-ace-ai-powered-games-npcs-2026
- [^236^] Unity Discussions — Runtime AI in Unity 6: https://discussions.unity.com/t/bringing-runtime-ai-to-unity-6/1529799
- [^237^] Medium — Unity Sentis + Hugging Face: https://medium.com/@olgaphila40/unitys-sentis-ai-technology
- [^239^] Poe Creator Docs — OpenAI Compatible API: https://creator.poe.com/docs/external-applications/openai-compatible-api
- [^240^] MindStudio — AI Agent Persistent Memory: https://www.mindstudio.ai/blog/ai-agent-persistent-memory-rag-vector-search
- [^241^] arXiv — LLM-Driven NPCs Cross-Platform: https://arxiv.org/html/2504.13928v1

---

*Research compiled for MEOK Universe — "Anyone can add their AI" platform design.*
