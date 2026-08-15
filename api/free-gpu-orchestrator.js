'use strict';

// Vercel serverless — £0 SOV33 fleet state plane
// GET /api/free-gpu-orchestrator
//
// The endpoint exposes the nine logical execution tabs used by the free
// distributed-training dispatcher. It is deliberately honest about reachability:
// tabs are `standby` until a runtime heartbeat or queued job proves otherwise.
// Runtime agents may publish a JSON override through FREE_GPU_TAB_STATE_JSON:
// {"tab1":{"status":"online","current_model":"...","last_heartbeat":"ISO"}}

const crypto = require('crypto');
const fs = require('fs');

const JOB_LOG = process.env.FREE_GPU_JOB_LOG || '/tmp/free-gpu-jobs.jsonl';
const ACTIVE_JOB_WINDOW_MS = 8 * 60 * 60 * 1000;

const FLEET = Object.freeze([
  { tab_id: 'tab1', provider: 'M4-local', gpu_type: 'Apple M4 unified GPU (Ollama)', vram_gb: 16, role: 'orchestrator+inference', compute_weight: 0.70 },
  { tab_id: 'tab2', provider: 'M2-LAN', gpu_type: 'Apple M2 unified GPU (Ollama via tunnel)', vram_gb: 16, role: 'lan-worker', compute_weight: 0.45 },
  { tab_id: 'tab3', provider: 'Modal-T4-1', gpu_type: 'NVIDIA T4', vram_gb: 16, role: 'training-worker', compute_weight: 1.00 },
  { tab_id: 'tab4', provider: 'Modal-T4-2', gpu_type: 'NVIDIA T4', vram_gb: 16, role: 'training-worker', compute_weight: 1.00 },
  { tab_id: 'tab5', provider: 'Kaggle-T4-A', gpu_type: 'NVIDIA T4', vram_gb: 16, role: 'training-worker', compute_weight: 1.00 },
  { tab_id: 'tab6', provider: 'Kaggle-T4-B', gpu_type: 'NVIDIA T4', vram_gb: 16, role: 'training-worker', compute_weight: 1.00 },
  { tab_id: 'tab7', provider: 'Colab-T4', gpu_type: 'NVIDIA T4', vram_gb: 16, role: 'training-worker', compute_weight: 1.00 },
  { tab_id: 'tab8', provider: 'Oracle-ARM-A1', gpu_type: 'Ampere A1 CPU control plane', vram_gb: 0, role: 'control+data', compute_weight: 0.12 },
  { tab_id: 'tab9', provider: 'Oracle-ARM-A2', gpu_type: 'Ampere A1 CPU control plane', vram_gb: 0, role: 'control+checkpoint', compute_weight: 0.12 },
]);

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function sigilFor(value) {
  const input = canonical(value);
  const secret = process.env.FREE_GPU_SIGIL_SECRET;
  return secret
    ? crypto.createHmac('sha256', secret).update(input).digest('hex')
    : crypto.createHash('sha256').update(input).digest('hex');
}

function parseStateOverrides() {
  try {
    const parsed = JSON.parse(process.env.FREE_GPU_TAB_STATE_JSON || '{}');
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed : {};
  } catch {
    return {};
  }
}

function readRecentJobs(nowMs) {
  try {
    const lines = fs.readFileSync(JOB_LOG, 'utf8').trim().split('\n').filter(Boolean).slice(-50);
    return lines.map(line => JSON.parse(line))
      .filter(job => job && Date.parse(job.timestamp) >= nowMs - ACTIVE_JOB_WINDOW_MS)
      .slice(-12)
      .reverse();
  } catch {
    return [];
  }
}

function validHeartbeat(value) {
  if (!value) return null;
  const timestamp = Date.parse(value);
  return Number.isFinite(timestamp) ? new Date(timestamp).toISOString() : null;
}

