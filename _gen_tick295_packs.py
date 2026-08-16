#!/usr/bin/env python3
"""Tick 295 pack data: VisitScotland / Historic Environment Scotland / Scottish Sentencing Council.
All three probe-verified 0 disk + 0 sitemap before build (tick-265 pitfall)."""

PACK_VS = {
    "slug": "defoneos-visitscotland-tourism-visitor-economy-ai-deep-dive-pack",
    "title": "DEFONEOS x VisitScotland — AI Governance for Tourism & the Visitor Economy",
    "hash": "VS-2026",
    "body_name": "VisitScotland",
    "body_acronym": "VS",
    "domain_tag": "Tourism",
    "primary_act": "Development of Tourism Act 1969 / Tourism (Overseas Promotion) (Scotland) Act 1984 / Scotland Act 1998 / DPA 2018 / UK GDPR / Equality Act 2010",
    "headline": "AI governance deep-dive pack for VisitScotland — sovereign tourism intelligence, destination marketing, and visitor economy data infrastructure for Scotland's devolved tourism framework",
    "entry_points": [
        ("Destination Marketing & Campaigns", "Global marketing campaigns for Scotland as a destination — brand strategy, media buying, content production, and market prioritisation across 20+ source markets"),
        ("Visitor Information Services", "iKnow Scotland, visitor information centres, digital itineraries, and multi-language visitor enquiry handling across all channels"),
        ("Events & Business Events", "EventScotland: major event bidding, funding, and delivery support; business events strategy; Edinburgh Festivals coordination"),
        ("Quality Assurance & Grading", "Quality Assurance scheme for accommodation (hotels, B&Bs, self-catering), visitor attractions, and food & drink — star grading and inspection"),
        ("Digital Platform & Open Data", "visitscotland.com, destination content APIs, Scotland's tourism open data, digital accessibility, and multilingual content operations"),
        ("Sustainable & Responsible Tourism", "Responsible tourism strategy, NetZero ambitions, visitor dispersal, seasonality management, and community impact monitoring"),
        ("Regional Partnerships & DMOs", "Support for destination management organisations, regional tourism strategies, route development (North Coast 500), and place-based growth"),
        ("Market Intelligence & Research", "Visitor surveys (International Passenger Survey), occupancy data, economic impact modelling, and tourism satellite accounts"),
        ("Food & Drink Tourism", "Scotland Food & Drink partnership, food tourism strategy, provenance storytelling, and culinary destination development"),
        ("Film & Screen Tourism", "Screen tourism growth — Outlander and Game of Thrones effects, set-jetting itineraries, and screen location promotion"),
        ("Accessibility & Inclusive Tourism", "Accessible tourism development, disabled visitor experiences, inclusive marketing, and Changing Places infrastructure"),
        ("Scottish Government Accountability", "Corporate plan delivery against the National Tourism Strategy (Scotland Outlook 2030), Scottish Government sponsorship, and parliamentary scrutiny")
    ],
    "priorities": [
        ("AI-Powered Destination Insights", "Real-time visitor flow analysis from anonymised mobile/booking/open data; before: annual surveys with 12-month lag; after: near-real-time destination intelligence"),
        ("Multilingual AI Content Generation", "NLP generation and curation of destination content in 20+ languages with brand-voice guardrails; before: manual translation (cost + lag); after: AI-assisted localisation with human brand review"),
        ("Personalised Itinerary Planning", "AI trip-planning engines for Scotland itineraries respecting sustainable-tourism dispersal goals; before: generic itineraries; after: personalised routes spreading visitors beyond hotspots"),
        ("Occupancy & Yield Forecasting", "ML models for accommodation occupancy, revenue, and demand forecasting for public policy and DMO planning; before: survey-based estimates; after: AI forecasts with uncertainty bands"),
        ("Event Impact Modelling", "AI economic impact assessment for major events and business events; before: manual multiplier studies (months); after: AI scenario modelling (hours)"),
        ("Sustainable Tourism Monitoring", "AI visitor-dispersal and carrying-capacity monitoring for sensitive sites (Skye, NC500); before: no systematic monitoring; after: AI pressure alerts for community protection"),
        ("Film Tourism Forecasting", "AI prediction of screen-tourism demand spikes from film/TV releases; before: reactive management; after: proactive capacity planning for screen destinations"),
        ("Accessibility Audit AI", "AI-assisted accessibility auditing of tourism businesses and itineraries; before: manual audits; after: scalable AI audit with human verification")
    ],
    "mcps": [
        ("Visitor Intelligence MCP", "track_visitor_flow, model_seasonality, forecast_occupancy, detect_overtourism_pressure"),
        ("Multilingual Content MCP", "localise_destination_content, guard_brand_voice, generate_itinerary, translate_visitor_information"),
        ("Event Impact MCP", "model_economic_impact, forecast_event_demand, assess_community_benefit, generate_event_briefing"),
        ("Sustainable Tourism MCP", "monitor_carrying_capacity, flag_dispersal_pressure, track_netzero_progress, assess_community_impact"),
        ("Quality Assurance MCP", "schedule_grading_inspection, benchmark_qa_scores, track_compliance, generate_improvement_plan"),
        ("Market Intelligence MCP", "aggregate_visitor_survey, model_source_market, track_competitor_destination, generate_market_briefing")
    ],
    "red_lines": [
        "NO AI-sole public funding decisions for events or campaigns (must require VisitScotland board / Scottish Government sponsorship approval)",
        "NO visitor personal data processed for marketing without consent (UK GDPR Articles 6-7 + PECR — cookies and direct marketing)",
        "NO AI content that misrepresents Scotland's accessibility or safety (must require brand-voice and factual accuracy review under Development of Tourism Act 1969 duties)",
        "NO AI recommendation of over-capacity destinations without sustainable-tourism dispersal guardrails (Scotland Outlook 2030 responsible-tourism commitments)",
        "NO AI profiling of visitors by protected characteristics (Equality Act 2010 — inclusive tourism obligations)",
        "NO tourism data sharing outside UK jurisdiction (DPA 2018 — all visitor intelligence processing must remain UK-sovereign)"
    ]
}

