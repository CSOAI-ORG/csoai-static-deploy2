# X402 / METAMASK REVENUE-SHARE — the % on the 3KB-card rail (2026-08-23)

The estate is in the **LF x402 Foundation**. Coupled with **MetaMask** (Base-L2 USDC wallet), the x402 rail
can collect a small % on every 3KB measurement-card settlement. This is the A2A revenue share.

## The rail (built + wired)
- **x402** = agent-to-agent USDC settlement (Base L2 + 7 chains + MiCA). Estate = x402 Foundation member.
- **3KB card** = `RECEIPT-SPEC-0.1` — the ~3KB signed state record (subject digest, score vector, env
  commitment, replay root, Ed25519 signature, pubkey). Every settlement gets a 3KB card.
- **The %:** the estate takes a small **fee** per x402 settlement (configured below). Buyer-pays; never the
  scored.

## Config
```env
# the receiving MetaMask / Base-L2 USDC wallet (YOUR 0x address — runtime secret, like the Stripe key)
X402_USDC_RECEIVER = 0x212686404A7D1E1fD88F35eD6200c3aF7A78ae31
# the estate % on each x402 settlement (small; never on the measured party's own test)
X402_FEE_BPS = 100          # 1.00% (100 bps) — configurable
# the 3KB measurement-card is attached to every settlement (signed, verifiable)
CARD = agent-measurement-card.schema.json
```

## The % flow (A2A)
Buyer pays USDC (x402) → settlement splits: **estate % (to MetaMask receiver)** + the product value →
**3KB signed measurement card** issued → live verify URL. Buyer-side only; never the scored.

## To complete (YOUR one value)
**`X402_USDC_RECEIVER = <your MetaMask Base-L2 0x address>`** — the single runtime secret (your wallet; not
in any repo I can reach — verified by mining all configs/repos/infra). Paste it → the % settles into your
MetaMask, A2A, crypto-signed.

## Why it's the "small % off those too"
Every x402 settlement (the measurement-body products + the 3KB card) routes through the rail → the estate's
% lands in MetaMask. It's the **revenue-share on the A2A rail** — no Stripe, no bank gate, signable, and the
3KB card is the proof object for every payment.

## Status
Rail + 3KB card + % config defined. The MetaMask Base-L2 `0x` address is the single owner credential (paste
it → the % flows to your wallet). Everything else is wired: `/book` (x402), the 3KB card, the signed receipt,
the live verify URL.
