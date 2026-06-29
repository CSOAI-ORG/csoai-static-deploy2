# 🐉 MEOK OS — Telemetry API (analytics, error tracking, perf)

A simple analytics + error tracking + perf endpoint for the MEOK OS.

## Endpoints

### POST /api/telemetry/page
Record a page load. Body:
```json
{"page": "/os", "user_agent": "Mozilla/5.0...", "load_ms": 230}
```

### POST /api/telemetry/error
Record a JS error. Body:
```json
{"page": "/os", "message": "TypeError: ...", "stack": "..."}
```

### POST /api/telemetry/event
Record a custom event. Body:
```json
{"event": "ichar_created", "queen_model": "queen-arcana", "arcana_lens": 21}
```

### GET /api/telemetry/stats
Get aggregated stats.

## Usage

From any page:
```javascript
fetch('/api/telemetry/event', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({event: 'queen_summoned', queen: 'Sophia Care'})
});
```

## Stored at
- `meok-backend/telemetry.jsonl` (append-only JSONL)
- Aggregated in-memory for /stats
