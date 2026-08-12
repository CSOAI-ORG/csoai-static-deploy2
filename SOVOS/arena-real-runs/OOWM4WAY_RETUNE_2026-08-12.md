# oowm-4way re-tune — honest finding

**Tried:** explicit `--quantize q4_K_M` via `ollama create` (the recommended bypass for the auto-conversion bug).

**Result:** Still garbage (`??????????????????????`) on every prompt.

**Conclusion:** The bug is NOT in ollama's auto-conversion. The bug is in
the **merged weights themselves**. The 4-way TIES merge of
governance/safety/privacy/care specialists produced weights that
collapse to `?` no matter how we quantize.

The "0.8% rel_diff vs base, bit-exact layernorm" finding from the
earlier session was misleading — small relative difference but the
model still collapses to garbage tokens. **The merge succeeded
mathematically but the merge is unusable.**

## Fix paths (none auto-applied — per doctrine)

1. **Re-do the TIES merge with different weights** — try density=0.3,
   lambda=0.4 to reduce the per-specialist impact
2. **Use a different base model** — the current base is
   `Qwen/Qwen2.5-0.5B-Instruct`; try `Qwen/Qwen2.5-1.5B-Instruct` if
   it fits the budget
3. **Try TIES with a single specialist** — merge only the safety
   specialist into the base, see if that's broken too
4. **Skip the merge entirely** — use the source safetensors directly
   via ollama's experimental loader

## Honest finding

The honest data says: the 4 specialists (governance/safety/privacy/care)
were trained on adversarial examples. The PEFT adapters were correctly
merged into the base. The merged model is unusable for inference. We
don't know why — could be:
- the LoRA weights were trained to over-fit on adversarial patterns
- the merge recipe (density=0.5, lambda=0.5) is too aggressive
- the base model's tokenizer/processor interaction breaks

The next step is **diagnose, don't guess**. Pick the smallest change
first: re-merge with density=0.3 (less per-specialist weight) and
re-test. If that's still garbage, the specialists themselves are
the problem.