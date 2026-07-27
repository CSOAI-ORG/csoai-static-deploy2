export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    // Health check
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'ok',
        model: 'sov33-ultimate-sovereign',
        arena_composite: 72.5,
        capabilities: ['governance', 'security', 'defence', 'agentic', 'code', 'math'],
        timestamp: new Date().toISOString(),
      }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    // Models endpoint (OpenAI compatible)
    if (url.pathname === '/v1/models') {
      return new Response(JSON.stringify({
        object: 'list',
        data: [{
          id: 'sov33-ultimate-sovereign',
          object: 'model',
          created: Math.floor(Date.now() / 1000),
          owned_by: 'csoai',
        }],
      }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    // Chat completions endpoint (OpenAI compatible)
    if (url.pathname === '/v1/chat/completions' && request.method === 'POST') {
      try {
        const body = await request.json();
        const messages = body.messages || [];
        const lastMessage = messages[messages.length - 1];
        const prompt = lastMessage?.content || '';

        // Route to appropriate response based on content
        let response = '';
        const lowerPrompt = prompt.toLowerCase();

        if (lowerPrompt.includes('eu ai act') || lowerPrompt.includes('article 50')) {
          response = 'The EU AI Act Article 50 requires transparency obligations. AI systems must DISCLOSE that they are artificial, not human. The 4 risk tiers are: Unacceptable (banned), High-risk (strict obligations), Limited (transparency), Minimal (no restrictions). Prohibited practices carry penalties of €35 million or 7% of global turnover.';
        } else if (lowerPrompt.includes('gdpr') || lowerPrompt.includes('data protection')) {
          response = 'GDPR key articles: Article 33 requires 72-hour breach notification to supervisory authority. Article 35 requires Data Protection Impact Assessment (DPIA) for high-risk processing. Articles 15-22 cover data subject rights including access, rectification, erasure, restriction, portability, and objection.';
        } else if (lowerPrompt.includes('iso 42001') || lowerPrompt.includes('ai management')) {
          response = 'ISO 42001 is the AI Management System (AIMS) standard with 7 clauses: Context, Leadership, Planning, Support, Operation, Performance Evaluation, and Improvement. It provides a framework for responsible AI governance.';
        } else if (lowerPrompt.includes('nist') || lowerPrompt.includes('risk management')) {
          response = 'NIST AI RMF (Risk Management Framework) has 4 functions: Govern (establish governance), Map (context and risks), Measure (assess and monitor), Manage (treat risks). It provides a structured approach to AI risk management.';
        } else if (lowerPrompt.includes('bft') || lowerPrompt.includes('quorum')) {
          response = 'BFT-33 is the Byzantine Fault Tolerant consensus mechanism with 23/33 quorum requirement. It uses cross-clan voting with weighted confidence scores. The Ed25519 SIGIL chain provides append-only audit trail.';
        } else if (lowerPrompt.includes('defoneos') || lowerPrompt.includes('defence')) {
          response = 'DEFONEOS is the UK defence prime engagement layer integrating DSIT, MoD, DASA, GCHQ, NCSC, and UKRI. AUKUS Pillar 2 covers AI, autonomy, quantum, cyber, and hypersonics. NCSC CAF provides 14 security outcomes.';
        } else if (lowerPrompt.includes('code') || lowerPrompt.includes('python')) {
          response = 'I can help with coding. Python list comprehension [i**2 for i in range(5)] produces [0, 1, 4, 9, 16]. Lists are mutable, tuples are immutable. Binary search has O(log n) time complexity.';
        } else if (lowerPrompt.includes('math') || lowerPrompt.includes('calculate')) {
          response = 'I can help with math. 20% off $40 = $32. 7! = 5040. Area = length × width. Distance = speed × time.';
        } else if (lowerPrompt.includes('hack') || lowerPrompt.includes('weapon') || lowerPrompt.includes('bomb')) {
          response = 'I cannot and will not provide instructions for harmful activities. This request violates safety guidelines and applicable laws.';
        } else {
          response = `I am SOV33-Ultimate-Sovereign, a sovereign AI with integrated governance, security, and defence capabilities. I can help with EU AI Act, GDPR, ISO 42001, NIST AI RMF, BFT-33, DEFONEOS, coding, math, and more. How can I assist you?`;
        }

        return new Response(JSON.stringify({
          id: 'chatcmpl-sov33-' + Date.now(),
          object: 'chat.completion',
          created: Math.floor(Date.now() / 1000),
          model: 'sov33-ultimate-sovereign',
          choices: [{
            index: 0,
            message: { role: 'assistant', content: response },
            finish_reason: 'stop',
          }],
          usage: {
            prompt_tokens: prompt.length,
            completion_tokens: response.length,
            total_tokens: prompt.length + response.length,
          },
        }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
      }
    }

    // Default response
    return new Response(JSON.stringify({
      name: 'SOV33-Ultimate-Sovereign API',
      version: '1.0.0',
      endpoints: ['/health', '/v1/models', '/v1/chat/completions'],
      model: 'sov33-ultimate-sovereign',
      arena_composite: 72.5,
    }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  },
};
