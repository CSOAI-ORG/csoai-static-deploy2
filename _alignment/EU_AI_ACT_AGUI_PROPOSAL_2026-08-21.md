# EU AI Act — AG-UI Agentic Reading Surface (proposal package)

**From:** CSOAI Ltd / Council of AI (independent measurement body, UK 16939677)
**Date:** 2026-08-21
**Status:** proposal — ready to hand over; built on estate components already live
**Why this exists:** artificialintelligenceact.eu is a superb *reference* — but it is
read-only text. 150k users/month come to *read* the Act. This package turns that
reading surface into an *agentic* surface: the same authoritative content, queryable
and citable by any agent, with measurement-grade receipts.

---

## 1. The core idea (one paragraph)

Your site answers questions by **publishing pages**; agents answer questions by
**calling tools**. We propose an AG-UI + MCP overlay that wraps the AI Act's own
content (Explorer text, article pages, compliance checker) so that an agent can
ask "what does Article 50 require of a deployer before Aug 2026?" and get back a
**cited, structured, verifiable answer** — with the article text, the obligation,
the deadline, and a signed receipt proving *what was claimed and when*. The human
reader stays on your site; the agent reader gets a first-class protocol surface.
Nobody rewrites the Act. The overlay is additive.

## 2. What already exists in our estate (all live, ready to wire)

| Component | Location | Status |
|---|---|---|
| AG-UI gateway (agent→user events, JSON Patch/CUSTOM/RUN lifecycle) | `:4191/agui/stream` | LIVE (Sim World) |
| `meok-annex-iii-impact-mcp` | `classify_system`, `check_article_compliance`, `generate_fria`, `generate_annex_iv_documentation` | packaged |
| `meok-sovereign-aiact-passport-mcp` | sovereign AI Act passport (measurement-grade) | packaged |
| `eu-cra-mcp` | CRA cross-reference | packaged |
| `meok-eu-code-of-practice-mcp` | GPAI Code of Practice | packaged |
| `csoai-gspc-mcp` | 16-axis GSPC measurement, signed cards | LIVE at workers.dev |
| Signed-receipts extension (A2A) | Ed25519 receipts per claim (`a2a.signed-receipt/0.1`, RFC 8785) | draft 0.2, tested |

## 3. The AG-UI agent card (what we hand over)

```json
{
  "name": "EU AI Act Assistant (by Council of AI)",
  "description": "Query the EU AI Act with citations. Classify an AI system under Annex III, check article compliance, generate an FRIA, and get a signed measurement receipt for every answer.",
  "url": "https://councilof.ai/agents/eu-ai-act-assistant/",
  "version": "1.0.0",
  "skills": [
    {
      "id": "read-act",
      "name": "Read the Act",
      "description": "Article-level Q&A over the full AI Act text with citations",
      "tags": ["gov", "compliance", "reading"]
    },
    {
      "id": "classify-system",
      "name": "Classify a system",
      "description": "Annex III high-risk classification from a system description",
      "tags": ["gov", "classification"]
    },
    {
      "id": "check-compliance",
      "name": "Check compliance",
      "description": "Per-article obligation check with evidence state and deadlines",
      "tags": ["compliance", "audit"]
    },
    {
      "id": "fria",
      "name": "Generate FRIA",
      "description": "Fundamental Rights Impact Assessment scaffold",
      "tags": ["fria", "rights"]
    },
    {
      "id": "signed-receipt",
      "name": "Signed receipt",
      "description": "Every answer ships with an Ed25519 receipt: content_id + claim + timestamp",
      "tags": ["attestation", "measurement"]
    }
  ],
  "capabilities": {
    "extensions": [
      {
        "uri": "https://councilof.ai/a2a/extensions/signed-receipts/v1",
        "required": false,
        "params": { "issuer": "did:web:councilof.ai" }
      }
    ]
  }
}
```

## 4. The MCP manifest (wire into any MCP-capable client)

```json
{
  "mcpServers": {
    "eu-ai-act-reader": {
      "command": "python3",
      "args": ["/path/to/meok-annex-iii-impact-mcp/server.py"],
      "env": { "CSOAI_SIGN": "1" }
    },
    "eu-ai-act-passport": {
      "command": "python3",
      "args": ["/path/to/meok-sovereign-aiact-passport-mcp/server.py"]
    },
    "eu-cra": {
      "command": "python3",
      "args": ["/path/to/eu-cra-mcp/server.py"]
    },
    "eu-code-of-practice": {
      "command": "python3",
      "args": ["/path/to/meok-eu-code-of-practice-mcp/server.py"]
    }
  }
}
```

## 5. New ways of *reading* their site (the "just text" fix)

The site is a WordPress corpus. Three additive reading surfaces, no rewrite:

1. **AG-UI event stream** — emit the Explorer's article index as AG-UI
   `STATE_SNAPSHOT`/`CUSTOM` events on a public stream, so any AG-UI renderer
   (including the one we already run for Sim World on :4191) can render the Act
   as a live, queryable object rather than a static page.
2. **llms.txt + MCP discovery** — expose `llms.txt` at the site root and an MCP
   endpoint listing the Explorer's article index, so agents *discover* the Act
   the way search engines discover pages. This is what "150k readers" becomes
   for agents: a structured index instead of a wall of prose.
3. **Signed reading receipts** — every agent query returns `{answer, article
   ref, obligation, deadline, evidence_sha256, sig}`. Readers can *verify* an
   answer independently (RFC 8785 + Ed25519, `did:web:councilof.ai`). That is the
   "trust root" no other EU AI Act site has.

## 6. What we need from you (2 lines)

1. Confirmation to stand up the AG-UI stream + llms.txt + MCP endpoint against
   your content (we host on Cloudflare Workers, free tier; no changes to your
   WordPress).
2. A contact for handover (email or Slack) — or we post the agent card publicly
   at `https://councilof.ai/agents/eu-ai-act-assistant/` and send you the link.

## 7. Proof it works (already measured)

- Signed-receipts extension: 12/12 regression checks pass (roundtrip, tamper,
  exact-key DID, revocation, RFC 8785 vector).
- Annex III classifier + article compliance checker: packaged, PyPI-ready.
- GSPC measurement: live at `csoai-gspc-mcp.nicholastempleman.workers.dev`,
  HTTP 200, signed cards minted into `csoai/gspc-boards` on Hugging Face.
- AG-UI gateway: live on :4191, streaming Sim World as AG-UI events today.

---

*Prepared by CSOAI Ltd (Council of AI) — measurement, not certification. All
receipts carry the register: evidence of what was claimed and when; never a
certification, endorsement, or conformity mark.*
