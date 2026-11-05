"""Free-electron numbers for the Drude and Sommerfeld scenes, in SI units."""

import numpy as np

R = 8.314462618  # J / (mol K)
K_B = 8.617333262e-5  # eV / K
HBAR2_2M = 3.80998212  # hbar^2 / 2 m_e in eV Angstrom^2

COPPER_DENSITY = 8.47e28  # free electrons per m^3, one per atom
COPPER_GAMMA_MEASURED = 0.695  # mJ / (mol K^2)


def drude_heat_capacity() -> float:
    """Classical equipartition: (3/2) k_B per electron, in J / (mol K)."""
    return 1.5 * R


def fermi_wavevector(density: float) -> float:
    """k_F = (3 pi^2 n)^(1/3), in 1/m."""
    return (3 * np.pi**2 * density) ** (1 / 3)


def fermi_energy(density: float) -> float:
    """E_F = hbar^2 k_F^2 / 2m, in eV."""
    k_angstrom = fermi_wavevector(density) * 1e-10
    return HBAR2_2M * k_angstrom**2


def sommerfeld_gamma(density: float) -> float:
    """Electronic heat capacity C = gamma T for free electrons, in mJ / (mol K^2)."""
    t_fermi = fermi_energy(density) / K_B
    return 1e3 * (np.pi**2 / 2) * R / t_fermi
