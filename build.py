"""
Solo Leveling style GitHub profile assets for Mxhesh-07.

Every number is real (GitHub API, 2026-10-26) except the attribute bars, which
are labelled SELF-ASSESSED. Progress percentages on quests are self-reported.

The canvas is 1200px wide but GitHub renders it at roughly 79% of that, so body
copy stays at 14px+ and secondary labels at 10px+ to remain legible.

Run:  python build.py     -> assets/*.svg
      python preview.py   -> preview/*.png
      python check.py     -> layout QA (overflow / collisions)
"""

from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

# -- palette ------------------------------------------------------------------
BG0, BG1 = "#04060e", "#0a1124"
INK = "#e6f0ff"
MUTED = "#8aa4c8"
DIM = "#4a648c"
LINE = "#1d3557"
BLUE = "#4fc3ff"
VIOLET = "#a78bfa"
GOLD = "#fbbf24"
RED = "#fb7185"
GREEN = "#4ade80"

FONT = ("ui-monospace,'SF Mono','Cascadia Mono','DejaVu Sans Mono',"
        "Consolas,'Liberation Mono',monospace")
KR = "'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR','NanumGothic',sans-serif"

DOT = "\u00b7"      # middle dot
ARROW = "\u2192"    # right arrow

# -- real data ----------------------------------------------------------------
DATA = dict(
    handle="Mxhesh-07",
    name="MAHESH S",
    klass="SHADOW CODER",
    job="PYTHON DEVELOPER",
    title="THE ONE WHO BUILDS ALONE",
    guild="SHREE DEVI INSTITUTE",
    rank="B",
    level=16,
    commits=123,
    next_level_at=128,
    repos=6,
    tests=422,
    languages=11,
    exp_pct=123 / 128,
)

QUESTS = [
    dict(rank="S", name="KAVACH", kind="BORDER VIDEO ANALYTICS",
         note=f"SIH 2026 {DOT} PS 26187 {DOT} MHA / SSB",
         tags=f"C++20 {DOT} CUDA {DOT} TensorRT {DOT} FastAPI",
         pct=0.90, status="IN PROGRESS"),
    dict(rank="S", name="MARK-42", kind="DESKTOP AI AGENT",
         note=f"Gemini Live {DOT} agentic tool loop {DOT} OpenGL hologram",
         tags=f"Python {DOT} Playwright {DOT} Ollama",
         pct=0.85, status="IN PROGRESS"),
    dict(rank="A", name="ITANTRAMESSAGE", kind="OFFLINE BT MESSENGER",
         note=f"422 tests {DOT} no INTERNET permission {DOT} Whisper x10 languages",
         tags=f"Kotlin {DOT} Android {DOT} RFCOMM",
         pct=0.70, status="1 BOSS LEFT"),
    dict(rank="A", name="NEMOTRON-DATA-FORGE", kind="DATASET PIPELINE",
         note=f"Topic {ARROW} graded, de-duplicated JSONL {DOT} Nebius x NVIDIA",
         tags=f"Python {DOT} Streamlit {DOT} Tavily",
         pct=1.0, status="CLEARED"),
]

ATTRS = [
    ("PYTHON", 0.92),
    ("COMPUTER VISION", 0.78),
    ("BACKEND", 0.74),
    ("MOBILE / ANDROID", 0.61),
    ("SYSTEMS / CUDA", 0.55),
]

EQUIP = [
    ("LANGUAGES", ["Python", "Kotlin", "C++", "SQL", "JavaScript"]),
    ("BACKEND", ["Django", "FastAPI", "REST APIs", "PostgreSQL", "SQLite"]),
    ("VISION / AI", ["OpenCV", "PyTorch", "Whisper", "Playwright", "TensorRT"]),
]


