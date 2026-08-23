#!/usr/bin/env python3
"""Tick 298 pack data: Great British Energy / Building Safety Regulator / UK Visas & Immigration.
All three probe-verified 0 disk + 0 sitemap before build (tick-265 pitfall)."""

PACK_GBE = {
    "slug": "defoneos-great-british-energy-clean-power-ai-deep-dive-pack",
    "title": "DEFONEOS x Great British Energy \u2014 AI Governance for Publicly-Owned Clean Power, Offshore Wind & Community Energy",
    "hash": "GBE-2026",
    "body_name": "Great British Energy",
    "body_acronym": "GBE",
    "domain_tag": "Energy/PublicOwnership",
    "primary_act": "Great British Energy Act 2025 / Energy Act 2023 / Climate Change Act 2008 / Electricity Act 1989 / Nuclear Installations Act 1965 / DPA 2018 + UK GDPR",
    "headline": "AI governance deep-dive pack for Great British Energy \u2014 the publicly-owned clean energy company established by the Great British Energy Act 2025 with \u00a38.3bn capitalisation, headquartered in Aberdeen, partnering with the Crown Estate on offshore wind and driving local power plans, community energy and clean-energy supply chains",
    "jurisdiction_note": "publicly-owned company created by statute, accountable to the Secretary of State for Energy Security and Net Zero and to Parliament",
    "gov_url": "https://www.gov.uk/government/organisations/great-british-energy",
    "entry_points": [
        ("Offshore Wind Development", "Partnership with the Crown Estate to de-risk and accelerate offshore wind projects, seabed leasing and early-stage development investment"),
        ("Local Power Plan", "Support for local authorities to develop community-scale clean energy projects \u2014 8 GW target through the Local Power Plan, including rooftop solar, onshore wind and community heating"),
        ("Community Energy Fund", "Funding and co-investment for community energy groups, cooperative ownership models and local renewable generation"),
        ("Nuclear & SMR Support", "Engagement with Great British Nuclear on small modular reactor deployment, siting feasibility and public investment in nuclear pathways"),
        ("Supply Chains & Ports", "Investment in ports, manufacturing and fabrication capacity to anchor the offshore wind and clean-energy supply chain in the UK"),
        ("Grid & Storage", "Coordination with the National Energy System Operator on grid connections, queue management and battery/storage co-location"),
        ("Jobs & Skills", "Office for Clean Energy Jobs partnership \u2014 skills pipelines, apprenticeships and regional employment planning for the clean-energy transition"),
        ("Investment & Co-financing", "Co-investment with private capital, UK Infrastructure Bank pathways and project finance structuring for first-of-a-kind projects"),
        ("R&D & Innovation", "Support for floating wind, green hydrogen production, tidal and emerging clean-energy technology demonstration"),
        ("Energy Bill Affordability", "Programmes linking clean-power roll-out to bill reduction for households, prioritising areas of fuel poverty"),
        ("Climate & Net Zero Delivery", "Contribution to the 2030 clean power by 2030 mission, carbon budgets under the Climate Change Act 2008 and sectoral decarbonisation pathways"),
        ("Public Accountability", "Parliamentary scrutiny, NAO value-for-money audit and annual reporting on \u00a38.3bn public capital deployment")
    ],
    "priorities": [
        ("Offshore Wind Portfolio Modelling", "AI scenario modelling across the offshore wind pipeline \u2014 cost curves, wind yield, seabed constraints and auction outcomes; before: spreadsheet-driven estimates; after: AI portfolio optimisation with analyst validation"),
        ("Local Power Siting Intelligence", "AI screening of local-authority sites for rooftop solar, wind and heat \u2014 planning constraints, grid proximity, irradiance/wind data; before: manual site surveys; after: AI pre-screened shortlists with planner sign-off"),
        ("Community Fund Application Triage", "AI-assisted completeness and eligibility checks for community energy funding applications; before: slow manual review; after: AI first-pass with human award decisions"),
        ("Grid Connection Queue Analytics", "AI analysis of connection queue data, curtailment risk and reinforcement requirements; before: opaque queue processes; after: AI queue dashboards shared with NESO"),
        ("Supply Chain Risk Monitoring", "AI monitoring of supplier solvency, delivery risk and single-point-of-failure exposure across ports and fabrication; before: periodic audits; after: AI continuous risk radar"),
        ("Clean Energy Skills Forecasting", "ML forecasting of regional skills demand across offshore wind, nuclear and retrofit trades; before: periodic labour surveys; after: AI workforce planning feeding the Office for Clean Energy Jobs"),
        ("Affordability Impact Analysis", "AI estimation of bill impacts from new generation by region and tenure type; before: static distributional analyses; after: AI live affordability dashboards"),
        ("Public Accountability Reporting", "AI drafting and consistency-checking of NAO-grade project reporting, cost-to-completion and milestone tracking; before: manual returns; after: AI-assisted reporting with finance sign-off")
    ],
    "mcps": [
        ("Offshore Wind MCP", "model_pipeline, assess_seabed_constraints, forecast_auction_outcome, generate_investment_case"),
        ("Local Power MCP", "screen_site, estimate_yield, flag_planning_constraint, generate_council_briefing"),
        ("Community Energy MCP", "triage_application, check_eligibility, model_ownership, generate_award_pack"),
        ("Grid Analytics MCP", "analyse_connection_queue, flag_curtailment_risk, model_storage_colocation, generate_neso_briefing"),
        ("Supply Chain MCP", "monitor_supplier_risk, flag_single_point_failure, track_delivery_milestone, generate_risk_report"),
        ("Green Skills MCP", "forecast_skill_demand, match_apprenticeship, plan_regional_training, generate_workforce_report")
    ],
    "red_lines": [
        "NO autonomous grid dispatch or operational control decisions by AI (safety-critical electricity system operations remain with licensed human operators under the Electricity Act 1989 regime)",
        "NO processing of nuclear safety-case or safeguarded nuclear data outside ONR-compliant handling arrangements (Nuclear Installations Act 1965 + ONR security requirements)",
        "NO exposure of critical national infrastructure data beyond NCSC CAF-aligned protections (energy CNI designation under the NIS Regulations 2018)",
        "NO AI-sole decisions on deployment of public money (all investment decisions require human sign-off audit-ready for the NAO and the Public Accounts Committee)",
        "NO algorithmic discrimination in community fund allocation or siting decisions (Equality Act 2010 public sector equality duty \u2014 fairness audits mandatory)",
        "NO cross-border transfer of energy market or infrastructure data outside UK/EEA adequacy arrangements (DPA 2018 + UK GDPR Chapter V)"
    ]
}

