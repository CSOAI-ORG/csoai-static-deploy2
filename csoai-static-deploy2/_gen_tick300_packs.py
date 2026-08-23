#!/usr/bin/env python3
"""Tick 300 pack data: Invest Northern Ireland / National Highways / UK Space Agency.
All three probe-verified 0 disk + 0 sitemap hits BEFORE build (tick-265 pitfall)."""

PACK_INVESTNI = {
    "slug": "defoneos-invest-northern-ireland-economic-development-ai-deep-dive-pack",
    "title": "DEFONEOS \u00d7 Invest Northern Ireland \u2014 AI Governance for Regional Economic Development, FDI & Trade",
    "hash": "INNI-2026",
    "body_name": "Invest Northern Ireland",
    "body_acronym": "Invest NI",
    "domain_tag": "Economic Dev",
    "primary_act": "Industrial Development Act (Northern Ireland) 2002 / Northern Ireland Act 1998 / Subsidy Control Act 2022 / DPA 2018 + UK GDPR / FOIA 2000",
    "headline": "AI governance deep-dive pack for Invest Northern Ireland \u2014 the regional economic development agency established under the Industrial Development Act (Northern Ireland) 2002, responsible for attracting foreign direct investment, supporting local business growth, promoting innovation, R&D and export across Northern Ireland, operating under the Department for the Economy with unique dual market access under the Windsor Framework",
    "jurisdiction_note": "Non-departmental public body of the Department for the Economy (Northern Ireland Executive). Accountable to the Northern Ireland Assembly. Operates under the Industrial Development Act (Northern Ireland) 2002 and the Subsidy Control Act 2022 for public funding decisions.",
    "gov_url": "https://www.investni.com/",
    "entry_points": [
        ("Foreign Direct Investment Attraction", "Targeted FDI marketing and lead generation across priority sectors \u2014 fintech, cybersecurity, advanced manufacturing, life & health sciences, screen production, agri-food \u2014 including site selection support and investor aftercare"),
        ("Local Business Growth & Export", "Growth accelerator programmes, trade advisory, export documentation support and market-entry assistance for NI small and medium enterprises exporting to GB, EU and beyond"),
        ("Innovation & R&D Support", "Innovation vouchers, R&D grants, competence centres (NI Advanced Composites & Engineering Centre, NI Connected Health Innovation Centre) and Knowledge Transfer Partnerships"),
        ("Trade Missions & Global Outreach", "NI regional offices in GB, Europe, North America, Middle East and Asia-Pacific \u2014 trade mission organisation, trade-show presence and in-market representation"),
        ("Sector Development Teams", "Dedicated sector teams for Advanced Manufacturing & Engineering, Fintech & Financial Services, Cybersecurity, Life & Health Sciences, Screen & Creative Industries, Agri-Food, and Low Carbon & Net Zero"),
        ("City & Growth Deals", "Belfast Region City Deal, Derry-Londonderry & Strabane City Deal, Mid South West Growth Deal \u2014 Invest NI as delivery partner for innovation, digital and infrastructure investment programmes"),
        ("Land & Property Portfolio", "Development and management of Invest NI's investment property portfolio across NI \u2014 business parks, innovation centres and incubator space for inward investors"),
        ("Skills & Talent Attraction", "Assured Skills programme \u2014 employer-led pre-employment training for FDI expansion projects; coordination with the Department for the Economy's Skills Strategy"),
        ("Start-up & Entrepreneurship", "Co-Founders accelerator, Propel pre-accelerator, Techstart NI grants and seed equity funds \u2014 high-growth start-up pipeline development"),
        ("Access to Finance", "Growth Loan Fund, Growth Finance Fund, Co-Fund NI equity investment alongside private investors, and referral to British Business Bank programmes"),
        ("Windsor Framework Trade Operations", "Advisory support on dual market access (UK internal market + EU single market) under the Windsor Framework \u2014 customs facilitations, trusted trader schemes, UK Internal Market Scheme"),
        ("Net Zero & Business Resilience", "Resource-efficiency consultancy, green loans, energy audits and supply-chain resilience support for NI businesses transitioning to net zero")
    ],
    "priorities": [
        ("FDI Lead Generation AI", "AI-enabled lead scoring across FDI targets, predictive models for sector-trend alignment, and automated matchmaking of investor requirements to NI sites, skills base and incentives; Target: reduce FDI conversion cycle from 18 months to 12 months"),
        ("Export Intelligence Platform", "AI analysis of global trade data, tariff schedules, and market-access conditions \u2014 identifying high-potential export markets for NI products by sector; Target: 200+ NI SMEs supported with AI export-intelligence reports annually"),
        ("R&D Tax Credit Advisory Automation", "AI-assisted R&D tax credit and grant eligibility screening for NI businesses \u2014 HMRC-compliant evidence packs; Target: increase R&D claims by 15% through automated eligibility flags"),
        ("Skills-Matching Engine", "AI matching of FDI workforce requirements to NI labour-market supply, training pipeline and Assured Skills capacity \u2014 real-time skills gap analysis; Target: reduce FDI skills-shortage risk by 25%"),
        ("Subsidy Control Compliance", "AI compliance checks on grant and loan programmes against Subsidy Control Act 2022 thresholds \u2014 automated red-flag detection on market-distortion risk, cumulative aid caps and mandatory referral triggers; Target: 100% compliance audit trail"),
        ("Sector Cluster Analytics", "AI analysis of NI's priority-sector clusters \u2014 supply-chain density, skills overlap, innovation spillover \u2014 to target FDI and growth interventions; Target: 5 cluster deep-dives refreshed quarterly"),
        ("Windsor Framework Trade Compliance", "AI-assisted customs classification, dual-use goods screening, and Windsor Framework movement verification for NI-exporting businesses; Target: reduce trade-administration burden by 30%"),
        ("Economic Impact Evaluation", "AI counterfactual evaluation of Invest NI's portfolio \u2014 jobs created, GVA uplift, ROI per programme and per sector; Target: continuous programme-effectiveness measurement replacing biennial evaluation cycles")
    ],
    "mcps": [
        ("Invest NI FDI Intel MCP", "score_lead, match_site, predict_sector_trend, generate_fdi_report"),
        ("Invest NI Export Match MCP", "identify_market, analyse_tariff, rank_opportunity, generate_export_report"),
        ("Invest NI Subsidy Control MCP", "check_threshold, flag_cumulative_aid, detect_market_distortion, generate_audit_trail"),
        ("Invest NI Skills Match MCP", "match_workforce, analyse_skills_gap, forecast_training_demand, generate_skills_report"),
        ("Invest NI Cluster Analytics MCP", "map_supply_chain, measure_spillover, detect_cluster_gap, generate_cluster_dashboard"),
        ("Invest NI Windsor Trade MCP", "classify_customs_code, screen_dual_use, verify_framework_movement, generate_compliance_pack")
    ],
    "red_lines": [
        "NO automated grant or funding decisions \u2014 all public-money allocation requires NAO-auditable human sign-off (Subsidy Control Act 2022 s.12 mandatory referral to the CMA Subsidy Advice Unit for subsidies of particular interest)",
        "NO sharing of commercially-sensitive company financial data beyond statutory information-sharing gateways (Industrial Development Act (NI) 2002 s.7 information powers constrained by DPA 2018 and the common-law duty of confidence)",
        "NO automated Windsor Framework dual-market access claims without UK-qualified legal verification (dual-market claims trigger EU single-market obligations \u2014 erroneous AI advice could constitute a breach of the UK-EU Withdrawal Agreement)",
        "NO automated subsidy control determination substituting for Subsidy Advice Unit assessment (market-distortion analysis requires economic judgement beyond algorithmic capability)",
        "NO profiling of individual entrepreneurs or business owners beyond DPA 2018 Schedule 1 conditions (including no automated credit-scoring or personal-capacity assessment without explicit consent)",
        "NO cross-border data flows outside UK GDPR/EU adequacy arrangements \u2014 NI economic development data includes GB-to-NI trade flows under the Windsor Framework which attract specific data-protection obligations"
    ]
}

