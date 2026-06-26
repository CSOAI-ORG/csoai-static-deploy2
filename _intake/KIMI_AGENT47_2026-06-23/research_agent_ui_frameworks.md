# AI Agent UI Frameworks & Frontend Tools Research
## For MEOK's 47-Agent Dashboard — July 2026

---

## 1. shadcn/agentcn (agentcn.run)

### GitHub Stats
| Metric | Value |
|--------|-------|
| **Repository** | `github.com/shadcn-labs/agentcn` |
| **Website** | https://agentcn.run |
| **Stars** | ~208 (very new, launched June 2026) |
| **License** | MIT |
| **Forks** | 9 |
| **Contributors** | 2 (Aniket Pawar, Claude) |
| **Commits** | 38 (as of June 22, 2026) |
| **Last Commit** | 19 hours ago (actively developed) |
| **Languages** | TypeScript 80.5%, MDX 14.8%, CSS 3.8% |

### What It Actually Is
**agentcn is NOT a UI component library** — it is a **registry of pre-built agent recipes** distributed via the shadcn CLI. Think of it as "shadcn/ui, but for agents" — complete agent implementations (not UI widgets) that you install with one command.

Each "component" is a **full agent recipe**: instructions, tools, skills, and workflows that you can drop into your project.

### Available Agent Recipes (NOT UI Components)

The following are **complete AI agents**, not UI components:

| Agent Recipe | Description | Install Command |
|-------------|-------------|-----------------|
| Deep Search | Researches questions, evaluates findings, iterates | `npx shadcn add @agentcn/eve/deep-search` |
| CSV to Questions | Summarizes CSVs, generates analytical questions | `npx shadcn add @agentcn/eve/csv-to-questions` |
| Feedback Summary | Categorizes customer feedback into executive reports | `npx shadcn add @agentcn/eve/feedback-summary` |
| Meeting Notes | Transcribes meetings to structured summaries | `npx shadcn add @agentcn/eve/meeting-notes` |
| Chat with PDF | RAG over PDFs with page citations | `npx shadcn add @agentcn/eve/chat-with-pdf` |
| Flash Cards from PDF | Converts PDFs to study flash cards | `npx shadcn add @agentcn/eve/flashcards-pdf` |
| Chat with YouTube | Answers questions from YouTube transcripts | `npx shadcn add @agentcn/eve/chat-with-youtube` |
| Docs Chatbot | Answers questions about library documentation | `npx shadcn add @agentcn/eve/docs-chatbot` |
| Chat with Database | SQL generation from natural language | `npx shadcn add @agentcn/eve/text-to-sql` |
| GitHub PR Review | Adaptive file-by-file code review | `npx shadcn add @agentcn/eve/github-review` |
| Slack Agent | Responds to Slack mentions/DMs | `npx shadcn add @agentcn/eve/slack-agent` |
| Google Sheets | Reads/analyzes/edits Google Sheets | `npx shadcn add @agentcn/eve/google-sheets` |
| Weather | Weather lookup via Open-Meteo API | `npx shadcn add @agentcn/eve/weather` |
| Docs Expert | Web search + citation for library questions | `npx shadcn add @agentcn/eve/docs-expert` |
| Claw Assistant | Sandboxed workspace file/shell operations | `npx shadcn add @agentcn/eve/claw` |
| Browser Agent | Playwright-driven browser automation | `npx shadcn add @agentcn/eve/browser-agent` |
| Company Knowledge | Internal document RAG with PII redaction | `npx shadcn add @agentcn/eve/company-knowledge` |

### Key Insight for MEOK
> **agentcn does NOT provide UI components** like agent lists, sidebars, chat interfaces, status indicators, or voting UIs. It provides **pre-built agent implementations** that you can use as templates for building your 47 MEOK agents. The UI must be built separately using shadcn/ui components + Vercel AI SDK.

### Installation (Quick Start)
```bash
# Add a specific agent recipe to your project
npx shadcn add @agentcn/eve/deep-search

# Or install manually
pnpm dlx shadcn add @agentcn/eve/chat-with-youtube
```

### Integration into React Project
```bash
# Step 1: Initialize shadcn/ui in your project
npx shadcn@latest init

# Step 2: Add shadcn/ui components you need for the dashboard
npx shadcn@latest add button card badge sidebar avatar \
  table tabs scroll-area input textarea select \
  switch dialog dropdown-menu tooltip progress

# Step 3: Add an agentcn agent recipe
npx shadcn add @agentcn/eve/chat-with-database

# Step 4: Install AI SDK for streaming
npm install ai @ai-sdk/react

# Step 5: Add your own agent configs in .agents/skills/
```

### How to Customize for MEOK's 47 Agents
```typescript
// Each MEOK agent follows this pattern:
// 1. Create agent skill files in .agents/skills/
// 2. Define the agent's tools in a tools/ directory
// 3. Register via the shadcn registry format

// Example: Registry entry for a MEOK Compliance Agent
// registry/compliance-agent.json
{
  "name": "meok-compliance-agent",
  "type": "registry:block",
  "title": "MEOK Compliance Agent",
  "description": "Monitors regulatory compliance across all 47 agents",
  "files": [
    {
      "path": "agents/compliance.ts",
      "type": "registry:file",
      "target": ".agents/skills/compliance.md"
    },
    {
      "path": "tools/compliance-check.ts",
      "type": "registry:file",
      "target": "tools/compliance-check.ts"
    }
  ]
}
```

### Bottom Line Assessment
| Criterion | Rating | Notes |
|-----------|--------|-------|
| **UI Components for Agent Dashboard** | Not applicable | This is NOT a UI library |
| **Agent Recipes/Templates** | Excellent | 18+ ready-to-use agents |
| **MEOK Agent List View** | Not provided | Build with shadcn/ui Table |
| **MEOK Chat Interface** | Not provided | Build with Vercel AI SDK |
| **MEOK Voting UI** | Not provided | Custom build |
| **Production Readiness** | Early (208 stars) | Very new, but from shadcn-labs |
| **TypeScript Support** | Excellent | 100% TypeScript |
| **Community** | Small but growing | Active development |

---

## 2. Mastra (mastra.ai)

### GitHub Stats
| Metric | Value |
|--------|-------|
| **Repository** | `github.com/mastra-ai/mastra` |
| **Website** | https://mastra.ai |
| **Stars** | 22,276+ (growing ~30-35/day) |
| **License** | Apache 2.0 |
| **Forks** | 1,779 |
| **Contributors** | 300+ |
| **Weekly npm downloads** | 300,000+ |
| **Last Stable Release** | Mastra 1.0 (January 2026) |
| **Funding** | $13M seed (Oct 2025), YC W25 |
| **Founded** | October 2024 |

### Who Built It
- **Sam Bhagwat** (CEO) — Co-founded Gatsby.js
- **Abhi Aiyer** (CTO) — Principal Engineer at Gatsby/Netlify
- **Shane Thomas** (CPO) — Staff Engineer at Gatsby/Netlify
- All three previously built Gatsby.js (acquired by Netlify)
- Y Combinator W25 batch

