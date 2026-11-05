"""Drude model: electrons drift through a lattice of ions under a field."""

from pathlib import Path

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
    ImageMobject,
    Line,
    Scene,
    Typst,
    ValueTracker,
    VGroup,
    VMobject,
    linear,
)

from animations import theme
from animations.balls import BallCloud
from animations.drude_sim import simulate

LOGO = Path(__file__).resolve().parents[1] / "assets" / "logo-cae.png"

FPS = 30
CENTER = UP * 1.4
ELECTRONS = 125  # one free electron per ion, as in copper
TAU = 0.6  # seconds of animation time; the chart axis is in units of tau
ACCEL = 0.8
TAUS = 40
FIELD_ON, FIELD_OFF = 8, 28  # in units of tau
SIM_SECONDS = TAUS * TAU
CHART_LEFT, CHART_RIGHT = -3.3, 3.6
CHART_BOTTOM, CHART_TOP = -4.1, -2.0
Y_MIN, Y_MAX = -0.25, 1.45  # in units of the steady drift accel * tau


def cubic_lattice(n: int, spacing: float) -> np.ndarray:
    axis = (np.arange(n) - (n - 1) / 2) * spacing
    return np.array([[x, y, z] for x in axis for y in axis for z in axis])


def chart_x(taus: float) -> float:
    return CHART_LEFT + (CHART_RIGHT - CHART_LEFT) * taus / TAUS


def chart_y(speed: float) -> float:
    """Map a drift speed to the chart, where 1.0 is accel * tau."""
    share = (speed / (ACCEL * TAU) - Y_MIN) / (Y_MAX - Y_MIN)
    return CHART_BOTTOM + (CHART_TOP - CHART_BOTTOM) * float(np.clip(share, 0, 1))


def drift_curve(drift: np.ndarray, upto: int) -> VMobject:
    count = max(upto, 2)
    taus = np.arange(count) / FPS / TAU
    corners = [[chart_x(t), chart_y(v), 0] for t, v in zip(taus, drift[:count])]
    curve = VMobject(stroke_color=theme.ACCENT, stroke_width=4)
    curve.set_points_as_corners(corners)
    return curve


def vertical_mark(taus: float, color) -> DashedLine:
    return DashedLine(
        [chart_x(taus), CHART_BOTTOM + 0.2, 0],
        [chart_x(taus), CHART_TOP - 0.1, 0],
        color=color,
        stroke_width=1.5,
    )


def chart_frame() -> VGroup:
    zero_y = chart_y(0)
    axis = Line(
        [CHART_LEFT, zero_y, 0],
        [CHART_RIGHT, zero_y, 0],
        color=theme.MUTED,
        stroke_width=2,
    )
    spine = Line(
        [CHART_LEFT, CHART_BOTTOM, 0],
        [CHART_LEFT, CHART_TOP, 0],
        color=theme.MUTED,
        stroke_width=2,
    )
    ticks = VGroup()
    for t in range(0, TAUS + 1, 10):
        ticks.add(
            Line(
                [chart_x(t), zero_y, 0],
                [chart_x(t), zero_y - 0.08, 0],
                color=theme.MUTED,
                stroke_width=2,
            ),
            Typst(str(t), color=theme.MUTED, font_size=22).move_to(
                [chart_x(t), zero_y - 0.28, 0]
            ),
        )
    x_label = Typst("$ t / tau $", color=theme.MUTED, font_size=26).move_to(
        [CHART_RIGHT - 0.2, CHART_BOTTOM + 0.05, 0]
    )
    y_label = Typst(
        "$ chevron.l v_x chevron.r $", color=theme.MUTED, font_size=26
    ).move_to([CHART_LEFT + 0.1, CHART_TOP + 0.25, 0])
    steady = DashedLine(
        [CHART_LEFT, chart_y(ACCEL * TAU), 0],
        [CHART_RIGHT, chart_y(ACCEL * TAU), 0],
        color=theme.FIELD,
        stroke_width=2,
    )
    steady_label = (
        Typst("$ e E tau / m $", color=theme.FIELD, font_size=26)
        .next_to(steady, UP, buff=0.06)
        .align_to(steady, RIGHT)
    )
    on_label = Typst("campo encendido", color=theme.FIELD, font_size=22).move_to(
        [chart_x(FIELD_ON) + 0.75, CHART_TOP + 0.05, 0]
    )
    off_label = Typst("campo apagado", color=theme.MUTED, font_size=22).move_to(
        [chart_x(FIELD_OFF) - 0.7, CHART_TOP + 0.05, 0]
    )
    return VGroup(
        axis,
        spine,
        ticks,
        x_label,
        y_label,
        steady,
        steady_label,
        vertical_mark(FIELD_ON, theme.FIELD),
        on_label,
        vertical_mark(FIELD_OFF, theme.MUTED),
        off_label,
    )


class DrudeGas(Scene):
    def construct(self):
        frames = int(SIM_SECONDS * FPS)
        run = simulate(
            ELECTRONS,
            frames,
            1 / FPS,
            TAU,
            ACCEL,
            thermal=1.0,
            half_box=1.6,
            seed=3,
            field_on_at=FIELD_ON * TAU,
            field_off_at=FIELD_OFF * TAU,
        )
        smooth = np.convolve(run.drift, np.ones(30) / 30, mode="same")

        self.title_card()

        heading = theme.title("Drude: la conductividad")
        caption = theme.caption(
            "rho = m / (n e^2 tau)",
            "cobre: $tau = 2,4 times 10^(-14)$ s"
            " · recorrido libre: 2,8 nm con la velocidad clásica, 38 nm con $v_F$",
        )
        caption[1].scale(0.85).move_to(UP * theme.NOTE_Y)
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
        frame = chart_frame()

        clock = ValueTracker(0)
        angle = ValueTracker(0.6)

        def field_is_on() -> bool:
            return FIELD_ON <= clock.get_value() / TAU < FIELD_OFF

        def step(group):
            i = min(int(clock.get_value() * FPS), frames - 1)
            group.points3d = run.positions[i]
            group.view(angle.get_value(), 0.9, 1.0).shift(CENTER)

        ions.add_updater(lambda m: m.view(angle.get_value(), 0.9, 1.0).shift(CENTER))
        electrons.add_updater(step)
        curve = drift_curve(smooth, 2)
        curve.add_updater(
            lambda c: c.become(drift_curve(smooth, int(clock.get_value() * FPS)))
        )
        for mob in (arrow, field):
            mob.add_updater(lambda m: m.set_opacity(1.0 if field_is_on() else 0.15))

        self.add(heading, caption)
        self.play(FadeIn(ions), FadeIn(electrons), FadeIn(arrow), FadeIn(field))
        self.add(frame, curve)
        self.play(
            clock.animate.set_value(SIM_SECONDS - 1 / FPS),
            angle.animate.set_value(1.6),
            run_time=SIM_SECONDS,
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
        logo = ImageMobject(str(LOGO)).scale_to_fit_height(2.6)
        handle = Typst("\\@caefisica", color=theme.MUTED, font_size=48)
        handle.next_to(logo, DOWN, buff=0.2)
        self.play(FadeIn(logo), FadeIn(handle), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(logo), FadeOut(handle), run_time=0.4)
