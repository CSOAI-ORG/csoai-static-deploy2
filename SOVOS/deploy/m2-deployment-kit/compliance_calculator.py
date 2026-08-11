#!/usr/bin/env python3
"""
compliance_calculator.py — EU AI Act risk classification calculator.

Usage:
  python3 compliance_calculator.py --description "AI system for hiring"
  python3 compliance_calculator.py --description "Chatbot for customer service" --format json
"""
import json, sys, argparse

RISK_LEVELS = {
    "prohibited": {
        "description": "AI practices banned under Article 5",
        "examples": ["social scoring", "subliminal manipulation", "untargeted facial recognition scraping"],
        "penalty": "up to €35M or 7% global annual turnover"
    },
    "high-risk": {
        "description": "AI systems under Annex III with strict obligations",
        "examples": ["biometric identification", "credit scoring", "hiring decisions", "law enforcement"],
        "penalty": "up to €15M or 3% global annual turnover",
        "obligations": ["risk management", "data governance", "technical documentation", "logging", "transparency", "human oversight", "accuracy testing"]
    },
    "limited-risk": {
        "description": "AI with transparency obligations (Articles 50-52)",
        "examples": ["chatbots", "deepfakes", "emotion recognition", "content generation"],
        "penalty": "up to €7.5M or 1% global annual turnover",
        "obligations": ["disclosure of AI nature", "labelling of AI-generated content"]
    },
    "minimal-risk": {
        "description": "Most AI systems with no specific obligations",
        "examples": ["spam filters", "recommendation systems", "video games"],
        "penalty": "N/A",
        "obligations": []
    }
}

HIGH_RISK_KEYWORDS = [
    "hiring", "recruitment", "credit", "loan", "insurance", "scoring",
    "biometric", "facial recognition", "law enforcement", "court", "judicial",
    "migration", "border", "critical infrastructure", "education", "assessment",
    "medical", "diagnosis", "treatment", "pharmaceutical"
]

PROHIBITED_KEYWORDS = [
    "social scoring", "subliminal", "manipulation", "exploitation",
    "vulnerability", "untargeted scraping", "facial recognition"
]

LIMITED_KEYWORDS = [
    "chatbot", "customer service", "deepfake", "emotion recognition",
    "content generation", "text generation", "image generation"
]

def classify(description: str) -> str:
    """Classify AI system risk level based on description."""
    desc_lower = description.lower()

    for kw in PROHIBITED_KEYWORDS:
        if kw in desc_lower:
            return "prohibited"

    for kw in HIGH_RISK_KEYWORDS:
        if kw in desc_lower:
            return "high-risk"

    for kw in LIMITED_KEYWORDS:
        if kw in desc_lower:
            return "limited-risk"

    return "minimal-risk"

def main():
    parser = argparse.ArgumentParser(description="EU AI Act Risk Classifier")
    parser.add_argument("--description", required=True, help="AI system description")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    level = classify(args.description)

    if args.format == "json":
        print(json.dumps({
            "risk_level": level,
            "details": RISK_LEVELS[level],
            "description": args.description
        }, indent=2))
    else:
        print(f"Risk Level: {level.upper()}")
        print(f"Description: {RISK_LEVELS[level]['description']}")
        print(f"Penalty: {RISK_LEVELS[level]['penalty']}")
        if RISK_LEVELS[level]['obligations']:
            print(f"Obligations: {', '.join(RISK_LEVELS[level]['obligations'])}")

if __name__ == "__main__":
    main()