PACK_BSR = {
    "slug": "defoneos-building-safety-regulator-higher-risk-buildings-ai-deep-dive-pack",
    "title": "DEFONEOS x Building Safety Regulator \u2014 AI Governance for Higher-Risk Buildings, Gateway Regimes & the Golden Thread",
    "hash": "BSR-2026",
    "body_name": "Building Safety Regulator",
    "body_acronym": "BSR",
    "domain_tag": "Safety/Regulation",
    "primary_act": "Building Safety Act 2022 / Fire Safety Act 2021 / Building Act 1984 / Health and Safety at Work etc. Act 1974 / DPA 2018 + UK GDPR",
    "headline": "AI governance deep-dive pack for the Building Safety Regulator \u2014 the HSE-hosted regulator established by the Building Safety Act 2022 to oversee higher-risk buildings through the three-gateway regime, the golden thread of information, mandatory occurrence reporting and the safety case regime for occupied buildings",
    "jurisdiction_note": "regulator established within the Health and Safety Executive under the Building Safety Act 2022 (England); accountable to the Secretary of State and Parliament",
    "gov_url": "https://www.gov.uk/government/organisations/building-safety-regulator",
    "entry_points": [
        ("Gateway One (Planning)", "Building control approval at planning stage for higher-risk buildings \u2014 fire safety strategy scrutiny before planning permission"),
        ("Gateway Two (Construction Start)", "Full plans assessment before construction begins \u2014 design and compliance approval for HRB work"),
        ("Gateway Three (Completion)", "Completion certificate applications \u2014 verification that the as-built building meets the requirements before occupation"),
        ("Safety Case Regime", "Safety case assessments and periodic reviews for occupied higher-risk buildings prepared by Accountable Persons"),
        ("Golden Thread of Information", "The digital record of a building \u2014 accurate, accessible, single-source-of-truth information held throughout a building's life"),
        ("Registered Building Inspectors", "Registration and regulation of building inspectors and building control approvers \u2014 the professionalisation of building control"),
        ("Building Control Profession", "Codes of conduct, competence frameworks and disciplinary arrangements for registered building control professionals"),
        ("Cladding & Remediation", "Remediation orders, assessment of unsafe cladding and oversight of remediation works under the Building Safety Act"),
        ("Mandatory Occurrence Reporting", "The statutory duty for occurrences relating to structural failure or fire spread that risk a significant number of lives to be reported"),
        ("Residents' Voice", "Complaints routes for residents of higher-risk buildings and engagement duties owed by Accountable Persons"),
        ("Enforcement & Prosecution", "Enforcement powers including stop notices, compliance notices and prosecution for building safety offences"),
        ("Industry Competence", "Oversight of the Building Industry Competence standards \u2014 competence requirements for the whole built-environment workforce")
    ],
    "priorities": [
        ("Safety Case Triage", "AI first-pass completeness and quality checks on safety case submissions; before: manual multi-week reviews; after: AI triage with inspector-led assessment"),
        ("Golden Thread Validation", "AI validation of golden thread information continuity across gateways \u2014 missing/contradictory information flags; before: document-by-document review; after: AI continuity checks with professional sign-off"),
        ("Occurrence Report Clustering", "AI clustering and thematic analysis of mandatory occurrence reports to surface systemic risk patterns; before: reactive incident review; after: AI early-warning risk themes"),
        ("Risk-Based Inspection Scheduling", "AI scheduling of building inspection resources weighted by safety-case risk indicators; before: calendar-driven allocation; after: AI risk-weighted inspection planning"),
        ("Remediation Progress Tracking", "AI tracking of remediation order compliance, cladding assessment backlog and completion milestones; before: spreadsheet-based tracking; after: AI live remediation dashboards"),
        ("Resident Complaint Routing", "AI routing and prioritisation of resident complaints and enquiries to the correct case team; before: manual triage queues; after: AI-assisted routing with human case handling"),
        ("Competence Records Management", "AI management of registered building inspector CPD, disciplinary and registration records; before: manual registers; after: AI-maintained professional registers"),
        ("Enforcement Intelligence", "AI analysis of building control and fire safety data to target enforcement where risk is highest; before: reactive enforcement; after: AI-informed proactive enforcement targeting")
    ],
    "mcps": [
        ("Safety Case MCP", "triage_safety_case, check_completeness, flag_residual_risk, generate_assessment_plan"),
        ("Golden Thread MCP", "validate_continuity, flag_missing_information, verify_version, generate_gateway_briefing"),
        ("Occurrence Reporting MCP", "cluster_occurrences, detect_theme, escalate_systemic_risk, generate_thematic_report"),
        ("Inspection Planner MCP", "weight_risk, schedule_inspection, allocate_resource, generate_patrol_plan"),
        ("Remediation Tracker MCP", "track_remediation_order, monitor_completion, flag_delay, generate_remediation_dashboard"),
        ("Competence Register MCP", "register_inspector, log_cpd, flag_disciplinary, generate_competence_report")
    ],
    "red_lines": [
        "NO AI sign-off of safety cases or gateway decisions (statutory decisions remain with human building inspectors and the regulator \u2014 AI assists assessment, never determines outcome)",
        "NO suppression, filtering or delay of mandatory occurrence reports by any automated process (the reporting duty is statutory and absolute)",
        "NO processing of residents' personal data beyond DPA 2018 + UK GDPR lawfulness and minimisation requirements (resident trust is central to the post-Grenfell regime)",
        "NO AI-sole enforcement or prosecution decisions (enforcement action requires human legal and regulatory judgement)",
        "NO automated conclusions about building safety without verifiable evidence trails in the golden thread (every AI output must reference source information)",
        "NO use of AI that could obscure or down-weight fire-safety risk signals (Grenfell lesson: honesty in risk data is non-negotiable \u2014 the system must fail safe, never fail quiet)"
    ]
}

