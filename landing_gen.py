#!/usr/bin/env python3
"""landing_gen.py — Phase 1 of the provision-page land grab.

Generates one static HTML page per statute provision into
`<deploy>/law/<statute>/<article-slug>.html`, plus the atlas index at
`<deploy>/law/index.html`.

THE LAW (GREENFIELD_LAND_GRAB_2026-07-29): no page ships without a provision,
a citation, and a working interaction. The generator REFUSES to emit a page
whose provision text is absent or trivially short — that is the
no-provision-no-page gate, not a nicety.

Corpus: eu-ai-act-compliance-mcp/data/regulations.db (417 articles + 13
annexes across EU AI Act, GDPR, DORA, NIS2, CRA, CSRD — full text, synced
from EUR-lex). Stdlib only.

    python3 landing_gen.py                # generate everything
    python3 landing_gen.py --selftest     # corpus sanity check, no writes
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path("/Users/nicholas/clawd/mcp-marketplace/eu-ai-act-compliance-mcp/data/regulations.db")
DEPLOY_DIR = Path("/Users/nicholas/csoai-pages-deploy")
SITE_BASE = "https://www.csoai.org"
MIN_PROVISION_CHARS = 80  # below this the page is refused (the gate)

# ─── Statute metadata ─────────────────────────────────────────────────────────

STATUTES = {
    "eu-ai-act": {
        "celex": "32024R1689",
        "name": "EU AI Act",
        "prefix": "EU-AIA",
        "official": "Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence",
        "source": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689",
        "binds_default": "Providers, deployers, importers, distributors and authorised representatives of AI systems placed on the EU market or whose output is used in the EU — with some duties also reaching general-purpose AI model providers.",
        "scope_q": "Do you develop, supply, or use an AI system whose output is used in the European Union?",
        "role_q": "Is your role one the Act regulates — provider, deployer, importer, distributor, or authorised representative?",
        "blurb": "The EU's horizontal AI regulation: risk-tiered duties from prohibited practices (Art. 5) through high-risk conformity to transparency marking (Art. 50).",
    },
    "gdpr": {
        "celex": "32016R0679",
        "name": "GDPR",
        "prefix": "GDPR",
        "official": "Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data",
        "source": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679",
        "binds_default": "Controllers and processors of personal data of people in the EU/EEA, and non-EU organisations offering goods or services to, or monitoring, people in the EU.",
        "scope_q": "Do you process personal data of people in the EU/EEA — or are you established there?",
        "role_q": "Are you a controller or a processor for that processing?",
        "blurb": "The EU's data-protection backbone: lawful bases, data-subject rights, DPIAs, breach notification, and the fines regime.",
    },
    "dora": {
        "celex": "32022R2554",
        "name": "DORA",
        "prefix": "DORA",
        "official": "Regulation (EU) 2022/2554 on digital operational resilience for the financial sector",
        "source": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R2554",
        "binds_default": "EU financial entities (banks, insurers, payment and e-money institutions, investment firms, crypto-asset service providers and more) and, through oversight and contract rules, their ICT third-party service providers.",
        "scope_q": "Are you a financial entity operating in the EU, or an ICT third-party provider serving one?",
        "role_q": "Does your role fall inside DORA's Article 2 scope (financial entity or critical ICT provider)?",
        "blurb": "Digital operational resilience for finance: ICT risk management, incident reporting, resilience testing and third-party oversight.",
    },
    "nis2": {
        "celex": "32022L2555",
        "name": "NIS2 Directive",
        "prefix": "NIS2",
        "official": "Directive (EU) 2022/2555 on measures for a high common level of cybersecurity across the Union",
        "source": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2555",
        "binds_default": "Essential and important entities — medium and large organisations in 18 critical sectors (energy, transport, health, digital infrastructure, space, and more) operating in the EU.",
        "scope_q": "Do you operate in one of NIS2's 18 critical sectors in the EU (energy, transport, health, digital, and similar)?",
        "role_q": "Are you a medium or large entity in that sector, or otherwise designated as essential or important?",
        "blurb": "The EU's cybersecurity baseline for critical sectors: risk-management measures, incident reporting in 24/72 hours, and management accountability.",
    },
    "cra": {
        "celex": "32024R2847",
        "name": "Cyber Resilience Act",
        "prefix": "CRA",
        "official": "Regulation (EU) 2024/2847 on horizontal cybersecurity requirements for products with digital elements",
        "source": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R2847",
        "binds_default": "Manufacturers, importers and distributors of products with digital elements made available on the EU market — hardware and software alike.",
        "scope_q": "Do you make a product with digital elements (hardware or software) available on the EU market?",
        "role_q": "Are you the manufacturer, an importer, or a distributor of that product?",
        "blurb": "Cybersecurity by design for products with digital elements: vulnerability handling, security updates, CE marking and conformity assessment.",
    },
    "csrd": {
        "celex": "32022L2464",
        "name": "CSRD",
        "prefix": "CSRD",
        "official": "Directive (EU) 2022/2464 as regards corporate sustainability reporting",
        "source": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022L2464",
        "binds_default": "Large EU undertakings and listed SMEs above the Accounting Directive thresholds, with group-level reporting for qualifying parent undertakings.",
        "scope_q": "Are you a large EU undertaking or listed SME above the Accounting Directive size thresholds?",
        "role_q": "Are you responsible for the undertaking's management report or sustainability reporting?",
        "blurb": "Corporate sustainability reporting under the ESRS: double materiality, assurance, and machine-readable disclosure.",
    },
}

ROLE_TERMS = [
    ("provider", "providers"), ("deployer", "deployers"), ("importer", "importers"),
    ("distributor", "distributors"), ("authorised representative", "authorised representatives"),
    ("controller", "controllers"), ("processor", "processors"),
    ("data subject", "data subjects"), ("financial entit", "financial entities"),
    ("ICT third-party", "ICT third-party providers"), ("essential entit", "essential entities"),
    ("important entit", "important entities"), ("manufacturer", "manufacturers"),
    ("notified bod", "notified bodies"), ("market surveillance", "market surveillance authorities"),
    ("supervisory authorit", "supervisory authorities"), ("undertaking", "undertakings"),
    ("competent authorit", "competent authorities"), ("operator", "operators"),
]

# ─── Hand-written plain-English overrides for high-traffic provisions ─────────
# Format: (statute_slug, article_number) -> {"demands": str, "binds": str}
# Everything NOT listed here gets verbatim obligation sentences extracted from
# the provision text itself — labelled as verbatim, never paraphrased by machine.

OVERRIDES = {
    ("eu-ai-act", 2): {
        "demands": "Defines the regulation's reach: it applies to providers placing AI systems or general-purpose AI models on the EU market (wherever established), to deployers located in the EU, and to providers and deployers outside the EU whose system's output is used in the EU. Carve-outs cover military/defence, pure R&D before market placement, and personal non-professional use.",
        "binds": "Anyone in the AI value chain touching the EU market — including non-EU companies whose AI output is used in the EU.",
    },
    ("eu-ai-act", 4): {
        "demands": "Requires providers and deployers to take measures to ensure a sufficient level of AI literacy of their staff and anyone operating systems on their behalf — considering technical knowledge, experience, education, the context of use, and the people affected.",
        "binds": "Providers and deployers of AI systems, in respect of their own workforce and contractors.",
    },
    ("eu-ai-act", 5): {
        "demands": "Prohibits eight classes of AI practice outright: manipulative or deceptive techniques causing significant harm, exploitation of vulnerabilities, social scoring, certain predictive policing, untargeted facial-image scraping, emotion inference at work or school, biometric categorisation of sensitive traits, and (narrowly gated) real-time remote biometric ID in public for law enforcement.",
        "binds": "Everyone placing on the market, putting into service, or using AI in the EU — no role is exempt.",
    },
    ("eu-ai-act", 6): {
        "demands": "Sets the classification rule for high-risk AI: systems used as a safety component of (or as) a product under EU harmonisation legislation requiring third-party conformity assessment, and systems in the Annex III areas, are high-risk — unless they pose no significant risk of harm because they only perform narrow procedural tasks.",
        "binds": "Providers determining their system's tier; the classification they reach triggers the whole Chapter III duty set.",
    },
    ("eu-ai-act", 9): {
        "demands": "Requires a continuous, iterative risk-management system across the entire lifecycle of a high-risk AI system: identify and analyse known and foreseeable risks, estimate and evaluate them, adopt mitigation and control measures, and test against them.",
        "binds": "Providers of high-risk AI systems.",
    },
    ("eu-ai-act", 10): {
        "demands": "Data and data-governance duties for high-risk systems: training, validation and testing datasets must be relevant, representative, and as error-free and complete as possible for the intended purpose, with bias examination and governance practices documented.",
        "binds": "Providers of high-risk AI systems (and those who train them).",
    },
    ("eu-ai-act", 13): {
        "demands": "Transparency to deployers: high-risk systems must ship with instructions for use that let the deployer interpret output correctly — covering capabilities, limitations, accuracy, foreseeable misuse, human-oversight measures and expected lifetime.",
        "binds": "Providers of high-risk AI systems, for the benefit of deployers.",
    },
    ("eu-ai-act", 14): {
        "demands": "High-risk systems must be designed so natural persons can oversee them effectively while in use — including the ability to interpret output, detect anomalies, and intervene or interrupt the system ('stop button').",
        "binds": "Providers (by design) and deployers (in operation) of high-risk AI systems.",
    },
    ("eu-ai-act", 16): {
        "demands": "The provider duty-list for high-risk systems: ensure compliance with the Chapter III requirements, maintain a quality management system, keep documentation and logs, undergo conformity assessment, draw up the EU declaration of conformity, affix CE marking, register in the EU database, and cooperate with authorities.",
        "binds": "Providers of high-risk AI systems.",
    },
    ("eu-ai-act", 17): {
        "demands": "Requires providers of high-risk systems to run a documented quality management system covering regulatory strategy, design control, testing, data management, risk management, post-market monitoring, incident reporting and record-keeping.",
        "binds": "Providers of high-risk AI systems (SMEs may comply in a simplified way).",
    },
    ("eu-ai-act", 26): {
        "demands": "The deployer duty-list for high-risk systems: use per instructions, ensure human oversight by competent people, keep input data relevant to the intended purpose, monitor operation, retain logs under their control, inform workers before workplace use, and inform affected people that they are subject to a high-risk system.",
        "binds": "Deployers of high-risk AI systems — the organisations that actually use them.",
    },
    ("eu-ai-act", 27): {
        "demands": "Fundamental-rights impact assessment before deployment of certain high-risk systems: public-law bodies, public-service providers, and deployers of credit-scoring and insurance-pricing systems must assess and document the impact on fundamental rights — processes, period of use, affected groups, risks of harm, oversight and complaint arrangements.",
        "binds": "Deployers that are public bodies or provide public services, and deployers of Annex III 5(b)/(c) systems (creditworthiness, insurance pricing).",
    },
    ("eu-ai-act", 43): {
        "demands": "Conformity assessment for high-risk systems: Annex III systems may generally use internal control (Annex VI); systems under Annex I harmonisation legislation, and biometric identification systems where harmonised standards are not applied, require third-party assessment by a notified body (Annex VII).",
        "binds": "Providers of high-risk AI systems choosing (or forced into) a conformity route.",
    },
    ("eu-ai-act", 49): {
        "demands": "Registration: before placing a high-risk AI system on the market, providers (or representatives) must register themselves and the system in the EU database — deployers who are public bodies must also register their use.",
        "binds": "Providers of high-risk systems; public-sector deployers for the use-registration part.",
    },
    ("eu-ai-act", 50): {
        "demands": "Transparency for people exposed to AI: users must be told when they interact with an AI system; synthetic content must be machine-readably marked as artificially generated or manipulated; deepfakes and AI-generated text published on matters of public interest must be visibly labelled. This duty is already in force.",
        "binds": "Providers of AI interaction systems and synthetic-content generators; deployers of emotion-recognition, biometric-categorisation, deepfake and AI-text systems.",
    },
    ("eu-ai-act", 53): {
        "demands": "Obligations for general-purpose AI model providers: technical documentation, information to downstream providers, a copyright-compliance policy, and a public summary of training content.",
        "binds": "Providers of general-purpose AI models (open-source models get a partial carve-out).",
    },
    ("eu-ai-act", 55): {
        "demands": "Extra duties for GPAI models with systemic risk (cumulative compute above 10^25 FLOPs or designated): model evaluation including adversarial testing, systemic-risk assessment and mitigation, serious-incident tracking and reporting, and adequate cybersecurity.",
        "binds": "Providers of general-purpose AI models classified as having systemic risk.",
    },
    ("eu-ai-act", 72): {
        "demands": "Post-market monitoring: providers must plan and run a system to collect and analyse data on high-risk system performance after placement, feeding continuous compliance evaluation.",
        "binds": "Providers of high-risk AI systems.",
    },
    ("eu-ai-act", 73): {
        "demands": "Serious-incident reporting: providers must report serious incidents (death, serious harm, critical-infrastructure disruption, fundamental-rights infringement) to market surveillance authorities — within 15 days generally, 2 days for critical infrastructure, 10 days for deaths.",
        "binds": "Providers of high-risk AI systems; deployers who detect incidents must inform the provider first.",
    },
    ("eu-ai-act", 99): {
        "demands": "The penalties article: prohibited-practice breaches up to €35m or 7% of global turnover; most other operator-duty breaches up to €15m or 3%; misleading information to authorities up to €7.5m or 1%. GPAI breaches carry their own ceiling.",
        "binds": "Every operator in scope — this is the enforcement teeth.",
    },
    ("eu-ai-act", -3): {
        "demands": "The high-risk catalogue: eight areas where AI systems are high-risk under Art. 6(2) — biometrics, critical infrastructure, education, employment, essential services (incl. credit scoring), law enforcement, migration, and administration of justice and democratic processes — each with the specific use-cases listed.",
        "binds": "Providers and deployers of any system whose purpose falls in a listed point; determines who carries Chapter III duties.",
    },
    ("eu-ai-act", -4): {
        "demands": "Technical documentation: the full file a provider must compile before a high-risk system is placed on the market — system description, design specs, data requirements, risk management, validation and testing, monitoring plan — kept up to date throughout the lifecycle.",
        "binds": "Providers of high-risk AI systems (the file authorities will ask for first).",
    },
    ("eu-ai-act", -6): {
        "demands": "The internal-control conformity route: the provider verifies its own quality management system and technical documentation against the Chapter III requirements and keeps evidence available for authorities for ten years.",
        "binds": "Providers of Annex III high-risk systems using self-assessment under Art. 43(2).",
    },
    ("eu-ai-act", -7): {
        "demands": "The notified-body conformity route: application, documentation review, audit of the quality management system, examination of the technical design, and the EU-type examination certificate a notified body issues.",
        "binds": "Providers of high-risk systems on the third-party route, and the notified bodies assessing them.",
    },
    ("gdpr", 5): {
        "demands": "The processing principles: lawfulness, fairness, transparency; purpose limitation; data minimisation; accuracy; storage limitation; integrity and confidentiality; and accountability — the controller must be able to demonstrate all of them.",
        "binds": "Controllers (accountability is explicitly theirs), with processors bound through the principles' operation.",
    },
    ("gdpr", 6): {
        "demands": "The lawful-basis menu: processing is lawful only under consent, contract, legal obligation, vital interests, public task, or legitimate interests (balanced against the data subject). Public authorities may not use legitimate interests for their tasks.",
        "binds": "Controllers choosing — and documenting — a basis before processing starts.",
    },
    ("gdpr", 7): {
        "demands": "Conditions for consent: it must be demonstrable, intelligible, as easy to withdraw as to give, and freely given — a contract cannot be conditioned on unnecessary consent. The child-consent age defaults to 16 (member states may lower to 13).",
        "binds": "Controllers relying on consent as their lawful basis.",
    },
    ("gdpr", 25): {
        "demands": "Data protection by design and by default: implement appropriate technical and organisational measures from the design stage, and by default process only the data necessary for each specific purpose.",
        "binds": "Controllers; producers of processing products are encouraged to take it into account.",
    },
    ("gdpr", 30): {
        "demands": "Records of processing activities: controllers (and processors) must maintain a written record of purposes, categories of data and recipients, transfers, retention periods and security measures.",
        "binds": "Controllers and processors, subject to the under-250-employee conditional exemption.",
    },
    ("gdpr", 32): {
        "demands": "Security of processing: measures appropriate to the risk — pseudonymisation and encryption, CIA of systems, restore capability, and regular testing and evaluation of the measures.",
        "binds": "Controllers and processors alike.",
    },
    ("gdpr", 33): {
        "demands": "Breach notification: a personal-data breach must be notified to the supervisory authority within 72 hours of becoming aware unless unlikely to risk rights and freedoms — with the prescribed content, or a documented justification for delay.",
        "binds": "Controllers (processors must alert the controller without undue delay).",
    },
    ("gdpr", 35): {
        "demands": "DPIA: where processing is likely to result in high risk — systematic profiling with significant effects, large-scale special-category data, large-scale public-area monitoring — a data protection impact assessment is required before processing.",
        "binds": "Controllers; the DPO advises and the supervisory authority is consulted on residual high risk.",
    },
    ("gdpr", 37): {
        "demands": "When a Data Protection Officer is mandatory: public authorities, controllers whose core activities are large-scale regular monitoring, or large-scale processing of special-category or conviction data.",
        "binds": "Controllers and processors meeting the triggers; groups may share a DPO.",
    },
    ("gdpr", 44): {
        "demands": "International transfers: personal data may leave the EEA only under an adequacy decision or appropriate safeguards (BCRs, SCCs), with narrow derogations — this article is the gate for every third-country transfer.",
        "binds": "Controllers and processors transferring personal data outside the EEA.",
    },
    ("gdpr", 83): {
        "demands": "The fines ladder: up to €10m or 2% of global turnover for processor/controller-infrastructure breaches; up to €20m or 4% for principle, basis, rights, or transfer breaches — whichever is higher in each tier.",
        "binds": "Controllers and processors; enforcement discretion sits with supervisory authorities.",
    },
    ("dora", 6): {
        "demands": "ICT risk-management framework: financial entities must run a sound, comprehensive and well-documented ICT risk framework — strategies, policies, tools and an annual review — as part of their overall governance.",
        "binds": "Financial entities; the management body bears ultimate responsibility.",
    },
    ("dora", 8): {
        "demands": "Identification duty: on a continuous basis identify all sources of ICT risk, all information assets and ICT systems supporting critical functions, and their dependencies — updated in step with changes.",
        "binds": "Financial entities.",
    },
    ("dora", 10): {
        "demands": "Detection: mechanisms to promptly detect anomalous activities, including network performance issues and ICT incidents, with multiple layers of control and alerting.",
        "binds": "Financial entities.",
    },
    ("dora", 11): {
        "demands": "Response and recovery: comprehensive ICT business continuity and disaster recovery plans, tested and audited, with backup, restoration and recovery measures — including for critical third-party failure scenarios.",
        "binds": "Financial entities (with proportionality for smaller ones).",
    },
    ("dora", 17): {
        "demands": "ICT incident management: detect, manage and classify incidents by impact criteria; report major incidents to the competent authority (initial, intermediate, final reports) and inform clients of major incidents affecting their interests.",
        "binds": "Financial entities.",
    },
    ("dora", 19): {
        "demands": "Incident reporting content and deadlines: the harmonised reporting templates, timelines and notification flows for major ICT-related incidents to competent authorities.",
        "binds": "Financial entities; competent authorities receive and relay reports.",
    },
    ("dora", 24): {
        "demands": "Digital operational resilience testing: a risk-based testing programme for all critical ICT systems at least yearly, plus threat-led penetration testing every three years on live production systems for entities the authority designates.",
        "binds": "Financial entities; TLPT requires internal or external testers meeting the article's conditions.",
    },
    ("dora", 28): {
        "demands": "Third-party risk governance: a strategy on ICT third-party risk, a register of all contractual arrangements, pre-contract due diligence, and exit strategies — with contractual minimums for critical providers.",
        "binds": "Financial entities; critical ICT third-party providers face direct oversight under Chapter V.",
    },
    ("dora", 30): {
        "demands": "Key contractual provisions: what contracts with ICT providers must contain — service descriptions, locations, data protection, access/audit rights, service levels, incident assistance, termination and exit terms.",
        "binds": "Financial entities writing ICT contracts; ICT providers must accept them in practice.",
    },
    ("nis2", 2): {
        "demands": "Scope: which entities are in — essential and important entities by sector (Annexes I/II) and size, plus inclusions regardless of size (DNS, TLD registries, cloud, and similar) and member-state designations.",
        "binds": "Medium and large entities in the 18 listed sectors; certain digital entities regardless of size.",
    },
    ("nis2", 3): {
        "demands": "Essential vs important: the classification rule — large entities in Annex I sectors are essential; others in scope are important — which decides supervision intensity and penalty ceilings.",
        "binds": "All in-scope entities; the label determines the enforcement regime applied to them.",
    },
    ("nis2", 21): {
        "demands": "Cybersecurity risk-management measures: at minimum — risk analysis and policies, incident handling, business continuity, supply-chain security, secure acquisition/development/maintenance, effectiveness assessment, cyber hygiene and training, cryptography, access control and MFA, and basic cyber hygiene practices.",
        "binds": "Essential and important entities; management bodies approve the measures and can be held liable.",
    },
    ("nis2", 23): {
        "demands": "Incident reporting: early warning within 24 hours of becoming aware of a significant incident, incident notification within 72 hours, and a final report within one month — to CSIRT or the competent authority, and recipients must be informed of mitigations.",
        "binds": "Essential and important entities.",
    },
    ("nis2", 34): {
        "demands": "General penalty framework: member states must provide effective, proportionate, dissuasive penalties — essential entities at least €10m or 2% of worldwide turnover for risk-measure and reporting breaches; important entities at least €7m or 1.4%.",
        "binds": "Essential and important entities; management persons can be temporarily suspended.",
    },
    ("cra", 2): {
        "demands": "Scope: applies to products with digital elements made available on the market whose intended purpose or reasonably foreseeable use includes a direct or indirect logical or physical data connection to a device or network.",
        "binds": "Manufacturers, importers and distributors of connected hardware and software.",
    },
    ("cra", 6): {
        "demands": "Security by design and by default: products must be designed, developed and produced so that — given the risks — they ensure an appropriate level of cybersecurity, and be delivered with a secure by default configuration.",
        "binds": "Manufacturers of products with digital elements.",
    },
    ("cra", 13): {
        "demands": "The manufacturer duty-list: design/develop per Annex I, run vulnerability handling, keep technical documentation and the EU declaration of conformity, affix CE marking, and report actively exploited vulnerabilities within the support period (expected to be at least five years).",
        "binds": "Manufacturers of products with digital elements.",
    },
    ("cra", 14): {
        "demands": "Vulnerability and incident reporting: manufacturers must report actively exploited vulnerabilities (early warning within 24 hours, notification within 72 hours, final report within 14 days of a corrective measure) and severe incidents affecting the security of the product.",
        "binds": "Manufacturers; reports go to the designated CSIRT and ENISA via the single reporting platform.",
    },
    ("csrd", 1): {
        "demands": "The substantive article: it amends the Accounting, Transparency, Audit and Insurance Accounts Directives to require sustainability reporting under the ESRS inside the management report, with double materiality, digital tagging, and mandatory assurance (limited at first).",
        "binds": "Large undertakings and listed SMEs (as amended by later omnibus proposals); statutory auditors provide the assurance.",
    },
    ("csrd", 3): {
        "demands": "Who reports and when: extends sustainability reporting obligations to large undertakings and listed SMEs on a phased timetable, and introduces consolidated reporting and subsidiary exemptions.",
        "binds": "Undertakings crossing the Accounting Directive size thresholds and listed SMEs.",
    },
}

# ─── Text helpers ─────────────────────────────────────────────────────────────

ROMAN = {i: r for i, r in enumerate(
    ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
     "XI", "XII", "XIII"], 0)}


def split_title(content: str, is_annex: bool) -> tuple[str, str]:
    """(title, body) — the corpus stores the official title as the lead-in
    before the first numbered paragraph (' 1. ' or ' (1) ')."""
    if is_annex:
        # annexes open with a header line 'ANNEX III' then a descriptive line
        lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        if lines and re.match(r"^ANNEX\s+[IVXLCDM]+$", lines[0], re.I):
            lines = lines[1:]
        title = lines[0] if lines else "Annex"
        body = re.sub(r"\s+", " ", content).strip()
        return _clean_title(title), body
    text = re.sub(r"\s+", " ", content).strip()
    title, body = None, text
    for pat, marker in ((r"\s1\.\s", "1. "), (r"\s\(1\)\s", "(1) ")):
        m = re.split(pat, text, maxsplit=1)
        if len(m) == 2 and 3 <= len(m[0]) <= 160:
            title, body = m[0], marker + m[1]
            break
    if title is None:
        s = re.split(r"(?<=[.!?])\s", text, maxsplit=1)
        title, body = s[0], (s[1] if len(s) > 1 else "")
    # run-on titles: 'Subject matter This Regulation lays down: (a) ...' — cut at
    # the first sentence starter and give the dropped prose back to the body.
    # Pass 1: explicit prose starters. Pass 2 (only if pass 1 misses): the
    # generic 'X ... shall' pattern, which is too trigger-happy to run first.
    if len(title) > 60:
        m = re.search(
            r"\s(?=(?:This (?:Regulation|Directive)|Member States|The Commission|"
            r"The ESAs|The European|Without prejudice|By way of|In order to|"
            r"Taking into account|Where\b|For the purposes|In (?:Article|Annex)\b|"
            r"Article \d|By \d|The [A-Z]|Providers?\b|Deployers?\b|Importers?\b|"
            r"Distributors?\b|Manufacturers?\b|Controllers?\b|Processors?\b|"
            r"Financial entit|Essential entit|Important entit|Competent authorit|"
            r"Supervisory authorit|Notified bod|Undertakings\b))", title)
        if m is None:
            m = re.search(r"\s(?=[A-Z]\S*(?:\s\S+){0,3}\s(?:shall|may|must)\b)", title)
        if m and m.start() >= 3 and title[:m.start()].strip():
            body = title[m.start():].strip() + " " + body
            title = title[:m.start()]
    return _clean_title(title), body


def _clean_title(title: str) -> str:
    t = title.replace("`", "")
    t = re.sub(r"^Article\s+\d+[a-z]?\s*", "", t)
    t = re.sub(r"^[a-z]\s+(?=[A-Z])", "", t)  # corpus mojibake: 'd Irregularities'
    t = re.sub(r"\s*For the purposes of this (Regulation|Directive):?\s*$", "", t)
    t = t.split(" is amended as follows")[0]
    # collapse a duplicated instrument citation ('Directive 2013/34/EU Directive 2013/34/EU')
    t = re.sub(r"\b((?:Directive|Regulation)\s+(?:\(EU\)\s+)?\S+)\s+\1\b", r"\1", t)
    t = t.strip(" .—:`")
    if len(t) > 120:
        t = t[:117].rsplit(" ", 1)[0] + "…"
    return t or "Provision"


def obligation_sentences(body: str, limit: int = 3) -> list[str]:
    """Verbatim sentences carrying 'shall' — the duties, in the law's own words."""
    sents = re.split(r"(?<=[.;])\s+(?=[A-Z(0-9])", body)
    out = []
    for s in sents:
        if re.search(r"\bshall\b", s) and 40 <= len(s) <= 600:
            out.append(s.strip())
        if len(out) >= limit:
            break
    return out


