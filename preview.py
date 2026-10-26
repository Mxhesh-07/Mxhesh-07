"""Render the SVG assets to PNG so they can be inspected visually."""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
PREVIEW = ROOT / "preview"
PREVIEW.mkdir(exist_ok=True)


async def main():
    names = sys.argv[1:] or [p.stem for p in sorted(ASSETS.glob("*.svg"))]
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1260, "height": 900},
                                      device_scale_factor=2)
        for name in names:
            svg = ASSETS / f"{name}.svg"
            html = f"""<!doctype html><html><head><meta charset="utf-8">
<style>
  html,body{{margin:0;padding:0;background:#ffffff}}
  body.dark{{background:#0d1117}}
  img{{display:block;width:1200px;height:auto}}
  .pad{{padding:20px}}
</style></head><body class="dark"><div class="pad">
<img src="{svg.as_uri()}"></div></body></html>"""
            tmp = PREVIEW / f"{name}.html"
            tmp.write_text(html, encoding="utf-8")
            await page.goto(tmp.as_uri())
            await page.wait_for_timeout(600)
            el = await page.query_selector("img")
            await el.screenshot(path=str(PREVIEW / f"{name}.png"))
            print(f"rendered {name}.png")
        await browser.close()


asyncio.run(main())
