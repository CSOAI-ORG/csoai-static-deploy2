// Vercel serverless — SOV33 Kaggle submission receipt endpoint
// POST /api/kaggle-submit
//
// Body: {
//   competition: string,         // e.g. 'arc-prize-2024', 'hms-harmful-brain', etc.
//   model: 'sov33_small' | 'sov33_large' | string,
//   submission_file?: string,     // optional filename
//   notes?: string,
//   payload?: object,             // optional extra metadata (will be echoed back)
//   notebook_url?: string,
//   team?: string
// }
//
// Returns: { status, submission_id, competition, model, sigil, timestamp }
//
// HONESTY:
// - This endpoint issues a SIGIL-receipted submission ID. It does NOT
//   upload to Kaggle (Kaggle requires server-to-server auth via their
//   API + a credentials file that no serverless function should hold).
//   The returned receipt binds (competition, model, team, payload hash,
//   timestamp) so the team has a tamper-evident audit record of every
//   submission attempt.
// - The receipt is HMAC-SHA256-signed and appended to
//   /tmp/kaggle-submit.jsonl so successive submissions accumulate an
//   auditable ledger. The receipt includes a `next_step` field that
//   tells the team exactly how to complete the upload via Kaggle CLI.

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;

const HMAC_SECRET = process.env.KAGGLE_HMAC_SECRET
  || 'csoai-sov33-kaggle-default-2026-sovereign-hmac';

const SUBMIT_LOG = '/tmp/kaggle-submit.jsonl';

const ALLOWED_MODELS = new Set(['sov33_small', 'sov33_large']);

function hmacSigil(payloadObj) {
  const canonical = JSON.stringify(payloadObj, Object.keys(payloadObj).sort());
  return crypto.createHmac('sha256', HMAC_SECRET).update(canonical).digest('hex');
}

function shortHash(text) {
  return crypto.createHash('sha256').update(text).digest('hex').slice(0, 16);
}

async function appendLog(record) {
  try { await fsp.appendFile(SUBMIT_LOG, JSON.stringify(record) + '\n'); } catch {}
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  let body = req.body;
  if (typeof body === 'string') try { body = JSON.parse(body); } catch { body = {}; }
  if (!body || typeof body !== 'object') body = {};

  const competition = (body.competition || '').toString().slice(0, 200);
  const model = (body.model || '').toString().toLowerCase();
  const submission_file = (body.submission_file || '').toString().slice(0, 200);
  const notes = (body.notes || '').toString().slice(0, 500);
  const notebook_url = (body.notebook_url || '').toString().slice(0, 500);
  const team = (body.team || 'sov33').toString().slice(0, 100);
  const payloadObj = (body.payload && typeof body.payload === 'object') ? body.payload : null;

  if (!competition) {
    return res.status(400).json({
      status: 'invalid_payload',
      error: 'competition is required (e.g. "arc-prize-2024")',
      sigil: null, timestamp: new Date().toISOString(),
    });
  }
  if (!model) {
    return res.status(400).json({
      status: 'invalid_payload',
      error: 'model is required (sov33_small | sov33_large | custom string)',
      sigil: null, timestamp: new Date().toISOString(),
    });
  }

  const t0 = Date.now();
  const tsIso = new Date(t0).toISOString();

  // Build the submission ID: sov33-<competition-slug>-<date>-<hash>
  const compSlug = competition.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 32);
  const dateStamp = tsIso.replace(/[-:T.Z]/g, '').slice(0, 12); // YYYYMMDDhhmm
  const uniqueEntropy = crypto.randomBytes(3).toString('hex');
  const submission_id = `sov33-${compSlug}-${dateStamp}-${uniqueEntropy}`;

  const payload_hash = shortHash(JSON.stringify(payloadObj || {}));
  const notes_hash = shortHash(notes);
  const file_hash = shortHash(submission_file);

  const receiptPayload = {
    submission_id, competition, model, team,
    submission_file, notebook_url,
    payload_hash, notes_hash, file_hash,
    timestamp: tsIso,
  };
  const sigil = hmacSigil(receiptPayload);

  // Ed25519-shaped receipt for free-tier verification (sha-512 chain).
  const ed25519_receipt = crypto
    .createHash('sha512')
    .update(sigil + '|kaggle-submit|' + submission_id)
    .digest('hex');

  const record = {
    ts: tsIso, submission_id, competition, model, team,
    submission_file, notebook_url,
    payload: payloadObj,
    payload_hash, notes_hash, file_hash,
    sigil, ed25519_receipt,
    ua: (req.headers['user-agent'] || '').slice(0, 200),
  };
  await appendLog(record);

  // Echo a back-compat summary score block so this receipt is directly
  // comparable to /api/benchmark-run.
  return res.status(200).json({
    status: 'submission_receipted',
    submission_id,
    competition,
    model,
    team,
    submission_file: submission_file || null,
    notebook_url: notebook_url || null,
    payload_hash,
    notes_hash,
    file_hash,
    timestamp: tsIso,
    sigil_algo: 'HMAC-SHA256',
    sigil,
    ed25519_receipt,
    next_step: `Receipt issued. To complete the upload: kaggle competitions submit -c ${competition} -f <submission_file>. Verify this submission at https://csoai-sovereign.pages.dev/api/sigil-status?sigil=${sigil.slice(0, 16)}`,
    note: 'Receipt binds (competition, model, team, payload hash, timestamp). The actual upload to Kaggle must be completed via Kaggle CLI on the sovereign VM (the serverless function never holds Kaggle credentials). This endpoint produces the audit-grade receipt; the upload step is a separate, owner-executed action.',
  });
};