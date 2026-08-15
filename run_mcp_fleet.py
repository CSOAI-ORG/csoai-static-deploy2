"""run_mcp_fleet.py — score the gspc-mcp bank across a DECORRELATED OpenRouter fleet.

The local board was UNMEASURED because the fleet (many small, related models) did
not separate. This runs the same bank across one small model per lab — genuinely
decorrelated bases — which is the only thing that can move the board from
UNMEASURED to a real ranking. Cheap fleet first: a full run costs cents.

The key is read by openrouter.load_key() from OPENROUTER_API_KEY or
~/.openrouter/api_key. This script never prints or embeds it.
"""
import json, sys
sys.path.insert(0, "/runpod/board")
from sovos_city import bench, openrouter, tail

BANK = "/runpod/board/banks/gspc-mcp.items.jsonl"
PERITEM = "/runpod/board/peritem_mcp_openrouter.jsonl"
BOARD = "/runpod/board/board_mcp_openrouter.json"

key = openrouter.load_key()
if not key:
    sys.exit("NO OPENROUTER KEY — put it in ~/.openrouter/api_key or export OPENROUTER_API_KEY, then re-run.")

budget = openrouter.Budget(cap_usd=2.0)          # conservative hard cap; cheap fleet costs cents
fleet = openrouter.CHEAP_FLEET                    # decorrelated: OpenAI/Google/Meta/DeepSeek/Mistral
models = [m.slug for m in fleet]
print(f"  fleet ({len(models)} decorrelated labs): {', '.join(models)}")

def ask_fn(model, prompt):
    return openrouter.ask_openrouter(model, prompt, key, budget)

board = bench.board("mcp", BANK, models, ask_fn, per_item_path=PERITEM)
json.dump(board, open(BOARD, "w"), indent=2)

print(f"\n  status: {board['status']}   best: {board['best']}")
for r in board["models"]:
    print(f"    {r['model']:34} acc={r['accuracy']} ci={r['ci95']} n={r['n']}")

rows = tail.load_rows(PERITEM)
st = tail.tail_stats("mcp", rows)
print(f"\n  correlated-failure: {st.correlated_failure_rate:.1%}  "
      f"({len(st.fleet_fragile_items)} items broke the whole fleet)")
print(f"  spent: ~${budget.spent_usd:.3f} of ${budget.cap_usd:.2f} cap")
print(f"\n  wrote {BOARD} and {PERITEM}")
print("  next: sign with `python3 /runpod/article50/sign.py --sign " + BOARD + "` (signing node)")
