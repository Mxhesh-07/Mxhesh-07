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
| hero | two light slashes sweeping behind the mask, breathing reiatsu aura, hell butterfly on an `animateMotion` path, three reiatsu rings, pulsing sun and detection dot |
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

The hero does not draw a person. A hand-coded face reads as a cartoon at any
size — the version that tried it was rejected twice — so the hero carries the
hollow mask instead: an object with hard geometry, which vector drawing does
well. It is built in `hollow_head()` under
`<g transform="translate(980 320) rotate(-6)">`, so every coordinate below is
mask-local, origin at the centre of the face:

| Layer | Coordinates (local) |
| :-- | :-- |
| plate | egg outline, `-128..128 x`, `-178..200 y`, `url(#gMask)` white→bone gradient |
| form | `url(#gBoneShade)` radial light from upper left, `#7C766B` shadow side, `fBone` turbulence grain at 9% |
| brow shelf | `gBrow` band, `-120..-28 y`, 32% black |
| jaw shadow | `gJaw` band, `120..210 y`, 30% black |
| eye sockets | swept slits `-122..-32 x` and `32..122 x`, `-88..-40 y`, `#07070A` |
| socket embers | curved line `±104,-60` to `±42,-60`, `RED`, 3.6 s opacity pulse |
| engraved marks | three tapered black slashes per side, `#241F19` at 50% |
| nose slits | angled lines `±20,26` to `±10,-2` |
| grin | `-92..92 x`, `56..150 y`, nine fangs above and eight below, clipped to it |
| chips | `112,-108` and `-108,96` on the edge, dark bite plus a lit lip |
| cracks | brow `-10,-178` to `-2,-86`, temple `96,-98` to `104,-58`, jaw |
| rim light | 3.6 px white along the lit left edge |

The mask sits on the orange sun and overlaps the hollow hole, so it reads as
white-on-black at the top and white-on-orange at the chin. Keep it inside the
sun (`r=300` at `980,296`) and let it break the hole's edge — that overlap is
what makes it look lit from behind. The cleaver is drawn first, at
`translate(1105 760) rotate(12)`, so the blade rises behind the mask's right
side and out of frame, and only its white outline reads against the black
page. If the mask reads flat, raise the jaw shading or the rim light before
adding detail — value does the work, not line count.

A real photograph is the only way to put an actual face in the hero: drop the
file in `assets/` and embed it as base64, since an SVG loaded through `<img>`
cannot fetch remote images.

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
