import numpy as np

from animations.drude_sim import simulate


def run(tau: float):
    return simulate(
        n=400,
        frames=600,
        dt=1 / 30,
        tau=tau,
        accel=0.8,
        thermal=1.0,
        half_box=1.6,
        seed=1,
    )


def test_drift_settles_near_accel_times_tau():
    tau = 0.5
    late = run(tau).drift[300:].mean()
    assert abs(late - 0.8 * tau) < 0.08


def test_shorter_tau_drifts_slower():
    assert run(0.2).drift[300:].mean() < run(0.8).drift[300:].mean()


def test_positions_stay_in_the_box():
    pos = run(0.5).positions
    assert np.abs(pos).max() <= 1.6
