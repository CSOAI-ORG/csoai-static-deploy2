#!/usr/bin/env python3
"""
jurisdiction_mapper.py — Map EU AI Act articles to UK, Singapore, Canada, US NIST equivalents.

Usage:
  python3 jurisdiction_mapper.py --article 9
  python3 jurisdiction_mapper.py --article 14 --format json
"""
import json, sys, argparse

CROSS_JURISDICTION_MAP = {
    9: {
        "eu_ai_act": "Article 9 — Risk Management System",
        "uk": "UK AI Bill (draft) — Risk management framework",
        "singapore": "AI Verify — Risk assessment framework",
        "canada": "AIDA (Artificial Intelligence and Data Act) — Risk management",
        "us_nist": "NIST AI RMF — MAP function"
    },
    10: {
        "eu_ai_act": "Article 10 — Data and Data Governance",
        "uk": "UK GDPR Article 5 — Data protection principles",
        "singapore": "PDPA — Personal Data Protection Act",
        "canada": "PIPEDA — Personal Information Protection",
        "us_nist": "NIST AI RMF — GOVERN function"
    },
    11: {
        "eu_ai_act": "Article 11 — Technical Documentation",
        "uk": "UK AI Bill — Transparency requirements",
        "singapore": "AI Verify — Documentation standards",
        "canada": "AIDA — Documentation requirements",
        "us_nist": "NIST AI RMF — Document AI systems"
    },
    12: {
        "eu_ai_act": "Article 12 — Record-Keeping / Logging",
        "uk": "UK GDPR Article 30 — Records of processing",
        "singapore": "PDPA — Accountability",
        "canada": "PIPEDA — Accountability principle",
        "us_nist": "NIST AI RMF — Monitoring"
    },
    13: {
        "eu_ai_act": "Article 13 — Transparency",
        "uk": "UK AI Bill — Transparency obligations",
        "singapore": "AI Verify — Transparency standards",
        "canada": "AIDA — Transparency requirements",
        "us_nist": "NIST AI RMF — COMMUNICATE function"
    },
    14: {
        "eu_ai_act": "Article 14 — Human Oversight",
        "uk": "UK AI Bill — Human oversight requirements",
        "singapore": "AI Verify — Human oversight standards",
        "canada": "AIDA — Human oversight requirements",
        "us_nist": "NIST AI RMF — Human oversight"
    },
    15: {
        "eu_ai_act": "Article 15 — Accuracy, Robustness and Cybersecurity",
        "uk": "UK Cyber Essentials — Security requirements",
        "singapore": "Cybersecurity Act — Security standards",
        "canada": "Cybersecure Canada — Security requirements",
        "us_nist": "NIST AI RMF — Performance metrics"
    },
    50: {
        "eu_ai_act": "Article 50 — Transparency Obligations (2 Aug 2026)",
        "uk": "UK AI Bill — Transparency provisions",
        "singapore": "AI Verify — Transparency framework",
        "canada": "AIDA — Transparency provisions",
        "us_nist": "NIST AI RMF — Communication"
    }
}

def main():
    parser = argparse.ArgumentParser(description="Jurisdiction Mapper")
    parser.add_argument("--article", type=int, required=True, help="EU AI Act article number")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    mapping = CROSS_JURISDICTION_MAP.get(args.article)
    if not mapping:
        print(f"No mapping found for Article {args.article}")
        sys.exit(1)

    if args.format == "json":
        print(json.dumps({"article": args.article, "mapping": mapping}, indent=2))
    else:
        print(f"EU AI Act Article {args.article}:")
        for jurisdiction, requirement in mapping.items():
            print(f"  {jurisdiction:15s}: {requirement}")

if __name__ == "__main__":
    main()
