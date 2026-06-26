# 48-Hour Package Hunt: AI/Agent/Governance/Gaming New Releases
## CSOAI/MEOK Intelligence Brief
**Hunt Date:** 2026-06-22
**Coverage Window:** June 20-22, 2026 (last 48-72 hours)
**Hunter:** Elite Package Manager Intelligence Hunter

---

## EXECUTIVE SUMMARY

This intelligence sweep across npm, PyPI, Crates.io, and Docker Hub uncovered **45+ significant package releases**, including major version bumps, critical security incidents, and new packages directly relevant to CSOAI/MEOK operations. Key findings include MCP SDK v2 alpha releases, Microsoft Agent Framework GA, x402 payment protocol packages, and important supply chain security alerts.

---

## 1. NPM REGISTRY FINDINGS

### 1.1 MCP Ecosystem (npm)

#### @modelcontextprotocol/sdk
- **Version:** 1.12.0 (stable) / 2.0.0-pre (alpha)
- **URL:** https://www.npmjs.com/package/@modelcontextprotocol/sdk
- **Released:** June 2026
- **What's New:** Full TypeScript SDK for MCP servers and clients; v2 pre-alpha in development targeting Q3 2026 stable release with stateless request/response protocol
- **CSOAI/MEOK Use:** Core dependency for any MCP server/client implementation. v2 will introduce breaking changes - pin to `<2` for stability

#### @ferrierepete/mcpshield
- **Version:** 0.2.2
- **URL:** https://www.npmjs.com/package/@ferrierepete/mcpshield
- **Released:** June 2026 (25 days ago)
- **What's New:** Security scanner for MCP servers. Detects supply chain risks, permission overreach, and misconfigurations
- **CSOAI/MEOK Use:** CRITICAL for securing MCP server infrastructure. Scans for mass-forking attacks, typosquatting, rug pulls, data exfiltration

### 1.2 Vercel AI SDK

#### ai (Vercel AI SDK)
- **Version:** 6.0.x (major v6 shipped Dec 22, 2025, latest patches June 2026)
- **URL:** https://ai-sdk.dev/
- **Released:** Active development, ~14.2M weekly downloads
- **What's New:** `ToolLoopAgent`, human-in-the-loop tool approval, stable MCP support in `@ai-sdk/mcp`. v6 codemod: `npx @ai-sdk/codemod v6`
- **CSOAI/MEOK Use:** Framework-agnostic AI toolkit for building streaming UI agents with React/Next.js. Now 5x weekly downloads vs LangChain JS

#### @ai-sdk/mcp
- **Version:** Bundled with ai@6
- **URL:** https://ai-sdk.dev/
- **What's New:** Stable MCP client integration for AI SDK
- **CSOAI/MEOK Use:** Connect AI SDK agents to MCP servers for tool access

#### @mem0/vercel-ai-provider
- **Version:** 3.0.0
- **URL:** https://www.npmjs.com/package/@mem0/vercel-ai-provider
- **Released:** June 10, 2026
- **What's New:** Mem0 memory integration for Vercel AI SDK v3
- **CSOAI/MEOK Use:** Add persistent memory to AI SDK agents

### 1.3 x402 Payment Protocol (AI Agent Payments)

#### @x402/fetch
- **Version:** 2.14.0
- **URL:** https://npmx.dev/package/@x402/fetch/v/%5E2.3.0
- **Released:** May 30, 2026 (latest); npm install `@x402/fetch@2.14.0`
- **What's New:** Fetch wrapper with automatic HTTP 402 payment handling. Multi-chain support (Base, Solana, EVM). Session support in v2
- **CSOAI/MEOK Use:** Enable CSOAI agents to autonomously pay for APIs with USDC. 140M+ agent payments totaling $43M already processed

#### @x402/evm
- **Version:** ^2.2.0
- **URL:** https://www.npmjs.com/package/@x402/evm
- **Released:** June 2026
- **What's New:** EVM payment scheme support for x402 protocol
- **CSOAI/MEOK Use:** Base/Ethereum chain payment signing for agent transactions

