# DRAFT — "Seoul signals: MCP's second year is about trust infrastructure"

**Status:** DRAFT v0.1, 2026-08-13 · reactive post for MCP Dev Summit Seoul (Aug 13–14) · publish after Day-2 keynotes land (24h window per F1) · zero-gate but owner posts
**Sources:** official schedule (mcpseoul2026.sched.com), agenda analysis, AAIF announcements of 2026-08-13 (57 new members incl. Visa/Wells Fargo/Alibaba Gold; Agentic AI Momentum Report)

---

MCP turned two this week in Seoul, and the agenda tells the story before any
keynote does. Of the ~60 sessions across two days, the densest clusters are not
about building servers — they are about **trusting** them:

- **Discovery is now named as the bottleneck.** "The MCP Registry Problem: Why
  Discoverability Is the Bottleneck Killing Ecosystem Growth" and "MCP Discovery
  Infrastructure: Registries, Trust, and Routing for Production Agents" are on the
  main track — the ecosystem admitting that a protocol without trustworthy
  discovery doesn't scale.
- **Conformance is a session topic, not a checkbox.** "Building and Testing MCP
  Servers With the Inspector, Conformance Suites, and Property-Based Testing" —
  the first conformance-testing talk at an MCP summit.
- **Security moved from bolt-on to headline track:** "Zero-Trust MCP: Treating
  Every Tool Call as an Untrusted API Request," "Hardening MCP Integrations
  Against Tool Poisoning," "The Confused Deputy Problem in MCP: Securing Chained
  Tool Calls in Multi-Agent Systems."
- **The buyers arrived.** AAIF announced 57 new members the same morning —
  Visa, Wells Fargo, Alibaba Gold — and an Agentic AI Momentum Report showing
  unpatched-CVE debt across 116 OSS agent projects up ~2.6× in six months.

The through-line: the question of MCP's third year is not "how do we connect
tools" but "how does anyone know what to trust." Registries without integrity
measurement are catalogs; conformance without signed, independently verifiable
evidence is a vibe. That is the gap a measurement layer fills — and it is the
gap we work in: signed verification records for MCP servers, a model-side
conformance leaderboard (the open slot nobody has claimed), and registry
curation that treats discoverability as an integrity problem, not an SEO problem.

[KEYNOTE-DELTA PLACEHOLDER: fold in Den Delimarsky's "Two Years of MCP: State of
the Ecosystem" content and the 10:00 TBA slot when published — check Day-2
keynotes (Sadogursky "MCP Is the Easy Part"; Baraiya "After the Tool Call")
before posting. One paragraph each, quoted precisely, no paraphrase drift.]

*Review notes (delete before publishing): (1) verify session titles against the
final sched.com page — agendas shift; (2) AAIF member list confirmed via their
Aug-13 announcement, cite it; (3) "the gap we work in" paragraph: name only
live artifacts (csoai 0.2.0 on PyPI, council-signal-mcp 0.1.2, MCP registry
io.github.CSOAI-ORG/csoai) — nothing unshipped; (4) tone: community event, no
vendor pitch (Linux Foundation CoC culture — analysis, not marketing).*
