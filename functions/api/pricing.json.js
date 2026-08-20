// Cloudflare Pages Function — /api/pricing.json (the ONE canonical pricing surface, RULING-2026-08-20).
// Empty tiers until a lane wires the 402 layer; the surface exists so the guard allowlist has a target.
const PRICING = {
  "schema": "csoai.pricing/0.1",
  "ruling": "RULING-2026-08-20-AGENT-PAYG",
  "updated": "2026-08-20T05:30:00Z",
  "policy": "machine-access fees only (data endpoints, relying-party agents). Money buys access, never standing. The measured set pays nothing, ever. Humans pay nothing. See /api/corrections for reversals.",
  "free_tier": "everything, rate-limited",
  "paid_tier": "same everything, faster + heavier \u2014 per-call fees above the free limit",
  "tiers": [],
  "signature": {
    "protected": "eyJhbGciOiJFZERTQSIsImtpZCI6ImRpZDp3ZWI6Y3NvYWkub3JnI3NpdGUtcmVsZWFzZS0xIiwidHlwIjoiSldUIn0",
    "contentId": "8765b38fe9b2906ea66e3b850f45597a7b7bf6a1de90f986a4c6b01d83501d78",
    "signature": "MKbo_U4lQcjdW0zfrWM4O5O3guhy0sHC9xH_rNpyBw09A4wm4elu_5L_INaRrrZ6dfWUBXrAvzGTYrYy75qHAQ"
  }
};

export async function onRequest(context) {
  return new Response(JSON.stringify(PRICING, null, 2), { headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "public, max-age=300" } });
}
