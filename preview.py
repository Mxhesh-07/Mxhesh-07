"""Render the SVG assets to PNG so they can be inspected visually."""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
PREVIEW = ROOT / "preview"
PREVIEW.mkdir(exist_ok=True)

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<style>
  html,body{{margin:0;padding:0;background:#0d1117}}
  img{{display:block;width:1200px;height:auto}}
  .pad{{padding:20px}}
</style></head><body><div class="pad">
<img src="{uri}"></div></body></html>"""


async def main():
    names = sys.argv[1:] or [p.stem for p in sorted(ASSETS.glob("*.svg"))]

    # drop previews of panels that no longer exist (asset renders keep an .html sibling)
    live = {p.stem for p in ASSETS.glob("*.svg")}
    for stale in PREVIEW.glob("*.png"):
        if stale.stem not in live and (PREVIEW / f"{stale.stem}.html").exists():
            stale.unlink()
            (PREVIEW / f"{stale.stem}.html").unlink()
            print(f"removed stale {stale.name}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1260, "height": 900},
                                      device_scale_factor=2)
        for name in names:
            svg = ASSETS / f"{name}.svg"
            tmp = PREVIEW / f"{name}.html"
            tmp.write_text(TEMPLATE.format(uri=svg.as_uri()), encoding="utf-8")
            await page.goto(tmp.as_uri())
            await page.wait_for_timeout(600)
            el = await page.query_selector("img")
            await el.screenshot(path=str(PREVIEW / f"{name}.png"))
            print(f"rendered {name}.png")
        await browser.close()


asyncio.run(main())
