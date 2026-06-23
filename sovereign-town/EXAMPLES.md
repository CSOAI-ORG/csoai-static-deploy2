# Sovereign Town — Usage Examples

## 1. Run a benchmark

```bash
cd p0_aqua
./.venv/bin/python -m benchmark run --policy dora_automated --scenario dora_incident_deadline --sign
```

This produces a signed manifest in `benchmark_runs/` and prints a run ID.

## 2. Verify a signed manifest

```bash
./.venv/bin/python -m benchmark verify --manifest benchmark_runs/<id>.json
```

Or use the browser verifier at `/verify` and paste the JSON.

## 3. Run the Policy Lab DORA experiment

```bash
./.venv/bin/python policy_lab.py vote experiments/dora_finance.json
./.venv/bin/python policy_lab.py spawn experiments/dora_finance.json --live
./.venv/bin/python policy_lab.py report experiments/dora_finance.json
```

The regulator view is written to `proofof-site/sovereign-town/experiments/dora-finance.html`.

## 4. Generate a new regulation experiment

Create `intake.json`:

```json
{
  "regulation": "EU AI Act",
  "framework": "eu_ai_act",
  "industry": "healthcare",
  "civilization": "Aethelgard",
  "hypothesis": "Prohibited-practice bans reduce manipulative agent actions",
  "articles": ["Art. 5 Prohibited AI practices"]
}
```

Then:

```bash
./.venv/bin/python policy_lab.py auto-spawn intake.json --live
```

## 5. Call an MCP tool through the dashboard proxy

```bash
curl -N http://127.0.0.1:3940/mcp/sse
```

Connects to the SSE stream. The `/workbench` page has a built-in MCP client UI.

## 6. Use the dashboard API

```bash
# Health
curl http://127.0.0.1:3940/api/health

# List experiments
curl http://127.0.0.1:3940/api/experiments

# SOV3 bridge handshake
curl http://127.0.0.1:3940/api/sov3/handshake
```

## 7. Run the full test suite

```bash
cd p0_aqua
./.venv/bin/python selftest.py
# (with services running)
./.venv/bin/python e2e_test.py
.venv-playwright/bin/python -m pytest browser_test.py
```