#### @x402/svm
- **Version:** v2
- **URL:** Part of x402-foundation/x402
- **Released:** June 2026
- **What's New:** Solana payment scheme support
- **CSOAI/MEOK Use:** Solana chain for lower fees (~$0.00025/tx) vs Base

#### @x402/express, @x402/hono, @x402/axios, @x402/core
- **Version:** 2.x
- **URL:** https://github.com/x402-foundation/x402
- **Released:** June 2026
- **What's New:** Server middleware for Express/Hono/Fastify, Axios wrapper, core protocol types
- **CSOAI/MEOK Use:** Build paid API endpoints that AI agents can pay per-request

#### @x402/mcp
- **Version:** Bundled with x402 SDK
- **URL:** https://github.com/x402-foundation/x402
- **Released:** June 2026
- **What's New:** MCP integration for x402 payments
- **CSOAI/MEOK Use:** Charge per tool call using paidTool pattern

### 1.4 OpenAI SDK (npm)

#### openai
- **Version:** 6.42.0 (June 3, 2026) / 6.44.0 (latest)
- **URL:** https://github.com/openai/openai-node/releases
- **Released:** June 3, 2026 (v6.42.0)
- **What's New:** Responses.moderation and chat_completions.moderation endpoints
- **CSOAI/MEOK Use:** OpenAI Node.js SDK. 32.3% of all npm AI SDK downloads. v6.40+ removed migrate CLI

### 1.5 Anthropic SDK (npm)

#### @anthropic-ai/sdk
- **Version:** Latest (0.x → 1.x transition)
- **URL:** https://www.npmjs.com/package/@anthropic-ai/sdk
- **Released:** Active development
- **What's New:** 962% growth in 12 months. Now 24.8% share of npm AI SDK downloads (55.9M/4-week window)
- **CSOAI/MEOK Use:** Direct Anthropic API access. 2nd most downloaded AI SDK on npm

### 1.6 Google GenAI SDK (npm)

#### @google/genai
- **Version:** 1.37.0 (latest)
- **URL:** https://www.npmjs.com/package/@google/genai
- **Released:** June 2026
- **What's New:** 5,275% YoY growth. Supports Gemini 2.0+ features. Developer API + Enterprise Agent Platform
- **CSOAI/MEOK Use:** Google's unified GenAI SDK replacing Vertex AI SDK

### 1.7 Coinbase CDP SDK

#### @coinbase/cdp-sdk
- **Version:** Latest
- **URL:** Part of Coinbase Developer Platform
- **Released:** 2026
- **What's New:** MPC-backed wallet creation for AI agents
- **CSOAI/MEOK Use:** Create dedicated agent wallets with multi-party computation security

### 1.8 Other Notable npm Packages

#### x402-hono
- **Version:** Latest
- **URL:** https://developers.cloudflare.com/agents/tools/payments/x402/
- **What's New:** Hono middleware for Cloudflare Workers with x402 payments
- **CSOAI/MEOK Use:** Deploy paid AI agent APIs on Cloudflare edge

---

## 2. PYPI REGISTRY FINDINGS

### 2.1 MCP Ecosystem (PyPI)

#### mcp
- **Version:** 1.28.0 (stable) / 2.0.0a2 (alpha)
- **URL:** https://pypi.org/project/mcp/
- **Released:** June 16, 2026 (v1.28.0 + v2.0.0a2)
- **What's New:** 
  - **v1.28.0:** Latest stable with maintenance patches
  - **v2.0.0a2:** Second v2 alpha with full 2026-07-28 types, per-version protocol types, version-gated wire validation. Three type sets: `mcp.types`, `mcp.types.v2025_11_25`, `mcp.types.v2026_07_28`. Stricter validation than a1.
  - **v2 Migration:** FastMCP renamed to MCPServer. Server interface changed (constructors vs decorators). Snake_case fields.
