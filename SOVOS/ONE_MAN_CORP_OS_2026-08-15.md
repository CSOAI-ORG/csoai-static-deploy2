# THE ONE-MAN-CORPORATION OS — CEO-Fabric Architecture (2026-08-15)

## The question, answered

**"Can we run the whole business as a team of specialist CEO agents, on K3/swarm/its own pod?"**

**Yes — and the compute placement is the key insight: the CEO agents are NOT
GPU-heavy.** They are orchestration + API-call + light-inference agents (exactly
like this session runs on OpenRouter). They do NOT belong on the A100/3090
(those stay for measurement). They belong on a **lightweight always-on
orchestrator** — the Oracle micros (fabric) + K3 (burst) + a cheap always-on
container — with the GPU fleet as the measurement engine they command.

## The Board of Directors (the CEO agents)

Not sov6 "families" (personality clans) — **business-function CEOs** (each an
MCP-wrapped specialist with its own toolset, routed by sovos_router, every
action signed):

| Seat | CEO agent | Toolset (harness) | What it runs |
|---|---|---|---|
| **CEO** | you (the only human) | final sign-off on everything | chairman of the board |
| **CFO** | accountant-agent | ERPNext (GPL-3.0, 38k★) + Stripe + bookkeeping | global tax prep, multi-currency, VAT, invoices |
| **CRO** | sales-agent | Twenty (55k★, open-source Salesforce) + named-account engine | pipeline, outreach, design partners |
| **CMO** | marketing-agent | n8n (200k★) + press pack + content engine | PR sequencing, blog, social |
| **CLO** | legal-IP-agent | OIN/LOT (done) + contract templates + OpenPatent | IP filings, contracts, compliance |
| **CTO** | dev-agent | Devin + Claude Code + 58-package monorepo | build, ship, fix |
| **COO** | ops-agent | fleet + cron + MCP workers + Oracle mesh | the measurement fabric runs |
| **CPO** | publishing-agent | distribution kit (Zenodo/HF/Kaggle/PyPI/npm) | signed cards → every registry |
| **CISO** | security-agent | claim-linter + firewall-lint + jail bank | neutrality + tamper-evidence |

## The routing layer (exists — extend it)

```
                YOU (Chairman — final sign-off)
                          │
              ┌───────────┴───────────┐
              │   sovos_router +      │
              │   MCP federation      │  ← EXISTS
              └───────────┬───────────┘
        ┌────────┬────────┼────────┬────────┐
        ▼        ▼        ▼        ▼        ▼
      CFO      CRO      CMO      CLO      CTO
   (ERPNext) (Twenty)  (n8n)   (legal)  (Devin)
        └────────┬────────┴────────┬────────┘
                 │  every action   │
                 ▼  SIGNED + logged▼
              measurement fabric (exists)
```

## Compute placement (the honest answer)

| Workload | Where it runs | Why |
|---|---|---|
| **CEO agents (orchestration)** | Oracle micros + K3 burst + cheap always-on container | They're API-call agents — 1GB RAM is enough for routing + tool dispatch |
| **Frontier measurement** | A100 (80GB) | board runs, heavy probes |
| **Mid measurement** | 3090 (24GB) | 24x7 arena loop |
| **Burst probes** | K3 serverless (2TB vol) | FlashBoot mid-size models |
| **Lightweight rotator** | A1.Flex (£0) | ~5-6 models/hour continuous |
| **Public surfaces** | Cloudflare Pages + Workers | releases, scoreboard, verify |

**The CEO agents do NOT need a GPU pod.** They need: API access (OpenRouter/
frontier models for reasoning), the MCP toolset, and the signed-card layer.
Putting them on the A100 wastes the GPU — the same mistake as running your
browser on the measurement rig.

## What's already built vs what's missing

| Layer | Status |
|---|---|
| Router + MCP federation | ✅ EXISTS (sovos_router, 30+ MCPs) |
| A2A swarm pattern | ✅ EXISTS (fishkeeper/muckaway/councilof/gspc_measure) |
| Signed-card fabric | ✅ EXISTS (bom_signer, oms_sign, csoai_core, verify) |
| Distribution | ✅ EXISTS (Zenodo kit, HF, Kaggle, PyPI, npm) |
| IP/legal | ✅ EXISTS (OIN 2.0, LOT, 42-comp inventory) |
| Marketing/press | ⚠️ EXISTS as pack, needs automation |
| Accounting/ERP | ❌ MISSING (install ERPNext) |
| CRM | ❌ MISSING (install Twenty) |
| Workflow automation | ⚠️ PARTIAL (wire n8n) |

## The 3 CEO-fabric pilots (this week, £0)

1. **CFO pilot**: stand up ERPNext (Docker on the A100's spare capacity or a
   £5/mo VPS) → ledger for the estate → signed monthly financial card
2. **CRO pilot**: Twenty CRM + the named-account engine → first 20 prospects
   tracked → outreach loop wired to n8n
3. **COO pilot**: the router already routes measurement; add a
   business-function routing table (finance→CFO, sales→CRO, etc.)

## The bigger play (why this is the product)

The One-Man-Corporation OS **is** the product. Every AI-economy company will
need exactly this: a router + specialist CEO agents + signed records — to run
with 1-2 humans. We dogfood it on ourselves, the signed cards prove it works,
and that's the design-partner offer: "run your company on the same fabric."

## Firewall in the CEO fabric

- ❌ No CEO agent may accept referral fees, paid placement, or
  rating-for-listing (the CMO/CRO agents are firewall-linted)
- ❌ No agent may sign a tax filing or contract — only prep; the human (and
  where required, a qualified professional) signs the authority act
- ✅ Every agent action is signed + logged — the board is audit-able end to end

---

*Status: architecture written. Pilots: CFO (ERPNext) + CRO (Twenty) + COO
(routing table) — all £0, all on the existing fabric.*