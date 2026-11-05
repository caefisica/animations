"""House style for every scene: a 9:16 white page, serif text, one dark-red accent.

Text is Typst (math in `$ ... $`). The page is a fixed grid: title at the top,
the 3D scene below it, a strip for the electric field, a chart, then the
formula and its note.
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

# Page grid in scene units (the frame is 9 wide and 16 tall). Nothing sits
# closer than MARGIN to an edge.
MARGIN = 0.6
LEFT_EDGE, RIGHT_EDGE = -4.5 + MARGIN, 4.5 - MARGIN
#
# Bands from the top, as the reference reel stacks them: title, the 3D scene
# with a corner label, the formula and its note as the scene's caption, then
# the chart. The chart's axis labels end at -7.2, 0.8 above the bottom edge.
TITLE_Y = 7.0
CORNER_Y = 6.2  # label in the scene's top-left corner
SCENE_Y = 3.8
FORMULA_Y = 0.2
NOTE_Y = -0.65

# Typst font sizes. At 120 px per unit, 30 or more stays legible on a phone.
TITLE_SIZE = 56
FORMULA_SIZE = 64
LABEL_SIZE = 36
TICK_SIZE = 30
NOTE_SIZE = 32


def title(text: str) -> Typst:
    return Typst(text, color=INK, font_size=TITLE_SIZE).move_to(UP * TITLE_Y)


def formula(math: str) -> Typst:
    return Typst(f"$ {math} $", color=ACCENT, font_size=FORMULA_SIZE).move_to(
        UP * FORMULA_Y
    )


def note(text: str) -> Typst:
    return Typst(text, color=MUTED, font_size=NOTE_SIZE).move_to(UP * NOTE_Y)


def caption(math: str, note_text: str) -> VGroup:
    return VGroup(formula(math), note(note_text))
