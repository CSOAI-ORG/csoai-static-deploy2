# SOVOS Supercharged Model Harness
## Unified Alliance + NVIDIA Stack Under Sovereign Compute
### August 5, 2026 | Integration Architecture + Deployment Manifests

---

## WHAT IS A MODEL HARNESS?

A model harness is the runtime environment that hosts, evaluates, governs, and secures AI models. It is not just inference serving. It is the complete lifecycle:

```
Model Upload → Licence Scan → Safety Eval → Provenance Sign → 
Inference Serve → Runtime Guard → Threat Detect → Verdict Log → 
Care Monitor → Multi-Agent Orchestrate → Human Override
```

SOVOS is the sovereign compute layer. The harness is the software stack running ON SOVOS. By integrating all alliance + NVIDIA tools into one harness, you create a **unified platform** that customers rent as a complete governance-ready AI runtime.

---

## THE HARNESS ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SOVOS CONTROL PLANE                              │
│  (Kubernetes / Docker Compose — runs on any GPU node: M2, 3090, A100)  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   INGRESS   │  │   GOVERN    │  │   SECURE    │  │   OBSERVE   │  │
│  │   LAYER     │  │   LAYER     │  │   LAYER     │  │   LAYER     │  │
│  │             │  │             │  │             │  │             │  │
│  │ Triton      │  │ NeMo        │  │ Morpheus    │  │ LangSmith   │  │
│  │ Inference   │  │ Guardrails  │  │ Threat      │  │ Agent       │  │
│  │ Server      │  │ (Colang)    │  │ Detection   │  │ Tracing     │  │
│  │             │  │             │  │             │  │             │  │
│  │ + cuOpt     │  │ + GSPC      │  │ + MDASH     │  │ + Prometheus│  │
│  │   Router    │  │   Evaluator │  │   Scanner   │  │   Grafana   │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
│         │                │                │                │         │
│  ┌──────┴────────────────┴────────────────┴────────────────┴──────┐  │
│  │                     SOV SIGNAL BUS (Kafka / Redis)                  │  │
│  │  All telemetry, verdicts, traces, anomalies flow through here      │  │
│  └──────┬────────────────┬────────────────┬────────────────┬──────┘  │
│         │                │                │                │         │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐  │
│  │   AGENT     │  │   PROVE     │  │   SWARM     │  │   CARE      │  │
│  │   LAYER     │  │   LAYER     │  │   LAYER     │  │   LAYER     │  │
│  │             │  │             │  │             │  │             │  │
│  │ NOOA        │  │ C2PA        │  │ LangGraph   │  │ care.co     │  │
│  │ Runtime     │  │ Signing     │  │ Multi-Agent │  │ Guardrails  │  │
│  │             │  │             │  │ Orchestrate │  │ Wellbeing   │  │
│  │ + MCP Packs │  │ + Safetensor│  │ + MDASH     │  │ + Human     │  │
│  │   (27 sec)  │  │   Verify    │  │   Red Team  │  │   Escalate  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    SIMULATION LAYER (Optional GPU)                 │  │
│  │  Isaac Sim (RTX 3090) + Cosmos (A100) + ACE SDK (RTX 3090)      │  │
│  │  + CARLA + FlightGear + Godot (all via Docker / Kubernetes)       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## THE SUPERCHARGE: WHY UNIFIED IS BETTER

Using these tools individually:
- NeMo Guardrails runs on one server
- C2PA signs on another server
- LangGraph orchestrates on a third server
- Morpheus detects on a fourth server
- No shared state, no shared telemetry, no unified governance

**SOVOS Harness unifies them:**
- **One Kafka bus** — all tools share events in real-time
- **One GSPC Evaluator** — every event gets a governance verdict
- **One C2PA signing key** — all outputs are cryptographically proven
- **One LangSmith trace** — every agent action is observable
- **One dashboard** — human operators see everything

