#!/usr/bin/env python3
"""Tick 299 pack data: Office for Clean Energy Jobs / Scottish Biometrics Commissioner / Parliamentary Digital Service.
All three probe-verified 0 disk + 0 sitemap BEFORE build (tick-265 pitfall)."""

PACK_OCEJ = {
    "slug": "defoneos-office-for-clean-energy-jobs-skills-ai-deep-dive-pack",
    "title": "DEFONEOS x Office for Clean Energy Jobs \u2014 AI Governance for Energy Workforce Planning, Skills Pipelines & Just Transition",
    "hash": "OCEJ-2026",
    "body_name": "Office for Clean Energy Jobs",
    "body_acronym": "OCEJ",
    "domain_tag": "Energy/Skills",
    "primary_act": "Great British Energy Act 2025 / Energy Act 2023 / Apprenticeships, Skills, Children and Learning Act 2009 / Equality Act 2010 / DPA 2018 + UK GDPR",
    "headline": "AI governance deep-dive pack for the Office for Clean Energy Jobs \u2014 the new statutory body established alongside Great British Energy to coordinate workforce planning, skills forecasting and just-transition delivery across offshore wind, nuclear, hydrogen, solar and retrofit sectors, ensuring the clean-energy economy delivers 500,000+ jobs by 2030 with regional equity",
    "jurisdiction_note": "UK-wide statutory office established alongside Great British Energy; accountable to the Secretary of State for Energy Security and Net Zero and the Skills Minister; coordinates with devolved administrations, the Department for Education, DWP and the Migration Advisory Committee on skills shortage occupations",
    "gov_url": "https://www.gov.uk/government/organisations/office-for-clean-energy-jobs",
    "entry_points": [
        ("Skills Forecasting & Labour Market Intelligence", "AI-driven modelling of future clean-energy skills demand by technology, region, qualification level and occupation \u2014 feeding the Department for Education's Skills and Labour Market Information system"),
        ("Apprenticeship Pipeline Coordination", "Mapping apprenticeship standards to clean-energy roles, supporting employers with levy-funded apprenticeship planning and coordination with the Institute for Apprenticeships and Technical Education"),
        ("Regional Just-Transition Planning", "Place-based workforce transition plans for industrial clusters \u2014 Grangemouth, Humber, Teesside, South Wales \u2014 coordinating retraining, relocation and social protection for workers leaving carbon-intensive sectors"),
        ("Further Education & Training Alignment", "Coordination with FE colleges, universities and private training providers on curriculum development for clean-energy occupations \u2014 wind turbine technicians, heat-pump installers, EV charging engineers"),
        ("Diversity & Inclusion in Energy", "Targeted programmes to increase representation of women, ethnic minorities and disabled workers in the clean-energy workforce from the current baseline"),
        ("STEM Pipeline for Clean Energy", "School-to-industry pathways \u2014 T-Levels, Skills Bootcamps and Higher Technical Qualifications aligned to clean-energy career routes"),
        ("Migration & Skills Shortages", "Coordinated input to the Migration Advisory Committee on clean-energy skills shortage occupations and the Skilled Worker visa route for energy-sector roles"),
        ("Offshore Wind Workforce", "Offshore wind-specific workforce planning for the 60 GW by 2030 target \u2014 97,000 jobs spanning turbine technicians, blade repair, foundation engineering and port operations"),
        ("Nuclear Workforce Pipeline", "Coordination with Great British Nuclear and the Nuclear Skills Taskforce on the 40,000-job nuclear workforce for new-build, SMRs and decommissioning"),
        ("Retrofit & Heat Workforce", "Workforce planning for the 27 million homes requiring energy-efficiency retrofit \u2014 200,000+ jobs in insulation, heat-pump installation and building-performance assessment"),
        ("Hydrogen & CCUS Skills", "Workforce development for the hydrogen production, transport and storage sector and the carbon capture, utilisation and storage clusters"),
        ("Regional Labour Market Observatories", "Regional observatories feeding real-time workforce data to local skills improvement plans and mayoral combined authorities")
    ],
    "priorities": [
        ("Skills Demand Forecasting", "AI multi-factor demand forecasting across clean-energy subsectors \u2014 wind, nuclear, hydrogen, solar, retrofit; before: static labour surveys; after: AI real-time demand models with regional granularity"),
        ("Just-Transition Impact Modelling", "AI modelling of employment displacement and replacement across industrial clusters, matching carbon-sector workers to clean-energy roles by skill proximity; before: generic transition estimates; after: AI worker-level transition pathways"),
        ("Apprenticeship Matching Platform", "AI matching of apprenticeship levy funds, employer demand and training provider capacity to optimise clean-energy apprenticeship starts; before: fragmented matching; after: AI clearing-house for clean-energy apprenticeships"),
        ("Diversity Targeting", "AI analysis of clean-energy workforce diversity gaps by region and occupation, with programme targeting recommendations; before: annual diversity reports; after: AI live diversity dashboards with intervention targeting"),
        ("FE Curriculum Gap Analysis", "AI analysis of FE provision against forecast skills demand to identify gaps where new or expanded training is needed; before: periodic curriculum reviews; after: AI continuous curriculum-demand gap analysis"),
        ("Migration Advisory Intelligence", "AI evidence packs for the Migration Advisory Committee on clean-energy skills shortage occupations \u2014 vacancy data, wage trends, training pipeline sufficiency; before: ad-hoc MAC submissions; after: AI real-time shortage intelligence"),
        ("Regional Labour Market Dashboards", "AI data fusion from HMRC RTI, ONS LFS, DWP benefit data and BEIS surveys into regional clean-energy workforce dashboards; before: fragmented data sources; after: AI unified regional observatories"),
        ("Workforce Programme Evaluation", "AI counterfactual evaluation of skills programmes \u2014 what works, what doesn't, by region and demographic; before: limited programme evaluation; after: AI continuous programme effectiveness measurement")
    ],
    "mcps": [
        ("Skills Forecasting MCP", "forecast_demand, model_scenario, identify_gap, generate_regional_forecast"),
        ("Just-Transition MCP", "model_displacement, match_skill_proximity, plan_retraining_pathway, generate_transition_plan"),
        ("Apprenticeship Clearing-House MCP", "match_levy_fund, find_training_provider, forecast_apprenticeship_demand, generate_clearing_house_report"),
        ("Diversity Analytics MCP", "measure_gap, target_intervention, track_progress, generate_diversity_dashboard"),
        ("FE Curriculum Mapper MCP", "map_provision, flag_gap, estimate_demand, generate_curriculum_report"),
        ("Regional Observatory MCP", "fuse_data_sources, monitor_indicator, detect_shift, generate_regional_dashboard")
    ],
    "red_lines": [
        "NO AI profiling of individual workers beyond DPA 2018 + UK GDPR requirements (personal employment data, skills assessment and retraining information are special-category sensitive \u2014 consent or statutory gateway required)",
        "NO automated decisions on funding allocation or programme eligibility without human sign-off (public money allocation decisions require NAO-auditable human accountability)",
        "NO algorithmic discrimination in retraining or programme access (Equality Act 2010 \u2014 protected characteristics including age, which is relevant to older workers transitioning from carbon sectors)",
        "NO exposure of commercially-sensitive employer workforce data beyond statutory information-sharing gateways (employer trust is central to workforce data-sharing arrangements)",
        "NO automated designation of skills shortage occupations for immigration purposes (MAC advice requires socio-economic judgement beyond algorithmic capability)",
        "NO data-sharing outside the statutory gateways defined for apprenticeship data, HMRC RTI data and DWP benefit data (each data source has its own statutory sharing framework)"
    ]
}