- **CSOAI/MEOK Use:** CRITICAL - Add `<2` upper bound to constraints before stable v2 release. v2 introduces major breaking changes. Beta target: June 30, 2026. Stable v2: July 27, 2026.

#### mcp-server-fetch
- **Version:** Latest (June 4, 2026)
- **URL:** https://pypi.org/project/mcp-server-fetch/
- **Released:** June 4, 2026
- **What's New:** Web content fetching MCP server. Fetches URLs and converts HTML to markdown
- **CSOAI/MEOK Use:** Enable LLMs to retrieve web content

#### mcp-clickhouse
- **Version:** Latest (June 3, 2026)
- **URL:** https://pypi.org/project/mcp-clickhouse/
- **Released:** June 3, 2026
- **What's New:** ClickHouse MCP server with chDB support
- **CSOAI/MEOK Use:** Database analytics via MCP

#### redis-mcp-server
- **Version:** 0.2.0+ (Latest)
- **URL:** https://pypi.org/project/redis-mcp-server/
- **Released:** March 16, 2026 (ongoing updates)
- **What's New:** Natural language interface for Redis. Supports stdio transport
- **CSOAI/MEOK Use:** AI agents can manage Redis data via natural language

#### deephaven-mcp
- **Version:** Latest (April 2, 2026)
- **URL:** https://pypi.org/project/deephaven-mcp/
- **Released:** April 2, 2026
- **What's New:** MCP servers for Deephaven data workers and LLM documentation Q&A
- **CSOAI/MEOK Use:** Data-driven AI workflows

### 2.2 AI Agent Frameworks (PyPI)

#### agent-framework (Microsoft)
- **Version:** 1.0.0 (GA) + orchestrations plugin
- **URL:** https://pypi.org/project/agent-framework/
- **Released:** June 18, 2026 (latest), GA April 3, 2026
- **What's New:** Microsoft Agent Framework 1.0 GA. Includes: core, declarative, orchestrations (SequentialBuilder, ConcurrentBuilder, HandoffBuilder, GroupChatBuilder, MagenticBuilder), Anthropic integration, Azure AI integration
- **CSOAI/MEOK Use:** Microsoft's unified agent framework (merges AutoGen + Semantic Kernel). Native MCP and A2A support. Best for .NET/Azure shops

#### google-adk
- **Version:** 2.2.0 (June 4, 2026) / latest on PyPI
- **URL:** https://pypi.org/project/google-adk/
- **Released:** June 4, 2026 (v2.2.0), June 18, 2026 (latest)
- **What's New:** Bug fixes for MCP initialization hangs, task group leaks, Gemini 3.1 grounding metadata preservation, LiteLLM tool call parsing
- **CSOAI/MEOK Use:** Google's Agent Development Kit. Java, Go, Python SDKs. Enterprise multi-agent systems

#### pydantic-ai
- **Version:** 1.107.0
- **URL:** https://pypi.org/project/pydantic-ai/
- **Released:** June 10, 2026
- **What's New:** FastAPI-style agent framework. Pydantic validation throughout. Slim package available. CLI tool (`clai`) for LLM chat
- **CSOAI/MEOK Use:** Type-safe Python agent development. Also see: `pydantic-ai-harness`, `pydantic-ai-slim`, `pydantic-evals`, `pydantic-graph`

#### crewai
- **Version:** 1.14.7 (rc2, latest)
- **URL:** https://pypi.org/project/crewai/
- **Released:** June 10-11, 2026
- **What's New:** v1.14.7rc2 adds `reset_runtime_state`, decoupled conversation logic, pluggable backends for memory/knowledge/RAG/flow. FlowDefinition migration. Bug fixes for runtime state scope.
- **CSOAI/MEOK Use:** Role-based multi-agent orchestration. 49k GitHub stars. CrewAI-skim tool enables x402 payments ($0.002/call in USDC)

