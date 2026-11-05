"""Shaded balls under orthographic projection, drawn as 2D circles.

Manim's Cairo 3D path meshes every sphere and takes seconds per frame, and its
OpenGL renderer cannot draw Typst text. Under an orthographic camera a lit
sphere is a circle with a highlight, so a Circle with a sheen is enough and
renders at 2D speed. `BallCloud` owns the 3D positions, projects them for a
camera angle and sorts them back to front.
"""

import numpy as np
from manim import UL, Circle, ManimColor, VGroup


def rotation(theta: float, phi: float) -> np.ndarray:
    """Rotate about z by theta, then tilt about x by phi."""
    cz, sz = np.cos(theta), np.sin(theta)
    cx, sx = np.cos(phi), np.sin(phi)
    about_z = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    about_x = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    return about_x @ about_z


class BallCloud(VGroup):
    def __init__(
        self,
        points: np.ndarray,
        radius: float,
        color,
        sheen: float = 0.6,
        z_offset: int = 0,
    ):
        self.z_offset = z_offset
        self.points3d = np.asarray(points, dtype=float)
        self.base = ManimColor(color)
        self.radius = radius
        balls = []
        for _ in self.points3d:
            ball = Circle(radius=radius, stroke_width=0)
            ball.set_fill(ManimColor(color), opacity=1)
            ball.set_sheen(sheen, UL)
            balls.append(ball)
        super().__init__(*balls)
        self.view(0.0, 1.0)

    def color_at(self, near: float) -> ManimColor:
        """Darken far balls toward white so depth reads on a white page."""
        return self.base.interpolate(ManimColor("#FFFFFF"), 0.45 * (1 - near))

    def view(self, theta: float, phi: float, zoom: float = 1.0) -> "BallCloud":
        rotated = self.points3d @ rotation(theta, phi).T
        depth = rotated[:, 1]
        order = np.argsort(np.argsort(-depth))
        near = (depth - depth.min()) / max(np.ptp(depth), 1e-9)
        for ball, p, rank, n in zip(self.submobjects, rotated, order, near):
            ball.move_to([p[0] * zoom, p[2] * zoom, 0])
            ball.set_z_index(int(rank) + self.z_offset)
            ball.scale_to_fit_width(2 * self.radius * zoom * (0.8 + 0.2 * n))
            ball.set_fill(self.color_at(n))
        return self
