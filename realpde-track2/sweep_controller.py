"""
Sweep controller hyperparameters (z_mult, adapt_every, max_adapt_steps,
drift_threshold, min_band) to maximize the local Track 2 proxy score.

Usage:
    python sweep_controller.py --model /root/realpde/trained_v2/model.pth
                               --stats /root/realpde/trained_v2/stats_real.npz
"""
import sys
import itertools
import glob
import numpy as np
import torch

sys.path.insert(0, "/root/realpde")
from data_pipeline import load_trajectory_normed, make_windows, run_ttt_stream
from local_eval import score_run
import submission


def main():
    model_dir = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "/root/realpde/trained_v2"
    stats_path = sys.argv[sys.argv.index("--stats") + 1] if "--stats" in sys.argv else f"{model_dir}/stats_real.npz"
    stats = np.load(stats_path)
    stats = {k: float(v) for k, v in stats.items()}

    files = sorted(glob.glob("/root/realpde/data/train_real/*.h5"))
    files = [f for f in files if not f.endswith("7575_0.h5")]
    val_files = files[3:6]  # held-out from training eval
    print("val:", [f.split("/")[-1] for f in val_files], flush=True)

    # preload windows once
    streams = []
    for f in val_files:
        traj = load_trajectory_normed(f, stats)
        wi, wo = make_windows(traj)
        streams.append((wi, wo))

    grid = list(itertools.product(
        [0.8, 1.0, 1.2, 1.5],          # z_mult
        [2, 3, 4],                     # adapt_every
        [1, 2, 3],                     # max_adapt_steps
        [0.15, 0.25, 0.35],            # drift_threshold
    ))
    print(f"{len(grid)} configs to try", flush=True)
    results = []
    for z, ae, mas, dt in grid:
        base = submission.get_ttt_model(model_dir, device="cuda")
        base.max_adapt_steps = mas
        base.adapt_every = ae
        base.drift_threshold = dt
        base.z_mult = z
        all_p, all_t, all_times, all_lo, all_hi = [], [], [], [], []
        for wi, wo in streams:
            preds, tgts, times, adapt, (lo, hi) = run_ttt_stream(base, wi, wo, "cuda")
            all_p += preds; all_t += tgts; all_times += times
            all_lo += lo; all_hi += hi
        lo = np.concatenate(all_lo) if all_lo else None
        hi = np.concatenate(all_hi) if all_hi else None
        res = score_run(all_p, all_t, all_times, lo, hi, stats)
        results.append((res["final_proxy"], z, ae, mas, dt, res))
        print(f"z={z} ae={ae} mas={mas} dt={dt}: proxy={res['final_proxy']:.3f} "
              f"rel={res['rel_l2_score']:.1f} time={res['time_score']:.1f} "
              f"sps={res['sps_score']:.1f}", flush=True)

    results.sort(key=lambda r: -r[0])
    print("\n=== TOP 5 ===", flush=True)
    for r in results[:5]:
        print(f"proxy={r[0]:.3f} z={r[1]} ae={r[2]} mas={r[3]} dt={r[4]}", flush=True)
    best = results[0]
    print(f"\nBEST: z={best[1]} ae={best[2]} mas={best[3]} dt={best[4]} "
          f"proxy={best[0]:.3f}", flush=True)
    for k, v in best[5].items():
        print(f"  {k}: {v:.4f}", flush=True)


if __name__ == "__main__":
    main()
