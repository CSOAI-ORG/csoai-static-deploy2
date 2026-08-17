# Train Ledger v0 — versioned fine-tune set registry (IP-6, Firewall-2 gated)

The registry of versioned fine-tune sets derived from the signed canon corpus. **Firewall 2 stands: judge/scorer models are never trained on honey/containment data; any IP-6 work passes counsel review first.**

## What lives here
- Versioned fine-tune set manifests (what's in, what's excluded, why)
- The held-out split doctrine: train never equals test; the anti-Goodhart separation is the secrecy boundary
- Review checklist per set (counsel sign-off required before any train run)

## Why a ledger
Verdicts, corrections, and review outcomes feed the ledger; judge quality improves per cycle — but only behind the firewall, and only with a held-out bank that never touches training. The ledger makes the split auditable.

## Guard (unrelaxed)
A fine-tuned judge is a measurement tool, not a marketing claim. No judge output ships as a measurement without the deterministic core behind it.
