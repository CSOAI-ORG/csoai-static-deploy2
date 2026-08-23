'use strict';

// Vercel serverless — £0 distributed training dispatcher
// POST /api/train-distributed
//
// Body: { model: 'sov33_small'|'sov33_large', dataset: string,
//         epochs: integer, tabs: ['tab1', ...] }
//
// The dispatcher produces a balanced, SIGIL-receipted shard manifest and
// records it to the ephemeral queue at /tmp/free-gpu-jobs.jsonl. This endpoint
// does not falsely claim that third-party notebook runtimes were started:
// `status: queued` means the manifest is ready for free worker agents to claim.

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;
const { FLEET, sigilFor } = require('./free-gpu-orchestrator');

const JOB_LOG = process.env.FREE_GPU_JOB_LOG || '/tmp/free-gpu-jobs.jsonl';
const ALLOWED_MODELS = new Set(['sov33_small', 'sov33_large']);
const TAB_MAP = new Map(FLEET.map(tab => [tab.tab_id, tab]));
const DATASET_PATTERN = /^[a-zA-Z0-9][a-zA-Z0-9._/-]{0,127}$/;

const MODEL_PROFILES = Object.freeze({
  sov33_small: {
    base_eta_seconds_per_epoch: 2700,
    minimum_vram_gb: 0,
    strategy: 'data-parallel QLoRA adapters; weighted shard manifest',
    default_batch_tokens: 2048,
  },
  sov33_large: {
    base_eta_seconds_per_epoch: 9600,
    minimum_vram_gb: 0,
    strategy: 'adapter-only/gradient shard training; no full-weight replication',
    default_batch_tokens: 1024,
  },
});

function parseBody(body) {
  if (typeof body === 'string') {
    try { return JSON.parse(body); } catch { return {}; }
  }
  return body && typeof body === 'object' && !Array.isArray(body) ? body : {};
}

function validate(body) {
  const errors = [];
  const model = String(body.model || '').toLowerCase();
  const dataset = String(body.dataset || '').trim();
  const epochs = Number(body.epochs);
  const tabs = Array.isArray(body.tabs) ? body.tabs.map(value => String(value).toLowerCase()) : [];

  if (!ALLOWED_MODELS.has(model)) errors.push('model must be sov33_small or sov33_large');
  if (!DATASET_PATTERN.test(dataset)) {
    errors.push('dataset must be a 1-128 character name using letters, numbers, dot, slash, underscore, or hyphen');
  }
  if (!Number.isInteger(epochs) || epochs < 1 || epochs > 100) errors.push('epochs must be an integer from 1 to 100');
  if (!tabs.length) errors.push('tabs must contain at least one tab_id');
  if (tabs.length > FLEET.length) errors.push(`tabs may contain at most ${FLEET.length} tab_ids`);
  if (new Set(tabs).size !== tabs.length) errors.push('tabs must not contain duplicates');
  const unknown = tabs.filter(tabId => !TAB_MAP.has(tabId));
  if (unknown.length) errors.push(`unknown tab_ids: ${unknown.join(', ')}`);

  return { errors, model, dataset, epochs, tabs };
}

function apportionShards(tabIds) {
  const workers = tabIds.map(tabId => TAB_MAP.get(tabId));
  const totalWeight = workers.reduce((sum, tab) => sum + tab.compute_weight, 0);
  let cursor = 0;

  return workers.map((tab, index) => {
    const start = cursor;
    const end = index === workers.length - 1
      ? 10000
      : Math.min(10000, cursor + Math.round((tab.compute_weight / totalWeight) * 10000));
    cursor = end;
    return {
      shard_id: `shard-${String(index + 1).padStart(2, '0')}`,
      tab_id: tab.tab_id,
      provider: tab.provider,
      gpu_type: tab.gpu_type,
      vram_gb: tab.vram_gb,
      role: tab.role,
      sample_range_bps: [start, end],
      dataset_fraction: Number(((end - start) / 10000).toFixed(4)),
      compute_weight: tab.compute_weight,
      state: 'queued_for_worker_claim',
    };
  });
}

function estimateEta(model, epochs, selectedTabs) {
  const profile = MODEL_PROFILES[model];
  const parallelWeight = selectedTabs.reduce((sum, tabId) => sum + TAB_MAP.get(tabId).compute_weight, 0);
  const coordinationPenalty = 1 + Math.max(0, selectedTabs.length - 1) * 0.035;
  const oracleOnlyPenalty = selectedTabs.every(tabId => TAB_MAP.get(tabId).vram_gb === 0) ? 4 : 1;
  return Math.max(60, Math.ceil((profile.base_eta_seconds_per_epoch * epochs * coordinationPenalty * oracleOnlyPenalty) / parallelWeight));
}

async function appendJob(record) {
  try {
    await fsp.appendFile(JOB_LOG, `${JSON.stringify(record)}\n`, { mode: 0o600 });
    return true;
  } catch {
    return false;
  }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Sovereign-Budget', 'GBP-0');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') {
    return res.status(405).json({
      status: 'method_not_allowed',
      error: 'POST required',
      sigil: null,
      timestamp: new Date().toISOString(),
    });
  }

  const body = parseBody(req.body);
  const { errors, model, dataset, epochs, tabs } = validate(body);
  const timestamp = new Date().toISOString();

  if (errors.length) {
    return res.status(400).json({
      status: 'invalid_payload',
      errors,
      allowed_tabs: FLEET.map(tab => tab.tab_id),
      sigil: null,
      timestamp,
    });
  }

  const shardsAssigned = apportionShards(tabs);
  const etaSeconds = estimateEta(model, epochs, tabs);
  const idMaterial = `${model}|${dataset}|${epochs}|${tabs.join(',')}|${timestamp}|${crypto.randomBytes(8).toString('hex')}`;
  const jobId = `train-${crypto.createHash('sha256').update(idMaterial).digest('hex').slice(0, 16)}`;
  const profile = MODEL_PROFILES[model];

  const manifest = {
    status: 'queued',
    job_id: jobId,
    model,
    dataset,
    epochs,
    shards_assigned: shardsAssigned,
    eta_seconds: etaSeconds,
    strategy: profile.strategy,
    batch_tokens_per_worker: profile.default_batch_tokens,
    checkpoint_policy: 'adapter checkpoint after every epoch; merge only after all shard receipts verify',
    budget_gbp: 0,
    timestamp,
  };
  const sigil = sigilFor(manifest);
  const stored = await appendJob({ ...manifest, sigil });

  return res.status(200).json({
    ...manifest,
    sigil,
    sigil_algorithm: process.env.FREE_GPU_SIGIL_SECRET ? 'HMAC-SHA256' : 'SHA-256 content receipt',
    queue_persistence: stored ? 'ephemeral_serverless_log' : 'response_receipt_only',
    execution_claim: 'Manifest queued for worker claim. This response does not assert that Modal, Kaggle, Colab, Ollama, or Oracle workers have started.',
    worker_contract: {
      claim: `GET /api/free-gpu-orchestrator then claim ${jobId} by tab_id`,
      checkpoint: `${dataset}/${jobId}/<tab_id>/epoch-<n>.adapter`,
      completion_receipt: 'worker must publish checkpoint hash + samples_processed + runtime_seconds',
    },
  });
};

module.exports.apportionShards = apportionShards;
module.exports.estimateEta = estimateEta;
