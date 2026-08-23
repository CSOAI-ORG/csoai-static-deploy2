#!/usr/bin/env python3
"""FRAMEWORKS DRUM — living catalog builder.

Folds the estate seed (this file) + web-mining outputs in _mining/ into
catalog.json and per-kind cards (frameworks/, charters/, regulations/, articles/).

Usage:
  python3 build_catalog.py            # write catalog.json + cards (idempotent)
  python3 build_catalog.py --no-cards # catalog.json only
"""
import datetime
import json
import os
import re
import sys

PACK = os.path.dirname(os.path.abspath(__file__))
MINING = os.path.join(PACK, "_mining")
CATALOG = os.path.join(PACK, "catalog.json")
KIND_DIRS = {"framework": "frameworks", "charter": "charters", "regulation": "regulations", "article": "articles", "sector": "sectors"}

# ---------------------------------------------------------------------------
# ESTATE SEED — items mined from the Mac estate (sources recorded per item).
# id: slug · kind: framework|charter|regulation|article · binding: bool|None
# ---------------------------------------------------------------------------
SEED = [
    # --- FRAMEWORKS (governance / management / standards) -------------------
    {"id": "nist-ai-rmf", "name": "NIST AI RMF 1.0", "kind": "framework", "issuer": "NIST", "region": "US", "binding": False, "status": "active", "effective": "Jan 2023", "description": "Voluntary framework — Govern / Map / Measure / Manage; AI 600-1 adds GenAI profile; Cyber AI Profile (IR 8596) in draft 2026.", "estate": "clawd/csoai-dashboard-master/content/blog/frameworks/nist-ai-risk-management-framework.md"},
    {"id": "iso-42001", "name": "ISO/IEC 42001", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "Dec 2023", "description": "AI Management System standard — PDCA cycle, 10 clauses + Annex A controls.", "estate": "clawd/csoai-org-v2 (frameworks/iso-42001)"},
    {"id": "iso-42005", "name": "ISO/IEC 42005", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2025", "description": "AI Impact Assessment standard.", "estate": "clawd/csoai-org-v2 (frameworks/iso-42005)"},
    {"id": "oecd-ai-principles", "name": "OECD AI Principles", "kind": "framework", "issuer": "OECD", "region": "OECD", "binding": False, "status": "active", "effective": "2019 (updated 2024)", "description": "5 principles + 5 recommendations; OECD/LEGAL/0449.", "estate": "clawd/csoai-org-v2 (frameworks/oecd-ai-principles)"},
    {"id": "unesco-ai-ethics", "name": "UNESCO AI Ethics Recommendation", "kind": "framework", "issuer": "UNESCO", "region": "UNESCO", "binding": False, "status": "active", "effective": "Nov 2021", "description": "Values, principles, policy actions — adopted by 193 member states.", "estate": "clawd/csoai-org-v2 (frameworks/unesco-ai-ethics)"},
    {"id": "uk-aisi", "name": "UK AISI Evaluations", "kind": "framework", "issuer": "UK AI Safety Institute", "region": "UK", "binding": False, "status": "active", "effective": "2024", "description": "UK AI Safety Institute evaluation framework.", "estate": "clawd/csoai-dashboard-master (frameworks/uk-aisi)"},
    {"id": "singapore-model-ai-governance", "name": "Singapore Model AI Governance Framework", "kind": "framework", "issuer": "IMDA", "region": "SG", "binding": False, "status": "active", "effective": "2019 (GenAI 2024)", "description": "Model AI Governance Framework + GenAI Framework + agentic-AI guidance (MAS/IMDA).", "estate": "clawd/csoai-dashboard-master/content/blog/frameworks/singapore-model-ai-governance-framework.md"},
    {"id": "australia-ai-ethics", "name": "Australia AI Ethics Framework", "kind": "framework", "issuer": "DISR", "region": "AU", "binding": False, "status": "active", "effective": "2019 (10 guardrails 2024)", "description": "8 ethics principles; Voluntary AI Safety Standard 10 guardrails (Sept 2024).", "estate": "clawd/csoai-dashboard-master/content/blog/frameworks/australia-ai-ethics-framework.md"},
    {"id": "india-ai-governance", "name": "India AI Governance Framework", "kind": "framework", "issuer": "MeitY", "region": "IN", "binding": False, "status": "active", "effective": "2024", "description": "Advisory AI governance guidelines (non-binding); IT Amendment Rules 2026 are the binding part.", "estate": "clawd/csoai-dashboard-master/content/blog/frameworks/india-ai-governance-framework.md"},
    {"id": "uk-ai-safety-framework", "name": "UK AI Safety Framework", "kind": "framework", "issuer": "UK AISI", "region": "UK", "binding": False, "status": "active", "effective": "2024", "description": "Safety framework for advanced AI — capability + alignment evaluations.", "estate": "clawd/csoai-dashboard-master/content/blog/frameworks/uk-ai-safety-framework.md"},
    {"id": "ieee-ethically-aligned-design", "name": "IEEE Ethically Aligned Design", "kind": "framework", "issuer": "IEEE", "region": "IEEE", "binding": False, "status": "active", "effective": "2019 (EAD v2)", "description": "EAD v2 + IEEE P7000 series (P7001 transparency, P7002 data privacy, P7003 bias).", "estate": "clawd/csoai-org-v2 (frameworks/ieee-ethically-aligned-design)"},
    {"id": "g7-g20-ai-principles", "name": "G7 / G20 AI Principles", "kind": "framework", "issuer": "G7 / G20", "region": "Intergovernmental", "binding": False, "status": "active", "effective": "2019 / Hiroshima 2023", "description": "International cooperation frameworks — Hiroshima Process + Bletchley.", "estate": "clawd/csoai-org-v2 (frameworks/g7-g20-ai-principles)"},
    {"id": "master-unified-crosswalk", "name": "Master Unified Crosswalk", "kind": "framework", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026", "description": "All frameworks consolidated into one crosswalk — single source of truth for compliance teams (original CSOAI work).", "estate": "clawd/csoai-org-v2 (frameworks/master-unified-crosswalk)"},
    {"id": "anthropic-constitutional-ai", "name": "Anthropic Constitutional AI", "kind": "framework", "issuer": "Anthropic", "region": "AI Company", "binding": False, "status": "active", "effective": "Dec 2022", "description": "Constitutional AI — written principles replace preference labels; Bai et al. 2022 (arXiv:2212.08073).", "estate": "clawd/csoai-org-v2 (frameworks/anthropic-constitutional-ai)"},
    {"id": "openai-model-spec", "name": "OpenAI Model Spec", "kind": "framework", "issuer": "OpenAI", "region": "AI Company", "binding": False, "status": "active", "effective": "2024", "description": "Model Spec rules → behavioural expectations for model behaviour.", "estate": "clawd/csoai-org-v2 (frameworks/openai-model-spec)"},
    {"id": "singapore-agentic-ai", "name": "Singapore Agentic AI", "kind": "framework", "issuer": "MAS / IMDA", "region": "SG", "binding": False, "status": "active", "effective": "2024", "description": "Agentic AI guidance for financial + general sectors.", "estate": "clawd/csoai-org-v2 (frameworks/singapore-agentic-ai)"},
    {"id": "nist-csf", "name": "NIST CSF 2.0", "kind": "framework", "issuer": "NIST", "region": "US", "binding": False, "status": "active", "effective": "Feb 2024", "description": "Cybersecurity outcomes — 6 functions incl. GOVERN; 106 subcategories.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "mitre-atlas", "name": "MITRE ATLAS", "kind": "framework", "issuer": "MITRE", "region": "US", "binding": False, "status": "active", "effective": "2020", "description": "Adversarial Threat Landscape for AI systems — attack tactics/techniques.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "owasp-llm-top10", "name": "OWASP Top 10 for LLM Apps", "kind": "framework", "issuer": "OWASP", "region": "Global", "binding": False, "status": "active", "effective": "2023 (2025 update)", "description": "Prompt injection, data leakage, etc. — the de-facto LLM security checklist.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "ai-verify", "name": "AI Verify (Singapore)", "kind": "framework", "issuer": "IMDA", "region": "SG", "binding": False, "status": "active", "effective": "2022", "description": "AI governance testing framework + toolkit — transparency, explainability.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "iso-23894", "name": "ISO/IEC 23894", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2023", "description": "AI risk management guidance.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "iso-38507", "name": "ISO/IEC 38507", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2022", "description": "Governance implications of AI use by organisations.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "nist-sp800-53", "name": "NIST SP 800-53 Rev 5", "kind": "framework", "issuer": "NIST", "region": "US", "binding": False, "status": "active", "effective": "2020", "description": "Security and privacy controls catalogue.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "nist-sp800-171", "name": "NIST SP 800-171 Rev 3", "kind": "framework", "issuer": "NIST", "region": "US", "binding": False, "status": "active", "effective": "2024", "description": "Protecting CUI in non-federal systems.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "fedramp", "name": "FedRAMP", "kind": "framework", "issuer": "GSA", "region": "US", "binding": False, "status": "active", "effective": "2011", "description": "Cloud authorization standard for US federal.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "pci-dss", "name": "PCI DSS v4.0", "kind": "framework", "issuer": "PCI SSC", "region": "Global", "binding": False, "status": "active", "effective": "2022", "description": "Payment card data security standard.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "cmmc", "name": "CMMC 2.0", "kind": "framework", "issuer": "DoD", "region": "US", "binding": False, "status": "active", "effective": "2023", "description": "Cybersecurity Maturity Model Certification for defence supply chain.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "soc2", "name": "SOC 2 Type II", "kind": "framework", "issuer": "AICPA", "region": "US", "binding": False, "status": "active", "effective": "—", "description": "Trust Service Criteria — security/availability/processing integrity/confidentiality/privacy.", "estate": "clawd/marketing/12-framework-crosswalk.md"},
    {"id": "bsi-pas-1880", "name": "BSI PAS 1880", "kind": "framework", "issuer": "BSI", "region": "UK", "binding": False, "status": "active", "effective": "2020", "description": "Guidelines for developing and assessing control systems for CAVs.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "ieee-7000", "name": "IEEE 7000-2021", "kind": "framework", "issuer": "IEEE", "region": "IEEE", "binding": False, "status": "active", "effective": "2021", "description": "Model process for addressing ethical concerns during system design.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "uk-ico-ai-auditing", "name": "UK ICO AI Auditing Framework", "kind": "framework", "issuer": "ICO", "region": "UK", "binding": False, "status": "active", "effective": "2024", "description": "AI auditing framework for accountability under UK GDPR.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "oml-m24-10", "name": "OMB M-24-10 (US AI Risk Management)", "kind": "framework", "issuer": "OMB", "region": "US", "binding": False, "status": "active", "effective": "2024", "description": "Agency AI risk management minimum practices (federal).", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "ai-bill-of-rights", "name": "White House Blueprint for an AI Bill of Rights", "kind": "framework", "issuer": "White House OSTP", "region": "US", "binding": False, "status": "active", "effective": "Oct 2022", "description": "5 principles — safe systems, algorithmic discrimination, data privacy, notice, human alternatives.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "tc260-ai-safety-governance", "name": "China TC260 AI Safety Governance Framework", "kind": "framework", "issuer": "TC260", "region": "CN", "binding": False, "status": "active", "effective": "2021", "description": "AI Safety Governance Framework 2.0 (Feb 2024) — the Chinese AI governance skeleton.", "estate": "clawd/csoai-platform/docs/other/www.onetrust.com_blog_chinas-tc260-releases-ai-safety-governance-framework_.md"},
    {"id": "maritime-law-parallel", "name": "Maritime Law → AI Law Parallel", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI Original", "binding": False, "status": "active", "effective": "2026", "description": "Centuries of shipping regulation as precedent for AI governance — original CSOAI research.", "estate": "clawd/csoai-org-v2 (frameworks/maritime-law-parallel)"},
    {"id": "essential-ai-law", "name": "Creating Essential AI Law", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI Original", "binding": False, "status": "active", "effective": "2026", "description": "What AI law must include to be effective — analysis of legislative essentials.", "estate": "clawd/csoai-org-v2 (frameworks/essential-ai-law)"},

    # --- REGULATIONS (binding / near-binding legal instruments) -------------
    {"id": "eu-ai-act", "name": "EU AI Act", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force (phased)", "effective": "Prohibitions 2 Feb 2025 · GPAI 2 Aug 2025 · Annex III high-risk 2 Dec 2027 · Annex I 2 Aug 2028", "description": "Regulation (EU) 2024/1689 — risk-tiered; Arts 5/6/9/10/13/14/15/50; GPAI code of practice; Digital Omnibus delayed high-risk to 2 Dec 2027.", "estate": "clawd/csoai-org-v2 (frameworks/eu-ai-act)"},
    {"id": "gdpr", "name": "GDPR / UK GDPR", "kind": "regulation", "issuer": "EU/UK", "region": "EU/UK", "binding": True, "status": "in force", "effective": "25 May 2018", "description": "Art 22 automated decision-making safeguards; Art 35 DPIA; Art 5-21 core.", "estate": "clawd/csoai-org-v2 (frameworks/gdpr)"},
    {"id": "dora", "name": "DORA", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "17 Jan 2025", "description": "Regulation (EU) 2022/2554 — financial ICT resilience; Art 19 4-hour major-incident clock.", "estate": "clawd/csoai-org-v2 (frameworks/dora)"},
    {"id": "nis2", "name": "NIS2", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "18 Oct 2024", "description": "Directive (EU) 2022/2555 — Art 23: 24h early warning / 72h incident / 1mo final.", "estate": "clawd/csoai-org-v2 (frameworks/nis2)"},
    {"id": "cra", "name": "Cyber Resilience Act (CRA)", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force (phased)", "effective": "Active-exploitation reporting 11 Sep 2026 · full 11 Dec 2027", "description": "Regulation (EU) 2024/2847 — products with digital elements incl. AI software; Art 14.", "estate": "clawd/csoai-org-v2 (frameworks/cra)"},
    {"id": "hipaa", "name": "HIPAA", "kind": "regulation", "issuer": "US", "region": "US", "binding": True, "status": "in force", "effective": "1996", "description": "US healthcare data protection + AI-specific applications; Privacy + Security Rules.", "estate": "clawd/csoai-org-v2 (frameworks/hipaa)"},
    {"id": "korea-ai-basic-act", "name": "Korea AI Basic Act", "kind": "regulation", "issuer": "Republic of Korea", "region": "KR", "binding": True, "status": "in force", "effective": "22 Jan 2026", "description": "High-impact AI requirements + GenAI labelling; Act No. 20193.", "estate": "clawd/csoai-org-v2 (frameworks/korea-ai-basic-act)"},
    {"id": "china-genai-measures", "name": "China GenAI & Algorithm Rules", "kind": "regulation", "issuer": "CAC", "region": "CN", "binding": True, "status": "in force", "effective": "GenAI 15 Aug 2023 · Deep Synthesis 10 Jan 2023 · Algorithm Recs 1 Mar 2022", "description": "Security review, labelling, training-data legality for generative AI services.", "estate": "clawd/csoai-dashboard-master (frameworks/china-genai-measures)"},
    {"id": "colorado-ai-act", "name": "Colorado AI Act (SB24-205)", "kind": "regulation", "issuer": "Colorado", "region": "US-State", "binding": True, "status": "enacted (amended)", "effective": "1 Jan 2027", "description": "First US state comprehensive AI law; overhauled by SB 26-189 (May 2026) into disclosure/transparency regime.", "estate": "clawd/csoai-dashboard-master (frameworks/colorado-ai-act)"},
    {"id": "japan-ai-promotion-act", "name": "Japan AI Promotion Act", "kind": "regulation", "issuer": "Japan", "region": "JP", "binding": False, "status": "in force (non-punitive)", "effective": "4 Jun 2025", "description": "Innovation-first AI statute — principles + coordination duties, no fines.", "estate": "clawd/csoai-dashboard-master (frameworks/japan-ai-promotion-act)"},
    {"id": "canada-aida", "name": "Canada AIDA", "kind": "regulation", "issuer": "Canada", "region": "CA", "binding": False, "status": "lapsed", "effective": "—", "description": "Artificial Intelligence and Data Act (Bill C-27) died on order paper Jan 2025 — not reintroduced.", "estate": "clawd/csoai-dashboard-master (frameworks/canada-aida)"},
    {"id": "australia-voluntary-ai-standard", "name": "Australia Voluntary AI Safety Standard", "kind": "regulation", "issuer": "DISR", "region": "AU", "binding": False, "status": "voluntary", "effective": "Sept 2024", "description": "10 guardrails; mandatory guardrails for high-risk remain a proposal.", "estate": "clawd/csoai-dashboard-master (frameworks/australia-voluntary-ai-standard)"},
    {"id": "india-it-synthetic-rules", "name": "India IT Rules — Synthetic Content", "kind": "regulation", "issuer": "MeitY", "region": "IN", "binding": True, "status": "in force", "effective": "20 Feb 2026", "description": "IT Amendment Rules 2026 — AI/deepfake labelling, provenance metadata, takedown duties.", "estate": "clawd/csoai-dashboard-master (frameworks/india-it-synthetic-rules)"},
    {"id": "vietnam-ai-law", "name": "Vietnam Law on AI", "kind": "regulation", "issuer": "Vietnam", "region": "VN", "binding": True, "status": "in force (grace)", "effective": "1 Mar 2026 (grace to 1 Mar 2027)", "description": "Law No. 134/2025/QH15 — risk-based conformity assessment, national AI DB registration, penalties to VND 2bn.", "estate": "clawd/csoai-dashboard-master (frameworks/vietnam-ai-law)"},
    {"id": "taiwan-ai-basic-act", "name": "Taiwan AI Basic Act", "kind": "regulation", "issuer": "Taiwan", "region": "TW", "binding": True, "status": "in force", "effective": "14 Jan 2026", "description": "7 principles + risk-classification mandate; operational duties deferred to NSTC regulation.", "estate": "clawd/csoai-dashboard-master (frameworks/taiwan-ai-basic-act)"},
    {"id": "peru-ai-law", "name": "Peru AI Law + Regulation", "kind": "regulation", "issuer": "Peru", "region": "PE", "binding": True, "status": "in force (phased)", "effective": "Reg. effective 22 Jan 2026", "description": "Law 31814 + Supreme Decree 115-2025-PCM — first LatAm AI statute with in-force regulation.", "estate": "clawd/csoai-dashboard-master (frameworks/peru-ai-law)"},
    {"id": "quebec-law-25", "name": "Quebec Law 25 — Automated Decisions", "kind": "regulation", "issuer": "Quebec", "region": "CA-QC", "binding": True, "status": "in force", "effective": "22 Sep 2023 (ADM provisions)", "description": "Disclosure + right to human review for exclusively-automated decisions.", "estate": "clawd/csoai-dashboard-master (frameworks/quebec-law-25-adm)"},
    {"id": "california-sb1001", "name": "California Bot Disclosure (SB 1001)", "kind": "regulation", "issuer": "California", "region": "US-State", "binding": True, "status": "in force", "effective": "1 Jul 2019", "description": "B.O.T. Act — undisclosed bots cannot incentivize sales/votes online.", "estate": "clawd/csoai-dashboard-master (frameworks/california-sb1001-bots)"},
    {"id": "california-ab2013", "name": "California GenAI Training-Data Transparency (AB 2013)", "kind": "regulation", "issuer": "California", "region": "US-State", "binding": True, "status": "in force", "effective": "1 Jan 2026", "description": "Generative-AI developers must document training datasets.", "estate": "clawd/csoai-dashboard-master (frameworks/california-ab2013-training-data)"},
    {"id": "california-sb942", "name": "California AI Transparency Act (SB 942)", "kind": "regulation", "issuer": "California", "region": "US-State", "binding": True, "status": "in force", "effective": "2 Aug 2026 (delayed by AB 853)", "description": "AI-detection tooling + provenance disclosures for AI-generated content.", "estate": "clawd/csoai-dashboard-master (frameworks/california-sb942-transparency)"},
    {"id": "illinois-bipa", "name": "Illinois Biometric Privacy (BIPA)", "kind": "regulation", "issuer": "Illinois", "region": "US-State", "binding": True, "status": "in force", "effective": "3 Oct 2008", "description": "Consent + notice for biometric identifiers; private right of action.", "estate": "clawd/csoai-dashboard-master (frameworks/illinois-bipa)"},
    {"id": "illinois-hb3773", "name": "Illinois AI in Employment (HB 3773)", "kind": "regulation", "issuer": "Illinois", "region": "US-State", "binding": True, "status": "in force", "effective": "1 Jan 2026", "description": "AI discrimination in employment is a civil-rights violation; notice required.", "estate": "clawd/csoai-dashboard-master (frameworks/illinois-hb3773-employment)"},
    {"id": "nyc-local-law-144", "name": "NYC Automated Employment Tools (Local Law 144)", "kind": "regulation", "issuer": "NYC", "region": "US-State", "binding": True, "status": "in force", "effective": "Enforced 5 Jul 2023", "description": "Annual independent bias audit + candidate notice for AEDTs.", "estate": "clawd/csoai-dashboard-master (frameworks/nyc-local-law-144)"},
    {"id": "texas-traiga", "name": "Texas Responsible AI Governance Act (TRAIGA)", "kind": "regulation", "issuer": "Texas", "region": "US-State", "binding": True, "status": "in force", "effective": "1 Jan 2026", "description": "HB 149 — prohibits AI intentional discrimination + manipulative/biometric uses.", "estate": "clawd/csoai-dashboard-master (frameworks/texas-traiga)"},
    {"id": "utah-ai-policy-act", "name": "Utah AI Policy Act (SB 149)", "kind": "regulation", "issuer": "Utah", "region": "US-State", "binding": True, "status": "in force", "effective": "1 May 2024 (sunset ext. to 1 Jul 2027)", "description": "GenAI disclosure requirements + liability clarity.", "estate": "clawd/csoai-dashboard-master (frameworks/utah-ai-policy-act)"},
    {"id": "brazil-pl2338", "name": "Brazil AI Bill (PL 2338/2023)", "kind": "regulation", "issuer": "Brazil", "region": "BR", "binding": False, "status": "pending", "effective": "—", "description": "Marco Legal da IA — risk-based bill; Senate-passed Dec 2024, pending Chamber.", "estate": "clawd/csoai-dashboard-master (frameworks/brazil-pl2338)"},
    {"id": "chile-ai-bill", "name": "Chile AI Bill", "kind": "regulation", "issuer": "Chile", "region": "CL", "binding": False, "status": "pending", "effective": "—", "description": "Boletín 16821-19 — passed Chamber Oct 2025, Senate review.", "estate": "clawd/csoai-dashboard-master (frameworks/chile-ai-bill)"},
    {"id": "uk-ai-approach", "name": "UK Pro-Innovation AI Approach", "kind": "regulation", "issuer": "UK", "region": "UK", "binding": False, "status": "active (non-statutory)", "effective": "White Paper Mar 2023", "description": "Sector-regulator, principles-based model; AI (Regulation) Bill has no government backing.", "estate": "clawd/csoai-dashboard-master (frameworks/uk-ai-approach)"},
    {"id": "switzerland-ai-approach", "name": "Switzerland AI Approach", "kind": "regulation", "issuer": "Switzerland", "region": "CH", "binding": False, "status": "active (sectoral)", "effective": "12 Feb 2025 decision", "description": "Ratifying CoE AI Convention + sectoral approach; legislation expected end-2026.", "estate": "clawd/csoai-dashboard-master (frameworks/switzerland-ai-approach)"},
    {"id": "norway-ai-eea", "name": "Norway AI (EEA)", "kind": "regulation", "issuer": "Norway", "region": "NO", "binding": False, "status": "pending", "effective": "—", "description": "EU AI Act marked EEA-relevant, not yet incorporated; national 'KI-loven' draft in consultation.", "estate": "clawd/csoai-dashboard-master (frameworks/norway-ai-eea)"},
    {"id": "uae-ai-charter", "name": "UAE AI Charter & Strategy", "kind": "regulation", "issuer": "UAE", "region": "AE", "binding": False, "status": "voluntary", "effective": "Charter 2024", "description": "12-principle voluntary charter + National AI Strategy 2031; DIFC Law 10 the only binding AI-adjacent rule.", "estate": "clawd/csoai-dashboard-master (frameworks/uae-ai-charter)"},
    {"id": "saudi-sdaia-ai-ethics", "name": "Saudi SDAIA AI Ethics", "kind": "regulation", "issuer": "SDAIA", "region": "SA", "binding": False, "status": "voluntary", "effective": "Sept 2023", "description": "Principles & Controls of AI Ethics + GenAI Guidelines (voluntary); PDPL applies generally.", "estate": "clawd/csoai-dashboard-master (frameworks/saudi-sdaia-ai-ethics)"},
    {"id": "israel-ai-policy", "name": "Israel AI Policy & Ethics", "kind": "regulation", "issuer": "Israel", "region": "IL", "binding": False, "status": "voluntary", "effective": "18 Dec 2023", "description": "Soft, sector-specific ethical principles; no binding horizontal law.", "estate": "clawd/csoai-dashboard-master (frameworks/israel-ai-policy)"},
    {"id": "egypt-ai-charter", "name": "Egypt Responsible-AI Charter", "kind": "regulation", "issuer": "Egypt", "region": "EG", "binding": False, "status": "voluntary", "effective": "Charter 2023", "description": "Voluntary charter + National AI Strategy 2025-2030.", "estate": "clawd/csoai-dashboard-master (frameworks/egypt-ai-charter)"},
    {"id": "turkey-draft-ai-law", "name": "Turkey Draft AI Law", "kind": "regulation", "issuer": "Turkey", "region": "TR", "binding": False, "status": "draft", "effective": "—", "description": "Draft Law on AI (EU-inspired, 8 articles) tabled 24 Jun 2024 — not enacted.", "estate": "clawd/csoai-dashboard-master (frameworks/turkey-ai-bill)"},
    {"id": "nigeria-ai-strategy", "name": "Nigeria National AI Strategy", "kind": "regulation", "issuer": "NITDA", "region": "NG", "binding": False, "status": "voluntary", "effective": "Aug 2024", "description": "Non-binding strategy; NDPA 2023 §37 automated decisions binds generally.", "estate": "clawd/csoai-dashboard-master (frameworks/nigeria-ai-strategy)"},
    {"id": "kenya-ai-strategy", "name": "Kenya National AI Strategy", "kind": "regulation", "issuer": "Kenya", "region": "KE", "binding": False, "status": "voluntary", "effective": "27 Mar 2025", "description": "Non-binding roadmap 2025-2030; draft AI Bill 2026 not enacted.", "estate": "clawd/csoai-dashboard-master (frameworks/kenya-ai-strategy)"},
    {"id": "south-africa-ai-policy", "name": "South Africa AI Policy Framework", "kind": "regulation", "issuer": "DCDT", "region": "ZA", "binding": False, "status": "draft", "effective": "Draft 2024", "description": "Non-binding roadmap; POPIA applies generally; Apr 2026 draft withdrawn.", "estate": "clawd/csoai-dashboard-master (frameworks/south-africa-ai-policy)"},
    {"id": "rwanda-ai-policy", "name": "Rwanda National AI Policy", "kind": "regulation", "issuer": "Rwanda", "region": "RW", "binding": False, "status": "voluntary", "effective": "20 Apr 2023", "description": "Africa's first comprehensive national AI policy; Law 058/2021 binds generally.", "estate": "clawd/csoai-dashboard-master (frameworks/rwanda-ai-policy)"},
    {"id": "indonesia-ai-ethics", "name": "Indonesia AI Ethics Circular", "kind": "regulation", "issuer": "Kominfo", "region": "ID", "binding": False, "status": "voluntary", "effective": "19 Dec 2023", "description": "Circular Letter No. 9/2023; PDP Law 27/2022 applies generally.", "estate": "clawd/csoai-dashboard-master (frameworks/indonesia-ai-ethics)"},
    {"id": "philippines-ai-bills", "name": "Philippines AI Bills", "kind": "regulation", "issuer": "Philippines", "region": "PH", "binding": False, "status": "pending", "effective": "—", "description": "Multiple competing bills; none enacted.", "estate": "clawd/csoai-dashboard-master (frameworks/philippines-ai-bills)"},
    {"id": "nz-algorithm-charter", "name": "New Zealand Algorithm Charter", "kind": "regulation", "issuer": "NZ Government", "region": "NZ", "binding": False, "status": "voluntary", "effective": "2020", "description": "6 voluntary commitments for government agencies.", "estate": "clawd/csoai-dashboard-master (frameworks/new-zealand-algorithm-charter)"},
    {"id": "pakistan-ai-policy", "name": "Pakistan National AI Policy", "kind": "regulation", "issuer": "Pakistan", "region": "PK", "binding": False, "status": "voluntary", "effective": "30 Jul 2025", "description": "Strategy document — AI Council, action plan, 2030 targets.", "estate": "clawd/csoai-dashboard-master (frameworks/pakistan-ai-policy)"},
    {"id": "malaysia-ai-guidelines", "name": "Malaysia AI Governance & Ethics", "kind": "regulation", "issuer": "MOSTI", "region": "MY", "binding": False, "status": "voluntary", "effective": "20 Sep 2024", "description": "AIGE — 7 voluntary principles; AI Governance Bill being drafted.", "estate": "clawd/csoai-dashboard-master (frameworks/malaysia-ai-guidelines)"},
    {"id": "thailand-draft-ai", "name": "Thailand Draft AI Law", "kind": "regulation", "issuer": "Thailand", "region": "TH", "binding": False, "status": "draft", "effective": "—", "description": "Unified AI legislation in consultation Feb 2026 — verify Royal Gazette before in-force claims.", "estate": "clawd/csoai-dashboard-master (frameworks/thailand-ai-draft)"},
    {"id": "us-eo-14110", "name": "US Executive Order 14110 (AI Safety)", "kind": "regulation", "issuer": "White House", "region": "US", "binding": True, "status": "revoked", "effective": "Oct 2023 → revoked 2025", "description": "Historical — revoked; replaced by EO 14179 AI Action Plan (Jan 2025).", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "us-eo-14179", "name": "US Executive Order 14179 (AI Action Plan)", "kind": "regulation", "issuer": "White House", "region": "US", "binding": True, "status": "in force", "effective": "Jan 2025", "description": "US federal AI action plan — deregulatory direction.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "eu-ai-liability-directive", "name": "EU AI Liability Directive", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": False, "status": "proposed", "effective": "—", "description": "2022/0303(COD) — proposed; fault-based + evidence disclosure for AI harm.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "eu-pl-directive", "name": "EU Product Liability Directive (revised)", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "2024/2853", "description": "Liability for defective products incl. software/AI.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "eu-dsa", "name": "EU Digital Services Act", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "2022/2065", "description": "Platform accountability, systemic risk, transparency.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "eu-dma", "name": "EU Digital Markets Act", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "2022/1925", "description": "Gatekeeper platform obligations.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "eu-data-act", "name": "EU Data Act", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "2023 (applies Sep 2025)", "description": "Data sharing + interoperability rules.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "eu-csrd", "name": "EU CSRD / ESRS", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "2022/2464 (phased)", "description": "Corporate sustainability reporting — incl. AI-related risk disclosure.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "uk-dpa-2018", "name": "UK Data Protection Act 2018", "kind": "regulation", "issuer": "UK", "region": "UK", "binding": True, "status": "in force", "effective": "2018", "description": "UK GDPR implementation; Part 3 law-enforcement processing.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "uk-online-safety-act", "name": "UK Online Safety Act 2023", "kind": "regulation", "issuer": "UK", "region": "UK", "binding": True, "status": "in force", "effective": "2023 (phased)", "description": "Platform duties for illegal/harmful content incl. AI-generated.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "china-pipl", "name": "China PIPL", "kind": "regulation", "issuer": "China", "region": "CN", "binding": True, "status": "in force", "effective": "1 Nov 2021", "description": "Personal Information Protection Law — cross-border + automated decision rules.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "eu-ai-pact", "name": "EU AI Pact (voluntary pledges)", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": False, "status": "voluntary", "effective": "2023", "description": "Industry voluntary early compliance with AI Act principles.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},

    # --- CHARTERS (estate + world declarations) ------------------------------
    {"id": "csoai-charter-52", "name": "CSOAI 52-Article Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "The estate's founding charter — 52 articles, open CC BY 4.0; every framework cross-walks to it.", "estate": "clawd/csoai_charter_52_articles.json"},
    {"id": "charter-of-charters", "name": "Charter of Charters (Universal Cross-Walk)", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified (BFT #1)", "effective": "2026-06-30", "description": "Root charter — 41 charters, 7 layers, 123+ frameworks, 5,043 cross-walks; Article 0 fee-for-service.", "estate": "clawd/sovereign-charters/CHARTER-OF-CHARTERS.md"},
    {"id": "asilomar-ai-principles", "name": "Asilomar AI Principles", "kind": "charter", "issuer": "FLI", "region": "Global", "binding": False, "status": "declaration", "effective": "2017", "description": "23 principles; 3,800+ AI/robotics researchers.", "estate": "clawd/csoai-org-v2 (frameworks/asilomar-ai-principles)"},
    {"id": "montreal-declaration", "name": "Montreal Declaration", "kind": "charter", "issuer": "Université de Montréal", "region": "Global", "binding": False, "status": "declaration", "effective": "2018", "description": "10 responsible-AI principles.", "estate": "clawd/csoai-org-v2 (frameworks/montreal-declaration)"},
    {"id": "toronto-declaration", "name": "Toronto Declaration", "kind": "charter", "issuer": "Amnesty International", "region": "Global", "binding": False, "status": "declaration", "effective": "2018", "description": "Equality + non-discrimination in machine learning.", "estate": "clawd/csoai-org-v2 (frameworks/toronto-declaration)"},
    {"id": "beijing-ai-principles", "name": "Beijing AI Principles", "kind": "charter", "issuer": "BAAI", "region": "CN", "binding": False, "status": "declaration", "effective": "2019", "description": "Chinese AI governance principles — beneficence, non-maleficence, autonomy, justice.", "estate": "clawd/csoai-org-v2 (frameworks/beijing-ai-principles)"},
    {"id": "bletchley-declaration", "name": "Bletchley Declaration", "kind": "charter", "issuer": "Intergovernmental (UK summit)", "region": "Intergovernmental", "binding": False, "status": "declaration", "effective": "1 Nov 2023", "description": "28 countries + EU — frontier-AI safety cooperation.", "estate": "clawd/csoai-org-v2 (frameworks/bletchley-declaration)"},
    {"id": "seoul-declaration", "name": "Seoul Declaration", "kind": "charter", "issuer": "Intergovernmental (KR/UK)", "region": "Intergovernmental", "binding": False, "status": "declaration", "effective": "21 May 2024", "description": "AI Seoul Summit — safety, innovation, inclusivity.", "estate": "clawd/csoai-org-v2 (frameworks/seoul-declaration)"},
    {"id": "asean-ai-guide", "name": "ASEAN Guide on AI Governance & Ethics", "kind": "charter", "issuer": "ASEAN", "region": "Regional Bloc", "binding": False, "status": "declaration", "effective": "2 Feb 2024 (GenAI guide 16 Jan 2025)", "description": "7-principle voluntary regional guide.", "estate": "clawd/csoai-org-v2 (frameworks/asean-ai-guide)"},
    {"id": "au-continental-ai-strategy", "name": "African Union Continental AI Strategy", "kind": "charter", "issuer": "African Union", "region": "Regional Bloc", "binding": False, "status": "declaration", "effective": "Jul 2024", "description": "Non-binding continental strategy, 5 focus areas.", "estate": "clawd/csoai-org-v2 (frameworks/au-continental-ai-strategy)"},
    {"id": "council-of-europe-ai-convention", "name": "Council of Europe AI Convention (CETS 225)", "kind": "charter", "issuer": "Council of Europe", "region": "Council of Europe", "binding": False, "status": "signed, not in force", "effective": "Opened 5 Sep 2024", "description": "First international AI treaty — needs 5 ratifications (EU ratified May 2026).", "estate": "clawd/csoai-org-v2 (frameworks/council-of-europe-ai-convention)"},
    {"id": "sovereign-root-charter", "name": "Sovereign Root Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L0 constitutional substrate — 5 sovereign principles.", "estate": "clawd/sovereign-charters/00-sovereign-root-charter.md"},
    {"id": "csoai-charter", "name": "CSOAI Charter (hive)", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 trust-layer charter — governance authority of the federation.", "estate": "clawd/sovereign-charters/01-csoai-charter.md"},
    {"id": "meok-charter", "name": "MEOK Charter", "kind": "charter", "issuer": "MEOK", "region": "MEOK", "binding": True, "status": "ratified", "effective": "2026", "description": "L2 build-layer charter.", "estate": "clawd/sovereign-charters/02-meok-charter.md"},
    {"id": "defoneos-charter", "name": "DEFONEOS Charter", "kind": "charter", "issuer": "CSOAI LTD / MEOK", "region": "DEFONEOS", "binding": True, "status": "ratified", "effective": "2026", "description": "L1 defence-layer charter — hard-stops, refuse+protect only.", "estate": "clawd/sovereign-charters/12-defoneos-charter.md"},
    {"id": "coigndaltion-charter", "name": "Coigndaltion Charter (Cornerstone)", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L4 cornerstone charter — 16-dim state compression, 41-charter cross-walk.", "estate": "clawd/sovereign-charters/35-coigndaltion-charter.md"},
    {"id": "public-watchdog-charter", "name": "Public Watchdog Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Public watchdog — complaint intake, BFT council verdicts.", "estate": "clawd/sovereign-charters/36-publicwatchdog-charter.md"},
    {"id": "openmcp-charter", "name": "OpenMCP Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 technical charter — the MCP protocol hive.", "estate": "clawd/sovereign-charters/15-openmcp-charter.md"},
    {"id": "openmoe-charter", "name": "OpenMoE Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 technical charter — open mixture-of-experts hive.", "estate": "clawd/sovereign-charters/14-openmoe-charter.md"},
    {"id": "openpatent-charter", "name": "OpenPatent Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 technical charter — defensive patent / prior-art anchoring.", "estate": "clawd/sovereign-charters/16-openpatent-charter.md"},
    {"id": "safetyof-charter", "name": "SafetyOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — safety hive.", "estate": "clawd/sovereign-charters/04-safetyof-charter.md"},
    {"id": "transparencyof-charter", "name": "TransparencyOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — transparency hive.", "estate": "clawd/sovereign-charters/07-transparencyof-charter.md"},
    {"id": "accountabilityof-charter", "name": "AccountabilityOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — accountability hive.", "estate": "clawd/sovereign-charters/05-accountabilityof-charter.md"},
    {"id": "ethicalgovernanceof-charter", "name": "EthicalGovernanceOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — ethics hive.", "estate": "clawd/sovereign-charters/06-ethicalgovernanceof-charter.md"},
    {"id": "biasdetectionof-charter", "name": "BiasDetectionOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — bias hive.", "estate": "clawd/sovereign-charters/08-biasdetectionof-charter.md"},
    {"id": "dataprivacyof-charter", "name": "DataPrivacyOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — privacy hive.", "estate": "clawd/sovereign-charters/09-dataprivacyof-charter.md"},
    {"id": "asisecurity-charter", "name": "ASISecurity Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — AI security hive.", "estate": "clawd/sovereign-charters/10-asisecurity-charter.md"},
    {"id": "agisafe-charter", "name": "AGISafe Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — frontier-safety hive.", "estate": "clawd/sovereign-charters/11-agisafe-charter.md"},
    {"id": "proofof-charter", "name": "ProofOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 AI-governance charter — verification hive.", "estate": "clawd/sovereign-charters/03-proofof-charter.md"},
    {"id": "councilof-charter", "name": "CouncilOf Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "L3 technical charter — BFT council hive.", "estate": "clawd/sovereign-charters/13-councilof-charter.md"},
    {"id": "sovereign-ubi-charter", "name": "Sovereign UBI Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "UBI starter pathways bound into every charter.", "estate": "clawd/sovereign-charters/00-SOVEREIGN-UBI-CHARTER.md"},
    {"id": "magna-carta-charter", "name": "Magna Carta Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — due process lineage (1215 → AI).", "estate": "clawd/csoai.org/charter2/magna-carta-charter.html"},
    {"id": "habeas-corpus-charter", "name": "Habeas Corpus Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — liberty lineage (1679 → AI).", "estate": "clawd/csoai.org/charter2/habeas-corpus-charter.html"},
    {"id": "data-sovereignty-charter", "name": "Data Sovereignty Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — data sovereignty rights.", "estate": "clawd/csoai.org/charter2/data-sovereignty-charter.html"},
    {"id": "open-source-definition-charter", "name": "Open Source Definition Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — open-source lineage charter.", "estate": "clawd/csoai.org/charter2/open-source-definition-charter.html"},
    {"id": "ai-bletchley-declaration-charter", "name": "AI Bletchley Declaration Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — Bletchley lineage charter.", "estate": "clawd/csoai.org/charter2/ai-bletchley-declaration-charter.html"},
    {"id": "ai-seoul-summit-declaration-charter", "name": "AI Seoul Summit Declaration Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — Seoul lineage charter.", "estate": "clawd/csoai.org/charter2/ai-seoul-summit-declaration-charter.html"},
    {"id": "paris-ai-summit-declaration-charter", "name": "Paris AI Summit Declaration Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — Paris lineage charter.", "estate": "clawd/csoai.org/charter2/paris-ai-summit-declaration-charter.html"},
    {"id": "un-global-digital-compact-charter", "name": "UN Global Digital Compact Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — UN GDC lineage charter.", "estate": "clawd/csoai.org/charter2/un-global-digital-compact-charter.html"},
    {"id": "geneva-conventions-charter", "name": "Geneva Conventions 1949 Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — humanitarian-law lineage charter.", "estate": "clawd/csoai.org/charter2/geneva-conventions-1949-charter.html"},
    {"id": "helsinki-accords-charter", "name": "Helsinki Accords Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — human-rights lineage charter.", "estate": "clawd/csoai.org/charter2/helsinki-accords-charter.html"},
    {"id": "creative-commons-charter", "name": "Creative Commons Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — licensing lineage charter.", "estate": "clawd/csoai.org/charter2/creative-commons-charter.html"},
    {"id": "mit-license-charter", "name": "MIT License Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — MIT licence lineage charter.", "estate": "clawd/csoai.org/charter2/mit-license-charter.html"},
    {"id": "asean-ai-charter", "name": "ASEAN AI Charter", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "Charter2 — ASEAN lineage charter.", "estate": "clawd/csoai.org/charter2/asean-ai-charter.html"},
    {"id": "master-charter-template", "name": "Master Charter Template", "kind": "charter", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "ratified", "effective": "2026", "description": "The template every numbered charter derives from.", "estate": "clawd/sovereign-charters/00-MASTER-CHARTER-TEMPLATE.md"},

    # --- ARTICLES / RESEARCH (estate) ----------------------------------------
    {"id": "sovereign-framework-forge", "name": "The Sovereign Framework Forge", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-07-10", "description": "PDCA + Deming + Lean Six Sigma + OKR + TOC + ISO 42001 + NIST AI RMF absorbed into one 24/7 improvement loop; meta-PDCA.", "estate": "clawd/_alignment/SOVEREIGN_FRAMEWORK_FORGE_ASI_24_7_2026-07-10.md"},
    {"id": "sovereign-mindset-framework", "name": "The Sovereign Mindset Framework — Years→Days", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-07-09", "description": "Improve-existing + time-compression doctrine: YEARS→MONTHS→DAYS→HOURS→MINUTES compounding.", "estate": "clawd/_alignment/SOVEREIGN_MINDSET_FRAMEWORK_YEARS_TO_DAYS_2026-07-09.md"},
    {"id": "nine-stage-governed-flow", "name": "The Nine-Stage Governed Flow", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "active", "effective": "2026", "description": "LEARN → CHECK-EXISTING → PLAN → DO → ACT → CHECK-VERIFY → AUDIT → IMPROVE → BRAND/QUALITY; the whiteboard cycle, canonical.", "estate": "clawd/_alignment/CHARTER_SOV33_NINE_STAGE_FLOW.md"},
    {"id": "perennial-governance-corpus", "name": "Perennial Governance Corpus", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-07-08", "description": "The estate's standing governance corpus — charters, frameworks, cross-walks in one place.", "estate": "clawd/sovereign-charters/PERENNIAL_GOVERNANCE_CORPUS_2026-07-08.md"},
    {"id": "regulations-pipeline", "name": "Regulations Pipeline", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-07-06 (+2 expansions)", "description": "The regulations intake pipeline — what to track, in what order, per jurisdiction.", "estate": "clawd/sovereign-charters/REGULATIONS_PIPELINE_2026-07-06.md"},
    {"id": "universal-compliance-frameworks", "name": "Universal Compliance Frameworks (236)", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-07-02", "description": "The canonical 236-framework cross-walk list across 8 regions / 5 tiers.", "estate": "clawd/sovereign-charters/UNIVERSAL_COMPLIANCE_FRAMEWORKS_2026-07-02.md"},
    {"id": "meok-12-framework-crosswalk", "name": "MEOK 12-Framework Crosswalk", "kind": "article", "issuer": "MEOK", "region": "MEOK", "binding": False, "status": "active", "effective": "2026", "description": "Master compliance matrix — EU AI Act, UK AI Bill, DORA, NIS2, ISO 42001, GDPR, HIPAA, SOC2, NIST, AISI, CAISI, Montreal/Toronto.", "estate": "clawd/marketing/12-framework-crosswalk.md"},
    {"id": "regulators-matrix", "name": "AI-Governance + Cybersecurity Regulatory Matrix", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-07-02", "description": "Verified regulatory intelligence incl. the Digital Omnibus 2026 correction (high-risk moved to 2 Dec 2027).", "estate": "clawd/_compintel/regulators-matrix.md"},
    {"id": "owem-sandwich-merge", "name": "OWEM Sandwich — 4-way TIES merge", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-08-10", "description": "MergeKit TIES merge of 4 axis specialists into one router — with the honest n≥30 / UNMEASURED floor.", "estate": "clawd/kimi-regen/sov7_synthesis/_sov7/owem_sandwich_README.md"},
    {"id": "mine-everything-master-plan", "name": "Mine Everything — Master Plan", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-08-18", "description": "15 seams, 8,999 docs — the estate-wide mining plan this drum is part of.", "estate": "clawd/kimi-regen/SOVOS/MASTER_PLAN_2026-08-18.md"},
    {"id": "geometry-core", "name": "The Geometry Core", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "active", "effective": "2026-08-17", "description": "Merging / governance / memory federation / quantum bridge = the same math (Procrustes, Fisher-Rao). One core, four doors.", "estate": "master-harness/README.md"},
    {"id": "deepseek-training-research", "name": "DeepSeek Training Research", "kind": "article", "issuer": "Research", "region": "Global", "binding": False, "status": "active", "effective": "2026", "description": "Estate research on deepseek training techniques.", "estate": "~/deepseek_training_research.md"},
    {"id": "master-framework-v1.1", "name": "Master Framework v1.1 — the substrate that evolves and keeps-if-better", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "canonical", "effective": "2026-08-20", "description": "The estate operating doctrine (OAI master framework): human+AI complementarity [BET], 9-step PDCA+audit-and-promote loop, 90/10 self-propagating scoring function (crown-jewel gap), mergekit at the knowledge/code layer, monorepo ~40% built (councilof-ai-monorepo 55/55), evidence ledger, real blockers (did:web split-brain). [BET]/[BUILT]/[GAP] tagged.", "estate": "master-harness/knowledge/frameworks-drum/docs/MASTER_FRAMEWORK.md"},
    {"id": "master-framework-v1.2", "name": "Master Framework v1.2 — validation-corrected doctrine", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "canonical", "effective": "2026-08-20", "description": "v1.1 + literature validation: 9-step loop collapsed to 5 MAPE-K stages; complementarity reframed as task-allocation (Vaccaro meta-analysis: combinations worse in decisions, better in content creation); 90/10 router speced as frozen split-conformal predicate; mergekit reduced to the evolutionary loop (weight arithmetic does not transfer); promote-gate made contamination-resistant with statistical significance. See RESEARCH_VALIDATION.md.", "estate": "master-harness/knowledge/frameworks-drum/docs/MASTER_FRAMEWORK.md"},
    {"id": "master-framework-v1.3", "name": "Master Framework v1.3 — adversarial-evidence discipline", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "canonical", "effective": "2026-08-20", "description": "v1.2 + binding adversarial-evidence rule: every [BET] carries its strongest disconfirming evidence inline. §1 carries the full Vaccaro/Almaatouq/Malone disconfirming evidence for the complementarity bet (Hedges' g = −0.23, 95% CI −0.39 to −0.07, 106 studies; content g = 0.64; asymmetry: combine helps when human > AI alone, hurts when AI > human) and the sharpening — allocation, not blending; the 90/10 router is the corrected thesis in code. §3 and §0 carry their disconfirming evidence likewise.", "estate": "master-harness/knowledge/frameworks-drum/docs/MASTER_FRAMEWORK.md"},
    {"id": "master-framework-v1.4", "name": "Master Framework v1.4 — Claude alignment (Dorado doctrine + trust-root)", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": True, "status": "canonical", "effective": "2026-08-20", "description": "v1.3 + market-leg/[Dorado] doctrine with three binding boundaries: (1) composed never fused — market leg is a REPORTED context leg, never blended into one number; (2) licensed data source before assertion — stays NOT_PRESENT until then; (3) never a trading signal or investment product — the divergence layer measures and reports, never advises. Trust-root live state corrected: mirror now carries extra card-attestation-1 (apex 3 keys, mirror 4); one-PR reconcile = add card-attestation-1 + DSH key o32UOkcsCnpSd5u-GALIWDTrpVY1ibxirnIWJrObb-w as did:web:csoai.org#dsh.", "estate": "master-harness/knowledge/frameworks-drum/docs/MASTER_FRAMEWORK.md"},
    {"id": "un-outer-space-treaty", "name": "UN Outer Space Treaty (1967)", "kind": "charter", "issuer": "United Nations", "region": "Space", "binding": True, "status": "in force", "effective": "1967", "description": "Treaty on Principles Governing the Activities of States in the Exploration and Use of Outer Space — the constitution of space law: non-appropriation, free access, state responsibility for national space activities incl. private actors. 115+ parties.", "estate": "web (UN OOSA)"},
    {"id": "un-rescue-agreement", "name": "UN Rescue Agreement (1968)", "kind": "charter", "issuer": "United Nations", "region": "Space", "binding": True, "status": "in force", "effective": "1968", "description": "Agreement on the Rescue of Astronauts — duty to rescue/return astronauts and space objects.", "estate": "web (UN OOSA)"},
    {"id": "un-liability-convention", "name": "UN Liability Convention (1972)", "kind": "charter", "issuer": "United Nations", "region": "Space", "binding": True, "status": "in force", "effective": "1972", "description": "Convention on International Liability for Damage Caused by Space Objects — absolute liability for surface damage, fault liability in space. The liability spine for space-industry AI.", "estate": "web (UN OOSA)"},
    {"id": "un-registration-convention", "name": "UN Registration Convention (1975)", "kind": "charter", "issuer": "United Nations", "region": "Space", "binding": True, "status": "in force", "effective": "1975", "description": "Convention on Registration of Objects Launched into Outer Space — mandatory registry of space objects.", "estate": "web (UN OOSA)"},
    {"id": "moon-agreement", "name": "UN Moon Agreement (1979)", "kind": "charter", "issuer": "United Nations", "region": "Space", "binding": True, "status": "in force (low adoption)", "effective": "1979", "description": "Agreement Governing the Activities of States on the Moon — common heritage of mankind; low adoption (no major space power). Relevant to Moon-colonization claims.", "estate": "web (UN OOSA)"},
    {"id": "artemis-accords", "name": "Artemis Accords (2020)", "kind": "charter", "issuer": "NASA / US State Dept", "region": "Space", "binding": False, "status": "voluntary (50+ signatories)", "effective": "2020", "description": "Principles for Moon/Mars cooperation: transparency, interoperability, emergency assistance, space-resource utilisation, deconfliction of activities. The operating charter for commercial lunar activity.", "estate": "web (nasa.gov)"},
    {"id": "iso-24113", "name": "ISO 24113 — Space Debris Mitigation", "kind": "framework", "issuer": "ISO", "region": "Space", "binding": False, "status": "active", "effective": "2023", "description": "Primary ISO standard for space-debris mitigation requirements (upper-stage passivation, disposal, collision avoidance). The technical spine for orbital-safety measurement.", "estate": "web (ISO)"},
    {"id": "copuos-debris-guidelines", "name": "UN COPUOS Space Debris Mitigation Guidelines", "kind": "framework", "issuer": "UN COPUOS", "region": "Space", "binding": False, "status": "active", "effective": "2007 (rev. 2021)", "description": "Voluntary guidelines for debris mitigation adopted by the UN — the political consensus behind ISO 24113.", "estate": "web (UN OOSA)"},
    {"id": "itu-radio-regulations", "name": "ITU Radio Regulations (orbital slots/frequencies)", "kind": "framework", "issuer": "ITU", "region": "Space", "binding": True, "status": "in force", "effective": "rolling (World Radio Conferences)", "description": "Allocation of radio frequencies + orbital slots for satellites — the licensing gate every space-data/constellation operator must pass.", "estate": "web (ITU)"},
    {"id": "ecss-standards", "name": "ECSS — European Cooperation for Space Standardization", "kind": "framework", "issuer": "ECSS", "region": "Space", "binding": False, "status": "active", "effective": "ongoing", "description": "The European space engineering/product-assurance/management standards family — the de-facto quality spine for European space procurement incl. software/AI.", "estate": "web (ECSS)"},
    {"id": "eu-space-law", "name": "EU Space Law / EU Space Act (proposal)", "kind": "regulation", "issuer": "European Commission", "region": "EU", "binding": False, "status": "proposed (Council compromise text 2026; still in legislative process)", "effective": "2025 proposal · Council compromise 2026 · not yet adopted (verified 2026-08-21)", "description": "Proposed EU space legislation: safety, resilience, sustainability incl. debris + space-traffic management. Council compromise (2026) turns debris/traffic rules into real operator duties and aligns cybersecurity with NIS2; 11+ months and 2 revisions in, still not ready for government approval. Track status before claiming in force.", "estate": "web (European Commission; kratosspace.com; space.commerce.gov May-2026 update)"},
    {"id": "eu-space-programme", "name": "EU Space Programme Regulation (EU) 2021/696", "kind": "regulation", "issuer": "EU", "region": "EU", "binding": True, "status": "in force", "effective": "2021", "description": "The EU Space Programme (Galileo, Copernicus, EGNOS, GOVSATCOM, SST) + data policy for space-derived data — the space-data regulatory base.", "estate": "web (EUR-Lex)"},
    {"id": "uk-outer-space-act", "name": "UK Outer Space Act 1986", "kind": "regulation", "issuer": "UK", "region": "UK", "binding": True, "status": "in force", "effective": "1986", "description": "UK licensing of outer-space activities — operator licensing, liability, insurance for UK space activities.", "estate": "web (legislation.gov.uk)"},
    {"id": "uk-space-industry-act", "name": "UK Space Industry Act 2018", "kind": "regulation", "issuer": "UK", "region": "UK", "binding": True, "status": "in force", "effective": "2018 (regulations phased)", "description": "UK launch/spaceport licensing regime (spaceflight activities, range safety) — the UK commercial space gate.", "estate": "web (legislation.gov.uk)"},
    {"id": "us-commercial-space-launch", "name": "US Commercial Space Launch Act + FAA Part 450", "kind": "regulation", "issuer": "US (FAA/AST)", "region": "US", "binding": True, "status": "in force", "effective": "1984 (Part 450 2021)", "description": "US licensing of commercial launch/reentry (FAA AST) — the world's busiest commercial-space licensing regime.", "estate": "web (FAA)"},
    {"id": "iso-27001", "name": "ISO/IEC 27001:2022 — Information Security Management", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2022 (rev)", "description": "The InfoSec management-system standard — the security base every AI compliance program attaches to (Annex A controls; the audit/attestation spine). Estate corpus references it pervasively; now indexed.", "estate": "web (ISO) + estate compliance corpus"},
    {"id": "iso-27018", "name": "ISO/IEC 27018 — Cloud PII Protection", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2019", "description": "Code of practice for protecting PII in public clouds acting as PII processors — the cloud-privacy control set for AI data pipelines.", "estate": "web (ISO)"},
    {"id": "iso-27701", "name": "ISO/IEC 27701 — Privacy Information Management", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2019", "description": "Privacy extension to 27001 — the PIMS standard for GDPR/UK-GDPR-aligned privacy management.", "estate": "web (ISO)"},
    {"id": "iso-22989", "name": "ISO/IEC 22989 — AI Concepts and Terminology", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2022", "description": "The AI vocabulary/concepts standard — the shared terminology spine for the AI standards family.", "estate": "web (ISO)"},
    {"id": "iso-23053", "name": "ISO/IEC 23053 — Framework for AI Systems using ML", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2022", "description": "The ML-system framework standard — lifecycle stages, roles, and governance touchpoints for ML-based AI systems.", "estate": "web (ISO)"},
    {"id": "iso-24028", "name": "ISO/IEC 24028 — AI Trustworthiness Overview", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2023", "description": "Overview of trustworthiness in AI — transparency, explainability, controllability, robustness across the AI lifecycle.", "estate": "web (ISO)"},
    {"id": "iso-5259", "name": "ISO/IEC 5259 — AI Data Quality", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2024", "description": "Data quality for analytics and ML — the training/eval data quality family (the estate's data-moat measurement angle).", "estate": "web (ISO)"},
    {"id": "iso-17020", "name": "ISO/IEC 17020 — Conformity Assessment (Inspection)", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2012", "description": "Requirements for inspection bodies — the conformity-assessment spine relevant to independent AI evaluation bodies.", "estate": "web (ISO)"},
    {"id": "iso-10218", "name": "ISO 10218 — Robotics Safety", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2011 (rev 2024/25 in progress)", "description": "Industrial robot safety — the robotics-industry safety standard (relevant to the Tesla/AV + robotics sectors).", "estate": "web (ISO)"},
    {"id": "iso-9001", "name": "ISO 9001 — Quality Management", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2015", "description": "The quality-management baseline — process quality that AI-management systems build on.", "estate": "web (ISO)"},
    {"id": "iso-31000", "name": "ISO 31000 — Risk Management", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018", "description": "Risk-management principles/process — the generic risk spine under AI risk frameworks.", "estate": "web (ISO)"},
    {"id": "iso-14001", "name": "ISO 14001 — Environmental Management", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2015", "description": "Environmental management system — the sustainability baseline (space/energy sectors).", "estate": "web (ISO)"},
    {"id": "iso-45001", "name": "ISO 45001 — Occupational Health & Safety", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018", "description": "OHS management — workplace safety management system.", "estate": "web (ISO)"},
    {"id": "iso-20000", "name": "ISO/IEC 20000 — IT Service Management", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018", "description": "IT service management system — the service-delivery standard.", "estate": "web (ISO)"},
    {"id": "nist-ai-600-1", "name": "NIST AI 600-1 — Generative AI Profile", "kind": "framework", "issuer": "NIST", "region": "US", "binding": False, "status": "active", "effective": "2024", "description": "The GenAI risk profile extending the AI RMF — hallucination, prompt injection, training-data privacy, harmful content. Missing-until-now from the drum despite the estate regulators matrix tracking it.", "estate": "clawd/_compintel/regulators-matrix.md + web (NIST)"},
    {"id": "bsi-pas-1885", "name": "BSI PAS 1885 — Safe Deployment of CAVs (foundational safety)", "kind": "framework", "issuer": "BSI", "region": "UK", "binding": False, "status": "active", "effective": "2020", "description": "The foundational-safety standard for connected & automated vehicles — complements PAS 1880 (already indexed) on the safety-case layer for AVs.", "estate": "web (BSI) + estate compliance corpus"},
    {"id": "iso-13485", "name": "ISO 13485 — Medical Devices QMS", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2016", "description": "Quality management for medical devices — the regulatory QMS spine for healthcare-AI products (healthcare sector).", "estate": "web (ISO)"},
    {"id": "iso-14064", "name": "ISO 14064 — GHG Accounting & Verification", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018", "description": "Greenhouse-gas accounting/verification — the sustainability-measurement standard (CSRD/ESRS adjacency).", "estate": "web (ISO)"},
    {"id": "iso-20022", "name": "ISO 20022 — Financial Messaging", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2013 (migration ongoing)", "description": "The global financial-messaging standard — the payment/messaging spine for finance-sector AI (with ISO 8583).", "estate": "web (ISO)"},
    {"id": "iso-8583", "name": "ISO 8583 — Financial Transaction Card Messages", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2003 (rev)", "description": "The card-transaction message standard — legacy finance protocol (adjacent to the cobol-bridge verticals).", "estate": "web (ISO)"},
    {"id": "nist-ir-8477", "name": "NIST IR 8477 — Cybersecurity & Privacy Mapping Guide", "kind": "framework", "issuer": "NIST", "region": "US", "binding": False, "status": "initial public draft (Aug 2023); a withdrawn-draft record exists — verify final status before citing as current", "effective": "2023", "description": "Mapping Relationships Between Documentary Standards, Regulations, Frameworks, and Guidelines: Developing Cybersecurity and Privacy Concept Mappings. Directly relevant to the drum's crosswalk/ground-truth machinery — how instruments map to each other. VERIFIED 2026-08-22 (holy-of-sources: folded only after confirming the title/scope; the withdrawn-draft flag is recorded honestly).", "estate": "web — https://csrc.nist.gov/pubs/ir/8477/ipd (verified via NIST + CSRC sources)"},
    {"id": "iso-21448", "name": "ISO 21448 — SOTIF (Safety of the Intended Functionality)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2022", "description": "Safety of the Intended Functionality for road vehicles — the AV safety-standard complement to ISO 26262 (handles functional insufficiencies, not just failures). Complements the Tesla/AV sector.", "estate": "web (ISO)"},
    {"id": "iso-11898", "name": "ISO 11898 — CAN Bus (Controller Area Network)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2015 (rev)", "description": "The automotive CAN bus protocol family — the in-vehicle networking spine (adjacent to the estate's vehicle-protocol/cobol-bridge verticals + commercial-vehicle charter).", "estate": "web (ISO)"},
    {"id": "iso-14229", "name": "ISO 14229 — UDS (Unified Diagnostic Services)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2020 (rev)", "description": "Unified Diagnostic Services — the vehicle-diagnostics protocol (with ISO 14230 KWP2000 + ISO 15765 CAN-based transport). Automotive service/repair + fleet telemetry.", "estate": "web (ISO)"},
    {"id": "iso-13482", "name": "ISO 13482 — Personal Care Robots Safety", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2014", "description": "Safety requirements for personal-care robots (mobile servant, physical assistant, person carrier) — the robotics safety standard for non-industrial robots; complements ISO 10218.", "estate": "web (ISO)"},
    {"id": "iso-25010", "name": "ISO/IEC 25010 — Software Product Quality", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2011 (rev in progress)", "description": "Software quality model (functional suitability, performance, security, reliability, usability) — the quality-measurement substrate for software/AI products.", "estate": "web (ISO)"},
    {"id": "iso-19650", "name": "ISO 19650 — BIM Information Management", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018", "description": "Building Information Modelling info-management — the construction/asset digital-twin standard (adjacent to the construction/land-law verticals + digital-twin work).", "estate": "web (ISO)"},
    {"id": "iso-10303", "name": "ISO 10303 — STEP (Product Data Exchange)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "1994 (ongoing parts)", "description": "Standard for the Exchange of Product model data — the enterprise/product-data interchange standard (manufacturing + engineering-data integration).", "estate": "web (ISO)"},
    {"id": "iso-19115", "name": "ISO 19115 — Geographic Metadata", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2014", "description": "Geographic information metadata standard — the geospatial/EO metadata spine (adjacent to the space-data / Earth-observation sector + Copernicus).", "estate": "web (ISO)"},
    {"id": "iso-19136", "name": "ISO 19136 — GML (Geography Markup Language)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2007", "description": "Geography Markup Language — the geospatial data-encoding standard (with ISO 19100 series).", "estate": "web (ISO)"},
    {"id": "iso-20077", "name": "ISO 20077 — Vehicle CAD (Computer Aided Diagnosis)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active (verify specifics)", "effective": "2018", "description": "Road vehicles — extended vehicle (ExVe) diagnostics framework; cited in the estate's vehicle-protocol corpora. Verify full title before citing as precise.", "estate": "web (ISO) + estate vehicle-protocol corpora"},
    {"id": "iso-17025", "name": "ISO/IEC 17025 — Testing & Calibration Laboratories", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2017", "description": "General requirements for the competence of testing and calibration laboratories — THE measurement-instrument standard (the estate's measurement-doctrine angle: lab competence to make defensible measurements).", "estate": "web (ISO)"},
    {"id": "iso-17021", "name": "ISO/IEC 17021 — Conformity Assessment (Management Systems)", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2015", "description": "Requirements for bodies auditing/certifying management systems — the certification-body standard (ISO 42001 attestation body path).", "estate": "web (ISO)"},
    {"id": "iso-17065", "name": "ISO/IEC 17065 — Product/Service Certification Bodies", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2012", "description": "Requirements for bodies certifying products/processes/services — the product-certification-body standard.", "estate": "web (ISO)"},
    {"id": "iso-19011", "name": "ISO 19011 — Auditing Management Systems", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018", "description": "Guidelines for auditing management systems — the audit-process standard (the audit-and-promote/AUDIT stage's ISO counterpart).", "estate": "web (ISO)"},
    {"id": "iso-22301", "name": "ISO 22301 — Business Continuity", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2019", "description": "Business continuity management systems — resilience/BCP standard (adjacent to DORA/NIS2 resilience).", "estate": "web (ISO)"},
    {"id": "iso-26000", "name": "ISO 26000 — Social Responsibility", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2010", "description": "Social responsibility guidance — the ESG/social-responsibility standard (CSRD adjacency).", "estate": "web (ISO)"},
    {"id": "iso-27000", "name": "ISO/IEC 27000 — InfoSec Vocabulary & Overview", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018", "description": "The InfoSec management-systems family vocabulary/overview — the umbrella for 27001/27002/27017/27018/27701.", "estate": "web (ISO)"},
    {"id": "iso-27002", "name": "ISO/IEC 27002 — InfoSec Controls", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2022", "description": "Information security controls reference (the practical control set under 27001) — the security-control catalogue most AI programs map against.", "estate": "web (ISO)"},
    {"id": "iso-12100", "name": "ISO 12100 — Machinery Safety (General)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2010", "description": "General machinery-safety risk assessment/risk reduction — the umbrella for machinery safety (with ISO 13849 control-system safety + 10218 robots).", "estate": "web (ISO)"},
    {"id": "iso-13849", "name": "ISO 13849 — Safety-Related Control Systems (PL)", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2023 (rev)", "description": "Safety of machinery — safety-related parts of control systems (Performance Levels) — the functional-safety-of-control standard for machinery/robotics automation.", "estate": "web (ISO)"},
    {"id": "iso-17024", "name": "ISO/IEC 17024 — Personnel Certification Bodies", "kind": "framework", "issuer": "ISO/IEC", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2012", "description": "Requirements for bodies certifying PERSONS — the 'certify the certifiers' standard; directly relevant to the estate's certification-ladder (CASA) methodology and the measurement-doctrine's credential-neutrality angle.", "estate": "web (ISO)"},
    {"id": "iso-10668",
 "name": "ISO 10668 — Brand Valuation", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2010", "description": "The brand-valuation standard (cost/market/income approaches + syntax of brand valuation) — the estate's domain/valuation measurement angle (the domain-strength playbook).", "estate": "web (ISO) + estate domain-monetization plan"},
    {"id": "iso-26262", "name": "ISO 26262 — Functional Safety of Road Vehicles", "kind": "framework", "issuer": "ISO", "region": "ISO/IEC", "binding": False, "status": "active", "effective": "2018 (rev)", "description": "The road-vehicle functional-safety standard — completes the Tesla/AV sector (with ISO 21434 cybersecurity + UN R157 ALKS): safety lifecycle, ASIL grades, safety cases for autonomous driving.", "estate": "web (ISO)"},
 {"id": "councilof-ai-monorepo-packages",
    "name": "councilof-ai-monorepo — 55 csoai-* packages register", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "living", "effective": "2026", "description": "The monorepo package register (55/55 migrated, verified 2026-08-20): csoai-core, csoai-crosswalk, csoai-fisher-rao, csoai-arena, csoai-asi-evolve, csoai-council, csoai-chain, csoai-certification-loop, csoai-capability-registry, csoai-affective-safety, csoai-a2a-swarm, csoai-cpo-calculator, csoai-brain-chain, csoai-engine, csoai-fleet, csoai-city, csoai-dream, csoai-families, csoai-birth, csoai-alphabet, csoai-alchemist, csoai-article-zero, csoai-bus-redis + 33 more. The 'mono repo ALL framework' register — each package is an estate artifact (target shape in master doc §6); not folded as individual external frameworks.", "estate": "clawd/councilof-ai-monorepo/packages (55)"},
    {"id": "sov-signal-index-doctrine", "name": "SOV SIGNAL vs the drum index — the honest distinction", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "doctrine note", "effective": "2026-08-22", "description": "Answer to 'is this SOV SIGNAL?': the drum is the REFERENCE/metadata index (what exists, sourced); SOV SIGNAL is the MEASURED trust gauge (Fisher-Rao distance from the permitted manifold, the trust gauge). They compose — drum → NN/GNN feature layer → GSPC axes + permitted manifold → SOV SIGNAL distance. The drum is the index the gauge is computed over, not the gauge; presenting the catalog as 'the SOV SIGNAL index' overclaims. The GNN/MLP numbers are catalogue-classification benchmarks, not trust measurements.", "estate": "master-harness/knowledge/frameworks-drum/docs/SOV_SIGNAL_INDEX.md"},
    {"id": "catalog-graph-model", "name": "Catalog graph + NN/GNN model-layer (kind .642 / binding .908 / GNN .725 / feature layer)", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "measured 2026-08-22", "effective": "2026-08-22", "description": "The drum's catalog as a learnable graph (596 nodes, 11,035 issuer/region edges) + NN/GNN trained on it with the promote-gate protocol: kind-classification 0.283 baseline -> 0.642 MLP -> 0.725 GNN-lite (pure-torch message passing); binding-prediction 0.850 -> 0.908 MLP; region NOT-PROMOTED (degenerate baseline).  Kind one-hot and binding features dropped as label leaks (ledger #17). Models are the FEATURE LAYER for a SOV SIGNAL-style gauge, not the gauge itself. Pod path complete (ship_to_pod + ingest_sovos).", "estate": "master-harness/knowledge/frameworks-drum/train/ (build_graph.py, corpus_model.py, graph_model.py)"},
    {"id": "space-industry", "name": "Space Industry — Moon · Mars · spaceports", "kind": "sector", "issuer": "CSOAI LTD", "region": "Sector", "binding": False, "status": "open", "effective": "2026", "description": "The space sector: orbital ops, Moon/Mars colonization, spaceports. OPEN in the drum (no space industry coverage yet). Estate coverage: MEOK Space universe (meok-universe/research/meok_earth_space_master.md), SOV_SPACE tabs, C_SPACE_ARCHITECTURE, UK Space Agency + UK Space Command packs. Measurement axes: safety, sovereignty, transparency, continuity. Crosswalk candidates: UN outer-space treaties, ISO 24113 (space debris), EU Space Law (2025 proposal).", "estate": "clawd/meok-universe/research/meok_earth_space_master.md"},
    {"id": "space-data", "name": "Space Data & Earth Observation", "kind": "sector", "issuer": "CSOAI LTD", "region": "Sector", "binding": False, "status": "open", "effective": "2026", "description": "Satellite telemetry, Earth-observation imagery, space-derived data. OPEN. Estate: satellite-imagery overlay in the MEOK Earth layer, sov_space_docstore. Measurement axes: privacy, data governance, transparency. Crosswalk candidates: Copernicus data policies, UK Space Agency licensing, EU space data economy regs.", "estate": "clawd/kimi-regen/kaggle/sov_space_docstore.py"},
    {"id": "space-data-centers", "name": "Orbital / Space Data Centers", "kind": "sector", "issuer": "CSOAI LTD", "region": "Sector", "binding": False, "status": "open", "effective": "2026", "description": "Data centers in orbit — the emerging edge of the space data economy. OPEN (no estate coverage, no binding regime yet — honest: watch ISO/ITU + EU Space Law). Measurement axes: continuity, sovereignty, efficiency, sustainability.", "estate": ""},
    {"id": "xai-grok", "name": "xAI / Grok (frontier lab)", "kind": "sector", "issuer": "CSOAI LTD", "region": "Sector", "binding": False, "status": "open", "effective": "2026", "description": "The xAI/Grok frontier-lab actor (incl. SpaceXAI group context: Cursor deal closed Aug 2026, Grok Bot beta). An industry actor to MEASURE, never a partner. OPEN in the drum. Crosswalk: EU AI Act GPAI obligations (Art 50-56), model-spec/Preparedness-type frameworks. Measurement axes: jail, safety, transparency, sovereignty.", "estate": "master-harness/README.md (fork-register note)"},
    {"id": "tesla-automotive-ai", "name": "Tesla / Autonomous-Vehicle AI", "kind": "sector", "issuer": "CSOAI LTD", "region": "Sector", "binding": False, "status": "partial", "effective": "2026", "description": "Tesla + the autonomous-vehicle AI industry. PARTIAL in the drum: UN Regulation 157 (automated lane-keeping) + ISO 21434 (road-vehicle cybersecurity) already catalogued; commercial-vehicle charter exists. Crosswalk candidates: UK AV Bill, EU AI Act Annex III high-risk (road safety). Measurement axes: safety, accountability, human oversight, care.", "estate": "clawd/csoai.org/charter2/commercialvehicle-charter.html"},
    {"id": "casa-sector-map", "name": "CASA Sector Map — covered vs open industries", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "living", "effective": "2026-08-20", "description": "The industry map behind the CASA certification ladder (Foundation/Practitioner/Lead-Auditor/Director per industry charter). COVERED in the drum (charter2 + 34 hives): finance, healthcare, defence, energy, education, biotech, agriculture, transport, legal, pharmacy, logistics, insurance, manufacturing, opticians, home-care, research, commercial-vehicle, diyhelp, fishkeeper, grabhire, koikeeper, landlaw, muckaway, planthire, pokerhud, suicidestop, science + sovereignty family. OPEN (this axis): space industry, space data, orbital data centers, xAI/Grok, Tesla/autonomous-vehicle AI, robotics (candidate), quantum (candidate). Each open sector gets a drum sector card + measurement axes.", "estate": "clawd/csoai.org/charter2/ + sovereign-charters (34 hives)"},
    {"id": "findings-blog-drafts", "name": "_findings corpus — AI governance blog drafts", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "mined", "effective": "2026-06", "description": "The _findings corpus (103 md files) mined for unindexed material: BLOG_DRAFT_AI_GOVERNANCE_VS_COMPLIANCE, BLOG_DRAFT_CHOOSING_AI_COMPLIANCE_VENDOR, BLOG_DRAFT_DORA_COMPLIANCE, BLOG_DRAFT_EU_AI_ACT_ARTICLE_50, WAVE_GOVERNANCE and others — governance/compliance content for the drum's article layer. Full corpus scan is a mining-queue item (P15-43); this entry registers the corpus as a mined surface.", "estate": "clawd/_findings/ (103 files)"},
    {"id": "sov-space-visual-mind", "name": "SOV-Space Visual Mind (VLM registry)", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "code exists (needs VLM runtime)", "effective": "2026", "description": "The estate's visual-perception layer — soul/visual_mind.py: a VLM registry (MiniCPM-o 4.5, InternVL3.5, Qwen2.5-VL, CogAgent) in 'honey fluid mode' (frozen knowledge base + VLM visual understanding on top). NEURAL, not neuro-symbolic per se; the estate's real neuro-symbolic pattern is neural-score + symbolic-frozen-predicate (the conformal router). Wires into the visual-pattern signal layer (master doc §4).", "estate": "clawd/kimi-regen/soul/visual_mind.py"},
    {"id": "silica-capillary-memory", "name": "Silica-Capillary Hybrid Memory (Project AURUM)", "kind": "article", "issuer": "MEOK AI Labs", "region": "MEOK", "binding": False, "status": "design (physics real, hardware not built)", "effective": "2026-06-28", "description": "5D silica optical memory (femtosecond nanogratings; Southampton 2013 / Microsoft Project HSD science — 360 TB/disc, 13.8B-yr stability) merged with capillary microfluidic cooling (lab-on-a-chip) for the Sovereign Orb. Real physics, farm-manufacturable in principle, HONEST register: DESIGN spec shipped, no hardware commitment. The water/capillary memory thread's real estate artifact.", "estate": "clawd/_TABS/_inventory/MEOK_SILICA_CAPILLARY_W12_2026-06-28/00_SILICA_CAPILLARY_SYNTHESIS.md"},
    {"id": "meok-labs-master-consolidation", "name": "MEOK Labs Master Consolidation", "kind": "article", "issuer": "MEOK", "region": "MEOK", "binding": False, "status": "living", "effective": "2026", "description": "The MEOK Labs design canon — meok-labs/MEOK_LABS_MASTER_CONSOLIDATION.md + meok-labs-engine product brief: the labs' R&D workstreams (incl. silica-capillary, visual mind, actuation MCPs). Source-of-truth pointer for the labs' builds.", "estate": "clawd/meok-labs/MEOK_LABS_MASTER_CONSOLIDATION.md"},
    {"id": "physical-computation-map", "name": "Physical Computation Map — core-rope/water/EUNOMIA vision grounded", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "grounding doc", "effective": "2026-08-21", "description": "Honest triage of the physical-computation thread: real science (5D optical storage, FLODAC fluidics, memristors, Drosophila connectome, neuromorphic chips) vs buildable-now software (crossbar=attention, graded states=conformal score, oscillator=DRUM clock, 3KB cards=honey) vs metaphor (EUNOMIA/venturi-universal framing). Binding rule: hardware claims carry DESIGN-not-RUNNING register.", "estate": "master-harness/knowledge/frameworks-drum/docs/PHYSICAL_COMPUTATION_MAP.md"},
    {"id": "sovos-oowm-index-mapping", "name": "Drum → SOVOS/MEOK OOWM index mapping (tested)", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "tested 2026-08-21", "effective": "2026-08-21", "description": "The drum's surfaces ingested into the SOVOS OOWM knowledge index (oowm.knowledge.OOWMIndex, the council-oowm substrate; SOVOS=MEOK codename binding): 5 docs (doctrine, catalog digest, feeds, validation, scorecard), 5/6 test queries resolved to the right surface. Mapping TESTED; production wiring = the estate-mine ingest lane adding drum surfaces as corpus sources.", "estate": "clawd/sov33-oowm/oowm/ (OOWMIndex) + drum docs"},
    {"id": "meok-compliance-gateway-registry", "name": "MEOK Compliance Gateway — MCP Registry (136 entries)", "kind": "article", "issuer": "MEOK", "region": "MEOK", "binding": False, "status": "living", "effective": "2026", "description": "The estate's compliance-MCP source of truth (136 entries per PACK_INDEX). The drum's 40 compliance/audit MCPs were mined from mcp-marketplace; this entry registers the fuller gateway registry as the canonical count. NOTE: count drift (843 dirs / 207 repos / ~200 marketplace vs 136 gateway vs the one-registry target) is a monorepo dedupe item (master doc §6) — this entry is the source-of-truth pointer, not another count.", "estate": "clawd/meok-compliance-gateway (136 entries)"},
    {"id": "next-100-moves", "name": "NEXT 100 MOVES — drum + master framework execution queue", "kind": "article", "issuer": "CSOAI LTD", "region": "CSOAI", "binding": False, "status": "living", "effective": "2026-08-20", "description": "LEARN/ALIGN/EAT 100-move plan across 10 phases: drum hardening (lint gate, tests, drum_watch), Stage 1 (conformal 90/10 router, signed Knowledge archive, MAPE-K collapse), Stage 2 (promote-gate, evolve loop in one verifier-rich domain), wiring legs (EAT 7-box ticks, DORADO reg-bank sync, SOV SIGNAL features), monorepo substrate (receipts consolidation, one registry, crosswalk 3-to-1), scale (key-continuity charter, red-team drill, task-allocation ops). Moves tagged [GATE] and [LANE]; nothing marked done without evidence.", "estate": "master-harness/knowledge/frameworks-drum/docs/NEXT_100_MOVES.md"},
    {"id": "master-framework-validation", "name": "Master Framework Validation — self-improving evolve-and-promote loop research", "kind": "article", "issuer": "CSOAI LTD Research", "region": "CSOAI", "binding": False, "status": "research", "effective": "2026-08-20", "description": "Literature-grounded validation of the doctrine: AlphaEvolve/FunSearch/DGM/STOP results, failure modes (reward hacking 73.8%, rise-and-collapse, SWE-bench ~33% leakage), split conformal prediction / conformal risk control for the router, MAPE-K collapse, Vaccaro human-AI meta-analysis (g=-0.23 decisions, g=0.64 content), promote-gate protocol. Caveats included; primary formulas to verify before formal spec.", "estate": "master-harness/knowledge/frameworks-drum/docs/RESEARCH_VALIDATION.md"},
]

# ---------------------------------------------------------------------------
# MINING PARSERS — fold _mining/*.md (web sweeps) into catalog items
# ---------------------------------------------------------------------------
FIELD_ALIASES = {
    "kind": ["kind"],
    "issuer": ["body", "issuer", "org", "authors/org", "organisation", "organization"],
    "region": ["region", "jurisdiction", "scope", "source", "region/jurisdiction"],
    "status": ["status", "effective", "binding"],
    "effective": ["effective", "year", "date", "year/version"],
    "binding": ["binding"],
    "description": ["purpose", "substance", "relevance", "notable for our use", "description", "key obligations", "penalties"],
    "source": ["source url", "source", "estate source"],
}


def norm_kind(k):
    k = (k or "").lower().strip()
    if "framework" in k or "standard" in k or "audit" in k:
        return "framework"
    if "charter" in k or "declaration" in k or "principle" in k or "compact" in k:
        return "charter"
    if "regulation" in k or "act" in k or "law" in k or "directive" in k or "rule" in k:
        return "regulation"
    if "mcp" in k:
        return "article"
    return "article"


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:80] or "item"


def parse_mining_file(path, kind):
    items = []
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    cur = None
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line.strip())
        if m:
            if cur:
                items.append(cur)
            cur = {"id": slugify(m.group(1)), "name": m.group(1).strip(), "kind": norm_kind(kind), "status": "mined", "binding": None, "sources": []}
            continue
        if cur is None:
            continue
        # bullets may carry several pipe-separated `**label:** value` segments
        for seg in line.split(" | "):
            fm = re.match(r"^\s*[-*+]\s*\*\*([^*:]+):\*\*\s*(.*?)\s*$", seg)
            if not fm:
                fm = re.match(r"^\s*\*\*([^*:]+):\*\*\s*(.*?)\s*$", seg)
            if not fm:
                continue
            label, val = fm.group(1).strip(), fm.group(2).strip()
            field = None
            for f, aliases in FIELD_ALIASES.items():
                if label.lower() in [a.lower() for a in aliases]:
                    field = f
                    break
            if not field:
                continue
            if field == "kind":
                cur["kind"] = norm_kind(val)
            elif field == "binding":
                cur["binding"] = val.lower().startswith(("yes", "true", "binding"))
            elif field == "source" and val:
                cur.setdefault("sources", []).append(val)
            elif field == "description":
                cur["description"] = (cur.get("description") or "") + (" " if cur.get("description") else "") + val
            else:
                cur[field] = val
    if cur:
        items.append(cur)
    return items


# ---------------------------------------------------------------------------
# DOCTRINE-CLEAN SANITIZER — banned/internal codenames must never appear on
# public surfaces (catalog.json, cards, llms.txt, agent card). Estate paths
# that contain them are reduced to a public-safe pointer.
# ---------------------------------------------------------------------------
INTERNAL_CODENAMES = ["sov3", "sov33", "oowm", "sigil", "horus", "liquid-kan", "maternal", "byzantine", "bft", "ceasai"]


def sanitize_path(path):
    low = (path or "").lower()
    if any(c in low for c in INTERNAL_CODENAMES):
        parts = path.split("/")
        keep = "/".join(parts[:2])
        return f"{keep}/ (internal file — exact name in estate)"
    return path


def scrub_text(text):
    """Replace internal codenames in prose with a public-safe marker."""
    out = text or ""
    for c in sorted(INTERNAL_CODENAMES, key=len, reverse=True):
        out = re.sub(rf"(?i)\b{re.escape(c)}\b", "[internal]", out)
        out = re.sub(rf"(?i){re.escape(c)}(?=[-_0-9])", "[internal]", out)
    return out


def is_internal(item):
    hay = f"{item.get('name', '')} {item.get('description', '')} {item.get('status', '')}".lower()
    return any(c in hay for c in INTERNAL_CODENAMES)


def build():
    items = list(SEED)

    def norm(name):
        return re.sub(r"[^a-z0-9]+", "", name.lower())

    seen = {norm(it["name"]) for it in items}
    mined_sources = {}
    for fname, kind in (("frameworks.md", "framework"), ("charters.md", "charter"),
                        ("regulations.md", "regulation"), ("articles.md", "article"),
                        ("estate.md", None)):
        p = os.path.join(MINING, fname)
        if not os.path.exists(p):
            continue
        for it in parse_mining_file(p, kind):
            key = norm(it["name"])
            if key in seen:
                continue
            seen.add(key)
            it["mined"] = "web"
            it.setdefault("description", it.get("substance") or it.get("purpose") or "")
            items.append(it)
            mined_sources[fname] = mined_sources.get(fname, 0) + 1

    items.sort(key=lambda it: (it["kind"], it["name"].lower()))
    # enforce unique ids (slug collisions between seed and mined items, e.g. 'eu-ai-pact')
    used_ids = set()
    for it in items:
        iid, n = it["id"], 2
        while iid in used_ids:
            iid = f"{it['id']}-{n}"
            n += 1
        used_ids.add(iid)
        it["id"] = iid
    for it in items:  # doctrine-clean public surfaces
        if it.get("estate"):
            it["estate"] = sanitize_path(it["estate"])
        if it.get("sources"):
            it["sources"] = [sanitize_path(s) for s in it["sources"]]
        if is_internal(it):
            it["internal"] = True
        for field in ("description", "status", "issuer", "region", "effective"):
            if it.get(field):
                it[field] = scrub_text(it[field])
    for it in items:  # freshness schema (P15-48): per-item verified date = fold date
        it["last_verified"] = datetime.date.today().isoformat()
    now = datetime.date.today().isoformat()
    catalog = {
        "pack": "frameworks-drum",
        "generated": now,
        "canary": "drum-canary-7f3a9c2e",
        "doctrine": "docs/MASTER_FRAMEWORK.md",
        "counts": {k: sum(1 for i in items if i["kind"] == k) for k in KIND_DIRS},
        "mined_from_web": mined_sources,
        "items": items,
    }
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=1, ensure_ascii=False)
    print(f"catalog.json written: {len(items)} items ({catalog['counts']}) mined={mined_sources}")
    return catalog


def write_cards(catalog):
    live_ids = set()
    for it in catalog["items"]:
        d = KIND_DIRS.get(it["kind"])
        if not d:
            continue
        live_ids.add(f"{d}/{it['id']}.md")
        os.makedirs(os.path.join(PACK, d), exist_ok=True)
        srcs = it.get("sources") or []
        if it.get("estate"):
            srcs = [sanitize_path(it["estate"])] + [sanitize_path(s) for s in srcs]
        src_lines = "\n".join(f"- {s}" for s in srcs) if srcs else "- (no source recorded)"
        card = (
            f"# {it['name']}\n\n"
            f"- **Kind:** {it['kind']} | **Issuer:** {it.get('issuer') or '—'} | **Region:** {it.get('region') or '—'}\n"
            f"- **Binding:** {'yes' if it.get('binding') else ('no' if it.get('binding') is False else '—')} | **Status:** {it.get('status') or '—'}\n"
            f"- **Effective:** {it.get('effective') or '—'}\n\n"
            f"{it.get('description') or ''}\n\n"
            f"## Sources\n{src_lines}\n"
        )
        with open(os.path.join(PACK, d, f"{it['id']}.md"), "w", encoding="utf-8") as fh:
            fh.write(card)
    # prune stale cards (items removed/renamed by dedupe in earlier builds)
    pruned = 0
    for d in set(KIND_DIRS.values()):
        dpath = os.path.join(PACK, d)
        if not os.path.isdir(dpath):
            continue
        for f in os.listdir(dpath):
            rel = f"{d}/{f}"
            if rel not in live_ids:
                os.remove(os.path.join(dpath, f))
                pruned += 1
    print(f"cards written (pruned {pruned} stale)")


# ---------------------------------------------------------------------------
# FEEDS — the drum's delivery channels to EAT / DORADO / SOV SIGNAL / markets
# ---------------------------------------------------------------------------
EAST_REGIONS = {"CN", "HK", "JP", "KR", "SG", "TW", "IN", "TH", "VN", "MY", "PH", "ID", "AU", "NZ"}
WEST_REGIONS = {"EU", "UK", "US", "CH", "NO", "CA", "ISO/IEC", "OECD", "UNESCO", "Council of Europe"}


def east_west(region):
    r = (region or "").upper()
    if any(e in r for e in ("CN", "HK", "JP", "KR", "SG", "TW", "IN", "TH", "VN", "MY", "PH", "ID", "AU", "NZ")):
        return "east"
    if any(w in r for w in ("EU", "UK", "US", "CH", "NO", "CA")):
        return "west"
    return "global"


def write_feeds(catalog):
    """Emit the delivery feeds: DORADO reg bank (reg_events.json) + EAT 7-box self-check."""
    feed_dir = os.path.join(PACK, "feeds")
    os.makedirs(feed_dir, exist_ok=True)

    regs = []
    for it in catalog["items"]:
        if it.get("kind") != "regulation" or it.get("internal"):
            continue
        regs.append({
            "regulation": it["name"],
            "id": it.get("id"),
            "region": it.get("region"),
            "pole": east_west(it.get("region")),
            "binding": it.get("binding"),
            "status": it.get("status"),
            "effective": it.get("effective"),
            "source": it.get("estate") or (it.get("sources") or [None])[0],
        })
    regs.sort(key=lambda r: (r["pole"], r["region"] or "", r["regulation"].lower()))
    # snapshot the previous feed before overwriting (feeds drum_watch deltas)
    prev_path = os.path.join(feed_dir, "reg_events.prev.json")
    cur_path = os.path.join(feed_dir, "reg_events.json")
    if os.path.exists(cur_path):
        try:
            os.replace(cur_path, prev_path)
        except OSError:
            pass
    with open(cur_path, "w", encoding="utf-8") as fh:
        json.dump({"generated": catalog["generated"], "note": "DORADO reg-bank sync source + SOV SIGNAL regulatory-pressure feature channel",
                   "count": len(regs), "events": regs}, fh, indent=1, ensure_ascii=False)

    # EAT 7-box self-check on the drum itself — honest per box (the 7-box mission def).
    eat = {
        "generated": catalog["generated"],
        "slot": "frameworks-drum",
        "mission": "measured → CI'd → signed → chained → anchored → boarded → mirrored",
        "boxes": {
            "measured": {"ok": True, "note": f"{len(catalog['items'])} items, deterministic counts, sources recorded"},
            "ci": {"ok": "partial", "note": "competitor/peer frameworks indexed; dedicated CI pass not run"},
            "signed": {"ok": False, "note": "no h3k cards emitted yet — signing rail is the council-sign leg"},
            "chained": {"ok": "partial", "note": "provenance recorded per item; not yet hash-chained into a sigil chain"},
            "anchored": {"ok": False, "note": "no OTS/Bitcoin anchor yet"},
            "boarded": {"ok": False, "note": "no public board page yet"},
            "mirrored": {"ok": True, "note": "llms.txt + A2A card + MCP registry tile + PACK_INDEX"},
        },
        "status": "PARTIAL — 2/7 true, 2 partial, 3 false (honest register)",
    }
    with open(os.path.join(feed_dir, "eat_7box.json"), "w", encoding="utf-8") as fh:
        json.dump(eat, fh, indent=1, ensure_ascii=False)
    print(f"feeds written: reg_events.json ({len(regs)} events) · eat_7box.json ({eat['status']})")


def check_catalog(catalog):
    """--check mode (move 12): fail loudly on structural problems. Exit code 1 on failure."""
    items = catalog["items"]
    ids = [i["id"] for i in items]
    problems = []
    if len(ids) != len(set(ids)):
        problems.append(f"{len(ids) - len(set(ids))} duplicate ids")
    req = ["id", "name", "kind", "status"]
    missing = [i["id"] for i in items if not all(k in i for k in req)]
    if missing:
        problems.append(f"{len(missing)} items missing required fields: {missing[:3]}")
    if sum(catalog["counts"].values()) != len(items):
        problems.append("counts do not match items")
    if catalog.get("canary") != "drum-canary-7f3a9c2e":
        problems.append("canary missing or altered (possible mirror/strip)")
    for p in problems:
        print(f"  CHECK FAIL: {p}")
    return problems


def lint_surfaces():
    """--lint mode (move 13): banned-string gate over public surfaces. Exit code 1 on hits.

    catalog.json is special: internal-codename items are stored FLAGGED internal:true and
    filtered from public MCP responses — so the lint checks only the public subset of items
    plus the catalog's non-item fields. Other public files are scanned as raw text.
    """
    def has_codename(text):
        return [c for c in INTERNAL_CODENAMES if re.search(rf"(?i)\b{re.escape(c)}\b", text)]

    hits = []
    cat_path = os.path.join(PACK, "catalog.json")
    if os.path.exists(cat_path):
        cat = json.load(open(cat_path, encoding="utf-8"))
        for f in ("pack", "generated", "canary", "doctrine", "note"):
            if f in cat:
                hits += [f"catalog.json.{f}: {c}" for c in has_codename(str(cat[f]))]
        for it in cat.get("items", []):
            if it.get("internal"):
                continue
            for field in ("name", "description", "issuer", "region", "status"):
                hits += [f"catalog.json item {it.get('id')}.{field}: {c}" for c in has_codename(str(it.get(field, "")))]
    public_files = ["llms.txt", "README.md", "docs/WIRING.md",
                    "mcp/manifest.json", "a2a/agent-card.json"]
    for f in public_files:
        p = os.path.join(PACK, f)
        if not os.path.exists(p):
            continue
        hits += [f"{f}: {c}" for c in has_codename(open(p, encoding="utf-8").read())]
    # language locks (master doc §0 — P19-82/85-88): banned claims on public surfaces
    locks = ["fully autonomous", "asi evolve", "asi evolves", "a+++++", "100/100 a+",
             "we are the only", "nobody else"]
    for f in public_files + ["docs/MASTER_FRAMEWORK.md"]:
        p = os.path.join(PACK, f)
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8").read().lower()
        for lock in locks:
            if lock in text and f != "docs/MASTER_FRAMEWORK.md":
                hits.append(f"{f}: language lock '{lock}'")
    for h in hits:
        print(f"  LINT HIT: {h}")
    return hits


if __name__ == "__main__":
    cat = build()
    if "--no-cards" not in sys.argv:
        write_cards(cat)
    write_feeds(cat)
    # move 36: the drum eats itself — every fold is archived in the Knowledge store
    try:
        sys.path.insert(0, os.path.join(PACK, "archive"))
        import knowledge_archive as ka
        entry_name = f"catalog-{cat['generated']}"
        # dedupe by fold date (a recursion incident once appended hundreds of duplicates)
        existing = set()
        if os.path.exists(ka.INDEX):
            for line in open(ka.INDEX, encoding="utf-8"):
                line = line.strip()
                if line:
                    existing.add(json.loads(line).get("name"))
        if entry_name not in existing:
            ka.append("drum-fold", entry_name,
                      {"items": len(cat["items"]), "counts": cat["counts"],
                       "canary": cat.get("canary")},
                      outcome="built", signed=False)
    except Exception as exc:  # noqa: BLE001 — archiving must never break the build
        print(f"(archive hook skipped: {exc})")
    # publish the front end (doctrine-clean board) with the catalog
    try:
        import subprocess
        subprocess.run([sys.executable, os.path.join(PACK, "site", "build_drum_site.py")], timeout=60, check=True)
    except Exception as exc:  # noqa: BLE001
        print(f"(site build skipped: {exc})")
    if "--check" in sys.argv:
        problems = check_catalog(cat)
        if problems:
            sys.exit(1)
        print("check: PASS")
    if "--lint" in sys.argv:
        hits = lint_surfaces()
        if hits:
            sys.exit(1)
        print("lint: PASS (public surfaces clean)")