def first_sentences(body: str, limit: int = 2, maxlen: int = 700) -> str:
    sents = re.split(r"(?<=[.;])\s+(?=[A-Z(0-9])", body)
    take, total = [], 0
    for s in sents:
        if total + len(s) > maxlen or len(take) >= limit:
            break
        take.append(s.strip())
        total += len(s)
    return " ".join(take)


def roles_mentioned(text: str) -> list[str]:
    low = text.lower()
    seen, out = set(), []
    for needle, label in ROLE_TERMS:
        if needle.lower() in low and label not in seen:
            seen.add(label)
            out.append(label)
    return out[:8]


def article_label(number: int, article_id: str) -> str:
    """'Article 27' or 'Annex III'."""
    if number > 0:
        return f"Article {number}"
    roman = article_id.replace("ANNEX", "").strip() or ROMAN[-number]
    return f"Annex {roman}"


def slug_for(number: int, article_id: str) -> str:
    if number > 0:
        return f"article-{number}"
    roman = (article_id.replace("ANNEX", "").strip() or ROMAN[-number]).lower()
    return f"annex-{roman}"


def anchor_for(prefix: str, number: int, article_id: str) -> str:
    if number > 0:
        return f"{prefix}-Art-{number}"
    roman = (article_id.replace("ANNEX", "").strip() or ROMAN[-number]).upper()
    return f"{prefix}-Annex-{roman}"


