"""
Local evaluation harness replicating the official Track 2 (LTTTA) scoring.

Reproduces the documented subscores from the competition Evaluation page:
  rel_l2, tke, mvpe, time, sps  (each 0-100) + a conservative final proxy.

NOTE: the official final_score combination is not published. This harness
computes the five subscores with the published formulas so we can optimize
locally; final_score proxy = simple mean of the five (for relative ranking).
"""

import numpy as np
import time

SIGMA_GLOBAL = 0.0563870   # frozen season constant (u,v channel std on train_real)
T_NUMERICAL = 0.72896      # s, numerical solver reference per step


def rel_l2_error(pred, target, eps=1e-8):
    """Per-window ||pred-target||_2 / max(||target||_2, eps) on u,v (flattened)."""
    p = pred[..., :2].reshape(pred.shape[0], -1)
    t = target[..., :2].reshape(target.shape[0], -1)
    err = np.linalg.norm(p - t, axis=1) / np.maximum(np.linalg.norm(t, axis=1), eps)
    return err.mean()


def tke_error(pred, target):
    """Relative L2 between TKE fields: ke = 0.5*(var_t(u) + var_t(v))."""
    def ke(x):
        u = x[..., 0]
        v = x[..., 1]
        u_prime = ((u - u.mean(axis=1, keepdims=True)) ** 2).mean(axis=1)
        v_prime = ((v - v.mean(axis=1, keepdims=True)) ** 2).mean(axis=1)
        return 0.5 * (u_prime + v_prime)
    pke = ke(pred).reshape(pred.shape[0], -1)
    tke = ke(target).reshape(target.shape[0], -1)
    return (np.linalg.norm(pke - tke, axis=1) /
            np.maximum(np.linalg.norm(tke, axis=1), 1e-8)).mean()


def mvpe_error(pred, target):
    """Mean velocity profile error in the wake: time-averaged u,v at probe
    points behind the airfoil (4 streamwise stations x up to 9 spanwise rows).
    H=32, W=64; airfoil occupies the left-center; wake = right side."""
    # Conservative probe grid: 4 streamwise stations in right half, 9 rows.
    w = pred.shape[3]
    h = pred.shape[2]
    stations = [int(w * 0.55), int(w * 0.65), int(w * 0.75), int(w * 0.85)]
    rows = np.linspace(0.1, 0.9, 9) * (h - 1)
    p = pred[..., :2].mean(axis=1)   # (N, H, W, 2) time-averaged
    t = target[..., :2].mean(axis=1)
    pprof = np.stack([p[:, int(r), s] for s in stations for r in rows], axis=1)  # (N, 36, 2)
    tprof = np.stack([t[:, int(r), s] for s in stations for r in rows], axis=1)
    pprof = pprof.reshape(pred.shape[0], -1)
    tprof = tprof.reshape(target.shape[0], -1)
    return (np.linalg.norm(pprof - tprof, axis=1) /
            np.maximum(np.linalg.norm(tprof, axis=1), 1e-8)).mean()


def err_to_score(e):
    return 100.0 / (1.0 + 0.5 * e)


def sps_score(pred, target, lower=None, upper=None, stats=None):
    """Safe Prediction Score. Bounds optional; default band = pred ± 0.05|pred|.

    Official flow: the evaluator denormalizes pred/bounds with the official
    train_real statistics, then computes coverage + nil in PHYSICAL space
    (sigma_global is a physical-space constant). We replicate by denormalizing
    with `stats` (dict with std_u/std_v) before scoring. If stats is None we
    assume pred/lower/upper are already in physical space.
    """
    if lower is None or upper is None:
        lower = pred - 0.05 * np.abs(pred)
        upper = pred + 0.05 * np.abs(pred)
    if stats is not None:
        def _denorm(x):
            y = x.copy()
            y[..., 0] = y[..., 0] * stats["std_u"] + stats["mean_u"]
            y[..., 1] = y[..., 1] * stats["std_v"] + stats["mean_v"]
            return y
        pred = _denorm(pred)
        target = _denorm(target)
        lower = _denorm(lower)
        upper = _denorm(upper)
    # scored channels u,v only
    p = pred[..., :2]; t = target[..., :2]; lo = lower[..., :2]; hi = upper[..., :2]

    errs = {
        "dm": rel_l2_error(pred, target),
        "tke": tke_error(pred, target),
        "mvpe": mvpe_error(pred, target),
    }
    weighted = 0.0
    for name, e in errs.items():
        pm = e / (0.5 + e)                      # per-window squashed error
        inside = (lo <= t) & (t <= hi)          # per-element coverage gate
        nil = (hi - lo) / SIGMA_GLOBAL          # normalized interval width (physical)
        elem = np.where(inside, (1 - pm) * np.exp(-nil), 0.0)
        branch = elem.mean()
        weight = {"dm": 0.5, "tke": 0.3, "mvpe": 0.2}[name]
        weighted += weight * branch
    return 100.0 * weighted


def score_run(preds, targets, step_times, lower=None, upper=None, stats=None):
    """preds/targets: list of (1,20,32,64,3) arrays. Returns dict of subscores."""
    preds = np.concatenate(preds, axis=0)
    targets = np.concatenate(targets, axis=0)
    rl2 = rel_l2_error(preds, targets)
    tke = tke_error(preds, targets)
    mvpe = mvpe_error(preds, targets)
    t_mean = float(np.mean(step_times))
    r = t_mean / T_NUMERICAL
    time_score = 100.0 / (1.0 + np.sqrt(r))
    sps = sps_score(preds, targets, lower, upper, stats)
    return {
        "rel_l2_err": rl2, "rel_l2_score": err_to_score(rl2),
        "tke_err": tke, "tke_score": err_to_score(tke),
        "mvpe_err": mvpe, "mvpe_score": err_to_score(mvpe),
        "mean_step_time_s": t_mean, "time_score": time_score,
        "sps_score": sps,
        "final_proxy": np.mean([err_to_score(rl2), err_to_score(tke),
                                err_to_score(mvpe), time_score, sps]),
    }


if __name__ == "__main__":
    # quick self-test with random data
    rng = np.random.default_rng(0)
    preds = [rng.normal(0, 1, (1, 20, 32, 64, 3)).astype(np.float32) for _ in range(3)]
    targets = [rng.normal(0, 1, (1, 20, 32, 64, 3)).astype(np.float32) for _ in range(3)]
    res = score_run(preds, targets, [0.05, 0.05, 0.05])
    for k, v in res.items():
        print(f"{k}: {v:.4f}")
