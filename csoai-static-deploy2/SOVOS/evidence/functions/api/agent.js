// AG-UI OS-native agent: knows the Council OS + products, routes intent to actions.
const CANON = {
  "SB 315":"Illinois SB 315 = the Illinois AI SAFETY MEASURES ACT. Signed 2026-07-06, effective 2027-01-01, mandatory annual independent third-party frontier audits from 2028-01-01. Canon #51."
};
const PRODUCTS = {
  products:"The Council OS product suite (measurement, not certification): Attestation-as-a-Service (signed, verifiable measurement credentials) — Capital Markets (/finance), AI-Liability (/insurer), Council Ledger/Dorado/Claimguard (/ledger), and the booking funnel (/book). View all: /products.",
  verify:"Verify a signed receipt: open /verify — any signed receipt verifies in-browser (WebCrypto) or with verify_signature.py, against the published pubkey bWbk52E47J6EkY4+pu0Hh/B1l1175AZoZsDEBr0EfWA=. Ed25519-signed on the signing node (key never leaves). Open /verify.",
  book:"Book a 5-day evidence pack: /book — a signed receipt + method + independence register for one use-case, priced €8-20k / €25-80k / €5-15k/yr. The form captures your lead. Measurement, not certification.",
  board:"The measurement board (/board): measured models (mistral 67.3 LEAD, llama3 66.6 TIE, qwen2.5:7b 63.3, 1.5b 60.5, 0.5b 32.6 RAG) with lead/tie/empty + honest registers (MEASURED/REPORTED/UNMEASURED), each with a signed receipt. Retrieved>>trained (+34-38); base>fine-tunes.",
  axes:"The merged axes (/axes): 16 governance axes (13 measured of 14) + the next financial axes — COBOL/legacy, Insurance, Market/bond, Agent-identity, Compliance-conformance. Each emits a signed receipt.",
  models:"The measurement-annotated model catalog (/models): models are MEASURED (GSPC lead/tie/empty), not just listed. View /models.",
  "AG-UI":"AG-UI is the agent→user wire (AUDIO_MESSAGE_START → CHUNK → END + TRANSCRIPT_DELTA, keyed by messageId). This chat IS the AG-UI surface."
};
function route(q){
  q=q.toLowerCase();
  for (const k of Object.keys(CANON)) if (q.includes(k.toLowerCase())) return {ground:CANON[k],link:null};
  if(q.includes('book')||q.includes('evidence pack')||q.includes('pack')) return {txt:PRODUCTS.book,link:'/book'};
  if(q.includes('verif')||q.includes('receipt')) return {txt:PRODUCTS.verify,link:'/verify'};
  if(q.includes('board')||q.includes('gspc')) return {txt:PRODUCTS.board,link:'/board'};
  if(q.includes('axes')||q.includes('axis')) return {txt:PRODUCTS.axes,link:'/axes'};
  if(q.includes('model')||q.includes('leaderboard')||q.includes('ranking')) return {txt:PRODUCTS.models,link:'/models'};
  if(q.includes('product')||q.includes('offer')||q.includes('suite')||q.includes('attestation')||q.includes('capabilities')||q.includes('service')) return {txt:PRODUCTS.products,link:'/products'};
  if(q.includes('ag-ui')||q.includes('agent')) return {txt:PRODUCTS['AG-UI'],link:null};
  return {txt:null,link:null};
}
export async function onRequestPost({ request, env }) {
  try{
    const { q } = await request.json(); if(!q) return new Response(JSON.stringify({ok:false,error:'no q'}),{status:400,headers:{'content-type':'application/json'}});
    const r = route(q);
    if (r.txt) return res(r.txt, (r.link?('/'+r.link.slice(1)+' · '):'')+'OS-native');
    if (r.ground) return res('Registry (canon #51-56): '+r.ground, 'registry');
    // fallback: model (doctrine-tight)
    const m=await fetch('https://api.deepseek.com/chat/completions',{method:'POST',headers:{'Authorization':'Bearer '+env.DEEPSEEK_API_KEY,'content-type':'application/json'},body:JSON.stringify({model:'deepseek-chat',max_tokens:200,messages:[{role:'system',content:'You are the Council of AI measurement agent (AG-UI OS-native). Measurement, not certification. Never fabricate a regulatory fact; if unsure say "UNMEASURED — consult the registry." Guide users to the right Council OS surface. Never promise a certificate.'},{role:'user',content:q}]})});
    const md=await m.json(); const answer=(md.choices&&md.choices[0]&&md.choices[0].message.content)?md.choices[0].message.content:'UNMEASURED — consult the registry.';
    return res(answer,'model');
  }catch(e){ return new Response(JSON.stringify({ok:false,error:String(e)}),{status:500,headers:{'content-type':'application/json'}}); }
}
function res(txt,type){
  return new Response(JSON.stringify({ok:true,answer:txt,section:type,
    events:[{t:'AUDIO_MESSAGE_START',messageId:'m-'+(Date.now())},{t:'TRANSCRIPT_DELTA',messageId:'m-'+(Date.now()),delta:txt,isFinal:true},{t:'AUDIO_MESSAGE_END',messageId:'m-'+(Date.now())}]
  }),{headers:{'content-type':'application/json'}});
}