# ─── Page template ────────────────────────────────────────────────────────────

CSS = """
:root{--gold:#c9a84c;--bg:#F5F0E6;--card:#FFFCF5;--ink:#2a1a14;--dim:#7a6a58;--border:rgba(201,168,76,.28)}
*{margin:0;box-sizing:border-box}
body{font-family:'Space Grotesk',-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
.wrap{max-width:780px;margin:0 auto;padding:40px 22px 70px}
.crumb{font-size:12.5px;color:var(--dim);margin-bottom:18px}
.crumb a{color:var(--gold);text-decoration:none;font-weight:600}
.kicker{font-size:11.5px;font-weight:800;letter-spacing:.24em;color:var(--gold);margin-bottom:10px}
h1{font-size:clamp(26px,4.4vw,38px);letter-spacing:-.03em;line-height:1.1}
.lede{margin-top:12px;font-size:15.5px;color:var(--dim);line-height:1.6;max-width:640px}
.lede b{color:var(--ink)}
.anchor-chip{display:inline-block;margin-top:14px;font:700 12px/1 ui-monospace,Menlo,monospace;background:#1a1410;color:var(--gold);border-radius:8px;padding:8px 12px;letter-spacing:.04em}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:22px;margin-top:16px}
.card h2{font-size:17px;margin-bottom:12px}
.card h2 .tag{font-size:10.5px;vertical-align:middle;margin-left:8px;padding:3px 8px;border-radius:99px;border:1px solid var(--border);color:var(--dim);font-weight:700;letter-spacing:.08em}
.prov{font-size:14.5px;line-height:1.7;color:#3a2c22;white-space:pre-wrap;max-height:340px;overflow:auto;border-left:3px solid var(--gold);padding-left:14px}
.prov b{color:var(--ink)}
ul.duty{margin:0;padding-left:18px;font-size:14.5px;line-height:1.65}
ul.duty li{margin-bottom:10px}
ul.duty li b{color:var(--ink)}
.roles{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.roles span{font-size:12px;font-weight:700;border:1px solid var(--border);border-radius:99px;padding:5px 11px;color:var(--dim)}
.q{margin-top:14px;font-size:14.5px;font-weight:600;line-height:1.5}
.opts{display:flex;gap:10px;margin-top:8px}
.opts button{padding:8px 18px;border-radius:10px;border:1px solid var(--border);background:var(--card);font:700 13.5px 'Space Grotesk',sans-serif;color:var(--ink);cursor:pointer}
.opts button.sel-y{background:#1a1410;color:var(--gold);border-color:#1a1410}
.opts button.sel-n{background:var(--card);color:var(--dim);border-color:#b04030}
.verdict{margin-top:16px;border-radius:12px;padding:14px 16px;font-size:14px;line-height:1.55;display:none}
.verdict.show{display:block}
.verdict.yes{background:#eef4e6;border:1px solid #7d9b5e;color:#2e4420}
.verdict.maybe{background:rgba(201,168,76,.12);border:1px solid var(--gold);color:#5c4a1a}
.verdict.no{background:#f7e8e4;border:1px solid #c46a5a;color:#6e2c1e}
.links{margin-top:26px;display:flex;gap:10px;flex-wrap:wrap}
.links a{padding:9px 16px;border:1px solid var(--border);border-radius:10px;text-decoration:none;color:var(--ink);font-weight:600;font-size:14px}
.links a.p{background:#1a1410;color:var(--gold);border-color:#1a1410}
.note{margin-top:22px;padding:15px 17px;border-left:3px solid var(--gold);background:rgba(201,168,76,.08);border-radius:0 10px 10px 0;font-size:13px;color:var(--dim);line-height:1.55}
.note a{color:var(--gold)}
.pn{display:flex;justify-content:space-between;gap:10px;margin-top:26px;font-size:13.5px}
.pn a{color:var(--gold);text-decoration:none;font-weight:700;max-width:48%}
footer{margin-top:34px;color:var(--dim);font-size:12.5px}
table.atlas{width:100%;border-collapse:collapse;font-size:13.5px}
table.atlas td{padding:6px 8px;border-bottom:1px solid rgba(201,168,76,.15);vertical-align:top}
table.atlas a{color:var(--ink);text-decoration:none;font-weight:600}
table.atlas a:hover{color:var(--gold)}
.stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:26px 0}
.stat{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px}
.stat .v{font-size:28px;font-weight:800;letter-spacing:-.02em}
.stat .k{font-size:12px;color:var(--dim);margin-top:2px}
"""

