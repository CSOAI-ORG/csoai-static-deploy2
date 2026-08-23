# STRANGER-VERIFIABLE RECEIPT — Ed25519 (2026-08-22)

## The artifact
`SOVOS/evidence/csoai-verdict-signed-ed25519-2026-08-22.json` (1,528 B)
= the clean sequential EAT measurement, signed on the signing node.

## The signature
- kind: `ed25519`
- pubkey (PUBLISH — verification key): `bWbk52E47J6EkY4+pu0Hh/B1l1175AZoZsDEBr0EfWA=`
- sig: `12F/bgnimuwF60QC0WdQTc6lCN095WcqWpXLo8Nsug2i1j6Cri6OtZDWze8/hLw8HlLNL0AKzbzfj0ZorxSVCw==`
- body_sha256: `964266a22283e96fbbd2c5f15778a053eac8ed33cc4ad54bb1c1c92db03f7757`
- verified: **✅ VALID** (`sign.py --verify` → "signed by the holder of the published key and is unaltered")

## How a stranger verifies (no trust, no key)
1. Take the artifact's `signature.pubkey` (or the published key above).
2. Recompute the canonical body (remove `signature`/`sha256`/`sig` fields, `json.dumps(sort_keys)`).
3. Verify Ed25519: `verify(base64decode(sig), public_key, canonical_body)`.
   - On-node: `python3 csoai-harness/sign.py --verify <artifact>` → `✅ VALID`.

## Discipline held
The Ed25519 **private key never left the signing node** (`oracle-micro1 145.241.232.16`,
`~/.sovos_keys/sovos_ed25519.key`, mode 0600). Signing was done ON the node. No key was copied to
the Mac; only the signed artifact + public key are published. PQC upgrade path = ML-DSA-65 via liboqs
(same body, swap primitive).

## The measurement it attests (REAL, clean sequential on 3090)
| Model | baseline → RAG |
|---|---|
| mistral:7b | 31.8 → **67.3** |
| llama3:8b | 30.8 → **66.6** |
| qwen2.5:7b | 28.0 → **63.3** |
| qwen2.5:1.5b | 26.0 → **60.5** |
| fair 0.5B | base 32.6 > sov33-v7 19.8 > sov33-evolved 11.4 |

Finding: retrieved knowledge >> trained (RAG +34–38 pts, confound-free). Measurement, not certification.