# -- helpers ------------------------------------------------------------------
def chamfer(x, y, w, h, c=18):
    return (f"M{x + c},{y} L{x + w - c},{y} L{x + w},{y + c} "
            f"L{x + w},{y + h - c} L{x + w - c},{y + h} "
            f"L{x + c},{y + h} L{x},{y + h - c} L{x},{y + c} Z")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=15, fill=INK, ls=2, weight="400", anchor="start",
         opacity=1.0, family=FONT, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}" opacity="{opacity}" {extra}>{esc(s)}</text>')


def brackets(x, y, w, h, size=20, color=BLUE, sw=2, opacity=0.85):
    p = []
    for cx, cy, dx, dy in ((x, y, 1, 1), (x + w, y, -1, 1),
                           (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        p.append(f'<path d="M{cx + dx * size},{cy} L{cx},{cy} L{cx},{cy + dy * size}" '
                 f'stroke="{color}" stroke-width="{sw}" fill="none" opacity="{opacity}"/>')
    return "".join(p)


def hexagon(cx, cy, r, fill="none", stroke=BLUE, sw=2, opacity=1.0, rot=0):
    import math
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 90 + rot)
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{opacity}"/>')


def bar(x, y, w, h, pct, color, uid, shimmer=True):
    cid = f"clip{uid}"
    out = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}"/></clipPath>']
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" '
               f'fill="#0d1a33" stroke="{LINE}" stroke-width="1"/>')
    out.append(f'<g clip-path="url(#{cid})">')
    out.append(f'<rect x="{x}" y="{y}" width="{w * pct:.1f}" height="{h}" rx="{h / 2}" fill="url(#grad{uid})"/>')
    if shimmer:
        out.append(f'<rect x="{x}" y="{y}" width="70" height="{h}" fill="url(#shim{uid})" opacity="0.5">'
                   f'<animate attributeName="x" from="{x - 80}" to="{x + w + 80}" '
                   f'dur="3.2s" repeatCount="indefinite"/></rect>')
    out.append("</g>")
    out.append(f'<defs><linearGradient id="grad{uid}" x1="0" y1="0" x2="1" y2="0">'
               f'<stop offset="0" stop-color="{color}" stop-opacity="0.55"/>'
               f'<stop offset="1" stop-color="{color}"/></linearGradient>'
               f'<linearGradient id="shim{uid}" x1="0" y1="0" x2="1" y2="0">'
               f'<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
               f'<stop offset="0.5" stop-color="#fff" stop-opacity="0.5"/>'
               f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>')
    return "".join(out)


DEFS = f"""
<defs>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="14" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG0}"/>
    <stop offset="0.55" stop-color="{BG1}"/>
    <stop offset="1" stop-color="#050a17"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{BLUE}" stop-opacity="0.9"/>
    <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0 H0 V40" fill="none" stroke="{LINE}" stroke-width="1" opacity="0.55"/>
  </pattern>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#9fd0ff" opacity="0.10"/>
  </pattern>
  <radialGradient id="vig" cx="0.5" cy="0.45" r="0.75">
    <stop offset="0.55" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.55"/>
  </radialGradient>
  <radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.55"/>
    <stop offset="0.45" stop-color="{VIOLET}" stop-opacity="0.16"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
</defs>
"""


def shell(w, h, body, title=None, subtitle=None):
    """Dark chamfered panel: grid, vignette, scanlines, corner brackets."""
    head = ""
    if title:
        head = (f'{text(44, 42, title, 16, BLUE, 5, "700")}'
                f'<rect x="44" y="54" width="240" height="2" fill="url(#edge)" opacity="0.9"/>'
                f'{text(w - 44, 42, subtitle or "", 12, DIM, 3, "400", anchor="end")}')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"
     viewBox="0 0 {w} {h}" role="img">
{DEFS}
  <g>
    <path d="{chamfer(1, 1, w - 2, h - 2, 26)}" fill="url(#bg)" stroke="{LINE}" stroke-width="1.5"/>
    <path d="{chamfer(1, 1, w - 2, h - 2, 26)}" fill="url(#grid)" opacity="0.5"/>
    <path d="{chamfer(1, 1, w - 2, h - 2, 26)}" fill="url(#vig)"/>
    <rect x="0" y="0" width="{w}" height="{h}" fill="url(#scan)" opacity="0.30">
      <animate attributeName="y" from="-{h}" to="{h}" dur="7s" repeatCount="indefinite"/>
    </rect>
    {brackets(1, 1, w - 2, h - 2, 26, BLUE, 2.5, 0.9)}
    {head}
  </g>
  {body}
</svg>
"""


# -- 1. hero ------------------------------------------------------------------
def hero():
    w, h = 1200, 420
    d = DATA
    b = []
    b.append('<g opacity="0.35">')
    for i, off in enumerate(range(5)):
        x = 760 + off * 46
        b.append(f'<rect x="{x}" y="0" width="2" height="{h}" fill="{BLUE}" '
                 f'opacity="{0.10 + 0.03 * i}"/>')
    b.append("</g>")

    b.append(text(44, 62, "SYSTEM // PLAYER PROFILE", 12, DIM, 5))
    b.append(f'<circle cx="1046" cy="58" r="4" fill="{GREEN}" filter="url(#glow)">'
             f'<animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/></circle>')
    b.append(text(1060, 62, "ONLINE", 12, GREEN, 4))

    b.append(f'<g filter="url(#soft)" opacity="0.45" data-deco="1">'
             f'{text(44, 172, d["name"], 66, BLUE, 7, "700")}</g>')
    b.append(text(44, 172, d["name"], 66, INK, 7, "700"))
    b.append(text(46, 214, "I BUILD SYSTEMS THAT SEE, HEAR, AND ACT.", 17, "#9dc4f0", 4))

    b.append(f'<rect x="44" y="242" width="620" height="1.5" fill="url(#edge)" opacity="0.8"/>')

    rows = [("JOB", d["job"]), ("TITLE", d["title"]), ("GUILD", d["guild"])]
    for i, (k, v) in enumerate(rows):
        y = 278 + i * 28
        b.append(text(44, y, k, 11, DIM, 4))
        b.append(text(146, y, v, 16, INK, 2.5, "700"))

    cx, cy, r = 1018, 176, 104
    b.append(hexagon(cx, cy, r, "rgba(11,26,48,0.85)", BLUE, 2, 0.95))
    b.append(hexagon(cx, cy, r - 12, "none", VIOLET, 1, 0.45, rot=30))
    b.append(f'<g filter="url(#glow)">{hexagon(cx, cy, r, "none", BLUE, 2.5, 0.9)}</g>')
    b.append(text(cx, cy - 46, "LEVEL", 12, MUTED, 6, anchor="middle"))
    b.append(text(cx, cy + 18, str(d["level"]), 62, INK, 2, "700", anchor="middle"))
    b.append(text(cx, cy + 50, "RANK " + d["rank"], 13, GOLD, 4, "700", anchor="middle"))
    b.append(f'<g opacity="0.5"><animateTransform attributeName="transform" type="rotate" '
             f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="26s" repeatCount="indefinite"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 16}" fill="none" stroke="{DIM}" '
             f'stroke-width="1" stroke-dasharray="3 14"/></g>')

    stats = [(d["repos"], "DUNGEONS"), (d["commits"], "COMMITS"),
             (d["tests"], "TESTS PASSING"), (d["languages"], "LANGUAGES")]
    xs = [44, 330, 590, 860]
    b.append(f'<rect x="44" y="356" width="1112" height="1" fill="{LINE}"/>')
    for (val, label), x in zip(stats, xs):
        b.append(text(x, 390, f"{val:02d}", 26, BLUE, 2, "700"))
        b.append(text(x, 410, label, 11, DIM, 4))

    return shell(w, h, "".join(b))


# -- 2. status window ---------------------------------------------------------
def status():
    w, h = 1200, 640
    d = DATA
    b = []
    b.append(text(44, 96, "STATUS WINDOW", 13, DIM, 5))

    info = [("NAME", d["name"]), ("JOB", d["job"]), ("CLASS", d["klass"]),
            ("TITLE", d["title"]), ("GUILD", d["guild"]),
            ("RANK", d["rank"] + "  " + DOT + "  AWAKENING")]
    for i, (k, v) in enumerate(info):
        y = 140 + i * 42
        b.append(text(44, y, k, 11, DIM, 4))
        b.append(text(44, y + 23, v, 18, INK, 2, "700"))
        b.append(f'<rect x="44" y="{y + 35}" width="470" height="1" fill="{LINE}" opacity="0.7"/>')

    b.append(f'<rect x="44" y="486" width="470" height="1" fill="{LINE}"/>')
    b.append(text(44, 516, "PASSIVE", 11, DIM, 4))
    b.append(text(44, 542, "NIGHT OWL  " + DOT + "  SHIPS WHAT RUNS", 15, VIOLET, 2, "700"))
    b.append(text(44, 576, "TITLE UNLOCKED AT 123 COMMITS", 11, DIM, 3))

    x, bw = 596, 470
    b.append(text(x, 96, "VITALS", 13, DIM, 5))
    vit = [("HP", "VITALITY", 0.78, RED, "78 / 100"),
           ("MP", "FOCUS", 0.64, BLUE, "64 / 100"),
           ("EXP", "TO NEXT LEVEL", d["exp_pct"], GOLD,
            f"{d['commits']} / {d['next_level_at']}")]
    for i, (tag, label, pct, color, val) in enumerate(vit):
        y = 128 + i * 66
        b.append(text(x, y + 13, tag, 14, color, 3, "700"))
        b.append(text(x + 56, y + 13, label, 12, MUTED, 3))
        b.append(text(x + bw, y + 13, val, 13, INK, 1.5, "700", anchor="end"))
        b.append(bar(x, y + 24, bw, 12, pct, color, f"s{i}"))

    b.append(text(x, 352, "ATTRIBUTES", 13, DIM, 5))
    b.append(text(x + bw, 352, "SELF-ASSESSED", 10.5, DIM, 3, anchor="end"))
    for i, (name, val) in enumerate(ATTRS):
        y = 380 + i * 48
        b.append(text(x, y + 11, name, 13.5, INK, 2.5))
        b.append(text(x + bw, y + 11, f"{int(val * 100)}", 13, BLUE, 1.5, "700", anchor="end"))
        b.append(bar(x, y + 22, bw, 9, val, BLUE, f"a{i}"))

    return shell(w, h, "".join(b), "STATUS", "PLAYER " + DOT + " Mxhesh-07 " + DOT + " LV 16")


# -- 3. quest log -------------------------------------------------------------
def quests():
    w, h = 1200, 860
    b = []
    b.append(text(44, 96, "QUEST LOG", 13, DIM, 5))
    b.append(text(1156, 96, "4 ACTIVE", 12, GOLD, 3, "700", anchor="end"))

    for i, q in enumerate(QUESTS):
        y = 120 + i * 172
        ch = 152
        cleared = q["pct"] >= 1.0
        color = GREEN if cleared else (GOLD if q["rank"] == "S" else BLUE)
        b.append(f'<path d="{chamfer(36, y, w - 72, ch, 14)}" fill="#080e1c" '
                 f'stroke="{LINE}" stroke-width="1.2"/>')
        b.append(f'<rect x="36" y="{y}" width="4" height="{ch}" fill="{color}" opacity="0.85"/>')

        hx, hy = 102, y + 56
        b.append(hexagon(hx, hy, 31, "rgba(10,24,44,0.9)", color, 2, 1))
        b.append(text(hx, hy + 12, q["rank"], 27, color, 2, "700", anchor="middle"))
        b.append(text(hx, hy + 54, "RANK", 10, DIM, 3, anchor="middle"))

        b.append(text(164, y + 46, q["name"], 28, INK, 3, "700"))
        b.append(text(164, y + 71, q["kind"], 12.5, MUTED, 4))
        b.append(text(164, y + 98, q["note"], 14, "#9db6d8", 1.2))
        b.append(text(164, y + 123, q["tags"], 13, VIOLET, 1.5, opacity=0.9))

        pw = 140
        b.append(f'<rect x="{w - 60 - pw}" y="{y + 26}" width="{pw}" height="28" rx="3" '
                 f'fill="none" stroke="{color}" stroke-width="1" opacity="0.9"/>')
        b.append(text(w - 60 - pw / 2, y + 45, q["status"], 11.5, color, 2.5, "700", anchor="middle"))

        bx, bwd = 164, w - 328
        b.append(text(bx, y + 143, "PROGRESS", 11, DIM, 3))
        b.append(text(bx + bwd, y + 143, f"{int(q['pct'] * 100)}%", 11.5, color, 2, "700", anchor="end"))
        b.append(bar(bx, y + 110, bwd, 8, q["pct"], color, f"q{i}"))

    b.append(text(44, h - 26, "CLEAR A DUNGEON " + ARROW + " PIN THE REPO", 10.5, DIM, 3))
    b.append(text(w - 44, h - 26, "PROGRESS SELF-REPORTED", 10.5, DIM, 3, anchor="end"))

    return shell(w, h, "".join(b), "QUESTS", "ARISE")


# -- 4. equipment -------------------------------------------------------------
def equipment():
    w, h = 1200, 380
    b = []
    b.append(text(44, 96, "EQUIPMENT", 13, DIM, 5))

    xs = [44, 424, 804]
    for (cat, items), x in zip(EQUIP, xs):
        b.append(text(x, 138, cat, 11.5, GOLD, 4, "700"))
        b.append(f'<rect x="{x}" y="148" width="330" height="1" fill="{LINE}"/>')
        for j, it in enumerate(items):
            y = 184 + j * 34
            b.append(f'<path d="M{x} {y - 9} l8 9 l-8 9" fill="none" stroke="{BLUE}" '
                     f'stroke-width="1.5" opacity="0.7"/>')
            b.append(text(x + 24, y, it, 16, INK, 2))

    b.append(text(44, h - 30, "SHADOW ARMY " + DOT + " 11 LANGUAGES UNDER CONTRACT", 11, DIM, 3))

    return shell(w, h, "".join(b), "LOADOUT", "PLAYER " + DOT + " Mxhesh-07")


# -- 5. footer ----------------------------------------------------------------
def footer():
    w, h = 1200, 300
    b = []
    # bloom first, so it sits behind everything
    b.append(f'<ellipse cx="{w / 2}" cy="186" rx="330" ry="96" fill="url(#bloom)" data-deco="1"/>')
    b.append(f'<text x="{w / 2}" y="106" font-family="{KR}" font-size="42" '
             f'fill="{VIOLET}" opacity="0.34" text-anchor="middle" letter-spacing="16" '
             f'data-deco="1">\uc77c\uc5b4\ub098\ub77c</text>')
    b.append(f'<g filter="url(#glow)" opacity="0.9">'
             f'{text(w / 2, 198, "ARISE", 46, INK, 18, "700", anchor="middle")}</g>')
    b.append(f'<rect x="{w / 2 - 210}" y="220" width="420" height="1.5" fill="url(#edge)"/>')
    b.append(text(w / 2, 254, "THE SYSTEM AWAITS YOUR NEXT DUNGEON", 11.5, DIM, 5, anchor="middle"))

    return shell(w, h, "".join(b))


if __name__ == "__main__":
    files = {
        "hero.svg": hero(),
        "status.svg": status(),
        "quests.svg": quests(),
        "equipment.svg": equipment(),
        "footer.svg": footer(),
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name}  ({len(svg) / 1024:.1f} KB)")