### What It Is
**Mastra is a TypeScript-native AI agent framework** — the most comprehensive TypeScript-first framework for building production AI agents. It provides:

| Feature | Description |
|---------|-------------|
| **Agents** | Autonomous agents with tool access, reasoning, and iteration |
| **Workflows** | Durable graph-based state machines with branching, loops, human-in-the-loop |
| **RAG** | Full retrieval pipeline: chunking, embedding, vector search, reranking |
| **Memory** | Conversation history, semantic recall, working memory, observational memory (94.87% LongMemEval) |
| **Evals** | Model-graded, rule-based, statistical evaluation |
| **MCP Support** | Model Context Protocol for external tool ecosystems |
| **Mastra Studio** | Local dev UI at localhost:4111 — chat with agents, inspect tool calls, view memory |
| **Multi-agent** | Supervisor pattern for orchestrating specialized sub-agents |
| **Observability** | Built-in tracing, export to LangSmith/Langfuse/Datadog |

### Quick Start
```bash
# Create a new Mastra project
npm create mastra@latest meok-orchestrator \
  --components agents,workflows,memory \
  --llm openai

cd meok-orchestrator

# Add API key
echo "OPENAI_API_KEY=your-key" >> .env

# Start the dev server with Studio
npm run dev  # Studio at http://localhost:4111
```

### Using Mastra for MEOK Agent Orchestration
```typescript
// src/mastra/agents/meok-agents.ts
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

// Define a tool for checking agent compliance
const complianceCheckTool = createTool({
  id: "compliance-check",
  description: "Check compliance status of a MEOK agent",
  inputSchema: z.object({
    agentId: z.string(),
    checkType: z.enum(["gdpr", "sebi", "aml", "kyc"]),
  }),
  execute: async ({ context }) => {
    // Check agent compliance in your system
    return { status: "compliant", lastAudit: "2026-07-01" };
  },
});

// Define a tool for BFT voting
const bftVoteTool = createTool({
  id: "bft-vote",
  description: "Cast a vote in the BFT Council",
  inputSchema: z.object({
    agentId: z.string(),
    proposalId: z.string(),
    vote: z.enum(["yes", "no", "abstain"]),
  }),
  execute: async ({ context }) => {
    // Record vote on the BFT consensus mechanism
    return { voteRecorded: true, timestamp: new Date().toISOString() };
  },
});

// Create the MEOK orchestrator agent
export const meokOrchestrator = new Agent({
  name: "MEOK Orchestrator",
  instructions: `
    You are the central orchestrator for MEOK's 47-agent system.
    You coordinate between specialized agents:
    - 12 Compliance Agents (GDPR, SEBI, AML, KYC monitoring)
    - 8 Trading Agents (execution, risk management)
    - 10 Data Agents (market data, sentiment analysis)
    - 7 Infrastructure Agents (DevOps, security)
    - 10 Analytics Agents (reporting, forecasting)
    Use the BFT Council for consensus decisions.
    Check pheromone matrix for agent coordination signals.
  `,
  model: "openai/gpt-5.4",
  tools: { complianceCheckTool, bftVoteTool },
});
```

### Mastra + React Frontend Integration
```typescript
// src/mastra/index.ts - Backend
import { Mastra } from "@mastra/core/mastra";
import { chatRoute } from "@mastra/ai-sdk";
import { meokOrchestrator } from "./agents/meok-agents";

export const mastra = new Mastra({
  agents: { meokOrchestrator },
  server: {
    apiRoutes: [
      chatRoute({
        path: "/chat/:agentId?",
        agent: "meokOrchestrator",
      }),
    ],
  },
});
```

```tsx
// frontend/components/MeokChat.tsx - Frontend
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport } from "ai";

export function MeokChat() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({
      api: "http://localhost:4111/chat",
    }),
  });

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`p-3 rounded-lg ${
            msg.role === "user" ? "bg-blue-100 ml-auto" : "bg-gray-100"
          } max-w-[80%]`}>
            {msg.parts?.map((part, i) => (
              part.type === "text" ? <span key={i}>{part.text}</span> : null
            ))}
          </div>
        ))}
      </div>
      <form onSubmit={(e) => {
        e.preventDefault();
        const input = e.currentTarget.elements.namedItem("msg") as HTMLInputElement;
        sendMessage({ text: input.value });
        input.value = "";
      }}>
        <input name="msg" placeholder="Command MEOK..." className="w-full p-3 border" />
      </form>
    </div>
  );
}
```

### Comparison to Other Frameworks

| Dimension | Mastra | LangChain/LangGraph | CrewAI | AutoGen |
|-----------|--------|---------------------|--------|---------|
| **Language** | TypeScript-native | Python-first, TS lags | Python-only | Python/.NET |
| **Stars** | 22K+ | 126K+ | 44K+ | 54K+ (maintenance) |
| **Setup Time** | Minutes | Hours | Minutes | Hours |
| **Memory System** | Built-in (4 types) | LangSmith (separate) | Basic | Basic |
| **Dev Studio** | Mastra Studio (built-in) | LangSmith (paid) | None | AutoGen Studio |
| **Best For** | TypeScript teams, web apps | Python teams, ML pipelines | Role-based collaboration | Research (deprecated) |
| **MEOK Fit** | Excellent (TypeScript + web) | Poor (Python mismatch) | Moderate (role-based fits) | Poor (deprecated) |

### When to Use Mastra for MEOK
- **Primary recommendation**: Use Mastra as the **backend orchestration layer** for MEOK's 47 agents
- Mastra handles: agent logic, memory, workflows, RAG, tool calling, observability
- Combine with: React + shadcn/ui for frontend + Vercel AI SDK for streaming

---

## 3. Vercel AI SDK (ai-sdk.dev)

### GitHub Stats
| Metric | Value |
|--------|-------|
| **Repository** | `github.com/vercel/ai` |
| **Website** | https://ai-sdk.dev |
| **Latest Version** | **AI SDK 6.x** (December 2025) |
| **License** | Open Source (free) |
| **Weekly npm downloads** | 1.8M+ |
| **Backed by** | Vercel |

### Three-Layer Architecture

```
AI SDK Core (server)     → generateText, streamText, generateObject, embed
    ↓
AI SDK UI (client)       → useChat, useCompletion, useObject
    ↓
AI SDK RSC (server)      → streamUI, createStreamableUI
```

### Key Features in v6
| Feature | Description |
|---------|-------------|
| **Server Actions** | Native React Server Actions replace API routes |
| **useChat hook** | Full chat lifecycle: messages, streaming, errors |
| **useAgent** | Agent-specific hook for tool-calling agents |
| **Streaming** | Real-time token streaming with `streamText()` |
| **Multi-provider** | 25+ providers: OpenAI, Anthropic, Google, xAI, Mistral |
| **Zod 4 integration** | Type-safe structured output |
| **Tool calling** | Multi-step tool execution with typed parameters |
| **AI Elements** | Pre-built UI components for agent interfaces |

