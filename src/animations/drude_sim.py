"""Drude electron gas: free flight under a field, reset at random collisions.

Units are scene units and seconds of animation time, not SI. `tau` is the mean
time between collisions. Drift speed settles at `accel * tau`.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Run:
    positions: np.ndarray  # (frames, n, 3)
    drift: np.ndarray  # (frames,) mean velocity along -x, field points +x


def simulate(
    n: int,
    frames: int,
    dt: float,
    tau: float,
    accel: float,
    thermal: float,
    half_box: float,
    seed: int = 0,
) -> Run:
    rng = np.random.default_rng(seed)

    def fresh_velocity(count: int) -> np.ndarray:
        v = rng.normal(size=(count, 3))
        return thermal * v / np.linalg.norm(v, axis=1, keepdims=True)

    pos = rng.uniform(-half_box, half_box, size=(n, 3))
    vel = fresh_velocity(n)
    positions = np.empty((frames, n, 3))
    drift = np.empty(frames)
    for i in range(frames):
        vel[:, 0] -= accel * dt
        pos = pos + vel * dt
        pos = (pos + half_box) % (2 * half_box) - half_box
        hit = rng.random(n) < 1 - np.exp(-dt / tau)
        vel[hit] = fresh_velocity(int(hit.sum()))
        positions[i] = pos
        drift[i] = -vel[:, 0].mean()
    return Run(positions, drift)
