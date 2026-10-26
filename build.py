"""
Solo Leveling inspired GitHub profile assets - v2.

Palette and structure follow the design brief:
  bg #050711 / panel #10182B / blue #38BDF8 / cyan #67E8F9
  violet #8B5CF6 / shadow #4C1D95 / text #F1F5F9 / muted #94A3B8

All figures are pulled from the GitHub API (2026-10-26) or from the repos'
own READMEs. Nothing is invented: no skill percentages, no fake stars, no
claimed certifications.

Canvas is 1200px wide; GitHub renders it at roughly 79% of that, so body copy
stays at 16px+ and labels at 12px+.

Run: python build.py
"""

import math
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

# -- palette ------------------------------------------------------------------
BG = "#050711"
BG2 = "#0B1020"
PANEL = "#10182B"
BLUE = "#38BDF8"
CYAN = "#67E8F9"
VIOLET = "#8B5CF6"
SHADOW = "#4C1D95"
INK = "#F1F5F9"
MUTED = "#94A3B8"
DIM = "#64748B"
LINE = "#1E293B"
LINE2 = "#243049"
GOLD = "#FCD34D"
GREEN = "#34D399"

MONO = ("ui-monospace,'SF Mono','Cascadia Mono','DejaVu Sans Mono',"
        "Consolas,'Liberation Mono',monospace")
SANS = ("'Segoe UI','Helvetica Neue',Helvetica,Arial,'Noto Sans',sans-serif")

DOT = "\u00b7"
ARROW = "\u2192"
DIAMOND = "\u25c6"

# -- verified data ------------------------------------------------------------
PLAYER = dict(
    handle="Mxhesh-07",
    name="MAHESH",
    role="STUDENT DEVELOPER",
    klass="DEVELOPER",
    rank="E \u2192 S",
    spec="AI " + DOT + " PYTHON " + DOT + " WEB",
    quest="BUILD USEFUL SOFTWARE",
    status="LEARNING " + DOT + " BUILDING " + DOT + " EVOLVING",
    tongues="TAMIL " + DOT + " ENGLISH",
    repos=6,
    commits=123,
    languages=11,
    tests=422,
)

# difficulty is thematic, not an award
QUESTS = [
    dict(rank="S", name="Mark-42", kind="DESKTOP AI ASSISTANT",
         desc="Always-on voice agent that drives a Windows desktop: Gemini Live "
              "audio, a planner/executor tool loop, screen OCR and browser control.",
         tech="Python / Gemini Live / Playwright / OpenGL",
         status="ACTIVE", url="https://github.com/Mxhesh-07/Mark-42"),
    dict(rank="S", name="KAVACH", kind="BORDER VIDEO ANALYTICS",
         desc="Smart India Hackathon 2026, PS 26187. Sub-3ms inference dispatch over "
              "CCTV, thermal and drone feeds with sealed event logs.",
         tech="C++20 / CUDA / TensorRT / FastAPI",
         status="ACTIVE", url="https://github.com/Mxhesh-07/kavach"),
    dict(rank="A", name="iTantraMessage", kind="OFFLINE MESSENGER",
         desc="Peer-to-peer messaging over raw Bluetooth. No server, no account, and no "
              "INTERNET permission in the release build. 422 tests passing.",
         tech="Kotlin / Android / RFCOMM / Whisper",
         status="ONE BOSS LEFT", url="https://github.com/Mxhesh-07/iTantraMessage"),
    dict(rank="A", name="nemotron-data-forge", kind="DATASET PIPELINE",
         desc="Turns a topic into a graded, de-duplicated, fine-tuning-ready dataset. "
              "Nebius x NVIDIA hackathon build.",
         tech="Python / Streamlit / Tavily",
         status="CLEARED", url="https://github.com/Mxhesh-07/nemotron-data-forge"),
]

ABILITIES = [
    ("CORE", ["Python", "JavaScript", "HTML", "CSS"], BLUE),
    ("AI & VISION", ["AI API integration", "Computer vision", "Voice assistants",
                     "Automation"], CYAN),
    ("TOOLING", ["Git", "GitHub", "VS Code", "FastAPI", "OpenCV", "Docker"], VIOLET),
]

