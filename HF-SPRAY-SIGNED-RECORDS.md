---
license: mit
task_categories:
  - text-classification
tags:
  - ai-governance
  - benchmark-quality
  - regulatory-compliance
  - signed-measurement
  - ed25519
  - measurement-not-certification
language:
  - en
pretty_name: CSOAI Benchmark-Quality + Regulatory Deadline Records
size_categories:
  - n<1K
---

# CSOAI Signed Measurement Records — HF Spray Pack

Two living, Ed25519-signed, machine-discoverable records from the Council of AI
(CSOAI Ltd, UK 16939677). Every record is deterministic (no LLM judge), chained,
and offline-verifiable. **Measurement, not certification. Verification free forever.**

## 1. Benchmark-Quality Register (`benchmark-quality-feed.json`, `csoai.benchmark-quality/0.1`)

Rates **third-party benchmark quality** from public artifacts only — never an
LLM judge. BetterBench criteria × OpenSSF Scorecard check design.

| Benchmark | Score | Integrity |
|---|---|---|
| ARC-AGI-3 (interactive) | 34.6/42 | 82.4% |
| SWE-bench Verified | 26.5/42 | 63.1% |
| MMLU | 23.2/42 | 55.3% |
| Terminal-Bench 2.x | 22.2/42 | 52.9% |
| GPQA | 22.0/42 | 52.4% |
| Chatbot Arena (LMArena) | 10.4/42 | 24.8% |

**Impartiality firewall (ISO/IEC 17020/17025): CSOAI's own boards are never
scored here.** Every record: `solicited:false · party_participated:false ·
access:public_artifacts_only · not_a_certification:true`.

## 2. Regulatory Deadline Record (`regulatory-deadline-record.json`, `csoai.regulatory-deadline-record/0.1`)

Regime-level process facts: **did the regulator hit the date it set itself?**
held / stated / deferred. Self-benchmarked, un-scored, un-ranked, no named
officials (Derbyshire shield). Never a league table.

Current deferrals (verified): EU AI Act Art 50(2) marking grace → 2026-12-02 ·
Annex III high-risk → 2027-12-02 · Annex I regulated products → 2028-08-02
(Digital Omnibus, Reg (EU) 2026/1744).

## Verify

```bash
# each record: content_id = sha256(canonical body, RFC 8785 JCS)
# signature = Ed25519(content_id) under the embedded pubkey; prev chains
python3 - <<'PY'
import json, hashlib, base64
from nacl.signing import VerifyKey
feed = json.load(open('benchmark-quality-feed.json'))
for r in feed['records']:
    body = {k: v for k, v in r.items() if k not in ('content_id','signature','prev','pubkey')}
    cid = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',',':')).encode()).hexdigest()
    assert cid == r['content_id']
    VerifyKey(bytes.fromhex(r['pubkey'])).verify(cid.encode(), base64.b64decode(r['signature']))
print('all records verify')
PY
```

## Live surfaces
- Register: https://csoai-site.pages.dev/benchmark-quality · feed: /benchmark-quality-feed.json · API: /api/benchmark-quality
- Deadline record: https://csoai-site.pages.dev/regulatory-deadline · feed: /regulatory-deadline-record.json · API: /api/regulatory-deadline
- Open in the AG-UI: every page carries `data-agui` routing that opens the living harness with the right task prompt.

**The line: measurement, not certification. Verification free forever. Nobody ranked pays, humans never pay.**
