"""sovos-engine — the EAT engine-cycle harness.

Subcommands (run with `python -m sovos_engine <cmd>`):
  status    — confirm engine count + per-axis state from the signed board manifests
  diagnose  — read the gaps: weakest models, spreads, floor-effect + unparsed-heavy models
  fix       — emit an Ed25519-signed (or honestly-unsigned) fix record into benchmark-results/engine-fixes/

The harness never touches the sealed signing key directly; it delegates signing to
sign.py (which refuses to fake-sign when the key is absent).
"""

__version__ = "1.0.0"
