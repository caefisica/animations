"""Drude model: electrons drift through a lattice of ions under a field."""

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    DashedLine,
    FadeIn,
    FadeOut,
    Scene,
    Typst,
    ValueTracker,
    VGroup,
    linear,
)

from animations import theme
from animations.balls import BallCloud
from animations.chart import Chart
from animations.drude_sim import simulate

FPS = 30
PHI = 0.9  # camera tilt
ZOOM = 0.9  # the lattice clears the title, the corner label and the formula
CENTER = UP * theme.SCENE_Y
ELECTRONS = 125  # one free electron per ion, as in copper
TAU = 0.6  # seconds of animation time; the chart axis is in units of tau
ACCEL = 0.8
TAUS = 40
FIELD_ON, FIELD_OFF = 8, 28  # in units of tau
SIM_SECONDS = TAUS * TAU
CHART = Chart(x_max=TAUS, y_min=-0.25, y_max=1.45)  # y in units of accel * tau
FIELD_COLUMNS, FIELD_ROWS = 3, 4
FIELD_OPACITY = 0.35  # faint enough that the lattice stays the subject


def cubic_lattice(n: int, spacing: float) -> np.ndarray:
    axis = (np.arange(n) - (n - 1) / 2) * spacing
    return np.array([[x, y, z] for x in axis for y in axis for z in axis])


def drift_curve(drift: np.ndarray, upto: int):
    count = max(upto, 2)
    taus = np.arange(count) / FPS / TAU
    return CHART.curve(taus, drift[:count] / (ACCEL * TAU), theme.ACCENT)


def vertical_mark(taus: float, color) -> DashedLine:
    return DashedLine(
        CHART.point(taus, CHART.y_min),
        CHART.point(taus, CHART.y_max),
        color=color,
        stroke_width=2,
    )


def chart_frame() -> VGroup:
    steady = DashedLine(
        CHART.point(0, 1.0), CHART.point(TAUS, 1.0), color=theme.FIELD, stroke_width=3
    )
    steady_label = Typst(
        "$ e E tau \\/ m $", color=theme.FIELD, font_size=theme.LABEL_SIZE
    ).next_to(steady, UP, buff=0.08)
    steady_label.align_to(steady, RIGHT)
    return VGroup(
        CHART.axes([0, 10, 20, 30, 40], "$ t \\/ tau $", "$ chevron.l v_x chevron.r $"),
        steady,
        steady_label,
        vertical_mark(FIELD_ON, theme.FIELD),
        vertical_mark(FIELD_OFF, theme.MUTED),
    )


def field_backdrop() -> VGroup:
    """A grid of equal arrows behind the lattice, along -x.

    E points against the electrons' drift. Every arrow has the same length: the
    field is uniform.
    """
    columns = np.linspace(-2.5, 2.5, FIELD_COLUMNS)
    rows = theme.SCENE_Y + np.linspace(-1.7, 1.7, FIELD_ROWS)
    return VGroup(
        *[
            Arrow(
                [x + 0.55, y, 0],
                [x - 0.55, y, 0],
                color=theme.FIELD,
                buff=0,
                stroke_width=7,
                max_tip_length_to_length_ratio=0.5,
            ).set_z_index(-10)
            for y in rows
            for x in columns
        ]
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
            "rho = m \\/ (n e^2 tau)", "cobre: $tau = 2,4 times 10^(-14)$ s"
        )
        ions = BallCloud(cubic_lattice(5, 0.8), 0.15, theme.SPHERE_DARK)
        electrons = BallCloud(run.positions[0], 0.13, theme.ACCENT, z_offset=1000)
        frame = chart_frame()

        clock = ValueTracker(0)
        angle = ValueTracker(0.6)

        def field_is_on() -> bool:
            return FIELD_ON <= clock.get_value() / TAU < FIELD_OFF

        def place(cloud):
            cloud.view(angle.get_value(), PHI, ZOOM).shift(CENTER)

        def step(group):
            i = min(int(clock.get_value() * FPS), frames - 1)
            group.points3d = run.positions[i]
            place(group)

        backdrop = field_backdrop()
        label_on = Typst(
            "$ E eq.not 0 $", color=theme.FIELD, font_size=theme.LABEL_SIZE
        )
        label_off = Typst("$ E = 0 $", color=theme.MUTED, font_size=theme.LABEL_SIZE)
        for label in (label_on, label_off):
            label.move_to([theme.LEFT_EDGE + label.width / 2, theme.CORNER_Y, 0])

        def refresh_field(_):
            on = 1.0 if field_is_on() else 0.0
            for arrow in backdrop:
                arrow.set_stroke(opacity=FIELD_OPACITY * on)
                arrow.tip.set_fill(opacity=FIELD_OPACITY * on)
            label_on.set_opacity(on)
            label_off.set_opacity(1 - on)

        ions.add_updater(place)
        electrons.add_updater(step)
        curve = drift_curve(smooth, 2)
        curve.add_updater(
            lambda c: c.become(drift_curve(smooth, int(clock.get_value() * FPS)))
        )
        driver = VGroup().add_updater(refresh_field)

        self.add(heading, caption, driver, backdrop, label_on, label_off)
        self.play(FadeIn(ions), FadeIn(electrons))
        self.add(frame, curve)
        self.play(
            clock.animate.set_value(SIM_SECONDS - 1 / FPS),
            angle.animate.set_value(1.6),
            run_time=SIM_SECONDS,
            rate_func=linear,
        )
        for mob in (ions, electrons, curve, driver):
            mob.clear_updaters()
        self.play(FadeOut(*self.mobjects), run_time=0.6)

    def title_card(self):
        name = Typst("Drude", color=theme.INK, font_size=120)
        sub = Typst("¿por qué un cable resiste?", color=theme.ACCENT, font_size=48)
        sub.next_to(name, DOWN, buff=0.5)
        self.play(FadeIn(name), FadeIn(sub), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(name), FadeOut(sub), run_time=0.6)
