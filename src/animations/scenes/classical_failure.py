"""The classical failure: Drude predicts an electron heat capacity 60 times too big."""

import numpy as np
from manim import (
    LEFT,
    UP,
    DashedLine,
    Dot,
    DoubleArrow,
    FadeIn,
    FadeOut,
    Scene,
    Typst,
    ValueTracker,
    linear,
)

from animations import metals, theme
from animations.balls import BallCloud
from animations.chart import Chart
from animations.drude_sim import simulate
from animations.scenes.drude import CENTER, PHI, ZOOM, cubic_lattice

FPS = 30
SECONDS = 14.0
T_MAX = 300.0
ELECTRONS = 125
CHART = Chart(x_max=T_MAX, y_max=14.0)
MEASURED = metals.COPPER_GAMMA_MEASURED * 1e-3  # J / (mol K^2)


def playback_frames(frames: int) -> np.ndarray:
    """Frame index to show at each output frame: thermal speed grows as sqrt(T)."""
    temperature = T_MAX * np.arange(frames) / frames
    return np.cumsum(np.sqrt(temperature / T_MAX)).astype(int)


class ClassicalFailure(Scene):
    def construct(self):
        frames = int(SECONDS * FPS)
        shown = playback_frames(frames)
        run = simulate(
            ELECTRONS,
            int(shown[-1]) + 1,
            1 / FPS,
            tau=0.6,
            accel=0.0,
            thermal=1.0,
            half_box=1.6,
            seed=5,
        )
        heading = theme.title("La falla clásica")
        caption = theme.caption(
            "C_V = 3 \\/ 2 R",
            "$gamma$ del cobre, mJ/(mol K²): 0,50 libres, 0,695 medido",
        )

        ions = BallCloud(cubic_lattice(5, 0.8), 0.15, theme.SPHERE_DARK)
        electrons = BallCloud(run.positions[0], 0.13, theme.ACCENT, z_offset=1000)

        axes = CHART.axes([0, 100, 200, 300], '$ T " (K)" $', '$ C " (J/(mol K))" $')
        drude_y = metals.drude_heat_capacity()
        drude_line = DashedLine(
            CHART.point(0, drude_y),
            CHART.point(T_MAX, drude_y),
            color=theme.INK,
            stroke_width=3,
        )
        drude_label = Typst(
            '$ "Drude: " 3 \\/ 2 R = 12","5 $',
            color=theme.INK,
            font_size=theme.LABEL_SIZE,
        ).next_to(drude_line, UP, buff=0.1)
        measured_label = Typst(
            '$ "medido a 300 K: " 0","21 $',
            color=theme.ACCENT,
            font_size=theme.LABEL_SIZE,
        ).move_to(CHART.point(T_MAX * 0.45, 2.0))
        gap_x = T_MAX * 0.8
        bracket = DoubleArrow(
            CHART.point(gap_x, MEASURED * T_MAX),
            CHART.point(gap_x, drude_y),
            color=theme.ACCENT,
            buff=0,
            stroke_width=4,
        )
        gap = Typst(
            "60 veces menos", color=theme.ACCENT, font_size=theme.LABEL_SIZE
        ).next_to(bracket, LEFT, buff=0.2)

        clock = ValueTracker(0)

        def place(cloud):
            theta = 0.9 + 0.2 * clock.get_value() / SECONDS
            cloud.view(theta, PHI, ZOOM).shift(CENTER)

        def step(group):
            i = min(int(clock.get_value() * FPS), frames - 1)
            group.points3d = run.positions[shown[i]]
            place(group)

        def temperature() -> float:
            return T_MAX * clock.get_value() / SECONDS

        electrons.add_updater(step)
        ions.add_updater(place)
        measured = CHART.curve([0, 1], [0, 0], theme.ACCENT)
        measured.add_updater(
            lambda c: c.become(
                CHART.curve(
                    [0, max(temperature(), 1e-3)],
                    [0, MEASURED * max(temperature(), 1e-3)],
                    theme.ACCENT,
                )
            )
        )
        marker = Dot(radius=0.08, color=theme.ACCENT)
        marker.add_updater(
            lambda d: d.move_to(CHART.point(temperature(), MEASURED * temperature()))
        )

        self.add(heading, caption, axes, drude_line, drude_label)
        self.play(FadeIn(ions), FadeIn(electrons))
        self.add(measured, marker)
        self.play(
            clock.animate.set_value(SECONDS - 1 / FPS),
            run_time=SECONDS,
            rate_func=linear,
        )
        for mob in (ions, electrons, measured, marker):
            mob.clear_updaters()
        self.play(FadeIn(measured_label), FadeIn(bracket), FadeIn(gap), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(*self.mobjects), run_time=0.6)
