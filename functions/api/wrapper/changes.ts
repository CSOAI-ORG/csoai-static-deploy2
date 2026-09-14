/**
 * GET /api/wrapper/changes?id=<pair> — Delta of wrapped supply and escrow since previous ledger as_of.
 * 
 * 402 via buildPaymentRequiredV2 + declareBazaarHttpGet.
 * &preview=1 free.
 * Price only in the 402.
 */

export async function onRequestGet(context: any) {
  const { request, env } = context;
  const url = new URL(request.url);
  const id = url.searchParams.get("id");
  const preview = url.searchParams.get("preview") === "1";
  
  if (!id) {
    return new Response(JSON.stringify({ error: "Missing id parameter" }), {
      status: 400,
      headers: { "content-type": "application/json" },
    });
  }
  
  // Preview mode is free
  if (preview) {
    return new Response(JSON.stringify({
      schema: "csoai.wrapper.changes/0.1",
      id: id,
      preview: true,
      note: "Preview mode. Full data requires payment.",
      wrapped_supply_delta: null,
      escrow_delta: null,
      previous_as_of: null,
      current_as_of: null,
    }, null, 2), {
      status: 200,
      headers: {
        "content-type": "application/json",
        "cache-control": "no-store",
        "access-control-allow-origin": "*",
      },
    });
  }
  
  // Paid mode - return 402 with payment required
  return new Response(JSON.stringify({
    x402Version: 2,
    error: "Payment required",
    accepts: [{
      scheme: "exact",
      network: "eip155:8453",
      resource: request.url,
      description: `Wrapped asset changes for ${id}`,
      mimeType: "application/json",
      outputSchema: { type: "object" },
      maxTimeoutSeconds: 300,
      extra: { name: "USDC", version: "2" }
    }],
    extensions: {
      bazaar: {
        listed: true,
        description: `Delta of wrapped supply and escrow for ${id} since previous ledger`,
      }
    }
  }, null, 2), {
    status: 402,
    headers: {
      "content-type": "application/json",
      "x-payment-required": "true",
    },
  });
}