LOG = [
    ("2026.10.22", "Mark-42", "Python"),
    ("2026.10.19", "nemotron-data-forge", "Python"),
    ("2026.10.05", "iTantraMessage", "Kotlin"),
    ("2026.09.29", "kavach", "Python / C++"),
    ("2026.07.27", "Portfolio-", "CSS"),
]

REWARDS = [
    ("SIH 2026", "KAVACH submitted to Smart India Hackathon, PS 26187"),
    ("422 TESTS", "iTantraMessage unit suite, 0 failures"),
    ("OFFLINE GATE", "Release build ships without INTERNET permission"),
]


# -- helpers ------------------------------------------------------------------
def chan(w, h, c):
    return (f"M{c},0 L{w - c},0 L{w},0 L{w},{h - c} L{w - c},{h} "
            f"L{c},{h} L0,{h} L0,{c} Z")


def chamfer(x, y, w, h, c=14):
    return (f"M{x + c},{y} L{x + w - c},{y} L{x + w},{y + c} "
            f"L{x + w},{y + h - c} L{x + w - c},{y + h} "
            f"L{x + c},{y + h} L{x},{y + h - c} L{x},{y + c} Z")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def T(x, y, s, size=16, fill=INK, ls=1.5, weight="400", anchor="start",
      opacity=1.0, family=MONO, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}" opacity="{opacity}" {extra}>{esc(s)}</text>')


def hexagon(cx, cy, r, fill="none", stroke=BLUE, sw=1.5, opacity=1.0, rot=0):
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 90 + rot)
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{opacity}"/>')


def chip(x, y, w, h, label, color, size=12.5, ls=2.5, fill="none", rx=4):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{color}" stroke-width="1" opacity="0.75"/>'
            + T(x + w / 2, y + h / 2 + size * 0.36, label, size, color, ls, "600",
                anchor="middle"))


def defs():
    return f"""
<defs>
  <linearGradient id="page" x1="0" y1="0" x2="0.2" y2="1">
    <stop offset="0" stop-color="{BG}"/>
    <stop offset="0.55" stop-color="#070B18"/>
    <stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0.4">
    <stop offset="0" stop-color="{INK}"/>
    <stop offset="0.55" stop-color="{CYAN}"/>
    <stop offset="1" stop-color="{BLUE}"/>
  </linearGradient>
  <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{BLUE}" stop-opacity="0.85"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PANEL}"/>
    <stop offset="1" stop-color="#0C1322"/>
  </linearGradient>
  <radialGradient id="aura" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.20"/>
    <stop offset="0.55" stop-color="{VIOLET}" stop-opacity="0.10"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vig" cx="0.5" cy="0.42" r="0.78">
    <stop offset="0.5" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.45"/>
  </radialGradient>
  <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="{BLUE}" opacity="0.16"/>
  </pattern>
  <filter id="glow" x="-70%" y="-70%" width="240%" height="240%">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="halo" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="26" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
"""