### How to Stream Agent Responses
```tsx
// app/actions/chat.ts — Server Action
"use server";
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";
import type { CoreMessage } from "ai";

export async function chat(messages: CoreMessage[]) {
  const result = streamText({
    model: openai("gpt-5.4"),
    system: "You are the MEOK orchestrator managing 47 specialized agents.",
    messages,
    tools: {
      checkAgentStatus: {
        description: "Check status of a MEOK agent",
        parameters: z.object({ agentId: z.string() }),
        execute: async ({ agentId }) => {
          return await getAgentStatus(agentId); // your function
        },
      },
    },
  });
  return result.toDataStream();
}
```

```tsx
// components/AgentChat.tsx — Client Component
"use client";
import { useChat } from "ai/react";
import { chat } from "@/app/actions/chat";

export function AgentChat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: chat, // Direct Server Action — no HTTP route needed
  });

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[80%] p-3 rounded-lg ${
              msg.role === "user" ? "bg-blue-600 text-white" : "bg-gray-100"
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && <div className="text-gray-400">Agent is thinking...</div>}
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={handleInputChange}
            placeholder="Send command to MEOK agents..."
            className="flex-1 border rounded-lg px-4 py-2"
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading} className="bg-zinc-900 text-white px-6 py-2 rounded-lg">
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
```

### How to Display Multi-Agent Conversations
```tsx
// Multi-agent conversation display
import { useChat } from "ai/react";

interface AgentMessage {
  id: string;
  role: "user" | "agent";
  agentId?: string;
  agentName?: string;
  content: string;
  timestamp: string;
  toolCalls?: Array<{ tool: string; input: unknown; output: unknown }>;
}

export function MultiAgentConversation({ messages }: { messages: AgentMessage[] }) {
  const agentColors: Record<string, string> = {
    compliance: "bg-green-100 border-green-300",
    trading: "bg-blue-100 border-blue-300",
    data: "bg-purple-100 border-purple-300",
    infra: "bg-orange-100 border-orange-300",
    analytics: "bg-pink-100 border-pink-300",
  };

  return (
    <div className="space-y-3">
      {messages.map((msg) => (
        <div key={msg.id} className={`p-3 rounded-lg border ${
          agentColors[msg.agentId?.split("-")[0] || "default"]
        }`}>
          <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
            <span className="font-semibold">{msg.agentName || msg.role}</span>
            <span>·</span>
            <span>{msg.timestamp}</span>
          </div>
          <div className="text-sm">{msg.content}</div>
          {msg.toolCalls?.map((tc, i) => (
            <div key={i} className="mt-2 p-2 bg-white/50 rounded text-xs font-mono">
              Tool: {tc.tool}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
```

### Free Tier Limits
| Provider | Free Tier | Notes |
|----------|-----------|-------|
| Vercel AI SDK | Unlimited (open source) | SDK is free; you pay for model usage |
| Vercel AI Gateway | 1M tokens/month free | Then $0.50 per 1M tokens |
| Vercel Hosting | Hobby tier: free | 100GB bandwidth, 10s serverless functions |

---

## 4. Other UI Frameworks Comparison

### Framework Matrix for MEOK

| Framework | Stars | Language | UI Type | Best For | MEOK Fit |
|-----------|-------|----------|---------|----------|----------|
| **Dify** | 138K+ | Python/JS | Visual Builder | Complete AI app builder | Moderate |
| **Open WebUI** | 142K+ | Python | Chat Interface | Local/self-hosted model UI | Low |
| **Flowise** | 47K+ | JS/TS | Visual Builder | LangChain visual workflows | Low |
| **AutoGen Studio** | 54K (deprecated) | Python | Prototyping UI | Research (maintenance mode) | Poor |
| **CrewAI** | 44K+ | Python | None (code-only) | Role-based multi-agent teams | Moderate |
| **LangChain.js** | 126K+ | JS/TS | None (code-only) | Maximum flexibility | Good (with custom UI) |

### Detailed Analysis

#### Dify (138K+ stars) — Complete AI App Builder
```bash
# Docker Compose setup
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d
# Access at http://localhost/install
```
- **Best for**: Teams that want a visual drag-and-drop AI app builder
- **Agent support**: ReAct + Function Calling, 50+ built-in tools
- **RAG**: Production-ready pipeline, built-in
- **MEOK Fit**: Low — Dify is opinionated and designed for chatbots/workflows, not custom multi-agent dashboards with voting UIs
- **License**: Dify Open Source License (Apache 2.0-based with commercial conditions)

#### Open WebUI (142K+ stars) — Chat Interface for Local Models
```bash
# Docker install
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```
- **Best for**: Self-hosted chat interface for Ollama/OpenAI models
- **Features**: PWA support, RAG, multi-model chats, voice, channels
- **MEOK Fit**: Low — designed for chat, not agent orchestration dashboards
- **License**: MIT

#### Flowise (47K+ stars) — Visual Agent Builder
```bash
npm install -g flowise
npx flowise start
# Open http://localhost:3000
```
- **Best for**: No-code LangChain workflow builder
- **MEOK Fit**: Low — visual builder, not a programmable dashboard
- **Status**: Acquired by Workday (August 2025)
- **License**: Apache 2.0

#### AutoGen / Microsoft Agent Framework
```bash
pip install -U autogenstudio
autogenstudio ui --port 8080
```
- **Status**: AutoGen is in maintenance mode (October 2025)
- **Replacement**: Microsoft Agent Framework (built on Semantic Kernel)
- **MEOK Fit**: Poor — Python-based, research-oriented, not for production web UIs

#### CrewAI (44K+ stars) — Role-Based Multi-Agent
```bash
pip install crewai
```
- **Best for**: Python teams building role-based agent crews
- **MEOK Fit**: Moderate — The role-based pattern fits MEOK's 47 agents well, but requires Python backend + separate frontend
- **License**: MIT

### Which Is Best for MEOK?

**Recommended Stack**: Mastra (backend) + React + shadcn/ui + Vercel AI SDK (frontend)

Rationale:
1. **TypeScript-native**: Full type safety across frontend and backend
2. **MEOK's 47 agents**: Mastra's supervisor pattern + memory + workflows fit perfectly
3. **Custom UI**: MEOK needs bespoke components (voting UI, pheromone matrix, compliance dashboard) — no off-the-shelf solution provides these
4. **Streaming**: Vercel AI SDK provides best-in-class streaming for agent responses
5. **Caravan-friendly**: PWA approach works offline with Mastra's local server

---

## 5. MEOK Dashboard Design

### Required Components (Custom — None Exist Off-the-Shelf)