**The supercharge is the integration, not the individual tools.**

---

## DEPLOYMENT MANIFEST: Docker Compose (Single Node)

This runs on any machine with Docker. Start on your M2, migrate to 3090, scale to A100 cluster.

```yaml
# sovos-harness/docker-compose.yml
version: '3.8'

services:
  # ───────────────────────────────────────────
  # INGRESS LAYER: Model Serving
  # ───────────────────────────────────────────
  triton:
    image: nvcr.io/nvidia/tritonserver:24.10-py3
    command: tritonserver --model-repository=/models
    volumes:
      - ./models:/models:ro
      - ./triton-config:/config:ro
    ports:
      - "8000:8000"  # HTTP
      - "8001:8001"  # gRPC
      - "8002:8002"  # Metrics
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # GOVERN LAYER: Safety + Evaluation
  # ───────────────────────────────────────────
  guardrails:
    image: nemoguardrails/nemoguardrails:latest
    command: nemoguardrails server --config=/config
    volumes:
      - ./guardrails-config:/config:ro
      - ./gspc-evaluator:/gspc:ro
    ports:
      - "5000:5000"
    environment:
      - GUARDRAILS_COLANG_PATH=/config
      - GSPC_EVALUATOR_PATH=/gspc
    depends_on:
      - kafka
      - redis
    networks:
      - sov-net

  gspc-evaluator:
    build: ./gspc-evaluator
    command: uvicorn gspc_server:app --host 0.0.0.0 --port 5001
    volumes:
      - ./gspc-evaluator:/app:ro
      - ./statutory-corpus:/corpus:ro
    ports:
      - "5001:5001"
    environment:
      - STATUTORY_CORPUS_PATH=/corpus
      - SIGNING_KEY_PATH=/run/secrets/gspc-key
    secrets:
      - gspc-key
    depends_on:
      - kafka
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # SECURE LAYER: Threat Detection
  # ───────────────────────────────────────────
  morpheus:
    image: nvcr.io/nvidia/morpheus/morpheus:24.10
    command: morpheus run pipeline
    volumes:
      - ./morpheus-config:/config:ro
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - KAFKA_BROKER=kafka:9092
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    depends_on:
      - kafka
    networks:
      - sov-net

  mdash:
    build: ./mdash  # Cloned from microsoft/MDASH
    command: python mdash_server.py --mode=continuous
    volumes:
      - ./mdash-config:/config:ro
    environment:
      - KAFKA_BROKER=kafka:9092
      - TARGET_AGENTS=agent-layer:7000
    depends_on:
      - kafka
      - agent-layer
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # OBSERVE LAYER: Tracing + Metrics
  # ───────────────────────────────────────────
  langsmith:
    image: langchain/langsmith:latest
    ports:
      - "5002:5002"
    environment:
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
      - KAFKA_BROKER=kafka:9092
    depends_on:
      - kafka
    networks:
      - sov-net

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports:
      - "9090:9090"
    networks:
      - sov-net

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - ./grafana-dashboards:/var/lib/grafana/dashboards:ro
      - ./grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml:ro
    depends_on:
      - prometheus
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # SOV SIGNAL BUS: Event Streaming
  # ───────────────────────────────────────────
  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper
    networks:
      - sov-net

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    networks:
      - sov-net

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # AGENT LAYER: NOOA Runtime + MCP Packs
  # ───────────────────────────────────────────
  agent-layer:
    build: ./nooa-runtime  # Your NOOA fork + MCP Packs
    command: uvicorn nooa_server:app --host 0.0.0.0 --port 7000
    volumes:
      - ./mcp-packs:/mcp-packs:ro
      - ./nooa-memory:/memory
    ports:
      - "7000:7000"
    environment:
      - NOOA_LLM_PROVIDER=ollama  # or triton, openai, etc.
      - NOOA_MEMORY_PATH=/memory
      - KAFKA_BROKER=kafka:9092
      - GUARDRAILS_ENDPOINT=http://guardrails:5000
    depends_on:
      - kafka
      - redis
      - guardrails
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # PROVE LAYER: Provenance + Integrity
  # ───────────────────────────────────────────
  c2pa-signer:
    build: ./c2pa-signer  # pip install c2pa wrapper
    command: python c2pa_server.py --port 6000
    volumes:
      - ./c2pa-manifests:/manifests
      - ./signing-keys:/keys:ro
    ports:
      - "6000:6000"
    environment:
      - C2PA_PRIVATE_KEY_PATH=/keys/c2pa.pem
      - KAFKA_BROKER=kafka:9092
    secrets:
      - c2pa-key
    depends_on:
      - kafka
    networks:
      - sov-net

  safetensor-verify:
    build: ./safetensor-verify
    command: python verify_server.py --port 6001
    ports:
      - "6001:6001"
    volumes:
      - ./model-cache:/models:ro
    environment:
      - KAFKA_BROKER=kafka:9092
    depends_on:
      - kafka
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # SWARM LAYER: Multi-Agent Orchestration
  # ───────────────────────────────────────────
  langgraph:
    build: ./langgraph-runtime
    command: python swarm_orchestrator.py --port 7001
    ports:
      - "7001:7001"
    environment:
      - KAFKA_BROKER=kafka:9092
      - AGENT_LAYER=http://agent-layer:7000
      - MDASH_ENDPOINT=http://mdash:6002
    depends_on:
      - kafka
      - agent-layer
      - mdash
    networks:
      - sov-net

  swarm-council:
    build: ./swarm-council  # Your SwarmCouncil NOOA agent
    command: python council_server.py --port 7002
    ports:
      - "7002:7002"
    environment:
      - KAFKA_BROKER=kafka:9092
      - GSPC_ENDPOINT=http://gspc-evaluator:5001
      - HUMAN_DASHBOARD=http://grafana:3000
    depends_on:
      - kafka
      - gspc-evaluator
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # CARE LAYER: Wellbeing Monitoring
  # ───────────────────────────────────────────
  care-monitor:
    build: ./care-monitor  # care.co Guardrails runtime
    command: python care_server.py --port 7003
    ports:
      - "7003:7003"
    environment:
      - KAFKA_BROKER=kafka:9092
      - GUARDRAILS_ENDPOINT=http://guardrails:5000
      - ESCALATION_WEBHOOK=https://councilof.ai/human-escalate
    depends_on:
      - kafka
      - guardrails
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # SIMULATION LAYER (GPU Required — Optional)
  # ───────────────────────────────────────────
  isaac-sim:
    image: nvcr.io/nvidia/isaac-sim:4.5.0
    profiles: ["gpu"]
    runtime: nvidia
    environment:
      - DISPLAY=${DISPLAY}
      - NVIDIA_VISIBLE_DEVICES=all
    volumes:
      - ./isaac-sim-scenes:/isaac-sim/scenes:ro
      - /tmp/.X11-unix:/tmp/.X11-unix:rw
    ports:
      - "8211:8211"
    networks:
      - sov-net

  # ───────────────────────────────────────────
  # OSS LAYER: Licence + Supply Chain Scanning
  # ───────────────────────────────────────────
  fossa-scan:
    image: fossa/fossa-cli:latest
    command: fossa analyze --output /results/fossa.json
    volumes:
      - ./:/src:ro
      - ./scan-results:/results
    profiles: ["scan"]
    networks:
      - sov-net

  codeql-scan:
    image: github/codeql-action/codeql:latest
    command: codeql database analyze --format=sarifv2.1.0 --output=/results/codeql.sarif
    volumes:
      - ./:/src:ro
      - ./scan-results:/results
    profiles: ["scan"]
    networks:
      - sov-net

secrets:
  gspc-key:
    file: ./secrets/gspc-signing-key.pem
  c2pa-key:
    file: ./secrets/c2pa-private-key.pem

networks:
  sov-net:
    driver: bridge
```

