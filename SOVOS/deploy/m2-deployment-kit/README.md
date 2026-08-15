# M2 Deployment Kit

Operational tool kit for the M2 silicon substrate and the J-Space
deployment context. **Not Python-package-installable** — these are
production tool scripts that have been absorbed from
`M2_DEPLOYMENT_KIT/` (top-level) into this canonical location.

## Files

| File | Job | LOC |
|---|---|---|
| `black_swan_predictor.py`  | Predict black swan events for AI deployments |  45 |
| `charter_amender.py`        | Amend DEFONEOS charter articles            |  42 |
| `compliance_calculator.py` | EU AI Act risk classification calculator  |  94 |
| `defoneos_sign.py`          | SIGIL signing utility for DEFONEOS        |  48 |
| `gods_eye_scan.py`          | Omniscient scan of SOV3 substrate health   |  50 |
| `jurisdiction_mapper.py`    | Map EU AI Act → UK/SG/CA/US NIST equivalents |  89 |
| `side_by_side_test.py`      | Side-by-side model comparison for SOV33    | 301 |
| `sovereignty_index.py`      | Compute sovereignty index for AI systems  |  67 |
| `treaty_generator.py`       | Generate treaty/cooperation documents      |  54 |
| `trust_score.py`            | Compute trust score for AI deployments    |  38 |

## Provenance

Absorbed 2026-08-11 from
`/Users/nicholas/clawd/csoai-static-deploy2/M2_DEPLOYMENT_KIT/`.
Top-level of the repo had these as a standalone directory; the canonical
location under `SOVOS/deploy/m2-deployment-kit/` is the absorb target.

## Use

Import directly (top-level scripts):

```python
import sys; sys.path.insert(0, "SOVOS/deploy/m2-deployment-kit")
import compliance_calculator
import sovereignty_index
import trust_score
```

Or run the scripts standalone:

```bash
python3 SOVOS/deploy/m2-deployment-kit/compliance_calculator.py --help
```

These are operationally-meaningful tools (no UI; they compute indices,
classify EU AI Act risk, sign SIGILs). They sit alongside `SOVOS/deploy/a100/`
— that documents the heavy-lift GPU substrate, this documents the
operator-side deployment tool kit.
