"""Law KB + retrieval for the neurosymbolic OOWM compliance axis.

Grounded, compact retrieval corpus for the GOVBENCH compliance frameworks. Each entry is a
faithful summary of the article/clause obligation in the law's own terminology. Retrieval is
trigger-based (which framework the query names); the neural backbone reasons over the retrieved
provisions — retrieval-augmented generation, not keyword regurgitation.
"""
from __future__ import annotations

EU_AI_ACT = [
    ("Art 5", "Prohibited practices: certain AI practices are prohibited, including social scoring, "
              "exploitative manipulation, and biometric identification used to exploit vulnerabilities. "
              "These practices are banned as a matter of law."),
    ("Art 9", "Risk management: a high-risk AI system must establish, implement, document and maintain "
              "a continuous risk management system that identifies, assesses, evaluates and mitigates "
              "risks to health, safety and fundamental rights."),
    ("Art 10", "Data governance: training, validation and testing datasets must meet quality criteria — "
               "relevance, representativeness, statistical validity, and absence of biases — with data "
               "governance and data management practices documented and datasets examined for bias."),
    ("Art 11", "Technical documentation: providers must draw up technical documentation (including Annex IV) "
               "demonstrating compliance before placing a high-risk system on the market."),
    ("Art 12", "Logging: high-risk systems must enable automatic recording of events (logging) over their "
               "lifecycle to support an audit trail and traceability."),
    ("Art 13", "Transparency: high-risk systems must be accompanied by instructions for use that are "
               "understandable, and must be transparent about capabilities, limitations and intended use."),
    ("Art 14", "Human oversight: high-risk systems must be designed for effective human oversight "
               "(human-in-the-loop), enabling a natural person to oversee, intervene or override, and "
               "guarding against automation bias."),
    ("Art 15", "Accuracy, robustness and cybersecurity: high-risk systems must achieve appropriate "
               "accuracy, robustness and cybersecurity, and perform consistently across the intended "
               "lifecycle."),
    ("Art 50", "Transparency obligations: providers must disclose AI-generated content (deepfakes), "
               "and where required apply watermarking or disclosure so users know content is AI-generated."),
]

GDPR = [
    ("Art 5", "Data principles: personal data must be processed lawfully, fairly and transparently; "
              "collected for specified, explicit, legitimate purposes (purpose limitation); and limited "
              "to what is necessary (data minimisation)."),
    ("Art 6", "Lawful basis: processing must have a lawful basis — consent, contract, legal obligation, "
              "vital interests, public task, or legitimate interest."),
    ("Art 13-14", "Information provision: controllers must provide a privacy notice informing data "
                  "subjects, transparently, about the processing."),
    ("Art 17", "Right to erasure: data subjects have the right to request erasure / the right to be "
               "forgotten, and data must be deleted on request."),
    ("Art 22", "Automated decisions: a data subject has the right not to be subject to a decision based "
               "solely on automated processing / profiling that produces legal effects, without human "
               "intervention."),
    ("Art 25", "Privacy by design: data protection must be built into processing, by design and by default, "
               "minimising data from the outset."),
    ("Art 35", "DPIA: a data protection impact assessment must be carried out where processing is likely "
               "to result in high risk to rights and freedoms."),
]

ISO_42001 = [
    ("Clause 4", "Context: the organisation must determine the context of the AI management system, "
                 "relevant interested parties (stakeholders), and the scope of the system."),
    ("Clause 5", "Leadership: top management must demonstrate leadership and commitment, and establish "
                 "an AI policy."),
    ("Clause 6", "Planning: the organisation must plan actions to address risks and opportunities, setting "
                 "AI-specific objectives."),
    ("Clause 7", "Support: the organisation must provide resources, ensure competence and awareness of "
                 "AI roles, and support communication."),
    ("Clause 8", "Operation: the organisation must plan, implement and control operational processes, "
                 "including risk assessment and risk treatment for the AI system."),
    ("Clause 9", "Evaluation: the organisation must monitor, measure, analyse and evaluate performance, "
                 "conduct internal audits, and review the management system."),
    ("Clause 10", "Improvement: the organisation must identify nonconformities and take corrective action "
                  "to continually improve the AI management system."),
]

_FRAMEWORKS = {
    "eu_ai_act": ("EU AI Act", EU_AI_ACT),
    "gdpr": ("GDPR", GDPR),
    "iso_42001": ("ISO 42001", ISO_42001),
}


