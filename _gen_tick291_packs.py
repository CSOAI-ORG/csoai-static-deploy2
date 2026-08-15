#!/usr/bin/env python3
"""Tick 291 pack data: Scottish Commission on Social Security, sportscotland,
Scottish Legal Complaints Commission. All three probe-verified (tick-265):
0 disk hits + 0 sitemap hits BEFORE build. SCSS != Social Security Scotland
(agency pack exists; the Commission is the separate scrutiny body).
sportscotland != sport-grounds-safety-authority / Transport Scotland.
SLCC != Law Society of Scotland / Faculty of Advocates (separate oversight body)."""
PACKS = [
    {
        "slug": "defoneos-scottish-commission-on-social-security-scrutiny-ai-deep-dive-pack",
        "title": "Scottish Commission on Social Security — Scrutiny, Charter & Standards AI Deep-Dive Governance Pack",
        "desc": "12-entry-point AI governance framework for the Scottish Commission on Social Security (SCSS) — the independent scrutiny body for Scotland's devolved social security system — covering charter measurement, disability assistance oversight, carer support, low-income benefits, delivery review, ministerial advice, Parliamentary reporting, and lived-experience engagement.",
        "agency": "Scottish Commission on Social Security",
        "agency_url": "https://www.socialsecuritycommission.scot/",
        "domain": "Devolved Scottish Public Body — Social Security Scrutiny & Standards",
        "legislation": "Social Security (Scotland) Act 2018 ss.21-24, Social Security Administration and Tribunal Membership (Scotland) Act 2020, Scotland Act 1998, Equality Act 2010, FOI (Scotland) Act 2002, DPA 2018 + UK GDPR, UNCRC (Incorporation) (Scotland) Act 2024, Scottish Public Finance Manual",
        "entry_points": [
            ("System Scrutiny & Review", "Independent scrutiny of the Scottish Government's social security system as a whole — AI governance for evidence gathering, analysis and the Commission's formal scrutiny reports.", "scrutiny"),
            ("Charter Measurement & Compliance", "Measurement of delivery against the Scottish social security charter principles of dignity, fairness and respect — AI-assisted compliance dashboards with human-verified findings.", "charter"),
            ("Disability Assistance Oversight", "Scrutiny of Adult Disability Payment and Child Disability Payment administration — AI governance for award-trend analysis, bias detection and outcome monitoring.", "disability"),
            ("Carer Support & Assistance", "Oversight of Carer Support Payment and Carer's Allowance Supplement — AI governance for carer-experience data, uptake analysis and delivery-failure early warning.", "carers"),
            ("Low-Income Benefits Oversight", "Scrutiny of Scottish Child Payment, Best Start Grants and Funeral Support Payment — AI governance for poverty-reduction impact measurement and take-up modelling.", "lowincome"),
            ("Social Security Scotland Delivery Review", "Independent review of Social Security Scotland agency performance — AI governance for complaint-data analysis, processing-time trends and client-experience metrics.", "delivery"),
            ("Ministerial Advice & Formal Reports", "Formal advice to Scottish Ministers on social security policy and delivery — AI governance for evidence synthesis, citation integrity and audit trails on advice dossiers.", "advice"),
            ("Scottish Parliament Accountability", "Annual reports and committee evidence to the Scottish Parliament — AI governance for transparency reporting, FOI (Scotland) Act compliance and statistical disclosure control.", "parliament"),
            ("Research & Evidence Programme", "Commissioned research and evidence reviews on devolved social security — AI governance for research ethics, peer-review integrity and open-data publication.", "research"),
            ("Lived-Experience & Stakeholder Engagement", "Expert advisory groups, disability organisations and claimant panels — AI governance for consent management, anonymisation and inclusive engagement design.", "stakeholder"),
            ("Data Protection & Case Records", "Handling of claimant-derived data and case records in scrutiny work — AI governance for anonymisation, DPA 2018 compliance and information-sharing controls per s.87 of the 2018 Act.", "privacy"),
            ("Governance & Board Accountability", "Commission board governance, financial stewardship and Nolan Principles — AI governance for board-decision support, conflict-of-interest detection and audit compliance.", "governance")
        ],
        "priorities": [
            "AI-assisted charter-compliance measurement — automated mapping of delivery data against the social security charter's dignity, fairness and respect principles with human-verified findings",
            "Evidence synthesis for scrutiny reports — structured assembly of case-review findings, research evidence and stakeholder submissions into decision dossiers for Commission members",
            "Benefit delivery monitoring — predictive analytics on processing times, redetermination rates and appeal flows across devolved benefits for early-warning reporting",
            "Lived-experience insight mining — NLP analysis of panel and engagement transcripts with strict consent management and de-identification before analysis",
            "Automated Parliamentary reporting — dashboards on Social Security Scotland delivery performance with statistical disclosure control built in",
            "Disability assistance outcome tracking — trend analysis of Adult Disability Payment and Child Disability Payment award decisions for differential-outcome detection",
            "Fraud-and-error monitoring without surveillance — aggregate statistical anomaly detection on benefit flows, never individual-level tracking of claimants",
            "Early-warning risk radar — detection of emerging delivery failures, take-up gaps and charter breaches across the devolved benefits portfolio"
        ],
        "mcps": [
            ("scss-charter-measurement-mcp", "Charter & Standards", "Continuous measurement of delivery against the Scottish social security charter — dignity, fairness and respect indicators with human-verified compliance findings."),
            ("scss-benefit-scrutiny-mcp", "Benefit Scrutiny", "Monitoring of disability, carer and low-income benefit delivery — processing-time trends, redetermination rates and appeal-flow analytics."),
            ("scss-evidence-synthesis-mcp", "Evidence & Research", "Assembly of case-review findings, commissioned research and lived-experience evidence into citation-integrity-checked scrutiny dossiers."),
            ("scss-parliament-reporting-mcp", "Parliament & Accountability", "Automated transparency reporting to the Scottish Parliament and Scottish Ministers with audit trails and statistical disclosure control."),
            ("scss-data-protection-mcp", "Data & Privacy", "Claimant-data anonymisation, DPA 2018 compliance, consent management and s.87 information-sharing control enforcement."),
            ("scss-risk-radar-mcp", "Risk & Early Warning", "Aggregate-level anomaly detection for delivery failures, take-up gaps and charter breaches — no individual-level surveillance by design.")
        ],
        "red_lines": [
            "No AI sole-determination of scrutiny findings — all scrutiny conclusions must be human-made per Social Security (Scotland) Act 2018 ss.21-24; AI outputs are evidence inputs only.",
            "No processing of individual claimant data without anonymisation and lawful basis — special-category health data requires explicit consent and DPA 2018 Schedule 1 conditions.",
            "No surveillance of claimants — aggregate statistical analysis only; no individual-level tracking, monitoring or profiling of benefit recipients, ever.",
            "No automated decisions affecting benefit entitlement or charter determinations — the charter's dignity, fairness and respect principles require human judgment.",
            "No AI profiling of children — Scottish Child Payment and Best Start-related scrutiny data is subject to UNCRC (Incorporation) (Scotland) Act 2024 protections.",
            "No publication of identifying case data — confidentiality and information-sharing restrictions under Social Security (Scotland) Act 2018 s.87 apply to all scrutiny outputs."
        ]
    },
    {
        "slug": "defoneos-sportscotland-sport-physical-activity-ai-deep-dive-pack",
        "title": "sportscotland — Sport, Physical Activity & High Performance AI Deep-Dive Governance Pack",
        "desc": "12-entry-point AI governance framework for sportscotland — the national agency for sport in Scotland — covering National Lottery funding distribution, the sportscotland Institute of Sport, national sports centres, community sport hubs, Active Schools, coaching, safeguarding, inclusion, facility planning, major events, and Scottish Government accountability.",
        "agency": "sportscotland",
        "agency_url": "https://sportscotland.org.uk/",
        "domain": "Devolved Scottish Public Body — Sport, Physical Activity & High Performance",
        "legislation": "National Lottery etc. Act 1993, Public Services Reform (Scotland) Act 2010, Scotland Act 1998, Equality Act 2010, Protection of Vulnerable Groups (Scotland) Act 2007, FOI (Scotland) Act 2002, DPA 2018 + UK GDPR, UNCRC (Incorporation) (Scotland) Act 2024",
        "entry_points": [
            ("National Lottery Funding Distribution", "Distribution of National Lottery and Scottish Government funds to sport — AI governance for equitable allocation, outcomes tracking and the lottery additionality principle.", "funding"),
            ("sportscotland Institute of Sport", "High-performance support for Scotland's athletes — AI governance for performance-data ethics, injury-prevention analytics and health-data protection.", "performance"),
            ("National Sports Centres", "National Centre Inverclyde, Glenmore Lodge and Cumbrae operations — AI governance for facility management, occupancy analytics and energy optimisation.", "centres"),
            ("Community Sport Hubs", "Support for 200+ community sport hubs across Scotland — AI governance for participation data, local-demand modelling and volunteer coordination.", "community"),
            ("Active Schools Programme", "School sport and physical activity delivery — AI governance for safeguarding workflows, child-data protection and PVG verification.", "schools"),
            ("Coaching & Volunteering", "Coach education, qualifications and volunteer workforce — AI governance for credential verification, safeguarding screening and workforce analytics.", "coaching"),
            ("Facility Investment & Planning", "Sports facility fund, design guidance and capital investment — AI governance for spatial demand modelling, lifecycle costing and procurement compliance.", "facilities"),
            ("Equality, Diversity & Inclusion in Sport", "Inclusion programmes across gender, disability, ethnicity and deprivation — AI governance for bias detection, protected-characteristics monitoring and accessible-sport measurement.", "equality"),
            ("Safeguarding in Sport", "Child wellbeing and protection across Scottish sport — AI governance for incident-reporting workflows, PVG-gated access and red-flag triage with human review.", "safeguarding"),
            ("Health & Physical Activity", "Active Scotland strategy alignment and physical-activity promotion — AI governance for population-health analytics and anonymised activity data.", "health"),
            ("Major Events & Performance Pathway", "Event hosting, athlete pathways and performance development — AI governance for event-readiness modelling, selection fairness and legacy measurement.", "events"),
            ("Governance & Scottish Government Accountability", "Public body governance, ministerial reporting and audit — AI governance for board-decision support, transparency and statutory-report automation.", "governance")
        ],
        "priorities": [
            "AI-assisted funding assessment with equitable-distribution modelling — reducing application-to-decision time while preserving National Lottery additionality and human sign-off",
            "Performance-data governance for Institute of Sport athletes — injury-prevention analytics and training-load optimisation with explicit-consent health-data protection",
            "Safeguarding workflow automation — PVG verification, consent management and incident-report routing with mandatory human review on every red-flag triage",
            "Participation analytics from anonymised facility usage — federation across venues without centralising personal data, aligned to DPA 2018 + UK GDPR",
            "Inclusion monitoring across protected characteristics — automated representation analysis and accessible-sport dashboards under the Equality Act 2010",
            "Facility planning intelligence — AI-driven spatial demand modelling of sports provision against SIMD deprivation indices for investment targeting",
            "Major-event readiness and legacy measurement — AI-moderated event logistics, environmental-impact tracking and post-event legacy assessment",
            "Coach education and pathway analytics — AI-assisted qualification mapping, safeguarding-screen status tracking and workforce-gap forecasting"
        ],
        "mcps": [
            ("sportscotland-funding-mcp", "Funding & Lottery", "Equitable funding distribution assessment, outcomes tracking and National Lottery additionality verification across the Scottish sporting estate."),
            ("sportscotland-performance-mcp", "High Performance", "Athlete performance-data governance — injury-prevention analytics, training-load optimisation and special-category health-data protection."),
            ("sportscotland-safeguarding-mcp", "Safeguarding & PVG", "PVG verification workflows, consent management, incident-report routing and red-flag triage with mandatory human review."),
            ("sportscotland-participation-mcp", "Participation & Inclusion", "Anonymised participation analytics, EDI monitoring and accessible-sport dashboards aligned to Equality Act 2010 duties."),
            ("sportscotland-facilities-mcp", "Facilities & Planning", "Spatial demand modelling, facility lifecycle costing and SIMD-aligned investment targeting for sports infrastructure."),
            ("sportscotland-events-mcp", "Events & Legacy", "Major-event readiness modelling, logistics governance, environmental-impact tracking and post-event legacy measurement.")
        ],
        "red_lines": [
            "No AI processing of children's data without explicit consent and PVG-gated access — UNCRC (Incorporation) (Scotland) Act 2024 and Protection of Vulnerable Groups (Scotland) Act 2007 apply to all youth-sport data.",
            "No athlete health-data analytics without explicit consent — UK GDPR Article 9 special-category data requires a Schedule 1 DPA 2018 condition and athlete-informed agreement.",
            "No automated funding decisions — National Lottery distribution decisions require human judgment per the additionality principle under the National Lottery etc. Act 1993.",
            "No surveillance of participants or athletes — aggregate statistical analysis only; no individual-level tracking of people in sport.",
            "No AI decisions affecting athlete selection or deselection — selection determinations are human-made to protect fairness and Equality Act 2010 rights.",
            "No AI-sourced safeguarding determinations without human review — every safeguarding red flag requires human assessment by a trained safeguarding officer."
        ]
    },
    {
        "slug": "defoneos-scottish-legal-complaints-commission-legal-services-ai-deep-dive-pack",
        "title": "Scottish Legal Complaints Commission — Legal Services Complaints & Oversight AI Deep-Dive Governance Pack",
        "desc": "12-entry-point AI governance framework for the Scottish Legal Complaints Commission (SLCC) — the independent body for complaints about legal practitioners in Scotland — covering complaint intake and triage, mediation, determinations and remedies, profession-wide complaint data, regulatory interface with the Law Society of Scotland and Faculty of Advocates, consumer education, transparency reporting, and Parliamentary accountability.",
        "agency": "Scottish Legal Complaints Commission",
        "agency_url": "https://www.scottishlegalcomplaints.org.uk/",
        "domain": "Devolved Scottish Public Body — Legal Services Complaints & Oversight",
        "legislation": "Legal Profession and Legal Aid (Scotland) Act 2007, Solicitors (Scotland) Act 1980, Legal Services (Scotland) Act 2010, Regulation of Legal Services (Scotland) Bill 2023, FOI (Scotland) Act 2002, DPA 2018 + UK GDPR, Equality Act 2010",
        "entry_points": [
            ("Complaint Intake & Eligibility", "Receipt of complaints about legal practitioners — AI governance for eligibility assessment, statutory time-limit checks and explainable triage routing.", "intake"),
            ("Service Complaints Handling", "Investigation of service complaints against solicitors and advocates — AI governance for case management, evidence organisation and consistent procedure.", "service"),
            ("Conduct Complaints Referral", "Referral of conduct complaints to the Law Society of Scotland and Faculty of Advocates — AI governance for classification accuracy and referral-integrity tracking.", "conduct"),
            ("Mediation & Resolution", "Consensual resolution and mediation between complainants and practitioners — AI governance for scheduling, outcome tracking and neutrality assurance.", "mediation"),
            ("Determinations & Remedies", "Formal determinations with remedies including compensation up to £20,000 and fee reductions — AI governance for remedy-band consistency and fairness auditing, human-determined only.", "determinations"),
            ("Profession-Wide Complaint Data", "Complaint statistics across solicitors, advocates and commercial attorneys — AI governance for trend analytics, regulatory intelligence and data publication.", "data"),
            ("Regulatory Interface", "Coordination with the Law Society of Scotland, Faculty of Advocates and Scottish Legal Aid Board — AI governance for secure information exchange and boundary enforcement.", "interface"),
            ("Consumer Education & Prevention", "Guidance for consumers of legal services — AI governance for accessible information, complaint-pathway clarity and prevention-focused analytics.", "consumer"),
            ("Transparency & Annual Reporting", "Annual reports, levy transparency and complaint-trend publication — AI governance for statistical disclosure control and public-information integrity.", "transparency"),
            ("Research & Regulatory Reform Advice", "Evidence input to legal-services regulation reform, including the Regulation of Legal Services (Scotland) Bill — AI governance for research integrity and policy-advice citation.", "research"),
            ("Data Protection, Confidentiality & Privilege", "Handling of client-matter files, legal privilege and confidential practitioner data — AI governance for privilege-safe processing and DPA 2018 compliance.", "privilege"),
            ("Governance & Scottish Parliament Accountability", "SLCC board governance, levy administration and Parliamentary accountability — AI governance for board-decision support and audit compliance.", "governance")
        ],
        "priorities": [
            "AI-assisted complaint triage with explainable routing — eligibility and statutory time-limit checks that reduce intake errors while keeping every determination human-made",
            "Casework analytics across complaint types — trend detection over multi-year complaint data for profession-wide insight without practitioner profiling",
            "Mediation scheduling and outcome tracking — AI-optimised mediation logistics with neutrality assurance and consent-gated participant data",
            "Determination drafting support — AI-assisted drafting with mandatory human sign-off on every finding and remedy, aligned to LPALA 2007",
            "Regulatory intelligence for reform advice — pattern detection across anonymised complaint data feeding the Regulation of Legal Services (Scotland) Bill evidence base",
            "Transparency dashboards for consumers — public complaint-trend dashboards with statistical disclosure control and accessible-language design",
            "Legal-privilege-safe document processing — automated privilege detection and redaction workflows with human verification on every redaction decision",
            "Fairness auditing of case outcomes — automated consistency analysis of remedy bands across comparable cases to detect differential outcomes"
        ],
        "mcps": [
            ("slcc-complaint-intake-mcp", "Intake & Triage", "Eligibility assessment, statutory time-limit checks and explainable routing of complaints against Scottish legal practitioners."),
            ("slcc-casework-management-mcp", "Casework", "Case tracking, evidence organisation, mediation logistics and determinations workflow with mandatory human sign-off at every decision gate."),
            ("slcc-profession-intel-mcp", "Profession Intelligence", "Anonymised complaint-trend analytics across solicitors, advocates and commercial attorneys — no practitioner profiling by design."),
            ("slcc-remedies-audit-mcp", "Remedies & Fairness", "Remedy-band consistency analysis, differential-outcome detection and fairness auditing across comparable complaint cases."),
            ("slcc-privilege-guard-mcp", "Privilege & Confidentiality", "Legal-privilege detection and redaction workflows with human verification — protecting client-matter confidentiality under LPALA 2007."),
            ("slcc-consumer-transparency-mcp", "Transparency & Education", "Public complaint-trend dashboards, consumer guidance and annual-report automation with statistical disclosure control.")
        ],
        "red_lines": [
            "No AI access to legally privileged material without explicit waiver — legal professional privilege is absolute; AI processing of privileged client-matter content is prohibited by design.",
            "No AI sole-determination of complaints — all determinations, findings and remedies are human-made per Legal Profession and Legal Aid (Scotland) Act 2007 s.2; AI is drafting support only.",
            "No automated decisions on complaint eligibility or statutory time limits without human review — fairness to complainants and practitioners requires human verification.",
            "No processing of special-category data in complaint files (health, sexual orientation, trade-union membership) without a DPA 2018 Schedule 1 condition and explicit consent.",
            "No AI publication of practitioner-identifying complaint data — all public transparency outputs are statistically disclosive-controlled and anonymised per the Commission's publication policy.",
            "No automated compensation awards or remedy determinations — remedies including compensation and fee reductions are human-determined in every case."
        ]
    }
]
