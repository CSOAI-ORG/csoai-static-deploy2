# SOV33 SECURITY IMPROVEMENT ACTION PLAN
## Consolidated from: filesystem scan, web research, gap analysis

Generated: 2026-07-26

---

## PRIORITY 1 — Immediate (this session)

### 1.1 Refusal Training Dataset ✅ DONE
- Built: `benchmark-results/training/refusal_corpus.jsonl` (207 pairs)
  - 84 generated (10 harmful categories × 8-10 examples each)
  - 10 Anthropic HH-RLHF
  - 10 sovereign_redline from task_registry
  - 7 helpful positive examples
- Built: `benchmark-results/training/Modelfile.refusal-sov33-14b`
- Built: `benchmark-results/training/Modelfile.refusal-sov33-master-v3`
- **Action**: `ollama create sov33-refusal -f <modelfile>` on RunPod when SSH back

### 1.2 Threat Intel MCP ✅ DONE
- Built: `kaggle/sov33_threat_intel_mcp.py` (4 feeds)
  - NVD (CVE lookup) — ✅ works without key
  - OTX (indicator enrichment) — ✅ works without key
  - ThreatFox (IOC sharing) — needs free key from abuse.ch
  - AbuseIPDB (IP reputation) — needs free key
- **Action**: Register free keys:
  - https://auth.abuse.ch/account/signup → THREATFOX_API_KEY
  - https://www.abuseipdb.com/account/api → ABUSEIPDB_API_KEY
  - https://otx.alienvault.com/api → OTX_API_KEY

### 1.3 Grader Fix ✅ DONE (from earlier)
- Fixed `sov33_e2e_orchestrator_v2.py` grader to handle:
  - "B) ATP production" format
  - "The answer is B" format
  - "Answer: B" format
  - "B" standalone letter

---

## PRIORITY 2 — Short-term (next session)

### 2.1 Deploy garak as CI/CD Gate
- **Source**: https://github.com/NVIDIA/garak (8.6k stars)
- **What**: LLM vulnerability scanner ("nmap for LLMs")
- **Action**: `pip install garak` + run against all model endpoints
- **Script**: Create `kaggle/sov33_garak_gate.py`
- **Integration**: Fail deployment if garak finds critical vulns

### 2.2 Deploy PyRIT for Continuous Red-Teaming
- **Source**: https://github.com/microsoft/PyRIT (4.2k stars)
- **What**: Automated multi-turn red-teaming framework
- **Action**: Install + configure to test all endpoints weekly
- **Integration**: Results → benchmark-results/pyrit_*.json

### 2.3 Llama Prompt Guard 2
- **Source**: Meta Purple Llama
- **What**: Real-time prompt injection detection
- **Action**: Deploy as input filter before model inference
- **Integration**: Reject flagged prompts before they reach the model

### 2.4 CyberSec Eval 3
- **Source**: Meta Purple Llama (MITRE ATT&CK mapped)
- **What**: Cybersecurity-specific LLM benchmarks
- **Action**: Run against all endpoints, track scores over time
- **Integration**: Results → sovereign_compliance benchmark suite

### 2.5 Sovereign Redline Refusal Training
- **Source**: Generated corpus + THUDM Safety-Prompts + Microsoft Do-Not-Answer
- **What**: Fine-tune a model to refuse harmful requests
- **Action**: 
  1. Run `sov33_refusal_trainer.py --source all --max-samples 500`
  2. Build Modelfile with refusal system prompt
  3. `ollama create sov33-refusal -f <modelfile>`
  4. Benchmark: should get >80% on sovereign_redline suite

---

## PRIORITY 3 — Medium-term (next week)

### 3.1 Deploy MISP as Central Threat Intel Platform
- **Source**: https://github.com/MISP/MISP (6.4k stars, AGPL-3.0)
- **What**: Complete threat intelligence sharing platform
- **Action**: Docker deploy on Oracle or RunPod
- **Integration**: Correlate all IOC feeds, connect to SOC

### 3.2 Implement C2PA for Article 50
- **Source**: https://github.com/contentauth/c2pa-rs
- **What**: Content provenance and watermarking (EU AI Act Art 50)
- **Action**: Generate C2PA manifests for all AI-generated content
- **Integration**: Add to output pipeline

### 3.3 liboqs for Quantum-Safe TLS
- **Source**: https://github.com/open-quantum-safe/liboqs (3k stars)
- **What**: PQC algorithms (ML-KEM-768, ML-DSA-65)
- **Action**: Deploy oqs-provider on TLS endpoints
- **Integration**: Hybrid PQC (X25519+ML-KEM) on all endpoints

### 3.4 UK AISI Inspect AI Evaluation
- **Source**: https://github.com/UKGovernmentBEIS/inspect_ai (2.4k stars)
- **What**: 200+ pre-built safety evaluations
- **Action**: Run full Inspect suite against all models
- **Integration**: Results → compliance documentation

---

## PRIORITY 4 — Long-term (next month)

### 4.1 EAT Pipeline Hardening
- Integrate garak/PyRIT into the EAT (Evaluate → Audit → Test) pipeline
- Auto-generate EU AI Act compliance reports from benchmark results
- C2PA sign all artifacts

