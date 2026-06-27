# READY TO FIRE: Public OpenPatent Push
# Time: 1 minute (after your "yes")
# Pre-req: Your explicit "yes publish" decision

## 7 Inventions Already Filed Locally

From `~/clawd/sovereign-town/openpatent_6layer_receipts.json`:

| # | Invention | Bitcoin TX | Status |
|---|---|---|---|
| 1 | Sovereign Substrate + Charter | 304d51ea... | DISCLOSED |
| 2 | Agent Passport + Narrowing | 4f3a92b7... | DISCLOSED |
| 3 | Maternal Covenant Care Floor | 8c12da44... | DISCLOSED |
| 4 | Sovereign Town Flywheel | 92e4bc61... | DISCLOSED |
| 5 | Per-Hive Threat Models | b71fc982... | DISCLOSED |
| 6 | Looking Glass (Jurisdiction Sim) | 5a39e8d3... | DISCLOSED |
| 7 | Pheromone Bus (Cross-Hive Alarm) | e721cd04... | DISCLOSED |

## What "push" means

Pushing = publishing to the **public** openpatent registry.

When you push:
- ✓ Prior art established (legally strong — 35 USC 273, Article 55 EPC)
- ✓ Bitcoin-anchored forever (already done locally)
- ✓ Discoverable by competitors (they can read it but can't patent it)
- ✗ Can NOT be re-patented by anyone (including us)
- ✗ Competitors see the design (that's the point)

## To push (when ready)

```bash
# 1. Review the 7 inventions
cat ~/clawd/sovereign-town/openpatent_6layer_receipts.json | jq '.[].title'

# 2. If you say "yes publish":
cd ~/clawd
git add sovereign-town/openpatent_6layer_receipts.json
git commit -m "feat(openpatent): confirm 7 sovereign-town inventions as prior art"
git push origin main

# 3. Then (separately, requires your consent + account):
# Push to public openpatent.ai registry via patentmcp deploy
```

## Critical decision matrix

| Your risk tolerance | Recommendation |
|---|---|
| Want max legal protection NOW | Push all 7 immediately |
| Want to wait for design-partner convos | Push top 3 first (substrate, passport, flywheel) |
| Want to keep trade secrets | Don't push, file patent instead (costs $30K+) |
