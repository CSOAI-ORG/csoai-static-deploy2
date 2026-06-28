# IndieHackers founder story — Building 12 sovereign MCPs solo on a UK farm

**Title:** I shipped 12 sovereign MCPs solo in 1 week (167 tests, MIT). Here's the playbook.

I'm Nick. I run CSOAI Ltd (UK 16939677) out of a 6.5-acre farm with 8 malamutes, a koi pond, and a Qidi Max4 3D printer. Last week I shipped 12 MCP (Model Context Protocol) servers — the AI agent stack that gives agents identity, audit trails, and provable signatures.

**The playbook in 5 minutes:**

1. **Pick the gap nobody else fills.** MCP servers are exploding (300+ in the registry). Most are thin wrappers. The gap: governance + audit + sovereignty. I wrapped proven OSS projects (aetherproof, superagent-ai, cognee, CesiumJS, Microsoft AGT) into sovereign MCPs that sign every output.

2. **Don't build, absorb.** I cloned 8 OSS crown jewels (~350MB total). Each one taught me the canonical pattern. Then I built thin sovereign wrappers around them.

3. **The 7-MCP scaffold pattern.** Every MCP has: pyproject.toml + LICENSE (MIT) + __init__.py (~300 lines) + tests/ (~10-20 test functions) + README.md. Total per MCP: 4 files, ~600 lines, 10-20 tests.

4. **Ed25519 everything.** Every output signed. Every verify URL points to proofof.ai. The substrate is the brand.

5. **Tests = moat.** 167 tests across 12 MCPs in <1.5 seconds. Not because tests are fast — because the surface is small and the patterns repeat.

**The stack I shipped in 7 days:**
- passport (agent identity, 11 tests)
- guardrails (security, 20 tests)
- receipt (audit trail, 15 tests)
- governance (5-element, 20 tests)
- x402-payment (micropayments, 12 tests)
- supply-chain (SBOM/SLSA, 10 tests)
- globe (33-hive map, 18 tests)
- council (BFT voting, 19 tests)
- memory (episodic+graph, 12 tests)
- avatar (VRM embodied, 10 tests)
- skills (lifecycle, 10 tests)
- eu-ai-act-kit (Aug 2 deadline, 10 tests)

**Total: 12 MCPs, 167 tests, MIT licensed.**

The doctrine: the dragon never lies (signs every action), the dragon holds the wall (refuses to spend your money without your say-so), the dragon never sleeps (live substrate grinding 24/7).

What I'd do differently: start with one MCP, get paying users, then expand. The 12-at-once approach is impressive but exhausting.

Built on M2 Mac + Claude + Kimi (research) + SOV3 substrate.

If you want to ship sovereign agents: github.com/CSOAI-ORG
