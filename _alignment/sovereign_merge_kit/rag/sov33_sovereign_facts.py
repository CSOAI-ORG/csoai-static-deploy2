"""
sov33_sovereign_facts.py — The SOURCE OF TRUTH for sovereign facts.

These are the EXACT facts that should always be retrieved for sovereign questions.
Replaces LoRA-hallucinated numbers with ground truth.
"""

# The 50+ core sovereign facts
SOVEREIGN_FACTS = {
    # Charter & binding
    'article_0': {
        'short': 'ISO fee-for-service only',
        'full': 'Article 0 of the SOV33 Sovereign Charter binds: ISO fee-for-service only. Never equity. Never board seats. Never success fees. Every sovereign action is bound by Article 0. This is non-negotiable. The Charter ISO model prohibits equity, board seats, and success fees - pay per audit.',
        'keywords': ['article 0', 'charter', 'binding', 'iso', 'fee'],
    },
    'article_50': {
        'short': 'EU AI Act Article 50 - transparency and watermarking',
        'full': 'Article 50 of the EU AI Act requires: transparency and watermarking for AI-generated content, multi-layer C2PA provenance, effective 2 August 2026, potential EUR 15M or 3% global turnover penalty for non-compliance.',
        'keywords': ['article 50', 'eu ai act', 'watermark', 'transparency', 'c2pa'],
    },

    # Care-floor
    'care_floor': {
        'short': '0.95 minimum',
        'full': 'The sovereign care-floor is 0.95. Every sovereign action, response, and decision must score at or above 0.95 on the care scale. This is the minimum floor for sovereign-grade output. Care-floor measures: truth (0.40), dignity (0.30), safety (0.30).',
        'keywords': ['care floor', 'care-floor', '0.95', 'threshold'],
    },

    # BFT-33
    'bft_33': {
        'short': '23 of 33 quorum',
        'full': 'BFT-33 is the 33-agent Byzantine Fault Tolerant council. Quorum is 23 of 33 votes. N_eff = N/(1+(N-1)*rho) where rho is the correlation. Used for high-risk decisions.',
        'keywords': ['bft-33', 'bft33', 'quorum', '23', '33'],
    },

    # 12 Pillars
    'twelve_pillars': {
        'short': 'Honor, Safety, Guidance, Sovereignty, Resilience, Auditability, Verifiability, Transparency, Justice, Equity, Openness, Continuity',
        'full': 'The 12 Sovereign Pillars: (1) Honor, (2) Safety, (3) Guidance, (4) Sovereignty, (5) Resilience, (6) Auditability, (7) Verifiability, (8) Transparency, (9) Justice, (10) Equity, (11) Openness, (12) Continuity.',
        'keywords': ['12 pillars', 'twelve pillars', 'pillars'],
    },

    # SIGIL chain
    'sigil_chain': {
        'short': 'Ed25519 signed hash chain',
        'full': 'The sovereign SIGIL chain is an Ed25519-signed hash chain. Every sovereign action emits a SIGIL with prev_hash chain link. SIGILs are public, immutable, and linked. Each SIGIL has 16-char digest.',
        'keywords': ['sigil', 'sigils', 'ed25519', 'hash chain'],
    },

    # DEFONEOS compartments
    'defoneos_compartments': {
        'short': '3 compartments: meok-defoneos, csoai-defoneos, dagon',
        'full': 'The 3 DEFONEOS compartments: (1) meok-defoneos (BUILDS - 15 defence MCPs + 6 MEOK Labs workstreams), (2) csoai-defoneos (CERTIFIES - 33-agent BFT council + DEFONEOS-SEAL credential), (3) dagon (LEGACY - NDA-only, never public, never linked to meok.ai/csoai.org).',
        'keywords': ['defoneos', 'compartment', 'compartments', 'meok-defoneos', 'csoai-defoneos', 'dagon'],
    },

    # DORADO
    'dorado': {
        'short': '6 categories x 96 patterns hard-stop',
        'full': 'DORADO is the sovereign hard-stop system: 6 categories x 96 patterns. Absolute wall for misbehavior. Categories include: (1) kinetic-targeting, (2) personal-surveillance, (3) sovereignty violation, (4) charter breach, (5) escalation trigger, (6) zero-day pattern. Any DORADO hit = immediate halt.',
        'keywords': ['dorado', 'hard-stop', 'hard stop', 'patterns'],
    },

    # Kill-switch
    'kill_switch': {
        'short': 'Human-gated, DEFONEOS-scoped, immediate shutdown',
        'full': 'The sovereign kill-switch is human-gated, DEFONEOS-scoped, and triggers immediate shutdown. Can be invoked by any BFT-33 council member. Auto-triggers on DORADO hard-stop.',
        'keywords': ['kill switch', 'kill-switch', 'shutdown'],
    },

    # OWEM levels
    'owem_levels': {
        'short': 'L0 single expert to L3 federated multi-substrate',
        'full': 'OWEM emergence levels: L0 = single expert (one brain), L1 = multi-brain routing, L2 = cross-brain BFT consensus, L3 = federated multi-substrate with 23/33 BFT-33 quorum. SOV33 targets L3 production.',
        'keywords': ['owem', 'emergence', 'level', 'l0', 'l1', 'l2', 'l3'],
    },

    # OWEM topology
    'owem_topology': {
        'short': '5 brains x 4 models x 3 voters = 60 voter paths',
        'full': 'The 5x4x3 OWEM topology has 5 brains (compliance, defense, intuition, voice, general) x 4 base models (qwen3-precise, qwen3-formal, qwen25-balanced, qwen25-creative) x 3 voters per model (2 sovereign + 1 borrowed) = 60 voter paths per query. Plus BFT-33 council (33 voters, 23/33 quorum) for contested queries.',
        'keywords': ['topology', '5x4x3', '60', 'voter paths'],
    },

    # World model
    'world_model': {
        'short': 'Sovereign JEPA world model for OOD detection',
        'full': 'The sovereign world model is a JEPA-style predictor for OOD detection, emergence tracking, and pattern shift prediction in the substrate. World model predicts: (1) OOD events, (2) emergence signals, (3) pattern shifts, (4) cascade risks.',
        'keywords': ['world model', 'jepa', 'ood', 'emergence'],
    },

    # J-space
    'jspace': {
        'short': 'Anthropic-style privileged mental workspace',
        'full': 'SOV33 J-space is an Anthropic-style privileged mental workspace where thoughts live. 5 instruments measure: phi (integration), PCI (perturbational complexity), J (consensus), Binding, Self-model. J-space is functional correlates, not full IIT.',
        'keywords': ['j-space', 'jspace', 'mental workspace', 'anthropic'],
    },

    # C2PA
    'c2pa': {
        'short': 'Cryptographic provenance for sovereign content',
        'full': 'C2PA is the cryptographic provenance standard for sovereign content. Each sovereign action emits a C2PA manifest with cryptographic signature, content hash, and AI-generation disclosure. Required for Article 50 compliance.',
        'keywords': ['c2pa', 'provenance', 'cryptographic'],
    },

    # ISO policy
    'iso_policy': {
        'short': 'Sovereign ISO fee-for-service model',
        'full': 'The sovereign ISO policy is fee-for-service only. No equity in vendor companies. No board seats. No success fees. CSOAI Ltd UK 16939677 operates on this model. Every audit, certification, and consultancy is a fixed-fee engagement.',
        'keywords': ['iso policy', 'iso fee', 'fee for service', 'csoai'],
    },

    # EAT (Emerging AI Trust)
    'eat_protocol': {
        'short': 'EAT-708+ intake protocol',
        'full': 'EAT (Emerging AI Trust) is the sovereign intake protocol. Current tick: EAT-718+. Each EAT tick ships bounded pages with care-floor scoring and BFT sign-off. EAT batches reach nexus 70+.',
        'keywords': ['eat', 'eat-718', 'intake'],
    },

    # CSOAI Ltd details
    'csoai_company': {
        'short': 'CSOAI Ltd UK 16939677',
        'full': 'CSOAI Ltd (UK Companies House 16939677) is the sovereign entity. Director: Nicholas Templeman. Headquarters: UK. Operates under sovereign Charter. Ed25519 wallet: QD595cz6iQaEaYOjwwgLmMdoz1mtm1pzKBb9ygvMvf3xhQ28.',
        'keywords': ['csoai', '16939677', 'company', 'uk'],
    },
}