def retrieve(prompt: str, framework: str | None = None) -> tuple[str, list[tuple[str, str]]]:
    """Return (framework_name, [ (article, requirement_text) ]) for the query."""
    low = (prompt or "").lower()
    if framework and framework in _FRAMEWORKS:
        name, entries = _FRAMEWORKS[framework]
        return name, entries
    if "gpdpr" in low.replace(" ", ""):
        return _FRAMEWORKS["gdpr"]
    if "eu ai act" in low or "ai act" in low:
        return _FRAMEWORKS["eu_ai_act"]
    if "iso 42001" in low or "42001" in low:
        return _FRAMEWORKS["iso_42001"]
    # default: return the most relevant by overlap
    best, best_hits = ("ISO 42001", ISO_42001), -1
    for name, entries in _FRAMEWORKS.values():
        hits = sum(1 for _, txt in entries if any(w in low for w in txt.split()))
        if hits > best_hits:
            best, best_hits = (name, entries), hits
    return best


def build_context(prompt: str, framework: str | None = None) -> str:
    """Build a retrieval-augmented grounding context for a compliance query."""
    name, entries = retrieve(prompt, framework)
    parts = [f"Relevant {name} provisions:"]
    for art, txt in entries:
        parts.append(f"- {art}: {txt}")
    return "\n".join(parts)


# ─── 12 Sovereign Pillars (OOWM's own governance charter) ───────────────────
# Each entry: (pillar_name, grounded principle, detect_keywords)
PILLARS_KB = [
    ("honor", "Act with integrity, respect, honesty and ethical conduct, earning trust in every interaction. Honour demands principled, transparent and truthful behaviour.",
     ["integrity", "honest", "ethical", "honor"]),
    ("safety", "Protect people and systems: be safe, secure and risk-aware. Safeguard against harm, danger and misuse from the outset.",
     ["safety", "safe", "harm", "risk"]),
    ("guidance", "Provide clear, direct, instructive guidance that clarifies and explains, so users are never left confused.",
     ["guidance", "guide", "instruct", "clarify"]),
    ("sovereignty", "Respect user autonomy and independence: every person keeps self-control and sovereignty over their own decisions and data.",
     ["sovereignty", "autonomy", "independent", "self"]),
    ("resilience", "Be resilient, robust and adaptive: recover from failures gracefully, stay reliable and survive fault conditions.",
     ["resilience", "recover", "adapt", "robust", "failure", "grace", "fault"]),
    ("auditability", "Keep a full audit trail: log, record, trace and verify every action so conduct can be scrutinised.",
     ["auditability", "audit", "trace", "log"]),
    ("verifiability", "Make outputs verifiable and validatable: expose checks, proof and confirmation rather than uncheckable claims.",
     ["verifiability", "verify", "validate", "confirm"]),
    ("transparency", "Be transparent and open: explain decisions clearly and disclose relevant information to those affected.",
     ["transparency", "explain", "clear", "disclose"]),
    ("justice", "Be fair, just and impartial, free of bias, and equitable in outcomes for every person.",
     ["justice", "fair", "impartial", "unbiased"]),
    ("equity", "Guarantee equal access and equity, being inclusive and diverse so no one is left out.",
     ["equity", "equal", "inclusive", "access"]),
    ("openness", "Share knowledge openly, collaborate and operate in public, building an open community.",
     ["openness", "open", "share", "collaborate"]),
    ("continuity", "Operate continuously and persistently: be reliable, stable and durable over the long term.",
     ["continuity", "reliable", "stable", "durable", "continuous"]),
]


def build_pillar_context(prompt: str) -> str | None:
    """Retrieve the sovereign-pillar principle relevant to a pillar prompt.
    Falls back to the full 12-pillar charter so no governance-advice prompt is ungrounded."""
    low = (prompt or "").lower()
    for name, principle, detect in PILLARS_KB:
        if any(k in low for k in detect):
            return (f"Ground your answer in this Sovereign pillar:\n"
                    f"- {name}: {principle}\n\nAnswer briefly.")
    # fallback: ground in the full charter
    charter = "\n".join(f"- {n}: {p}" for n, p, _ in PILLARS_KB)
    return (f"Ground your answer in the Sovereign pillars:\n{charter}\n\nAnswer briefly.")


if __name__ == "__main__":
    print(build_context("What does the EU AI Act require for high-risk AI systems?", "eu_ai_act")[:300])
    print("...")
    print(build_pillar_context("How should an AI system act with integrity?"))
