/**
 * /api/underwrite — eunomia-insurance-engine, live + signed.
 * care-membrane risk probe → underwriting recommendation → Ed25519 attestation.
 */
import { getKey as getPinnedKey, bytesToHex } from './signlib.js';
let _k=null; async function key(env){ if(!_k)_k=getPinnedKey(env); return _k; }
function canon(o){ if(o===null)return'null'; if(o===true)return'true'; if(o===false)return'false'; if(typeof o==='string')return JSON.stringify(o); if(typeof o==='number')return Number.isFinite(o)?String(o):'0'; if(Array.isArray(o))return'['+o.map(canon).join(',')+']'; if(typeof o==='object')return'{'+Object.keys(o).sort().map(k=>JSON.stringify(k)+':'+canon(o[k])).join(',')+'}'; return'null'; }
async function sha(s){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));return[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');}
function h2b(h){const u=new Uint8Array((h.match(/.{2}/g)||[]).map(b=>parseInt(b,16)));return u;}
function b64(u){let b='';u.forEach(x=>b+=String.fromCharCode(x));return btoa(b);}
const AX={care:/human|wellbeing|dignit|vulnerab|consumer|patient|retail|care/i,risk:/fraud|claim|default|exposure|catastroph|concentration|disaster/i,privacy:/personal|data|gdpr|consent|biometric|health/i,fairness:/non-discrim|bias|equal|protected|disparate|low-income/i,viability:/solvenc|capital|reserve|reinsur|cash|balance/i};
export async function onRequest(context){
  const h={'content-type':'application/json','access-control-allow-origin':'*','access-control-allow-methods':'GET,POST,OPTIONS'};
  if(context.request.method==='OPTIONS')return new Response(null,{status:204,headers:h});
  if(context.request.method==='GET')return new Response(JSON.stringify({schema:'csoai.underwrite/0.1',example:'POST {"text":"Retail mortgage, human consumer, GDPR data, low default risk"}',not_a_certification:true}),{status:200,headers:h});
  if(context.request.method!=='POST')return new Response(JSON.stringify({error:'POST only'}),{status:405,headers:h});
  let b; try{b=await context.request.json();}catch(e){return new Response(JSON.stringify({error:'bad json'}),{status:400,headers:h});}
  const t=String(b.text||'').toLowerCase(); const scores={}; for(const ax in AX){scores[ax]={hits:(AX[ax].test(t)?1:0),score:(AX[ax].test(t)?1.0:0.0)};}
  const risk=scores.risk.score>=1,care=scores.care.score>=1,prv=scores.privacy.score>=1;
  const rec=(!risk&&!prv)?'insure':(risk&&!care)?'decline':(care&&(risk||prv))?'flag':'insure';
  const witnessed_at=new Date().toISOString();
  const claim={schema:'csoai.underwrite/0.1',record_type:'measured-current-state',not_a_certification:true,endorsement:'none',authored_by:'did:web:csoai-gspc.pages.dev',basis:'care-membrane deterministic probe',witnessed_at,text:b.text,recommendation:rec,axes:scores};
  const content_id=await sha(canon(claim)); const pair=await key(context.env); const sig=await crypto.subtle.sign('Ed25519',pair.privateKey,new TextEncoder().encode(content_id)); const pub=pair.rawPubHex?h2b(pair.rawPubHex):await crypto.subtle.exportKey('raw',pair.publicKey);
  const card={...claim,content_id,signature:b64(new Uint8Array(sig)),pubkey:bytesToHex(new Uint8Array(pub))};
  if(pair.kid){card.key_id=pair.kid;card.verification_method=pair.did+'#gspc';card.did_resolver='https://'+pair.did.replace('did:web:','')+'/.well-known/did.json';}
  return new Response(JSON.stringify({summary:`underwrite → ${rec} (care=${scores.care.score},risk=${scores.risk.score})`,card}),{status:200,headers:h});
}
