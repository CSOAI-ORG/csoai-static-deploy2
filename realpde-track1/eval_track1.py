"""
Track 1 (Sim2Real) local evaluation harness.

Official bundle layout:
    data/<phase>/input_data/samples.npz     {"input": (N,20,32,64,3), "sample_id"?}
    data/<phase>/reference_data/targets.npz {"target": (N,20,32,64,3)}

Scoring: five 0-100 subscores (rel_l2, tke, mvpe, time, sps) with the same
formulas as Track 2 (SPS weights 0.5/0.3/0.2). final_score combination hidden.
"""

import time
import numpy as np
import torch

from local_eval import (rel_l2_error, tke_error, mvpe_error, err_to_score,
                        sps_score, T_NUMERICAL)


def score_batch(preds, targets, step_times=None, lower=None, upper=None):
    """preds/targets: (N,20,32,64,3) arrays."""
    rl2 = rel_l2_error(preds, targets)
    tke = tke_error(preds, targets)
    mvpe = mvpe_error(preds, targets)
    if step_times is not None:
        t_mean = float(np.mean(step_times))
        r = t_mean / T_NUMERICAL
        time_sc = 100.0 / (1.0 + np.sqrt(r))
    else:
        time_sc = float("nan")
    sps = sps_score(preds, targets, lower, upper)
    return {
        "rel_l2_err": rl2, "rel_l2_score": err_to_score(rl2),
        "tke_err": tke, "tke_score": err_to_score(tke),
        "mvpe_err": mvpe, "mvpe_score": err_to_score(mvpe),
        "time_score": time_sc,
        "sps_score": sps,
        "final_proxy": np.mean([err_to_score(rl2), err_to_score(tke),
                                err_to_score(mvpe), time_sc, sps]),
    }


def run_batch_eval(model, samples, targets=None, num_workers=0):
    """samples: (N,20,32,64,3) raw numpy; targets optional for scoring."""
    x = torch.from_numpy(np.asarray(samples, dtype=np.float32))
    preds, times = [], []
    model.model.eval()
    with torch.no_grad():
        for i in range(0, x.size(0), 32):
            t0 = time.perf_counter()
            out = model.predict(x[i:i+32].numpy())
            times.append((time.perf_counter() - t0) / 32)
            if isinstance(out, dict):
                preds.append(out["prediction"])
            else:
                preds.append(np.asarray(out))
    preds = np.concatenate(preds, axis=0)
    if targets is None:
        return preds
    return score_batch(preds, np.asarray(targets), times)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/root/realpde")
    from submission_model import SubmissionModel
    from data_pipeline import load_h5, make_windows, normalize
    import numpy as np

    stats = np.load("/root/realpde/trained_v1/stats_real.npz")
    stats = {k: float(v) for k, v in stats.items()}
    # build a pseudo-batch from a couple real trajectories (windowed)
    import glob, os
    files = sorted(glob.glob("/root/realpde/data/train_real/*.h5"))[:2]
    ins, outs = [], []
    for f in files:
        traj = load_h5(f, add_p=True)
        traj = normalize(traj, stats)
        wi, wo = make_windows(traj)
        ins.append(wi); outs.append(wo)
    samples = np.concatenate(ins)[:64]
    targets = np.concatenate(outs)[:64]
    m = SubmissionModel("/root/realpde/trained_v1")
    res = run_batch_eval(m, samples, targets)
    for k, v in res.items():
        print(f"{k}: {v:.4f}")
