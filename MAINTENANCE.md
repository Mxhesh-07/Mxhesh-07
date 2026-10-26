# Maintaining this profile

Everything visual is generated. Don't hand-edit the SVG files — they get
overwritten the next time `build.py` runs.

The theme is Bleach: black page, paper-white ink, Ichigo orange, blood red,
zanpakuto, hollow hole, reiatsu shockwaves, 卍解.

## Layout

```
README.md            the profile itself
assets/*.svg         generated artwork (10 panels)
build.py             single source of truth for every panel
check.py             layout QA: overflow, collisions, crowding
static_checks.py     XML validity, remote refs, contrast ratios
audit.py             pixel audit of the rendered PNGs
preview.py           renders each SVG to preview/*.png
preview_github.py    renders a fake GitHub page at real content width
```

## Rebuild

```bash
python build.py        # regenerate assets/
python check.py        # must print 0 issue(s)
python static_checks.py
python preview.py      # optional: PNGs to eyeball
```

Then commit `assets/` and `README.md` together. If you change an asset without
committing the regenerated file, the profile keeps showing the old artwork.

## Updating content

**Shinigami file, metrics, seat** — the `PLAYER` dict in `build.py`:

```python
commits=123, repos=6, languages=11, tests=422
```

Those four are the only numbers rendered. Re-pull them from GitHub when they go
stale:

```bash
gh api graphql -f query='{ user(login:"Mxhesh-07") { repositories(first:20) {
  nodes { name defaultBranchRef { target { ... on Commit { history { totalCount } } } } } } } }'
```

**Projects** — the `QUESTS` list. One entry per card; the file name is derived
from `name`, so renaming a project needs its `README.md` `<img>` path updated
too. `status` is free text (`ACTIVE`, `ONE BOSS LEFT`, `SEALED`); `SEALED`
switches the stamp to pale blue, everything else uses orange. `threat` is the
thematic class shown above the card (MENOS / ARRANCAR).

**Abilities** — the `ABILITIES` list. Deliberately has no percentages. Only add
a tool here if at least one public repo uses it.

**Activity log** — the `LOG` list holds the five most recent pushes. **Rewards**
holds shipped work only; no certificates, no awards, no placeholders pretending
to be achievements.

## Animation

All motion is SMIL (`<animate>`, `<animateMotion>`, `stroke-dashoffset`). It
runs inside `<img>` because it is declarative SVG, not script. Current inventory:

| Panel | Motion |
| :-- | :-- |
| hero | two light slashes sweeping behind the figure, breathing reiatsu aura, hell butterfly on an `animateMotion` path, three reiatsu rings, pulsing sun and detection dot |
| player | breathing reiatsu aura behind the commit count |
| abilities | each release's reiatsu underline charges and fades, staggered |
| quests | a sheen sweeps across the panel, clipped to its cut corners |
| mission | aura pulse, objective rule draws itself left to right |
| log | sheen sweep across the log panel, blinking push beacon |
| footer | 卍解 draws its stroke, three reiatsu rings, a gleam runs up the planted zanpakuto, white bankai flash every 7s |

Tuning knobs are the `dur`, `begin` and `values` attributes in the generator —
keep `repeatCount="indefinite"` so the profile never freezes mid-animation. Keep
amplitudes small: GitHub renders the panels at ~79% width, and anything that
moves more than a few percent of the canvas reads as jitter rather than intent.

## Interactivity (and its limits)

A README cannot run JavaScript, and an SVG inside `<img>` never receives hover,
click or cursor events — GitHub's sanitizer removes both. So "interactive" here
means only what GitHub really supports:

- **`<details>` / `<summary>` blocks** in `README.md`: SHIKAI numbers, BANKAI
  project table, SQUAD contact. They open and close on click, no script needed.
- **Linked quest cards**: every 任務 panel is wrapped in `<a href>` to its repo,
  and the repo link in the BANKAI table stays clickable.

If a future request is "make it react to the mouse", the honest answer is that
GitHub cannot do it — the closest upgrade is more collapsibles or a linked
landing page.

## The character

