#!/usr/bin/env python3
"""Tick 289 pack DATA: NHS Scotland / National Services Scotland, Scottish Enterprise, Scottish Biometrics Commissioner."""
# Probe-verified 0 disk + 0 sitemap hits BEFORE build (tick-265 pitfall).

PACKS = [
    {
        "slug": "defoneos-nhs-scotland-national-services-ai-deep-dive-pack",
        "title": "NHS Scotland — National Services Governance AI Deep-Dive Pack",
        "agency": "NHS Scotland — National Services Scotland (NSS)",
        "agency_url": "https://www.nhsnss.org/",
        "domain": "National Health Service Shared Services",
        "desc": "National Services Scotland (NSS) is the national board providing shared services to NHS Scotland: national procurement, IT infrastructure, counter-fraud, practitioner services, and the Scottish National Blood Transfusion Service. This deep-dive pack maps 12 entry points for AI governance, 8 transformation priorities, 6 MCP servers, and 6 non-negotiable red lines anchored in Scottish health legislation.",
        "entry_points": [
            ("National Procurement & Supply Chain", "NHS National Procurement delivers ~£1.3bn annual spend across 22 NHS boards. AI spend analytics, demand forecasting, and supplier risk screening.", "procurement"),
            ("National IT Infrastructure & Digital", "NSS operates national NHS Scotland digital infrastructure including the SWAN network and national systems. AI capacity planning, incident response analytics, and system health monitoring.", "digital"),
            ("NHS Scotland Assure — Built Environment", "Healthcare built-environment assurance: estates risk, infection control standards, and capital project governance. AI estate condition modelling and capital prioritisation.", "assure"),
            ("Counter Fraud Services", "NHS Scotland Counter Fraud Services investigates fraud against the health service. AI anomaly detection, network analytics, and fraud-pattern classification.", "fraud"),
            ("Practitioner Services", "Payments to GPs, dentists, pharmacists, and ophthalmic practitioners; primary care contractor governance. AI payment integrity checks and contract compliance analytics.", "practitioner"),
            ("Scottish National Blood Transfusion Service", "SNBTS supplies blood, tissues, and cellular therapies to all Scottish hospitals. AI blood-stock modelling, donor recruitment analytics, and expiry-loss minimisation.", "blood"),
            ("Organ & Tissue Donation Services", "Organ and tissue donation under opt-out legislation. AI donor-register matching, theatre coordination, and consent-record verification.", "organ"),
            ("Data, Intelligence & Statistics", "National health data services supporting NHS boards and research. AI health-data linkage, pseudonymisation governance, and statistical disclosure control.", "data"),
            ("Information Governance & Cyber Security", "NHS Scotland cyber operations, incident response, and IG assurance. AI threat intelligence triage, phishing detection, and security-log analytics.", "cyber"),
            ("Workforce & HR Shared Services", "NHS Scotland employs ~180,000 staff; national workforce systems and pay. AI workforce analytics, roster optimisation, and wellbeing early-warning analytics.", "workforce"),
            ("Sustainability & Net Zero", "NHS Scotland climate emergency strategy — net zero by 2040. AI carbon analytics for estates, fleet, and anaesthetic gases.", "climate"),
            ("Governance & Scottish Parliament Accountability", "NSS accountability to Scottish Ministers, Scottish Parliament Health Committee, and Audit Scotland. AI governance reporting and parliamentary evidence automation.", "governance")
        ],
        "priorities": [
            "AI procurement spend analytics replacing quarterly manual returns → live category dashboards, 15% addressable savings identification",
            "AI blood-stock demand forecasting replacing static rotation tables → 30% expiry-loss reduction, emergency-reserve integrity",
            "AI counter-fraud anomaly detection replacing sample-based audit → continuous transaction screening, earlier intervention",
            "AI payment integrity checks replacing manual post-payment review → 90% faster contract-compliance verification",
            "AI cyber threat-intelligence triage replacing manual alert queues → 40% faster mean-time-to-respond, analyst focus on real threats",
            "AI estate condition modelling replacing quinquennial surveys → continuous condition monitoring, evidence-based capital prioritisation",
            "AI pseudonymisation governance replacing manual disclosure review → safer national data linkage, auditable statistical disclosure control",
            "AI workforce wellbeing early-warning replacing annual staff surveys → proactive intervention, absence-pattern analytics"
        ],
        "mcps": [
            ("defoneos-nhs-procurement-mcp", "Procurement", "Spend analytics, demand forecasting, supplier risk screening, category dashboards"),
            ("defoneos-nhs-data-governance-mcp", "Compliance", "Pseudonymisation governance, statistical disclosure control, data-sharing audit, Caldicott alignment"),
            ("defoneos-nhs-cyber-mcp", "Security", "Threat intelligence triage, phishing detection, security-log analytics, incident response support"),
            ("defoneos-nhs-fraud-mcp", "Finance", "Anomaly detection, fraud-pattern classification, network analytics, investigation support"),
            ("defoneos-nhs-blood-supply-mcp", "Health", "Blood-stock modelling, donor recruitment analytics, expiry-loss minimisation, reserve monitoring"),
            ("defoneos-nhs-workforce-mcp", "HR", "Workforce analytics, roster optimisation, wellbeing early-warning, absence-pattern analytics")
        ],
        "red_lines": [
            "National Health Service (Scotland) Act 1978 — Duties of Scottish Ministers and health boards. AI must not ration, triage, or gate clinical care outside clinical governance structures.",
            "Data Protection Act 2018 / UK GDPR — Health data is special-category data; NHS Caldicott principles apply. AI must operate under the strictest health-data regime with documented lawful basis.",
            "Human Tissue (Authorisation) (Scotland) Act 2019 — Deemed-authorisation organ donation. AI must never auto-finalise consent records; the register and family contact remain human-governed.",
            "NHS Scotland Clinical Governance — DCB-style clinical-safety standards for health software. AI must not provide diagnostic or treatment recommendations without clinical safety assurance.",
            "Equality Act 2010 (Public Sector Equality Duty) — AI must not introduce or amplify health-outcome disparities across protected characteristics.",
            "Scotland Act 1998 — Devolved health and social care. AI must respect Scottish devolved competence, NHS Scotland Board autonomy, and Scottish Parliament accountability."
        ],
        "legislation": "National Health Service (Scotland) Act 1978 / NHS Reform (Scotland) Act 2004 / Public Bodies (Joint Working) (Scotland) Act 2014 / Human Tissue (Authorisation) (Scotland) Act 2019 / DPA 2018 + UK GDPR / Equality Act 2010 / Scotland Act 1998 / Climate Change (Scotland) Act 2009"
    },
    {
        "slug": "defoneos-scottish-enterprise-economic-development-ai-deep-dive-pack",
        "title": "Scottish Enterprise — Economic Development AI Deep-Dive Pack",
        "agency": "Scottish Enterprise",
        "agency_url": "https://www.scottish-enterprise.com/",
        "domain": "Economic Development & Innovation",
        "desc": "Scottish Enterprise is Scotland's national economic development agency, supporting business growth, innovation, exports, and inward investment. This deep-dive pack maps 12 entry points for AI governance, 8 transformation priorities, 6 MCP servers, and 6 non-negotiable red lines anchored in Scottish economic development legislation and UK subsidy control.",
        "entry_points": [
            ("Business Growth & Account Management", "Account-managed support for high-growth Scottish companies. AI growth-potential scoring, intervention matching, and outcome tracking.", "growth"),
            ("Innovation & R&D Support", "Grants and support for company R&D, academic collaboration, and commercialisation. AI project-screening analytics and innovation-mapping.", "innovation"),
            ("Investment & Foreign Direct Investment", "Inward investment attraction and investor pipeline for Scotland. AI FDI opportunity matching, site-selection analytics, and investor-intelligence.", "fdi"),
            ("Export Support & Trade (SDI)", "Scottish Development International supports exporters across global markets. AI export-market opportunity mapping and trade-barrier intelligence.", "export"),
            ("Energy Transition & Low Carbon", "Support for offshore wind, hydrogen, and net-zero supply chains. AI project-readiness screening and supply-chain gap analytics.", "energy"),
            ("Digital & Advanced Manufacturing", "Digital adoption, Industry 4.0, and advanced manufacturing transformation. AI adoption-readiness assessment and productivity analytics.", "manufacturing"),
            ("Life Sciences & Health Innovation", "Scottish life sciences cluster support and company growth. AI clinical-trial pipeline mapping and cluster analytics.", "lifesciences"),
            ("Financial Readiness & Funding", "Grant, loan, and equity-readiness support with public funds. AI subsidy-control compliance screening and fund-integrity analytics.", "funding"),
            ("Place, Property & Infrastructure", "Scottish Enterprise property portfolio, speculative buildings, and site regeneration. AI portfolio performance analytics and place-based impact modelling.", "place"),
            ("Data Analytics & Economic Intelligence", "Scottish economic data, company intelligence, and evaluation. AI economic forecasting and intervention counterfactual analysis.", "intelligence"),
            ("Equality, Fair Work & Inclusive Growth", "Fair Work First conditionality and inclusive-growth objectives. AI fair-work compliance tracking and equality analytics.", "fairwork"),
            ("Governance & Scottish Government Accountability", "Scottish Enterprise accountability to Scottish Ministers, Scottish Parliament Economy Committee, and Audit Scotland. AI governance reporting and evaluation automation.", "governance")
        ],
        "priorities": [
            "AI growth-potential scoring replacing manual account reviews → consistent intervention matching, measurable outcome tracking",
            "AI export-market opportunity mapping replacing static market guides → live opportunity feeds, sector-country fit scoring",
            "AI FDI pipeline analytics replacing spreadsheet tracking → real-time pipeline dashboards, aftercare risk early-warning",
            "AI energy-transition supply-chain gap analytics replacing consultancy studies → continuous gap mapping, project-readiness screening",
            "AI subsidy-control compliance screening replacing manual checks → automatic Subsidy Control Act 2022 boundary checking",
            "AI economic intelligence dashboards replacing annual evaluation reports → continuous counterfactual analysis, live KPIs",
            "AI fair-work compliance tracking replacing periodic audits → continuous Fair Work First conditionality monitoring",
            "AI governance reporting replacing quarterly manual returns → automated Scottish Government-ready evidence packs"
        ],
        "mcps": [
            ("defoneos-enterprise-growth-mcp", "Economy", "Growth-potential scoring, intervention matching, account analytics, outcome tracking"),
            ("defoneos-export-intelligence-mcp", "Trade", "Export-market opportunity mapping, trade-barrier intelligence, sector-country fit scoring"),
            ("defoneos-fdi-pipeline-mcp", "Investment", "FDI opportunity matching, investor intelligence, pipeline dashboards, aftercare monitoring"),
            ("defoneos-subsidy-control-mcp", "Compliance", "Subsidy Control Act 2022 boundary checking, fund-integrity analytics, transparency-return automation"),
            ("defoneos-energy-transition-mcp", "Energy", "Offshore-wind and hydrogen supply-chain gap analytics, project-readiness screening, cluster mapping"),
            ("defoneos-economic-intelligence-mcp", "Intelligence", "Economic forecasting, intervention counterfactual analysis, evaluation analytics, KPI dashboards")
        ],
        "red_lines": [
            "Subsidy Control Act 2022 — Public subsidy decisions are statutory determinations. AI must never autonomously approve, deny, or vary subsidy awards; it screens and surfaces.",
            "Enterprise and New Towns (Scotland) Act 1990 — Scottish Enterprise statutory functions. AI must operate within statutory powers and Scottish Government direction.",
            "UK State-aid / WTO subsidy boundary — Cross-border effects analysis is a legal determination. AI flags risk; legally-qualified officials decide.",
            "Data Protection Act 2018 — Confidential company financial data, trade secrets, and commercial-in-confidence material. AI must enforce need-to-know access and retention limits.",
            "Freedom of Information (Scotland) Act 2002 — Public-interest and commercial-harm exemptions. AI must support, not pre-empt, FOI determinations.",
            "Climate Change (Scotland) Act 2009 + Fair Work conditionality — Net-zero and fair-work duties. AI must not optimise purely for economic return against statutory net-zero and Fair Work First objectives."
        ],
        "legislation": "Enterprise and New Towns (Scotland) Act 1990 / Subsidy Control Act 2022 / Scotland Act 1998 / DPA 2018 / FOI (Scotland) Act 2002 / Equality Act 2010 / Climate Change (Scotland) Act 2009 / Economic Crime and Corporate Transparency Act 2023"
    },
    {
        "slug": "defoneos-scottish-biometrics-commissioner-oversight-ai-deep-dive-pack",
        "title": "Scottish Biometrics Commissioner — Oversight AI Deep-Dive Pack",
        "agency": "Office of the Scottish Biometrics Commissioner",
        "agency_url": "https://www.biometricscommissioner.scot/",
        "domain": "Biometrics Oversight & Data Protection",
        "desc": "The Scottish Biometrics Commissioner is an independent statutory office providing oversight of biometric data and technologies in Scottish policing and criminal justice, established under the Scottish Biometrics Commissioner Act 2020. This deep-dive pack maps 12 entry points for AI governance, 8 transformation priorities, 6 MCP servers, and 6 non-negotiable red lines anchored in the statutory Code of Practice and human rights law.",
        "entry_points": [
            ("Statutory Code of Practice Oversight", "The Commissioner's Code of Practice governs acquisition, retention, use, and destruction of biometric data. AI conformance checking and code-version tracking.", "code"),
            ("Police Scotland & SPA Oversight", "Oversight of Police Scotland and Scottish Police Authority biometric data use. AI compliance dashboards and custody-fingerprint governance analytics.", "police"),
            ("Biometric Data Retention & Deletion", "Retention schedules and deletion assurance under the Criminal Procedure (Scotland) Act 1995 and DPA Part 3. AI retention-audit automation and deletion verification.", "retention"),
            ("Ethical Approval & Advisory Group", "The Scottish Biometrics Ethics Advisory Group scrutinises new biometric deployments. AI ethics-review pipeline and precedent analytics.", "ethics"),
            ("Data Protection & Human Rights Compliance", "DPA 2018 Part 3, Article 8 ECHR private-life compliance. AI privacy-impact screening and human-rights compatibility checking.", "dpr"),
            ("Children & Young Persons Safeguarding", "Biometric data of children under the Age of Criminal Responsibility (Scotland) Act 2019 and UNCRC. AI child-data safeguards and red-flag analytics.", "children"),
            ("Lawful Acquisition & Use Audit", "Audit of lawful acquisition, use, and search of biometric databases. AI audit-trail analytics and pattern-of-concern detection.", "audit"),
            ("Public Confidence & Transparency", "Public trust, transparency reporting, and community engagement. AI public-sentiment analytics and transparency-report automation.", "transparency"),
            ("Research, Innovation & Technology Watch", "Horizon-scanning for new biometric and AI technologies. AI technology-watch feeds and deployment-risk pre-assessment.", "research"),
            ("Complaints & Independent Review", "Independent review of complaints about biometric data use. AI complaint-triage analytics and outcome-consistency monitoring.", "complaints"),
            ("Inter-agency Coordination", "Coordination with UK ICO, Biometrics and Surveillance Camera Commissioner, and justice partners. AI cross-regulator briefing automation.", "interagency"),
            ("Governance & Scottish Parliament Accountability", "Accountability to Scottish Ministers and the Scottish Parliament. AI parliamentary evidence automation and annual-report analytics.", "parliament")
        ],
        "priorities": [
            "AI code-of-practice conformance checking replacing manual inspection → continuous compliance monitoring, deviation early-warning",
            "AI retention-and-deletion audit automation replacing sample checks → full-population deletion verification, schedule integrity",
            "AI ethics-review pipeline replacing paper-based submissions → faster advisory-group scrutiny, precedent-consistent outcomes",
            "AI bias-detection across biometric system outputs replacing periodic studies → continuous demographic-differential monitoring",
            "AI transparency-report automation replacing annual manual compilation → real-time public-report generation, FOI-ready outputs",
            "AI child-data safeguard analytics replacing manual redaction review → age-based flagging, UNCRC alignment checks",
            "AI technology-watch feeds replacing ad-hoc research → continuous horizon-scanning, deployment-risk pre-assessment",
            "AI parliamentary evidence automation replacing manual briefings → Committee-ready evidence packs, live oversight dashboards"
        ],
        "mcps": [
            ("defoneos-biometrics-code-mcp", "Governance", "Code-of-practice conformance checking, deviation early-warning, code-version tracking"),
            ("defoneos-biometrics-retention-mcp", "Compliance", "Retention-schedule audit, deletion verification, DPA Part 3 alignment, audit-trail analytics"),
            ("defoneos-biometrics-ethics-mcp", "Ethics", "Ethics-review pipeline, advisory-group precedent analytics, deployment-risk pre-assessment"),
            ("defoneos-biometrics-bias-mcp", "Fairness", "Demographic-differential monitoring, bias detection, protected-characteristic analytics"),
            ("defoneos-biometrics-transparency-mcp", "Transparency", "Transparency-report automation, public-sentiment analytics, FOI-ready output generation"),
            ("defoneos-biometrics-children-mcp", "Safeguarding", "Child-data safeguard analytics, age-based flagging, UNCRC alignment checks, red-flag monitoring")
        ],
        "red_lines": [
            "Scottish Biometrics Commissioner Act 2020 — Statutory Code of Practice governs all biometric data use in Scottish policing. AI must never enable, automate, or accelerate biometric deployment outside the Code.",
            "Data Protection Act 2018 Part 3 — Law-enforcement biometric processing. AI must operate within Part 3 safeguards with documented necessity and proportionality.",
            "Human Rights Act 1998 Article 8 — Private life. AI must not contribute to indiscriminate retention or disproportionate biometric data use.",
            "Age of Criminal Responsibility (Scotland) Act 2019 + UNCRC (Incorporation) (Scotland) Act 2024 — Children's biometric data carries the highest safeguards. AI must flag, never process, child data outside statutory protection.",
            "Equality Act 2010 — Biometric systems carry documented demographic-differential risk. AI must detect and surface bias; it must never tune matching thresholds to engineer differential outcomes.",
            "No mass surveillance — This pack documents oversight and red-line enforcement only. No facial-recognition deployment, no live-linking of biometric databases, no watchlist automation."
        ],
        "legislation": "Scottish Biometrics Commissioner Act 2020 / DPA 2018 Part 3 / Criminal Procedure (Scotland) Act 1995 / Police and Fire Reform (Scotland) Act 2012 / Age of Criminal Responsibility (Scotland) Act 2019 / UNCRC (Incorporation) (Scotland) Act 2024 / Human Rights Act 1998 / Equality Act 2010"
    }
]