#### 5.1 Agent Roster (47 Agents, Filterable)
```tsx
// components/meok/AgentRoster.tsx
import { useState } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface MeokAgent {
  id: string;
  name: string;
  role: "compliance" | "trading" | "data" | "infrastructure" | "analytics";
  status: "active" | "idle" | "error" | "paused";
  lastActivity: string;
  complianceScore: number;
  tasksCompleted: number;
}

const AGENTS: MeokAgent[] = [
  // 12 Compliance Agents
  { id: "compliance-01", name: "GDPR Guardian", role: "compliance", status: "active", lastActivity: "2s ago", complianceScore: 98, tasksCompleted: 1247 },
  { id: "compliance-02", name: "SEBI Sentinel", role: "compliance", status: "active", lastActivity: "5s ago", complianceScore: 97, tasksCompleted: 983 },
  // ... 45 more agents
];

export function AgentRoster() {
  const [filter, setFilter] = useState("");
  const [roleFilter, setRoleFilter] = useState<string>("all");

  const filtered = AGENTS.filter((a) => {
    const matchesSearch = a.name.toLowerCase().includes(filter.toLowerCase());
    const matchesRole = roleFilter === "all" || a.role === roleFilter;
    return matchesSearch && matchesRole;
  });

  const statusColor = (status: string) => {
    switch (status) {
      case "active": return "bg-green-500";
      case "idle": return "bg-yellow-500";
      case "error": return "bg-red-500";
      case "paused": return "bg-gray-400";
      default: return "bg-gray-400";
    }
  };

  return (
    <Card className="w-full">
      <CardHeader className="space-y-2">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold">MEOK Agent Roster (47)</h2>
          <Badge variant="outline">{filtered.length} agents</Badge>
        </div>
        <div className="flex gap-2">
          <Input
            placeholder="Search agents..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="flex-1"
          />
          <Select value={roleFilter} onValueChange={setRoleFilter}>
            <SelectTrigger className="w-[140px]">
              <SelectValue placeholder="All Roles" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Roles</SelectItem>
              <SelectItem value="compliance">Compliance (12)</SelectItem>
              <SelectItem value="trading">Trading (8)</SelectItem>
              <SelectItem value="data">Data (10)</SelectItem>
              <SelectItem value="infrastructure">Infra (7)</SelectItem>
              <SelectItem value="analytics">Analytics (10)</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {filtered.map((agent) => (
            <div key={agent.id} className="p-3 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-2 h-2 rounded-full ${statusColor(agent.status)}`} />
                <span className="font-medium text-sm">{agent.name}</span>
                <Badge variant="outline" className="text-xs ml-auto">{agent.role}</Badge>
              </div>
              <div className="text-xs text-gray-500 space-y-1">
                <div>Score: {agent.complianceScore}% | Tasks: {agent.tasksCompleted}</div>
                <div>Last: {agent.lastActivity}</div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
```

#### 5.2 BFT Council Voting Interface
```tsx
// components/meok/BftVotingPanel.tsx
import { useState } from "react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

interface BftProposal {
  id: string;
  title: string;
  description: string;
  status: "open" | "closed" | "executing";
  votes: { yes: number; no: number; abstain: number };
  quorum: number;
  deadline: string;
}

