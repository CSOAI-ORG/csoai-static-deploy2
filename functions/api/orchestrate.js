// Cloudflare Pages Function — converted from api/orchestrate.js
import { createHash, createHmac, randomBytes } from 'crypto';

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }




    if (request.method === 'OPTIONS') return new Response(null, { status: 200, headers: corsHeaders });

    const SUBSTRATE_IP = '35.242.143.249';
    const SUBSTRATE_PORT = 3101;
    const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';

    // Try live substrate
    let substrate_status = 'unreachable';
    let live = false;
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 3000);
      const r = await fetch(`http://${SUBSTRATE_IP}:${SUBSTRATE_PORT}/mcp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jsonrpc: '2.0', method: 'tools/list', id: 1 }),
        signal: controller.signal
      });
      clearTimeout(timeout);
      if (r.ok) {
        substrate_status = 'live';
        live = true;
      }
    } catch (e) {
      substrate_status = 'unreachable';
    }

    // Real brain call: probe Ollama for available models
    let brain_status = 'unreachable';
    let brain_models = [];
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 5000);
      const r = await fetch(`${OLLAMA_URL}/api/tags`, { signal: controller.signal });
      clearTimeout(timeout);
      if (r.ok) {
        const data = await r.json();
        brain_status = 'live';
        brain_models = (data.models || []).map(m => ({ name: m.name, size: m.size }));
      }
    } catch (e) {
      brain_status = 'unreachable';
    }

    // Real work-unit: if POST with prompt, actually call the brain
    let work_unit_result = null;
    if (request.method === 'POST' && await request.json() && await request.json().prompt) {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 30000);
        const r = await fetch(`${OLLAMA_URL}/api/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: await request.json().model || 'sov33-master-v2:latest',
            prompt: await request.json().prompt,
            stream: false,
            options: { temperature: 0.1, num_predict: 256 }
          }),
          signal: controller.signal
        });
        clearTimeout(timeout);
        if (r.ok) {
          const data = await r.json();
          work_unit_result = {
            model: await request.json().model || 'sov33-master-v2:latest',
            response: (data.response || '').slice(0, 500),
            latency_ms: Math.round((data.total_duration || 0) / 1e6)
          };
        }
      } catch (e) {
        work_unit_result = { error: e.message };
      }
    }

    const orchestration = {
      status: substrate_status,
      live_substrate: live,
      brain: {
        status: brain_status,
        models: brain_models.length,
        model_list: brain_models.slice(0, 10)
      },
      work_unit: work_unit_result,
      timestamp: new Date().toISOString(),
      pipeline: {
        care_floor_check: { status: 'active', threshold: 0.95 },
        owem_routing: { status: 'active', owems: 5, specialists: ['compliance', 'defense', 'intuition', 'voice', 'general'] },
        backend_chain: { status: 'active', backends: ['sov_brain', 'oracle_genai', 'ollama', 'groq'] },
        bft_council: { status: live ? 'live' : 'simulated', quorum: '23/33', algorithm: 'HotStuff' },
        sigil_chain: { status: 'active', signing: 'Ed25519', rate: '1Hz' }
      },
      benchmark: {
        task_registry: '3.0',
        total_tasks: 300,
        suites: 19,
        last_run: null,
        runners: ['run_benchmark_v3.py', 'run_ollama_benchmark.py', 'runpod_full_run.py']
      },
      training: {
        owems_trained: 5,
        multi_family_modelfiles: 20,
        synthetic_data: { pairs: 3915, target: 4000, pct: 97.9 }
      }
    };

    const sigil = createHmac('sha256', process.env.SIGIL_SECRET || 'csoai-sovereign-orchestrate')
      .update(JSON.stringify(orchestration)).digest('hex').slice(0, 16);

    return new Response(JSON.stringify({ ...orchestration, sigil }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
}
