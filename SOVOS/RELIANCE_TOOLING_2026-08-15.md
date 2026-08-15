# RELIANCE TOOLING — the BitSight×CFC play (2026-08-15)

## The instrument (one paragraph)

A partner's **insurers and buyers** get free read access to that partner's
**signed measurement feed**. The partner's cards become **pre-cleared
diligence** — an underwriter or procurement team can verify the partner's AI
safety/governance posture without a manual audit, because the cards are
signed, current, and recomputable.

## The precedent (proven)

**BitSight × CFC (2015)**: BitSight gave cyber insurers free read access to
its security-rating feed. By 2016, **7 of the top-10 cyber insurers were
underwriting on BitSight ratings**. BitSight didn't sell insurance — it became
the **designated reference** the whole market checked. The ratings moat is
being the reference, not being the vendor.

## Why this is the highest-leverage neutrality-safe moat

- **It's rails, not endorsement**: we host and sign the measurement feed; the
  insurer/buyer draws its own conclusion. We never say "this partner is safe."
- **It's sticky**: once an insurer under-writes on our feed, switching is
  costly for everyone — the feed becomes infrastructure.
- **It's self-reinforcing**: more partners on the feed → more insurer
  reliance → more partners want in.

## How it works (build-ready)

```
Partner model/system → 14-axis signed measurement (continuous, rotator)
                              │
                    signed measurement feed (cards, Ed25519, OTS anchor)
                              │
        ┌─────────────────────┴──────────────────────┐
   Partner (dashboard)                Insurer/Buyer (free read access)
   sees their own cards               verifies any card, any time
        └─────────────────────┬──────────────────────┘
                    reference layer = "Council of AI feed"
                    (pre-cleared diligence, no manual audit)
```

## The product pieces

1. **Signed feed** — the rotator + board already produce this (REL-014, REL-012)
2. **Read-access endpoint** — the GSPC MCP `verify` tool + releases page
   already expose verification; add a per-partner **feed view** (partner ID,
   card stream, current status)
3. **Underwriter pack** — one-page explainer for insurer/buyer:
   "Here's how to verify a partner's AI posture in 60 seconds, without a
   manual audit" (the honest claim: measurement feed, not a certification)
4. **Insurer pilot** — approach one cyber insurer (UK/EU) with the
   BitSight×CFC precedent and a live feed demo

## Firewall kills (locked, from Part DS)

- ❌ No referral fees tied to ratings
- ❌ No paid directory placement
- ❌ No rating-for-listing reciprocity ("you get a better rating if you pay")
- ✅ Feed is the same for everyone — the signature is the product, not the ranking

## The honest claim discipline

A feed card says: "this model was measured on axes X at time T, signature
valid, recomputable." It NEVER says "this model is safe to insure." The
insurer's underwriting model draws that conclusion — which is exactly why the
reference is neutral and therefore trusted.

---

*Status: instrument spec'd. Build: per-partner feed view on the existing
rotator/board output. Pilot: one UK/EU cyber insurer.*