export function BftVotingPanel({ proposal }: { proposal: BftProposal }) {
  const totalVotes = proposal.votes.yes + proposal.votes.no + proposal.votes.abstain;
  const yesPercent = totalVotes > 0 ? (proposal.votes.yes / totalVotes) * 100 : 0;
  const noPercent = totalVotes > 0 ? (proposal.votes.no / totalVotes) * 100 : 0;
  const quorumMet = totalVotes >= proposal.quorum;

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold">{proposal.title}</h3>
            <p className="text-sm text-gray-500">{proposal.description}</p>
          </div>
          <Badge variant={proposal.status === "open" ? "default" : "secondary"}>
            {proposal.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-green-600">Yes: {proposal.votes.yes}</span>
            <span>{yesPercent.toFixed(1)}%</span>
          </div>
          <Progress value={yesPercent} className="bg-gray-200" />

          <div className="flex justify-between text-sm">
            <span className="text-red-600">No: {proposal.votes.no}</span>
            <span>{noPercent.toFixed(1)}%</span>
          </div>
          <Progress value={noPercent} className="bg-gray-200" />

          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Abstain: {proposal.votes.abstain}</span>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Total: {totalVotes}/47 agents</span>
          <span>Quorum: {proposal.quorum} {quorumMet ? "(met)" : "(pending)"}</span>
          <span>Ends: {proposal.deadline}</span>
        </div>

        {proposal.status === "open" && (
          <div className="flex gap-2">
            <Button variant="default" className="flex-1 bg-green-600 hover:bg-green-700">
              Vote Yes
            </Button>
            <Button variant="default" className="flex-1 bg-red-600 hover:bg-red-700">
              Vote No
            </Button>
            <Button variant="outline" className="flex-1">
              Abstain
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

#### 5.3 Pheromone Matrix Visualization
```tsx
// components/meok/PheromoneMatrix.tsx
import { useMemo } from "react";

interface PheromoneSignal {
  from: string;
  to: string;
  strength: number; // 0-1
  type: "task" | "alert" | "data" | "sync";
}

export function PheromoneMatrix({ signals }: { signals: PheromoneSignal[] }) {
  const agentIds = useMemo(() => {
    const ids = new Set<string>();
    signals.forEach((s) => { ids.add(s.from); ids.add(s.to); });
    return Array.from(ids).sort();
  }, [signals]);

  const matrix = useMemo(() => {
    const m: Record<string, Record<string, PheromoneSignal[]>> = {};
    agentIds.forEach((id) => { m[id] = {}; agentIds.forEach((j) => { m[id][j] = []; }); });
    signals.forEach((s) => { m[s.from][s.to].push(s); });
    return m;
  }, [signals, agentIds]);

  const typeColor = (type: string) => {
    switch (type) {
      case "task": return "#3b82f6"; // blue
      case "alert": return "#ef4444"; // red
      case "data": return "#8b5cf6"; // purple
      case "sync": return "#10b981"; // green
      default: return "#9ca3af";
    }
  };

  const cellSize = 24;

  return (
    <div className="overflow-x-auto">
      <svg
        width={(agentIds.length + 1) * cellSize}
        height={(agentIds.length + 1) * cellSize}
        className="mx-auto"
      >
        {/* Column headers */}
        {agentIds.map((id, i) => (
          <text key={`col-${id}`} x={(i + 1) * cellSize + cellSize / 2} y={12} fontSize="8" textAnchor="middle">
            {id.slice(0, 4)}
          </text>
        ))}
        {/* Row headers */}
        {agentIds.map((id, i) => (
          <text key={`row-${id}`} x={cellSize - 4} y={(i + 1) * cellSize + cellSize / 2 + 3} fontSize="8" textAnchor="end">
            {id.slice(0, 4)}
          </text>
        ))}
        {/* Matrix cells */}
        {agentIds.map((fromId, i) =>
          agentIds.map((toId, j) => {
            const sigs = matrix[fromId][toId];
            const maxStrength = sigs.length > 0 ? Math.max(...sigs.map((s) => s.strength)) : 0;
            const dominantType = sigs.length > 0
              ? sigs.sort((a, b) => b.strength - a.strength)[0].type
              : null;
            return (
              <rect
                key={`${fromId}-${toId}`}
                x={(j + 1) * cellSize}
                y={(i + 1) * cellSize}
                width={cellSize - 1}
                height={cellSize - 1}
                fill={dominantType ? typeColor(dominantType) : "#f3f4f6"}
                opacity={maxStrength > 0 ? 0.2 + maxStrength * 0.8 : 1}
                rx={2}
              />
            );
          })
        )}
      </svg>
      <div className="flex gap-4 justify-center mt-2 text-xs">
        {["task", "alert", "data", "sync"].map((type) => (
          <div key={type} className="flex items-center gap-1">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: typeColor(type) }} />
            <span className="capitalize">{type}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

#### 5.4 Town Map (Circuit Pyramid View)
```tsx
// components/meok/TownMap.tsx
// A hierarchical visualization of MEOK agents in a pyramid/circuit layout
import { useState } from "react";

interface TownNode {
  id: string;
  name: string;
  level: number; // 0 = apex (orchestrator), 1 = layer 1, etc.
  x: number;     // 0-1 normalized position
  status: "active" | "idle" | "error";
  children?: string[];
}

const TOWN_NODES: TownNode[] = [
  { id: "orchestrator", name: "MEOK Core", level: 0, x: 0.5, status: "active", children: ["compliance-hub", "trading-hub", "data-hub", "infra-hub", "analytics-hub"] },
  { id: "compliance-hub", name: "Compliance", level: 1, x: 0.1, status: "active", children: ["compliance-01", "compliance-02", "compliance-03"] },
  { id: "trading-hub", name: "Trading", level: 1, x: 0.3, status: "active", children: ["trading-01", "trading-02"] },
  { id: "data-hub", name: "Data", level: 1, x: 0.5, status: "active", children: ["data-01", "data-02", "data-03"] },
  { id: "infra-hub", name: "Infra", level: 1, x: 0.7, status: "active", children: ["infra-01", "infra-02"] },
  { id: "analytics-hub", name: "Analytics", level: 1, x: 0.9, status: "active", children: ["analytics-01", "analytics-02", "analytics-03"] },
  { id: "compliance-01", name: "GDPR", level: 2, x: 0.05, status: "active" },
  { id: "compliance-02", name: "SEBI", level: 2, x: 0.1, status: "active" },
  { id: "compliance-03", name: "AML", level: 2, x: 0.15, status: "idle" },
  { id: "trading-01", name: "Execution", level: 2, x: 0.28, status: "active" },
  { id: "trading-02", name: "Risk", level: 2, x: 0.32, status: "active" },
  { id: "data-01", name: "Market", level: 2, x: 0.48, status: "active" },
  { id: "data-02", name: "Sentiment", level: 2, x: 0.52, status: "error" },
  { id: "data-03", name: "ESG", level: 2, x: 0.56, status: "active" },
  { id: "infra-01", name: "Security", level: 2, x: 0.68, status: "active" },
  { id: "infra-02", name: "DevOps", level: 2, x: 0.72, status: "active" },
  { id: "analytics-01", name: "Forecast", level: 2, x: 0.88, status: "active" },
  { id: "analytics-02", name: "Reporting", level: 2, x: 0.92, status: "idle" },
  { id: "analytics-03", name: "Backtest", level: 2, x: 0.96, status: "active" },
];

export function TownMap() {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const statusColor = (status: string) => {
    switch (status) {
      case "active": return "#22c55e";
      case "idle": return "#eab308";
      case "error": return "#ef4444";
      default: return "#9ca3af";
    }
  };

  const levels = 3;
  const levelHeight = 120;

  return (
    <div className="w-full overflow-x-auto">
      <svg viewBox="0 0 600 360" className="w-full max-w-3xl mx-auto">
        {/* Connection lines */}
        {TOWN_NODES.map((node) =>
          node.children?.map((childId) => {
            const child = TOWN_NODES.find((n) => n.id === childId);
            if (!child) return null;
            return (
              <line
                key={`${node.id}-${childId}`}
                x1={node.x * 600}
                y1={node.level * levelHeight + 40}
                x2={child.x * 600}
                y2={child.level * levelHeight + 20}
                stroke="#d1d5db"
                strokeWidth="1"
                strokeDasharray="4 2"
              />
            );
          })
        )}
        {/* Nodes */}
        {TOWN_NODES.map((node) => (
          <g
            key={node.id}
            onClick={() => setSelectedNode(node.id)}
            className="cursor-pointer"
          >
            <circle
              cx={node.x * 600}
              cy={node.level * levelHeight + 30}
              r={node.level === 0 ? 20 : 14}
              fill={statusColor(node.status)}
              stroke={selectedNode === node.id ? "#1f2937" : "#fff"}
              strokeWidth={selectedNode === node.id ? 3 : 2}
            />
            <text
              x={node.x * 600}
              y={node.level * levelHeight + 60}
              textAnchor="middle"
              fontSize="10"
              fill="#374151"
            >
              {node.name}
            </text>
            {node.level === 0 && (
              <text
                x={node.x * 600}
                y={node.level * levelHeight + 75}
                textAnchor="middle"
                fontSize="9"
                fill="#6b7280"
              >
                47 agents
              </text>
            )}
          </g>
        ))}
      </svg>
    </div>
  );
}
```

#### 5.5 Compliance Status Dashboard
```tsx
// components/meok/ComplianceDashboard.tsx
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

interface ComplianceMetric {
  regulation: string;
  score: number;
  status: "passing" | "warning" | "critical";
  lastCheck: string;
  agents: number;
}

const COMPLIANCE_DATA: ComplianceMetric[] = [
  { regulation: "GDPR", score: 98, status: "passing", lastCheck: "2m ago", agents: 47 },
  { regulation: "SEBI", score: 95, status: "passing", lastCheck: "5m ago", agents: 47 },
  { regulation: "AML", score: 87, status: "warning", lastCheck: "10m ago", agents: 45 },
  { regulation: "KYC", score: 99, status: "passing", lastCheck: "1m ago", agents: 47 },
  { regulation: "MiFID II", score: 72, status: "critical", lastCheck: "1h ago", agents: 38 },
  { regulation: "Basel III", score: 91, status: "passing", lastCheck: "15m ago", agents: 42 },
];

export function ComplianceDashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {COMPLIANCE_DATA.map((metric) => (
        <Card key={metric.regulation} className={
          metric.status === "critical" ? "border-red-400" :
          metric.status === "warning" ? "border-yellow-400" : ""
        }>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <h3 className="font-bold">{metric.regulation}</h3>
              <Badge variant={
                metric.status === "passing" ? "default" :
                metric.status === "warning" ? "secondary" : "destructive"
              }>
                {metric.status}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            <Progress value={metric.score} className="h-2" />
            <div className="flex justify-between text-xs text-gray-500">
              <span>Score: {metric.score}%</span>
              <span>{metric.agents}/47 agents</span>
            </div>
            <div className="text-xs text-gray-400">Last check: {metric.lastCheck}</div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```

#### 5.6 Real-Time Agent Activity Feed
```tsx
// components/meok/ActivityFeed.tsx
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

interface ActivityEvent {
  id: string;
  timestamp: string;
  agentId: string;
  agentName: string;
  type: "task" | "alert" | "vote" | "sync" | "error";
  message: string;
}

const ACTIVITY_EVENTS: ActivityEvent[] = [
  { id: "1", timestamp: "14:32:01", agentId: "compliance-01", agentName: "GDPR Guardian", type: "task", message: "Completed quarterly data audit" },
  { id: "2", timestamp: "14:31:45", agentId: "trading-03", agentName: "Risk Manager", type: "alert", message: "Position limit approaching for Nifty futures" },
  { id: "3", timestamp: "14:31:22", agentId: "orchestrator", agentName: "MEOK Core", type: "vote", message: "BFT Proposal #2842 passed (38/47 votes)" },
  { id: "4", timestamp: "14:30:58", agentId: "data-07", agentName: "Sentiment Analyzer", type: "error", message: "Twitter API rate limit exceeded, retrying in 60s" },
  { id: "5", timestamp: "14:30:15", agentId: "compliance-05", agentName: "KYC Validator", type: "task", message: "Processed 23 new KYC verifications" },
];

export function ActivityFeed() {
  const typeColor = (type: string) => {
    switch (type) {
      case "task": return "bg-blue-100 text-blue-800";
      case "alert": return "bg-red-100 text-red-800";
      case "vote": return "bg-green-100 text-green-800";
      case "sync": return "bg-purple-100 text-purple-800";
      case "error": return "bg-red-200 text-red-900";
      default: return "bg-gray-100";
    }
  };

  return (
    <ScrollArea className="h-[400px] w-full">
      <div className="space-y-2 p-2">
        {ACTIVITY_EVENTS.map((event) => (
          <div key={event.id} className="flex gap-3 p-2 rounded-lg hover:bg-gray-50 text-sm">
            <div className="text-xs text-gray-400 whitespace-nowrap pt-0.5">{event.timestamp}</div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-0.5">
                <span className="font-medium truncate">{event.agentName}</span>
                <Badge variant="outline" className={`text-xs ${typeColor(event.type)}`}>
                  {event.type}
                </Badge>
              </div>
              <p className="text-gray-600 text-xs truncate">{event.message}</p>
            </div>
          </div>
        ))}
      </div>
    </ScrollArea>
  );
}
```

---

## 6. Mobile-First Design (Caravan-Optimized)

### Context: Nick Is in a Caravan with Spotty Internet

### Responsive Design Strategy
```tsx
// app/layout.tsx — Mobile-first layout
import { Sidebar } from "@/components/ui/sidebar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function MeokDashboardLayout() {
  return (
    <div className="flex flex-col md:flex-row h-screen bg-gray-50">
      {/* Mobile: Collapsible bottom nav / Desktop: Left sidebar */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t z-50">
        <MobileNavBar />
      </div>

      {/* Desktop sidebar */}
      <div className="hidden md:block w-64 border-r bg-white">
        <DesktopSidebar />
      </div>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto p-4 pb-20 md:pb-4">
        <MobileTabView /> {/* Shows tabs on mobile */}
        <DesktopGridView /> {/* Shows grid on desktop */}
      </main>
    </div>
  );
}

// Mobile-optimized tab view
function MobileTabView() {
  return (
    <Tabs defaultValue="roster" className="md:hidden">
      <TabsList className="grid grid-cols-4 w-full">
        <TabsTrigger value="roster">Agents</TabsTrigger>
        <TabsTrigger value="activity">Feed</TabsTrigger>
        <TabsTrigger value="compliance">Rules</TabsTrigger>
        <TabsTrigger value="map">Map</TabsTrigger>
      </TabsList>
      <TabsContent value="roster"><AgentRoster /></TabsContent>
      <TabsContent value="activity"><ActivityFeed /></TabsContent>
      <TabsContent value="compliance"><ComplianceDashboard /></TabsContent>
      <TabsContent value="map"><TownMap /></TabsContent>
    </Tabs>
  );
}
```

### Touch-Friendly Controls
```css
/* globals.css — Touch optimizations */
@media (pointer: coarse) {
  /* Larger tap targets for touch */
  .tap-target {
    min-height: 44px;
    min-width: 44px;
  }

  /* Bigger buttons on mobile */
  button, [role="button"] {
    padding: 12px 20px;
    font-size: 16px; /* Prevents iOS zoom on input focus */
  }

  /* Larger form inputs */
  input, select, textarea {
    font-size: 16px;
    padding: 12px;
  }
}

/* Prevent pull-to-refresh on mobile for app-like feel */
body {
  overscroll-behavior: none;
}
```

### Offline Capability (Service Worker)
```typescript
// public/sw.js — Service Worker for offline support
const CACHE_NAME = "meok-dashboard-v1";
const STATIC_ASSETS = [
  "/",
  "/dashboard",
  "/static/js/main.js",
  "/static/css/main.css",
];

// Install: Cache static assets
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
});

// Fetch: Stale-while-revalidate strategy
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetchPromise = fetch(event.request).then((networkResponse) => {
        if (networkResponse.ok) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, clone);
          });
        }
        return networkResponse;
      }).catch(() => cached); // Fall back to cache

      return cached || fetchPromise;
    })
  );
});

