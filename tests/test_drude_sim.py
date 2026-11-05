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


def test_drift_decays_with_tau_after_the_field_turns_off():
    tau = 0.5
    result = simulate(
        n=4000,
        frames=600,
        dt=1 / 30,
        tau=tau,
        accel=0.8,
        thermal=1.0,
        half_box=1.6,
        seed=2,
        field_off_at=10.0,
    )
    steady = result.drift[290:300].mean()
    after_one_tau = result.drift[300 + int(tau * 30)]
    assert abs(after_one_tau / steady - np.exp(-1)) < 0.12


def test_shorter_tau_drifts_slower():
    assert run(0.2).drift[300:].mean() < run(0.8).drift[300:].mean()


def test_positions_stay_in_the_box():
    pos = run(0.5).positions
    assert np.abs(pos).max() <= 1.6
