# Durability Probe Resolutions — 2026-08-13 (mined, not assumed)

Resolving the Part CE/CB durability flags by probing actual hosts — receipts, not
docs. All verified live this session.

## 1. The 4 sovereign GGUFs — DURABLE (both hosts) ✅
The "truncated GGUF tarball" (Part CE) is a **transient consolidation convenience
copy, NOT the authoritative store.** The real models live in each pod's ollama
blob store with MATCHING digests across two independent hosts:

| model | digest | 3090 | A100 |
|---|---|---|---|
| sov-safety-v1 | 9099a3c385da | ✅ | ✅ |
| sov-merge-slerp-gguf | ad2c104a3060 | ✅ | ✅ |
| sov-merge-dare-gguf | cb100aab53ab | ✅ | ✅ |
| sov-refusal-combo-lora | eb45e430d588 | ✅ | ✅ |

Digest equality across hosts = the integrity receipt (same blobs, both machines).
**3-copy durability satisfied** (git/HF + persistent volume + 2 pod hosts).

## 2. specialists training data — SOURCE INTACT ✅
`specialists_v1.tar.gz` truncation is likewise a convenience-copy issue. The real
source JSONL is on 3090:
- safety_mixed.jsonl (314KB) · care_mixed.jsonl (3.4MB) · privacy_mixed.jsonl (390KB)
- normalize.py present
- Plus a 12GB `/workspace/mac-backup` tree (incl. sovereign_merge_kit, alliance_contrib)

## 3. Disk pressure — REAL but improved
- 3090: / at **79%** (was 90%) — arena migrated or cleaned; 6.4GB free
- A100: / at **50%** — 51GB free, healthy

## Action added
No re-archive urgent on GGUFs/specialists (source durable). Disk pressure on 3090
is manageable but the 4 sovereign GGUFs + a valid backup should be the first thing
off that host when the owner authorizes a mirror (they already exist on A100, so
the 3090 pressure is not a single point of loss).