function tabState(base, overrides, jobs) {
  const override = overrides[base.tab_id] || {};
  const assignedJob = jobs.find(job => Array.isArray(job.shards_assigned)
    && job.shards_assigned.some(shard => shard.tab_id === base.tab_id));

  let status = 'standby';
  let currentModel = null;
  let lastHeartbeat = null;
  let loadPct = 0;
  let activeJobId = null;

  if (assignedJob) {
    status = assignedJob.status === 'running' ? 'training' : 'queued';
    currentModel = assignedJob.model || null;
    lastHeartbeat = validHeartbeat(assignedJob.timestamp);
    loadPct = assignedJob.status === 'running' ? 92 : 8;
    activeJobId = assignedJob.job_id || null;
  }

  const allowedStatuses = new Set(['standby', 'online', 'queued', 'training', 'degraded', 'offline']);
  if (allowedStatuses.has(override.status)) status = override.status;
  if (typeof override.current_model === 'string' && override.current_model.trim()) {
    currentModel = override.current_model.trim().slice(0, 120);
  } else if (override.current_model === null) {
    currentModel = null;
  }
  if (validHeartbeat(override.last_heartbeat)) lastHeartbeat = validHeartbeat(override.last_heartbeat);
  if (Number.isFinite(Number(override.load_pct))) loadPct = Math.max(0, Math.min(100, Number(override.load_pct)));
  if (typeof override.active_job_id === 'string') activeJobId = override.active_job_id.slice(0, 100);

  const receiptPayload = {
    tab_id: base.tab_id,
    provider: base.provider,
    gpu_type: base.gpu_type,
    vram_gb: base.vram_gb,
    status,
    current_model: currentModel,
    last_heartbeat: lastHeartbeat,
  };

  return {
    ...receiptPayload,
    sigil: sigilFor(receiptPayload),
    role: base.role,
    load_pct: loadPct,
    active_job_id: activeJobId,
    compute_weight: base.compute_weight,
  };
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Sovereign-Budget', 'GBP-0');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') {
    return res.status(405).json({
      status: 'method_not_allowed',
      error: 'GET required',
      sigil: null,
      timestamp: new Date().toISOString(),
    });
  }

  const timestamp = new Date().toISOString();
  const nowMs = Date.parse(timestamp);
  const jobs = readRecentJobs(nowMs);
  const overrides = parseStateOverrides();
  const tabs = FLEET.map(tab => tabState(tab, overrides, jobs));
  const totalVramGb = tabs.reduce((sum, tab) => sum + tab.vram_gb, 0);
  const activeTabs = tabs.filter(tab => ['online', 'queued', 'training'].includes(tab.status));
  const activeModels = new Set(tabs.map(tab => tab.current_model).filter(Boolean));
  const trainingTabs = tabs.filter(tab => tab.status === 'training');
  const queuedShards = tabs.filter(tab => tab.status === 'queued').length;

  const core = {
    status: trainingTabs.length ? 'training' : activeTabs.length ? 'fleet_ready' : 'fleet_standby',
    tabs,
    total_vram_gb: totalVramGb,
    total_active_models: activeModels.size,
    timestamp,
  };

  return res.status(200).json({
    ...core,
    sigil: sigilFor(core),
    sigil_algorithm: process.env.FREE_GPU_SIGIL_SECRET ? 'HMAC-SHA256' : 'SHA-256 content receipt',
    budget_gbp: 0,
    accelerator_tabs: tabs.filter(tab => tab.vram_gb > 0).length,
    control_plane_tabs: tabs.filter(tab => tab.vram_gb === 0).length,
    fleet_throughput: {
      training_tabs: trainingTabs.length,
      queued_shards: queuedShards,
      capacity_weight_t4_equivalent: Number(tabs.reduce((sum, tab) => sum + tab.compute_weight, 0).toFixed(2)),
      measured_samples_per_second: null,
      note: 'Capacity is a scheduler weight, not a measured benchmark. Live samples/sec remains null until workers publish heartbeats.',
    },
    training_jobs: jobs.map(job => ({
      job_id: job.job_id,
      model: job.model,
      dataset: job.dataset,
      epochs: job.epochs,
      status: job.status,
      shard_count: Array.isArray(job.shards_assigned) ? job.shards_assigned.length : 0,
      eta_seconds: job.eta_seconds,
      timestamp: job.timestamp,
      sigil: job.sigil,
    })),
    freshness: activeTabs.length
      ? 'Runtime/queue evidence available for at least one tab.'
      : 'No live heartbeat evidence received; all tabs are honestly reported as standby.',
  });
};

module.exports.FLEET = FLEET;
module.exports.sigilFor = sigilFor;
