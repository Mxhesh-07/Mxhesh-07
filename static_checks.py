"""Static checks: XML validity, contrast, remote refs, sizing."""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ASSETS = Path(__file__).parent / "assets"
PANEL = (10, 17, 36)  # #0a1124, roughly the lightest part of the backdrop


def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg=PANEL):
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


fails = 0
for f in sorted(ASSETS.glob("*.svg")):
    raw = f.read_text(encoding="utf-8")
    ET.fromstring(raw)  # raises if malformed

    remote = re.findall(r'(?:xlink:)?href="(?!#)[^"]+"', raw)
    scripts = re.findall(r"<script|foreignObject|on\w+=", raw)
    ids = set(re.findall(r'\bid="([^"]+)"', raw))
    missing = sorted(set(re.findall(r"url\(#([^)]+)\)", raw)) - ids)
    print(f"{f.name:15} valid-xml  {len(raw) / 1024:5.1f} KB  "
          f"remote-refs={len(remote)}  forbidden={len(scripts)}  "
          f"missing-refs={len(missing)}")
    if missing:
        print(f"                undefined paint refs: {missing}")
    if remote or scripts or missing:
        fails += 1

# contrast of every distinct text fill
seen = {}
attr_re = re.compile(r'(\w[\w-]*)="([^"]*)"')
for f in sorted(ASSETS.glob("*.svg")):
    for m in re.finditer(r"<text\b([^>]*)>([^<]*)</text>", f.read_text(encoding="utf-8")):
        attrs = dict(attr_re.findall(m.group(1)))
        fill, label = attrs.get("fill", ""), m.group(2)
        if not re.fullmatch(r"#[0-9a-fA-F]{3,6}", fill):
            continue
        size = float(attrs.get("font-size", 16))
        prev = seen.get(fill)
        if prev is None or size < prev[1]:
            seen[fill] = (ratio(rgb(fill)), size, label)

print("\ntext fill      contrast  smallest-size  sample")
for fill, (c, size, label) in sorted(seen.items(), key=lambda kv: kv[1][0]):
    flag = ""
    if c < 3.0 and size >= 11:
        flag = "  <-- low contrast on body text"
        fails += 1
    print(f"{fill:12}  {c:5.2f}:1   {size:5.1f}px      {label[:30]!r}{flag}")

print(f"\n{fails} failure(s)")
sys.exit(1 if fails else 0)