PACK_SBC = {
    "slug": "defoneos-scottish-biometrics-commissioner-police-ai-deep-dive-pack",
    "title": "DEFONEOS x Scottish Biometrics Commissioner \u2014 AI Governance for Biometric Data Oversight, Police Scotland & Criminal Justice",
    "hash": "SBC-2026",
    "body_name": "Scottish Biometrics Commissioner",
    "body_acronym": "SBC",
    "domain_tag": "Justice/Biometrics",
    "primary_act": "Scottish Biometrics Commissioner Act 2020 / Data Protection Act 2018 + UK GDPR / Police and Fire Reform (Scotland) Act 2012 / Criminal Justice (Scotland) Act 2016 / Human Rights Act 1998",
    "headline": "AI governance deep-dive pack for the Scottish Biometrics Commissioner \u2014 the independent oversight body established by the Scottish Biometrics Commissioner Act 2020 to oversee the acquisition, retention, use and destruction of biometric data for criminal justice and policing purposes in Scotland, including live facial recognition, custody imaging, fingerprint and DNA databases",
    "jurisdiction_note": "Independent office-holder established by the Scottish Biometrics Commissioner Act 2020, accountable to the Scottish Parliament; jurisdiction covers Police Scotland, the Scottish Police Authority and Scottish criminal justice bodies",
    "gov_url": "https://www.biometricscommissioner.scot/",
    "entry_points": [
        ("Code of Practice Oversight", "Statutory Code of Practice on the acquisition, retention, use and destruction of biometric data for criminal justice and policing purposes \u2014 compliance monitoring, complaints and improvement recommendations"),
        ("Live Facial Recognition Review", "Oversight of Police Scotland's use of live facial recognition and retrospective facial recognition technologies in public places \u2014 necessity, proportionality and human rights compliance"),
        ("Custody Imaging Oversight", "Monitoring of custody imaging (photographing persons in police custody) \u2014 data quality, retention schedules, deletion compliance and rights of data subjects"),
        ("DNA & Fingerprint Retention", "Oversight of the Scottish DNA Database and fingerprint database \u2014 retention periods, deletion of innocent persons' profiles and compliance with ECHR Article 8"),
        ("Biometric Data Ethics Advisory", "Advisory function to Police Scotland, the Scottish Police Authority and Scottish Ministers on ethical, legal and human rights dimensions of biometric technologies"),
        ("Children's Biometric Data", "Specific oversight and enhanced protections for biometric data of children in the criminal justice system \u2014 age-appropriate safeguards, parental consent and best-interests assessment"),
        ("Emerging Biometric Technologies", "Horizon-scanning and advisory on emerging biometrics \u2014 voice recognition, gait analysis, iris recognition, keystroke dynamics, AI behavioural analytics"),
        ("Equality & Human Rights Impact", "Assessment of biometric data use for its differential impact on protected groups \u2014 ethnicity, age, disability, and the risk of algorithmic bias in biometric matching"),
        ("Transparency & Public Reporting", "Annual reporting to the Scottish Parliament, public consultation on biometrics policy and transparency about biometric data holdings and usage"),
        ("Police Scotland Compliance Audits", "Compliance audit programme for Police Scotland custody suites, forensic services and digital evidence units \u2014 biometric data handling against the statutory Code of Practice"),
        ("International Standards Alignment", "Engagement with UK Biometrics and Surveillance Camera Commissioner, ICO and international biometrics oversight bodies on interoperability standards and human rights frameworks"),
        ("Data Breach & Complaint Investigation", "Investigation of biometric data breaches, complaints about biometric data handling, and recommendations for remedial action to Police Scotland")
    ],
    "priorities": [
        ("LFR Necessity & Proportionality Assessment", "AI-assisted structured assessment of Police Scotland's LFR deployment proposals against ECHR Article 8 necessity and proportionality tests; before: manual legal review; after: AI structured necessity framework with Commissioner review"),
        ("Custody Image Retention Compliance", "AI monitoring of custody image retention schedules and automated flagging of images held beyond statutory retention periods; before: manual sampling; after: AI continuous retention compliance monitoring"),
        ("Algorithmic Bias Audit Pipeline", "AI fairness-audit pipeline for biometric matching algorithms used by Police Scotland \u2014 ethnicity, age and gender bias testing across fingerprint, facial and DNA matching; before: ad-hoc bias testing; after: AI continuous algorithmic fairness auditing"),
        ("Emerging Tech Horizon Scanning", "AI horizon-scanning and technology assessment briefings on emerging biometric modalities \u2014 gait, voice, iris, keystroke; before: periodic horizon scans; after: AI continuous technology watch with ethical risk assessment"),
        ("DNA Database Deletion Compliance", "AI monitoring of the Scottish DNA Database for profiles that should have been deleted under statutory retention rules \u2014 innocent persons, children, non-convicted; before: periodic manual audit; after: AI continuous deletion compliance monitoring"),
        ("Complaint Triage & Pattern Detection", "AI-assisted triage of biometrics complaints to identify systemic issues across custody suites and police divisions; before: reactive complaint handling; after: AI pattern-detection for systemic improvement"),
        ("Transparency Dashboard", "AI-powered public transparency dashboard showing biometric data holdings, deletion rates, compliance metrics and complaints statistics; before: annual reports only; after: AI live transparency dashboards"),
        ("Audit Programme Risk-Targeting", "AI risk-weighting of custody suites and forensic units for compliance audit scheduling; before: calendar-driven audits; after: AI risk-targeted audit programme")
    ],
    "mcps": [
        ("LFR Assessment MCP", "assess_necessity, test_proportionality, evaluate_legal_basis, generate_rights_impact_assessment"),
        ("Retention Compliance MCP", "monitor_retention_schedule, flag_overheld_image, audit_deletion_compliance, generate_retention_report"),
        ("Algorithmic Bias MCP", "audit_fairness, test_differential_performance, flag_disparate_impact, generate_bias_report"),
        ("Horizon Scanning MCP", "scan_emerging_tech, assess_risk, map_ethical_framework, generate_technology_briefing"),
        ("DNA Deletion MCP", "audit_profile_retention, flag_deletion_required, verify_deletion, generate_database_compliance_report"),
        ("Complaints Intelligence MCP", "triage_complaint, detect_systemic_pattern, recommend_improvement, generate_complaints_report")
    ],
    "red_lines": [
        "NO AI-sole determination of ECHR necessity or proportionality (Article 8 assessments are matters of legal judgement requiring the Commissioner's independent human evaluation)",
        "NO automated deletion of biometric data without human verification (the statutory duty of deletion rests with the data controller; AI flags non-compliance but never executes deletion autonomously)",
        "NO algorithmic profiling that could identify specific individuals from biometric data without statutory gateway (the Commissioner's oversight function does not extend to operational biometric matching)",
        "NO data-sharing outside the statutory framework of the Scottish Biometrics Commissioner Act 2020 (the Commissioner's access to Police Scotland data is governed by the Act and must be purpose-limited)",
        "NO use of AI that could undermine the Commissioner's independence from Police Scotland and the Scottish Government (the Commissioner is an independent office-holder accountable to Parliament, not to the executive)",
        "NO processing of children's biometric data without enhanced safeguards beyond standard DPA 2018 requirements (the Commissioner's statutory duty on children's biometric data requires the highest standard of protection)"
    ]
}

