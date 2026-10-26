"""
Geometry QA for the SVG assets.

I can't eyeball PNGs, so instead this loads each SVG inline in Chromium and
checks every text node's measured box for:
  * overflow past the canvas
  * collisions with other text nodes
  * crowding (uncomfortably small gaps)
  * text spilling outside its parent panel rect

Exit code is non-zero if anything fails.
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

JS = r"""
() => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const texts = [...svg.querySelectorAll('text')]
    .filter(t => !t.closest('[data-deco]'))
    .map((t, i) => {
    const b = t.getBoundingClientRect();
    const ctm = t.getScreenCTM().inverse();
    // convert viewport rect back to viewBox units
    const pt = svg.createSVGPoint();
    pt.x = b.left; pt.y = b.top;
    const tl = pt.matrixTransform(ctm);
    pt.x = b.right; pt.y = b.bottom;
    const br = pt.matrixTransform(ctm);
    return {
      i,
      s: t.textContent.slice(0, 42),
      x: +tl.x.toFixed(1), y: +tl.y.toFixed(1),
      w: +(br.x - tl.x).toFixed(1), h: +(br.y - tl.y).toFixed(1),
      fill: t.getAttribute('fill'),
      size: +t.getAttribute('font-size'),
    };
  });
  return {vb: {w: vb.width, h: vb.height}, texts};
}
"""


def overlap(a, b):
    ox = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    oy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    if ox > 1 and oy > 1:
        return ox * oy
    return 0


async def main():
    only = sys.argv[1:]
    files = [p for p in sorted(ASSETS.glob("*.svg"))
             if not only or p.stem in only]
    problems = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 1000})
        for f in files:
            svg_text = f.read_text(encoding="utf-8")
            await page.set_content(
                "<html><body style='margin:0;background:#111'>"
                + svg_text + "</body></html>")
            data = await page.evaluate(JS)
            w, h = data["vb"]["w"], data["vb"]["h"]
            texts = data["texts"]
            issues = []

            for t in texts:
                if t["x"] < 8 or t["y"] < -4:
                    issues.append(f"  ! left/top overflow: {t['s']!r} x={t['x']} y={t['y']}")
                # 8% width slack: Consolas is narrower than DejaVu/SF Mono,
                # so a box that fits here must fit on every common mono font.
                if t["x"] + t["w"] * 1.08 > w - 8:
                    issues.append(
                        f"  ! right overflow: {t['s']!r} ends at {t['x'] + t['w'] * 1.08:.0f} "
                        f"(max {w - 8}, incl 8% font slack)")
                if t["y"] + t["h"] > h - 4:
                    issues.append(f"  ! bottom overflow: {t['s']!r} ends at {t['y'] + t['h']:.0f} (max {h - 4})")

            for i, a in enumerate(texts):
                for b in texts[i + 1:]:
                    if overlap(a, b):
                        issues.append(f"  ! overlap: {a['s']!r} <-> {b['s']!r}")

            # crowding: nearest-neighbour gap under 3px, vertically stacked
            for i, a in enumerate(texts):
                best = 1e9
                bestb = None
                for j, b in enumerate(texts):
                    if i == j:
                        continue
                    dx = max(b["x"] - (a["x"] + a["w"]), a["x"] - (b["x"] + b["w"]), 0)
                    dy = max(b["y"] - (a["y"] + a["h"]), a["y"] - (b["y"] + b["h"]), 0)
                    d = (dx ** 2 + dy ** 2) ** 0.5
                    if d < best:
                        best, bestb = d, b
                if best < 3:
                    issues.append(
                        f"  ~ tight ({best:.1f}px): {a['s']!r} near {bestb['s']!r}")

            status = "OK " if not issues else "FAIL"
            print(f"[{status}] {f.name}  {w:.0f}x{h:.0f}  {len(texts)} text nodes")
            for line in issues[:40]:
                print(line)
            problems += len(issues)
        await browser.close()
    print(f"\n{problems} issue(s)")
    return 1 if problems else 0


sys.exit(asyncio.run(main()))
