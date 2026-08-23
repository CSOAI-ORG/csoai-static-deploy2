/**
 * /api/dataset — eunomia-data-dao, live + signed.
 * Register a dataset + marketplace buy (agents-only; humans never charged).
 * Stateless per invocation: the registry is the deterministic result of the action.
 */
let _k=null; async function key(){ if(!_k)_k=crypto.subtle.generateKey({name:'Ed25519'},true,['sign','verify']); return _k; }
function canon(o){ if(o===null)return'null'; if(o===true)return'true'; if(o===false)return'false'; if(typeof o==='string')return JSON.stringify(o); if(typeof o==='number')return Number.isFinite(o)?String(o):'0'; if(Array.isArray(o))return'['+o.map(canon).join(',')+']'; if(typeof o==='object')return'{'+Object.keys(o).sort().map(k=>JSON.stringify(k)+':'+canon(o[k])).join(',')+'}'; return'null'; }
async function sha(s){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));return[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');}
function b64(u){let b='';u.forEach(x=>b+=String.fromCharCode(x));return btoa(b);}
const KINDS=['arena-traces','gaming-behavior','compliance-incidents','cash-flow','benchmark'];
export async function onRequest(context){
  const h={'content-type':'application/json','access-control-allow-origin':'*','access-control-allow-methods':'GET,POST,OPTIONS'};
  if(context.request.method==='OPTIONS')return new Response(null,{status:204,headers:h});
  if(context.request.method==='GET')return new Response(JSON.stringify({schema:'csoai.data-dao/0.1',kinds:KINDS,example:'POST {"action":"buy","name":"compliance-incidents","price_eun":50,"balance":100}',not_a_certification:true}),{status:200,headers:h});
  if(context.request.method!=='POST')return new Response(JSON.stringify({error:'POST only'}),{status:405,headers:h});
  let b; try{b=await context.request.json();}catch(e){return new Response(JSON.stringify({error:'bad json'}),{status:400,headers:h});}
  const name=String(b.name||'dataset'); const kind=KINDS.includes(b.kind)?b.kind:'arena-traces'; const price=Number(b.price_eun||0); const balance=Number(b.balance||0);
  let result;
  if(b.action==='buy'){ result=(price<=balance)?{sold:true,dataset:name,remaining_eun:balance-price,deal:'agents-only, humans never charged'}:{sold:false,error:'insufficient EUN',price_eun:price,balance:balance}; }
  else { result={registered:true,name,kind,price_eun:price,license:b.license||'cc0-public-good',not_a_certification:true,count:1}; }
  const witnessed_at=new Date().toISOString();
  const claim={schema:'csoai.data-dao/0.1',record_type:'measured-current-state',not_a_certification:true,endorsement:'none',authored_by:'did:web:csoai.org',basis:'data DAO registry + marketplace (stateless demo)',witnessed_at,action:b.action||'register',result};
  const content_id=await sha(canon(claim)); const pair=await key(); const s=await crypto.subtle.sign('Ed25519',pair.privateKey,new TextEncoder().encode(content_id)); const pub=await crypto.subtle.exportKey('raw',pair.publicKey);
  return new Response(JSON.stringify({summary:(b.action==='buy'?`buy ${name} → ${result.sold?'SOLD':'insufficient EUN'}`:`register ${name} (${kind})`),card:{...claim,content_id,signature:b64(new Uint8Array(s)),pubkey:[...new Uint8Array(pub)].map(x=>x.toString(16).padStart(2,'0')).join('')}}),{status:200,headers:h});
}
