const crypto = require('crypto');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  const registry = {
    version: '3.0',
    timestamp: new Date().toISOString(),
    total_models: 61,
    sovereign_safe: 53,
    owems: {
      count: 5,
      specialists: ['compliance', 'defense', 'intuition', 'voice', 'general'],
      all_sovereign_trained: true,
      backends: {
        colab_t4: ['compliance', 'defense', 'intuition', 'voice'],
        runpod_rtx3090: ['general']
      }
    },
    families: {
      qwen: { base: 'qwen2.5:0.5b', adapters: 5, status: 'built' },
      llama: { base: 'llama3.2:3b', adapters: 5, status: 'modelfiles_ready' },
      deepseek: { base: 'deepseek-coder:1.3b', adapters: 5, status: 'modelfiles_ready' },
      mistral: { base: 'mistral:7b', adapters: 5, status: 'modelfiles_ready' }
    },
    benchmarks: {
      task_registry_version: '3.0',
      total_tasks: 300,
      suites: 19,
      last_run: null
    },
    governance: {
      care_floor: 0.95,
      bft_quorum: '23/33',
      sigil_chain: 'Ed25519',
      article_0: 'ISO fee-for-service only'
    }
  };

  const sigil = crypto.createHmac('sha256', process.env.SIGIL_SECRET || 'csoai-sovereign-registry')
    .update(JSON.stringify(registry)).digest('hex').slice(0, 16);

  return res.status(200).json({ ...registry, sigil });
};
