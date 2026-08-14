#!/usr/bin/env python3
"""Wire the signed-card issuance leg: sign a REAL board into a card, push to MinIO.

Fixes audit breach #2 — 'signed-cards bucket holds 0 objects'. The code existed
(measure_api._emit_card → chain.append); nothing had ever run it end-to-end and
pushed the result to the store. This does exactly that, using a genuinely
MEASURED, non-counsel-gated axis (art5 — conduct), NOT affect (counsel-gated).

Output: card JSON to stdout + written to /tmp/issued_card.json for rclone push.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, '/workspace/jeeves-exec/SOVOS/packages/sovos-city/src')
from sovos_city.chain import Chain  # noqa: E402
from sovos_city.measure_api import MeasureService  # noqa: E402

AXIS = 'art5'
BOARD_PATH = Path('/workspace/jeeves-exec/SOVOS/boards-v2-2026-08-12/board_art5.json')

# 1. Load the real board (the ProtocolRun result — genuine measurement)
board = json.loads(BOARD_PATH.read_text())
print(f'board: axis={board.get("axis")} bank_items={board.get("bank_items")} '
      f'status={board.get("status")} best={board.get("best")}')

# 2. Chain with the pod's existing key (~/.sovos/city_ed25519)
chain = Chain('/workspace/jeeves-exec/SOVOS/issuance-chain.jsonl',
              key_path='/root/.sovos/city_ed25519')
svc = MeasureService(chain, store=Path('/tmp/measure-jobs'))

# 3. Sign the board into a card via the real service path
job = svc.measure(protocol='gspc-board-v2', model=board.get('best') if isinstance(board.get('best'), str) else board.get('best', {}).get('model', 'unknown'),
                  bank_version=board.get('axis', AXIS),
                  axes=[board.get('axis', AXIS)],
                  run_fn=lambda *a: board)
card = job.card
assert card and card.get('signed') is True, f'card not signed: {card}'

# 4. Verify through the service's own verify()
v = svc.verify(card)
print(f'signed: {card["signed"]} | signer: {card["signer"][:20]}... | '
      f'epoch: {card["epoch"]} | content_id: {card["content_id"][:20]}...')
print(f'verify: valid={v["valid"]} content_id_matches={v["content_id_matches"]}')

# 5. Persist for rclone push
out = Path('/tmp/issued_card.json')
out.write_text(json.dumps(card, indent=1))
print(f'card written: {out} ({out.stat().st_size} bytes)')
