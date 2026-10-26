"""
Local stand-in for the GitHub profile page.

Builds preview/github.html from README.md with local asset paths (so it works
before the repo exists) and renders it at GitHub's real content width.
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
PREVIEW = ROOT / "preview"
PREVIEW.mkdir(exist_ok=True)

md = (ROOT / "README.md").read_text(encoding="utf-8")
md = re.sub(r"https://raw\.githubusercontent\.com/Mxhesh-07/Mxhesh-07/main/assets/",
            "../assets/", md)
md = re.sub(r"<sub>(.*?)</sub>", r'<p class="fine">\1</p>', md, flags=re.S)
md = re.sub(r"<code>(.*?)</code>", r"<code>\1</code>", md)
md = md.replace("**Connect** —", "<p><strong>Connect</strong> —")
md = md.replace("</p>\n\n<sub>", "</p>\n\n<p class=fine>")

# markdown -> html, only the bits this README uses
md = re.sub(r'<a href="([^"]+)">\s*\n?<img ([^>]+)>\s*\n?</a>',
            r'<a href="\1"><img \2></a>', md)
md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', md)
md = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", md)

html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Mxhesh-07 · profile preview</title>
<style>
  body {{ margin:0; background:#0d1117; color:#e6edf3;
         font:16px/1.5 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif; }}
  .wrap {{ max-width:1012px; margin:0 auto; padding:24px 32px 64px; }}
  .pinned {{ margin-top:32px; padding-top:24px; border-top:1px solid #30363d; }}
  .pinned h2 {{ font-size:16px; font-weight:400; color:#e6edf3; margin:0 0 12px; }}
  .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
  .card {{ border:1px solid #30363d; border-radius:6px; padding:16px; background:#0d1117; }}
  .card b {{ color:#58a6ff; font-weight:600; }}
  .card p {{ margin:6px 0 0; font-size:12px; color:#8b949e; }}
  a {{ color:#4493f8; text-decoration:none; }}
  img {{ max-width:100%; }}
  p {{ margin:16px 0; }}
  .fine {{ font-size:12px; color:#8b949e; }}
  .banner {{ font-size:12px; color:#8b949e; border:1px dashed #30363d;
             border-radius:6px; padding:8px 12px; margin-bottom:20px; }}
</style></head>
<body><div class="wrap">
<div class="banner">Local preview at GitHub's 1012px content width, dark theme.
Hover nothing, click nothing — this is just the layout.</div>
{md}
<div class="pinned">
  <h2>Pinned</h2>
  <div class="grid">
    <div class="card"><b>Mark-42</b><p>J.A.R.V.I.S.-style voice assistant for Windows</p></div>
    <div class="card"><b>kavach</b><p>Border video analytics · SIH 2026</p></div>
    <div class="card"><b>iTantraMessage</b><p>Offline Bluetooth messenger</p></div>
    <div class="card"><b>nemotron-data-forge</b><p>Graded dataset pipeline</p></div>
  </div>
</div>
</div></body></html>"""

(PREVIEW / "github.html").write_text(html, encoding="utf-8")


async def shot():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 1100, "height": 1400},
                                device_scale_factor=1)
        await page.goto((PREVIEW / "github.html").as_uri())
        await page.wait_for_timeout(900)
        await page.screenshot(path=str(PREVIEW / "github-full.png"), full_page=True)
        h = await page.evaluate("document.body.scrollHeight")
        print(f"preview/github.html  ({h}px tall) + github-full.png")
        await b.close()


asyncio.run(shot())