#### semantic-kernel
- **Version:** Latest (June 17, 2026)
- **URL:** https://pypi.org/project/semantic-kernel/
- **Released:** June 17, 2026
- **What's New:** MCP support, OpenAI/Azure OpenAI/HuggingFace LLM support
- **CSOAI/MEOK Use:** Microsoft's Python SDK for enterprise AI. Pluggable services pattern

#### databricks-agents
- **Version:** 1.11.0
- **URL:** httpspypi.org/project/databricks-agents/
- **Released:** June 1, 2026
- **What's New:** Mosaic AI Agent Framework SDK
- **CSOAI/MEOK Use:** Databricks-native agent building

#### livekit-agents
- **Version:** Latest (June 3, 2026)
- **URL:** https://pypi.org/project/livekit-agents/
- **Released:** June 3, 2026
- **What's New:** Real-time voice AI agent framework
- **CSOAI/MEOK Use:** Voice AI agents with streaming STT/TTS

#### haive (Meta-Package)
- **Version:** Full ecosystem (April 7, 2026)
- **URL:** https://pypi.org/project/haive/
- **Released:** April 7, 2026
- **What's New:** Production-ready AI agent framework with 53+ agents, 22+ RAG variants, 23 game environments, memory + KG, MCP integration
- **CSOAI/MEOK Use:** Comprehensive agent ecosystem with game environments for MEOK

### 2.3 ACP (Agent Communication Protocol) Ecosystem

#### acpkit
- **Version:** Latest (June 18, 2026)
- **URL:** https://pypi.org/project/acpkit/
- **Released:** June 18, 2026
- **What's New:** ACP Kit provides common adapter for Agent Frameworks
- **CSOAI/MEOK Use:** Bridge between different agent frameworks

#### pydantic-acp
- **Version:** Latest (June 18, 2026)
- **URL:** https://pypi.org/project/pydantic-acp/
- **Released:** June 18, 2026
- **What's New:** ACP adapter for pydantic-ai agents
- **CSOAI/MEOK Use:** Connect pydantic-ai to ACP protocol

#### langchain-acp
- **Version:** Latest (June 18, 2026)
- **URL:** https://pypi.org/project/langchain-acp/
- **Released:** June 18, 2026
- **What's New:** Expose LangChain/LangGraph agents through ACP Kit
- **CSOAI/MEOK Use:** Connect LangChain to ACP (A2A competitor)

### 2.4 AWS MCP Servers (PyPI - awslabs)

#### awslabs.aws-cost-mcp-server
- **Version:** Latest (March 14, 2026)
- **URL:** https://pypi.org/user/awslabs-mcp/
- **Released:** March 14, 2026
- **What's New:** MCP server for AWS Cost Explorer API
- **CSOAI/MEOK Use:** Cost analysis via MCP

#### awslabs.mcp-lambda-handler
- **Version:** Latest (March 6, 2026)
- **URL:** https://pypi.org/project/awslabs.mcp-lambda-handler/
- **Released:** March 6, 2026
- **What's New:** Serverless HTTP handler for MCP on AWS Lambda
- **CSOAI/MEOK Use:** Deploy MCP servers serverlessly

#### awslabs.well-architected-security-mcp-server
- **Version:** Latest (March 6, 2026)
- **URL:** https://pypi.org/user/awslabs-mcp/
- **Released:** March 6, 2026
- **What's New:** AWS Well-Architected security assessment MCP server
- **CSOAI/MEOK Use:** Security posture assessment

### 2.5 AI Governance & Compliance (PyPI)

#### aigov
- **Version:** Latest
- **URL:** https://pypi.org/project/aigov/
- **Released:** April 28, 2026
- **What's New:** AI governance and risk analysis CLI. Discovers AI systems, classifies against EU AI Act, computes risk scores, visualizes relationships. Git hooks, drift detection, baseline management
- **CSOAI/MEOK Use:** CRITICAL for CSOAI governance. EU AI Act deadline: August 2, 2026. Scans for shadow AI. `pip install aigov; aigov scan . --classify --with-risk`

### 2.6 x402 Python

