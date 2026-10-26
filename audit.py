"""
Pixel audit: a stand-in for looking at the PNGs.

Checks each render for ink coverage, accent-colour presence, and dead bands, so
a blank / clipped / monochrome render cannot pass unnoticed.
"""

import sys
from pathlib import Path
from PIL import Image
import colorsys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PREVIEW = Path(__file__).parent / "preview"

# hue families, in degrees. Thin antialiased strokes never hit an exact RGB value,
# so accents are detected by hue + saturation instead of pixel equality.
HUES = {
    "cyan/blue": (175, 215),
    "violet": (240, 288),
    "gold": (30, 60),
    "green": (140, 175),
    "rose": (330, 360),
}


def accent_of(px):
    r, g, b = px[:3]
    mx, mn = max(r, g, b), min(r, g, b)
    if mx < 70 or mx - mn < 38:
        return None
    h = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[0] * 360
    for name, (lo, hi) in HUES.items():
        if lo <= h <= hi:
            return name
    return None


fails = 0
for f in sorted(PREVIEW.glob("*.png")):
    im = Image.open(f).convert("RGB")
    w, h = im.size
    px = im.load()
    step = 3
    total = ink = bright = 0
    accents = {k: 0 for k in HUES}
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
            hit = accent_of((r, g, b))
            if hit:
                accents[hit] += 1

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
    if not found:
        problems.append("no accent colour at all (flat grey render?)")
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