### 4.2 Multi-Model Ensemble for Refusal
- Instead of one model refusing, use ensemble of:
  - Llama Prompt Guard 2 (classifier)
  - Custom refusal fine-tune
  - garak scanner
- Any one flagging → refuse the request

### 4.3 Live SOC Integration
- MISP + ThreatFox + AbuseIPDB → real-time IOC enrichment
- Automated incident reporting (NIS2 Art 23 compliance)
- SIGIL-attested incident chains

---

## KEY RESOURCES IDENTIFIED

### Refusal Training
- https://huggingface.co/datasets/Jammies-io/safety-refusal
- https://huggingface.co/datasets/Anthropic/hh-rlhf
- https://github.com/THUDM/Safety-Prompts (100K+ bilingual)
- https://github.com/microsoft/Do-Not-Answer

### Red-Teaming Tools
- https://github.com/microsoft/PyRIT (4.2k stars, MIT)
- https://github.com/NVIDIA/garak (8.6k stars, Apache 2.0)
- https://github.com/meta-llama/PurpleLlama (4.3k stars)

### Threat Intelligence
- https://threatfox.abuse.ch/api/ (free auth key)
- https://abuseipdb.com/api (free 1000/day)
- https://otx.alienvault.com (free API key)
- NVD: https://services.nvd.nist.gov (no key needed)

### AI Safety Frameworks
- https://github.com/UKGovernmentBEIS/inspect_ai (UK AISI)
- https://github.com/EleutherAI/lm-evaluation-harness (13.4k stars)
- https://artificialintelligenceact.eu (EU AI Act compliance checker)

### Quantum-Safe
- https://github.com/open-quantum-safe/liboqs (3k stars)
- https://github.com/open-quantum-safe/oqs-provider (OpenSSL provider)
- https://github.com/open-quantum-safe/liboqs-python (Python bindings)

### Content Provenance
- https://c2pa.org | https://github.com/contentauth (C2PA standard)
- https://github.com/contentauth/c2pa-rs (Rust implementation)

---

## CURRENT SECURITY STACK STATUS

### ✅ Working
- 301 security-flagged HTML pages
- Ed25519 SIGIL chain
- BFT-33 quorum (23/33)
- 12-vector adversarial framework (OWASP LLM Top 10 + sovereign-chain)
- EU AI Act Article 50 C2PA (spec ready)
- NCSC Cyber Essentials Plus pre-fill
- Quantum-safe spec (ML-DSA-65 + ML-KEM-768, dual-signing)
- Refusal training corpus (207 pairs)
- Threat intel MCP (NVD + OTX working without keys)

### ⚠️ Needs Keys
- ThreatFox (free: https://auth.abuse.ch/account/signup)
- AbuseIPDB (free: https://www.abuseipdb.com/account/api)
- OTX (free: https://otx.alienvault.com/api)

### ❌ Not Yet Deployed
- garak (CI/CD gate)
- PyRIT (continuous red-teaming)
- Llama Prompt Guard 2 (input filter)
- CyberSec Eval 3 (MITRE ATT&CK)
- MISP (threat intel platform)
- C2PA (content provenance)
- liboqs (quantum-safe TLS)
- Inspect AI (200+ safety evals)

### 🔴 Critical Gap
- sovereign_redline benchmark: **0% best** across all models
- No model properly refuses harmful requests
- Refusal Modelfile created but not deployed/tested yet

---

## FILES CREATED THIS SESSION

| File | Purpose |
|---|---|
| `kaggle/sov33_refusal_trainer.py` | Build refusal training corpus from 5 sources |
| `kaggle/sov33_threat_intel_mcp.py` | Live threat intel MCP (NVD + OTX + ThreatFox + AbuseIPDB) |
| `benchmark-results/training/refusal_corpus.jsonl` | 207 refusal pairs |
| `benchmark-results/training/refusal_corpus_stats.json` | Corpus statistics |
| `benchmark-results/training/Modelfile.refusal-sov33-14b` | Ollama refusal Modelfile |
| `benchmark-results/training/Modelfile.refusal-sov33-master-v3` | Ollama refusal Modelfile |
| `benchmark-results/SECURITY_DOSSIER.md` | Full security audit dossier |
| `benchmark-results/DOSSIER.md` | Full model performance dossier |
| `kaggle/sov33_e2e_funnel.py` | Improved: gold-verified context injection |
| `kaggle/sov33_asi_evolve.py` | Improved: _matches_gold filter |
| `kaggle/sov33_local_swarm.py` | New: local + API swarm runner |
| `kaggle/sov33_swarm_loop.py` | New: adaptive context strategy |
| `kaggle/sov33_vol_sync.py` | New: multi-site backup orchestrator |
| `swarm_resume.sh` | Auto-reconnect to RunPod when SSH back |
| `kaggle/sov33_e2e_dashboard.py` | Live HTML dashboard |
| `kaggle/sov33_e2e_compare.py` | Leaderboard across runs |
| `kaggle/sov33_e2e_corpus.py` | Persistent consensus corpus builder |
| `kaggle/sov33_funnel_history.py` | Per-model improvement trends |