SELF_CHECK_JS = """
(function(){
  var answers=[null,null,null];
  var qs=document.querySelectorAll('[data-q]');
  qs.forEach(function(q){
    var idx=+q.getAttribute('data-q');
    q.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        answers[idx]=b.getAttribute('data-v')==='y';
        q.querySelectorAll('button').forEach(function(x){x.className='';});
        b.className=answers[idx]?'sel-y':'sel-n';
        render();
      });
    });
  });
  function render(){
    var v=document.getElementById('verdict');
    if(answers.some(function(a){return a===null;})){v.className='verdict';return;}
    var msg,cls;
    if(!answers[0]){cls='no';msg='<b>Likely out of scope of this instrument.</b> Your situation does not appear to trigger the instrument itself — check the scope article linked on this page to be sure.';}
    else if(answers[1]&&answers[2]){cls='yes';msg='<b>Likely in scope — this provision probably binds you.</b> Read the provision text and duties above closely, and confirm against the official source before acting.';}
    else{cls='maybe';msg='<b>Possibly in scope.</b> The instrument applies but this specific provision may not, depending on the facts. The provision text above and the official source are the arbiters — this check is orientation, not advice.';}
    v.className='verdict show '+cls;v.innerHTML=msg;
  }
})();
"""


def provision_page(st_slug: str, st: dict, art: dict, prev_art, next_art,
                   total_in_statute: int) -> str:
    esc = html.escape
    label = article_label(art["number"], art["article_id"])
    title, body = art["title"], art["body"]
    anchor = art["anchor"]
    canon = f"{SITE_BASE}/law/{st_slug}/{art['slug']}.html"
    ovr = OVERRIDES.get((st_slug, art["number"]))
    is_annex = art["number"] < 0

    # (b) what it demands — hand-written where we have it, verbatim elsewhere
    if ovr:
        demands_html = f'<ul class="duty"><li>{esc(ovr["demands"])}</li></ul>'
        demands_tag = "PLAIN ENGLISH"
    else:
        obs = obligation_sentences(body)
        if obs:
            items = "".join(f"<li>{esc(o)}</li>" for o in obs)
            demands_html = (
                '<p class="lede" style="margin-top:0;font-size:13.5px">Key duties, '
                '<b>verbatim</b> from the provision text:</p>'
                f'<ul class="duty">{items}</ul>')
            demands_tag = "VERBATIM FROM TEXT"
        else:
            demands_html = f'<p class="prov" style="max-height:none;border:none;padding-left:0">{esc(first_sentences(body))}</p>'
            demands_tag = "VERBATIM FROM TEXT"

    binds = ovr["binds"] if ovr else st["binds_default"]
    roles = roles_mentioned(art["content"])
    roles_html = ""
    if roles:
        chips = "".join(f"<span>{esc(r)}</span>" for r in roles)
        roles_html = (f'<div style="margin-top:14px;font-size:12px;color:var(--dim)">'
                      f'Roles named in the provision text:</div><div class="roles">{chips}</div>')

    excerpt = art["content"] if len(art["content"]) <= 6000 else art["content"][:6000] + " …"
    subject_q = (f"Does your activity touch this provision's subject — {title[:90].lower()}?"
                 if title else "Does your activity touch this provision's subject matter?")

    nav_prev = (f'<a href="{prev_art["slug"]}.html">← {esc(article_label(prev_art["number"], prev_art["article_id"]))}</a>'
                if prev_art else "<span></span>")
    nav_next = (f'<a href="{next_art["slug"]}.html">{esc(article_label(next_art["number"], next_art["article_id"]))} →</a>'
                if next_art else "<span></span>")

    ld = {
        "@context": "https://schema.org",
        "@type": "LegislationObject",
        "name": f"{st['name']} {label} — {title}",
        "legislationType": "Regulation (EU)" if st["celex"][5] == "R" else "Directive (EU)",
        "legislationIdentifier": st["celex"],
        "url": canon,
        "isPartOf": {"@type": "Legislation", "name": st["official"]},
        "sameAs": st["source"],
    }

    desc = (f"{st['name']} {label} — {title[:80]}: what it demands, who it binds, "
            f"and a 3-question scope self-check. CSOAI law atlas.")

    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(st['name'])} {esc(label)} — {esc(title[:70])} | CSOAI Law Atlas</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a1a2f'/%3E%3Ctext x='16' y='23' font-family='Arial' font-size='20' font-weight='800' fill='%23e6c766' text-anchor='middle'%3EC%3C/text%3E%3C/svg%3E"/>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<div class="wrap">
