# Maintaining this profile

Everything visual is generated. Don't hand-edit the SVG files — they get
overwritten the next time `build.py` runs.

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

**Player card, metrics, ranks** — the `PLAYER` dict in `build.py`:

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
too. Set `status` to `CLEARED` to switch the card to green.

**Abilities** — the `ABILITIES` list. Deliberately has no percentages. Only add
a tool here if at least one public repo uses it.

**Activity log** — the `LOG` list holds the five most recent pushes. **Rewards**
holds shipped work only; no certificates, no awards, no placeholders pretending
to be achievements.

## Placeholders left to replace

| Field | Where | Notes |
| :-- | :-- | :-- |
| Avatar / portrait | — | None used. The player card shows an `M` monogram instead, because SVG loaded as an image cannot fetch your GitHub avatar. |
| Spoken languages | `PLAYER["tongues"]` | Currently "TAMIL · ENGLISH". Add Kannada/Hindi if you want them listed. |
| Email | `README.md` | `mxhesh.dev@gmail.com`. Change it in the Connect line if you'd rather use a different address. |
| Stars received | not shown | Your public repos currently have zero, so the metric was left out rather than displayed as a discouraging zero. Add it to the player tiles once it's meaningful. |

## Validation checklist

Run before pushing a change:

- [ ] `python check.py` prints `0 issue(s)`
- [ ] `python static_checks.py` prints `0 failure(s)` and `remote-refs=0`
- [ ] every `<img>` in `README.md` points at a file that exists in `assets/`
- [ ] each quest card's `<a href>` matches a real, public repository
- [ ] numbers in `PLAYER` still match the GitHub API
- [ ] no line claims a certification, award or completion you can't point at
- [ ] preview at ~400px wide: panels scale to the column, never overflow
- [ ] alt text still describes each panel accurately

## Rendering rules learned the hard way

- GitHub strips `<style>` and `<script>`; the only styling that survives is
  inside the SVG files themselves.
- SVG loaded through `<img>` cannot fetch external fonts or images. Fonts are
  system stacks; the Korean watermark in the hero uses whatever CJK font the
  viewer has.
- Third-party stat cards (`github-readme-stats`, streak counters) are avoided on
  purpose — they fail silently, and a broken image looks worse than no image.
- Canvas width is 1200px but GitHub renders at roughly 79% of that, so the
  smallest text is kept at 10px+ to land at 8px on screen.
