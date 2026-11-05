"""Drude model: electrons drift through a lattice of ions under a field."""

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Typst,
    ValueTracker,
    VGroup,
    VMobject,
    linear,
)

from animations import theme
from animations.balls import BallCloud, project
from animations.drude_sim import simulate

FPS = 30
PHI = 0.9  # camera tilt
LINE_OFFSETS = (-1.0, 0.0, 1.0)  # field lines cross the box in a 3 x 3 grid
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


def field_lines(angle: float) -> VGroup:
    """Thin arrows along +x through the lattice: the field acting on every electron."""
    lines = VGroup()
    for y in LINE_OFFSETS:
        for z in LINE_OFFSETS:
            start = CENTER + project([-2.0, y, z], angle, PHI)
            end = CENTER + project([2.0, y, z], angle, PHI)
            lines.add(
                Arrow(
                    start,
                    end,
                    color=theme.FIELD,
                    buff=0,
                    stroke_width=3,
                    tip_length=0.18,
                    max_tip_length_to_length_ratio=1,
                )
            )
    return lines.set_z_index(500)  # over the ions, under the electrons


PULSES_PER_LINE = 4
PULSE_PERIOD = 1.6  # seconds for a pulse to cross the box


def place_pulses(pulses: VGroup, angle: float, seconds: float, on: float) -> None:
    """Move blue dots along each field line, +x, so the field reads as flow."""
    index = 0
    for y in LINE_OFFSETS:
        for z in LINE_OFFSETS:
            for k in range(PULSES_PER_LINE):
                share = (seconds / PULSE_PERIOD + k / PULSES_PER_LINE) % 1
                point = [-2.0 + 4.0 * share, y, z]
                pulses[index].move_to(CENTER + project(point, angle, PHI))
                pulses[index].set_fill(opacity=0.9 * on)
                index += 1


def field_arrow(angle: float) -> Arrow:
    """The headline arrow, drawn above the lattice along the projected +x axis."""
    along = project([1.0, 0.0, 0.0], angle, PHI)
    along = along / np.linalg.norm(along)
    middle = CENTER + UP * 3.1
    return Arrow(
        middle - along * 1.5,
        middle + along * 1.5,
        color=theme.FIELD,
        buff=0,
        stroke_width=10,
        max_tip_length_to_length_ratio=1,
    ).set_z_index(2000)


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
        frame = chart_frame()

        clock = ValueTracker(0)
        angle = ValueTracker(0.6)

        def field_is_on() -> bool:
            return FIELD_ON <= clock.get_value() / TAU < FIELD_OFF

        def step(group):
            i = min(int(clock.get_value() * FPS), frames - 1)
            group.points3d = run.positions[i]
            group.view(angle.get_value(), PHI, 1.0).shift(CENTER)

        lines = field_lines(angle.get_value())
        arrow = field_arrow(angle.get_value())
        label_on = Typst("$ E eq.not 0 $", color=theme.FIELD, font_size=44)
        label_off = Typst("$ E = 0 $", color=theme.MUTED, font_size=44)
        pulses = VGroup(
            *[
                Dot(radius=0.07, color=theme.FIELD).set_z_index(600)
                for _ in range(len(LINE_OFFSETS) ** 2 * PULSES_PER_LINE)
            ]
        )

        def refresh_field(_):
            on = 1.0 if field_is_on() else 0.0
            place_pulses(pulses, angle.get_value(), clock.get_value(), on)
            for old, new in zip(lines, field_lines(angle.get_value()), strict=True):
                old.become(new)
                old.set_stroke(opacity=0.6 * on)
                old.tip.set_fill(opacity=0.6 * on)
            arrow.become(field_arrow(angle.get_value()))
            arrow.set_stroke(opacity=on).set_fill(opacity=on)
            label_on.move_to(arrow.get_end() + UP * 0.45).set_opacity(on)
            label_off.move_to(CENTER + UP * 3.1).set_opacity(1 - on)

        ions.add_updater(lambda m: m.view(angle.get_value(), PHI, 1.0).shift(CENTER))
        electrons.add_updater(step)
        curve = drift_curve(smooth, 2)
        curve.add_updater(
            lambda c: c.become(drift_curve(smooth, int(clock.get_value() * FPS)))
        )
        driver = VGroup().add_updater(refresh_field)

        self.add(heading, caption, driver, lines, pulses, arrow, label_on, label_off)
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
        sub = Typst("¿por qué un cable resiste?", color=theme.ACCENT, font_size=44)
        sub.next_to(name, DOWN, buff=0.5)
        self.play(FadeIn(name), FadeIn(sub), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(name), FadeOut(sub), run_time=0.6)