The hero figure is drawn from scratch in `fighter()` — an original vector
homage, not traced from a frame. Back view, cropped at the waist, so there is no
face to get wrong: spiky orange hair (`HAIR` / `HAIR_D`), black shihakusho with
the white crossed under-collar, and a giant cleaver rising from behind the right
shoulder (`cleaver()`, positioned by the `translate(...) rotate(15)` in that
function).

Geometry knobs, top to bottom:

- head centre `cx, cy = 980, 300` and radii `rx, ry = 66, 80` — the head is sized
  to sit inside the hollow hole (`r=148`); move either and the framing breaks
- `torso` path — the shoulder curve and the crop width at y=800
- `hair_spikes()` — spike count, length range and the darker strands

The body fills with `gBody` (a near-black gradient) rather than flat black, so
the silhouette stays visible below the sun where the page is already black.
If the figure reads too heavy, raise the bottom stop of `gBody` or shrink
`ry`; if it reads as a blob, lengthen the spikes and raise the rim-light opacity.

## Placeholders left to replace

| Field | Where | Notes |
| :-- | :-- | :-- |
| Portrait | — | None used. The hero draws a stylised sun, hollow hole and zanpakuto instead of a photo, because SVG loaded as an image cannot fetch your GitHub avatar. |
| Seat (`16`) | `PLAYER["seat"]` | Thematic: `1 + commits // 8`. It is labelled `THEMATIC` on the panel and is **not** a rank. Recompute or delete the tile. |
| Threat class | `QUESTS[*]["threat"]` | Thematic difficulty label (MENOS / ARRANCAR), not a certification. |
| Email | `README.md` | `mxhesh.dev@gmail.com`. Change it in the SQUAD block if you'd rather use a different address. |
| Stars received | not shown | Your public repos currently have zero, so the metric was left out rather than displayed as a discouraging zero. Add it to the player tiles once it's meaningful. |
| Spoken languages | — | Not shown. The old "TAMIL · ENGLISH" row was dropped in the manga redesign; add it back to the registry rows if you want it. |

## Validation checklist

Run before pushing a change:

- [ ] `python check.py` prints `0 issue(s)`
- [ ] `python static_checks.py` prints `0 failure(s)` and `remote-refs=0`
- [ ] every `<img>` in `README.md` points at a file that exists in `assets/`
- [ ] each quest card's `<a href>` matches a real, public repository
- [ ] numbers in `PLAYER` still match the GitHub API
- [ ] no line claims a certification, award or completion you can't point at
- [ ] each panel still contains at least one `<animate>` (see the Animation table)
- [ ] preview at ~400px wide: panels scale to the column, never overflow
- [ ] alt text still describes each panel accurately
- [ ] `<details>` blocks still render collapsed and open on click on github.com

## Rendering rules learned the hard way

- GitHub strips `<style>` and `<script>`; the only styling that survives is
  inside the SVG files themselves. SMIL attributes survive, which is why every
  animation is built from `<animate>` / `<animateMotion>` rather than CSS.
- SVG loaded through `<img>` cannot fetch external fonts or images. Fonts are
  system stacks: Impact for the poster type, Segoe UI for body, and Yu Gothic →
  Hiragino → Noto CJK for the Japanese labels (死神ファイル, 斬魄刀, 任務, 卍解).
  A viewer with no CJK font at all would see empty boxes — the one rendering
  risk of the theme. Keep a Latin label beside every Japanese one.
- Decorative type (the giant translucent 斬/霊/装, the vertical 卍解, lightning
  lines) is wrapped in `<g data-deco="1">` so `check.py` ignores it when
  measuring text collisions. Art that is meant to be sat on top of other art
  needs that tag.
- Moving art that crosses text is also `data-deco`: the katana, slash sweep and
  butterfly deliberately pass over panels.
- Third-party stat cards (`github-readme-stats`, streak counters) are avoided on
  purpose — they fail silently, and a broken image looks worse than no image.
- Canvas width is 1200px but GitHub renders at roughly 79% of that, so the
  smallest text is kept at 10px+ to land at 8px on screen.
