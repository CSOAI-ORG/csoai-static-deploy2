/**
 * /api/instruments — the EUNOMIA routing-table catalog (agent-discoverable).
 *
 * The "instruments" are the routable governance objects. This returns counts +
 * the class map (with eunomia:// URIs) + the live schema — the thing an agent
 * curls to discover the Council OS in seconds. 291 MCP · 15 hive · 13 axes.
 *
 * Measurement, not certification.
 */
import lookupData from '../../lookup-public.json';
import regulationFeed from '../../regulation-feed.json';
import benchmarkQualityFeed from '../../benchmark-quality-feed.json';
import registersData from '../../registers-data.json';
import estateBoard from '../../estate-board.json';

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,OPTIONS', 'access-control-allow-headers': 'Content-Type' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method !== 'GET') return new Response(JSON.stringify({ error: 'GET only' }), { status: 405, headers });

  const models = Object.keys(lookupData.models || {});
  const regs = regulationFeed.regulations || [];
  const benches = benchmarkQualityFeed.records || [];
  const regs2 = registersData.registers || {};

  const classes = [
    ['model', 'measured open-weight models', models.length, 'eunomia://model/<name>'],
    ['regulation', 'regimes, CELEX-keyed', regs.length, 'eunomia://regulation/<id>'],
    ['benchmark', 'third-party benchmark quality', benches.length, 'eunomia://benchmark/<name>'],
    ['register', 'signed Ed25519 registers', Object.keys(regs2).length, 'eunomia://register/<name>'],
    ['bridge', 'Layer-0 legacy/financial bridges', 15, 'eunomia://bridge/<proto>'],
    ['axis', 'governance axes', 13, 'eunomia://axis/<axis>'],
    ['sector', 'routable sectors (sign-all)', 6, 'eunomia://sector/<sector>'],
  ];

  return new Response(JSON.stringify({
    schema: 'csoai.instruments/0.1',
    counts: { mcp: 291, hive: 15, axes: 13, models: models.length, regulations: regs.length, benchmarks: benches.length, registers: Object.keys(regs2).length },
    classes: classes.map(([kind, desc, n, uri]) => ({ kind, desc, count: n, uri })),
    route_scheme: 'eunomia://<class>[/<id>]',
    headline: '291 rules, one sign · measurement, not certification',
    board_stamp: estateBoard.board_stamp || estateBoard.board?.board_stamp || null,
    examples: [
      'eunomia://model/nemotron-3-nano:30b',
      'eunomia://regulation/REG-001',
      'eunomia://bridge/iso20022',
      'eunomia://risk-oracle/x402',
    ],
    not_a_certification: true,
  }), { status: 200, headers });
}
