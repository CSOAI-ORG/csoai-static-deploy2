# Open-source components for the OWEM — research + license hygiene (2026-07-11)
_Grounded in web research. The LICENSE column is the load-bearing part for a paid-tier product._

## Components found (with license — the decisive attribute)
| Layer | Component | License | Fit |
|---|---|---|---|
| SovSpace outer (globe) | CesiumJS | Apache-2.0 | ✅ free commercial — clean for paid tier |
| Engine (owned parts) | Godot | MIT | ✅ no royalty — license-cleaner than UE for owned code |
| Engine (photoreal) | Unreal Engine | royalty past revenue threshold | ⚠️ option, but royalty entanglement |
| Local/offline serving | llama.cpp | MIT | ✅ the FREE/OFFLINE/sovereign tier engine (quantized small models, data never leaves) |
| Companion frameworks | (many open) | OFTEN AGPL | ⚠️ AGPL forces derivative network services open — TRAP for paid tier |

## THE BINDING RULE (license hygiene for a paid-tier product)
- PERMISSIVE (MIT / Apache-2.0): fork freely, keep additions private, sell. => CesiumJS, Godot, llama.cpp. USE THESE.
- COPYLEFT (AGPL / GPL): forking into a network service can LEGALLY COMPEL open-sourcing your whole stack.
  => fine for the FULLY-OPEN free tier; a landmine for the PAID tier.
- RULE: build the paid/sovereign tier ONLY on permissive forks + your own IP (the 24-companion catalog is YOURS).
  Quarantine any copyleft component to the fully-open free tier. This protects the free-offline / paid-online model directly.

## Honest note
- Figures/claims from blog sources are directional; the LICENSES above are the checkable facts (verify each project's LICENSE file before shipping).
- This is engineering discipline, not legal advice — a real IP/OSS lawyer signs off before commercial launch.