// Background sync for offline actions
self.addEventListener("sync", (event) => {
  if (event.tag === "bft-vote-sync") {
    event.waitUntil(syncPendingVotes());
  }
});
```

### PWA Manifest
```json
{
  "name": "MEOK Dashboard",
  "short_name": "MEOK",
  "description": "Orchestrate 47 MEOK agents from anywhere",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#111827",
  "orientation": "portrait-primary",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### Offline Data Strategy
```typescript
// hooks/useOfflineAgentData.ts
import { useState, useEffect } from "react";

interface CachedData<T> {
  data: T;
  timestamp: number;
  stale: boolean;
}

export function useOfflineAgentData<T>(key: string, fetcher: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    const load = async () => {
      // Try cache first for instant display
      const cached = localStorage.getItem(`meok-cache-${key}`);
      if (cached) {
        const parsed: CachedData<T> = JSON.parse(cached);
        setData(parsed.data);
        setIsLoading(false);
      }

      // Fetch fresh data if online
      if (navigator.onLine) {
        try {
          const fresh = await fetcher();
          setData(fresh);
          localStorage.setItem(`meok-cache-${key}`, JSON.stringify({
            data: fresh,
            timestamp: Date.now(),
            stale: false,
          }));
        } catch (e) {
          console.warn("Fetch failed, using cached data", e);
        }
      }
    };

    load();

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, [key]);

  return { data, isOnline, isLoading };
}
```

### Connection-Aware UI
```tsx
// components/meok/ConnectionStatus.tsx
export function ConnectionStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [latency, setLatency] = useState<number | null>(null);

  useEffect(() => {
    const check = () => setIsOnline(navigator.onLine);
    window.addEventListener("online", check);
    window.addEventListener("offline", check);

    // Ping server periodically to check latency
    const interval = setInterval(async () => {
      if (!navigator.onLine) return;
      const start = performance.now();
      try {
        await fetch("/api/health", { method: "HEAD" });
        setLatency(performance.now() - start);
      } catch {
        setLatency(null);
      }
    }, 30000);

    return () => {
      window.removeEventListener("online", check);
      window.removeEventListener("offline", check);
      clearInterval(interval);
    };
  }, []);

  if (isOnline && latency && latency < 500) {
    return <Badge variant="outline" className="bg-green-50 text-green-700">Online ({Math.round(latency)}ms)</Badge>;
  }
  if (isOnline && latency && latency >= 500) {
    return <Badge variant="outline" className="bg-yellow-50 text-yellow-700">Slow ({Math.round(latency)}ms)</Badge>;
  }
  return <Badge variant="outline" className="bg-red-50 text-red-700">Offline</Badge>;
}
```

---

## 7. Complete Working Example: MEOK Dashboard

### Project Setup
```bash
# 1. Create Next.js project
npx create-next-app@latest meok-dashboard --typescript --tailwind --app

cd meok-dashboard

# 2. Initialize shadcn/ui
npx shadcn@latest init

# 3. Add shadcn/ui components
npx shadcn@latest add button card badge sidebar avatar \
  table tabs scroll-area input textarea select \
  switch dialog dropdown-menu tooltip progress

# 4. Install AI SDK for streaming
npm install ai @ai-sdk/react @ai-sdk/openai

# 5. Install Mastra backend (in separate directory)
cd ..
mkdir meok-backend
cd meok-backend
npm create mastra@latest . --components agents,workflows,memory

# 6. Install Mastra AI SDK bridge
npm install @mastra/ai-sdk
```

### File Structure
```
meok-dashboard/
├── app/
│   ├── layout.tsx          # Root layout with sidebar
│   ├── page.tsx            # Main dashboard
│   ├── actions/
│   │   └── chat.ts         # Server Action for agent chat
│   └── globals.css
├── components/
│   ├── ui/                 # shadcn/ui components (auto-installed)
│   └── meok/               # Custom MEOK components
│       ├── AgentRoster.tsx
│       ├── BftVotingPanel.tsx
│       ├── PheromoneMatrix.tsx
│       ├── TownMap.tsx
│       ├── ComplianceDashboard.tsx
│       ├── ActivityFeed.tsx
│       ├── MobileNavBar.tsx
│       ├── DesktopSidebar.tsx
│       ├── ConnectionStatus.tsx
│       └── AgentChat.tsx
├── hooks/
│   └── useOfflineAgentData.ts
├── public/
│   ├── manifest.json       # PWA manifest
│   ├── sw.js              # Service Worker
│   ├── icon-192.png
│   └── icon-512.png
├── lib/
│   └── utils.ts
├── next.config.js
├── package.json
└── tsconfig.json
```

### Root Layout (PWA + Responsive)
```tsx
// app/layout.tsx
import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MEOK Dashboard",
  description: "Orchestrate 47 MEOK agents",
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "MEOK",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: "#111827",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

### Main Dashboard Page
```tsx
// app/page.tsx
import { AgentRoster } from "@/components/meok/AgentRoster";
import { ComplianceDashboard } from "@/components/meok/ComplianceDashboard";
import { ActivityFeed } from "@/components/meok/ActivityFeed";
import { TownMap } from "@/components/meok/TownMap";
import { BftVotingPanel } from "@/components/meok/BftVotingPanel";
import { ConnectionStatus } from "@/components/meok/ConnectionStatus";
import { AgentChat } from "@/components/meok/AgentChat";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardHeader, CardContent } from "@/components/ui/card";

