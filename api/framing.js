// sovereign-framing-mcp — Programmatic access to the DEFONEOS framing library
// GET  /api/framing?format=json&topic=any — return all framin frames as JSON
// GET  /api/framing?format=quote-cards — single-line shortcuts for press/distribution
// GET  /api/framing?format=markdown — formatted markdown suitable for embedding
//
// HONESTY: Each frame is attributed to CSOAI canon with canonical URL. Frames are
// freely usable with attribution; off-the-record requires explicit request.

const FRAMES = [
  {
    id: 'one-line-cmmc',
    format: '1-line',
    topic: 'positioning',
    text: 'CA3O is the CMMC for AI.',
    attribution: 'CSOAI Charter, ratified 1795→2026',
    permalink: '/defoneos-framing#one-line-cmmc',
    permission: 'freely-usable',
  },
  {
    id: 'one-line-cheaper',
    format: '1-line',
    topic: 'pricing',
    text: 'DEFONEOS delivers sovereign defence AI at 94-98% cheaper than Palantir. Same outcomes, different substrate.',
    attribution: '5-year TCO comparison: £285K (DEFONEOS) vs £4.9M (Palantir) · /defoneos-cost-comparison',
    permalink: '/defoneos-framing#one-line-cheaper',
    permission: 'freely-usable',
  },
  {
    id: 'one-line-substrate',
    format: '1-line',
    topic: 'substrate',
    text: 'DEFONEOS is the sovereign AI substrate UK + EU + AUKUS defence primes turn to for EU AI Act compliance, SIGIL-signed audit trails, and a kill-switch that actually works.',
    attribution: 'CSOAI Sovereign Substrate canon',
    permalink: '/defoneos-framing#one-line-substrate',
    permission: 'freely-usable',
  },
  {
    id: 'paragraph-sovereign-by-construction',
    format: 'paragraph',
    topic: 'sovereignty',
    text: 'A sovereign AI substrate is more than hosted-in-UK compute. Sovereignty is constitutional: it means Charter Article 0 binding (no equity, no board seats, no success fees — capture-proof by math, not by contract), BFT 23/33 council governance, Ed25519-signed SIGIL chain, 7 protocol-enforced red lines, and a Fork Doctrine.',
    attribution: 'CSOAI Sovereign Substrate canon, ratified 2026',
    permalink: '/defoneos-framing#paragraph-sovereign',
    permission: 'freely-usable',
  },
  {
    id: 'paragraph-procurement-window',
    format: 'paragraph',
    topic: 'procurement',
    text: 'EU AI Act enforcement: T-27 days. UK JSP 936 / DSEC: forcing assurance on autonomy deployments now. NATO Autonomy Policy: meaningful human control required. AUKUS Pillar 2: £3.5B over 5 years for sovereign AI cooperation.',
    attribution: 'CSOAI procurement forecast, July 2026',
    permalink: '/defoneos-framing#paragraph-procurement',
    permission: 'freely-usable',
  },
  {
    id: 'paragraph-red-lines',
    format: 'paragraph',
    topic: 'care-floor',
    text: 'DEFONEOS will not enable kinetic-targeting patterns, individual surveillance, civilian harm optimisation, sovereignty violation, auto-escalation, lying to humans, or irreversibility without confirmation. The 7 protocol-enforced red lines are the strength, not the weakness.',
    attribution: 'CSOAI Care Floor + Hard Stops doctrine, 2026',
    permalink: '/defoneos-framing#paragraph-red-lines',
    permission: 'freely-usable',
  },
  {
    id: 'paragraph-always-on',
    format: 'paragraph',
    topic: 'operational',
    text: 'The substrate runs. The OOWM loops. The 4 alignment tests gate every action. The 6 NNs learn. The 33 agents deliberate. The 12 mindsets read. The SIGIL chain witnesses. Forever.',
    attribution: 'SOV3³ reference, /sov3-oowm-all-models',
    permalink: '/defoneos-framing#paragraph-always-on',
    permission: 'freely-usable',
  },
  {
    id: 'paragraph-iso-fee',
    format: 'paragraph',
    topic: 'governance',
    text: 'CSOAI\'s Charter Article 0 binds us to ISO fee-for-service only. No equity, no board seats, no success fees. Capture-proof by math, not by contract. The sovereign substrate remains available to any party willing to procure, even those whose commercial terms the founders may otherwise dislike.',
    attribution: 'CSOAI Charter Article 0',
    permalink: '/defoneos-framing#paragraph-iso-fee',
    permission: 'freely-usable',
  },
  {
    id: 'paragraph-fork-doctrine',
    format: 'paragraph',
    topic: 'forkability',
    text: 'Anyone can fork DEFONEOS. The fork is sovereign. The fork inherits Charter Article 0 + Care Floor 0.95 + BFT 23/33 + SIGIL chain + DORADO 1-click + EU AI Act compliance evidence + Crown Authorisation lineage + MIT licence. This is not a vendor dependency.',
    attribution: 'CSOAI Fork Doctrine, 2026',
    permalink: '/defoneos-framing#paragraph-fork',
    permission: 'freely-usable',
  },
];

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 'public, max-age=600');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'method not allowed' });

  const format = (req.query.format || 'json').toString();
  const topic = (req.query.topic || '').toString();
  let frames = FRAMES;
  if (topic) frames = frames.filter(f => f.topic === topic);

  if (format === 'quote-cards') {
    return res.status(200).json({ format: 'quote-cards', count: frames.length, items: frames });
  }
  if (format === 'markdown') {
    let md = '# DEFONEOS Framing Library\n\n';
    md += '> Citation-ready framings. SIGIL-backed. Freely usable with attribution.\n\n';
    for (const f of frames) {
      md += `## ${f.id} (${f.format} · ${f.topic})\n\n`;
      md += `> ${f.text}\n\n`;
      md += `*— ${f.attribution}*\n\n`;
      md += `Source: https://csoai-sovereign.pages.dev${f.permalink}\n\n---\n\n`;
    }
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    return res.status(200).send(md);
  }

  return res.status(200).json({
    name: 'sovereign-framing-mcp',
    version: '1.0.0',
    description: 'Programmatic access to DEFONEOS sovereign framing library. Verbatim quotes, citation recipes, attribution defaults.',
    topic_filter: topic || 'none',
    frames,
    usage: 'GET /api/framing?format=json (default) | quote-cards | markdown  · topic=any|positioning|pricing|substrate|sovereignty|procurement|care-floor|operational|governance|forkability',
    timestamp: new Date().toISOString(),
  });
};
