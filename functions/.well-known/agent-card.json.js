
/**
 * /.well-known/agent-card.json — Council of AI signed A2A agent card (AXIS 17).
 * "Our own card signed first." A stranger validates content_id + Ed25519 with the
 * did:web:csoai-gspc.pages.dev#gspc key. Measurement, not certification.
 */
import { getKey, canon, sha256hex, bytesToB64, bytesToHex } from '../api/signlib.js';
const CARD = {"@context":"https://www.w3.org/ns/agent-card/v1","schema":"csoai.agent-card/0.1","record_type":"measured-current-state","not_a_certification":true,"endorsement":"none","authored_by":"did:web:csoai-gspc.pages.dev","id":"did:web:csoai-gspc.pages.dev#gspc","name":"Council of AI measurement gatekeeper","description":"Independent governance MEASUREMENT body. Measures, signs, publishes — never certifies.","did":"did:web:csoai-gspc.pages.dev","capabilities":["measure","verify","jail-probe","enter-arena","route","register"],"endpoints":[{"protocol":"mcp","url":"https://csoai-gspc.pages.dev/mcp"},{"protocol":"http","url":"https://csoai-gspc.pages.dev/api/gspc"},{"protocol":"a2a","url":"https://csoai-gspc.pages.dev/.well-known/agent-card.json"}],"jurisdiction":"UK/EU","witnessed_at":"2026-08-24T16:06:40.145Z","content_id":"cf346bd05b111ed5ae90fea2ec2068228923a046bf5f3d8a01338cb5a65a6391","signature":"Z+xiMXi5NECC9sbrYw431NRif+hOKpMTUI2nyabd7wOkI0oRUkAEWGwIyD3zh/CuebO1ECalzRczc4+yKrm/BQ==","pubkey":"54bc68205ba96421e355cdf1c320827bf473c2b84bd5ed764c736204c548c78e","key_id":"did:web:csoai-gspc.pages.dev#gspc","verification_method":"did:web:csoai-gspc.pages.dev#gspc","did_resolver":"https://csoai-gspc.pages.dev/.well-known/did.json"};
export async function onRequest(context){
  const headers={'content-type':'application/json','access-control-allow-origin':'*','access-control-allow-methods':'GET,OPTIONS'};
  if(context.request.method==='OPTIONS')return new Response(null,{status:204,headers});
  return new Response(JSON.stringify(CARD),{status:200,headers});
}
