// /api/owem — the canonical OWEM manifest. ONE source of truth for how the sovereign mind is tiered,
// so every surface (workspace brains, council, chat, MCP) routes the same way and it's inspectable.
//
// The honest semantics (grounded in the real models in sov33_compute.py + /api/chat):
//   • SOV33      = the MIND. Not a size. Owns the persona, memory, governance (care-floor + Ed25519),
//                  the tool fleet, and all three OWEM tiers.
//   • character  = the MIND's face/embodiment (named + archetyped per user). Same mind, your face.
//   • OWEM tiers = real models the mind routes to BY JOB, not by identity. Care-floor gates every emit.
export default function handler(req, res){
  res.setHeader('Access-Control-Allow-Origin','*'); res.setHeader('Cache-Control','public, max-age=300');
  return res.status(200).json({
    spec: 'meok.owem.v1',
    mind: 'SOV33',
    embodiment: 'the character (your named, archetyped Sovereign) — same mind, your face',
    governance: { care_floor: 0.95, signing: 'Ed25519 (SIGIL)', note: 'every tier’s OUTPUT is care-floored + signed before it emits — that, not model size, is what makes it sovereign' },
    tiers: {
      small: { job: 'reflex / presence', model: 'llama-3.1-8b-instant', size: '8B',
               does: ['predictive typing', 'intent detection', 'which surface to open', 'interim drafts', 'the workspace RIGHT brain'],
               runs: 'groq (sub-second) or local Ollama — cheap, always-on, can be offline', tier_param: 'small' },
      medium:{ job: 'tools / agent', model: 'llama-3.3-70b-versatile', size: '70B',
               does: ['the everyday voice', 'tool-router (picks MCP cards)', 'the PDCA action loop', 'orchestration'],
               runs: 'groq 70B (default) → OCI 70B (sovereign, signed)', tier_param: 'medium' },
      large: { job: 'deep / verify', model: 'openai/gpt-oss-120b (or Claude via key)', size: '120B',
               does: ['careful reasoning', 'governance adjudication', 'Council synthesis', 'the workspace LEFT brain'],
               runs: 'groq 120B → Claude/GPT with the user’s own key (Council)', tier_param: 'large' },
    },
    maps_to_question: {
      'is the character a small OWEM?': 'no — the character is the embodiment; SMALL is its fast reflex',
      'is SOV33 a size?': 'no — SOV33 is the whole mind that owns all three tiers',
      'medium is for tools?': 'yes — medium (70B) is the tools/agent tier',
      'large is for SOV33?': 'large (120B/Claude) is the DEEP tier SOV33 routes to for hard/verify work',
    },
    usage: 'POST /api/chat with { message, tier: "small"|"medium"|"large", persona } — tier picks the real model.',
  });
}