def panel(w, h, body, accent=BLUE, scan=True):
    """Base surface: gradient page, dot grid, vignette, hairline border, one accent rule."""
    sweep = ""
    if scan:
        sweep = (f'<rect x="0" y="0" width="{w}" height="2" fill="{CYAN}" opacity="0.10">'
                 f'<animate attributeName="y" from="-4" to="{h}" dur="11s" '
                 f'repeatCount="indefinite"/></rect>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"
     viewBox="0 0 {w} {h}" role="img">
{defs()}
  <g>
    <path d="{chamfer(0.5, 0.5, w - 1, h - 1, 18)}" fill="url(#page)"/>
    <path d="{chamfer(0.5, 0.5, w - 1, h - 1, 18)}" fill="url(#dots)" opacity="0.5"/>
    <path d="{chamfer(0.5, 0.5, w - 1, h - 1, 18)}" fill="url(#vig)"/>
    <path d="{chamfer(0.5, 0.5, w - 1, h - 1, 18)}" fill="none"
          stroke="{LINE2}" stroke-width="1"/>
    <rect x="0" y="0.5" width="{w}" height="1.4" fill="url(#rule)" opacity="0.55"/>
    <rect x="0" y="0.5" width="96" height="1.4" fill="{accent}" opacity="0.9"/>
    {sweep}
  </g>
  {body}
</svg>
"""


def section(x, label, color=DIM, width=None):
    """Small section label with a trailing hairline."""
    out = T(x, 46, label, 13, color, 5, "600")
    if width:
        out += (f'<rect x="{x + width}" y="40" width="80" height="1" fill="{LINE2}"/>')
    return out


# -- 1. hero ------------------------------------------------------------------
def hero():
    w, h = 1200, 576
    b = []
    cx, cy = 600, 268

    # aura + magic circle
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="440" ry="250" fill="url(#aura)"/>')
    b.append(f'<g opacity="0.5"><animateTransform attributeName="transform" type="rotate" '
             f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="90s" repeatCount="indefinite"/>'
             f'<circle cx="{cx}" cy="{cy}" r="196" fill="none" stroke="{BLUE}" '
             f'stroke-width="1" stroke-dasharray="2 12" opacity="0.55"/></g>')
    b.append(f'<g opacity="0.4"><animateTransform attributeName="transform" type="rotate" '
             f'from="360 {cx} {cy}" to="0 {cx} {cy}" dur="140s" repeatCount="indefinite"/>'
             f'<circle cx="{cx}" cy="{cy}" r="238" fill="none" stroke="{VIOLET}" '
             f'stroke-width="1" stroke-dasharray="40 26 6 26" opacity="0.5"/></g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="164" fill="none" stroke="{LINE2}" stroke-width="1"/>')

    # rune ticks
    for i in range(24):
        a = math.radians(i * 15)
        r1, r2 = 210, 216 if i % 3 else 224
        b.append(f'<line x1="{cx + r1 * math.cos(a):.1f}" y1="{cy + r1 * math.sin(a):.1f}" '
                 f'x2="{cx + r2 * math.cos(a):.1f}" y2="{cy + r2 * math.sin(a):.1f}" '
                 f'stroke="{BLUE}" stroke-width="1" opacity="0.30"/>')

    # particles
    stars = [(140, 120, 1.6, 0.5), (232, 392, 1.2, 0.35), (300, 96, 1.1, 0.3),
             (392, 470, 1.7, 0.45), (486, 88, 1.3, 0.3), (760, 74, 1.4, 0.4),
             (842, 460, 1.5, 0.4), (930, 140, 1.2, 0.32), (1010, 330, 1.6, 0.5),
             (1082, 210, 1.2, 0.3), (700, 502, 1.3, 0.34), (520, 500, 1.2, 0.3),
             (120, 300, 1.1, 0.28), (1064, 470, 1.4, 0.38)]
    for i, (x, y, r, o) in enumerate(stars):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CYAN}" opacity="{o}">'
                 f'<animate attributeName="opacity" values="{o};{o * 0.25:.2f};{o}" '
                 f'dur="{3 + (i % 4)}s" repeatCount="indefinite"/></circle>')

    b.append(T(cx, 76, f"{DIAMOND} HUNTER SYSTEM // 001", 12.5, MUTED, 6, "500",
               anchor="middle"))
    b.append(f'<rect x="{cx - 120}" y="90" width="240" height="1" fill="url(#rule)" opacity="0.7"/>')

    # title
    b.append(f'<g filter="url(#halo)" opacity="0.35" data-deco="1">'
             f'{T(cx, 268, PLAYER["name"], 104, BLUE, 16, "700", anchor="middle", family=SANS)}</g>')
    b.append(T(cx, 268, PLAYER["name"], 104, "url(#title)", 16, "700", anchor="middle",
               family=SANS))
    b.append(T(cx, 330, "SHADOW DEVELOPER", 21, BLUE, 13, "600", anchor="middle"))

    b.append(f'<rect x="{cx - 210}" y="356" width="420" height="1" fill="url(#rule)" opacity="0.8"/>')

    b.append(T(cx, 394, "Every developer starts at level 1.", 19, INK, 1, "400",
               anchor="middle", family=SANS, opacity=0.92))
    b.append(T(cx, 424,
               "Student developer building AI assistants, computer vision and web apps "
               "with Python.", 15.5, MUTED, 0.6, "400", anchor="middle", family=SANS))

    # system initialised chip
    cw = 268
    b.append(f'<rect x="{cx - cw / 2}" y="458" width="{cw}" height="38" rx="4" '
             f'fill="#0A1728" stroke="{CYAN}" stroke-width="1" opacity="0.9"/>')
    b.append(f'<circle cx="{cx - cw / 2 + 26}" cy="477" r="4" fill="{GREEN}" filter="url(#glow)">'
             f'<animate attributeName="opacity" values="1;0.15;1" dur="2.4s" '
             f'repeatCount="indefinite"/></circle>')
    b.append(T(cx - cw / 2 + 44, 482, "SYSTEM INITIALIZED", 13, CYAN, 4, "600"))

    b.append(T(56, 540, "PLAYER " + PLAYER["handle"].upper(), 11.5, DIM, 3))
    b.append(T(w - 56, 540, "STATUS: ONLINE", 11.5, GREEN, 3, anchor="end"))

    return panel(w, h, "".join(b))


# -- 2. player status ---------------------------------------------------------
def player():
    w, h = 1200, 476
    b = [section(56, "PLAYER STATUS", BLUE, 600)]

    # monogram card
    b.append(f'<rect x="56" y="76" width="300" height="252" rx="6" fill="url(#card)" '
             f'stroke="{LINE2}" stroke-width="1"/>')
    b.append(f'<ellipse cx="206" cy="176" rx="120" ry="86" fill="url(#aura)" opacity="0.55"/>')
    b.append(hexagon(206, 168, 62, "#0A1728", BLUE, 1.5, 0.9))
    b.append(hexagon(206, 168, 54, "none", VIOLET, 1, 0.45, rot=30))
    b.append(T(206, 188, "M", 54, INK, 0, "700", anchor="middle", family=SANS))
    b.append(T(206, 262, PLAYER["name"], 24, INK, 5, "600", anchor="middle", family=SANS))
    b.append(T(206, 288, PLAYER["role"], 11.5, MUTED, 4, "500", anchor="middle"))
    b.append(T(206, 316, PLAYER["tongues"], 10.5, DIM, 3, anchor="middle"))

    # identity rows
    rows = [("PLAYER", PLAYER["handle"]), ("CLASS", PLAYER["klass"]),
            ("RANK", PLAYER["rank"]), ("SPECIALIZATION", PLAYER["spec"]),
            ("CURRENT QUEST", PLAYER["quest"]), ("STATUS", PLAYER["status"])]
    x, rw = 396, 748
    for i, (k, v) in enumerate(rows):
        y = 100 + i * 42
        b.append(T(x, y, k, 11.5, DIM, 4))
        b.append(T(x + 190, y, v, 15.5, INK, 1.6, "500"))
        b.append(f'<rect x="{x}" y="{y + 14}" width="{rw}" height="1" fill="{LINE}" opacity="0.75"/>')

    b.append(T(x, 344, "RANK SHOWS PROGRESSION, NOT A CERTIFICATION", 10.5, DIM, 2.5))

    # metric tiles
    tiles = [(PLAYER["commits"], "COMMITS"), (PLAYER["repos"], "PUBLIC REPOS"),
             (PLAYER["languages"], "LANGUAGES"), (PLAYER["tests"], "PASSING TESTS")]
    tw, gap = 252, 20
    for i, (val, label) in enumerate(tiles):
        tx = 56 + i * (tw + gap)
        b.append(f'<rect x="{tx}" y="352" width="{tw}" height="96" rx="6" fill="url(#card)" '
                 f'stroke="{LINE2}" stroke-width="1"/>')
        b.append(f'<rect x="{tx}" y="352" width="3" height="96" fill="{BLUE}" opacity="0.8"/>')
        b.append(T(tx + 22, 398, f"{val:02d}", 34, INK, 1, "700", family=SANS))
        b.append(T(tx + 22, 424, label, 11, MUTED, 3))

    return panel(w, h, "".join(b))


# -- 3. abilities -------------------------------------------------------------
def abilities():
    w, h = 1200, 372
    b = [section(56, "HUNTER ABILITIES", CYAN, 600),
         T(1144, 46, "NO PERCENTAGES " + DOT + " WHAT I ACTUALLY USE", 10.5, DIM, 2.5,
           anchor="end")]

    cw, ch, gap = 352, 236, 26
    for i, (cat, items, color) in enumerate(ABILITIES):
        x = 56 + i * (cw + gap)
        b.append(f'<rect x="{x}" y="76" width="{cw}" height="{ch}" rx="6" fill="url(#card)" '
                 f'stroke="{LINE2}" stroke-width="1"/>')
        b.append(f'<rect x="{x}" y="76" width="{cw}" height="2" fill="{color}" opacity="0.65"/>')
        b.append(T(x + 24, 112, cat, 12, color, 4, "600"))
        b.append(f'<rect x="{x + 24}" y="124" width="{cw - 48}" height="1" fill="{LINE}"/>')
        for j, it in enumerate(items):
            y = 158 + j * 30
            b.append(f'<path d="M{x + 24} {y - 9} l4.5 9 l-4.5 9 l-4.5 -9 Z" fill="{color}" '
                     f'opacity="0.55"/>')
            b.append(T(x + 42, y, it, 15, INK, 0.8))

    return panel(w, h, "".join(b))


# -- 4. quest cards -----------------------------------------------------------
def quest_card(q, idx):
    w, h = 1200, 200
    accent = GOLD if q["rank"] == "S" else BLUE
    cleared = q["status"] == "CLEARED"
    status_color = GREEN if cleared else accent
    b = [section(56, f"QUEST {idx:02d}", DIM, 600)]

    b.append(f'<rect x="56" y="70" width="{w - 112}" height="112" rx="6" fill="url(#card)" '
             f'stroke="{LINE2}" stroke-width="1"/>')
    b.append(f'<rect x="56" y="70" width="3" height="112" fill="{accent}" opacity="0.85"/>')

    b.append(hexagon(98, 114, 22, "#0A1728", accent, 1.2, 0.95))
    b.append(T(98, 123, q["rank"], 19, accent, 0, "700", anchor="middle", family=SANS))

    # row 1: name + status
    b.append(T(140, 104, q["name"], 22, INK, 1.2, "600", family=SANS))
    pill_w = 132
    b.append(chip(w - 112 - 24 - pill_w, 84, pill_w, 26, q["status"], status_color, 10.5, 2))

    # row 2: kind (left) and stack (right)
    b.append(T(140, 127, q["kind"], 11, MUTED, 3.5))
    b.append(T(w - 136, 127, q["tech"], 11, VIOLET, 1, anchor="end", opacity=0.9))

    # row 3: description, wrapped
    for i, line in enumerate(wrap(q["desc"], 108)[:2]):
        b.append(T(140, 152 + i * 22, line, 13.5, "#CBD5E1", 0.4, family=SANS))

    return panel(w, h, "".join(b), accent=accent, scan=False)


def wrap(s, width):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if len(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# -- 5. current mission -------------------------------------------------------
def mission():
    w, h = 1200, 330
    b = [section(56, "CURRENT OBJECTIVE", VIOLET, 600)]

    b.append(f'<ellipse cx="600" cy="150" rx="420" ry="120" fill="url(#aura)" opacity="0.5"/>')
    b.append(T(600, 138, "\u201cTransform ideas into working software.\u201d", 34, INK, 1,
               "600", anchor="middle", family=SANS))
    b.append(f'<rect x="440" y="158" width="320" height="1" fill="url(#rule)" opacity="0.8"/>')

    goals = [("01", "SHARPEN AI & PYTHON", "Go deeper on models, vision and agents."),
             ("02", "SHIP PRACTICAL SOFTWARE", "Finished beats impressive on paper."),
             ("03", "LEARN IN PUBLIC", "Repos, tests and write-ups, not promises.")]
    cw, gap = 344, 26
    for i, (num, title, note) in enumerate(goals):
        x = 56 + i * (cw + gap)
        b.append(f'<rect x="{x}" y="192" width="{cw}" height="98" rx="6" fill="url(#card)" '
                 f'stroke="{LINE2}" stroke-width="1"/>')
        b.append(T(x + 22, 224, num, 11, VIOLET, 3, "600"))
        b.append(T(x + 22, 250, title, 14.5, INK, 2, "600"))
        b.append(T(x + 22, 272, note, 11.5, MUTED, 0.6, family=SANS))

    return panel(w, h, "".join(b), accent=VIOLET)


# -- 6. system log + rewards --------------------------------------------------
def log_panel():
    w, h = 1200, 424
    b = [section(56, "SYSTEM LOG", CYAN, 600)]

    # left: activity
    b.append(f'<rect x="56" y="76" width="576" height="300" rx="6" fill="url(#card)" '
             f'stroke="{LINE2}" stroke-width="1"/>')
    b.append(T(80, 108, "RECENT PUSHES", 11, DIM, 4))
    for i, (date, repo, lang) in enumerate(LOG):
        y = 144 + i * 44
        b.append(T(80, y, date, 12, DIM, 1.5))
        b.append(T(196, y, repo, 14, INK, 0.8, "500"))
        b.append(T(608, y, lang, 11.5, BLUE, 2, anchor="end"))
        b.append(f'<rect x="80" y="{y + 12}" width="528" height="1" fill="{LINE}" opacity="0.7"/>')

    # right: rewards
    b.append(f'<rect x="656" y="76" width="488" height="300" rx="6" fill="url(#card)" '
             f'stroke="{LINE2}" stroke-width="1"/>')
    b.append(T(680, 108, "REWARDS UNLOCKED", 11, DIM, 4))
    for i, (title, note) in enumerate(REWARDS):
        y = 146 + i * 76
        b.append(hexagon(700, y - 4, 13, "#0A1728", GOLD, 1, 0.85))
        b.append(T(700, y + 1, DIAMOND, 9, GOLD, 0, "700", anchor="middle"))
        b.append(T(724, y, title, 14, GOLD, 2, "600"))
        for j, line in enumerate(wrap(note, 44)[:2]):
            b.append(T(724, y + 21 + j * 19, line, 11.5, MUTED, 0.5, family=SANS))

    b.append(T(56, h - 16, "LOG PULLED FROM THE GITHUB API " + DOT +
               " REWARDS ARE SHIPPED WORK, NOT CLAIMED CERTIFICATES", 10, DIM, 2))

    return panel(w, h, "".join(b), accent=CYAN)


# -- 7. footer ----------------------------------------------------------------
def footer():
    w, h = 1200, 300
    b = []
    b.append(f'<ellipse cx="600" cy="132" rx="380" ry="110" fill="url(#aura)" opacity="0.55"/>')
    b.append(T(600, 116, "THE JOURNEY DOESN'T END HERE.", 36, INK, 2, "600",
               anchor="middle", family=SANS))
    b.append(T(600, 158, "Keep building. Keep learning. Keep leveling up.", 17, MUTED, 1,
               anchor="middle", family=SANS))
    b.append(f'<rect x="450" y="186" width="300" height="1" fill="url(#rule)" opacity="0.8"/>')
    b.append(T(600, 222, f"{DIAMOND} PLAYER: MAHESH", 12, CYAN, 5, "600", anchor="middle"))
    b.append(T(600, 246, "SYSTEM STATUS: ALWAYS EVOLVING", 11.5, VIOLET, 4, anchor="middle"))
    return panel(w, h, "".join(b), accent=VIOLET)


if __name__ == "__main__":
    files = {
        "hero.svg": hero(),
        "player.svg": player(),
        "abilities.svg": abilities(),
        "mission.svg": mission(),
        "log.svg": log_panel(),
        "footer.svg": footer(),
    }
    for i, q in enumerate(QUESTS, 1):
        slug = q["name"].lower().replace(" ", "-")
        files[f"quest-{i}-{slug}.svg"] = quest_card(q, i)

    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name:34} {len(svg) / 1024:5.1f} KB")

    # drop assets from the previous design
    keep = set(files)
    for old in OUT.glob("*.svg"):
        if old.name not in keep:
            old.unlink()
            print(f"removed stale {old.name}")
