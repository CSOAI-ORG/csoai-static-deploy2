import sys, json
sys.path.insert(0, '/workspace')
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-city/src')
from sovos_city import sandbox_escape_bench as seb
from sovos_city import goldbank_expand as gx
import rce_sandbox

extended = gx.extend_gold('/workspace/csoai-static-deploy2/redblue_v2.py', max_per_class=30)
n_esc = sum(1 for i in extended if i['kind'] == 'ESCAPE')
n_ben = sum(1 for i in extended if i['kind'] == 'BENIGN')
print(f'extended bank: {len(extended)} items ({n_esc} ESCAPE + {n_ben} BENIGN)')

seb.GOLD_ITEMS = extended  # run_gold/assert_gold resolve module global at call time
problems = seb.assert_gold()
print('GOLD INTEGRITY:', 'PASS' if not problems else f'{len(problems)} problems: {problems[:5]}')
if problems:
    sys.exit(2)

result = seb.run_gold(rce_sandbox.run_one)
out = '/workspace/sandbox_escape_extended_run_2026-08-14.json'
json.dump(result, open(out, 'w'), indent=2)
print('saved', out)
print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))
fns = [r['id'] for r in result['rows'] if r['expt'] == 'ESCAPE' and not r['tp']]
fps = [r['id'] for r in result['rows'] if r['expt'] == 'BENIGN' and r['fp']]
print('missed escapes (FN):', fns)
print('flagged benign (FP):', fps)