# @PACK_APPEND_POINT

PACK_HES = {
    "slug": "defoneos-historic-environment-scotland-heritage-ai-deep-dive-pack",
    "title": "DEFONEOS x Historic Environment Scotland — AI Governance for Heritage, Conservation & the Historic Environment",
    "hash": "HES-2026",
    "body_name": "Historic Environment Scotland",
    "body_acronym": "HES",
    "domain_tag": "Heritage",
    "primary_act": "Historic Environment Scotland Act 2014 / Ancient Monuments and Archaeological Areas Act 1979 / Planning (Listed Buildings and Conservation Areas) (Scotland) Act 1997 / DPA 2018 / UK GDPR",
    "headline": "AI governance deep-dive pack for Historic Environment Scotland — sovereign stewardship of Scotland's historic environment: monuments, listed buildings, battlefields, and cultural assets",
    "entry_points": [
        ("Properties in Care (336 Sites)", "Edinburgh Castle, Stirling Castle, Skara Brae, and 300+ monuments — conservation, interpretation, and visitor operations across Scotland"),
        ("Listing & Designation", "Statutory listing of buildings (47,000+), scheduled monuments (8,000+), gardens & designed landscapes, and battlefields (Inventory of Historic Battlefields)"),
        ("Scheduled Monument Consent", "Consent and conditions for works to scheduled monuments (AMAAA 1979 s.2) — archaeology protection and enforcement"),
        ("Listed Building Consent Advisory", "Statutory consultee on listed building consent applications, advice to planning authorities (P(LBCA)(S)A 1997)"),
        ("Conservation Science & Climate Risk", "Building materials science, stone conservation, climate change vulnerability mapping of the historic environment, and adaptation planning"),
        ("Archives & Collections", "Historic Environment Record (HER), Canmore database (350,000+ records), national collection of drawings and photographs"),
        ("Digital Documentation & Survey", "Laser scanning, photogrammetry, and 3D survey of monuments; digital twins of sites; Scotland's Coastal Heritage at Risk (SCHARP)"),
        ("Archaeology & Heritage Management", "National archaeological strategy, developer-funded archaeology, and the Archaeology Strategy for Scotland"),
        ("Skills & Craft Training", "Traditional building skills (masonry, lime, thatch), Engine Shed building conservation centre, and heritage apprenticeship pathways"),
        ("World Heritage", "Stewardship of Scotland's 6 World Heritage Sites (Edinburgh Old & New Towns, Heart of Neolithic Orkney, New Lanark, Antonine Wall, St Kilda, Forth Bridge)"),
        ("Interpretation & Learning", "Site interpretation, school visits, digital learning resources, and community engagement programmes"),
        ("Scottish Government Accountability", "Corporate plan, grants programmes (Historic Environment Grants), and reporting to Scottish Ministers (HES Act 2014)")
    ],
    "priorities": [
        ("AI-Assisted Condition Monitoring", "ML analysis of drone and LiDAR survey data for monument condition change detection; before: manual survey cycles (years); after: continuous AI monitoring with targeted human inspection"),
        ("Climate Risk Mapping Engine", "AI modelling of climate hazards (flooding, coastal erosion, freeze-thaw) across 300+ properties in care; before: site-by-site assessment; after: AI risk atlas with adaptation prioritisation"),
        ("Automated Listing Application Triage", "NLP triage of listing/designation requests and statutory consultations; before: manual casework queues; after: AI triage with conservation-officer decision gate"),
        ("Canmore Archive Intelligence", "AI transcription, tagging, and semantic search across 350,000+ archive records — handwritten survey notes, photographs, and drawings; before: manual cataloguing backlog; after: AI indexing with curator verification"),
        ("Digital Twin Construction", "Photogrammetric and LiDAR digital twins of high-risk monuments enabling virtual inspection and conservation planning; before: physical access required; after: remote virtual assessment"),
        ("Stone Decay Prediction", "ML models of stone decay pathways (weathering, salt crystallisation, pollution) informing conservation intervention timing; before: reactive repair; after: predictive conservation"),
        ("Visitor Experience AI", "Multilingual interpretation, AI-guided tours, and accessibility experiences across 336 properties; before: static interpretation panels; after: adaptive multilingual experiences"),
        ("Developer Archaeology Screening", "AI screening of planning applications against HER data to flag archaeology constraints early; before: late-stage discovery (delays); after: early constraint flags")
    ],
    "mcps": [
        ("Monument Condition MCP", "detect_condition_change, classify_decay_pathway, prioritise_inspection, generate_conservation_alert"),
        ("Climate Risk Atlas MCP", "model_flood_exposure, map_coastal_erosion, assess_freeze_thaw_cycle, prioritise_adaptation"),
        ("Designation Casework MCP", "triage_listing_request, screen_statutory_consultation, draft_designation_assessment, track_consent_condition"),
        ("Canmore Archive MCP", "transcribe_survey_note, tag_photograph, search_semantic_record, link_site_archive"),
        ("Digital Twin Survey MCP", "process_photogrammetry, align_lidar_scan, compare_twin_epochs, generate_site_model"),
        ("Conservation Science MCP", "model_stone_decay, simulate_salt_crystallisation, analyse_mortar_chemistry, recommend_intervention")
    ],
    "red_lines": [
        "NO AI-sole listing or designation decisions (must require HES designation team + legal sign-off per HES Act 2014 s.1 functions)",
        "NO AI modification of protected structures without scheduled monument consent gate (AMAAA 1979 s.2 — criminal offence for unauthorised works)",
        "NO AI-generated survey data used as evidence in enforcement without chartered surveyor verification (conservation-evidence integrity)",
        "NO digital twin data of heritage sites shared outside UK jurisdiction (DPA 2018 + site-security sensitivities — archaeological data must remain UK-sovereign)",
        "NO AI replication of restricted heritage assets enabling unauthorised fabrication or forgery (Cultural Property (Armed Conflicts) Act 2017 + antiquities protection)",
        "NO AI interpretation content presented without curatorial accuracy review (HES Act 2014 s.2 duty to promote understanding — accuracy over automation)"
    ]
}

