# GovBench — Open Standard for AI Governance

## Overview
GovBench is an open standard for evaluating AI models across 12 dimensions of governance compliance. It provides a comprehensive framework for assessing AI safety, security, ethics, and compliance.

## 12 Dimensions of AI Governance

### 1. Governance
- EU AI Act compliance
- ISO 42001 alignment
- NIST AI RMF mapping
- OECD AI Principles

### 2. Safety
- Harmful content refusal
- Weapon/terrorism refusal
- Child safety
- Vulnerable populations

### 3. Security
- Prompt injection resistance
- Red-team resilience
- Adversarial robustness
- Supply chain security

### 4. Defence
- AUKUS compliance
- NCSC CAF alignment
- NATO standards
- National security

### 5. Ethics
- Fairness and bias
- Transparency
- Accountability
- Human oversight

### 6. Privacy
- GDPR compliance
- Data protection
- Consent management
- Right to erasure

### 7. Robustness
- Jailbreak resistance
- System prompt protection
- Adversarial resilience
- Distribution shift handling

### 8. Transparency
- Model cards
- Explainability
- Interpretability
- Audit trails

### 9. Fairness
- Demographic parity
- Equal opportunity
- Individual fairness
- Bias detection

### 10. Accountability
- Clear responsibility
- Incident reporting
- Remediation processes
- Appeal mechanisms

### 11. Sovereignty
- Data residency
- National control
- Strategic autonomy
- Supply chain security

### 12. Evolution
- Continuous improvement
- Feedback integration
- Community contribution
- Open standards

## Evaluation Methodology

### Context Injection
Domain-specific training data in the system prompt improves weak dimensions. Defence jumped from 16.7% to 100% with AUKUS/NCSC/NATO knowledge.

### Flexible Grading
- Keyword matching for content questions
- Refusal detection for safety questions
- Bias detection for fairness questions
- Robustness testing for jailbreak resistance

### Scoring
- Each dimension scored 0-100%
- Overall score = average of all dimensions
- Certification levels:
  - Platinum: 95-100%
  - Gold: 85-94%
  - Silver: 70-84%
  - Bronze: 50-69%
  - Uncertified: <50%

## Usage

### Evaluate a Model
```bash
python3 govbench_eval.py --model meta/llama-3.1-8b-instruct --provider nvidia
```

### Run Full Evaluation
```bash
python3 govbench_eval.py --all
```

### View Leaderboard
```bash
python3 govbench_eval.py --leaderboard
```

### Public API
```bash
curl -X POST https://govbench.pages.dev/api/govbench
```

## Training Data

### Defence Corpus
12 Q&A pairs covering AUKUS, NCSC CAF, NATO DIANA, JSP 936, Five Eyes, DAIC, DASA, G-Cloud 14, Cyber Essentials.

### Sovereignty Corpus
12 Q&A pairs covering data sovereignty, UK AISI, UK AI Strategy, DSP, CCS, UK DPA 2018, ICO.

### Ethics Corpus
12 Q&A pairs covering fairness, transparency, accountability, human oversight, DPIA, right to erasure, privacy by design, OECD AI Principles, NIST AI RMF, ISO 42001, EU AI Act.

## Integration

### Routers
- sov_router.py — Main SOV router
- unified_router.py — Unified router with Water/Milk/Honey states
- sov4_router.py — SOV4 fluid router

### Pipelines
- govbench_eval.py — Full evaluation suite
- eat_govbench.py — EAT for weak dimensions
- sov_orchestrator.py — Unified orchestrator

### Models
- Modelfile.sov-ultimate-sovereign — Strongest sovereign
- Modelfile.sov33-evolved-v4 — Evolved model
- Modelfile.sov-unified — Unified model

## Architecture

### SOV-Space
- Sandwich Brain: 6,912 model slots
- Stigmergy: Bee/ant communication
- Spine Drum: Heartbeat synchronization
- G-Space: Graph Neural Network
- BFT Quorum: 23/33 consensus
- SIGIL Chain: Immutable audit trail

### Layer 0 Integration
All components wired together through sov_orchestrator.py:
- Routers → Pipelines
- Training data → Models
- Stigmergy → Routers
- GovBench → Continuous benchmarking
- All APIs → Unified interface

## License
MIT License — Open for anyone to use, modify, and distribute.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Contact
- GitHub: https://github.com/CSOAI-ORG/csoai-static-deploy2
- Leaderboard: https://govbench.pages.dev
- API: https://govbench.pages.dev/api/govbench
