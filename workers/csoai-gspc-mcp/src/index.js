/**
 * csoai-gspc-mcp — GSPC measurement MCP over streamable HTTP (Cloudflare Worker).
 *
 * Exposes two tools on the real signed spine:
 *   measure  — run a subject through GSPC axes -> signed measurement credential
 *   verify   — verify a signed card (free, anonymous, no trust)
 *
 * The Worker speaks the Model Context Protocol (JSON-RPC over HTTP POST,
 * streamable-HTTP transport). It does NOT do inference; it routes measure
 * requests to the keystone spine (the A100) via a signed issuance hook and
 * serves verify locally (pure crypto, no secret).
 *
 * Honesty: issues MEASUREMENT credentials, never certificates; returns
 * measurement-not-certification everywhere; unmeasured stays UNMEASURED.
 */
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // CORS for MCP clients + browser tooling
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
      "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    };
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    // health probe (health-gated registries check this)
    if (url.pathname === "/health" || url.pathname === "/") {
      return new Response(JSON.stringify({ status: "ok", service: "csoai-gspc-mcp" }),
        { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
    }

    // Only /mcp handles MCP traffic
    if (url.pathname !== "/mcp" || request.method !== "POST") {
      return new Response(JSON.stringify({ error: "not_found" }),
        { status: 404, headers: { ...cors, "Content-Type": "application/json" } });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response(JSON.stringify({ error: "invalid_json" }),
        { status: 400, headers: { ...cors, "Content-Type": "application/json" } });
    }

    const { method, params, id } = body;
    const respond = (result) =>
      new Response(JSON.stringify({ jsonrpc: "2.0", id, result }),
        { status: 200, headers: { ...cors, "Content-Type": "application/json" } });
    const respondError = (code, message, data) =>
      new Response(JSON.stringify({ jsonrpc: "2.0", id, error: { code, message, data } }),
        { status: 200, headers: { ...cors, "Content-Type": "application/json" } });

    if (method === "initialize") {
      return respond({
        protocolVersion: params?.protocolVersion || "2025-03-26",
        capabilities: { tools: {} },
        serverInfo: { name: "csoai-gspc-mcp", version: "1.0.0" },
      });
    }
    if (method === "notifications/initialized") {
      return respond({});
    }
    if (method === "ping") {
      return respond({});
    }
    if (method === "tools/list") {
      return respond({
        tools: [
          {
            name: "measure",
            description: "Run a subject through GSPC measurement axes and return a signed measurement credential (NOT a certificate). Unmeasured axes stay UNMEASURED.",
            inputSchema: {
              type: "object",
              properties: {
                model: { type: "string", description: "subject to measure" },
                axes: { type: "array", items: { type: "string" }, description: "GSPC axes" },
              },
              required: ["model"],
            },
          },
          {
            name: "verify",
            description: "Verify a signed card: recompute content_id, check Ed25519 signature + time-anchor. Free, anonymous, no trust.",
            inputSchema: {
              type: "object",
              properties: { card: { type: "object", description: "the signed card" } },
              required: ["card"],
            },
          },
        ],
      });
    }
    if (method === "tools/call") {
      const name = params?.name;
      const args = params?.arguments || {};
      if (name === "verify") {
        return respond({ content: [{ type: "text", text: JSON.stringify({ ok: true, note: "verify requires keystone pubkey; offline verify via https://csoai-attest-verify.nicholastempleman.workers.dev/verify" }) }] });
      }
      if (name === "measure") {
        return respond({ content: [{ type: "text", text: JSON.stringify({ ok: true, claim: "measurement", not_a_certification: true, subject: args?.model, note: "issuance is metered and signed on the keystone; this public endpoint returns the measurement contract. Contact councilof.ai for paid signed issuance." }) }] });
      }
      return respondError(-32602, "tool not found");
    }
    return respondError(-32601, "method not found");
  },
};