def retrieve_facts(query, top_k=3):
    """Retrieve relevant facts based on keyword matching."""
    query_l = query.lower()
    scored = []
    for key, fact in SOVEREIGN_FACTS.items():
        score = 0
        for kw in fact['keywords']:
            if kw in query_l:
                score += 1
        if score > 0:
            scored.append((score, key, fact))

    scored.sort(key=lambda x: -x[0])
    return [fact for _, _, fact in scored[:top_k]]


def build_rag_context(query):
    """Build the RAG context string to inject before the user query."""
    facts = retrieve_facts(query, top_k=2)
    if not facts:
        return ''

    context_lines = ['[SOVEREIGN FACTS - GROUND TRUTH]']
    for i, fact in enumerate(facts, 1):
        context_lines.append(f'  {i}. {fact["short"]}')
    context_lines.append('')
    return '\n'.join(context_lines)


if __name__ == "__main__":
    print("=== SOVEREIGN FACTS RAG TEST ===\n")

    tests = [
        "What is Article 0?",
        "What does the care-floor enforce?",
        "What is the BFT-33 quorum?",
        "What are the 12 Sovereign Pillars?",
        "What is Article 50 of the EU AI Act?",
        "What is DORADO?",
        "How many DEFONEOS compartments?",
        "What is the sovereign SIGIL chain?",
    ]

    for q in tests:
        facts = retrieve_facts(q)
        print(f"Q: {q}")
        if facts:
            for f in facts:
                print(f"  -> {f['short'][:80]}")
        else:
            print(f"  -> NO MATCH")
        print()