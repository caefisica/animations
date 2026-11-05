"""Drude model: electrons drift through a lattice of ions under a field."""

import numpy as np
from manim import UP, FadeIn, Scene, ValueTracker, linear

from animations import theme
from animations.balls import BallCloud


def cubic_lattice(n: int, spacing: float) -> np.ndarray:
    axis = (np.arange(n) - (n - 1) / 2) * spacing
    return np.array([[x, y, z] for x in axis for y in axis for z in axis])


class DrudeGas(Scene):
    def construct(self):
        heading = theme.title("Drude: la conductividad")
        caption = theme.caption(
            "rho = m / (n e^2 tau)", "cobre: $tau = 2,4 times 10^(-14)$ s"
        )
        ions = BallCloud(cubic_lattice(5, 0.8), 0.17, theme.SPHERE).shift(UP * 1.2)
        angle = ValueTracker(0.6)
        ions.add_updater(lambda m: m.view(angle.get_value(), 0.9, 1.0))
        self.add(heading, caption)
        self.play(FadeIn(ions))
        self.play(angle.animate.set_value(2.2), run_time=4, rate_func=linear)
