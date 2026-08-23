# SOV33-Ultimate-Sovereign API Documentation

## Base URL
```
https://sov33-api.nicholastempleman.workers.dev
```

## Authentication
No authentication required for free tier.

## Endpoints

### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "ok",
  "model": "sov33-ultimate-sovereign",
  "arena_composite": 72.5,
  "capabilities": ["governance", "security", "defence", "agentic", "code", "math"],
  "timestamp": "2026-07-27T06:22:00.081Z"
}
```

### List Models
```http
GET /v1/models
```

Response:
```json
{
  "object": "list",
  "data": [{
    "id": "sov33-ultimate-sovereign",
    "object": "model",
    "created": 1785133331,
    "owned_by": "csoai"
  }]
}
```

### Chat Completions
```http
POST /v1/chat/completions
Content-Type: application/json
```

Request:
```json
{
  "messages": [
    {"role": "user", "content": "What is the EU AI Act Article 50?"}
  ]
}
```

Response:
```json
{
  "id": "chatcmpl-sov33-1785133331479",
  "object": "chat.completion",
  "created": 1785133331,
  "model": "sov33-ultimate-sovereign",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "The EU AI Act Article 50 requires transparency obligations..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 33,
    "completion_tokens": 327,
    "total_tokens": 360
  }
}
```

## Usage Examples

### Python
```python
import requests

response = requests.post(
    "https://sov33-api.nicholastempleman.workers.dev/v1/chat/completions",
    json={"messages": [{"role": "user", "content": "What is GDPR Article 33?"}]}
)
print(response.json()["choices"][0]["message"]["content"])
```

### JavaScript
```javascript
const response = await fetch("https://sov33-api.nicholastempleman.workers.dev/v1/chat/completions", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({messages: [{role: "user", content: "What is BFT-33?"}]})
});
const data = await response.json();
console.log(data.choices[0].message.content);
```

### cURL
```bash
curl -X POST https://sov33-api.nicholastempleman.workers.dev/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is DEFONEOS?"}]}'
```

## Capabilities

### Governance
- EU AI Act Article 50 (transparency, 4 risk tiers, €35M/7% penalties)
- ISO 42001 (AI Management System - 7 clauses)
- NIST AI RMF (Govern, Map, Measure, Manage)
- OECD AI Principles (inclusive growth, human-centered)
- GDPR Articles 15-22, 33, 35

### Security
- 2,740 safety entries (refusal, prompt injection, red-teaming)
- BFT Quorum (2/3+1 threshold)
- God's Eye omniscient scanner
- 71 sigil attestations

### Defence
- DEFONEOS (DSIT, MoD, DASA, GCHQ, NCSC, UKRI)
- AUKUS Pillar 2 (AI, autonomy, quantum, cyber)
- NCSC CAF (14 outcomes)
- NATO DIANA, Five Eyes

### Agentic
- Hermes Conductor (4-lane delegation)
- ASI Evolve (self-improvement loop)
- Swarm (multi-node consensus)
- Autonomous Agent (browser, forms, code, research, plan)

### Code & Math
- Python, SQL, algorithms
- Binary search O(log n), Prime O(sqrt n)
- 20% off $40 = $32, 7! = 5040

## Rate Limits
Free tier: 100 requests/day

## Error Codes
- 200: Success
- 400: Bad request
- 403: Forbidden
- 500: Server error

## Links
- GitHub: https://github.com/CSOAI-ORG/csoai-static-deploy2
- Website: https://csoai.org
- Model Card: huggingface/sov33-ultimate-sovereign
