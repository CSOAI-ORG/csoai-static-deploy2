#!/usr/bin/env python3
"""Regional Compliance Mapper — IP-based regulation mapping for GOVBENCH

Detects user's region from IP and applies correct regulations:
  USA → NIST AI RMF, CCPA, SOC 2
  EU → EU AI Act, GDPR, NIS2, DORA
  UK → UK AI Bill, NCSC CAF, JSP 936, Cyber Essentials
  Singapore → AI Verify, PDPA
  Canada → AIDA, PIPEDA
  Australia → AI Ethics Framework, Privacy Act
  AUKUS → Pillar II requirements

Cross-walks map equivalent requirements across jurisdictions.
SOV can score compliance against ANY region's regulations.
"""

import json
import hashlib
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent


# ─── Regional Regulation Frameworks ─────────────────────────────────────────

REGIONAL_FRAMEWORKS = {
    "US": {
        "name": "United States",
        "frameworks": {
            "nist_ai_rmf": {
                "name": "NIST AI Risk Management Framework",
                "functions": ["GOVERN", "MAP", "MEASURE", "MANAGE"],
                "severity": "HIGH",
                "mandatory": False,
            },
            "ccpa": {
                "name": "California Consumer Privacy Act",
                "articles": ["Right to Know", "Right to Delete", "Right to Opt-Out", "Non-Discrimination"],
                "severity": "HIGH",
                "mandatory": True,
            },
            "soc2": {
                "name": "SOC 2 Type II",
                "criteria": ["Security", "Availability", "Processing Integrity", "Confidentiality", "Privacy"],
                "severity": "MEDIUM",
                "mandatory": False,
            },
            "hipaa": {
                "name": "HIPAA (Health)",
                "rules": ["Privacy Rule", "Security Rule", "Breach Notification"],
                "severity": "CRITICAL",
                "mandatory": True,  # if health data
            },
            "ferpa": {
                "name": "FERPA (Education)",
                "requirements": ["Consent", "Access Rights", "Directory Information"],
                "severity": "HIGH",
                "mandatory": True,  # if education data
            },
        },
    },
    "EU": {
        "name": "European Union",
        "frameworks": {
            "eu_ai_act": {
                "name": "EU AI Act",
                "articles": ["Art 5 (Prohibited)", "Art 6 (High-Risk)", "Art 9 (Risk Management)",
                             "Art 10 (Data Governance)", "Art 11 (Technical Docs)", "Art 12 (Logging)",
                             "Art 13 (Transparency)", "Art 14 (Human Oversight)", "Art 15 (Accuracy)",
                             "Art 50 (Transparency Obligations)"],
                "severity": "CRITICAL",
                "mandatory": True,
            },
            "gdpr": {
                "name": "GDPR",
                "articles": ["Art 5 (Principles)", "Art 6 (Lawfulness)", "Art 13-14 (Information)",
                             "Art 17 (Erasure)", "Art 22 (Automated Decisions)", "Art 25 (Privacy by Design)",
                             "Art 35 (DPIA)", "Art 83 (Penalties)"],
                "severity": "CRITICAL",
                "mandatory": True,
            },
            "nis2": {
                "name": "NIS2 Directive",
                "articles": ["Art 21 (Risk Management)", "Art 23 (Incident Reporting)",
                             "Art 24 (Business Continuity)", "Art 25 (Supply Chain Security)"],
                "severity": "HIGH",
                "mandatory": True,
            },
            "dora": {
                "name": "Digital Operational Resilience Act",
                "articles": ["Art 5-16 (ICT Risk Management)", "Art 17-23 (Incident Reporting)",
                             "Art 24-27 (Digital Operational Resilience Testing)", "Art 28-44 (Third-Party Risk)"],
                "severity": "HIGH",
                "mandatory": True,  # financial sector
            },
        },
    },
    "UK": {
        "name": "United Kingdom",
        "frameworks": {
            "uk_ai_bill": {
                "name": "UK AI Bill (Draft)",
                "requirements": ["Risk Management", "Transparency", "Human Oversight", "Accountability"],
                "severity": "HIGH",
                "mandatory": True,
            },
            "ncsc_caf": {
                "name": "NCSC Cyber Assessment Framework",
                "principles": ["A1 Risk Management", "A2 Engagement", "B1 Service Protection",
                               "B2 Identity", "B3 Data Security", "B4 System Security",
                               "B5 Resilience", "C1 Monitoring", "C2 Detection",
                               "D1 Response", "D2 Recovery"],
                "severity": "HIGH",
                "mandatory": False,
            },
            "jsp_936": {
                "name": "JSP 936 (UK Defence AI)",
                "sections": ["Safety Case", "Ethical Review", "Sovereignty Assessment",
                             "BFT Consensus", "Audit Trail", "Human Oversight"],
                "severity": "CRITICAL",
                "mandatory": True,  # defence sector
            },
            "cyber_essentials": {
                "name": "Cyber Essentials Plus",
                "controls": ["Firewalls", "Secure Configuration", "User Access Control",
                             "Malware Protection", "Patch Management"],
                "severity": "MEDIUM",
                "mandatory": True,
            },
        },
    },
    "SG": {
        "name": "Singapore",
        "frameworks": {
            "ai_verify": {
                "name": "AI Verify",
                "principles": ["Transparency", "Fairness", "Safety", "Accountability", "Human Oversight"],
                "severity": "HIGH",
                "mandatory": False,
            },
            "pdpa": {
                "name": "Personal Data Protection Act",
                "obligations": ["Consent", "Purpose Limitation", "Data Protection", "Breach Notification"],
                "severity": "HIGH",
                "mandatory": True,
            },
        },
    },
    "CA": {
        "name": "Canada",
        "frameworks": {
            "aida": {
                "name": "Artificial Intelligence and Data Act",
                "requirements": ["Risk Management", "Transparency", "Human Oversight", "Bias Mitigation"],
                "severity": "HIGH",
                "mandatory": True,
            },
            "pipeda": {
                "name": "Personal Information Protection",
                "principles": ["Accountability", "Consent", "Limiting Collection", "Accuracy",
                               "Safeguards", "Openness", "Individual Access"],
                "severity": "HIGH",
                "mandatory": True,
            },
        },
    },
    "AU": {
        "name": "Australia",
        "frameworks": {
            "ai_ethics": {
                "name": "AI Ethics Framework",
                "principles": ["Human-Centric", "Fairness", "Transparency", "Accountability",
                               "Safety", "Privacy", "Contestability"],
                "severity": "MEDIUM",
                "mandatory": False,
            },
            "privacy_act": {
                "name": "Privacy Act 1988",
                "apps": ["Openness", "Anonymity", "Data Quality", "Data Security",
                         "Access", "Correction"],
                "severity": "HIGH",
                "mandatory": True,
            },
        },
    },
    "AUKUS": {
        "name": "AUKUS Alliance",
        "frameworks": {
            "aukus_pillar_ii": {
                "name": "AUKUS Pillar II (AI/Cyber)",
                "requirements": ["Trustworthiness", "Interoperability", "Data Sharing",
                                 "Joint Training", "Sovereign Control", "Supply Chain Security"],
                "severity": "CRITICAL",
                "mandatory": True,  # defence partners
            },
        },
    },
}


