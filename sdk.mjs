/* @csoai/sdk — the Council OS app SDK.
 *
 * ONE import from any app/agent/website. No auth wall, no sales call, no key.
 * Every method returns a signed, did:web-resolvable object (measurement, not
 * certification). The isValid() helper recomputes content_id and checks the
 * Ed25519 signature WITHOUT trusting us — the stranger-verification door.
 *
 *   import { csoai } from './sdk.mjs';
 *   const board = await csoai.board();
 *   const card  = await csoai.attest({ sector:'bond', subject:'UK Gilt' });
 *   const ok    = await csoai.isValid(card);   // recompute + Ed25519, no trust
 *
 * BOUNDARY (doctrine): an attestation is an independent, verifiable OPINION/MEASUREMENT
 * about an asset. It NEVER tokenizes that asset, NEVER confers ownership or claim
 * rights, and is NOT itself a token. It rides alongside an instrument. We are the
 * measurement layer, never the issuer. We licence attestation infra white-label;
 * we never mint or tokenize anyone's assets.
 */
const H = 'https://csoai-gspc.pages.dev';
const GET = async (u) => {
  const r = await fetch(H + u);
  if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + u);
  return r.json();
};
const POST = async (u, b) => {
  const r = await fetch(H + u, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(b) });
  if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + u);
  const d = await r.json();
  // write/measure endpoints return {summary, card} — hand the caller the card
  // directly so it is ready for isValid(). Preserve both on the card for breadth.
  if (d && d.card) return d.card;
  return d;
};

// ---- offline content_id recompute (RFC 8785 canonical JSON, same as /api/verify) ----
function canon(o) {
  if (o === null) return 'null';
  if (o === true) return 'true';
  if (o === false) return 'false';
  if (typeof o === 'string') return JSON.stringify(o);
  if (typeof o === 'number') return Number.isFinite(o) ? String(o) : '0';
  if (Array.isArray(o)) return '[' + o.map(canon).join(',') + ']';
  if (typeof o === 'object') return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}';
  return 'null';
}
async function sha256hex(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('');
}
function b64bytes(b64) { return Uint8Array.from(atob(b64), c => c.charCodeAt(0)); }
// multibase base58btc → raw pubkey bytes (Ed25519VerificationKey2020)
function b58dec(s) {
  const AL = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
  s = String(s).replace(/^z/, '');
  let n = 0n; for (const c of s) n = n * 58n + BigInt(AL.indexOf(c));
  const b = []; while (n > 0n) { b.push(Number(n & 255n)); n >>= 8n; }
  return new Uint8Array(b.reverse());
}

export const csoai = {
  // ---- read surfaces (signed) ----
  board: () => GET('/api/gspc'),
  instruments: () => GET('/api/instruments'),
  registers: () => GET('/api/registers'),
  route: (uri) => GET('/api/route?uri=' + encodeURIComponent(uri)),
  signal: (axis = 'gov', jur = 'EU') => GET('/api/signal?axis=' + axis + '&jurisdiction=' + jur),
  sovSignal: () => GET('/api/sov-signal'),
  deadline: () => GET('/api/regulation'),
  chain: (head, n = 10) => GET('/api/chain' + (head ? '?head=' + head + '&n=' + n : '?n=' + n)),
  measureAxis: (axis = 'gov') => GET('/api/measure-axis?axis=' + encodeURIComponent(axis)),
  firstFine: () => GET('/api/first-fine'),
  receipts: () => GET('/api/receipts'),
  methodology: () => GET('/api/methodology'),
  integrityReport: () => GET('/api/report-benchmark-integrity'),

  // ---- write/measure (signed cards) ----
  attest: (obj) => POST('/api/attest', obj),
  dvp: (obj) => POST('/api/dvp', obj),
  underwrite: (obj) => POST('/api/underwrite', obj),
  crosswalk: (obj) => POST('/api/crosswalk', obj),
  cobol: (obj) => POST('/api/cobol', obj),
  sign: (digest) => POST('/api/sign', { digest }),

  // ---- verify (server) ----
  verify: (card) => POST('/api/verify', card),

  // ---- STRANGER-VERIFY (offline, trusts only did:web) ----
  // 1) recompute content_id from the canonical body (strip server/meta fields)
  // 2) resolve did:web → pubkey (Ed25519VerificationKey2020, multibase)
  // 3) check the Ed25519 signature. No trust in us required.
  async isValid(card) {
    try {
      const body = { ...card };
      for (const k of ['content_id', 'signature', 'pubkey', 'prev', 'key_id', 'verification_method', 'did_resolver']) delete body[k];
      const recomputed = await sha256hex(canon(body));
      if (recomputed !== card.content_id) return { valid: false, why: 'content_id mismatch' };

      const didHost = card.key_id
        ? String(card.key_id).replace('did:web:', '').split('#')[0]
        : 'csoai-gspc.pages.dev';
      const doc = await (await fetch('https://' + didHost + '/.well-known/did.json')).json();
      const vm = (doc.verificationMethod || []).find(x => x.id === (card.key_id || doc.id + '#gspc'));
      if (!vm) return { valid: false, why: 'no verificationMethod' };
      // support both Ed25519VerificationKey2020 (multibase) and JsonWebKey2020 (publicKeyJwk)
      const pubraw = vm.publicKeyJwk ? jwkX(vm.publicKeyJwk) : b58dec(vm.publicKeyMultibase || '');
      if (!pubraw.length) return { valid: false, why: 'unsupported key format' };
      const pub = await crypto.subtle.importKey('raw', pubraw, { name: 'Ed25519' }, true, ['verify']);
      const ok = await crypto.subtle.verify('Ed25519', pub, b64bytes(card.signature), new TextEncoder().encode(card.content_id));
      return { valid: ok, why: ok ? 'stranger-verified via ' + card.key_id : 'bad signature' };
    } catch (e) {
      return { valid: false, why: String(e) };
    }
  },
};

// helper: if a did doc publishes publicKeyJwk (OKP/Ed25519), decode x → raw bytes
function jwkX(jwk) {
  if (jwk && jwk.crv === 'Ed25519' && jwk.x) {
    const b = atob(jwk.x);
    return new Uint8Array([...b].map(c => c.charCodeAt(0)));
  }
  return new Uint8Array(0);
}

export default csoai;
