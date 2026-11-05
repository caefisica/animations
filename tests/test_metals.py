import pytest

from animations import metals


def test_copper_fermi_energy_is_about_seven_ev():
    assert metals.fermi_energy(metals.COPPER_DENSITY) == pytest.approx(7.0, abs=0.1)


def test_copper_free_gamma_matches_the_textbook_half_millijoule():
    assert metals.sommerfeld_gamma(metals.COPPER_DENSITY) == pytest.approx(
        0.50, abs=0.02
    )


def test_drude_overshoots_the_measured_heat_capacity_sixtyfold():
    measured_at_300k = metals.COPPER_GAMMA_MEASURED * 1e-3 * 300
    ratio = metals.drude_heat_capacity() / measured_at_300k
    assert 55 < ratio < 65