PACK_PDS = {
    "slug": "defoneos-parliamentary-digital-service-ai-deep-dive-pack",
    "title": "DEFONEOS x Parliamentary Digital Service \u2014 AI Governance for Hansard, Digital Parliament & Select Committee Evidence",
    "hash": "PDS-2026",
    "body_name": "Parliamentary Digital Service",
    "body_acronym": "PDS",
    "domain_tag": "Parliament/Digital",
    "primary_act": "Parliamentary Papers Act 1840 / Parliamentary Privilege (pre-1689 common law + Article 9 Bill of Rights 1689) / Freedom of Information Act 2000 / Data Protection Act 2018 + UK GDPR / Constitutional Reform and Governance Act 2010",
    "headline": "AI governance deep-dive pack for the Parliamentary Digital Service \u2014 the bicameral digital team serving the House of Commons and House of Lords with AI-readiness for Hansard production, select committee evidence management, Members' enquiry handling, parliamentary broadcasting and digital public engagement, operating within the unique constitutional framework of parliamentary privilege and the sovereignty of Parliament",
    "jurisdiction_note": "Joint department of both Houses of Parliament (House of Commons and House of Lords), governed by the bicameral Administration Committee and Services Committee; bound by parliamentary privilege, not subject to FOIA for parliamentary records, and exempt from certain UK GDPR provisions where processing is for parliamentary functions under the DPA 2018 Schedule 2 exemption",
    "gov_url": "https://www.parliament.uk/business/commons/parliamentary-digital-service/",
    "entry_points": [
        ("Hansard Production & Reporting", "Official report of parliamentary proceedings \u2014 near-verbatim transcription, web publication and archiving of 150,000+ pages of proceedings per year across Commons, Lords and Westminster Hall"),
        ("Select Committee Evidence Management", "Digital submission, processing, redaction and publication of written and oral evidence to select committees \u2014 50+ committees, 10,000+ evidence submissions per year"),
        ("Members' Enquiry & Casework Systems", "Digital systems for Members of Parliament and Peers to manage constituency casework, correspondence and Parliamentary Questions"),
        ("Parliamentary Broadcasting", "Live broadcasting and archive of parliamentary proceedings \u2014 Parliamentlive.tv, archive digitisation and multimedia content delivery"),
        ("Digital Public Engagement", "Digital platforms for public engagement with Parliament \u2014 petitions website, committees digital engagement, outreach and education tools"),
        ("Parliamentary Archives Digitisation", "Digitisation and digital preservation of the Parliamentary Archives \u2014 8 million+ documents spanning 1497 to the present within the Parliamentary Archives' digital strategy"),
        ("Cybersecurity of Parliament", "Cyber defence of the Parliamentary network, Members' devices and the parliamentary digital estate against state-sponsored and criminal cyber threats"),
        ("Members' Digital Services", "Digital support for 650 MPs and 800+ Peers \u2014 devices, connectivity, email, remote participation and secure communications infrastructure"),
    ("Parliamentary Data & Search", "Maintain APIs, metadata standards and semantic enrichment for parliamentary data. Operate the parliament.uk search engine and the parliamentary ontology of terms, indexing 30+ million pages of proceedings and committee publications"),
        ("Constitutional AI & Privilege", "AI deployed in a parliamentary context where parliamentary privilege precludes external judicial oversight of internal proceedings \u2014 Article 9 Bill of Rights 1689 and exclusive cognisance"),
        ("Election & Ceremonial Digital", "Digital services for general elections (650 new MPs onboarded in 6 weeks), State Opening of Parliament, address-in-reply debates and other constitutional ceremonies"),
        ("Inter-Parliamentary Digital Cooperation", "Engagement with the Inter-Parliamentary Union, the ECPRD (European Centre for Parliamentary Research and Documentation) and other parliamentary digital services on shared AI standards for legislatures")
    ],
    "priorities": [
        ("Hansard AI Transcription", "AI-assisted transcription and semantic enrichment of parliamentary proceedings with human Hansard reporter verification; before: fully manual transcription; after: AI draft with reporter sign-off maintaining near-verbatim standard"),
        ("Select Committee Evidence Triage", "AI-assisted categorisation, sensitive-content detection and routing of committee evidence submissions; before: manual triage of 10K+ submissions; after: AI pre-categorisation with committee clerk verification"),
        ("Parliamentary Search Modernisation", "AI semantic search across 30M+ parliamentary pages \u2014 Hansard, committee reports, research briefings, deposited papers; before: keyword-only search; after: AI natural-language search with citation-grounded results"),
        ("Members' Casework Assistant", "AI-assisted drafting, information retrieval and routing for constituency casework enquiries; before: manual caseworker research; after: AI research assistant with MP staff sign-off"),
        ("Cybersecurity Threat Intelligence", "AI threat detection and intelligence fusion for the parliamentary digital estate against state-sponsored cyber threats; before: signature-based detection; after: AI behavioural threat detection with NCSC coordination"),
        ("Parliamentary Archives AI", "AI-assisted metadata extraction, OCR enhancement and entity recognition for the 8M-document Parliamentary Archives digitisation programme; before: manual metadata creation; after: AI metadata enrichment with archivist verification"),
        ("Petition & Public Engagement Analytics", "AI analysis of e-petition themes, public engagement patterns and committee inquiry suggestions from public input; before: manual petition analysis; after: AI thematic analysis with committee consideration"),
        ("Privilege-Aware AI Framework", "Development of the parliamentary AI governance framework that respects Article 9 privilege and exclusive cognisance while providing safe, effective AI services; before: no AI governance framework for parliamentary context; after: privilege-aware AI governance with bicameral approval")
    ],
    "mcps": [
        ("Hansard Transcription MCP", "transcribe_proceedings, enrich_semantics, assign_speaker, generate_hansard_draft"),
        ("Evidence Triage MCP", "categorise_submission, detect_sensitive_content, route_to_committee, generate_evidence_bundle"),
        ("Parliamentary Search MCP", "semantic_search, cite_authority, retrieve_proceeding, generate_search_briefing"),
        ("Casework Assistant MCP", "research_enquiry, draft_response, retrieve_guidance, generate_casework_brief"),
        ("Cyber Threat MCP", "detect_threat, fuse_intelligence, monitor_estate, generate_threat_report"),
        ("Archives Digitisation MCP", "extract_metadata, enhance_ocr, recognise_entity, generate_archival_record")
    ],
    "red_lines": [
        "NO AI processing that could breach Article 9 Bill of Rights 1689 or the principle of exclusive cognisance (parliamentary proceedings cannot be impeached or questioned in any court; AI must respect the unique constitutional boundary of Parliament's internal jurisdiction)",
        "NO AI summarisation or alteration of Hansard near-verbatim content without human reporter sign-off (the official record is constitutionally significant and must be human-verified for accuracy and context; AI drafts only, never publishes autonomously)",
        "NO AI processing of constituent personal data in Members' casework beyond the parliamentary processing exemption (DPA 2018 Schedule 2 \u2014 constituent data processed for Members' parliamentary functions is exempt from certain GDPR provisions but must still meet the DPA 2018 data protection principles)",
        "NO AI-sole decisions on evidence redaction, publication or non-publication (decisions on evidence handling are matters for committee chairs and clerks exercising parliamentary judgement)",
        "NO external AI models processing unredacted parliamentary proceedings without bicameral governance approval (parliamentary data sovereignty \u2014 external model access requires explicit bicameral governance, not operational IT decisions)",
        "NO AI that could undermine the Clerk of the House's or Clerk of the Parliaments' constitutional independence as principal constitutional advisers (AI supports but never substitutes for the Clerks' constitutional functions)"
    ]
}

PACKS = [PACK_OCEJ, PACK_SBC, PACK_PDS]