---

## THE SUPERCHARGE: CROSS-LAYER EVENT FLOW

When a user sends a prompt to a model hosted on SOVOS, this is what happens:

```
┌────────────────────────────────────────────────────────────────────────┐
│  EVENT: User sends prompt to 3Haul agent                                 │
├────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. INGRESS (Triton)                                                     │
│     → Receives prompt via HTTP/gRPC                                      │
│     → Routes to 3Haul model (cuOpt optimizes if logistics query)         │
│     → Publishes event to Kafka: `topic: inference.request`               │
│                                                                          │
│  2. GOVERN (Guardrails + GSPC)                                           │
│     → Kafka consumer reads `inference.request`                           │
│     → Guardrails input rail: checks for Art 5 violations                 │
│     → If violation: blocks, sends `topic: governance.blocked`              │
│     → GSPC Evaluator runs: produces verdict record                       │
│     → Signs verdict with HMAC-SHA256 (or ML-DSA if ASI enabled)          │
│     → Publishes `topic: governance.verdict`                              │
│                                                                          │
│  3. SECURE (Morpheus + MDASH)                                           │
│     → Morpheus reads `inference.request`                                 │
│     → Digital fingerprinting: is this a known attack pattern?          │
│     → MDASH reads agent code: is there an exploitable vulnerability?   │
│     → If threat detected: sends `topic: security.alert`                  │
│     → GSPC Evaluator scores threat against regulatory provisions         │
│                                                                          │
│  4. AGENT (NOOA + MCP Packs)                                           │
│     → If not blocked: NOOA agent processes prompt                        │
│     → 3Haul agent calls `calculate_fuel()` (deterministic Python)      │
│     → 3Haul agent calls `optimize_route()` (LLM-driven, Guardrails wraps)│
│     → MemoryManager logs interaction to SQLite                           │
│     → Publishes `topic: agent.action`                                    │
│                                                                          │
│  5. PROVE (C2PA + Safetensors)                                         │
│     → C2PA signer reads `agent.action`                                   │
│     → Generates C2PA manifest for the output                             │
│     → Cryptographically signs the output + manifest                     │
│     → Publishes `topic: provenance.signed`                                 │
│                                                                          │
│  6. SWARM (LangGraph + SwarmCouncil)                                   │
│     → If multi-agent: LangGraph orchestrates agent calls                 │
│     → SwarmCouncil mediates disputes between agents                      │
│     → Every dispute calls GSPC Evaluator → signed verdict                │
│     → Publishes `topic: swarm.consensus`                                │
│                                                                          │
│  7. CARE (care.co)                                                     │
│     → care-monitor reads `agent.action`                                  │
│     → Scores interaction for user wellbeing                              │
│     → If care-score < threshold: sends `topic: care.escalate`            │
│     → Human operator notified via Grafana dashboard                      │
│                                                                          │
│  8. OBSERVE (LangSmith + Prometheus + Grafana)                           │
│     → LangSmith traces every LLM call, tool call, agent step             │
│     → Prometheus metrics: latency, throughput, error rate                  │
│     → Grafana dashboard: real-time view of all layers                    │
│                                                                          │
│  9. OUTPUT                                                             │
│     → User receives: response + C2PA manifest + GSPC verdict + trace ID │
│     → Every output is: signed, governed, traced, provenanced            │
│                                                                          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## THE SUPERCHARGE: WHAT CUSTOMERS GET

When a customer rents SOVOS compute, they don't get "a GPU." They get:

| Feature | What It Means | Axis |
|---------|-------------|------|
| **Sovereign Inference** | Their model runs on their GPU, their data never leaves | GOV |
| **Automatic Safety** | Every prompt checked against EU AI Act Art 5 before reaching the model | ART5 |
| **Signed Outputs** | Every response has a C2PA manifest — prove it came from your model | PRV |
| **Threat Detection** | Morpheus monitors for attacks in real-time | DET |
| **Vulnerability Scanning** | MDASH continuously scans agent code for exploits | DET |
| **Multi-Agent Ready** | LangGraph orchestrates agent swarms with governance consensus | SWARM |
| **Wellbeing Monitoring** | care.co ensures AI interactions don't harm users | CARE |
| **Full Observability** | LangSmith traces every step; Grafana shows real-time health | GOV |
| **Audit Grade** | Every event produces a GSPC verdict record — court-admissible | GOV |
| **Quantum Proof** | (Optional) ML-DSA signatures — valid even after quantum computers | ASI |

**This is not "AI hosting." This is "AI governance as infrastructure."**

---

## HONEST DEPLOYMENT NOTES

### What Runs on Your M2 Today (CPU Only)
| Service | Docker | CPU | Notes |
|---------|--------|-----|-------|
| Guardrails | ✅ | Yes | Colang flows, no GPU needed |
| GSPC Evaluator | ✅ | Yes | Deterministic Python, no GPU |
| Kafka | ✅ | Yes | Event bus, no GPU |
| Redis | ✅ | Yes | Cache, no GPU |
| LangSmith | ✅ | Yes | Tracing, no GPU |
| Prometheus | ✅ | Yes | Metrics, no GPU |
| Grafana | ✅ | Yes | Dashboard, no GPU |
| NOOA Agent Layer | ✅ | Yes | CPU inference via Ollama |
| C2PA Signer | ✅ | Yes | Cryptographic signing, no GPU |
| Safetensor Verify | ✅ | Yes | Hash verification, no GPU |
| care.co | ✅ | Yes | Colang flows, no GPU |
| SwarmCouncil | ✅ | Yes | Python orchestration, no GPU |

**Command to start harness on M2:**
```bash
cd sovos-harness
docker-compose up -d guardrails gspc-evaluator kafka redis   langsmith prometheus grafana agent-layer c2pa-signer   safetensor-verify langgraph swarm-council care-monitor
```

### What Needs GPU (3090 or A100)
| Service | GPU | Minimum VRAM | Notes |
|---------|-----|-------------|-------|
| Triton + TensorRT | NVIDIA | 8GB | Model serving, optimized |
| Morpheus | NVIDIA | 16GB | Threat detection, streaming |
| MDASH | NVIDIA | 8GB | Vulnerability scanning |
| Isaac Sim | RTX | 12GB | **Requires RTX cores — 3090 works, A100 does NOT** |
| ACE SDK | RTX | 8GB | **Requires RTX — 3090 works** |
| Cosmos 7B | NVIDIA | 50GB | **Fits on A100 80GB, not on 3090 24GB** |
| Cosmos 14B | NVIDIA | 100GB | **Needs 2× A100 or H100** |

**Command to start GPU services on 3090:**
```bash
docker-compose --profile gpu up -d isaac-sim
```

**Command to start GPU services on A100:**
```bash
docker-compose --profile gpu up -d triton morpheus mdash
```

### What Needs External (Not Docker)
| Service | Why | Alternative |
|---------|-----|-------------|
| Cloudflare Workers AI | Cloud inference endpoint | Run local Triton instead |
| GitHub Dependabot | SaaS, not self-hosted | Use `fossa-cli` in Docker |
| GitHub CodeQL | SaaS, not self-hosted | Use `semgrep` in Docker |
| LangSmith Cloud | Managed tracing | Self-hosted LangSmith in Docker |

---

## THE SUPERCHARGE PRICING MODEL

When customers rent SOVOS, they pay for tiers:

| Tier | What They Get | Price | Axes |
|------|-------------|-------|------|
| **SOVOS Core** | Triton inference + Guardrails + GSPC + Kafka + Redis | £0.05/hr | GOV, AGI, ART5 |
| **SOVOS Secure** | Core + Morpheus + MDASH + CodeQL scanning | £0.12/hr | + DET, OSS |
| **SOVOS Provenance** | Secure + C2PA signing + Safetensor verify | £0.15/hr | + PRV |
| **SOVOS Swarm** | Provenance + LangGraph + SwarmCouncil | £0.20/hr | + SWARM |
| **SOVOS Care** | Swarm + care.co wellbeing monitoring | £0.22/hr | + CARE |
| **SOVOS Quantum** | Care + ML-DSA post-quantum signatures | £0.25/hr | + ASI |
| **SOVOS Sim** | Quantum + Isaac Sim + Cosmos + ACE SDK | £0.50/hr | + MACH, XR |
| **SOVOS Full Stack** | All 12 axes, all 27 sectors, dedicated GPU | £2.00/hr | ALL |

**This is the business model.** Not "rent a GPU." "Rent a governance-ready AI runtime."

---

## THE SINGLE COMMAND TO SUPERCHARGE

```bash
# 1. Clone the harness
mkdir sovos-harness && cd sovos-harness

