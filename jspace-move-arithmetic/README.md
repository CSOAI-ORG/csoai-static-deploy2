# J-Space Move Arithmetic

**Task-vector composition for self-healing routing in multi-clan AI systems.**

This is the novel artifact: applying the same math as MergeKit (TIES, DARE,
error-vector subtraction) to chess-board moves instead of neural-network
weights.

## What it does

- **TIES-Move** — trim/elect-sign/merge across candidate moves. Errors get voted out by majority.
- **DARE-Move** — random dropout + rescale. Prune redundant moves; keep load-bearing ones.
- **Error-Vector Subtraction** — represents failure modes as NEGATIVE task vectors. `move* = move − λ·ε_error`. Preemptively blocks doomed queries.
- **Router** — composes all three. Deterministic. No `while True`. No recursion.

## Run it

```bash
PYTHONPATH= python3 tests/test_move_arithmetic.py
```

Expected: `✅ 7/7 tests PASSED`

## Why it's novel

Task-vector arithmetic (Ilharco 2023, Yadav 2023, Yu 2023) has been applied
exclusively to neural-network weights. We extend it to **routing decisions**.

Result: a router that learns from every crash without recursive re-planning.
Every crash becomes a permanent `−ε_error` in the database, applied to all
future moves. Wasted inference on doomed queries: eliminated.

## Paper

See `papers/arxiv-jspace-move-arithmetic.md` for the full preprint.

## License

MIT — CSOAI Ltd (UK 16939677)