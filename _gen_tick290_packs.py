#!/usr/bin/env python3
"""Tick 290 pack data: Creative Scotland, South of Scotland Enterprise, Scottish Parliament Corporate Body."""
PACKS = [
    {
        "slug": "defoneos-creative-scotland-arts-culture-creative-industries-ai-deep-dive-pack",
        "title": "Creative Scotland — Arts, Culture, and Creative Industries AI Deep-Dive Governance Pack",
        "desc": "12-entry-point AI governance framework for Creative Scotland — the public body that supports Scotland's arts, screen, and creative industries — covering funding distribution, screen sector development, cultural venues, place partnerships, creative learning, international promotion, equalities, data, and Parliamentary accountability.",
        "agency": "Creative Scotland",
        "agency_url": "https://www.creativescotland.com/",
        "domain": "Devolved Scottish Public Body — Arts, Culture & Creative Industries",
        "legislation": "Public Services Reform (Scotland) Act 2010, National Lottery etc. Act 1993, Scotland Act 1998 s.89, Equality Act 2010, FOI (Scotland) Act 2002, DPA 2018 + UK GDPR, Scottish Ministerial Directions on Public Bodies, Creative Scotland Act 2025 (Bill)",
        "entry_points": [
            ("Regular Funding Portfolio", "Multi-year funding to 121 arts organisations — AI governance across funding allocation, outcomes measurement, and compliance monitoring.", "funding"),
            ("National Lottery Distribution", "Distribution of National Lottery funds for arts, screen, and creative projects — AI-optimised grant assessment while maintaining the additionality principle.", "lottery"),
            ("Screen Scotland", "Scotland's screen sector development unit — AI governance for film/TV production incentives, location scouting, crew databases, and IP exploitation.", "screen"),
            ("Creative Industries Development", "Support for games, design, publishing, music, and digital content — AI governance for IP protection, fair remuneration, and market access.", "industries"),
            ("Place-Based Partnerships", "Cultural regeneration and place-making across Scotland — AI governance for community engagement, environmental impact, and equitable distribution.", "place"),
            ("Creative Learning & Young People", "Youth arts, education partnerships, and talent pipelines — AI governance for safeguarding, data protection, and equitable access.", "learning"),
            ("International Strategy", "Export support, international festivals, and cultural diplomacy — AI governance for cross-border data flows, sanctions compliance, and IP protection.", "international"),
            ("Equalities, Diversity & Inclusion", "EDI duty across all funding and programmes — AI governance for bias detection, inclusive procurement, and protected characteristics monitoring.", "equalities"),
            ("Research, Data & Evidence", "Sector intelligence, economic impact analysis, and audience data — AI governance for data ethics, anonymisation, and open data publication.", "data"),
            ("Capital & Venues Investment", "Capital grants for cultural infrastructure — AI governance for procurement compliance, sustainability assessment, and whole-life costing.", "capital"),
            ("Climate & Environmental Action", "Net-zero alignment across the cultural sector — AI governance for carbon accounting, sustainable touring, and green procurement.", "climate"),
            ("Scottish Parliament Accountability", "Annual report, ministerial directions, and Public Audit Committee scrutiny — AI governance for transparency, audit trails, and FOI compliance.", "accountability")
        ],
        "priorities": [
            "AI-assisted grant assessment with explainable scoring, bias detection, and human-in-the-loop decision gates — reducing cycle time from 16 weeks to 6 weeks",
            "Screen Scotland production pipeline optimisation — AI-moderated crew database, location intelligence, and co-production treaty compliance automation",
            "Audience data platform with privacy-first analytics — federated learning across venues without centralising personal data, aligned to GDPR/DPA 2018",
            "EDI monitoring automation — real-time protected characteristics analysis across funding portfolio with automated pay-gap and representation dashboards",
            "Creative IP rights management — AI-assisted rights clearance, royalty tracking, and fair-remuneration enforcement across digital platforms",
            "Climate impact measurement — embedded carbon tracking for funded organisations with AI-optimised green-touring and venue-energy recommendations",
            "Place-based cultural investment modelling — AI-driven spatial analysis of cultural provision against SIMD deprivation indices to target underserved communities",
            "International cultural export pipeline — AI-moderated market intelligence, sanctions screening, and bilateral co-production compliance routing"
        ],
        "mcps": [
            ("creativescotland-grants-mcp", "Grant & Funding", "Explainable AI grant assessment with bias detection, additionality verification, and outcomes tracking across 121 funded organisations."),
            ("screen-scotland-production-mcp", "Screen & Production", "Film/TV production pipeline governance — crew accreditation, location intelligence, co-production treaty compliance, and IP rights management."),
            ("creative-audience-data-mcp", "Audience & Data", "Privacy-first audience analytics via federated learning — venue benchmarking, demographic mapping, and DPA 2018 compliance across the cultural sector."),
            ("creative-place-equity-mcp", "Place & Equity", "Spatial analysis of cultural provision, SIMD-aligned funding targeting, EDI monitoring, and community-engagement impact measurement."),
            ("creative-climate-culture-mcp", "Climate & Sustainability", "Embedded carbon tracking for arts organisations, green-touring optimisation, and net-zero venue transition roadmaps."),
            ("creative-export-compliance-mcp", "Export & Compliance", "International cultural export governance — sanctions screening, bilateral treaty routing, cross-border data flow compliance, and IP exploitation monitoring.")
        ],
        "red_lines": [
            "No AI sole-decision on grant awards — all funding determinations must include human-in-the-loop review per Scottish Public Finance Manual and Ministerial Directions (Public Services Reform (Scotland) Act 2010).",
            "No processing of special-category data (artistic content preferences, political expression through art) without explicit consent and DPA 2018 Schedule 1 Part 1 conditions.",
            "No automated restrictions on artistic expression — AI governance frameworks must respect Article 10 ECHR (freedom of expression) as incorporated by the Human Rights Act 1998 and Scotland Act 1998 s.29.",
            "No cross-border data transfer of cultural audience data without UK adequacy assessment and ICO-compliant transfer mechanisms under UK GDPR Articles 44-49.",
            "No National Lottery distribution decisions delegated to AI — lottery additionality principle requires human judgment per National Lottery etc. Act 1993 s.25 and Creative Scotland Directions.",
            "No AI profiling of children and young people under 18 in creative learning programmes — enhanced protections per Age of Criminal Responsibility (Scotland) Act 2019 and UNCRC (Incorporation) (Scotland) Act 2024."
        ]
    },
    {
        "slug": "defoneos-south-of-scotland-enterprise-economic-development-ai-deep-dive-pack",
        "title": "South of Scotland Enterprise — Economic Development and Community Wealth-Building AI Deep-Dive Governance Pack",
        "desc": "12-entry-point AI governance framework for South of Scotland Enterprise (SOSE) — the economic development agency for Dumfries & Galloway and the Scottish Borders — covering business growth, community wealth-building, net-zero transition, skills, land, tourism, natural capital, and Parliamentary accountability.",
        "agency": "South of Scotland Enterprise",
        "agency_url": "https://www.southofscotlandenterprise.com/",
        "domain": "Devolved Scottish Public Body — Regional Economic Development",
        "legislation": "South of Scotland Enterprise Act 2019, Enterprise and New Towns (Scotland) Act 1990 (as amended), Community Empowerment (Scotland) Act 2015, Land Reform (Scotland) Act 2016, Climate Change (Scotland) Act 2009, Equality Act 2010, FOI (Scotland) Act 2002, DPA 2018 + UK GDPR",
        "entry_points": [
            ("Business Growth & Innovation", "Grants, loans, and advisory for SMEs and social enterprises across the South of Scotland — AI governance for fair-credit assessment, fraud detection, and impact measurement.", "business"),
            ("Community Wealth-Building", "Community-led economic development, community ownership, and local procurement — AI governance for participatory budgeting, community benefit clauses, and democratic accountability.", "community"),
            ("Net-Zero Transition", "Green jobs, renewable energy, and just transition planning — AI governance for carbon accounting, supply-chain decarbonisation, and transition-risk modelling.", "netzero"),
            ("Skills & Employability", "Workforce development, apprenticeship pipelines, and digital skills — AI governance for skills-gap analysis, fair-access algorithms, and qualification-matching.", "skills"),
            ("Land & Assets", "Strategic land acquisition, development sites, and property portfolio — AI governance for Land Register integration, compulsory-purchase safeguards, and community right-to-buy compliance.", "land"),
            ("Tourism & Visitor Economy", "Destination development, visitor data, and seasonal-economy resilience — AI governance for visitor-impact modelling, privacy-compliant footfall analytics, and carrying-capacity assessment.", "tourism"),
            ("Natural Capital & Environment", "Ecosystem services, peatland restoration, and biodiversity net-gain — AI governance for natural-capital accounting, satellite monitoring, and environmental-impact assessment.", "nature"),
            ("Digital & Connectivity", "Rural broadband, 5G, and digital inclusion — AI governance for digital-poverty mapping, infrastructure ROI modelling, and equitable-access prioritisation.", "digital"),
            ("Social Enterprise & Third Sector", "Support for social enterprises, cooperatives, and community interest companies — AI governance for social-impact measurement, fair-work compliance, and charitable-status verification.", "social"),
            ("Investment & Finance", "Equity investment, loan funds, and blended finance — AI governance for investment-committee decision support, portfolio-risk modelling, and Subsidy Control Act 2022 compliance.", "investment"),
            ("Policy, Research & Intelligence", "Regional economic data, labour-market analysis, and policy evaluation — AI governance for data ethics, open-data publication, and statistical-disclosure control.", "policy"),
            ("Scottish Parliament Accountability", "Annual report, ministerial directions, and Public Audit Committee scrutiny — AI governance for transparency, audit trails, and statutory-report automation.", "accountability")
        ],
        "priorities": [
            "AI-assisted business-grant assessment with fair-credit modelling and fraud detection — reducing SME application-to-decision time from 12 weeks to 4 weeks",
            "Community wealth-building platform — AI-moderated participatory budgeting, community-benefit tracking, and local-supply-chain multiplier analysis",
            "Natural-capital accounting engine — satellite-based ecosystem-services valuation with AI-driven biodiversity net-gain monitoring and peatland-carbon verification",
            "Rural skills-matching system — AI-powered gap analysis linking employer demand to training provision across Dumfries & Galloway and Scottish Borders",
            "Land-asset intelligence platform — AI integration with Registers of Scotland, compulsory-purchase compliance automation, and community right-to-buy notification workflows",
            "Tourism carrying-capacity model — AI-driven visitor-footfall prediction, environmental-impact assessment, and seasonal-economy resilience planning",
            "Just-transition workforce modelling — AI forecasting of green-job creation against fossil-fuel job displacement with retraining-pathway optimisation",
            "Digital-poverty mapping and connectivity ROI — AI-driven spatial analysis of broadband deprivation against infrastructure investment scenarios"
        ],
        "mcps": [
            ("sose-business-growth-mcp", "Business & Investment", "AI-assisted business grant and loan assessment with fair-credit modelling, fraud detection, and Subsidy Control Act 2022 compliance verification."),
            ("sose-community-wealth-mcp", "Community & Place", "Participatory budgeting support, community-benefit clause tracking, local procurement multiplier analysis, and Community Empowerment Act compliance."),
            ("sose-natural-capital-mcp", "Natural Capital", "Satellite-based ecosystem-services valuation, peatland-carbon verification, biodiversity net-gain monitoring, and natural-capital accounting automation."),
            ("sose-land-asset-mcp", "Land & Property", "Land Register integration, compulsory-purchase compliance, community right-to-buy notification, and strategic-development-site intelligence."),
            ("sose-tourism-economy-mcp", "Tourism & Visitor Economy", "Visitor-footfall prediction, carrying-capacity modelling, privacy-compliant analytics, and seasonal-economy resilience assessment."),
            ("sose-skills-workforce-mcp", "Skills & Employability", "Skills-gap analysis, fair-access algorithms, apprenticeship-pathway optimisation, and just-transition workforce modelling.")
        ],
        "red_lines": [
            "No AI sole-decision on compulsory-purchase orders or land acquisition — all land-transaction determinations require human-in-the-loop review per Land Reform (Scotland) Act 2016 and SOSE Act 2019 s.9.",
            "No automated refusal of community right-to-buy applications — community-ownership rights under the Community Empowerment (Scotland) Act 2015 and Land Reform (Scotland) Act 2016 are protected statutory entitlements.",
            "No processing of personal financial data (SME loan applications, credit assessments) without explicit consent and DPA 2018 Schedule 1 conditions for automated decision-making under Article 22 UK GDPR.",
            "No AI profiling for investment decisions that could result in indirect discrimination against protected characteristics under the Equality Act 2010 — all investment-committee decisions require equality-impact assessment.",
            "No automated Subsidy Control Act 2022 determinations — all subsidy decisions must include human verification of market-impact assessment and Competition & Markets Authority referral triggers.",
            "No AI-driven natural-capital valuation that substitutes for statutory Environmental Impact Assessment (EIA) or Strategic Environmental Assessment (SEA) — AI outputs are inputs to, not replacements for, statutory assessment processes."
        ]
    },
    {
        "slug": "defoneos-scottish-parliament-corporate-body-governance-administration-ai-deep-dive-pack",
        "title": "Scottish Parliament Corporate Body — Parliamentary Governance and Administration AI Deep-Dive Governance Pack",
        "desc": "12-entry-point AI governance framework for the Scottish Parliament Corporate Body (SPCB) — the body responsible for the Scottish Parliament's staff, property, security, and resources — covering parliamentary services, digital transformation, security, procurement, data governance, broadcasting, and public accountability.",
        "agency": "Scottish Parliament Corporate Body",
        "agency_url": "https://www.parliament.scot/",
        "domain": "Devolved Scottish Parliamentary Body — Governance, Administration & Security",
        "legislation": "Scotland Act 1998 ss.21-22 sch.2, Scottish Parliamentary Corporate Body (Crown Status) Order 1999, Public Finance and Accountability (Scotland) Act 2000, FOI (Scotland) Act 2002, Official Secrets Act 1989, Equality Act 2010, Procurement Reform (Scotland) Act 2014, DPA 2018 + UK GDPR, Scottish Parliament (Assistance for Political Parties) Act 2021",
        "entry_points": [
            ("Parliamentary Services & Clerking", "Support for MSPs, committees, and chamber business — AI governance for legislative drafting assistance, amendment tracking, and procedural-advice automation.", "clerk"),
            ("Digital Transformation & ICT", "Parliamentary network, systems, and digital services — AI governance for privileged-communications security, network segmentation, and supply-chain assurance.", "digital"),
            ("Parliamentary Security", "Physical security, cyber defence, and personnel vetting — AI governance for threat detection, access-control systems, and SC/DV clearance management.", "security"),
            ("Procurement & Commercial", "Public procurement for parliamentary goods and services — AI governance for tender evaluation, fraud detection, and Procurement Reform (Scotland) Act 2014 compliance.", "procurement"),
            ("Human Resources & Workforce", "Parliamentary staff employment, diversity, and wellbeing — AI governance for fair-recruitment algorithms, pay-gap analysis, and employee-data protection.", "hr"),
            ("Finance & Audit", "Scottish Parliament budget, accounts, and audit — AI governance for financial-control automation, fraud-risk assessment, and Public Audit Committee reporting.", "finance"),
            ("Property, Facilities & Estates", "Holyrood building, constituency offices, and parliamentary estate — AI governance for building-management systems, energy optimisation, and physical-access logging.", "estates"),
            ("Data Governance & Information Management", "Parliamentary records, MSP correspondence, and official data — AI governance for records retention, classification, and FOI (Scotland) Act 2002 compliance.", "data"),
            ("Broadcasting, Media & Public Engagement", "Parliamentary broadcasting, webcasting, and public information — AI governance for content moderation, accessibility, and disinformation detection.", "media"),
            ("Official Report & Publications", "Official Report (Hansard), legislation, and committee reports — AI governance for transcription accuracy, metadata integrity, and authenticated-publication workflows.", "publications"),
            ("Legal Services", "Parliamentary legal advice, legislative competence, and litigation — AI governance for legal-research assistance, privilege protection, and ECHR compliance verification.", "legal"),
            ("Public Accountability & Governance", "SPCB governance, audit committee, and public accountability — AI governance for board-decision support, conflict-of-interest detection, and Nolan Principles compliance.", "governance")
        ],
        "priorities": [
            "AI-assisted legislative drafting with automated amendment-tracking, competence-verification against the Scotland Act 1998, and procedural-rule compliance checking",
            "Parliamentary cybersecurity transformation — AI-driven threat detection, privileged-communications segmentation, and supply-chain risk assessment aligned to NCSC CAF",
            "Smart-procurement platform with AI tender evaluation, Subsidy Control Act compliance, and automated fraud-risk scoring — reducing procurement cycle from 18 weeks to 8 weeks",
            "Data-governance automation — AI classification of parliamentary records, automated FOI (Scotland) Act response drafting, and retention-schedule enforcement",
            "Accessible broadcasting and webcasting — AI-real-time transcription, BSL interpretation routing, and content-moderation against disinformation",
            "Workforce-analytics platform — AI-driven pay-gap analysis, diversity-monitoring dashboards, and fair-recruitment algorithm auditing",
            "Holyrood estate smart-building optimisation — AI energy management, occupancy analytics, and physical-access anomaly detection",
            "Official Report automation — AI transcription verification, metadata enrichment, and authenticated-publication workflows with digital-signature chaining"
        ],
        "mcps": [
            ("spcb-legislative-drafting-mcp", "Legislative & Committee", "AI-assisted legislative drafting, amendment tracking, competence verification, and procedural-rule compliance — anchored to Scotland Act 1998 and Standing Orders."),
            ("spcb-parliamentary-security-mcp", "Parliamentary Security", "Threat detection, privileged-communications segmentation, personnel-vetting management, and NCSC CAF-aligned cyber defence for parliamentary networks."),
            ("spcb-procurement-mcp", "Procurement & Commercial", "AI tender evaluation, fraud detection, Subsidy Control Act compliance, and Procurement Reform (Scotland) Act 2014 statutory-report automation."),
            ("spcb-data-governance-mcp", "Data & Records", "Parliamentary record classification, FOI (Scotland) Act 2002 response automation, retention-schedule enforcement, and data-protection impact assessment."),
            ("spcb-broadcasting-accessibility-mcp", "Broadcasting & Media", "Real-time transcription, BSL interpretation routing, content moderation, disinformation detection, and webcasting-accessibility compliance."),
            ("spcb-finance-audit-governance-mcp", "Finance, Audit & Governance", "Financial-control automation, fraud-risk assessment, Public Audit Committee reporting, and Nolan Principles compliance monitoring for SPCB governance.")
        ],
        "red_lines": [
            "No AI processing of MSP privileged communications — parliamentary privilege is absolute under Scotland Act 1998 s.41 and Article 9 of the Bill of Rights 1689; no AI system may access, process, or analyse privileged material without explicit SPCB resolution.",
            "No AI-driven access to parliamentary security systems (CCTV, access control, personnel vetting data) without human authorisation and SC/DV clearance — Official Secrets Act 1989 and SPCB Security Directions apply.",
            "No automated decisions on FOI (Scotland) Act 2002 responses — all FOI determinations require human assessment of public-interest tests, exemptions, and prejudice tests per the Scottish Information Commissioner's guidance.",
            "No AI transcription of committee proceedings that substitutes for the Official Report's human-verified process — AI may assist but final Official Report text must be human-authenticated per SPCB publishing standards.",
            "No AI-driven procurement decisions without human verification of conflict-of-interest declarations, equalities impact, and Sustainability Duty compliance under Procurement Reform (Scotland) Act 2014.",
            "No AI processing of MSP casework data (constituent personal data) without explicit consent and DPA 2018 Schedule 1 Part 2 conditions — MSPs are data controllers for casework; SPCB systems must maintain data-controller separation."
        ]
    }
]