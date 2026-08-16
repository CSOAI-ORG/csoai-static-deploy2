# KEY CONTINUITY — CSOAI Signing Identities (2026-08-16)

**Status: binding estate note.** Two distinct Ed25519 signing identities exist.
Every public verify surface MUST label which key signed an artifact.

## The two identities

| Identity | Public key (hex) | Public key (base64) | Lives in | Signs |
|---|---|---|---|---|
| **Estate chain key** (`city_ed25519`) | `33472e026871db20cdbd99e76c47532ebfcf84b37abed5b260dae3589df5696d` | `M0cuAmhx2yDNvZnnbEdTLr/PhLN6vtWyYNrjWJ31aW0=` | Pods: `/root/.sovos/city_ed25519` (PEM) | Fleet board chains, measurement cards, release proofs, fleet-art5 chain |
| **Site/release key** (`CSOAI_ED25519_SK`) | hex of `03g9l+dVNGVEAVVWQrJU9aLtkYTN3uARd52P7DEq+8g=` (base64) | `03g9l+dVNGVEAVVWQrJU9aLtkYTN3uARd52P7DEq+8g=` | meok-keystone (macOS keychain `meok-keystone`, account `CSOAI_ED25519_SK`, 32-byte hex seed) | Site deploys, release cards, /verify worker artifacts |

## Rules

1. **Never mix.** A card signed by one key must name that key in its `pubkey` field. Both already do — keep it that way.
2. **Public verify pages publish BOTH pubkeys**, labelled "estate chain key" and "site/release key", so a third party can attribute any artifact.
3. **Canonical form** (both identities): `json.dumps(payload, sort_keys=True, separators=(",",":"), ensure_ascii=False)` → `content_id = sha256(canonical)` → Ed25519 signature over `content_id` bytes.
4. **Rotation**: if either key rotates, the OLD pubkey stays published with a `superseded-by` pointer. Evidence history is append-only; keys are never erased.
5. The keystone seed never leaves the keystone; the pod key never leaves the pods. No HMAC-fallback card ever ships.

Signed-off: Nicholas Templeman <nicholas@csoai.org>