<div class="crumb"><a href="/law/">Law atlas</a> &nbsp;/&nbsp; <a href="/law/#{st_slug}">{esc(st['name'])}</a> &nbsp;/&nbsp; {esc(label)}</div>
<div class="kicker">✦ {esc(st['name'].upper())} · {esc(label.upper())}</div>
<h1>{esc(title)}</h1>
<p class="lede"><b>{esc(st['name'])} {esc(label)}</b> · {esc(st['official'])} ·
<a style="color:var(--gold)" href="{st['source']}">official text (EUR-lex)</a></p>
<div class="anchor-chip" id="{anchor}">⚓ provision anchor: {anchor}</div>

<div class="card"><h2>What it demands <span class="tag">{demands_tag}</span></h2>
{demands_html}</div>

<div class="card"><h2>Who it binds</h2>
<p style="font-size:14.5px;line-height:1.65">{esc(binds)}</p>
{roles_html}</div>

<div class="card"><h2>Does this bind you? <span class="tag">3-QUESTION SELF-CHECK</span></h2>
<div class="q" data-q="0">1. {esc(st['scope_q'])}
  <div class="opts"><button data-v="y">Yes</button><button data-v="n">No</button></div></div>
<div class="q" data-q="1">2. {esc(st['role_q'])}
  <div class="opts"><button data-v="y">Yes</button><button data-v="n">No</button></div></div>