PACK_NH = {
    "slug": "defoneos-national-highways-strategic-road-network-ai-deep-dive-pack",
    "title": "DEFONEOS \u00d7 National Highways \u2014 AI Governance for the Strategic Road Network, Digital Roads & Asset Management",
    "hash": "NH-2026",
    "body_name": "National Highways",
    "body_acronym": "NH",
    "domain_tag": "Transport/CNI",
    "primary_act": "Infrastructure Act 2015 / Highways Act 1980 / Road Traffic Regulation Act 1984 / Traffic Management Act 2004 / DPA 2018 / Civil Contingencies Act 2004",
    "headline": "AI governance deep-dive pack for National Highways \u2014 the government-owned company responsible for operating, maintaining and improving England's 4,300-mile Strategic Road Network of motorways and major A roads, delivering the Road Investment Strategy, smart motorway technology, digital twin of the SRN and the Lower Thames Crossing, under sponsor the Department for Transport",
    "jurisdiction_note": "Government-owned company (company number 09346363) incorporated under the Companies Act 2006, operating under a licence from the Secretary of State for Transport issued under the Infrastructure Act 2015. Exercising the highway authority functions of the Secretary of State for the strategic road network in England.",
    "gov_url": "https://nationalhighways.co.uk/",
    "entry_points": [
        ("Strategic Road Network Operations", "24/7 operation of 4,300 miles of motorways and major A roads carrying four million journeys daily \u2014 7 Regional Operations Centres with National Traffic Information Service incident detection and response"),
        ("Regional Operations Centres", "7 ROCs (North West, Yorkshire & North East, West Midlands, East Midlands, East, South East, South West) \u2014 regional traffic-officer patrols, control rooms and incident-response coordination with emergency services"),
        ("Smart Motorways & Technology", "Stopped Vehicle Detection radar, variable speed limits, Red X lane-closure enforcement, queue-protection and MIDAS traffic sensors \u2014 400+ miles of smart motorway currently operating"),
        ("Road Investment Strategy Delivery", "RIS3 (2025-2030) \u00a327.4bn capital programme \u2014 enhancement schemes, major renewals, designated funds for safety, environment, innovation, and users & communities"),
        ("Major Projects", "Lower Thames Crossing (14.3-mile new road linking Kent and Essex), A303 Stonehenge (Amesbury to Berwick Down scheme), A428 Black Cat to Caxton Gibbet, M2/M20 junction improvements"),
        ("Asset Management & Maintenance", "Structures (9,000+ bridges), pavements, drainage, technology assets and geotechnical assets \u2014 condition monitoring, deterioration modelling and lifecycle planning across \u00a3130bn asset value"),
        ("Safety, Health & Wellbeing", "Zero KSIs (Killed or Seriously Injured) by 2040 target \u2014 road-safety audits, collision investigation, vulnerable-road-user protection, road-worker safety, and Home Safe and Well behavioural programme"),
        ("Digital Roads & Connected Vehicles", "Digital twin of the strategic road network, C-ITS (Cooperative Intelligent Transport Systems), connected and autonomous vehicle trials, open data feeds and third-party data services"),
        ("Environment & Net Zero", "2040 net zero construction and maintenance, 2030 net zero corporate operations \u2014 carbon-reduction plan, biodiversity net gain delivery, air quality monitoring and noise mitigation"),
        ("Severe Weather & Emergency Response", "Winter fleet operations (535 gritters), severe-weather watch, flood-resilience planning and civil contingencies response under the National Severe Weather Warning Service"),
        ("Network Planning & Consent", "Development Consent Order applications for nationally significant infrastructure projects (NSIPs) under the Planning Act 2008 \u2014 environmental impact assessment, public consultation and statutory consultation"),
        ("Supply Chain & Delivery Partners", "16 delivery integration partners, construction and maintenance supply chain under the Collaborative Delivery Framework \u2014 SME engagement, social value and modern slavery compliance")
    ],
    "priorities": [
        ("AI Traffic Prediction & Incident Detection", "AI predictive models for congestion, collision risk and incident detection using MIDAS loop data, CCTV feeds and third-party floating vehicle data; before: reactive incident response; after: AI pre-positioned traffic-officer patrols and 30-minute-early incident prediction; Target: 15% reduction in incident-related delays"),
        ("Asset Deterioration Modelling", "AI pavement, structure and technology-asset deterioration models optimising lifecycle renewal spend across \u00a3130bn asset base; before: condition-based renewal on fixed cycles; after: AI risk-based renewal prioritising safety-critical assets; Target: 8% lifecycle-cost saving"),
        ("Digital Twin Analytics", "AI analytics on the SRN digital twin \u2014 what-if scenario modelling for scheme options, climate-resilience stress-testing and operational-impact forecasting; Target: 20% reduction in scheme design-iteration cycles"),
        ("Severe Weather Response Optimization", "AI integration of Met Office forecast data, thermal-mapping sensors and historical gritting-effectiveness data \u2014 optimised gritter routing and pre-treatment scheduling; Target: 10% reduction in winter-service fleet mileage"),
        ("Roadworks Planning AI", "AI coordination of lane-closure scheduling across the SRN \u2014 minimising simultaneous restrictions on diversion routes and balancing maintenance windows against traffic demand; Target: 8% reduction in roadworks-related journey-delay minutes"),
        ("Collision Analytics & Safety", "AI analysis of STATS19 collision data, road geometry and traffic-flow patterns to identify high-risk cluster sites and countermeasure effectiveness; Target: 12% reduction in KSIs at AI-identified priority sites"),
        ("Carbon Accounting Automation", "AI cradle-to-grave carbon tracking for construction materials, fleet operations, maintenance activities and supply-chain emissions \u2014 PAS 2080:2023 compliant reporting; Target: auditable scope-1/2/3 carbon reporting at programme level"),
        ("Supply Chain Risk Analytics", "AI supply-chain mapping for the 16 delivery integration partners and tier-2 suppliers \u2014 financial-health monitoring, modern-slavery risk flags, carbon-compliance scoring and single-point-of-failure detection; Target: zero tier-1 supplier insolvency surprises")
    ],
    "mcps": [
        ("National Highways Traffic MCP", "predict_congestion, detect_incident, forecast_journey_time, recommend_diversion"),
        ("National Highways Asset MCP", "model_deterioration, prioritise_renewal, forecast_condition, generate_asset_report"),
        ("National Highways Safety MCP", "cluster_collision_risk, evaluate_countermeasure, detect_vulnerable_site, generate_safety_dashboard"),
        ("National Highways Carbon MCP", "track_carbon, model_abatement, verify_pas2080, generate_carbon_report"),
        ("National Highways Weather MCP", "integrate_met_forecast, optimise_gritting, model_flood_risk, generate_winter_plan"),
        ("National Highways Scheme MCP", "model_traffic_impact, simulate_diversion, assess_economic_benefit, generate_scheme_optioneering")
    ],
    "red_lines": [
        "NO autonomous control of traffic signals, variable-mandatory speed limits, lane-closure signals or any active traffic-management system \u2014 all operational control must remain under direct human supervision (Road Traffic Regulation Act 1984 s.14 temporary restrictions require human authorisation)",
        "NO AI-sole road-closure decisions \u2014 emergency or planned road closures require human risk assessment, police/emergency-service coordination, and statutory notification (Traffic Management Act 2004 Part 3 network management duty requires human judgement on network effects)",
        "NO personal data from ANPR, CCTV or journey-time monitoring beyond DPA 2018 Part 3 law-enforcement processing conditions \u2014 including no automated individual-vehicle tracking, no facial-recognition processing, and no journey-pattern profiling without statutory authority",
        "NO automated safety-incident determination \u2014 serious collision investigation and safety audit require human professional engineering judgement (Road Safety Audit standard GG119 requires qualified audit team leader sign-off)",
        "NO Environmental Impact Assessment determinations without human EIA sign-off \u2014 EIA Regulations 2017 require a 'competent expert' to prepare the Environmental Statement (automated generation would not satisfy the Regulations)",
        "NO strategic road network operational data transmission outside UK territorial jurisdiction \u2014 SRN traffic, asset and incident data are CNI-classified; cross-border data flows to third countries require specific Secretary of State authorisation under the National Security and Investment Act 2021"
    ]
}