PACK_UKVI = {
    "slug": "defoneos-uk-visas-immigration-casework-ai-deep-dive-pack",
    "title": "DEFONEOS x UK Visas & Immigration \u2014 AI Governance for Visa Casework, Sponsorship & Digital Borders",
    "hash": "UKVI-2026",
    "body_name": "UK Visas & Immigration",
    "body_acronym": "UKVI",
    "domain_tag": "Immigration/HomeOffice",
    "primary_act": "Immigration Act 1971 / Nationality and Borders Act 2022 / Immigration and Asylum Act 1999 / UK GDPR + DPA 2018 / Equality Act 2010",
    "headline": "AI governance deep-dive pack for UK Visas & Immigration \u2014 the Home Office directorate running the visa system, eVisa and ETA rollout, sponsor licensing and asylum casework; DEFONEOS applies human-decided-outcomes governance so AI supports caseworkers without ever replacing statutory decision-making",
    "jurisdiction_note": "Home Office directorate (UK-wide), accountable to the Home Secretary; casework decisions subject to judicial review and tribunal oversight",
    "gov_url": "https://www.gov.uk/government/organisations/uk-visas-and-immigration",
    "entry_points": [
        ("Visa Casework & Decision-Making", "Entry clearance, visit, work, study and family visa decision casework across global decision-making centres"),
        ("eVisa Rollout", "Replacement of biometric residence permits with digital immigration status (eVisas) and the View and Prove service"),
        ("Electronic Travel Authorisation", "ETA issuance for non-visa nationals \u2014 automated eligibility screening with human oversight of refusals"),
        ("Sponsor Licensing", "Sponsor Management System \u2014 licensing, compliance visits and certificate of sponsorship allocation for employers and education providers"),
        ("Asylum Casework", "Asylum claims, screening interviews and substantive casework \u2014 decision quality and safeguarding duties"),
        ("Biometrics & Identity", "Biometric enrolment, identity verification and document checking across visa application centres and digital channels"),
        ("Border Transformation", "Digital border programme \u2014 permission-to-travel integration, advance passenger data and contactless corridors"),
        ("Appeals & Administrative Review", "Tribunal bundles, administrative review of refusals and case preparation for the First-tier Tribunal (IAC)"),
        ("Nationality & Citizenship", "Naturalisation, registration and British citizenship casework with ceremony and passport coordination"),
        ("EU Settlement Scheme", "Settled and pre-settled status casework, late applications and ongoing eligibility verification"),
        ("Windrush Schemes", "Windrush Compensation Scheme and Windrush status documentation \u2014 the operational response to the Windrush Lessons Learned Review"),
        ("Public Enquiry & Contact", "Customer contact centres, MP correspondence and complaints handling across the visa lifecycle")
    ],
    "priorities": [
        ("Casework Triage & Routing", "AI routing of straightforward applications (e.g. low-risk visit visas with complete evidence) to accelerated paths; before: uniform queues; after: AI triage with human decision on every outcome"),
        ("Document Verification Support", "AI-assisted document authenticity screening and evidence completeness checks; before: manual document review; after: AI pre-screening with caseworker confirmation"),
        ("Sponsor Compliance Risk Scoring", "AI risk scoring of sponsor licence compliance signals to target compliance visits; before: random and reactive visits; after: AI-informed risk-based compliance"),
        ("Guidance Retrieval", "AI retrieval of the current Immigration Rules and policy guidance relevant to a case type; before: manual guidance search; after: AI citation-checked guidance retrieval"),
        ("Appeals Bundle Assembly", "AI assembly and pagination of tribunal bundles from case files; before: manual collation weeks; after: AI bundle generation with caseworker verification"),
        ("Language & Interpretation Matching", "AI matching of interpretation and translation needs for interviews and asylum casework; before: manual booking; after: AI-assisted matching with human delivery"),
        ("Contact Centre Assistance", "AI first-line answers on application status and process questions; before: long call queues; after: AI status assistant with human escalation"),
        ("Decision Quality Sampling", "AI-assisted sampling and review of decided cases for consistency and error patterns; before: limited manual sampling; after: AI quality dashboards feeding continuous improvement")
    ],
    "mcps": [
        ("Casework Triage MCP", "route_application, flag_missing_evidence, detect_straightforward_case, generate_triage_report"),
        ("Document Verification MCP", "screen_document, flag_authenticity_risk, check_consistency, generate_evidence_summary"),
        ("Sponsor Compliance MCP", "score_sponsor_risk, plan_compliance_visit, track_cos_allocation, generate_licence_report"),
        ("Appeals Bundle MCP", "assemble_bundle, paginate_documents, index_evidence, generate_tribunal_pack"),
        ("Guidance Retrieval MCP", "retrieve_rule, cite_authority, flag_policy_change, generate_guidance_briefing"),
        ("Enquiry Assistant MCP", "answer_status_query, route_complaint, escalate_case, generate_mp_reply_draft")
    ],
    "red_lines": [
        "NO automated grant or refusal of immigration status without human caseworker decision (Article 22 UK GDPR rights on automated decisions + the Windrush Lessons Learned Review's rejection of rigid automated outcomes)",
        "NO AI training or decisions on data retained in breach of the Windrush-era retention lessons (documentation retention and destruction schedules are mandatory)",
        "NO processing of biometric data beyond DPA 2018 Schedule 1 conditions and ICO biometric data guidance (consent, necessity and proportionality tests apply)",
        "NO algorithmic profiling on protected characteristics (Equality Act 2010 \u2014 nationality, ethnicity and religion are protected characteristics; fairness audits mandatory)",
        "NO data-sharing outside the immigration exemption boundaries in DPA 2018 Schedule 2 (the exemption is narrow and must be applied case-by-case, not by default)",
        "NO AI credibility assessments in asylum casework without human review (trauma-informed decision-making and safeguarding duties remain with human caseworkers)"
    ]
}

PACKS = [PACK_GBE, PACK_BSR, PACK_UKVI]
