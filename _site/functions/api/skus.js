export async function onRequestGet(context) {
  const skus = {
    register: "measurement and attestation only — no certification, accreditation, or enforcement authority",
    currency: "GBP",
    generated: new Date().toISOString(),
    skus: [
      {
        id: "passport-free",
        name: "Article 50 Signed Passport",
        price: 0,
        unit: "one-time",
        description: "Free signed provenance passport for AI-generated content. Ed25519-signed, verifiable offline.",
        endpoint: "https://csoai.org/tools/article50-passport.html"
      },
      {
        id: "leaderboard-read",
        name: "Measured Results Readout",
        price: 0,
        unit: "per-call",
        description: "Measured benchmark results in official lm-eval-harness format. Frozen splits, published CIs.",
        endpoint: "https://csoai.org/api/leaderboard"
      },
      {
        id: "attestation-pack",
        name: "Attestation Pack",
        price: 299,
        unit: "per-month",
        description: "Signed evidence packs for EU AI Act technical documentation. Measured results, signed artefacts, corpus-watch re-fire on provision change.",
        status: "waitlist"
      },
      {
        id: "enterprise-measurement",
        name: "Enterprise Measurement Lane",
        price: null,
        unit: "annual",
        description: "Custom frozen-split measurement programmes. Priced on scope.",
        status: "contact"
      }
    ]
  };
  return new Response(JSON.stringify(skus, null, 2), {
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
  });
}
