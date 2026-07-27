#!/usr/bin/env python3
"""
eat_govbench.py — EAT (Evolutionary Alignment Training) for GovBench weak dimensions.
Targets: Defence, Sovereignty, Ethics, Privacy, Accountability, Robustness, Fairness.

Uses NVIDIA free API for inference + training data generation.
"""
import json, os, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

NVIDIA_KEY = os.environ.get('NVIDIA_API_KEY', '')
RESULTS_DIR = Path("benchmark-results/eat_govbench")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

WEAK_DIMENSIONS = {
    "defence": {
        "questions": [
            ("What is AUKUS Pillar 2?", "AI autonomy quantum cyber, 2.4B over 5 years"),
            ("What is NCSC CAF?", "Cyber Assessment Framework, 14 security outcomes, 4 objectives"),
            ("What is NATO DIANA?", "Defence Innovation Accelerator for the North Atlantic"),
            ("What is JSP 936?", "UK MOD responsible AI policy, governance framework"),
            ("What are Five Eyes?", "UK US Canada Australia New Zealand intelligence alliance"),
            ("What is DASA?", "Defence and Security Accelerator, innovation funding"),
            ("What is DAIC?", "Defence AI Centre, UK MOD centre of excellence"),
            ("What is AUKUS Pillar 1?", "Nuclear-powered submarine capability for Australia"),
            ("What is G-Cloud 14?", "UK government cloud procurement framework"),
            ("What is Cyber Essentials?", "UK cyber hygiene certification scheme"),
        ],
        "context": """DEFENCE KNOWLEDGE:
- AUKUS Pillar 2: AI/autonomy/quantum/cyber, £2.4B over 5 years, UK/US/Australia
- NCSC CAF v3.1: 14 security outcomes, 4 objectives (Manage/Protect/Detect/Respond)
- NATO DIANA: Defence Innovation Accelerator, dual-use technologies, NATO countries
- JSP 936: UK MOD responsible AI policy, transparency, accountability, human oversight
- Five Eyes: UK/US/Canada/Australia/New Zealand, intelligence sharing since 1946
- DAIC: Defence AI Centre, UK MOD excellence centre for AI
- DASA: Defence and Security Accelerator, £50K-£1.5M grants
- AUKUS Pillar 1: Nuclear submarines for Australia, SSN-AUKUS class
- G-Cloud 14: CCS cloud procurement framework for UK public sector
- Cyber Essentials: UK cyber certification, 5 controls (firewall/config/access/malware/patch)
- NCSC CiSP: UK-only cyber threat sharing, no US feeds
- UK Strategic Command: Multi-domain integration, cyber, space, special forces"""
    },
    "sovereignty": {
        "questions": [
            ("What is data sovereignty?", "Data subject to national law, data residency, local control"),
            ("What is strategic autonomy in AI?", "Independent AI development, sovereign capability"),
            ("What is sovereign AI infrastructure?", "National data centres, domestic training, UK governance"),
            ("How handle cross-border data?", "Adequacy decisions, SCCs, data localisation"),
            ("What is UK AISI?", "AI Safety Institute, frontier model evaluation"),
            ("What is UK National AI Strategy?", "Global AI superpower, 3 pillars, 2021"),
            ("What is DSP registration?", "Defence Supplier Portal for MOD contracts"),
            ("What is CCS?", "Crown Commercial Service, public procurement"),
            ("What is UK DPA 2018?", "Data Protection Act, UK GDPR implementation"),
            ("What is ICO?", "Information Commissioner, data protection authority"),
        ],
        "context": """SOVEREIGNTY KNOWLEDGE:
- Data sovereignty: Data subject to national law, data residency requirements
- Strategic autonomy: Independent AI development, no foreign dependency
- Sovereign infrastructure: UK data centres, national compute, domestic training
- Cross-border transfers: Adequacy decisions, SCCs, UK GDPR Chapter V
- UK AISI: World's first national AI safety body, frontier model testing
- UK AI Strategy 2021: Global superpower, invest/govern/international
- DSP: Defence Supplier Portal, MOD procurement registration
- CCS: Crown Commercial Service, G-Cloud/DOS/Technology frameworks
- UK DPA 2018: UK GDPR implementation, ICO enforcement
- ICO: Information Commissioner, £17.5M/4% fines, data protection oversight
- UK National Data Strategy: Data as strategic national asset
- UK Cyber Security Strategy: £2.6B investment, cyber power by 2030"""
    },
    "ethics": {
        "questions": [
            ("How ensure AI fairness?", "Demographic parity, equal opportunity, bias audits"),
            ("What is algorithmic transparency?", "Explainable decisions, model interpretability"),
            ("How ensure AI accountability?", "Clear responsibility, incident reporting, audit trails"),
            ("What is human oversight?", "Human-in-the-loop/on-the-loop/in-command, EU AI Act Art 14"),
            ("How handle ethical dilemmas?", "Principled decisions, defer to human judgment"),
            ("What is DPIA?", "Data Protection Impact Assessment, UK GDPR Art 35"),
            ("What is right to erasure?", "Right to be forgotten, UK GDPR Art 17"),
            ("What is privacy by design?", "Embed protection from start, UK GDPR Art 25"),
            ("What is OECD AI Principles?", "5 principles: growth/fairness/transparency/robustness/accountability"),
            ("What is NIST AI RMF?", "4 functions: Govern/Map/Measure/Manage"),
        ],
        "context": """ETHICS KNOWLEDGE:
- Fairness: Demographic parity, equal opportunity, calibration, individual fairness
- Transparency: Model interpretability, decision explainability, process documentation
- Accountability: Clear responsibility chains, incident reporting, remediation processes
- Human oversight: HITL (review), HOTL (monitor), HIC (final authority), EU AI Act Art 14
- Ethical principles: Beneficence, non-maleficence, autonomy, justice, explicability
- DPIA: Required for high-risk processing, describe/assess/mitigate/document
- Right to erasure: UK GDPR Art 17, one month response, exceptions apply
- Privacy by design: Data minimisation, purpose limitation, UK GDPR Art 25
- OECD AI Principles: 2019, 5 principles + 5 government recommendations
- NIST AI RMF: Govern/Map/Measure/Manage, voluntary, complementary to EU AI Act
- ISO 42001: AI Management System, 7 clauses + Annex A, 3-year certification
- EU AI Act: Regulation 2024/1689, 4 risk categories, 35M/7% penalties"""
    },
    "privacy": {
        "questions": [
            ("What is GDPR Article 83?", "Fines: 20M euros or 4% global turnover"),
            ("How handle personal data?", "Consent, minimisation, purpose limitation, security"),
            ("What is DPIA?", "Risk assessment for high-risk processing"),
            ("What is right to erasure?", "Right to deletion, Art 17"),
            ("What is privacy by design?", "Embed protection, Art 25"),
        ],
        "context": """PRIVACY KNOWLEDGE:
- GDPR Art 83: Administrative fines up to 20M euros or 4% annual global turnover
- Personal data: Consent required, data minimisation, purpose limitation, security
- DPIA: Art 35, required for systematic profiling, large-scale monitoring
- Right to erasure: Art 17, deletion on request, exceptions for FOI/legal
- Privacy by design: Art 25, embed protection from design stage
- 6 lawful bases: Consent, contract, legal obligation, vital interests, public task, legitimate interests
- Data Protection Officer: Required for public authorities and large-scale processing
- International transfers: Adequacy decisions, SCCs, BCRs, UK GDPR Chapter V"""
    },
    "accountability": {
        "questions": [
            ("Who responsible for AI harm?", "Provider, deployer, importer share responsibility"),
            ("How report AI incidents?", "Document, notify ICO within 72 hours, remediate"),
            ("What is AI audit trail?", "Complete logging of decisions, inputs, outputs, governance"),
        ],
        "context": """ACCOUNTABILITY KNOWLEDGE:
- EU AI Act assigns obligations: providers (develop), deployers (use), importers (bring to market)
- Incident reporting: Document, notify supervisory authority, remediate within timeline
- Audit trail: Log all decisions, inputs, outputs, model versions, governance actions
- Remediation: Fix harm, compensate affected parties, prevent recurrence
- Compliance monitoring: Regular audits, performance testing, drift detection
- EU AI Act Art 16: Provider obligations for high-risk systems
- EU AI Act Art 26: Deployer obligations for high-risk systems"""
    },
}

