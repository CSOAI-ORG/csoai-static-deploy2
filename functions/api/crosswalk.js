/**
 * /api/crosswalk — eunomia-east-west-bridge, live + signed.
 * Map an East governance signal (TC260 / social-credit / PDCA) to a West output.
 */
import { getKey as getPinnedKey, bytesToHex } from './signlib.js';
let _k=null; async function key(env){ if(!_k)_k=getPinnedKey(env); return _k; }
function canon(o){ if(o===null)return'null'; if(o===true)return'true'; if(o===false)return'false'; if(typeof o==='string')return JSON.stringify(o); if(typeof o==='number')return Number.isFinite(o)?String(o):'0'; if(Array.isArray(o))return'['+o.map(canon).join(',')+']'; if(typeof o==='object')return'{'+Object.keys(o).sort().map(k=>JSON.stringify(k)+':'+canon(o[k])).join(',')+'}'; return'null'; }
async function sha(s){const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));return[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');}
function b64(u){let b='';u.forEach(x=>b+=String.fromCharCode(x));return btoa(b);}
function h2b(h){return new Uint8Array((h.match(/.{2}/g)||[]).map(b=>parseInt(b,16)));}
const W={'tc260-registry':{east:'TC260 algorithm registry (China)',west:'NIST AI RMF / EU AI Act high-risk dossier',kind:'governance-score'},'social-credit-profile':{east:'China social credit / behaviour profile',west:'GDPR-anonymised verifiable identity',kind:'identity'},'pdca-cycle':{east:'PDCA',west:'Agile + on-chain attestation (proofof-ai)',kind:'lifecycle'},'algorithm-filing':{east:'TC260 filing',west:'EU AI Act Art 5 / NIST RMF mapping',kind:'compliance-crosswalk'},'data-localisation':{east:'PIPL data localisation',west:'EU data adequacy + GDPR minimalisation',kind:'data-flow'}};
export async function onRequest(context){
  const h={'content-type':'application/json','access-control-allow-origin':'*','access-control-allow-methods':'GET,POST,OPTIONS'};
  if(context.request.method==='OPTIONS')return new Response(null,{status:204,headers:h});
  if(context.request.method==='GET')return new Response(JSON.stringify({schema:'csoai.crosswalk/0.1',example:'POST {"signal":"tc260-registry"}',signals:Object.keys(W),not_a_certification:true}),{status:200,headers:h});
  if(context.request.method!=='POST')return new Response(JSON.stringify({error:'POST only'}),{status:405,headers:h});
  let b; try{b=await context.request.json();}catch(e){return new Response(JSON.stringify({error:'bad json'}),{status:400,headers:h});}
  const sig=String(b.signal||'').toLowerCase().replace(/ /g,'-'); const hit=W[sig];
  const result=hit?{east_signal:b.signal,east:hit.east,west_output:hit.west,output_kind:hit.kind,trust:'both trust the CSOAI attestation, not each other',matched:true}:{east_signal:b.signal,matched:false,note:'unmapped — report honestly, never interpolate'};
  const witnessed_at=new Date().toISOString();
  const claim={schema:'csoai.crosswalk/0.1',record_type:'measured-current-state',not_a_certification:true,endorsement:'none',authored_by:'did:web:csoai-gspc.pages.dev',basis:'curated East->West translation table',witnessed_at,crosswalk:result};
  const content_id=await sha(canon(claim)); const pair=await key(context.env); const s=await crypto.subtle.sign('Ed25519',pair.privateKey,new TextEncoder().encode(content_id)); const pub=pair.rawPubHex?h2b(pair.rawPubHex):await crypto.subtle.exportKey('raw',pair.publicKey);
  const card={...claim,content_id,signature:b64(new Uint8Array(s)),pubkey:bytesToHex(new Uint8Array(pub))};
  if(pair.kid){card.key_id=pair.kid;card.verification_method=pair.did+'#gspc';card.did_resolver='https://'+pair.did.replace('did:web:','')+'/.well-known/did.json';}
  return new Response(JSON.stringify({summary:result.matched?`${sig} → ${result.west_output}`:`${sig} → unmapped (honest)`,card}),{status:200,headers:h});
}