<div class="q" data-q="2">3. {esc(subject_q)}
  <div class="opts"><button data-v="y">Yes</button><button data-v="n">No</button></div></div>
<div id="verdict" class="verdict"></div></div>

<div class="card"><h2>The provision <span class="tag">{len(art['content']):,} CHARS · OFFICIAL TEXT</span></h2>
<div class="prov"><b>{esc(label)}.</b> {esc(excerpt)}</div>
<div style="margin-top:12px;font-size:12.5px;color:var(--dim)">Full consolidated text:
<a style="color:var(--gold)" href="{st['source']}">EUR-lex, CELEX {st['celex']}</a></div></div>

<div class="pn">{nav_prev}{nav_next}</div>
<div class="links">
  <a class="p" href="{st['source']}">Read the official text</a>
  <a href="/law/">Law atlas index</a>
  <a href="/gspc-gap-map">The 1,312-cell GSPC gap map</a>
  <a href="/gspc-arena">GSPC arena</a>
</div>
<div class="note"><b>What this page is not:</b> legal advice, and not a certification of
compliance. It is a working orientation to one provision — the citation above is the
authority. One of {total_in_statute} provisions of the {esc(st['name'])} mapped in the atlas.</div>
<footer>CSOAI · Council for the Safety of Artificial Intelligence · provision anchor <b>{anchor}</b> for GSPC cell linkage · measured, not marketed</footer>
</div>
<script>{SELF_CHECK_JS}</script>
</body></html>"""

# ─── Corpus loading + the gate ────────────────────────────────────────────────

def load_corpus(db_path: Path) -> dict[str, list[dict]]:
    """{statute_slug: [article dicts sorted: articles asc, then annexes I→XIII]}"""
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    out = {}
    for slug, st in STATUTES.items():
        rows = con.execute(
            "SELECT article_number, article_id, content FROM articles "
            "WHERE celex=? ORDER BY article_number", (st["celex"],)).fetchall()
        arts = []
        for number, aid, content in rows:
            is_annex = number < 0
            title, body = split_title(content or "", is_annex)
            arts.append({
                "number": number, "article_id": aid, "content": content or "",
                "title": title, "body": body, "slug": slug_for(number, aid),
                "anchor": anchor_for(st["prefix"], number, aid),
                "annex": is_annex,
            })
        # articles ascending, then annexes I → XIII (number -1 → -13)
        arts.sort(key=lambda a: (1, -a["number"]) if a["annex"] else (0, a["number"]))
        out[slug] = arts
    con.close()
    return out


def gated(arts: list[dict]) -> tuple[list[dict], list[dict]]:
    """THE GATE: no provision text, no page. Returns (kept, refused)."""
    kept, refused = [], []
    for a in arts:
        (kept if len(a["content"].strip()) >= MIN_PROVISION_CHARS else refused).append(a)
    return kept, refused


# ─── Index + sitemap ──────────────────────────────────────────────────────────

def index_page(corpus: dict[str, list[dict]], counts: dict[str, int]) -> str:
    esc = html.escape
    total = sum(counts.values())
    annex_total = sum(1 for arts in corpus.values() for a in arts if a["annex"])
    art_total = total - annex_total
    cards = []
    for slug, st in STATUTES.items():
        arts = corpus[slug]
        rows = []
        for a in arts:
            label = article_label(a["number"], a["article_id"])
            t = a["title"][:80] + ("…" if len(a["title"]) > 80 else "")
            rows.append(
                f'<tr><td style="white-space:nowrap;width:96px"><a href="/law/{slug}/{a["slug"]}.html">{esc(label)}</a></td>'
                f'<td><a href="/law/{slug}/{a["slug"]}.html" style="font-weight:400;color:var(--dim)">{esc(t)}</a></td>'
                f'<td style="white-space:nowrap;font:11px ui-monospace,monospace;color:var(--dim)">{a["anchor"]}</td></tr>')
        cards.append(f"""