PACK_UKSA = {
    "slug": "defoneos-uk-space-agency-civil-space-programme-ai-deep-dive-pack",
    "title": "DEFONEOS \u00d7 UK Space Agency \u2014 AI Governance for Civil Space, Satellite Launch, Earth Observation & Space Safety",
    "hash": "UKSA-2026",
    "body_name": "UK Space Agency",
    "body_acronym": "UKSA",
    "domain_tag": "Space/CNI",
    "primary_act": "Space Industry Act 2018 / Outer Space Act 1986 / Science and Technology Act 1965 / DPA 2018 + UK GDPR / UN Outer Space Treaty 1967 / UK Spaceflight Regulations 2021 / National Security and Investment Act 2021",
    "headline": "AI governance deep-dive pack for the UK Space Agency \u2014 the executive agency of the Department for Science, Innovation and Technology responsible for the UK's civil space programme, including satellite launch from SaxaVord and Sutherland spaceports, earth observation for climate science, satellite navigation and PNT resilience, ESA membership, space surveillance and tracking, and the National Space Innovation Programme",
    "jurisdiction_note": "Executive agency of the Department for Science, Innovation and Technology. Exercises powers under the Space Industry Act 2018 (with the Civil Aviation Authority as spaceflight regulator). Represents the UK at the European Space Agency (ESA) and the UN Committee on the Peaceful Uses of Outer Space (COPUOS).",
    "gov_url": "https://www.gov.uk/government/organisations/uk-space-agency",
    "entry_points": [
        ("National Space Strategy Delivery", "Delivery of the UK's National Space Strategy and civil space programme \u2014 \u00a31.6bn total UK space investment over five years covering earth observation, satellite communications, navigation, space science and launch"),
        ("Satellite Launch Capability", "UK sovereign launch capability from SaxaVord (Shetland) and Sutherland (Highlands) vertical spaceports, plus horizontal launch from Spaceport Cornwall \u2014 regulatory support for launch-operator licence applications under the Space Industry Act 2018"),
        ("Earth Observation & Climate", "EO programme including the TRUTHS climate-calibration mission, participation in ESA Copernicus and the UK EO Climate Information Service \u2014 satellite-derived climate data for net zero policy and environmental monitoring"),
        ("Satellite Navigation & PNT Resilience", "UK alternative to the EU Galileo programme post-Brexit \u2014 Navigation Innovation Support Programme (NISP) for resilient Position, Navigation and Timing, including quantum navigation and LEO-PNT constellations"),
        ("Space Science & Exploration", "UK participation in ESA science missions (ExoMars Rosalind Franklin rover, James Webb Space Telescope MIRI instrument, PLATO exoplanet mission), the Artemis Accords for lunar exploration and the UK Space Exploration Programme"),
        ("Space Surveillance & Tracking", "UK Space Operations Centre at RAF High Wycombe with UKSA civil SST sensors \u2014 collision-avoidance analysis, re-entry prediction, debris-catalogue maintenance and space-domain awareness for UK-licensed satellites"),
        ("Regulatory Interface with CAA", "UKSA as space-policy body working alongside the Civil Aviation Authority (spaceflight regulator under the Space Industry Act 2018) and the Health and Safety Executive (ground-safety regulator) \u2014 licence application readiness, safety-case guidance and environmental-assessment coordination"),
        ("International Partnerships", "ESA participation (UK is fourth-largest contributor), NASA bilateral cooperation (Artemis, ISS de-orbit vehicle), ISRO cooperation, AUKUS space working group, UK-Australia Space Bridge, and the International Charter on Space and Major Disasters"),
        ("National Space Innovation Programme", "NSIP grant funding for UK space SMEs and research organisations \u2014 technology development, in-orbit demonstration missions, and commercialisation pathways for UK space IP"),
        ("Space Clusters & Regional Growth", "Harwell Space Cluster (Oxfordshire \u2014 largest space cluster in Europe), Space Park Leicester, Westcott Venture Park propulsion test centre, Space Hub Sutherland, Goonhilly Earth Station \u2014 regional space-ecosystem development"),
        ("Skills & Workforce Pipeline", "Space apprenticeships, Space Placements in Industry (SPIN) scheme, ESA graduate trainee programme and UK Space Sector Skills Survey \u2014 building the 47,000-strong UK space workforce"),
        ("Debris Mitigation & Orbital Sustainability", "UK lead on UN COPUOS guidelines for long-term sustainability of outer space, UK Space Sustainability Mark (kitemark for debris-compliant missions), Space Sustainability \u00a3102m programme and active debris removal (Astroscale partnership)")
    ],
    "priorities": [
        ("Satellite Data Analytics AI", "AI analysis of EO satellite data for climate monitoring, flood prediction, crop-yield forecasting and maritime domain awareness \u2014 multi-sensor fusion across optical, SAR and hyperspectral; before: manual satellite-image interpretation; after: AI automated change detection at continental scale; Target: 50-fold increase in EO data throughput"),
        ("Launch Safety-Case Modelling", "AI-assisted debris-casualty-risk modelling, flight-termination analysis and range-safety computation for UK spaceport licence applications; before: deterministic modelling with conservative margins; after: AI probabilistic safety-case optimisation; Target: 30% reduction in licence-application preparation time"),
        ("Orbital Debris Risk Prediction", "AI conjunction-assessment and collision-avoidance analysis for the 2,000+ UK-licensed objects on orbit \u2014 debris-path prediction, manoeuvre-optimisation and re-entry-risk assessment; Target: 50% reduction in false-positive conjunction alerts"),
        ("PNT Resilience Monitoring", "AI monitoring of GNSS signal integrity, jamming/spoofing detection across UK territory and maritime exclusive economic zone \u2014 integration with the National Timing Centre; Target: real-time PNT interference mapping for CNI operators"),
        ("Space Weather Forecasting Integration", "AI integration of Met Office Space Weather Operations Centre data with satellite-operator risk management \u2014 geomagnetic-storm prediction, single-event-upset risk, and ionospheric-scintillation forecasting; Target: automated 72-hour space-weather risk advisories"),
        ("EO Data Fusion for Climate Policy", "AI fusion of multiple EO datasets (atmospheric composition, land-surface temperature, sea-level, ice-sheet mass) for UK climate-policy evidence \u2014 automated IPCC AR7 contribution analysis; Target: continuous climate-indicator reporting replacing periodic manual assessments"),
        ("Spaceport Licensing Decision Support", "AI risk-screening for UK spaceport licence applicants \u2014 environmental-impact compliance, safety-case completeness checking and public-consultation analysis; Target: pre-screen 100% of licence applications for completeness before CAA formal review"),
        ("Space Supply Chain Analytics", "AI mapping of the UK space supply chain \u2014 1,200+ space-sector organisations \u2014 including ITAR/EAR exposure, single-source dependency detection, and NSIA 2021 mandatory-notification trigger analysis; Target: automated fortnightly supply-chain risk reports")
    ],
    "mcps": [
        ("UKSA Launch Licence MCP", "screen_safety_case, model_casualty_risk, check_environmental_compliance, generate_licence_assessment"),
        ("UKSA Satellite Data MCP", "fuse_multisensor, detect_change, classify_landcover, generate_eo_report"),
        ("UKSA Debris Tracking MCP", "assess_conjunction, predict_reentry, optimise_manoeuvre, generate_collision_report"),
        ("UKSA Space Weather MCP", "model_geomagnetic_storm, predict_single_event_upset, forecast_scintillation, generate_weather_advisory"),
        ("UKSA PNT Monitor MCP", "detect_jamming, map_interference, assess_resilience, generate_pnt_report"),
        ("UKSA Supply Chain MCP", "map_space_supply_chain, detect_itar_exposure, flag_single_source, generate_supply_chain_report")
    ],
    "red_lines": [
        "NO AI-sole launch licence determination \u2014 CAA spaceflight licensing under the Space Industry Act 2018 requires human safety-case assessment, environmental-determination sign-off, and public-consultation evaluation (automated licence decisions would not satisfy the Act's regulator duty of care)",
        "NO satellite imagery processing that constitutes personal surveillance \u2014 UKSA civil EO data must not be used for individual identification, tracking of persons, or any purpose engaging Article 8 ECHR (Right to Private Life) without specific statutory authority",
        "NO PNT interference detection data sharing outside UK security gateways \u2014 GNSS jamming/spoofing data collected by UKSA PNT sensors constitutes sensitive CNI intelligence; disclosure requires National Security Vetting clearance and the data owner's explicit authorisation",
        "NO export-controlled space technology data stored or processed outside UK export-control jurisdiction \u2014 ITAR, EAR, UK Strategic Export Control Lists and the Export Control Order 2008 apply to UKSA's international programme data; extraterritorial data storage could constitute an export-control breach",
        "NO autonomous collision-avoidance manoeuvre commands for UK-licensed satellites \u2014 conjunction assessment outputs must be human-reviewed before any manoeuvre recommendation is communicated to the satellite operator (the Outer Space Act 1986 s.3 license condition requires operator control of the spacecraft at all times)",
        "NO UK international space-treaty commitments generated or communicated by AI without Foreign, Commonwealth and Development Office clearance \u2014 UN COPUOS submissions, ESA Council positions and bilateral space agreements involve diplomatic undertakings which cannot be delegated to automated systems"
    ]
}


PACKS = [PACK_INVESTNI, PACK_NH, PACK_UKSA]