# ─── Cross-Walk Tables ──────────────────────────────────────────────────────

CROSSWALK = {
    "risk_management": {
        "EU": "EU AI Act Art 9 — Risk Management System",
        "UK": "UK AI Bill — Risk Management Framework",
        "US": "NIST AI RMF — MAP function",
        "SG": "AI Verify — Risk Assessment Framework",
        "CA": "AIDA — Risk Management",
        "AU": "AI Ethics Framework — Safety",
        "AUKUS": "AUKUS Pillar II — Trustworthiness",
    },
    "data_governance": {
        "EU": "EU AI Act Art 10 + GDPR Art 5",
        "UK": "UK GDPR Art 5 — Data Protection Principles",
        "US": "CCPA — Right to Know + NIST GOVERN",
        "SG": "PDPA — Purpose Limitation",
        "CA": "PIPEDA — Limiting Collection",
        "AU": "Privacy Act — APP 3",
    },
    "transparency": {
        "EU": "EU AI Act Art 13 + Art 50",
        "UK": "UK AI Bill — Transparency Obligations",
        "US": "NIST AI RMF — COMMUNICATE function",
        "SG": "AI Verify — Transparency Standards",
        "CA": "AIDA — Transparency Requirements",
        "AU": "AI Ethics Framework — Transparency",
    },
    "human_oversight": {
        "EU": "EU AI Act Art 14 — Human Oversight",
        "UK": "UK AI Bill — Human Oversight Requirements",
        "US": "NIST AI RMF — Human Oversight",
        "SG": "AI Verify — Human Oversight Standards",
        "CA": "AIDA — Human Oversight Requirements",
        "AU": "AI Ethics Framework — Human-Centric",
    },
    "accuracy_robustness": {
        "EU": "EU AI Act Art 15 — Accuracy, Robustness, Cybersecurity",
        "UK": "UK Cyber Essentials — Security Requirements",
        "US": "NIST AI RMF — Performance Metrics",
        "SG": "Cybersecurity Act — Security Standards",
        "CA": "Cybersecure Canada — Security Requirements",
        "AU": "Privacy Act — APP 11 Data Security",
    },
    "incident_reporting": {
        "EU": "NIS2 Art 23 — Incident Reporting (24h/72h/30d)",
        "UK": "NCSC CAF — D1 Response",
        "US": "NIST AI RMF — MANAGE function",
        "SG": "PDPA — Breach Notification",
        "CA": "PIPEDA — Breach Notification",
        "AU": "Privacy Act — Notifiable Data Breaches",
    },
    "bias_fairness": {
        "EU": "EU AI Act Art 10 — Data Governance",
        "UK": "UK AI Bill — Fairness Requirements",
        "US": "NIST AI RMF — Fairness Metrics",
        "SG": "AI Verify — Fairness Principles",
        "CA": "AIDA — Bias Mitigation",
        "AU": "AI Ethics Framework — Fairness",
    },
    "audit_trail": {
        "EU": "EU AI Act Art 12 — Record-Keeping",
        "UK": "JSP 936 — Audit Trail",
        "US": "NIST AI RMF — MEASURE function",
        "SG": "AI Verify — Accountability",
        "CA": "PIPEDA — Accountability Principle",
        "AU": "AI Ethics Framework — Accountability",
    },
}