export default function MeokDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-4 py-3 sticky top-0 z-40">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center text-white font-bold text-sm">
              M
            </div>
            <div>
              <h1 className="font-bold text-lg leading-tight">MEOK Dashboard</h1>
              <p className="text-xs text-gray-500">47 Agents · BFT Council Active</p>
            </div>
          </div>
          <ConnectionStatus />
        </div>
      </header>

      {/* Desktop: Full Grid / Mobile: Tabs */}
      <div className="max-w-7xl mx-auto p-4">
        {/* Desktop Layout */}
        <div className="hidden md:grid md:grid-cols-12 gap-4">
          {/* Left: Agent Roster */}
          <div className="col-span-4 space-y-4">
            <AgentRoster />
            <Card>
              <CardHeader><h3 className="font-bold">Live Chat</h3></CardHeader>
              <CardContent className="h-[400px]"><AgentChat /></CardContent>
            </Card>
          </div>

          {/* Center: Map + Activity */}
          <div className="col-span-5 space-y-4">
            <Card>
              <CardHeader><h3 className="font-bold">Town Map</h3></CardHeader>
              <CardContent><TownMap /></CardContent>
            </Card>
            <Card>
              <CardHeader><h3 className="font-bold">Activity Feed</h3></CardHeader>
              <CardContent><ActivityFeed /></CardContent>
            </Card>
          </div>

          {/* Right: Compliance + Voting */}
          <div className="col-span-3 space-y-4">
            <ComplianceDashboard />
            <BftVotingPanel proposal={{
              id: "2842",
              title: "Increase Position Limits",
              description: "Proposal to increase Nifty futures position limits by 15%",
              status: "open",
              votes: { yes: 31, no: 12, abstain: 4 },
              quorum: 35,
              deadline: "14:45",
            }} />
          </div>
        </div>

        {/* Mobile Layout: Tabs */}
        <div className="md:hidden pb-20">
          <Tabs defaultValue="agents">
            <TabsList className="grid grid-cols-5 w-full mb-4">
              <TabsTrigger value="agents">Agents</TabsTrigger>
              <TabsTrigger value="map">Map</TabsTrigger>
              <TabsTrigger value="activity">Feed</TabsTrigger>
              <TabsTrigger value="compliance">Rules</TabsTrigger>
              <TabsTrigger value="chat">Chat</TabsTrigger>
            </TabsList>
            <TabsContent value="agents"><AgentRoster /></TabsContent>
            <TabsContent value="map">
              <Card><CardContent className="pt-4"><TownMap /></CardContent></Card>
            </TabsContent>
            <TabsContent value="activity">
              <Card><CardHeader><h3 className="font-bold">Activity Feed</h3></CardHeader><CardContent><ActivityFeed /></CardContent></Card>
            </TabsContent>
            <TabsContent value="compliance">
              <ComplianceDashboard />
              <div className="mt-4">
                <BftVotingPanel proposal={{
                  id: "2842", title: "Increase Position Limits",
                  description: "Increase Nifty futures limits by 15%",
                  status: "open", votes: { yes: 31, no: 12, abstain: 4 },
                  quorum: 35, deadline: "14:45",
                }} />
              </div>
            </TabsContent>
            <TabsContent value="chat">
              <Card className="h-[calc(100vh-200px)]"><CardContent className="h-full p-0"><AgentChat /></CardContent></Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
```

### Agent Chat with Streaming (Full Implementation)
```tsx
// components/meok/AgentChat.tsx
"use client";

import { useChat } from "ai/react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { useRef, useEffect } from "react";

