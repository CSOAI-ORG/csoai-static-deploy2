# SOVEREIGN CHARTER — LOOP FACTORY
## loopfactory.ai
## CSOAI Ltd · UK Companies House 16939677 · London, United Kingdom

> **Charter Article 0**: Never take equity, board seats, revenue-sharing, or success fees from institutions we certify. ISO fee-for-service model ONLY. **CA3O is the CMKC for AI.**

## ARTICLE I — SOVEREIGN FOUNDATION
| Field | Value |
|---|---|
| **Hive Slug** | `loopfactory` |
| **Domain** | `loopfactory.ai` |
| **Industry** | Sovereign Workflow Automation & Trigger Orchestration |
| **UK SIC** | 62090 — Other information technology service activities |
| **MCP Tools** | `cron-ai-mcp`, `webhook-ai-mcp` |
| **BFT Council Ratification** | Council #LOO-001 — Quorum 23/33 |

## ARTICLE II — INDUSTRY DOMAIN & MARKET

### II.A — Scope
LoopFactory provides sovereign automation infrastructure: cron job scheduling, webhook trigger management, event-driven workflow orchestration, and action chaining. Unlike Zapier/Make/IFTTT which are US-cloud-dependent and charge £20-£800/month, LoopFactory is free, self-hosted, UK-sovereign, and every automation is Ed25519-signed with BFT-verifiable execution logs.

### II.B — Market & Barriers
- **Global TAM**: £15.2B (workflow automation market by 2027)
- **Current Barrier**: Cloud dependency, vendor lock-in, recurring SaaS costs. Zapier charges £20-£800/mo. Make charges £9-£29/mo. All US-hosted.
- **Sovereign Barrier Drop**: Free, self-hosted, Ed25519-verified automation. No cloud dependency. No vendor lock-in. Every trigger, every action, every execution is cryptographically signed and auditable.

### II.C — Black Swan Window
- **Cloud sovereignty movement (2026+)**: EU data residency laws tightening. UK GDPR post-Brexit divergence. Organisations seeking sovereign automation alternatives.
- **AI agent orchestration (2026-2027)**: As AI agents proliferate, the need for sovereign, verifiable agent-to-agent automation infrastructure becomes critical.

### II.D — Technical Architecture
- **Cron Engine**: Full 5-field (minute, hour, day, month, weekday) and 7-field (second, minute, hour, day, month, weekday, year) support. Special strings: @yearly, @monthly, @weekly, @daily, @hourly, @reboot. Timezone-aware scheduling with DST handling.
- **Webhook Engine**: HMAC-SHA256 signing, replay protection via nonce+timestamp, IP whitelisting, rate limiting (token bucket algorithm), payload validation (JSON Schema), dead letter queue for failed deliveries.
- **Workflow Patterns**: Fan-out (one trigger → N parallel actions), Saga (compensating transactions for rollback), Circuit Breaker (stop cascade failures), Retry with Exponential Backoff (1s, 2s, 4s, 8s, 16s, max 5 retries), Idempotency Keys for at-least-once delivery.
- **Enterprise Architecture**: Multi-tenant isolation, per-tenant rate limits, queue depth monitoring (alert at >1,000 pending), SLA tracking (p95/p99 latency), Ed25519-signed execution logs per workflow run.

### II.E — Comparison With Existing Tools
| Feature | LoopFactory | Zapier | Make (Integromat) | IFTTT |
|---|---|---|---|---|
| **Cost** | FREE | £20-£800/mo | £9-£29/mo | Free (limited) |
| **Hosting** | Self-hosted | US Cloud | US Cloud | US Cloud |
| **Sovereign** | ✅ UK | ❌ | ❌ | ❌ |
| **Ed25519 Audit** | ✅ | ❌ | ❌ | ❌ |
| **BFT Governance** | ✅ | ❌ | ❌ | ❌ |
| **Air-Gap Deploy** | ✅ | ❌ | ❌ | ❌ |
| **Open Source** | ✅ MIT | ❌ | ❌ | ❌ |
| **Multi-Step** | ✅ Unlimited | ✅ (paid tiers) | ✅ | ❌ (1 action) |

## ARTICLE III — FREE TRAINING PATHWAY

