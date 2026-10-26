"""
Pixel audit: a stand-in for looking at the PNGs.

Checks each render for ink coverage, accent-colour presence, and dead bands, so
a blank / clipped / monochrome render cannot pass unnoticed.
"""

import sys
from pathlib import Path
from PIL import Image

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PREVIEW = Path(__file__).parent / "preview"
ACCENTS = {
    "blue": (79, 195, 255),
    "violet": (167, 139, 250),
    "gold": (251, 191, 36),
    "green": (74, 222, 128),
    "red": (251, 113, 133),
}


def near(px, target, tol=46):
    return all(abs(a - b) <= tol for a, b in zip(px[:3], target))


fails = 0
for f in sorted(PREVIEW.glob("*.png")):
    im = Image.open(f).convert("RGB")
    w, h = im.size
    px = im.load()
    step = 3
    total = ink = bright = 0
    accents = {k: 0 for k in ACCENTS}
    bands = [0] * 12
    band_n = [0] * 12
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y]
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            total += 1
            if lum > 32:
                ink += 1
            if lum > 150:
                bright += 1
            band = min(11, y * 12 // h)
            bands[band] += lum
            band_n[band] += 1
            for k, c in ACCENTS.items():
                if near((r, g, b), c):
                    accents[k] += 1
                        # only count one accent per pixel
                    break

    cov = 100 * ink / total
    brightpct = 100 * bright / total
    bandmeans = [b / n for b, n in zip(bands, band_n)]
    dead = sum(1 for m in bandmeans if m < 8)
    found = [k for k, v in accents.items() if v > total * 0.0001]

    problems = []
    if cov < 2:
        problems.append("almost no ink (blank render?)")
    if brightpct < 0.05:
        problems.append("no bright pixels (text missing?)")
    if len(found) < 2:
        problems.append(f"only {len(found)} accent colour(s): {found}")
    if dead > 4:
        problems.append(f"{dead}/12 dead horizontal bands")

    status = "OK " if not problems else "FAIL"
    print(f"[{status}] {f.name:16} {w}x{h}  ink={cov:5.1f}%  bright={brightpct:4.2f}%  "
          f"accents={','.join(found) or 'none'}")
    print("        band luminance: " + " ".join(f"{m:3.0f}" for m in bandmeans))
    for p in problems:
        print("        ! " + p)
        fails += 1

print(f"\n{fails} problem(s)")
sys.exit(1 if fails else 0)
