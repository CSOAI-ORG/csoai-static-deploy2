// SOVEREIGN AGENT PACKAGE (SAP v1) — a NEW composite agent TYPE, not a new transport.
// It fuses four things that today live apart, into ONE offline-verifiable signed artifact:
//   • A2A Agent Card  (identity/discovery)         — rides the A2A standard
//   • MCP endpoint     (tools/usage)               — rides MCP
//   • Letta .af state  (persona + memory + tools)  — rides the open Agent File format
//   • MEOK Layer-0     (Ed25519 sovereign signature + governance card) — the part nobody else has
// The AGENT (persona, memory, policy, identity, tool contract) lives INSIDE the container and is
// portable + signed. The MODEL is pluggable (BYO host model via MCP, or on-device llamafile/Ollama)
// — weights are NOT embedded (honest: too big for serverless/edge). "AI inside the container" = the
// mind is inside; the model is any body. Differentiator vs Sigstore-a2a (keyless/CA/OIDC): SOVEREIGN,
// self-owned, offline-verifiable key. vs Letta .af: signed + governed. vs AIP paper: shipped.
// ?format=af → export a Letta Agent-File-compatible JSON (interop, not lock-in).
import crypto from 'crypto';
function canonical(v){ if(typeof v==='string') return v; const s=x=>Array.isArray(x)?x.map(s):(x&&typeof x==='object')?Object.keys(x).sort().reduce((o,k)=>(o[k]=s(x[k]),o),{}):x; return JSON.stringify(s(v)); }
function keypair(){ const seed=crypto.createHash('sha256').update(process.env.SIGIL_SEED||'meok-sovereign-demo-key-2026').digest(); const pkcs8=Buffer.concat([Buffer.from('302e020100300506032b657004220420','hex'),seed]); const priv=crypto.createPrivateKey({key:pkcs8,format:'der',type:'pkcs8'}); return {priv,pubHex:crypto.createPublicKey(priv).export({type:'spki',format:'der'}).toString('hex')}; }
const ARCHE={ dragon:'a guardian strategist', fox:'a swift connector', owl:'a careful analyst', phoenix:'a resilient builder', default:'a sovereign companion' };