export function AgentChat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, status } = useChat({
    api: "/api/chat",
    maxSteps: 5, // Allow multi-step tool calls
  });
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const getStatusBadge = () => {
    switch (status) {
      case "submitted": return <Badge variant="outline" className="bg-yellow-50">Sending...</Badge>;
      case "streaming": return <Badge variant="outline" className="bg-green-50">Agent thinking...</Badge>;
      default: return null;
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <ScrollArea className="flex-1 p-3" ref={scrollRef}>
        <div className="space-y-3">
          {messages.length === 0 && (
            <div className="text-center text-gray-400 py-8">
              <p className="font-medium">MEOK Command Center</p>
              <p className="text-sm">Send commands to your 47 agents</p>
              <div className="mt-4 space-y-1 text-xs">
                <p>"Check compliance status for all agents"</p>
                <p>"Show me the BFT council votes"</p>
                <p>"Which agents are reporting errors?"</p>
              </div>
            </div>
          )}
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[85%] rounded-lg p-3 text-sm ${
                  message.role === "user"
                    ? "bg-gray-900 text-white"
                    : "bg-gray-100 text-gray-900"
                }`}
              >
                {/* Show tool calls */}
                {message.parts?.map((part, i) => {
                  if (part.type === "tool-invocation") {
                    return (
                      <div key={i} className="mt-1 p-2 bg-white/10 rounded text-xs font-mono">
                        Tool: {part.toolInvocation.toolName}
                        {part.toolInvocation.state === "result" && (
                          <span className="text-green-400 ml-2">Done</span>
                        )}
                      </div>
                    );
                  }
                  if (part.type === "text") {
                    return <span key={i}>{part.text}</span>;
                  }
                  return null;
                }) || <span>{message.content}</span>}
              </div>
            </div>
          ))}
          {getStatusBadge()}
        </div>
      </ScrollArea>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-3 border-t bg-white">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={handleInputChange}
            placeholder="Command MEOK..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading || !input.trim()} size="sm">
            {isLoading ? "..." : "Send"}
          </Button>
        </div>
      </form>
    </div>
  );
}
```

### Backend API Route
```tsx
// app/api/chat/route.ts
import { openai } from "@ai-sdk/openai";
import { streamText, tool } from "ai";
import { z } from "zod";
import { NextResponse } from "next/server";

// Mock agent database
const AGENTS_DB = Array.from({ length: 47 }, (_, i) => ({
  id: `agent-${String(i + 1).padStart(3, "0")}`,
  name: ["GDPR Guardian", "SEBI Sentinel", "Risk Manager", "Market Data", "Sentiment AI", "KYC Validator"][i % 6] + ` ${Math.floor(i / 6) + 1}`,
  role: ["compliance", "compliance", "trading", "data", "data", "compliance"][i % 6],
  status: Math.random() > 0.1 ? "active" : (Math.random() > 0.5 ? "idle" : "error"),
  complianceScore: 85 + Math.floor(Math.random() * 15),
}));

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai("gpt-4o"),
    system: `You are the MEOK Orchestrator, managing 47 specialized AI agents across compliance, trading, data, infrastructure, and analytics.
    You have access to tools to check agent status, run compliance checks, and view BFT council votes.
    Always respond concisely. Use tools when the user asks about specific agents or data.`,
    messages,
    tools: {
      listAgents: tool({
        description: "List all MEOK agents with their status",
        parameters: z.object({
          filter: z.enum(["all", "active", "idle", "error", "compliance", "trading", "data", "infrastructure", "analytics"]).optional(),
        }),
        execute: async ({ filter = "all" }) => {
          let agents = AGENTS_DB;
          if (filter && filter !== "all") {
            if (["active", "idle", "error"].includes(filter)) {
              agents = agents.filter((a) => a.status === filter);
            } else {
              agents = agents.filter((a) => a.role === filter);
            }
          }
          return { agents: agents.slice(0, 10), total: agents.length };
        },
      }),
      checkCompliance: tool({
        description: "Check compliance scores across all agents",
        parameters: z.object({}),
        execute: async () => {
          const scores = AGENTS_DB.map((a) => a.complianceScore);
          const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
          return {
            average: avg.toFixed(1),
            passing: AGENTS_DB.filter((a) => a.complianceScore >= 90).length,
            failing: AGENTS_DB.filter((a) => a.complianceScore < 85).length,
          };
        },
      }),
      getBftVotes: tool({
        description: "Get current BFT council voting status",
        parameters: z.object({ proposalId: z.string().optional() }),
        execute: async ({ proposalId }) => {
          return {
            proposal: proposalId || "2842",
            yes: 31, no: 12, abstain: 4,
            quorum: 35, status: "quorum_met",
          };
        },
      }),
    },
  });

  return result.toDataStreamResponse();
}
```

---

## 8. Final Recommendations for MEOK

### Recommended Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend Framework** | Next.js 15 + React 19 | App shell, routing, SSR |
| **UI Components** | shadcn/ui | Buttons, cards, tables, dialogs, etc. |
| **AI Chat** | Vercel AI SDK 6 (useChat) | Streaming agent responses |
| **Backend Agents** | Mastra 1.0 | Agent orchestration, memory, workflows |
| **Styling** | Tailwind CSS | Utility-first responsive styling |
| **State Management** | React hooks + localStorage | Offline-capable state |
| **PWA** | Service Worker + Manifest | Offline support, installable |
| **Mobile** | Touch-friendly CSS + Tabs | Caravan-optimized mobile UX |

### What Gets Built Custom vs. Off-the-Shelf

| Component | Source | Effort |
|-----------|--------|--------|
| Button, Card, Input, Dialog | shadcn/ui (install) | Low |
| Chat streaming UI | Vercel AI SDK useChat | Low |
| Agent orchestration logic | Mastra | Low-Medium |
| **Agent Roster (47 agents)** | Custom build | Medium |
| **BFT Voting UI** | Custom build | Medium |
| **Pheromone Matrix** | Custom build | High |
| **Town Map (circuit pyramid)** | Custom build | High |
| **Compliance Dashboard** | Custom build | Medium |
| **Activity Feed** | Custom build | Low |
| Offline sync, PWA | Custom build | Medium |

### Development Phases

| Phase | Features | Timeline |
|-------|----------|----------|
| **MVP (Week 1-2)** | Agent roster, chat interface, compliance dashboard | 2 weeks |
| **V2 (Week 3-4)** | BFT voting, activity feed, mobile optimization | 2 weeks |
| **V3 (Week 5-6)** | Town map, pheromone matrix, offline support | 2 weeks |
| **Production (Week 7-8)** | PWA, performance, security hardening | 2 weeks |

### Cost Estimate

| Item | Cost |
|------|------|
| shadcn/ui | Free (open source) |
| Vercel AI SDK | Free (open source) |
| Mastra | Free (open source, Apache 2.0) |
| Next.js hosting (Vercel Hobby) | Free |
| OpenAI API (GPT-4o) | ~$50-200/month depending on usage |
| Domain + SSL | $12-20/year |
| **Total Monthly** | **$50-200** |

---

*Research compiled: July 2026*
*Sources: GitHub repos, official documentation, npm registry, community benchmarks*
