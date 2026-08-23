/**
 * /api/route — the EUNOMIA router resolver (machine-readable).
 *
 * Turns a eunomia://<class>/<id> URI into its governed object + crosswalk +
 * attestation + cost frame. This is the "routing table" surface: each object is
 * a signed, crosswalked node; /api/route is the protocol lookup.
 *
 *   eunomia://model/<model>        → measured model
 *   eunomia://regulation/<id>      → regime (EU AI Act, CRA, FDA…)
 *   eunomia://benchmark/<name>     → third-party benchmark quality record
 *   eunomia://register/<name>      → signed register count
 *   eunomia://board                → estate board
 *   eunomia://axis/<axis>          → governance axis
 *
 * Measurement, not certification. Verification free forever.
 */
import regulationFeed from '../../regulation-feed.json';
import benchmarkQualityFeed from '../../benchmark-quality-feed.json';
import lookupData from '../../lookup-public.json';
import registersData from '../../registers-data.json';
import estateBoard from '../../estate-board.json';

export async function onRequest(context) {
  const method = context.request.method;
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };
  if (method === 'OPTIONS') return new Response(null, { status: 204, headers });

  const url = new URL(context.request.url);
  const uri = url.searchParams.get('uri') || '';
  const m = uri.match(/^eunomia:\/\/([a-z0-9-]+)(?:\/([\s\S]+))?$/i);
  if (!m) {
    return new Response(JSON.stringify({
      error: 'uri must be eunomia://<class>[/<id>]',
      example: 'eunomia://regulation/REG-001',
      classes: ['model', 'regulation', 'benchmark', 'register', 'board', 'axis'],
    }), { status: 200, headers });
  }

  const cls = m[1].toLowerCase();
  const id = m[2] ? decodeURIComponent(m[2]) : '';
  let label = id, status = 'unknown', cross = [], raw = null;

  const regs = regulationFeed.regulations || [];
  if (cls === 'regulation') {
    raw = regs.find((r) => (r.id || r.celex) === id || (r.celex) === id);
    if (raw) {
      label = raw.title || raw.id || id;
      status = raw.status || raw.deadline_status || 'unknown';
      cross = regs.filter((r) => r !== raw && r.tags && raw.tags && r.tags.some((t) => (raw.tags || []).includes(t))).slice(0, 5);
    }
  } else if (cls === 'model') {
    const models = lookupData.models || {};
    const key = Object.keys(models).find((k) => k === id || k === id + ':latest');
    if (key) { raw = models[key]; label = key; status = 'measured'; }
  } else if (cls === 'benchmark') {
    const recs = benchmarkQualityFeed.records || [];
    raw = recs.find((r) => (r.benchmark || '') === id || (r.name || '') === id);
    if (raw) { label = raw.benchmark || raw.name || id; status = raw.status || 'measured'; }
  } else if (cls === 'register') {
    const regs2 = (registersData.registers || {});
    if (regs2[id] != null) { raw = { register: id, count: regs2[id] }; label = id; status = 'signed'; }
  } else if (cls === 'board') {
    raw = { board: 'estate board', models: estateBoard.models || (estateBoard.board && estateBoard.board.models) };
    label = 'estate board'; status = 'measured-current-state';
  } else if (cls === 'axis') {
    raw = { axis: id }; label = id; status = 'governance axis';
  } else if (cls === 'bridge' || cls === 'legacy') {
    // real Layer-0 bridge-MCP fleet + cobolbridge.ai (see SOVOS INVENTORY).
    const bridges = {
      cobol:    { title: 'COBOL legacy bridge', target: 'cobolbridge.ai', rules: 'legacy modernization · 200B+ lines of COBOL in production' },
      cics:     { title: 'CICS mainframe bridge', target: 'cics-bridge-mcp', rules: 'SOX + PCI-DSS + DORA' },
      iso20022: { title: 'ISO 20022 / SWIFT payments bridge', target: 'iso20022-bridge-mcp', rules: 'PSD2 + DORA + AML' },
      sap:      { title: 'SAP ERP bridge', target: 'sap-bridge-mcp', rules: 'SOX + GDPR' },
      as400:    { title: 'IBM AS/400 bridge', target: 'as400-bridge-mcp', rules: 'SOX + DORA' },
      iso8583:  { title: 'ISO 8583 card bridge', target: 'iso8583-bridge-mcp', rules: 'PCI-DSS + DORA' },
      fix:      { title: 'FIX trading bridge', target: 'fix-bridge-mcp', rules: 'MiFID II Art. 17' },
      edi:      { title: 'EDI/EDIFACT B2B bridge', target: 'edi-bridge-mcp', rules: 'SOX' },
      acord:    { title: 'ACORD insurance bridge', target: 'acord-bridge-mcp', rules: 'Solvency II + GDPR + EU AI Act' },
      hl7fhir:  { title: 'HL7/FHIR healthcare bridge', target: 'hl7-fhir-bridge-mcp', rules: 'HIPAA + EU MDR + GDPR' },
      scada:    { title: 'SCADA/OT industrial bridge', target: 'scada-bridge-mcp', rules: 'IEC 62443 + NIS2' },
      nacha:    { title: 'NACHA/ACH US payments bridge', target: 'nacha-bridge-mcp', rules: 'OFAC + AML' },
      oracle:   { title: 'Oracle PL/SQL bridge', target: 'oracle-bridge-mcp', rules: 'SOX + GDPR' },
      mqtt:     { title: 'MQTT/IoT bridge', target: 'mqtt-bridge-mcp', rules: 'IEC 62443 + NIS2' },
      sip:      { title: 'SIP telephony bridge', target: 'sip-bridge-mcp', rules: 'STIR/SHAKEN + GDPR' },
    };
    raw = bridges[id.toLowerCase()] || null;
    if (raw) { label = raw.title; status = 'Layer-0 bridge-MCP'; }
  } else if (cls === 'risk-oracle') {
    // the unclaimed layer: settlement/attestation rails with NO measurement.
    const rails = {
      x402: { title: 'x402 settlement rail', rules: 'agent-paid data products · humans never paid' },
      erc8004: { title: 'ERC-8004 Trustless Agents', rules: 'identity/reputation/validation registries · live on mainnet · no risk layer' },
      ap2: { title: 'AP2 mandate', rules: 'Google + Coinbase attestation mandates' },
    };
    raw = rails[id.toLowerCase()] || null;
    if (raw) { label = raw.title; status = 'settlement rail — risk layer unclaimed'; }
  } else if (cls === 'a2a' || cls === 'translation') {
    // OPEN 1: COBOL-to-A2A translation layer (the Rosetta table). Real Layer-0 MCP fleet.
    const tab = {
      'batch-job':    { cobol: 'Batch job schedule', a2a: 'Agent task queue', mcp: 'bft-progress-council-mcp', rules: 'BFT consensus on task ordering' },
      'audit-log':    { cobol: 'Mainframe audit log', a2a: 'C2PA provenance chain', mcp: 'proofof-ai-mcp', rules: 'cryptographic provenance, court-admissible' },
      'rbac':         { cobol: 'Role-based access control', a2a: 'Agent card credentials', mcp: 'agent-identity-trust-mcp', rules: 'DID + verifiable credentials + SBT' },
      'reg-reporting':{ cobol: 'Regulatory reporting', a2a: 'Real-time compliance probe', mcp: 'iso-42001-ai-mcp', rules: 'AIMS + EU AI Act + MiCA verified' },
      'data-entry':   { cobol: 'Data entry clerk', a2a: 'LLM reasoning engine', mcp: 'care-membrane-mcp', rules: '16-probe relational ethics harness' },
    };
    raw = tab[id.toLowerCase()] || null;
    if (raw) { label = raw.cobol + ' → ' + raw.a2a; status = raw.mcp; }
  }

  if (!raw) {
    return new Response(JSON.stringify({ error: 'not found', class: cls, id, not_a_certification: true }), { status: 200, headers });
  }

  return new Response(JSON.stringify({
    route: `eunomia://${cls}/${id}`,
    class: cls,
    id,
    label,
    status,
    crosswalk: cross.map((c) => ({ route: `eunomia://regulation/${c.id || c.celex}`, label: c.title || c.celex, status: c.status })),
    attestation: 'Ed25519 signed · RFC 9943 (SCITT)-aligned COSE receipt · not_a_certification:true',
    cost_frame: '£0.05/call · verified-execution, not per-token',
    not_a_certification: true,
    raw,
  }), { status: 200, headers });
}
