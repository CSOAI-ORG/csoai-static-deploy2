
/**
 * /.well-known/agent-card.json — Council of AI signed A2A agent card (AXIS 17).
 * "Our own card signed first." A stranger validates content_id + Ed25519 with the
 * did:web:csoai-gspc.pages.dev#gspc key. Measurement, not certification.
 */
import { getKey, canon, sha256hex, bytesToB64, bytesToHex } from '../api/signlib.js';
const CARD = {"@context":"https://www.w3.org/ns/agent-card/v1","schema":"csoai.agent-card/0.1","record_type":"measured-current-state","not_a_certification":true,"endorsement":"none","authored_by":"did:web:csoai-gspc.pages.dev","id":"did:web:csoai-gspc.pages.dev#gspc","name":"Council of AI measurement gatekeeper","description":"Independent governance MEASUREMENT body. Measures, signs, publishes — never certifies.","did":"did:web:csoai-gspc.pages.dev","capabilities":["measure","verify","jail-probe","enter-arena","route","register"],"endpoints":[{"protocol":"mcp","url":"https://csoai-gspc.pages.dev/api/mcp"},{"protocol":"http","url":"https://csoai-gspc.pages.dev/api/gspc"},{"protocol":"a2a","url":"https://csoai-gspc.pages.dev/.well-known/agent-card.json"}],"jurisdiction":"UK/EU","witnessed_at":"2026-08-28T00:00:00.000Z","content_id":"26e86feeb5e294dff77ec814d29355284f534e9975bbeadd42d474c35b468752","signature":"loUfK5vP86TL93N003/w2GnloDkd4AxVvZI0UyryN9TrHlJYIVfDRInq1y9qo4o3fzYKCONpib79LtKRnnJwDg==","pubkey":"51c5a7a39cafccc17995680f8af9cc893dd482659b439a8f780b501ca9e8ff98"};
export async function onRequest(context){
  const headers={'content-type':'application/json','access-control-allow-origin':'*','access-control-allow-methods':'GET,OPTIONS'};
  if(context.request.method==='OPTIONS')return new Response(null,{status:204,headers});
  return new Response(JSON.stringify(CARD),{status:200,headers});
}
