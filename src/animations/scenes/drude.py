"""Drude model: electrons drift through a lattice of ions under a field."""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    DashedLine,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Typst,
    ValueTracker,
    VMobject,
    linear,
)

from animations import theme
from animations.balls import BallCloud
from animations.drude_sim import simulate

FPS = 30
CENTER = UP * 1.4
ELECTRONS = 125  # one free electron per ion, as in copper
SIM_SECONDS = 24
FIELD_OFF = 13.0
CHART_LEFT, CHART_RIGHT = -3.6, 3.6
CHART_BOTTOM, CHART_TOP = -4.1, -2.1
TAU = 0.5
ACCEL = 0.8


def cubic_lattice(n: int, spacing: float) -> np.ndarray:
    axis = (np.arange(n) - (n - 1) / 2) * spacing
    return np.array([[x, y, z] for x in axis for y in axis for z in axis])


def drift_curve(drift: np.ndarray, upto: int) -> VMobject:
    """Polyline of the drift speed in the chart box, scaled to its steady value."""
    count = max(upto, 2)
    xs = np.linspace(CHART_LEFT, CHART_RIGHT, len(drift))[:count]
    peak = ACCEL * TAU * 1.6
    ys = CHART_BOTTOM + (CHART_TOP - CHART_BOTTOM) * np.clip(drift[:count] / peak, 0, 1)
    curve = VMobject(stroke_color=theme.ACCENT, stroke_width=4)
    curve.set_points_as_corners([[x, y, 0] for x, y in zip(xs, ys)])
    return curve


class DrudeGas(Scene):
    def construct(self):
        frames = SIM_SECONDS * FPS
        run = simulate(
            ELECTRONS,
            frames,
            1 / FPS,
            TAU,
            ACCEL,
            thermal=1.0,
            half_box=1.6,
            seed=3,
            field_off_at=FIELD_OFF,
        )
        smooth = np.convolve(run.drift, np.ones(45) / 45, mode="same")

        self.title_card()

        heading = theme.title("Drude: la conductividad")
        caption = theme.caption(
            "rho = m / (n e^2 tau)", "cobre: $tau = 2,4 times 10^(-14)$ s"
        )
        ions = BallCloud(cubic_lattice(5, 0.8), 0.15, theme.SPHERE_DARK).shift(CENTER)
        electrons = BallCloud(
            run.positions[0], 0.13, theme.ACCENT, z_offset=1000
        ).shift(CENTER)
        arrow = Arrow(
            CENTER + LEFT * 1.6 + DOWN * 2.3,
            CENTER + RIGHT * 1.6 + DOWN * 2.3,
            color=theme.FIELD,
            buff=0,
            stroke_width=8,
        )
        field = Typst("$ E $", color=theme.FIELD, font_size=48).next_to(
            arrow, RIGHT, buff=0.2
        )
        axis = Line(
            [CHART_LEFT, CHART_BOTTOM, 0],
            [CHART_RIGHT, CHART_BOTTOM, 0],
            color=theme.MUTED,
            stroke_width=2,
        )
        label = Typst(
            "velocidad de arrastre (escala exagerada)",
            color=theme.MUTED,
            font_size=24,
        ).move_to([0, CHART_TOP + 0.45, 0])
        steady_y = CHART_BOTTOM + (CHART_TOP - CHART_BOTTOM) / 1.6
        steady = DashedLine(
            [CHART_LEFT, steady_y, 0],
            [CHART_RIGHT, steady_y, 0],
            color=theme.FIELD,
            stroke_width=2,
        )
        steady_label = (
            Typst("$ v_d = e E tau / m $", color=theme.FIELD, font_size=26)
            .next_to(steady, UP, buff=0.08)
            .align_to(steady, RIGHT)
        )
        off_x = CHART_LEFT + (CHART_RIGHT - CHART_LEFT) * FIELD_OFF / SIM_SECONDS
        off_mark = Line(
            [off_x, CHART_BOTTOM, 0],
            [off_x, CHART_BOTTOM + 0.3, 0],
            color=theme.MUTED,
            stroke_width=2,
        )
        off_label = Typst("E = 0", color=theme.MUTED, font_size=24).next_to(
            off_mark, DOWN, buff=0.1
        )

        clock = ValueTracker(0)
        angle = ValueTracker(0.6)

        def step(group):
            i = min(int(clock.get_value() * FPS), frames - 1)
            group.points3d = run.positions[i]
            group.view(angle.get_value(), 0.9, 1.0).shift(CENTER)

        def redraw(curve):
            i = int(clock.get_value() * FPS)
            curve.become(drift_curve(smooth, i))

        ions.add_updater(lambda m: m.view(angle.get_value(), 0.9, 1.0).shift(CENTER))
        electrons.add_updater(step)
        curve = drift_curve(smooth, 2)
        curve.add_updater(redraw)

        self.add(heading, caption)
        self.play(FadeIn(ions), FadeIn(electrons), FadeIn(arrow), FadeIn(field))
        self.add(axis, label, steady, steady_label, off_mark, off_label, curve)
        for mob in (arrow, field):
            mob.add_updater(
                lambda m: m.set_opacity(1.0 if clock.get_value() < FIELD_OFF else 0.15)
            )
        self.play(
            clock.animate.set_value(SIM_SECONDS - 1),
            angle.animate.set_value(1.6),
            run_time=SIM_SECONDS - 1,
            rate_func=linear,
        )
        for mob in (ions, electrons, curve, arrow, field):
            mob.clear_updaters()
        self.play(FadeOut(*self.mobjects), run_time=0.6)
        self.end_card()

    def title_card(self):
        name = Typst("Drude", color=theme.INK, font_size=120)
        sub = Typst("¿por qué un cable resiste?", color=theme.ACCENT, font_size=44)
        sub.next_to(name, DOWN, buff=0.5)
        self.play(FadeIn(name), FadeIn(sub), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(name), FadeOut(sub), run_time=0.6)

    def end_card(self):
        mark = Typst("CAE Física", color=theme.MUTED, font_size=56)
        self.play(FadeIn(mark), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(mark), run_time=0.4)