<div class="card" id="{slug}"><h2>{esc(st['name'])} <span class="tag">{counts[slug]} PAGES</span></h2>
<p style="font-size:13.5px;color:var(--dim);line-height:1.55;margin-bottom:10px">{esc(st['blurb'])}
<a style="color:var(--gold)" href="{st['source']}">Official text</a></p>
<table class="atlas">{''.join(rows)}</table></div>""")

    ld = {"@context": "https://schema.org", "@type": "CollectionPage",
          "name": "CSOAI Law Atlas — provision-level map of six EU instruments",
          "url": f"{SITE_BASE}/law/",
          "about": [s["official"] for s in STATUTES.values()]}

    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Law Atlas — {total} provisions, page by page | CSOAI</title>
<meta name="description" content="Every provision of the EU AI Act, GDPR, DORA, NIS2, the Cyber Resilience Act and the CSRD — what it demands, who it binds, and a working scope self-check per page.">
<link rel="canonical" href="{SITE_BASE}/law/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230a1a2f'/%3E%3Ctext x='16' y='23' font-family='Arial' font-size='20' font-weight='800' fill='%23e6c766' text-anchor='middle'%3EC%3C/text%3E%3C/svg%3E"/>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<div class="wrap">
<div class="crumb"><a href="/">CSOAI</a> &nbsp;/&nbsp; Law atlas</div>
<div class="kicker">✦ THE LAW ATLAS</div>
<h1>{total} provisions. One page each. No filler.</h1>
<p class="lede">One working page per provision of six EU instruments — <b>what it demands,
who it binds, and a 3-question scope self-check</b> on every page. Each page carries a
<b>provision anchor</b> so GSPC gap-map cells link straight to the law they measure.
The rule of this atlas: no page without a provision, a citation, and a working interaction.</p>
<div class="stat-row">
  <div class="stat"><div class="v">{total}</div><div class="k">provision pages</div></div>
  <div class="stat"><div class="v">{art_total}</div><div class="k">articles</div></div>
  <div class="stat"><div class="v">{annex_total}</div><div class="k">annexes</div></div>
  <div class="stat"><div class="v">{len(STATUTES)}</div><div class="k">instruments</div></div>
</div>
{''.join(cards)}
<div class="links">
  <a class="p" href="/gspc-gap-map">The 1,312-cell GSPC gap map</a>
  <a href="/greenfield.html">The greenfield audit</a>
  <a href="/gspc-arena">GSPC arena</a>
</div>
<div class="note"><b>What this atlas is not:</b> legal advice, and not a certification.
It is a working map of the law as published — every page links the official consolidated
text on EUR-lex, which is the authority.</div>
<footer>CSOAI · Council for the Safety of Artificial Intelligence · measured, not marketed · csoai.org</footer>
</div></body></html>"""


