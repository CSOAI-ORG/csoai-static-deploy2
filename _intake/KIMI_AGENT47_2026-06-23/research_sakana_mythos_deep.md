# Sakana AI Complete Product Line Research
## Clarifying the "Japanese Mythos 5" Confusion

**Research Date:** June 22, 2026
**Key Finding:** "Mythos 5" and "Fable 5" are **ANTHROPIC (US)** models, NOT Sakana products. The TikTok "Japanese Mythos 5" claim is a misunderstanding that conflates Sakana Fugu (Japanese AI orchestration) with Anthropic Mythos (US model banned by export controls).

---

## TABLE OF CONTENTS

1. [Sakana AI Company Background](#1-sakana-ai-company-background)
2. [THE PRODUCT LINE: Clarifying the Confusion](#2-the-product-line)
3. [The "Export Controls" Angle](#3-the-export-controls-angle)
4. [Fugu API Integration Guide](#4-fugu-api-integration-guide)
5. [Sakana's Other Products & Research](#5-sakana-other-products)
6. [Other Japanese AI Companies](#6-other-japanese-ai-companies)
7. [Strategic Implications for CSOAI/MEOK](#7-strategic-implications)

---

## 1. SAKANA AI COMPANY BACKGROUND

### Founders

| Founder | Role | Background |
|---------|------|------------|
| **David Ha** | Co-Founder & CEO | Former Research Scientist at Google, led Google Brain Research team in Japan. PhD from University of Tokyo. Previously Managing Director and head of interest rates trading at Goldman Sachs Japan. Hong Kong-born Canadian, long-term Japan resident. Named TIME100 Most Influential People in AI 2025. |
| **Llion Jones** | Co-Founder & CTO | Co-author of the landmark "Attention Is All You Need" paper (2017) that introduced the Transformer architecture underlying all modern LLMs. Former Google researcher. |
| **Ren Ito** | Co-Founder & Chairman | Graduated from University of Tokyo Faculty of Law. Former Japanese Ministry of Foreign Affairs. Held executive roles at Mercari and Stability AI before co-founding Sakana AI in 2023. |

### Company Overview

| Attribute | Details |
|-----------|---------|
| **Company Name** | Sakana AI K.K. (Sakana AI Co., Ltd.) |
| **Founded** | July 2023 |
| **Headquarters** | Azabudai Hills Mori JP Tower 22F, 1-3-1 Azabudai, Minato-ku, Tokyo, 106-0041 JAPAN |
| **Industry** | Frontier AI / Applied AI / Sovereign AI |
| **Focus** | Nature-inspired AI (swarm intelligence, evolutionary computation, collective intelligence) |
| **Team Size** | ~102 employees (as of November 2025, including contractors) |
| **Revenue** | $30M ARR (as of November 2025) |
| **Valuation** | $2.63B (post-Series B, November 2025) |
| **Status** | Japan's most valuable unlisted AI startup (fastest to unicorn) |

### Funding History

| Round | Date | Amount | Valuation | Key Investors |
|-------|------|--------|-----------|---------------|
| **Seed** | 2024 | $30M | - | Lux Capital, Khosla Ventures |
| **Series A** | 2024 | $200M | $1B | MUFG, SMBC, Mizuho, Itochu, KDDI, Nomura, NVIDIA, Salesforce Ventures, NEA, Google |
| **Series B** | Nov 2025 | $135M | $2.6B | MUFG, Khosla Ventures, NEA, Lux Capital, In-Q-Tel (IQT), Factorial Funds, Macquarie Capital, NVIDIA, Salesforce Ventures, and 25+ others |

**Total Raised:** $365M across 3 rounds

### Key Japanese Investors
ITOCHU Group, ANA Holdings, MPower Partners, SBI Group, STNet (Shikoku Electric Power), Global Brain, KDDI, CCI Group, JAFCO, Dai-ichi Life Insurance, Tokio Marine & Nichido, NEC, Nippon Life Insurance, Nomura Holdings, Fujitsu, Sumitomo Mitsui Banking Corp, Mitsubishi UFJ Financial Group (MUFG), Mitsubishi Electric, Mizuho Financial Group, Miyako Capital, Meiji Yasuda Life Insurance

### Key Overseas Investors
500 Global, Basis Set Ventures, Citi Group, Datadog, Factorial Funds, Fundomo, Geodesic Capital, Google, In-Q-Tel (IQT), July Fund, Khosla Ventures, Learn Capital, Lux Capital, Macquarie Capital, Mouro Capital (Santander), NEA, NVIDIA, Ora Global, Salesforce Ventures, Translink Capital

### Research Focus Areas
Sakana AI's work is organized into three pillars:
- **Research:** Collective intelligence, evolution-inspired AI, The AI Scientist, Darwin Godel Machine, ShinkaEvolve, AB-MCTS
- **Applied:** Finance, defense, intelligence - solutions reaching into Japan's social infrastructure
- **Product:** User-facing AI products: Sakana Chat, Sakana Marlin, Sakana Fugu

---

## 2. THE PRODUCT LINE: CLARIFYING THE CONFUSION

### THE CRITICAL CLARIFICATION

| Name | What It Actually Is | Who Owns It | Status |
|------|-------------------|-------------|--------|
| **Fable 5** | Anthropic's top-tier AI model (Claude Fable 5) | **Anthropic (US)** | BANNED by US export controls June 12, 2026 |
| **Mythos 5** | Anthropic's underlying cybersecurity-capable model (Claude Mythos 5) | **Anthropic (US)** | BANNED by US export controls June 12, 2026 |
| **Fugu** | Multi-agent orchestration system | **Sakana AI (Japan)** | LAUNCHED June 22, 2026 - commercially available |
| **Mythos Preview** | Anthropic's earlier preview model | **Anthropic (US)** | Replaced by Mythos 5, now also restricted |

### What Happened

1. **Anthropic** (US company, founded by Dario Amodei) developed **Mythos**, a powerful cybersecurity-capable AI model
2. They built **Fable 5** on top of Mythos with safety guardrails to restrict access to dangerous capabilities
3. On **June 12, 2026**, the US Commerce Department issued export controls banning Anthropic from distributing Fable 5 and Mythos 5 to ANY foreign nationals (including non-citizen employees)
4. Anthropic had to disable both models for ALL users worldwide
5. On **June 22, 2026**, Sakana AI launched **Fugu**, which achieves similar/better performance WITHOUT relying on Anthropic's banned models
6. TikTok/Twitter confusion: People conflated "Sakana Fugu" (Japanese AI) with "Mythos" (Anthropic's banned model) -> The "Japanese Mythos 5" myth was born

**"Japanese Mythos 5" does NOT exist. Mythos is 100% American (Anthropic). Fugu is Japanese (Sakana AI) and is an ALTERNATIVE to Mythos, not a version of it.**

---

### FUGU: Sakana AI's Multi-Agent Orchestration System

**Product URL:** https://sakana.ai/fugu
**Console:** https://console.sakana.ai/
**Launch Date:** June 22, 2026 (beta opened April 24, 2026)
**Status:** Commercially available

#### What Fugu Does

Fugu is a **multi-agent orchestration system** that behaves like a single foundation model. Instead of being one monolithic model, Fugu is itself a **7B parameter coordinator LLM** trained to call other LLMs in an agent pool - including instances of itself recursively.

**The user experience:** You send one API request. Fugu breaks down complex tasks, delegates sub-tasks to a pool of expert foundation models, verifies their work, and synthesizes the final output. The complexity is entirely abstracted behind a single OpenAI-compatible API endpoint.

**Key quote from Sakana:** "Fugu is itself an LLM, trained to call various LLMs in an agent pool, including instances of itself recursively."

#### How It Works (Technical)

Built on two ICLR 2026 papers:

1. **TRINITY**: An evolved LLM coordinator that assigns Thinker, Worker, and Verifier roles across a multi-model pool, adaptively delegating work across coding, math, reasoning, and knowledge tasks.

2. **The Conductor**: Trained with reinforcement learning to discover natural-language coordination strategies, designing agent communication patterns and focused prompts that help diverse LLM pools outperform individual workers.

Fugu learns to coordinate dynamically - it decides when to delegate, how agents should communicate, and how to combine their outputs. This is NOT hardcoded routing; it's learned orchestration.

#### Two Variants

| Feature | **Fugu** (Standard) | **Fugu Ultra** |
|---------|-------------------|----------------|
| **Model ID** | `fugu` | `fugu-ultra-20260615` |
| **Focus** | Low latency, everyday tasks | Maximum quality on complex tasks |
| **Agent Pool** | Configurable (opt-out available) | Fixed full pool |
| **Best For** | Coding, code review, chatbots, interactive work | Paper reproduction, Kaggle competitions, cybersecurity analysis, patent research |
| **Latency** | Fast | Slow (11 seconds to 4+ hours depending on task) |
| **Context Window** | 1M tokens | 1M tokens (272K threshold for higher pricing) |
| **Reasoning Effort** | `high`, `xhigh`/`max` | Automatic deep reasoning |

#### Benchmark Performance (Fugu Ultra vs Competitors)

| Benchmark | Fugu | Fugu Ultra | Opus 4.8 | Gemini 3.1 Pro | GPT 5.5 |
|-----------|------|-----------|----------|---------------|---------|
| **SWE Bench Pro** | 59.0 | **73.7** | 69.2 | 54.2 | 58.6 |
| **TerminalBench 2.1** | 80.2 | **82.1** | 74.6 | 70.3 | 78.2 |
| **LiveCodeBench** | **92.9** | **93.2** | 87.8 | 88.5 | 85.3 |
| **Humanity's Last Exam** | 47.2 | **50.0** | 49.8 | 44.4 | 41.4 |
| **GPQA-D** | **95.5** | **95.5** | 92.0 | 94.3 | 93.6 |
| **Long Context Reasoning** | **74.7** | 73.3 | 67.7 | 72.7 | 74.3 |
| **MRCRv2** | 86.6 | 93.6 | 87.9 | 84.9 | **94.8** |

**Key claim:** Fugu Ultra matches or exceeds Anthropic's Fable 5 and Mythos Preview across rigorous benchmarks, delivering "frontier capability without the risk of export controls."

---

### Pricing

#### Subscription Plans (Monthly)

| Plan | Price | Usage | Best For |
|------|-------|-------|----------|
| **Standard** | $20/month | Baseline allowance | Lightweight daily use, occasional API calls, personal experiments |
| **Pro** | $100/month | 10x Standard | Regular coding, review, research sessions throughout the week |
| **Max** | $200/month | 20x Standard | Power users with long-running, deeper tasks |

- Every tier includes BOTH Fugu and Fugu Ultra
- Subscribe before July 2026: **free second month**
- Subscription tokens served at lower priority than pay-as-you-go

#### Pay-as-You-Go (Enterprise)

**For Fugu (standard):**
- 1 agent active: Pay standard rate of that specific underlying model
- Multiple agents active: Pay single rate of the TOP TIER model involved (NO stacking fees)

**For Fugu Ultra:**

| Token Type | Standard (<=272K context) | Extended (>272K context) |
|------------|---------------------------|--------------------------|
| **Input** | $5 / 1M tokens | $10 / 1M tokens |
| **Output** | $30 / 1M tokens | $45 / 1M tokens |
| **Cached Input** | $0.50 / 1M tokens | $1.00 / 1M tokens |

**Pricing comparison with frontier models:**

| Model | Input | Output | Total |
|-------|-------|--------|-------|
| MiMo-V2.5 Flash | $0.10 | $0.30 | $0.40 |
| DeepSeek V4 Flash | $0.14 | $0.28 | $0.42 |
| GPT-5.4 | $2.50 | $15.00 | $17.50 |
| Gemini 3.1 Pro (>200K) | $4.00 | $18.00 | $22.00 |
| Claude Opus 4.8 | $5.00 | $25.00 | $30.00 |
| GPT-5.5 | $5.00 | $30.00 | $35.00 |
| **Sakana Fugu Ultra** | **$5.00** | **$30.00** | **$35.00** |
| Claude Fable 5 / Mythos 5 | $10.00 | $50.00 | $60.00 |

#### Important Pricing Caveat

Fugu Ultra's API responses include detailed usage fields separating user-visible tokens from internal orchestration tokens. **The orchestration tokens (background work when Fugu delegates, verifies, routes between agents) represent REAL token usage and ARE counted toward the final price.** They are NOT absorbed by the provider.

Usage fields in response:
```json
{
  "usage": {
    "input_tokens": 120,
    "output_tokens": 80,
    "total_tokens": 200,
    "input_tokens_details": {
      "cached_tokens": 0,
      "orchestration_input_tokens": 0,
      "orchestration_input_cached_tokens": 0
    },
    "output_tokens_details": {
      "orchestration_output_tokens": 0
    }
  }
}
```

---

## 3. THE "EXPORT CONTROLS" ANGLE

### What Happened on June 12, 2026

The US Commerce Department issued an export control directive requiring Anthropic to **halt all access** to Fable 5 and Mythos 5. The directive:
- Applied to ALL foreign nationals, including those inside the US
- Included Anthropic's own non-citizen employees
- Forced Anthropic to disable both models for EVERYONE (not just foreign users)
- The trigger was reportedly Amazon's report to the White House about potential safety guardrail bypasses

### Anthropic's Response

Anthropic CEO Dario Amodei and the company:
- Disagreed with the finding, calling it a "misunderstanding"
- Noted the jailbreak was narrow, not universal
- Pointed out the same technique could work on other models (including GPT-5.5) that weren't subject to export controls
- Called for "transparent, fair, clear" statutory process for blocking model deployments
- Stated: "If this standard was applied across the industry, it would essentially halt all new model deployments for all frontier model providers"

### The G7 Fallout

French President Emmanuel Macron warned at the G7 summit: If the US can "turn off the switch from one day to the next," it harms not just European customers but the AI companies themselves. This triggered a broader debate about **AI sovereignty** - the need for countries to have access to AI that can't be unilaterally revoked by the US government.

### How Fugu Addresses This

| Risk | With Anthropic Fable/Mythos | With Sakana Fugu |
|------|---------------------------|-----------------|
| **Export controls** | Models can be banned overnight | Swappable agent pool routes around restrictions |
| **Single vendor lock-in** | Dependent on Anthropic | Dynamically routes across multiple providers |
| **Geopolitical risk** | US policy decides access | Japanese company, multi-model architecture |
| **Service continuity** | All-or-nothing (one provider) | Graceful degradation if one provider is restricted |

**Sakana's positioning:** "Fugu functions as a hedge against sudden supply chain disruptions. The platform relies on a completely swappable agent pool. Fugu dynamically routes traffic around any restricted or degraded provider to maintain service continuity."

### How This Benefits CSOAI/MEOK

1. **Access to frontier-level AI** without depending on US models subject to export controls
2. **Multi-model redundancy** - if one provider is restricted, Fugu routes to others
3. **Japanese sovereignty angle** - Sakana is a Japanese company, making it a natural partner for Sino-Nova (Japanese-inspired civilization)
4. **OpenAI-compatible API** - drop-in replacement for existing integrations
5. **No training data lock-in** - can opt out of data usage for training

---

## 4. FUGU API INTEGRATION GUIDE

### API Endpoint

```
Base URL: https://api.sakana.ai/v1
```

### Authentication

```bash
export SAKANA_API_KEY="sk-..."
# Authorization: Bearer <api_key>
```

### Quick Test

```bash
curl -X POST https://api.sakana.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SAKANA_API_KEY" \
  -d '{"model":"fugu","messages":[{"role":"user","content":"How many r in word strawberry"}]}'
```

### Model IDs

| Model | ID | Description |
|-------|-----|-------------|
| **Fugu** | `fugu` | Balanced performance/latency, configurable pool |
| **Fugu Ultra** | `fugu-ultra-20260615` | Maximum quality, fixed full pool |

### Python SDK Example (OpenAI-compatible)

```python
from openai import OpenAI

api_key = "YOUR_API_KEY"
client = OpenAI(
    base_url="https://api.sakana.ai/v1",
    api_key=api_key
)

# Fugu Ultra for complex tasks
response = client.responses.create(
    model="fugu-ultra",
    input="Write a concise explanation of how TLS works",
    timeout=120.0,
)
print(response.output_text)
```

### Python SDK with Reasoning Effort

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.sakana.ai/v1",
    api_key="YOUR_API_KEY"
)

# Fugu with high reasoning effort
response = client.responses.create(
    model="fugu",
    input="Complex reasoning task here",
    reasoning={"effort": "high"},  # or "xhigh" / "max"
    timeout=120.0,
)
print(response.output_text)
```

### Codex CLI Integration

**One-line install:**
```bash
curl -fsSL https://sakana.ai/fugu/install | bash
```

**Launch:**
```bash
codex-fugu
```

### Manual Codex Configuration

Save to `~/.codex/fugu.json` (model catalog) and `~/.codex/fugu.config.toml` (profile). Full configs available at: https://github.com/SakanaAI/fugu

Key resilience settings for Codex:
```toml
stream_idle_timeout_ms = 7200000   # 2h: don't drop slow turns
stream_max_retries = 5             # reconnect dropped streams
request_max_retries = 4            # retry transient HTTP failures
```

### API Features

| Feature | Support |
|---------|---------|
| **OpenAI-compatible API** | Yes - Chat Completions + Responses endpoints |
| **Streaming** | Yes |
| **Reasoning effort levels** | `high`, `xhigh`/`max` (Fugu model only) |
| **Image input** | Yes (multimodal) |
| **Context window** | 1M tokens |
| **Built-in tools** | Web search available |
| **Provider opt-out** | Yes (Fugu standard, not Ultra) |
| **Training data opt-out** | Yes (via console) |
| **Timeout recommendation** | 120s+ for Fugu Ultra complex tasks |

### Geographical Restrictions

| Region | Availability |
|--------|-------------|
| **Japan** | Full access |
| **US** | Full access |
| **Most non-EU countries** | Full access |
| **EU/EEA** | NOT AVAILABLE (GDPR compliance in progress) |
| **Other regions** | May be restricted by local regulations |

### Rate Limits & Quotas

- Subscription plans have usage quotas (Standard = baseline, Pro = 10x, Max = 20x)
- Pay-as-you-go has no explicit rate limit but elastic capacity
- One verification session (6 API calls + 1 codex-fugu run) used ~18% of 5-hour quota and ~6% of weekly quota on Standard plan
- Standard plan best understood as "getting familiar as an individual" - for regular Fugu Ultra business use, Pro or higher is recommended

---

## 5. SAKANA'S OTHER PRODUCTS & RESEARCH

### Commercial Products

#### Sakana Marlin (Autonomous Research Agent)

| Attribute | Details |
|-----------|---------|
| **What** | Autonomous research assistant - "Virtual CSO" (Chief Strategy Officer) |
| **Launch** | June 15, 2026 (GA) |
| **How it works** | Input a research topic, AI autonomously researches for up to 8 hours, produces 100+ page reports with executive slides |
| **Use cases** | Strategic planning, market research, risk analysis, competitive analysis, patent landscape |
| **Pricing** | Pay-per-use: 100 credits/run at 98 JPY/credit; Pro: 150,000 JPY/month; Team: 400,000 JPY/month; Enterprise: Custom |
| **Technology** | Combines AI Scientist + AB-MCTS multi-model coordination |
| **Beta** | ~300 professionals tested from April 2026 |
| **URL** | https://sakana.ai/marlin |

#### Sakana Chat (Japanese Chat AI)

| Attribute | Details |
|-----------|---------|
| **What** | Free AI chat service optimized for Japanese users |
| **Launch** | March 24, 2026 |
| **Models** | Namazu series (alpha) - adapted from DeepSeek, Meta Llama, OpenAI models via post-training |
| **Features** | Web search integration, multiple speaking styles (Standard, Polite, Osaka dialect) |
| **Availability** | Japan only |
| **Data storage** | Google Cloud infrastructure within Japan |
| **URL** | https://chat.sakana.ai |

### Research Projects & Open Source Tools

#### The AI Scientist
- First AI system to fully automate the scientific research process
- Can perform idea generation, experimentation, paper writing
- First AI-conducted paper accepted at premier ML conference (March 2026)
- Results published in **Nature** (March 2026)
- Not a commercial product (research project)

#### ShinkaEvolve (Open Source)
- Evolutionary framework for program optimization
- Discovers new algorithms using LLMs as mutation operators
- **Apache 2.0 license** - fully open source
- Achieves SOTA circle packing with ~150 evaluations (vs thousands for prior systems)
- Code: https://github.com/SakanaAI/ShinkaEvolve
- Paper: https://arxiv.org/abs/2509.19349

#### Darwin Godel Machine (Open Source)
- Self-improving AI that rewrites its own code
- Improved SWE-bench from 20% to 50% through self-modification
- Collaboration with Jeff Clune's lab at UBC
- Cost: ~$22,000 per 80-iteration run (research prototype, not production-ready)
- Code: https://github.com/jennyzzt/dgm
- Paper: https://arxiv.org/abs/2505.22954

#### AB-MCTS (Research)
- Multiple frontier models cooperating through tree search
- Outperforms individual models on hard reasoning tasks
- Published at NeurIPS 2025 Spotlight
- Core technology behind Sakana Marlin

#### Trinity (Research - ICLR 2026)
- Evolved LLM coordinator that assigns Thinker/Worker/Verifier roles
- Set SOTA on LiveCodeBench (86.2% pass@1)
- Zero-shot transfer to unseen tasks
- Core engine powering Fugu

#### The Conductor (Research - ICLR 2026)
- 7B model trained with RL to orchestrate other LLMs
- Hit SOTA on GPQA-Diamond and LiveCodeBench by orchestrating, not solving
- Learns communication topologies and prompt engineering for worker agents
- Core engine powering Fugu

#### Namazu LLM Series
- Post-trained adaptations of open-weight frontier models for Japanese specifications
- Three variants: Namazu-DeepSeek-V3.1-Terminus, Llama-3.1-Namazu-405B, Namazu-gpt-oss-120B
- Corrects biases inherent in overseas-developed models
- Maintains frontier performance while optimizing for Japanese language/culture
- Model weights publication planned

#### TreeQuest (Open Source)
- Implementation of AB-MCTS
- Available on GitHub under Apache 2.0
- https://github.com/SakanaAI/treequest

---

## 6. OTHER JAPANESE AI COMPANIES

### Preferred Networks (PFN) - The Other Major Japanese AI Lab

| Attribute | Details |
|-----------|---------|
| **Founded** | March 2014 (Tokyo) |
| **Founders** | Toru Nishikawa (CEO), Daisuke Okanohara (COO) |
| **Focus** | Vertically integrated AI: chips -> supercomputers -> foundation models -> applications |
| **Employees** | 201-500 |
| **Key Products** | PLaMo (Japanese LLM), MN-Core AI processors, Preferred Computing Platform (PFCP) |
| **PLaMo Prime** | Japan-made LLM built from scratch, strong Japanese language performance |
| **PLaMo API** | Commercial API for PLaMo Prime |
| **Partners** | Toyota, FANUC, MUFG, SBI Group, Mitsubishi Corporation, ENEOS |
| **Supercomputer** | MN-3 (topped Green500 3x in 2020-2021 as world's most energy-efficient) |
| **Open Source** | Optuna (hyperparameter optimization), Chainer (deep learning framework - now transitioned to PyTorch), PLaMo-13B |
| **URL** | https://www.preferred.jp/en |

**PFN vs Sakana AI comparison:**

| Dimension | Sakana AI | Preferred Networks |
|-----------|-----------|-------------------|
| **Founded** | 2023 | 2014 |
| **Approach** | Nature-inspired (evolution, collective intelligence) | Vertically integrated (chips to apps) |
| **Products** | Fugu, Marlin, Chat, AI Scientist | PLaMo, MN-Core, PFCP, Optuna |
| **Valuation** | $2.6B | ~$3.5B+ (estimated) |
| **Open Source** | ShinkaEvolve, DGM, TreeQuest | Optuna, Chainer (legacy) |
| **Focus** | Multi-agent orchestration, research automation | Japanese LLM, AI chips, on-premise |
| **Hardware** | None (software-only) | Own AI processors (MN-Core) |

### Other Japanese AI Labs to Watch

1. **CyberAgent** - Large internet company with AI research division
2. **Rakuten** - Developing Rakuten AI models (Rakuten AI 3.0)
3. **NTT** - NTT Data AI, large enterprise AI solutions
4. **SoftBank** - Arm-based AI initiatives, SoftBank Vision Fund investments
5. **Toshiba / Hitachi / Fujitsu** - Enterprise AI and industrial applications
6. **ABEJA** - MLOps and AI solutions for manufacturing/retail
7. **LeapMind** - Edge AI and model compression

---

## 7. STRATEGIC IMPLICATIONS FOR CSOAI/MEOK

### Can Fugu Orchestrate CSOAI's 47 Agents?

**Direct Answer: Not directly.** Fugu is designed to orchestrate a pool of **frontier foundation models** (like GPT, Gemini, Claude, etc.), not arbitrary custom agents. It routes API calls to different LLM providers, not to custom agent frameworks.

**However, there are integration paths:**

1. **Drop-in LLM replacement:** Replace individual LLM calls in CSOAI's 47 agents with Fugu's API. Each agent gets the benefit of multi-model routing behind a single endpoint.

2. **Orchestration layer:** Use Fugu Ultra for the most complex reasoning tasks (strategic planning, analysis, decision-making) while keeping the 47-agent framework for task-specific execution.

3. **Hybrid architecture:** CSOAI's agents handle task execution; Fugu handles the reasoning/planning layer that decides which agents to call.

### API Compatibility Assessment

| Requirement | Fugu Support | Notes |
|-------------|-------------|-------|
| **OpenAI-compatible API** | Yes | Drop-in replacement |
| **Streaming responses** | Yes | |
| **Custom agent orchestration** | No | Fugu orchestrates LLMs, not custom agents |
| **Tool/function calling** | Partial | Via Responses API |
| **Japanese language** | Yes | Via Namazu models in pool |
| **High-reasoning mode** | Yes | `high`, `xhigh`/`max` effort levels |
| **Long context (1M tokens)** | Yes | |
| **Image input** | Yes | Multimodal support |

### Cost Analysis for CSOAI Scale

| Scenario | Estimated Monthly Cost |
|----------|----------------------|
| Standard subscription (individual/personal) | $20/month |
| Pro subscription (regular team use) | $100/month |
| Max subscription (power users) | $200/month |
| Production workloads (pay-as-you-go) | Variable; $5 input / $30 output per 1M tokens (Ultra) |
| CSOAI-scale (47 agents, heavy usage) | Likely $1,000-5,000+/month depending on token volume |

### The Sino-Nova Civilization Angle

Sakana AI is particularly relevant for CSOAI's Sino-Nova civilization concept because:

1. **Japanese cultural alignment:** Sakana's Namazu models are specifically adapted for Japanese language and cultural context
2. **Sovereign AI:** Japanese-developed, not subject to US or Chinese export controls
3. **Nature-inspired philosophy:** Collective intelligence mirrors the decentralized, nature-inspired ethos of Sino-Nova
4. **Multi-agent philosophy:** Fugu's "swarm intelligence" approach aligns with CSOAI's 47-agent architecture
5. **Partnership potential:** Sakana works with Japanese enterprises and government; natural partner for a Japan-inspired civilization framework

### Key Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| **EU unavailability** | GDPR compliance pending | Not relevant if operating from US/Asia |
| **Proprietary routing** | Cannot see which models are called | Acceptable for most use cases; opt-out available for compliance |
| **High latency (Ultra)** | 11 seconds to 4+ hours for complex tasks | Use Fugu standard for interactive; Ultra for batch/deep reasoning |
| **Token cost (Ultra)** | $35/1M tokens total is expensive | Use subscription for predictable costs; standard Fugu for routine tasks |
| **New product** | Only launched June 2026 | Beta tested with 500+ users; strong benchmark validation |
| **Training data opt-in** | Default ON for training data usage | Opt out via console before serious use |

### Recommended Integration Strategy

1. **Phase 1 (Immediate):** Sign up for Standard plan ($20/month), test Fugu and Fugu Ultra with CSOAI's existing workflows
2. **Phase 2:** Integrate Fugu API as a reasoning backend for the most complex agents in the 47-agent system
3. **Phase 3:** Use Fugu Ultra for strategic planning tasks (replaces need for Fable 5/Mythos 5)
4. **Phase 4:** Evaluate Sakana Marlin for autonomous research tasks within the civilization framework

---

## SUMMARY: THE COMPLETE PICTURE

### For Nick (who saw the TikTok about "Japanese Mythos 5"):

**There is NO "Japanese Mythos 5."** Here's what actually exists:

| What was claimed | What it actually is |
|-----------------|-------------------|
| "Japanese Mythos 5" | **Mythos 5** = Anthropic's (US) banned model |
| "Sakana Fugu" | **Fugu** = Sakana AI's (Japan) multi-agent orchestration system |
| Confusion on TikTok | People conflated Fugu's performance claims with Mythos's name |

**The real story:**
1. Anthropic (US) built Fable 5 and Mythos 5 - super powerful AI models
2. US government banned them on June 12, 2026 (export controls)
3. Sakana AI (Japan) launched Fugu on June 22, 2026 - a different approach that achieves similar/better performance by orchestrating multiple models
4. Fugu is NOT a version of Mythos - it's a completely different system from a different country
5. The "Japanese Mythos 5" confusion is like calling a Honda "a Japanese Ford Mustang" - they're different products from different companies

### The Bottom Line

**Sakana Fugu is a real, available, powerful alternative to the banned Anthropic models.** It offers:
- Frontier-level performance (matching Fable 5 on benchmarks)
- No export control risk (swappable multi-model pool)
- OpenAI-compatible API (easy integration)
- Japanese company (sovereign AI advantage)
- Reasonable pricing ($20-200/month subscription, or $5/$30 per 1M tokens)

**Sakana AI is Japan's most valuable AI startup ($2.6B valuation), founded by ex-Google DeepMind researchers, and Fugu is their flagship international commercial product.**

---

## APPENDIX: RESOURCES

### Sakana AI Links
- **Main site:** https://sakana.ai
- **Fugu product:** https://sakana.ai/fugu
- **Fugu console:** https://console.sakana.ai
- **Fugu pricing:** https://console.sakana.ai/pricing
- **Fugu get started:** https://console.sakana.ai/get-started
- **Marlin product:** https://sakana.ai/marlin
- **Sakana Chat:** https://chat.sakana.ai
- **GitHub:** https://github.com/SakanaAI
- **ShinkaEvolve:** https://sakana.ai/shinka-evolve
- **Darwin Godel Machine:** https://sakana.ai/dgm
- **TRINITY paper:** https://arxiv.org/abs/2512.04695
- **Conductor paper:** https://arxiv.org/abs/2512.04388
- **Technical report:** https://github.com/SakanaAI/fugu/blob/main/Fugu_technical_report.pdf

### Preferred Networks Links
- **Main site:** https://www.preferred.jp/en
- **PLaMo:** https://www.preferred.jp/en/business/genai

### News Sources
- VentureBeat Fugu launch: https://venturebeat.com/orchestration/sakana-fugu
- AI-News Fugu analysis: https://www.artificialintelligence-news.com/news/sakana-ai-fugu
- MarkTechPost Fugu launch: https://www.marktechpost.com/2026/06/22/sakana-ai-launches-sakana-fugu
- Classmethod Fugu first-touch (Japanese): https://dev.classmethod.jp/en/articles/sakana-fugu-ga-first-touch/
- Fortune Anthropic export controls: https://fortune.com/2026/06/13/anthropic-fable-mythos-export-controls
- Business Insider Anthropic ban: https://www.businessinsider.com/anthropic-fable-mythos-export-control-2026-6
- Cobo export controls analysis: https://www.cobo.com/agentic-wallet/news/us-ai-export-controls
- TIME100 David Ha: https://time.com/collections/time100-ai-2025/7305851/david-ha/
- Nikkei Sakana unicorn: https://asia.nikkei.com/business/technology/artificial-intelligence/sakana-ai-takes-crown-as-japan-s-most-valuable-unicorn