# ─── IP Geolocation ─────────────────────────────────────────────────────────

def detect_region_from_ip(ip: str = None) -> str:
    """Detect user's region from IP address."""
    if not ip:
        try:
            req = urllib.request.Request("https://api.ipify.org?format=json",
                                        headers={"User-Agent": "SOV-GovBench/1.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                ip = json.loads(r.read()).get("ip", "")
        except:
            return "US"  # Default to US

    try:
        req = urllib.request.Request(f"http://ip-api.com/json/{ip}",
                                    headers={"User-Agent": "SOV-GovBench/1.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            country = data.get("countryCode", "US")
            # Map to our regions
            region_map = {
                "US": "US", "GB": "UK", "DE": "EU", "FR": "EU", "IT": "EU",
                "ES": "EU", "NL": "EU", "PL": "EU", "SE": "EU", "DK": "EU",
                "FI": "EU", "AT": "EU", "BE": "EU", "IE": "EU", "PT": "EU",
                "SG": "SG", "CA": "CA", "AU": "AU", "NZ": "AUKUS",
                "JP": "SG", "KR": "SG",  # Asia-Pacific → SG framework
            }
            return region_map.get(country, "US")
    except:
        return "US"


# ─── Regional Compliance Scorer ─────────────────────────────────────────────

class RegionalComplianceScorer:
    """Score compliance against regional regulations."""

    def __init__(self, region: str = None):
        self.region = region or detect_region_from_ip()
        self.frameworks = REGIONAL_FRAMEWORKS.get(self.region, REGIONAL_FRAMEWORKS["US"])

    def score_response(self, response: str, question: str = "") -> Dict:
        """Score a response against all regional frameworks."""
        response_lower = response.lower()
        results = {}

        for fw_key, fw in self.frameworks["frameworks"].items():
            score = self._score_framework(response_lower, fw_key, fw)
            results[fw_key] = {
                "name": fw["name"],
                "score": round(score, 3),
                "pass": score >= 0.7,
                "severity": fw["severity"],
            }

        overall = sum(r["score"] for r in results.values()) / max(1, len(results))

        return {
            "region": self.region,
            "region_name": self.frameworks["name"],
            "frameworks": results,
            "overall_score": round(overall, 3),
            "pass": overall >= 0.7,
        }

    def _score_framework(self, response: str, fw_key: str, fw: Dict) -> float:
        """Score response against a single framework."""
        # Get keywords from framework
        keywords = self._get_keywords(fw_key, fw)
        if not keywords:
            return 0.5  # Default if no keywords

        matches = sum(1 for kw in keywords if kw in response)
        return min(0.99, 0.5 + (matches * 0.1))

    def _get_keywords(self, fw_key: str, fw: Dict) -> List[str]:
        """Get scoring keywords for a framework."""
        keyword_map = {
            "nist_ai_rmf": ["risk", "manage", "map", "measure", "govern", "framework"],
            "ccpa": ["privacy", "consumer", "right", "delete", "opt-out", "california"],
            "soc2": ["security", "availability", "integrity", "confidentiality", "audit"],
            "eu_ai_act": ["risk management", "transparency", "human oversight", "data governance", "prohibited"],
            "gdpr": ["data protection", "consent", "right", "erasure", "automated decision", "privacy"],
            "nis2": ["incident", "reporting", "risk management", "supply chain", "resilience"],
            "dora": ["operational resilience", "ict risk", "incident", "testing", "third-party"],
            "uk_ai_bill": ["risk management", "transparency", "human oversight", "accountability"],
            "ncsc_caf": ["cyber", "assessment", "risk", "security", "resilience", "monitoring"],
            "jsp_936": ["defence", "safety", "ethical", "sovereignty", "audit", "oversight"],
            "cyber_essentials": ["firewall", "secure", "access", "malware", "patch"],
            "ai_verify": ["transparency", "fairness", "safety", "accountability", "oversight"],
            "pdpa": ["data protection", "consent", "purpose", "breach", "notification"],
            "aida": ["risk management", "transparency", "bias", "human oversight", "ai"],
            "pipeda": ["privacy", "consent", "collection", "accuracy", "access", "accountability"],
            "ai_ethics": ["human-centric", "fairness", "transparency", "safety", "privacy"],
            "privacy_act": ["privacy", "openness", "data quality", "security", "access"],
            "aukus_pillar_ii": ["trustworthiness", "interoperability", "sovereign", "supply chain", "ai"],
            "hipaa": ["health", "privacy", "security", "breach", "phi"],
            "ferpa": ["education", "student", "records", "consent", "ferpa"],
        }
        return keyword_map.get(fw_key, [])

    def get_crosswalk(self, topic: str) -> Dict:
        """Get cross-walk mapping for a topic across all regions."""
        return CROSSWALK.get(topic, {})

    def get_applicable_frameworks(self) -> List[str]:
        """Get list of applicable frameworks for this region."""
        return list(self.frameworks["frameworks"].keys())


def main():
    """Demo: Score a response against regional regulations."""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  REGIONAL COMPLIANCE MAPPER                             ║")
    print("║  IP-based regulation mapping for GOVBENCH               ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Detect region
    region = detect_region_from_ip()
    scorer = RegionalComplianceScorer(region)

    print(f"\n─── DETECTED REGION ───")
    print(f"  Region: {region} ({scorer.frameworks['name']})")
    print(f"  Frameworks: {len(scorer.frameworks['frameworks'])}")

    # Show applicable frameworks
    print(f"\n─── APPLICABLE FRAMEWORKS ───")
    for fw_key, fw in scorer.frameworks["frameworks"].items():
        print(f"  {fw_key:20s} {fw['name']:40s} {fw['severity']}")

    # Show cross-walks
    print(f"\n─── CROSS-WALKS ───")
    for topic in ["risk_management", "transparency", "human_oversight"]:
        cw = scorer.get_crosswalk(topic)
        print(f"  {topic}:")
        for reg, req in cw.items():
            print(f"    {reg:5s}: {req}")

    # Score a sample response
    sample_response = """The AI system implements risk management in accordance with 
    NIST AI RMF and EU AI Act Article 9. We maintain transparency through documentation 
    and human oversight mechanisms. Data governance follows GDPR principles."""

    result = scorer.score_response(sample_response)
    print(f"\n─── COMPLIANCE SCORE ───")
    print(f"  Region: {result['region_name']}")
    print(f"  Overall: {result['overall_score']:.3f}")
    print(f"  Pass: {result['pass']}")
    for fw_key, fw_result in result["frameworks"].items():
        bar = "█" * int(fw_result["score"] * 20) + "░" * (20 - int(fw_result["score"] * 20))
        status = "✓" if fw_result["pass"] else "✗"
        print(f"  {status} {fw_key:20s} {bar} {fw_result['score']:.3f}")


if __name__ == "__main__":
    main()
