import numpy as np
import pytest

from animations import metals
from animations.scenes import sommerfeld


def test_occupied_states_fill_a_sphere_in_energy_order():
    filled = sommerfeld.occupied(sommerfeld.k_points())
    norms = np.linalg.norm(filled, axis=1)
    assert np.all(np.diff(norms) >= 0)
    assert norms.max() <= sommerfeld.RADIUS
    sphere = 4 / 3 * np.pi * sommerfeld.RADIUS**3
    assert len(filled) == pytest.approx(sphere, rel=0.1)


def test_energy_at_the_fermi_radius_is_the_fermi_energy():
    edge = np.array([sommerfeld.RADIUS, 0.0, 0.0])
    assert sommerfeld.energy(edge) == pytest.approx(
        metals.fermi_energy(metals.COPPER_DENSITY)
    )