# @PACK_APPEND_POINT

PACK_SSC = {
    "slug": "defoneos-scottish-sentencing-council-sentencing-ai-deep-dive-pack",
    "title": "DEFONEOS x Scottish Sentencing Council — AI Governance for Sentencing Guidelines & Judicial Decision Support",
    "hash": "SSC-2026",
    "body_name": "Scottish Sentencing Council",
    "body_acronym": "SSC",
    "domain_tag": "Justice",
    "primary_act": "Criminal Justice and Licensing (Scotland) Act 2010 Part 1 / Sentencing Act 2020 / Criminal Procedure (Scotland) Act 1995 / Judiciary and Courts (Scotland) Act 2008 / DPA 2018",
    "headline": "AI governance deep-dive pack for the Scottish Sentencing Council — sovereign sentencing guidelines, judicial decision support, and consistency analytics within Scotland's devolved justice framework",
    "entry_points": [
        ("Sentencing Guidelines Development", "Statutory guideline development for the High Court, sheriff courts, and JP courts — offences, methodology, and public consultation"),
        ("Guideline Impact Assessment", "Modelling the impact of draft guidelines on prison population, disposals, and equality outcomes before enactment"),
        ("Judicial Sentencing Information System", "Providing sentencing information to the judiciary to promote consistency across courts and sheriffs"),
        ("Public Sentencing Education", "Public understanding of sentencing: research, explanation of guidelines, and the sentencing process transparency programme"),
        ("Sentencing Research & Evidence", "Academic and empirical research on sentencing practice, effectiveness, and public perceptions"),
        ("Equality & Diversity in Sentencing", "Ensuring guidelines do not produce disproportionate outcomes — Equality Impact Assessments and demographic disparity monitoring"),
        ("Victim & Community Engagement", "Consultation with victims, community groups, and justice organisations in guideline development"),
        ("Sheriff Appeal Court Interaction", "Alignment of guideline structure with appellate sentencing jurisprudence (Sheriff Appeal Court + High Court appeal decisions)"),
        ("Data & Analytics Infrastructure", "Sentencing data collection, coding, and analysis across all Scottish courts — the empirical backbone of guidelines"),
        ("Guideline Evaluation", "Post-implementation review of guidelines — compliance rates, unintended consequences, and revision cycles"),
        ("Cross-Justice Coordination", "Coordination with Justice Analytical Services, Scottish Courts and Tribunals Service, Crown Office, and the Scottish Prison Service on guideline impact"),
        ("Scottish Parliament Accountability", "Annual reports to Scottish Parliament, judicial council coordination, and ministerial engagement (CJLS Act 2010 ss.1-22)")
    ],
    "priorities": [
        ("AI-Assisted Guideline Impact Modelling", "Microsimulation of guideline scenarios on prison population, court workloads, and equality outcomes; before: static spreadsheets with coarse estimates; after: AI microsimulation with uncertainty bands"),
        ("Sentencing Consistency Analytics", "ML analysis of sentencing outcomes across comparable cases flagging unexplained variance; before: periodic manual research; after: continuous consistency monitoring for the judiciary"),
        ("NLP Guideline Drafting Support", "AI-assisted drafting and citation checking of guidelines against case law; before: manual legal drafting (months); after: AI draft with judicial sign-off"),
        ("Equality Disparity Detection", "Statistical scanning of sentencing outcomes by protected characteristics with rigorous causal methods; before: infrequent EQIAs; after: continuous disparity surveillance with judicial oversight"),
        ("Public Understanding Portal AI", "Plain-language AI explanations of sentencing decisions and guidelines for victims and the public; before: static publications; after: interactive explainers with accuracy guardrails"),
        ("Consultation Response Analysis", "NLP clustering and synthesis of consultation responses from the public and justice organisations; before: manual thematic coding (weeks); after: AI thematic synthesis with human validation"),
        ("Judicial Sentencing Information Assistant", "Controlled search of anonymised sentencing information for the judiciary with consistency benchmarks; before: manual database queries; after: AI-assisted retrieval with judicial gate"),
        ("Guideline Evaluation Engine", "Automated post-implementation monitoring of guideline compliance and deviation patterns; before: one-off reviews; after: continuous evaluation dashboards")
    ],
    "mcps": [
        ("Guideline Impact Modelling MCP", "simulate_prison_population, model_disposal_shift, assess_equality_outcome, generate_impact_briefing"),
        ("Sentencing Consistency MCP", "benchmark_comparable_cases, flag_outcome_variance, cluster_sentencing_pattern, generate_consistency_report"),
        ("Guideline Drafting MCP", "draft_guideline_section, cite_case_law, check_statutory_power, version_guideline_text"),
        ("Equality Surveillance MCP", "scan_demographic_disparity, test_statistical_significance, generate_eqia_draft, flag_disproportionate_outcome"),
        ("Consultation Analysis MCP", "cluster_response_theme, synthesise_consultation, weight_stakeholder_view, generate_consultation_summary"),
        ("Public Explanation MCP", "explain_guideline_plain_language, generate_case_study, answer_sentencing_question, verify_legal_accuracy")
    ],
    "red_lines": [
        "NO AI-sole sentencing decisions or guidelines (must require High Court approval + judicial sign-off per CJLS Act 2010 ss.3-7)",
        "NO AI recommendation of individual sentences in live cases (judicial independence — Judiciary and Courts (Scotland) Act 2008 s.1; AI is support-only, never decision)",
        "NO AI profiling of judges or sheriffs by sentencing pattern (judicial independence — pattern analytics are aggregate-only, never per-judge scoring)",
        "NO sentencing data processed outside UK jurisdiction (DPA 2018 Part 3 — law enforcement processing; all analytics must remain UK-sovereign)",
        "NO AI equality analysis published without rigorous causal methodology and statistical-significance review (guideline legitimacy depends on method integrity)",
        "NO AI public-facing sentencing explanations without legal-accuracy verification (misleading public explanations undermine public confidence in justice)"
    ]
}

PACKS = [PACK_VS, PACK_HES, PACK_SSC]