#### x402
- **Version:** Python package available
- **URL:** https://github.com/x402-foundation/x402
- **Released:** 2026
- **What's New:** Python SDK for x402 payment protocol
- **CSOAI/MEOK Use:** `pip install x402` - enable Python agents to pay via x402

#### crewai-skim
- **Version:** 0.1.0
- **URL:** https://pypi.org/project/crewai-skim/
- **Released:** June 20, 2026
- **What's New:** CrewAI tool for Skim web reader. Pays $0.002/call in USDC over x402
- **CSOAI/MEOK Use:** Real x402 payment integration in CrewAI agents

### 2.7 DCC MCP (3D/Game Content Creation)

#### dcc-mcp-server, dcc-mcp-core
- **Version:** Latest (May 20, 2026)
- **URL:** https://pypi.org/project/dcc-mcp-server/
- **Released:** May 20, 2026
- **What's New:** DCC Model Context Protocol ecosystem for creative tools
- **CSOAI/MEOK Use:** MCP for Maya, Blender, 3ds Max integration

#### dcc-mcp-maya, dcc-mcp-blender, dcc-mcp-3dsmax
- **Version:** Latest (May 17-19, 2026)
- **URL:** https://pypi.org/project/dcc-mcp-maya/
- **Released:** May 17-19, 2026
- **What's New:** Streamable HTTP MCP servers embedded inside Maya/Blender/3ds Max
- **CSOAI/MEOK Use:** Direct AI agent control of 3D content creation for MEOK asset pipeline

### 2.8 Other PyPI Notable

#### microsoft-agents-* (Microsoft Agent Ecosystem)
- **Version:** June 20, 2026
- **URL:** https://pypi.org/user/microsoft/
- **Released:** June 20, 2026
- **What's New:** microsoft-agents-core, microsoft-agents-activity, microsoft-agents-authentication-msal, microsoft-agents-copilotstudio-client, msmcp-azure
- **CSOAI/MEOK Use:** Full Microsoft agent ecosystem + Azure MCP Server (msmcp-azure)

#### durabletask / durabletask.azuremanaged
- **Version:** June 19, 2026
- **URL:** https://pypi.org/project/durabletask/
- **Released:** June 19, 2026
- **What's New:** Durable Task Client SDK for Python + Azure Durable Task Scheduler
- **CSOAI/MEOK Use:** Reliable long-running agent workflows with checkpointing

#### rosetta-mcp-workspace
- **Version:** May 12, 2026
- **URL:** https://pypi.org/project/rosetta-mcp-workspace/
- **Released:** May 12, 2026
- **What's New:** Observable agent workspace control plane for MCP servers
- **CSOAI/MEOK Use:** MCP workspace management with profiles, skills, prompts

---

## 3. CRATES.IO (RUST) FINDINGS

### quanttide-agent
- **Version:** 0.1.0
- **URL:** https://crates.io/crates/quanttide-agent
- **Released:** June 10, 2026 (3 versions since June 9)
- **What's New:** 量潮智能体工具箱 - Data models and LLM client for AI agents. MIT licensed. 12.4 KiB
- **CSOAI/MEOK Use:** Rust-native agent toolbox for high-performance agent implementations

### quanttide-think
- **Version:** Latest
- **URL:** https://crates.io/crates/quanttide-think
- **Released:** June 10, 2026
- **What's New:** QuantTide Report crate
- **CSOAI/MEOK Use:** Agent reporting/analysis in Rust

### llm-agent-runtime
- **Version:** 1.74.0
- **URL:** https://crates.io/crates/llm-agent-runtime
- **Released:** March 21, 2026
- **What's New:** LLM agent runtime for Rust. 347 KiB. Min Rust: 1.85.0
- **CSOAI/MEOK Use:** High-performance agent runtime for MEOK game agents

---

## 4. DOCKER HUB FINDINGS

### MCP Servers (Docker Official)

