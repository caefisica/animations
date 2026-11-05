"""House style for every scene: a 9:16 white page, serif text, one dark-red accent.

Text is Typst (math in `$ ... $`). Layout is fixed. The title sits at the top, the 3D scene in the middle, the
formula and its note below it, and an optional chart at the bottom.
"""

from manim import (
    UP,
    ManimColor,
    Typst,
    VGroup,
)

INK = ManimColor("#222222")
ACCENT = ManimColor("#8B2A1F")
MUTED = ManimColor("#8A8A8A")
SPHERE = ManimColor("#6E6E6E")
SPHERE_DARK = ManimColor("#4A4A4A")
FIELD = ManimColor("#2B4F8F")

TITLE_Y = 7.0
FORMULA_Y = -5.2
NOTE_Y = -6.3


def title(text: str) -> Typst:
    return Typst(text, color=INK, font_size=44).move_to(UP * TITLE_Y)


def formula(math: str) -> Typst:
    return Typst(f"$ {math} $", color=ACCENT, font_size=64).move_to(UP * FORMULA_Y)


def note(text: str) -> Typst:
    return Typst(text, color=MUTED, font_size=26).move_to(UP * NOTE_Y)


def caption(math: str, note_text: str) -> VGroup:
    return VGroup(formula(math), note(note_text))
