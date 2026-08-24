/**
 * /api/cobol — the proof of weave (Open 1, live).
 *
 * Reads one COBOL COPYBOOK (a batch record layout) and emits one JSON schema
 * plus the routable `eunomia://bridge/cobol` URI. This is the atomic unit that
 * turns a legacy batch instruction into a routable, attesteable A2A object.
 *
 *   POST {copybook}  → { fields:[...], schema:{...}, route }
 *   GET              → schema + example
 *
 * Measurement, not certification. Deterministic, offline, no LLM in the parse.
 */

const FIELD_RE = /^\s*(\d+)\s+([A-Z0-9][A-Z0-9-]*)\s+PIC\s+([A-Z0-9()V]+)\s*\.?\s*$/i;

function parseCopybook(text) {
  const fields = [];
  for (const line of String(text || '').split('\n')) {
    const m = FIELD_RE.exec(line);
    if (!m) continue;
    const level = parseInt(m[1], 10);
    const name = m[2];
    const pic = m[3];
    const numeric = pic.indexOf('9') >= 0;
    const digits = (pic.match(/\d+/g) || []).reduce((a, b) => a + parseInt(b, 10), 0);
    fields.push({ field: name, level, pic, type: numeric ? 'number' : 'string', width: digits || null, signed: pic.startsWith('S') });
  }
  return fields;
}

function toJsonSchema(fields) {
  const properties = {};
  const required = [];
  for (const f of fields) {
    properties[f.field] = { type: f.type, description: 'PIC ' + f.pic };
    if (f.level <= 0) required.push(f.field);
  }
  return { '$schema': 'https://json-schema.org/draft/2020-12/schema', title: 'COPYBOOK-batch', type: 'object', properties, required };
}

export async function onRequest(context) {
  const headers = { 'content-type': 'application/json', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'GET,POST,OPTIONS', 'access-control-allow-headers': 'Content-Type' };
  if (context.request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
  if (context.request.method === 'GET') {
    return new Response(JSON.stringify({ schema: 'csoai.cobol-bridge/0.1', example: 'POST {"copybook":"01 SETTLEMENT-RECORD.\\n  10 SETTLE-DATE PIC X(8).\\n  10 NOTIONAL PIC 9(12)V99."}', not_a_certification: true }), { status: 200, headers });
  }
  if (context.request.method !== 'POST') return new Response(JSON.stringify({ error: 'POST or GET only' }), { status: 405, headers });

  let body;
  try { body = await context.request.json(); } catch (e) { return new Response(JSON.stringify({ error: 'invalid JSON' }), { status: 400, headers }); }
  if (!body.copybook) return new Response(JSON.stringify({ error: 'need copybook' }), { status: 400, headers });

  const fields = parseCopybook(body.copybook);
  const schema = toJsonSchema(fields);
  return new Response(JSON.stringify({
    fields,
    schema,
    route: 'eunomia://bridge/cobol',
    note: 'COPYBOOK → JSON schema. The atomic unit of the bond router. Measurement, not certification.',
    next: 'POST this schema as the object to /api/attest to sign + chain it.',
  }), { status: 200, headers });
}
