# MVT 5 — FIX LOOP & SECURITY (design layer)

Date: 2026-08-22 · lane: K3 (spec) / LANE (code) · REAL: autonomy defaulted ON in-window, unsigned
gates everywhere (H21/H22).

## 1. Signed-recipe gate (step 151, 👑)
Claude Code managed HTTP `PreToolUse` hooks: verify signature + consent token.
`allowManagedHooksOnly` blocks overrides. Exploit flooring: hook ask floors auto mode (survives
the Aug 14 default). Gate: unsigned recipe hard-fails e2e.

## 2. DeepJack mitigation matrix (step 158, 👑)
`cursor://`, `warp://`, `vscode://mcp/install`, `windsurf://` — coverage page + gate rules.
Deeplink-install detector: base64-blob installs + nested double-encoded URIs (catches both
DeepJack tricks). Status: disclosed Jul 15, duped to Apr 27, reproducible in 3.9.8, no vendor
response, no CVE (H4, D05 §1).

## 3. Shai-Hulud config-integrity counter (step 161, 👑)
Signed config manifests — hooks/tasks load only if user/org-key signed. Hash-pin configs at
workspace-trust time; drift alerts. Design note: provenance verifies WHERE, not WHAT (keyv@6.0.0
lesson).

## 4. Marketplace spoofing counter (step 167)
Publisher signing + name↔key binding. (Codex #39165; strictKnownMarketplaces wave, D05 §4/§6).

## 5. Recipe artifact (step 154)
JSON + Sigstore keyless signature (issuer, scope, expiry). Upsell whitelist enforced in emitter;
affiliate/referral money banned permanently (R1). Bridge executes client-side under the client's
gate (R2 — never server-side exec).

## 6. Honest status
Spec layer DRAFTED; code = LANE. Kill criteria: vendor ships native signed-config gate → we
differentiate on independence, not mechanism.
