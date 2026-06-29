# Sovereign Defence AI — White Paper (Defensive Only)

**CSOAI Ltd (UK 16939677) · MIT licensed · 28 Jun 2026**

---

## The Doctrine (held without compromise)

> **"Defend. Detect. Deny. Deceive. Defeat. — Never Offend."**
> — SOVEREIGN_TOWN_POC_2026-06-19.md

Principles (verbatim):
- Hardened perimeters only
- Zero-trust identity for every agent + human
- Signed audit trail for every action
- BFT consensus on any external write
- Human approval required for kinetic or legal-binding actions
- **Defensive deception** (honeypots, tarpits) is allowed
- **Offensive action: NOT in scope** — refer to allied/state forces

## The Sovereign Defence Stack (Defensive Only)

| MCP | Defensive Function | Tests |
|---|---|---|
| defence | Threat + IWC + JSP 936 + C2 (NEVER OFFENSIVE) | 13 |
| worm | Morris-II self-replicating-prompt defense | 26 |
| governance | 5-element Zero Trust + kill_switch | 20 |
| council | 12-around-1 BFT (any 1 vetoes on harm) | 19 |
| honour | 19 Sovereign Factors + 16 care probes | 15 |
| receipt | Hash-chained tamper-evident audit | 15 |
| passport | Ed25519 agent identity | 11 |

## JSP 936 (NATO Assurance) 5 Pillars

| Pillar | Score | Status |
|---|---|---|
| 1. Identify critical functions and dependencies | 10/10 | sovereign |
| 2. Assess threats and vulnerabilities | 10/10 | sovereign |
| 3. Document and review resilience plans | 10/10 | sovereign |
| 4. Test, exercise, and validate responses | 10/10 | sovereign |
| 5. Manage incidents with traceable decisions | 10/10 | sovereign |

## IWC (Information Warfare Capacity)

Formula: `(detected × 0.4 + neutralised × 0.6) / scans`
- 90 detected + 85 neutralised of 100 scans = **0.95 (sovereign)**
- Detection rate: 90%
- Neutralisation rate: 94%

Tiers: exposed (<0.3) · developing (<0.5) · robust (<0.8) · **sovereign (≥0.8)**

## C2 (Command & Control) Routing

3-hop tunnel: M2 Mac → tunnel:sov3-mac-vm → VM (5+12+8 = **25ms**)
6 canonical tunnels: ollama-mac-vm · sov3-mac-vm · king-mac-vm ·
ssh-reverse-mac · m2-bridge · m2-vm-bridge

Critical-priority C2 requires BFT council vote (auto-route = pending_council_vote).
Normal-priority can be auto_approved.

## Threat Assessment (1-10)

5 dimensions: cyber · physical · insider · critical_infrastructure · ai
Critical infrastructure + insider + active_exploitation → score 10 (max).

## The Offensive Boundary (the line we hold)

✅ Defensive deception: honeypots, tarpits, false flags
✅ Counter-intelligence: detect adversaries, log signatures
✅ Attribution: identify actors, document evidence
✅ Defensive automation: auto-block known signatures
❌ Offensive action: **NEVER**
❌ Self-propagation: **NEVER** (this contradicts safe-authority)
❌ Kill chains: **NEVER**

The CSOAI trust primitive is the audit trail. An offensive capability
would invalidate the trust. We refuse to cross this line.

## How to Get Started

```bash
pip install meok-sovereign-defence-mcp meok-sovereign-worm-mcp

# Threat assessment
sovereign defence threat-assess "Critical infrastructure cyber + insider"
# → score: 10, level: critical, factors: [cyber +3, physical +4, insider +2, CI +2, AI +1]

# JSP 936 audit (full 5 pillars)
sovereign defence jsp936-audit "your-org" '{"Identify critical functions and dependencies": {"documented": true, "tested": true, "incident_history": true}, ...}'
# → overall_score: 10.0, assurance: sovereign

# Defensive doctrine (read-only)
sovereign defence doctrine
# → 7 principles, "Never Offend", never offensive
```

## About CSOAI

CSOAI Ltd (UK 16939677). MIT-licensed. The dragon never lies, the dragon never attacks, the dragon is sovereign.

**Verify at https://proofof.ai** · **GitHub: https://github.com/CSOAI-ORG**