def law_sitemap(urls: list[str]) -> str:
    today = dt.date.today().isoformat()
    body = "\n".join(
        f'  <url><loc>{SITE_BASE}{u}</loc><lastmod>{today}</lastmod>'
        f'<changefreq>monthly</changefreq><priority>0.7</priority></url>'
        for u in urls)
    return ("<?xml version='1.0' encoding='UTF-8'?>\n"
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB_PATH))
    ap.add_argument("--out", default=str(DEPLOY_DIR))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        print(f"FATAL: corpus not found: {db}", file=sys.stderr)
        return 1

    corpus = load_corpus(db)
    total_raw = sum(len(v) for v in corpus.values())

    if args.selftest:
        for slug, arts in corpus.items():
            kept, refused = gated(arts)
            print(f"{slug:10s} {len(arts):4d} provisions · gate keeps {len(kept)}, "
                  f"refuses {len(refused)}")
        print(f"total raw provisions: {total_raw}")
        return 0

    out_root = Path(args.out) / "law"
    out_root.mkdir(parents=True, exist_ok=True)

    kept_corpus, counts, refused_all, urls = {}, {}, [], []
    for slug, arts in corpus.items():
        kept, refused = gated(arts)
        kept_corpus[slug], counts[slug] = kept, len(kept)
        refused_all.extend((slug, a) for a in refused)
        d = out_root / slug
        d.mkdir(exist_ok=True)
        for i, a in enumerate(kept):
            prev_a = kept[i - 1] if i else None
            next_a = kept[i + 1] if i + 1 < len(kept) else None
            page = provision_page(slug, STATUTES[slug], a, prev_a, next_a, len(kept))
            (d / f"{a['slug']}.html").write_text(page, encoding="utf-8")
            urls.append(f"/law/{slug}/{a['slug']}.html")

    (out_root / "index.html").write_text(
        index_page(kept_corpus, counts), encoding="utf-8")
    (out_root / "sitemap.xml").write_text(law_sitemap(["/law/"] + urls), encoding="utf-8")

    total = sum(counts.values())
    print(f"✅ generated {total} provision pages + atlas index into {out_root}")
    for slug in STATUTES:
        print(f"   {slug:10s} {counts[slug]:4d} pages")
    if refused_all:
        print(f"⛔ gate refused {len(refused_all)} (provision text < {MIN_PROVISION_CHARS} chars):")
        for slug, a in refused_all:
            print(f"   {slug} {a['article_id']} ({len(a['content'].strip())} chars)")
    else:
        print("⛔ gate refused 0 — every provision carried real text")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
