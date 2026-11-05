"""Sommerfeld: electrons fill the lowest wave states of a box, two per k-point."""

import numpy as np
from manim import (
    LEFT,
    RIGHT,
    UP,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Scene,
    Typst,
    ValueTracker,
    VGroup,
    linear,
)

from animations import metals, theme
from animations.balls import BallCloud
from animations.chart import Chart
from animations.scenes.drude import CENTER, PHI, ZOOM

HALF = 3  # k-points run from -HALF to HALF along each axis
RADIUS = 3.05  # Fermi radius in grid units: the sphere just fits the cube
SPACING = 0.5
FILL_SECONDS = 10.0
HOLD_SECONDS = 2.5
E_FERMI = metals.fermi_energy(metals.COPPER_DENSITY)
CHART = Chart(x_max=1.3, y_max=12.0)


def k_points() -> np.ndarray:
    axis = np.arange(-HALF, HALF + 1)
    return np.array([[x, y, z] for x in axis for y in axis for z in axis], dtype=float)


def occupied(points: np.ndarray) -> np.ndarray:
    """Points inside the Fermi sphere, lowest energy first."""
    norms = np.linalg.norm(points, axis=1)
    inside = points[norms <= RADIUS]
    return inside[np.argsort(np.linalg.norm(inside, axis=1), kind="stable")]


def energy(point: np.ndarray) -> float:
    """Free-electron energy in eV, with |k| = RADIUS giving E_F."""
    return E_FERMI * (np.linalg.norm(point) / RADIUS) ** 2


class Sommerfeld(Scene):
    def construct(self):
        grid = k_points()
        filled = occupied(grid)
        count = len(filled)

        t_fermi = f"{E_FERMI / metals.K_B:,.0f}".replace(",", " ")
        heading = theme.title("Sommerfeld: ondas en una caja")
        caption = theme.caption(
            "E_F = ħ^2 k_F^2 \\/ (2 m)",
            f"cobre: $E_F$ = {E_FERMI:.1f} eV · $T_F$ = {t_fermi} K".replace(".", ","),
        )
        rule = Typst(
            '$ "2 electrones por punto " k $',
            color=theme.MUTED,
            font_size=theme.LABEL_SIZE,
        )
        rule.move_to([theme.LEFT_EDGE + rule.width / 2, theme.CORNER_Y, 0])

        empty = BallCloud(grid * SPACING, 0.07, "#BDBDBD")
        full = BallCloud(filled * SPACING, 0.12, theme.ACCENT, z_offset=1000)

        axes = CHART.axes([0, 0.5, 1.0], "$ k \\/ k_F $", '$ E " (eV)" $')
        xs = np.linspace(0, 1.3, 60)
        parabola = CHART.curve(xs, E_FERMI * xs**2, theme.INK, width=3)
        fermi_line = DashedLine(
            CHART.point(0, E_FERMI),
            CHART.point(1.3, E_FERMI),
            color=theme.ACCENT,
            stroke_width=3,
        )
        fermi_label = Typst(
            '$ E_F = 7","0 " eV" $', color=theme.ACCENT, font_size=theme.LABEL_SIZE
        ).next_to(fermi_line, UP, buff=0.1)
        fermi_label.align_to(fermi_line, LEFT).shift(RIGHT * 0.2)
        states = VGroup(
            *[
                Dot(
                    CHART.point(np.linalg.norm(p) / RADIUS, energy(p)),
                    radius=0.05,
                    color=theme.ACCENT,
                )
                for p in filled
            ]
        )

        progress = ValueTracker(0)
        angle = ValueTracker(0.2)

        def shown() -> int:
            return int(progress.get_value() * count)

        def place(cloud):
            cloud.view(angle.get_value(), PHI, ZOOM).shift(CENTER)

        def refresh_full(group):
            place(group)
            for j, ball in enumerate(group):
                ball.set_fill(opacity=1.0 if j < shown() else 0.0)

        def refresh_states(group):
            for j, dot in enumerate(group):
                dot.set_fill(opacity=1.0 if j < shown() else 0.0)

        empty.add_updater(place)
        full.add_updater(refresh_full)
        states.add_updater(refresh_states)

        self.add(heading, rule, caption, axes, parabola, fermi_line, fermi_label)
        self.play(FadeIn(empty), FadeIn(full), run_time=0.8)
        self.add(states)
        self.play(
            progress.animate.set_value(1.0),
            angle.animate.set_value(1.2),
            run_time=FILL_SECONDS,
            rate_func=linear,
        )
        self.wait(HOLD_SECONDS)
        for mob in (empty, full, states):
            mob.clear_updaters()
        self.play(FadeOut(*self.mobjects), run_time=0.6)
