# animations

Vertical physics reels, built with [Manim](https://www.manim.community/) and
[Typst](https://typst.app/). Each scene is one 9:16 video.

## Run

```sh
mise install
mise run setup
uv run manim render -r 540,960 --frame_rate 15 src/animations/scenes/drude.py DrudeGas   # preview
uv run manim render -qh src/animations/scenes/drude.py DrudeGas                          # final
```

`manim.cfg` sets the 1080×1920 page. Do not pass `-ql`, `-qm` or `-qh` when
previewing: they override the page with a 16:9 size. Use `-r WIDTH,HEIGHT`.

## Layout

| Path | Holds |
| --- | --- |
| `src/animations/theme.py` | Palette and the fixed page layout: title, scene, formula, note |
| `src/animations/balls.py` | `BallCloud`, shaded spheres drawn as 2D circles |
| `src/animations/scenes/` | One module per animation |

## Decisions

- **Typst, not LaTeX.** `manim[typst]` ships the compiler in a wheel. TinyTeX
  weighs 612 MB and its `tlmgr` failed on first use. Output matches closely, but
  fraction bars come out thin. Formulas go in `$ ... $` through `theme.formula`.
- **No 3D engine.** Manim's Cairo 3D meshes each sphere and took about 2 s per
  frame for 64 spheres. Its OpenGL renderer fails on Typst text
  (`set_stroke() got an unexpected keyword argument 'family'`, manim 0.22.1).
  `BallCloud` projects points itself and sorts them back to front.

## Site

`site/` is a Vite + Solid 2 page that shows the rendered animations in an
Instagram-style grid. Styles come from the culqi360 web app tokens. It deploys
to https://caefisica.github.io/animations/ with `.github/workflows/pages.yml`.

```sh
cd site
bun install
bun run dev        # local server
bun run typecheck && bun run test && bun run build
```

Add an animation by putting `<slug>.mp4` and `<slug>.png` in `site/public/media/`
and a row in `site/src/catalog.ts`.