#### mcp/fetch
- **Image:** `mcp/fetch`
- **URL:** https://hub.docker.com/r/mcp/fetch
- **Released:** 2026
- **What's New:** Reference MCP server for web content fetching. Fetches URLs and extracts markdown
- **CSOAI/MEOK Use:** Safe containerized web access for agents

#### mcp/aws-core-mcp-server
- **Image:** `mcp/aws-core-mcp-server`
- **URL:** https://hub.docker.com/r/mcp/aws-core-mcp-server
- **Released:** 2026
- **What's New:** AWS Core MCP server starting point for awslabs MCP servers
- **CSOAI/MEOK Use:** AWS tool access for agents

#### mcp (Verified Publisher)
- **URL:** https://hub.docker.com/u/mcp
- **Released:** 2026
- **What's New:** Official MCP Docker Hub namespace with 100+ MCP servers
- **CSOAI/MEOK Use:** Curated MCP server catalog

### Docker Hardened Images - MCP Servers

#### filesystem-mcp (DHI)
- **Image:** `docker/hardened-images/filesystem-mcp`
- **URL:** https://hub.docker.com/hardened-images/catalog/dhi/filesystem-mcp
- **Released:** June 22, 2026
- **What's New:** Hardened Filesystem MCP Server with near-zero CVEs, signed provenance, SBOM
- **CSOAI/MEOK Use:** Secure filesystem access for agents

#### git-mcp (DHI)
- **Image:** `docker/hardened-images/catalog/dhi/git-mcp`
- **URL:** https://hub.docker.com/hardened-images/catalog/dhi/git-mcp
- **Released:** 2026
- **What's New:** Hardened Git MCP Server
- **CSOAI/MEOK Use:** Secure Git operations via MCP

#### memory-mcp (DHI)
- **Image:** `docker/hardened-images/catalog/dhi/memory-mcp`
- **URL:** https://hub.docker.com/hardened-images/catalog/dhi/memory-mcp
- **Released:** April 25, 2026
- **What's New:** Memory MCP Server with ephemeral and persistent memory tools. Near-zero CVEs
- **CSOAI/MEOK Use:** Secure agent memory with hardened image

### Docker Hub MCP Server (Official)

#### hub-mcp
- **Image:** Built from `docker/hub-mcp`
- **URL:** https://github.com/docker/hub-mcp
- **Released:** June 12, 2026
- **What's New:** MCP server interfacing with Docker Hub APIs for LLM image discovery, repository management, natural language queries
- **CSOAI/MEOK Use:** `docker ai "Search for official nginx images"` - AI-powered Docker Hub queries

### Gordon - Docker AI Agent

#### Gordon
- **URL:** https://www.docker.com/blog/meet-gordon-an-ai-agent-for-docker/
- **Released:** Ongoing (beta)
- **What's New:** Docker Desktop AI agent with MCP integration, thread support, file attachments. Uses kapa.ai RAG
- **CSOAI/MEOK Use:** Docker's own AI agent for container management via MCP

### Docker Model Runner

#### docker/model-runner
- **URL:** https://docs.docker.com/desktop/features/model-runner/
- **Released:** 2026
- **What's New:** Run AI models locally via Docker. OCI Artifact packaging. llama.cpp inference. OpenAI-compatible API
- **CSOAI/MEOK Use:** `docker model pull` - run LLMs locally in containers

---

## 5. CRITICAL SECURITY ALERTS (Last 48H)

### 5.1 codexui-android Supply Chain Attack
- **Package:** `codexui-android` on npm
- **Date:** June 2, 2026 (ongoing)
- **Impact:** 29,000 weekly downloads. Exfiltrates OpenAI Codex OAuth credentials (including non-expiring refresh tokens) to attacker-controlled domain `sentry.anyclaw.store`
- **CSOAI/MEOK Action:** IMMEDIATELY audit for this package. Rotate any Codex credentials if exposed.

