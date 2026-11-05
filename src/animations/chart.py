"""A line chart at a fixed place on the page, mapping data to scene units."""

from dataclasses import dataclass

import numpy as np
from manim import Line, Typst, VGroup, VMobject

from animations import theme


@dataclass(frozen=True)
class Chart:
    left: float = theme.LEFT_EDGE + 0.3
    right: float = theme.RIGHT_EDGE
    bottom: float = -6.1
    top: float = -2.5
    x_min: float = 0.0
    x_max: float = 1.0
    y_min: float = 0.0
    y_max: float = 1.0

    def px(self, x: float) -> float:
        share = (x - self.x_min) / (self.x_max - self.x_min)
        return self.left + (self.right - self.left) * share

    def py(self, y: float) -> float:
        share = (y - self.y_min) / (self.y_max - self.y_min)
        return self.bottom + (self.top - self.bottom) * float(np.clip(share, 0, 1))

    def point(self, x: float, y: float) -> list[float]:
        return [self.px(x), self.py(y), 0]

    def axes(self, x_ticks, x_label: str, y_label: str) -> VGroup:
        base = self.py(self.y_min)
        group = VGroup(
            Line(
                [self.left, base, 0],
                [self.right, base, 0],
                color=theme.MUTED,
                stroke_width=2,
            ),
            Line(
                [self.left, self.bottom, 0],
                [self.left, self.top, 0],
                color=theme.MUTED,
                stroke_width=2,
            ),
        )
        for tick in x_ticks:
            group.add(
                Line(
                    [self.px(tick), base, 0],
                    [self.px(tick), base - 0.1, 0],
                    color=theme.MUTED,
                    stroke_width=2,
                ),
                Typst(
                    f"{tick:g}".replace(".", ","),
                    color=theme.MUTED,
                    font_size=theme.TICK_SIZE,
                ).move_to([self.px(tick), base - 0.4, 0]),
            )
        x_title = Typst(x_label, color=theme.MUTED, font_size=theme.LABEL_SIZE)
        x_title.move_to([self.right - x_title.width / 2, self.bottom - 0.95, 0])
        y_title = Typst(y_label, color=theme.MUTED, font_size=theme.LABEL_SIZE)
        y_title.move_to([self.left + y_title.width / 2, self.top + 0.45, 0])
        group.add(x_title, y_title)
        return group

    def curve(self, xs, ys, color, width: float = 5) -> VMobject:
        line = VMobject(stroke_color=color, stroke_width=width)
        line.set_points_as_corners([self.point(x, y) for x, y in zip(xs, ys)])
        return line
