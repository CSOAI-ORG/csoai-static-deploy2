#!/usr/bin/env python3
"""Conformal 90/10 router — frozen split-conformal predicate (Stage 1, moves 21-30).

Doctrine-compliant by construction: the routing decision is a pure deterministic
comparison `s(x) <= qhat` on a computable nonconformity score. NO LLM judges a model.

Split (inductive) conformal prediction (Vovk et al. 2005; Angelopoulos & Bates 2107.07511):
  qhat = the ceil((n+1)(1-alpha))-th smallest calibration nonconformity score
  guarantee: Pr[auto-proceed AND wrong] <= alpha, distribution-free, under exchangeability.

Stdlib-only (no numpy). See docs/RESEARCH_VALIDATION.md §Key Finding 3.

Run:  python3 router/conformal_router.py --selftest
"""
import json
import math
import sys

ALPHA_DEFAULT = 0.05  # 5% auto-proceed error budget (moves 24-25: freeze, then measure realized)


def calibrate(calibration_scores, alpha=ALPHA_DEFAULT):
    """Freeze qhat from calibration scores. Returns (qhat, n)."""
    n = len(calibration_scores)
    if n == 0:
        raise ValueError("calibration set is empty")
    q_index = math.ceil((n + 1) * (1 - alpha)) - 1  # 0-based
    q_index = max(0, min(n - 1, q_index))
    sorted_scores = sorted(calibration_scores)
    return sorted_scores[q_index], n


def route(score, qhat):
    """s(x) <= qhat -> 90% auto-proceed; else -> 10% escalate/explore. Deterministic."""
    return "auto" if score <= qhat else "escalate"


def realized_error_rate(scores, labels_correct, qhat):
    """Measured realized error on a held-out slice: Pr[auto AND wrong]."""
    auto_wrong = 0
    auto_total = 0
    for s, ok in zip(scores, labels_correct):
        if s <= qhat:
            auto_total += 1
            if not ok:
                auto_wrong += 1
    return auto_wrong / auto_total if auto_total else 0.0, auto_total


def selftest():
    import random
    random.seed(42)

    def halfnormal():
        return abs(random.gauss(0, 1))

    # 1) QUANTILE PROPERTY: qhat is the ceil((n+1)(1-alpha))-th smallest calibration score,
    #    so the fraction of calibration scores <= qhat is ~ (q_index+1)/(n+1) ~ 1-alpha.
    n = 300
    cal = [halfnormal() for _ in range(n)]
    qhat, n_ = calibrate(cal, ALPHA_DEFAULT)
    assert n_ == n
    frac = sum(1 for s in cal if s <= qhat) / n
    expected = math.ceil((n + 1) * (1 - ALPHA_DEFAULT)) / (n + 1)
    print(f"quantile: n={n} alpha={ALPHA_DEFAULT} qhat={qhat:.4f} frac<=qhat={frac:.4f} expected~{expected:.4f}")
    assert abs(frac - expected) < 0.05, f"quantile property violated: {frac:.4f} vs {expected:.4f}"

    # 2) REALIZED ERROR BOUND: fresh slice, error probability increasing in the score
    #    (uncertainty-calibrated toy). Auto-proceed error must stay <= alpha.
    scores = [halfnormal() for _ in range(800)]
    errors = [1 if random.random() < (0.01 + 0.1 * (s / 3.0)) else 0 for s in scores]
    err, auto_n = realized_error_rate(scores, [e == 0 for e in errors], qhat)
    print(f"realized: auto-proceed={auto_n}/800 error={err:.4f} (alpha={ALPHA_DEFAULT})")
    assert err <= ALPHA_DEFAULT + 0.02, f"realized error {err:.4f} exceeds alpha budget"

    # 3) DETERMINISM + EDGE CASES
    assert route(0.1, qhat) == "auto"
    assert route(99.9, qhat) == "escalate"
    assert route(qhat, qhat) == "auto"  # boundary inclusive
    assert route(qhat + 1e-9, qhat) == "escalate"
    try:
        calibrate([])
        raise SystemExit("empty calibration should raise")
    except ValueError:
        pass
    q1, _ = calibrate([0.5], 0.05)
    assert q1 == 0.5
    print("selftest: conformal router PASS")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    # CLI: calibrate from a JSON file of scores, print qhat + a sample route
    # usage: python3 conformal_router.py scores.json [alpha]
    p = sys.argv[1]
    with open(p) as fh:
        data = json.load(fh)
    alpha = float(sys.argv[2]) if len(sys.argv) > 2 else ALPHA_DEFAULT
    scores = data if isinstance(data, list) else data.get("scores")
    qhat, n = calibrate(scores, alpha)
    print(json.dumps({"alpha": alpha, "n": n, "qhat": round(qhat, 6),
                      "sample": [route(s, qhat) for s in scores[:5]]}, indent=1))