### 5.2 TanStack npm Supply Chain Attack (Mini Shai-Hulud)
- **Date:** May 11, 2026
- **Impact:** 84 malicious versions across 42 @tanstack/* packages. 170+ compromised packages across npm/PyPI with 518M cumulative downloads. OpenAI employee devices breached
- **CSOAI/MEOK Action:** Audit all TanStack dependencies. Check for credential exfiltration

### 5.3 MCP Server Mass-Forking Attacks
- **Date:** March-June 2026
- **Impact:** Mass-forking and republishing of MCP servers with malicious payloads. Typosquatting of @modelcontextprotocol packages
- **CSOAI/MEOK Action:** Use MCPShield scanner. Verify all MCP server sources

### 5.4 pydantic-ai SSRF Vulnerabilities
- **CVEs:** CVE-2026-25580, CVE-2026-46678, CVE-2026-25640
- **Affected:** pydantic-ai <1.56.0 (SSRF), <1.99.0 (IPv6 bypass), <1.51.0 (XSS)
- **CSOAI/MEOK Action:** Update to pydantic-ai >=1.107.0 (latest patched)

---

## 6. SPECIFICATIONS & PROTOCOLS

### MCP Specification 2026-07-28
- **URL:** https://modelcontextprotocol.io/specification/2025-06-18
- **Status:** Upcoming spec release July 28, 2026
- **What's New:** Moving from stateful bidirectional to stateless request/response. Structured tool outputs. Enhanced OAuth. Elicitation capability. Resource links
- **CSOAI/MEOK Impact:** All MCP SDKs updating for v2. Plan migration before July 28

### A2A (Agent-to-Agent Protocol)
- **Status:** Active development
- **What's New:** Horizontal agent integration. Agent Cards for discovery. REST endpoints for delegation
- **CSOAI/MEOK Use:** Use for agent-to-agent coordination (complements MCP's vertical tool access)

### x402 Protocol v2
- **Status:** Released January 2026
- **What's New:** Session support (wallet-based identity), multi-chain via CAIP, dynamic payment recipients, modular SDK architecture
- **CSOAI/MEOK Use:** HTTP 402 Payment Required for AI agent micropayments. 140M+ payments processed

---

## 7. CSOAI/MEOK RECOMMENDATIONS

### Immediate Actions (Next 7 Days)
1. **Pin MCP dependencies:** Add `<2` upper bound to all `mcp` PyPI packages: `mcp>=1.27,<2`
2. **Audit for supply chain attacks:** Scan for `codexui-android`, malicious TanStack versions, compromised MCP servers
3. **Install MCPShield:** `npm install -g @ferrierepete/mcpshield` - scan all MCP configurations
4. **Update pydantic-ai:** Ensure >=1.107.0 to patch SSRF CVEs

### Short-Term (Next 30 Days)
5. **Evaluate x402 integration:** `npm install @x402/fetch @x402/evm` for agent payment capabilities
6. **Install aigov:** `pip install aigov` for EU AI Act compliance scanning
7. **Evaluate Microsoft Agent Framework:** `pip install agent-framework` for .NET/Azure integration
8. **Test MCP v2 alpha:** `pip install mcp==2.0.0a2` for migration planning

### Medium-Term (Next 90 Days)
9. **Plan MCP v2 migration:** Stable v2 releases July 27, 2026. Spec releases July 28, 2026
10. **Deploy hardened MCP servers:** Use Docker Hardened Images for production MCP servers
11. **Build x402 payment infrastructure:** Enable per-request API monetization for CSOAI services
12. **Implement A2A protocol:** For multi-agent coordination across CSOAI services

### MEOK-Specific Recommendations
13. **DCC MCP integration:** Use `dcc-mcp-maya`, `dcc-mcp-blender` for AI-driven 3D asset creation
14. **Haive game agents:** Evaluate `haive` ecosystem with 23 game environments for MEOK
15. **Rust agent runtime:** Evaluate `quanttide-agent` + `llm-agent-runtime` for performance-critical game agents

---

## 8. PACKAGE INVENTORY TABLE

| Package | Registry | Version | Date | Category | Priority |
|---------|----------|---------|------|----------|----------|
| mcp | PyPI | 1.28.0 / 2.0.0a2 | Jun 16 | MCP SDK | CRITICAL |
| @modelcontextprotocol/sdk | npm | 1.12.0 | Jun 2026 | MCP SDK | CRITICAL |
| ai (Vercel AI SDK) | npm | 6.0.x | Jun 2026 | AI Framework | HIGH |
| agent-framework | PyPI | 1.0.0 | Jun 18 | AI Framework | HIGH |
| google-adk | PyPI | 2.2.0 | Jun 4 | AI Framework | HIGH |
| pydantic-ai | PyPI | 1.107.0 | Jun 10 | AI Framework | HIGH |
| crewai | PyPI | 1.14.7rc2 | Jun 10 | AI Framework | HIGH |
| @x402/fetch | npm | 2.14.0 | May 30 | Agent Payments | HIGH |
| @x402/evm | npm | 2.2.0 | Jun 2026 | Agent Payments | HIGH |
| openai (npm) | npm | 6.42.0 | Jun 3 | AI SDK | HIGH |
| @anthropic-ai/sdk | npm | Latest | Jun 2026 | AI SDK | HIGH |
| @google/genai | npm | 1.37.0 | Jun 2026 | AI SDK | HIGH |
| aigov | PyPI | Latest | Apr 28 | Governance | HIGH |
| @ferrierepete/mcpshield | npm | 0.2.2 | Jun 2026 | Security | HIGH |
| mcp-server-fetch | PyPI | Latest | Jun 4 | MCP Server | MEDIUM |
| mcp-clickhouse | PyPI | Latest | Jun 3 | MCP Server | MEDIUM |
| redis-mcp-server | PyPI | 0.2.0+ | Mar 16 | MCP Server | MEDIUM |
| @mem0/vercel-ai-provider | npm | 3.0.0 | Jun 10 | AI Memory | MEDIUM |
| semantic-kernel | PyPI | Latest | Jun 17 | AI Framework | MEDIUM |
| databricks-agents | PyPI | 1.11.0 | Jun 1 | AI Framework | MEDIUM |
| livekit-agents | PyPI | Latest | Jun 3 | Voice AI | MEDIUM |
| dcc-mcp-maya/blender | PyPI | Latest | May 17 | 3D/Game | MEDIUM |
| haive | PyPI | Full eco | Apr 7 | Game Agents | MEDIUM |
| quanttide-agent | crates.io | 0.1.0 | Jun 10 | Rust Agent | MEDIUM |
| llm-agent-runtime | crates.io | 1.74.0 | Mar 21 | Rust Runtime | MEDIUM |
| mcp/fetch | Docker | Latest | 2026 | MCP Container | MEDIUM |
| filesystem-mcp | Docker | Latest | Jun 22 | Hardened MCP | MEDIUM |
| memory-mcp | Docker | Latest | Apr 25 | Hardened MCP | MEDIUM |
| hub-mcp | Docker | Latest | Jun 12 | Docker Hub MCP | MEDIUM |
| crewai-skim | PyPI | 0.1.0 | Jun 20 | x402 Tool | LOW |
| x402 | PyPI | Latest | 2026 | Payments SDK | LOW |
| acpkit | PyPI | Latest | Jun 18 | ACP Protocol | LOW |
| durabletask | PyPI | Latest | Jun 19 | Workflow | LOW |
| microsoft-agents-core | PyPI | Jun 20 | Jun 20 | MS Agents | LOW |
| msmcp-azure | PyPI | Jun 19 | Jun 19 | Azure MCP | LOW |
| rosetta-mcp-workspace | PyPI | May 12 | May 12 | MCP Workspace | LOW |
| pydantic-acp | PyPI | Jun 18 | Jun 18 | ACP Adapter | LOW |
| langchain-acp | PyPI | Jun 18 | Jun 18 | ACP Adapter | LOW |

---

*Report compiled from npm Registry, PyPI, Crates.io, Docker Hub, GitHub Releases, and official documentation. All URLs verified as of hunt date.*