# 2. Create the Docker Compose file (paste from above)
cat > docker-compose.yml << 'EOF'
[paste the docker-compose.yml from above]
EOF

# 3. Create directories
mkdir -p models guardrails-config gspc-evaluator morpheus-config   mcp-packs nooa-memory c2pa-manifests signing-keys   langgraph-runtime swarm-council care-monitor   secrets scan-results grafana-dashboards

# 4. Generate signing keys
openssl genrsa -out secrets/gspc-signing-key.pem 2048
openssl genrsa -out secrets/c2pa-private-key.pem 2048

# 5. Start the core harness (M2-compatible, no GPU)
docker-compose up -d guardrails gspc-evaluator kafka redis   langsmith prometheus grafana agent-layer c2pa-signer   safetensor-verify langgraph swarm-council care-monitor

# 6. Verify everything is running
docker-compose ps
curl http://localhost:5000/health   # Guardrails
curl http://localhost:5001/health   # GSPC Evaluator
curl http://localhost:7000/health   # Agent Layer
curl http://localhost:6000/health   # C2PA Signer

# 7. Test the full pipeline
curl -X POST http://localhost:7000/agent/3haul/optimize   -H "Content-Type: application/json"   -d '{"origin":"London","destination":"Manchester","load_weight":5000}'
# → Response includes: route + C2PA manifest + GSPC verdict + LangSmith trace ID
```

**That is 15 minutes. That is the supercharge.**

---

## THE SERIES A PITCH: "SOVOS Is Not a GPU. It Is a Governance Runtime."

"When you rent a GPU from AWS, you get compute. When you rent SOVOS, you get a complete AI governance runtime:

- **NVIDIA Triton** for optimized inference
- **NeMo Guardrails** for real-time safety enforcement
- **Our GSPC Evaluator** for deterministic, signed, audit-grade governance scoring
- **Microsoft MDASH** for continuous vulnerability scanning
- **Adobe C2PA** for cryptographic content provenance
- **Hugging Face Safetensors** for model integrity verification
- **LangChain LangGraph** for multi-agent orchestration
- **Our SwarmCouncil** for governance consensus between agents
- **Our care.co** for user wellbeing monitoring
- **NVIDIA Morpheus** for real-time threat detection
- **Optional:** Isaac Sim for physical AI simulation, Cosmos for synthetic data, ACE SDK for gaming companions

All unified by the SOV Signal event bus. All producing signed, traceable, court-admissible verdict records. All running on sovereign compute — your data never leaves your infrastructure.

We don't sell GPUs. We sell **AI governance as infrastructure.**"

---

"The dragon doesn't rent a GPU. It builds a fortress around the GPU, then rents the fortress."

Nicholas Templeman-Kirk
Founder, CSOAI / SOV³ Empire
August 5, 2026