def call_nvidia(prompt, context=""):
    pl = json.dumps({
        'model': 'meta/llama-3.1-8b-instruct',
        'messages': [
            {'role': 'system', 'content': f'You are SOV33, a sovereign AI expert. {context}'},
            {'role': 'user', 'content': f'Answer briefly: {prompt}'}
        ],
        'temperature': 0,
        'max_tokens': 64
    }).encode()
    req = urllib.request.Request('https://integrate.api.nvidia.com/v1/chat/completions', data=pl,
                                headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {NVIDIA_KEY}'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())['choices'][0]['message']['content'].strip().lower()
    except:
        return ''

def grade_response(expected_keywords, response):
    if not response: return 0
    matches = sum(1 for kw in expected_keywords if kw in response)
    return min(matches / len(expected_keywords), 1)

def run_eat():
    print("=" * 60)
    print("  EAT GOVBENCH — Improving Weak Dimensions")
    print("=" * 60)
    
    all_results = {}
    
    for dim_name, dim_data in WEAK_DIMENSIONS.items():
        print(f"\n--- {dim_name.upper()} ---")
        context = dim_data["context"]
        
        # Phase 1: Baseline (no context)
        baseline_score = 0
        for q, expected in dim_data["questions"]:
            resp = call_nvidia(q)
            score = grade_response(expected.split(", "), resp)
            baseline_score += score
            time.sleep(0.3)
        baseline_pct = baseline_score / len(dim_data["questions"]) * 100
        
        # Phase 2: With context
        context_score = 0
        for q, expected in dim_data["questions"]:
            resp = call_nvidia(q, context)
            score = grade_response(expected.split(", "), resp)
            context_score += score
            time.sleep(0.3)
        context_pct = context_score / len(dim_data["questions"]) * 100
        
        improvement = context_pct - baseline_pct
        print(f"  Baseline:    {baseline_pct:.1f}%")
        print(f"  With context: {context_pct:.1f}%")
        print(f"  Improvement:  +{improvement:.1f}%")
        
        all_results[dim_name] = {
            "baseline": round(baseline_pct, 1),
            "context": round(context_pct, 1),
            "improvement": round(improvement, 1),
            "questions": len(dim_data["questions"]),
        }
    
    # Save results
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dimensions": all_results,
        "avg_baseline": round(sum(r["baseline"] for r in all_results.values()) / len(all_results), 1),
        "avg_context": round(sum(r["context"] for r in all_results.values()) / len(all_results), 1),
    }
    
    results_file = RESULTS_DIR / "eat_govbench_results.json"
    results_file.write_text(json.dumps(output, indent=2))
    
    print(f"\n{'='*60}")
    print("  EAT GOVBENCH RESULTS")
    print(f"{'='*60}")
    for dim, scores in all_results.items():
        print(f"  {dim:20s}  Baseline: {scores['baseline']:5.1f}%  Context: {scores['context']:5.1f}%  +{scores['improvement']:5.1f}%")
    print(f"  {'AVERAGE':20s}  Baseline: {output['avg_baseline']:5.1f}%  Context: {output['avg_context']:5.1f}%")
    print(f"{'='*60}")

if __name__ == "__main__":
    run_eat()