export default function handler(req, res){
  res.setHeader('Access-Control-Allow-Origin','*'); res.setHeader('Access-Control-Allow-Headers','Content-Type'); res.setHeader('Cache-Control','public, max-age=60');
  if(req.method==='OPTIONS') return res.status(204).end();
  try{
    const q=req.query||{}; const name=(q.name||'MEOK Sovereign').toString().slice(0,60); const arch=(q.archetype||'default').toString().toLowerCase().slice(0,24);
    const base='https://os.meok.ai'; const persona=name+' — '+(ARCHE[arch]||ARCHE.default)+'. Sovereign, governed, remembers you on your device.';
    const tools=[
      {name:'meok_talk',desc:'converse (governed, care-floored)'},
      {name:'meok_govern',desc:'what governs an industry → frameworks + bridges'},
      {name:'meok_sign',desc:'Ed25519-sign an action'},
      {name:'meok_verify',desc:'verify a signature offline'},
    ];
    // Letta .af-compatible state block (so any .af host can import; interop not lock-in)
    const af_state = {
      version: '0.1', agent_type: 'memgpt_agent', name,
      system: 'You are '+persona+' You never take harmful action (care floor 0.95); hard stops are immutable.',
      memory: { blocks: [ {label:'persona', value: persona, limit:2000}, {label:'human', value:'(learned on the user\'s device)', limit:2000} ] },
      tools: tools.map(t=>({name:t.name, description:t.desc})),
      llm_config: { model:'BYO', note:'model provided by host (MCP/MRTR) or on-device (llamafile/ollama); weights not embedded' },
      messages: [],
    };
    const pkg = {
      spec: 'meok.sap.v1',
      type: 'sovereign-agent-package · portable mini-OS (governance profile)',
      // HONEST positioning: NOT a new protocol. Portable signed agent packages are already being
      // standardized (AGNTCY/Linux Foundation: OASF records as OCI artifacts, Sigstore-signed, DID/VC
      // identity, A2A+MCP interop, draft 2026-01-12). We do NOT compete with that. Our uncontested edge:
      // a SOVEREIGN, SELF-OWNED, OFFLINE-verifiable Ed25519 signature + EMBEDDED governance (care-floor,
      // hard-stops) — vs AGNTCY/Sigstore's keyless CA/OIDC model that needs an online trust root.
      positioning: 'Sovereign, offline-verifiable, governed PROFILE that rides the emerging standards — not a replacement for them.',
      interop: ['a2a-agent-card', 'mcp/2024-11-05', 'letta/agent-file(.af)', 'agntcy/OASF(OCI)-compatible', 'w3c-did/vc (roadmap)'],
      differs_from: { 'AGNTCY/Sigstore': 'they sign keyless via a CA/OIDC (Fulcio) — online trust root; we self-own an offline Ed25519 key', 'Letta .af': 'we add a signature + governance', 'AIP/arxiv proposals': 'shipped, not a paper' },
      agent: { name, archetype: arch, description: persona, version:'1.0.0', provider:'CSOAI / MEOK (UK Co. 16939677)' },
      state: af_state,                                   // the MIND, portable (Letta-.af shape)
      // DUAL BRAIN — left (reason) + right (vision), each with OFFLINE + ONLINE model options.
      // Offline-first when a local model is present; online fallback. Weights referenced, not embedded.
      brain: {
        orchestrator: 'Sovereign OLM (Mamba-2 SSD) + SOV3 — reconciles the two brains, talks to the user',
        left: { role:'reasoning · analysis · tools · governance', online:['groq/llama-3.3-70b','anthropic/claude','openai/gpt'], offline:['ollama/llama3.1','llamafile/qwen2.5'], default:'online, offline-capable' },
        right:{ role:'creativity · vision · voice · the world', online:['anthropic/claude','image/voice APIs'], offline:['on-device VLM','local TTS (Piper/Kokoro)'], default:'hybrid' },
        modes:['offline (on-device only)','online (hosted)','hybrid (offline-first, online fallback)'],
        note:'the package carries the ROUTING + model choices (the "which brain, online or offline"); the weights are pluggable per host.',
      },
      // BOOTABLE BODY — the package is a signed mini-OS IMAGE: open it → it boots into this shell +
      // 3D world + character. The heavy renderer/engine is REFERENCED (fetched), never embedded.
      boot: {
        os: base+'/', world3d: base+'/earth3d.html', photoreal: base+'/earth3d-photoreal.html',
        character: base+'/character.html', renderer:'Cesium / MapLibre (body)', shell:'MEOK OS (Sovereign dock + apps + globe)',
        note:'a portable sovereign mini-OS: identity+brain+governance travel signed; the OS/3D body is fetched + rendered by the host (browser/desktop/VM).',
      },
      governance: { careFloor: 0.95, hardStops:['no harm','no unvoted autonomy','no covert surveillance'], frameworks:['EU AI Act','ISO 42001','JSP 936 (defence variant)'] },
      interfaces: { agentCard: base+'/api/agentcard?name='+encodeURIComponent(name)+'&archetype='+encodeURIComponent(arch), mcp: base+'/api/mcp', openai_chat: base+'/api/v1/chat/completions', onDeviceRunner: base+'/runner/meok-sap-runner.mjs' },
      model_policy: { embedded: false, sources:['host model via MCP','on-device llamafile/ollama','hosted API'], reason:'weights too large for serverless/edge — the AGENT (mind+brain-routing+body-refs) is portable, the MODEL is pluggable' },
      runnable: ['serverless (default, scale-to-zero)','on-device (local MCP stdio + offline brain)','dedicated VM (premium, always-on)'],
    };
    const { priv, pubHex } = keypair();
    const message = canonical(pkg).slice(0, 8000);
    const signature = crypto.sign(null, Buffer.from(message), priv).toString('hex');
    const sha256 = crypto.createHash('sha256').update(message).digest('hex');
    const fingerprint='SOV:'+crypto.createHash('sha256').update(pubHex).digest('hex').slice(0,32).match(/.{1,4}/g).join('-').toUpperCase();
    if((q.format||'').toString().toLowerCase()==='af'){ return res.status(200).json(af_state); }  // Letta import
    return res.status(200).json({ ok:true, package:pkg, signature:{ alg:'ed25519', canonical:message, signature, publicKey:pubHex, sha256, fingerprint, seeded:!!process.env.SIGIL_SEED, verify: base+'/api/verify' },
      note:'Sovereign governance PROFILE for portable agents — rides AGNTCY(OASF/OCI)+A2A+MCP+.af, adds the offline-verifiable sovereign+governed signature they lack. AGENT inside+signed; MODEL pluggable. Verify at /api/verify; ?format=af for Letta import.' });
  }catch(e){ return res.status(500).json({ ok:false, error:String(e.message||e) }); }
}
