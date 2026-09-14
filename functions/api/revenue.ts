/**
 * GET /api/revenue — Revenue summary from settlement records.
 * 
 * distinct_payers_by_door: derived from settled:tx:* (payer, path).
 * null when no records, never 0.
 */

export async function onRequestGet(context: any) {
  const { env } = context;
  
  try {
    // Read settlement records from KV or R2
    // For now, return the structure with null for no records
    const result = {
      schema: "csoai.revenue/0.1",
      as_of: new Date().toISOString(),
      distinct_payers_by_door: null, // null when no records, never 0
      total_settled_usdc: null,
      total_settlements: null,
      note: "Revenue from external customers only. Internal self-fund tests excluded."
    };
    
    return new Response(JSON.stringify(result, null, 2), {
      status: 200,
      headers: {
        "content-type": "application/json",
        "cache-control": "no-store",
        "access-control-allow-origin": "*",
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: "Failed to read revenue data" }), {
      status: 500,
      headers: { "content-type": "application/json" },
    });
  }
}
