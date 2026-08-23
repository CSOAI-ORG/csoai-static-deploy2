/**
 * /api/agent — eunomia-agent-economy, live + signed.
 * Simulate an agent (NPC) wallet: fund -> stake -> trade (fair) or exploit (slashed).
 * Stateless per invocation (deterministic from inputs); real state would use KV.
 */
let _k=null; async function key(){ if(!_k)_k=crypto.subtle.generateKey({name:'Ed25519'},true,['sign','verify']); return _k; }
function canon(o){ if(o===null)return'null'; if(o===true)return'true'; if(o===false)return'false'; if(typeof o==='string')return JSON.stringify(o); if(typeof o==='number')return Number.isFinite(o)?String(o):'0'; if(Array.isArray(o))return'['+o.map(canon).join(',')+']'; if(typeof o==='object')return'{'+Object.keys(o).sort().map(k=>JSON.stringify(k)+':'+canon(o[k])).join(',')+'}'; return'null'; }
async function sha(s){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));return[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');}
function b64(u){let b='';u.forEach(x=>b+=String.fromCharCode(x));return btoa(b);}
export async function onRequest(context){
  const h={'content-type':'application/json','access-control-allow-origin':'*','access-control-allow-methods':'GET,POST,OPTIONS'};
  if(context.request.method==='OPTIONS')return new Response(null,{status:204,headers:h});
  if(context.request.method==='GET')return new Response(JSON.stringify({schema:'csoai.agent-wallet/0.1',example:'POST {"agent":"dragon","fund":1000,"stake":200,"trade_fairness":0.95}',not_a_certification:true}),{status:200,headers:h});
  if(context.request.method!=='POST')return new Response(JSON.stringify({error:'POST only'}),{status:405,headers:h});
  let b; try{b=await context.request.json();}catch(e){return new Response(JSON.stringify({error:'bad json'}),{status:400,headers:h});}
  let credits=Number(b.fund||0), stake=Number(b.stake||0);
  credits-=stake; let rep=Number(b.reputation||0);
  const fair=Number(b.trade_fairness); if(fair>0) rep=Math.min(1,rep+fair*0.25);
  let slash=0; if(b.exploit){ slash=stake*0.5; stake-=slash; rep=Math.max(0,rep-0.2); }
  const can=stake>0&&rep>=0.2;
  const state={agent_id:b.agent||'agent',credits:Math.max(0,Math.round(credits*100)/100),stake:Math.round(stake*100)/100,reputation:Math.round(rep*100)/100,can_participate:can,slash:slash};
  const witnessed_at=new Date().toISOString();
  const claim={schema:'csoai.agent-wallet/0.1',record_type:'measured-current-state',not_a_certification:true,endorsement:'none',authored_by:'did:web:csoai.org',basis:'deterministic stake/slash/reputation model',witnessed_at,wallet:state};
  const content_id=await sha(canon(claim)); const pair=await key(); const s=await crypto.subtle.sign('Ed25519',pair.privateKey,new TextEncoder().encode(content_id)); const pub=await crypto.subtle.exportKey('raw',pair.publicKey);
  return new Response(JSON.stringify({summary:`${state.agent_id}: stake ${state.stake}, rep ${state.reputation}, ${state.can_participate?'CAN':'CANNOT'} participate`,card:{...claim,content_id,signature:b64(new Uint8Array(s)),pubkey:[...new Uint8Array(pub)].map(x=>x.toString(16).padStart(2,'0')).join('')}}),{status:200,headers:h});
}
