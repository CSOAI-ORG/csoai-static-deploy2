# bridges — the "wrap not replace" proof

Doctrine-clean bridge tools that turn legacy/static estate data into machine-readable form
WITHOUT migrating it. Each is a real, runnable, tested tool — a parser/translator, never a
money or settlement layer. [BUILT]

## cobol_copybook.py — COBOL COPYBOOK → JSON

Reads a COBOL COPYBOOK (01-level record + PIC field definitions) and parses fixed-width COBOL
records into JSON. The "wrap not replace" proof: legacy mainframe batch data becomes
machine-readable without touching or migrating the mainframe.

```
python3 bridges/cobol_copybook.py --selftest
```

Handles the common COBOL DISPLAY PICs: `X(n)` (alphanumeric), `9(n)` (unsigned int),
`9(n)Vmm` / `S9(n)Vmm` (implied decimal — the `V` is not in the record; sign detected via a
trailing `-`/overpunch, documented as conservative, never zoned/SWIFT assumed).

### The doctrine boundary (don't cross it)

The parser is a **reference/read** tool. The settlement (smart-contract atomic DvP), tokens,
staking, agent wallets, and data-DAO layers described in the full bond-market vision are
**Phase 2 crypto — compliance-gated** (`ops/EUNOMIA_PHASED_PLAN_2026-08-23.md`): Nick's go +
legal/securities review + audit. This repo does NOT contain or scaffold any of that. The
parser stops at "legacy data → machine-readable JSON," which is the honest, buildable core.