| Tier | Name | Modules | Duration | Cert |
|---|---|---|---|---|
| **T1** | Foundation | Automation Fundamentals, Cron Expression Mastery (5-field vs 7-field, special strings, timezone handling), Webhook Basics (HTTP methods, payload formats, authentication), Trigger Types (schedule, webhook, event, manual), Action Types (HTTP, email, MCP call, script) | 4 weeks | CASA-1 |
| **T2** | Practitioner | Complex Workflow Design (branching, parallelisation, fan-out/fan-in), Error Handling & Retry Logic (exponential backoff, circuit breaker, dead letter queues), Multi-Step Pipeline Orchestration, API Integration Patterns (REST, GraphQL, MCP, WebSocket), Webhook Security (HMAC signing, replay protection, IP whitelisting) | 8 weeks | CASA-2 |
| **T3** | Lead Auditor | Automation Security Auditing (OWASP automation risks, injection attacks, privilege escalation), Workflow Optimisation (bottleneck detection, parallelisation analysis, cost modelling), Enterprise Automation Architecture (multi-tenant, rate limiting, queue depth management, SLA monitoring), Compliance-Aware Automation (GDPR Art 22, SOC 2, audit trail requirements) | 12 weeks | CASA-3 |
| **T4** | Director | Automation Governance Design (policy-as-code, approval workflows, change management), Multi-Tenant Automation Platforms (tenant isolation, resource quotas, billing models), BFT-Verified Workflow Chains (council-approved automation sequences, Sigil-signed execution), Sovereign Automation Strategy (national-level automation infrastructure) | 16 weeks | CASA-4 |

### III.B — UE5 Simulation Scenarios

1. **The Pipeline Builder**: Design a multi-step automation pipeline in a 3D visual workspace. Drag-and-drop triggers (schedule, webhook, MCP event), connect actions (HTTP call, email, script, database query), add branching logic (if/else, switch, parallel fan-out), configure error handling (retry 3× with exponential backoff, then dead letter). Test the pipeline with simulated events. View the Ed25519 execution log. Pass if pipeline completes 100 test events with zero unhandled errors.

2. **The Cron Storm**: 500 cron jobs fire simultaneously at midnight. CPU spikes to 95%. Some jobs depend on others. Diagnose the conflicts: identify jobs with overlapping resource requirements, detect dependency deadlocks, implement staggered scheduling with priority queues, add rate limiting without dropping jobs. Pass if all 500 jobs complete within the 5-minute SLA window with zero deadlocks.

3. **The Webhook Avalanche**: 10,000 webhooks arrive in 60 seconds from an upstream system that went into overdrive. Triage the flood: HMAC-verify each webhook (reject forgeries), classify by priority (critical/high/normal/low), route to appropriate handlers, implement backpressure to signal the upstream to slow down. Pass if all verified webhooks are processed within 2 minutes with zero forgery acceptances.

4. **The Migration**: A company has 200 Zapier zaps and 50 Make scenarios. Map each trigger → action pair to LoopFactory equivalents. Handle the edge cases: multi-step zaps with paths, Make scenarios with iterators/aggregators, custom code steps, filter conditions. Verify functional equivalence. Generate the migration report. Pass if 100% of automated workflows are successfully migrated.

5. **The Midnight Recovery**: The 2am batch automation (payroll processing, 50K transactions) has failed due to a cascading dependency failure. Access the execution logs, identify the root cause (a database connection pool exhaustion from a leaking workflow), fix the leak, restart the batch from the last successful checkpoint, verify no duplicate transactions. Pass if all 50K transactions complete before the 6am business opening SLA.

### III.C — UBI Starter
- Foundation (T1) → Automation builder marketplace (£300/mo training credits)
- Practitioner (T2) → Workflow engineering contracts (£600/mo project credits)
- Lead Auditor (T3) → Enterprise automation audit contracts (£900/mo)
- Director (T4) → Automation governance council presidency (£1,200/mo stipend)

## ARTICLE IV — COMPLIANCE (GDPR Art 22 — automated decision-making transparency; SOC 2 — automation audit trails; ISO 27001 — secure automation infrastructure; UK Data Protection Act 2018)

## ARTICLE V — CROSS-WALK
| Target | Relationship |
|---|---|
| **meok** | Substrate provider — LoopFactory runs on MEOK MCP infrastructure |
| **csoai** | Certification authority — Watchdog certs for automation auditors |
| **meok-compliance-gateway** | x402 payment triggers — usage-based billing via compliance gateway |
| **councilof** | BFT-verified workflow approval chains |
| **proofof** | Sigil-signed automation execution attestations |
| **asisecurity** | Automation security auditing — OWASP automation risks |
| **dataprivacyof** | GDPR Art 22 compliance for automated decisions |
| **cobolbridge** | Legacy batch job (JCL) → LoopFactory migration |

## ARTICLE VI — SIGNATURE CHAIN
```
Charter ID: CSOAI-CHARTER-loopfactory-2026-06-30
SHA-256: a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6
Ed25519 Signature: (reserved)
SIGIL Digest: e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6
BFT Ratification: Council #LOO-001, 23/33
```

> *"Automation without audit is chaos. Automation with Ed25519 is sovereign infrastructure."* 🐉
