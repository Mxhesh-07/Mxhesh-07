"""
Solo Leveling style profile art - v3, manga poster language.

v1 and v2 were dashboards: panels, labels, bars. This version is drawn like an
anime / manga chapter page instead - a hooded silhouette, halftone screentone,
focus lines, katakana, chapter stamps and a "to be continued" spread.

Every number is still real (GitHub API, 2026-10-26, and the repos' own
READMEs). No skill percentages, no invented awards, no fake stars.

Run: python build.py
"""

import math
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

# -- palette ------------------------------------------------------------------
BG = "#04060D"
BG2 = "#0A1428"
INK = "#F4F7FB"
MUTED = "#93A4BF"
DIM = "#5C6C87"
BLUE = "#3B82F6"
SKY = "#67E8F9"
CYAN = "#7DD3FC"
VIOLET = "#8B5CF6"
DEEP = "#1E3A8A"
GOLD = "#FBBF24"
GREEN = "#34D399"
LINE = "#16233C"
LINE2 = "#22314F"

SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
HEAVY = ("'Segoe UI Black','Segoe UI','Arial Black','Helvetica Neue',"
         "Helvetica,Arial,sans-serif")
JP = ("'Yu Gothic','Yu Gothic UI',Meiryo,'Hiragino Kaku Gothic ProN',"
      "'Hiragino Sans','Noto Sans JP','Noto Sans CJK JP',sans-serif")

DOT = "\u00b7"
DIAMOND = "\u25c6"
ARROW = "\u2192"

# -- verified data ------------------------------------------------------------
PLAYER = dict(
    handle="Mxhesh-07",
    name="MAHESH",
    role="STUDENT DEVELOPER",
    klass="DEVELOPER",
    rank="E \u2192 S",
    spec="AI " + DOT + " PYTHON " + DOT + " WEB",
    quest="BUILD USEFUL SOFTWARE",
    level=16,
    exp_now=3,
    exp_max=8,
    repos=6,
    commits=123,
    languages=11,
    tests=422,
)

# rank = difficulty of the build, not a mark I was given
QUESTS = [
    dict(rank="S", name="Mark-42", kind="DESKTOP AI ASSISTANT",
         jp="\u5f71\u306e\u4ed5\u4e8b",
         desc="Always-on voice agent that drives a Windows desktop: Gemini Live "
              "audio, planner and executor tool loop, screen OCR, browser control.",
         tech="Python / Gemini Live / Playwright / OpenGL",
         status="ACTIVE", url="https://github.com/Mxhesh-07/Mark-42"),
    dict(rank="S", name="KAVACH", kind="BORDER VIDEO ANALYTICS",
         jp="\u56fd\u5883\u306e\u773c",
         desc="Smart India Hackathon 2026, problem statement 26187. Sub-3ms "
              "inference over CCTV, thermal and drone feeds, sealed event logs.",
         tech="C++20 / CUDA / TensorRT / FastAPI",
         status="ACTIVE", url="https://github.com/Mxhesh-07/kavach"),
    dict(rank="A", name="iTantraMessage", kind="OFFLINE MESSENGER",
         jp="\u7e4b\u304c\u308b\u58f0",
         desc="Peer-to-peer messaging over raw Bluetooth. No server, no account, "
              "no INTERNET permission in the release build. 422 tests passing.",
         tech="Kotlin / Android / RFCOMM / Whisper",
         status="ONE BOSS LEFT", url="https://github.com/Mxhesh-07/iTantraMessage"),
    dict(rank="A", name="nemotron-data-forge", kind="DATASET PIPELINE",
         jp="\u30c7\u30fc\u30bf\u306e\u7089",
         desc="Turns a topic into a graded, de-duplicated, fine-tuning-ready "
              "dataset. Nebius x NVIDIA hackathon build.",
         tech="Python / Streamlit / Tavily",
         status="CLEARED", url="https://github.com/Mxhesh-07/nemotron-data-forge"),
]

ABILITIES = [
    ("\u57fa\u672c", "BASE", "CORE",
     ["Python", "JavaScript", "HTML", "CSS"], BLUE),
    ("\u80fd\u529b", "POWER", "AI & VISION",
     ["AI API integration", "Computer vision", "Voice assistants", "Automation"],
     SKY),
    ("\u9053\u5177", "TOOLS", "TOOLING",
     ["Git", "GitHub", "VS Code", "FastAPI", "OpenCV", "Docker"], VIOLET),
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
    ("422 TESTS", "iTantraMessage unit suite, zero failures"),
    ("OFFLINE GATE", "Release build ships without INTERNET permission"),
]

GOALS = [
    ("01", "SHARPEN AI & PYTHON", "Go deeper on models, vision and agents."),
    ("02", "SHIP PRACTICAL SOFTWARE", "Finished beats impressive on paper."),
    ("03", "LEARN IN PUBLIC", "Repos, tests and write-ups, not promises."),
]


# -- primitives ---------------------------------------------------------------
_id = 0


def uid(prefix="c"):
    global _id
    _id += 1
    return f"{prefix}{_id}"


class Rand:
    """Tiny deterministic LCG so the artwork is identical on every build."""

    def __init__(self, seed=7):
        self.s = seed

    def next(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return self.s / 2147483648

    def rng(self, a, b):
        return a + (b - a) * self.next()


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def T(x, y, s, size=16, fill=INK, ls=1.2, weight="400", anchor="start",
      opacity=1.0, family=SANS):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}" opacity="{opacity}">{esc(s)}</text>')


def hexagon(cx, cy, r, fill="none", stroke=BLUE, sw=1.2, opacity=1.0, rot=0):
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 90 + rot)
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{opacity}"/>')


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


def deco(svg):
    """Mark decorative text so the geometry checker ignores it."""
    return f'<g data-deco="1">{svg}</g>'


def defs():
    return f"""
<defs>
  <linearGradient id="gPage" x1="0" y1="0" x2="0.6" y2="1">
    <stop offset="0" stop-color="{BG}"/>
    <stop offset="0.45" stop-color="#070C16"/>
    <stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <linearGradient id="gPanel" x1="0" y1="0" x2="0.2" y2="1">
    <stop offset="0" stop-color="#0A101E"/>
    <stop offset="1" stop-color="#05080F"/>
  </linearGradient>
  <radialGradient id="gAura" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.34"/>
    <stop offset="0.5" stop-color="{VIOLET}" stop-opacity="0.14"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gMoon" cx="0.42" cy="0.36" r="0.62">
    <stop offset="0" stop-color="#DBEAFE" stop-opacity="0.95"/>
    <stop offset="0.28" stop-color="#93C5FD" stop-opacity="0.55"/>
    <stop offset="0.62" stop-color="{BLUE}" stop-opacity="0.30"/>
    <stop offset="1" stop-color="{DEEP}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="gName" x1="0" y1="0" x2="1" y2="0.6">
    <stop offset="0" stop-color="#FFFFFF"/>
    <stop offset="0.7" stop-color="#E0F2FE"/>
    <stop offset="1" stop-color="#7DD3FC"/>
  </linearGradient>
  <linearGradient id="gRimL" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#E0F2FE" stop-opacity="0.95"/>
    <stop offset="0.35" stop-color="{SKY}" stop-opacity="0.7"/>
    <stop offset="1" stop-color="{SKY}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gRimR" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.85"/>
    <stop offset="0.6" stop-color="{VIOLET}" stop-opacity="0.32"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gBlade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.35" stop-color="#E0F2FE" stop-opacity="0.9"/>
    <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="1"/>
    <stop offset="0.8" stop-color="{SKY}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{SKY}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gFadeUp" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="{BG}" stop-opacity="1"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="htA" width="9" height="9" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.9" fill="{CYAN}" opacity="0.20"/>
  </pattern>
  <pattern id="htB" width="6" height="6" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.1" fill="{VIOLET}" opacity="0.18"/>
  </pattern>
  <filter id="fGlow" x="-70%" y="-70%" width="240%" height="240%">
    <feGaussianBlur stdDeviation="4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="fBig" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="18" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="fSoft" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="26"/>
  </filter>
</defs>
"""


def doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n{defs()}\n{body}\n</svg>\n')


def page(w, h, accent=BLUE, halftone="bottom"):
    out = [f'<rect width="{w}" height="{h}" fill="url(#gPage)"/>']
    out.append(f'<ellipse cx="{w * 0.5}" cy="{-h * 0.15}" rx="{w * 0.75}" '
               f'ry="{h * 0.7}" fill="url(#gAura)" opacity="0.45"/>')
    if halftone == "bottom":
        out.append(f'<rect x="0" y="{h * 0.52}" width="{w}" height="{h * 0.48}" '
                   f'fill="url(#htA)" opacity="0.55"/>')
        out.append(f'<rect x="0" y="{h * 0.52}" width="{w}" height="{h * 0.48}" '
                   f'fill="url(#gFadeUp)" opacity="0.85"/>')
    out.append(f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" '
               f'fill="none" stroke="{LINE}" stroke-width="1"/>')
    out.append(f'<rect x="0" y="0" width="64" height="3" fill="{accent}" '
               f'opacity="0.9"/>')
    out.append(f'<rect x="{w - 4}" y="{h * 0.5}" width="3" height="{h * 0.18}" '
               f'fill="{accent}" opacity="0.35"/>')
    return "".join(out)


def mpanel(x, y, w, h, cut=30, accent=None, texture="corner"):
    """Angular manga panel: cut corners, hairline, screentone in one corner."""
    cid = uid("clip")
    pts = (f"{x + cut},{y} {x + w - cut},{y} {x + w},{y + cut} "
           f"{x + w},{y + h - cut} {x + w - cut},{y + h} {x + cut},{y + h} "
           f"{x},{y + h - cut} {x},{y + cut}")
    out = [f'<clipPath id="{cid}"><polygon points="{pts}"/></clipPath>',
           f'<polygon points="{pts}" fill="url(#gPanel)" stroke="{LINE2}" '
           f'stroke-width="1"/>']
    if texture == "corner":
        out.append(f'<g clip-path="url(#{cid})"><rect x="{x + w * 0.52}" y="{y}" '
                   f'width="{w * 0.48}" height="{h}" fill="url(#htA)" '
                   f'opacity="0.30"/></g>')
    elif texture == "bottom":
        out.append(f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y + h * 0.55}" '
                   f'width="{w}" height="{h * 0.45}" fill="url(#htA)" '
                   f'opacity="0.34"/></g>')
    if accent:
        out.append(f'<line x1="{x + cut}" y1="{y + 1.5}" x2="{x + w * 0.42}" '
                   f'y2="{y + 1.5}" stroke="{accent}" stroke-width="2"/>')
        out.append(f'<line x1="{x + w * 0.62}" y1="{y + 1.5}" x2="{x + w - cut}" '
                   f'y2="{y + 1.5}" stroke="{accent}" stroke-width="1" '
                   f'opacity="0.35"/>')
    return "".join(out)


def stamp(cx, cy, r, label, color, rot=-9, size=None):
    """Dashed rank stamp, slightly rotated, like a chapter badge."""
    size = size or r * 0.9
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#05080F" '
            f'stroke="{color}" stroke-width="1" opacity="0.9"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 5}" fill="none" stroke="{color}" '
            f'stroke-width="1" stroke-dasharray="3 4" opacity="0.6"/>'
            + T(cx, cy + size * 0.35, label, size, color, 0, "900",
                anchor="middle", family=HEAVY) + "</g>")


def speedlines(cx, cy, r0, r1, n=68, color=CYAN, seed=11, op=(0.05, 0.2)):
    rnd = Rand(seed)
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.rng(-0.008, 0.008)
        inner = r0 + rnd.rng(10, 150)
        outer = r1 + rnd.rng(-90, 180)
        out.append(
            f'<line x1="{cx + inner * math.cos(a):.1f}" '
            f'y1="{cy + inner * math.sin(a):.1f}" '
            f'x2="{cx + outer * math.cos(a):.1f}" '
            f'y2="{cy + outer * math.sin(a):.1f}" stroke="{color}" '
            f'stroke-width="{rnd.rng(0.6, 2.4):.1f}" '
            f'opacity="{rnd.rng(*op):.2f}"/>')
    return "".join(out)


def level_meta(w, h, jp, label, color=SKY):
    return (T(24, 62, jp, 24, color, 8, "700", family=JP)
            + T(24, 88, label, 12, MUTED, 5.5, "600"))


# -- 1. hero: the awakening ------------------------------------------------
def figure():
    """Hooded silhouette with glowing eyes, rim light and a torn cloak."""
    cloak = ("M 0,-205 C -62,-205 -112,-158 -124,-102 C -136,-46 -124,8 -108,40 "
             "C -156,58 -204,92 -222,138 C -250,204 -260,270 -262,330 "
             "L 262,330 C 260,270 250,204 222,138 C 204,92 156,58 108,40 "
             "C 124,8 136,-46 124,-102 C 112,-158 62,-205 0,-205 Z")
    tatters = ("M -262,330 L -228,330 L -238,372 L -204,332 L -176,330 "
               "L -150,366 L -120,332 L -60,330 L -34,360 L -6,332 L 44,330 "
               "L 70,362 L 98,332 L 150,330 L 176,364 L 200,332 L 262,330 "
               "L 262,338 L -262,338 Z")
    p = []
    p.append(f'<path d="{cloak}" fill="url(#gPanel)" stroke="{LINE2}" '
             f'stroke-width="1"/>')
    p.append(f'<path d="{tatters}" fill="#060A14" stroke="{LINE2}" '
             f'stroke-width="1"/>')
    p.append(f'<ellipse cx="0" cy="-86" rx="66" ry="82" fill="#02040A"/>')
    p.append(f'<ellipse cx="0" cy="-86" rx="66" ry="82" fill="none" '
             f'stroke="{DEEP}" stroke-width="1.4" opacity="0.7"/>')
    p.append(f'<path d="M -104,44 L -46,150 L 0,96 L 46,150 L 104,44" '
             f'fill="none" stroke="{LINE2}" stroke-width="1.4" opacity="0.9"/>')
    p.append(f'<path d="M -196,196 L -176,236 L -186,258 M 178,180 L 196,224 '
             f'L 184,250" fill="none" stroke="{SKY}" stroke-width="1.2" '
             f'opacity="0.30"/>')
    p.append(f'<g opacity="0.85">{hexagon(0, 190, 17, "none", SKY, 1.2, 0.7)}'
             f'{hexagon(0, 190, 8, "#0A1728", SKY, 1, 0.9, rot=30)}</g>')
    p.append(f'<path d="M -30,-203 C -84,-196 -114,-158 -124,-102 C -136,-46 '
             f'-124,8 -108,40 C -156,58 -204,92 -222,138 C -250,204 -260,270 '
             f'-262,330" fill="none" stroke="url(#gRimL)" stroke-width="2.6"/>')
    p.append(f'<path d="M 30,-203 C 84,-196 114,-158 124,-102 C 136,-46 124,8 '
             f'108,40 C 156,58 204,92 222,138 C 250,204 260,270 262,330" '
             f'fill="none" stroke="url(#gRimR)" stroke-width="2"/>')
    p.append(f'<g filter="url(#fGlow)">'
             f'<path d="M -46,-96 L -14,-106 L -11,-88 L -42,-82 Z" fill="{SKY}">'
             f'<animate attributeName="opacity" values="1;0.45;1" dur="3.6s" '
             f'repeatCount="indefinite"/></path>'
             f'<path d="M 46,-96 L 14,-106 L 11,-88 L 42,-82 Z" fill="{SKY}">'
             f'<animate attributeName="opacity" values="1;0.45;1" dur="3.6s" '
             f'repeatCount="indefinite"/></path></g>')
    p.append(f'<path d="M -40,-92 L -18,-99 L -17,-91 L -38,-86 Z" fill="#FFFFFF"/>'
             f'<path d="M 40,-92 L 18,-99 L 17,-91 L 38,-86 Z" fill="#FFFFFF"/>')
    return "".join(p)


def hero():
    w, h = 1200, 780
    cx, cy = 828, 400
    b = [page(w, h, SKY)]

    b.append(f'<circle cx="{cx}" cy="{cy - 72}" r="252" fill="url(#gMoon)" '
             f'opacity="0.55"/>')
    b.append(f'<circle cx="{cx}" cy="{cy - 72}" r="252" fill="none" '
             f'stroke="{CYAN}" stroke-width="1" opacity="0.28"/>')
    b.append(f'<circle cx="{cx}" cy="{cy - 72}" r="264" fill="none" '
             f'stroke="{VIOLET}" stroke-width="1" stroke-dasharray="2 10" '
             f'opacity="0.35"/>')

    b.append(deco(speedlines(cx, cy - 40, 250, 760, 76, CYAN, 23)))

    b.append(f'<g transform="rotate(-34 600 400)">'
             f'<rect x="-260" y="392" width="1520" height="16" fill="url(#gBlade)" '
             f'filter="url(#fBig)" opacity="0.85"/>'
             f'<rect x="-260" y="397" width="1520" height="4" fill="#E0F2FE" '
             f'opacity="0.55"/></g>')

    b.append(f'<ellipse cx="{cx}" cy="742" rx="300" ry="26" fill="{BLUE}" '
             f'opacity="0.14" filter="url(#fSoft)"/>')

    b.append(f'<g transform="translate({cx} {cy})">{figure()}</g>')

    rnd = Rand(41)
    embers = []
    for i in range(22):
        ex, ey = rnd.rng(500, 1160), rnd.rng(120, 740)
        r = rnd.rng(1.2, 3.2)
        o = rnd.rng(0.25, 0.7)
        col = CYAN if i % 3 else VIOLET
        embers.append(f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{r:.1f}" fill="{col}" '
                      f'opacity="{o:.2f}"><animate attributeName="opacity" '
                      f'values="{o:.2f};0.05;{o:.2f}" dur="{3 + i % 5}s" '
                      f'repeatCount="indefinite"/></circle>')
    b.append(deco("".join(embers)))

    # copy block
    b.append(T(88, 120, "CHAPTER 01 " + DOT + " AWAKENING", 12.5, SKY, 5.5, "600"))
    b.append(f'<rect x="88" y="134" width="248" height="2" fill="{SKY}" opacity="0.7"/>')
    b.append(T(88, 214, "\u5f71\u306e\u958b\u767a\u8005", 30, MUTED, 7, "600", family=JP))

    b.append(f'<g transform="translate(92 348) skewX(-7)">'
             + T(0, 0, PLAYER["name"], 106, "url(#gName)", 3, "900", family=HEAVY)
             + "</g>")
    b.append(f'<g transform="translate(92 414) skewX(-7)">'
             + T(0, 0, "SHADOW DEVELOPER", 25, SKY, 11, "700")
             + "</g>")
    b.append(f'<rect x="88" y="436" width="268" height="1" fill="{LINE2}"/>')

    b.append(T(88, 478, "Every developer starts at level 1.", 21, INK, 0.5, "400"))
    b.append(T(88, 510, "Python " + DOT + " AI " + DOT + " computer vision " + DOT
               + " offline-first Android", 14.5, MUTED, 0.4))

    b.append(f'<rect x="88" y="544" width="300" height="40" rx="2" fill="#07101F" '
             f'stroke="{SKY}" stroke-width="1" opacity="0.9"/>')
    b.append(f'<circle cx="112" cy="564" r="4.5" fill="{GREEN}" filter="url(#fGlow)">'
             f'<animate attributeName="opacity" values="1;0.12;1" dur="2.2s" '
             f'repeatCount="indefinite"/></circle>')
    b.append(T(130, 569, "SYSTEM INITIALIZED", 12.5, SKY, 3.5, "600"))

    b.append(T(88, 638, "LV", 15, DIM, 4, "600"))
    b.append(T(122, 640, f"{PLAYER['level']:02d}", 34, INK, 1, "900", family=HEAVY))
    b.append(f'<rect x="88" y="656" width="300" height="9" fill="#0B1526" '
             f'stroke="{LINE2}" stroke-width="1"/>')
    b.append(f'<rect x="88" y="656" '
             f'width="{300 * PLAYER["exp_now"] / PLAYER["exp_max"]:.0f}" '
             f'height="9" fill="{SKY}" opacity="0.85"/>')
    b.append(T(400, 666, f"{PLAYER['exp_now']} / {PLAYER['exp_max']} EXP " + DOT
               + " 123 COMMITS", 10.5, DIM, 2))

    b.append(T(88, 738, "PLAYER " + PLAYER["handle"].upper(), 11.5, DIM, 3))
    b.append(T(1112, 738, "STATUS: ONLINE", 11.5, GREEN, 3, anchor="end"))

    b.append(deco(f'<g transform="translate(1150 150) rotate(90)">'
                  + T(0, 0, "\u76ee\u899a\u3081\u3088\u3001\u5f71\u3088", 19, BLUE, 9,
                      "600", family=JP, opacity=0.85) + "</g>"))

    return doc(w, h, "".join(b))


# -- 2. player status: manga grid -----------------------------------------
def player():
    w, h = 1200, 604
    b = [page(w, h, BLUE, halftone=None)]

    b.append(mpanel(24, 24, 696, 304, 34, BLUE, "corner"))
    b.append(T(56, 66, "\u72b6\u614b", 15, SKY, 6, "600", family=JP))
    b.append(T(56, 92, "PLAYER STATUS", 12.5, MUTED, 5.5, "600"))
    rows = [("PLAYER", PLAYER["handle"]), ("CLASS", PLAYER["klass"]),
            ("RANK", PLAYER["rank"]), ("SPECIALIZATION", PLAYER["spec"]),
            ("CURRENT QUEST", PLAYER["quest"])]
    for i, (k, v) in enumerate(rows):
        y = 146 + i * 38
        b.append(T(56, y, k, 10.5, DIM, 3.6))
        b.append(T(268, y, v, 16.5, INK, 1.2, "600"))
        b.append(f'<rect x="56" y="{y + 12}" width="632" height="1" fill="{LINE}" '
                 f'opacity="0.8"/>')

    b.append(mpanel(736, 24, 440, 304, 34, GOLD, "corner"))
    b.append(T(768, 66, "\u7b49\u7d1a", 15, GOLD, 6, "600", family=JP))
    b.append(T(768, 92, "LEVEL", 12.5, MUTED, 5.5, "600"))
    b.append(T(768, 216, f"{PLAYER['level']:02d}", 108, INK, 0, "900", family=HEAVY))
    b.append(T(1144, 108, "E " + ARROW + " S", 22, GOLD, 4, "700", anchor="end"))
    b.append(T(1144, 132, "PROGRESSION", 9.5, DIM, 3, anchor="end"))
    b.append(f'<rect x="768" y="248" width="376" height="10" fill="#0B1526" '
             f'stroke="{LINE2}" stroke-width="1"/>')
    b.append(f'<rect x="768" y="248" '
             f'width="{376 * PLAYER["exp_now"] / PLAYER["exp_max"]:.0f}" '
             f'height="10" fill="{GOLD}" opacity="0.85"/>')
    b.append(T(768, 292, f"{PLAYER['exp_now']} / {PLAYER['exp_max']} EXP TO LV "
               f"{PLAYER['level'] + 1}", 11, DIM, 2.5))

    tiles = [(f"{PLAYER['commits']}", "COMMITS", "\u63a8\u9032", CYAN),
             (f"{PLAYER['repos']:02d}", "PUBLIC REPOS", "\u4f5c\u54c1", SKY),
             (f"{PLAYER['languages']:02d}", "LANGUAGES", "\u8a9e\u5f59", VIOLET),
             (f"{PLAYER['tests']}", "PASSING TESTS", "\u8a66\u9a13", GREEN)]
    tw = (1200 - 48 - 3 * 14) / 4
    for i, (val, label, jp, col) in enumerate(tiles):
        x = 24 + i * (tw + 14)
        b.append(mpanel(x, 348, tw, 232, 28, col, "bottom"))
        b.append(T(x + 22, 386, jp, 13, col, 5, "600", family=JP))
        b.append(T(x + 22, 408, label, 10, MUTED, 3.4, "600"))
        b.append(T(x + 22, 500, val, 62, INK, 0, "900", family=HEAVY))
        b.append(f'<rect x="{x + 22}" y="524" width="{tw - 44}" height="1" '
                 f'fill="{col}" opacity="0.5"/>')

    b.append(T(24, 592, "RANK IS PROGRESSION, NOT A CERTIFICATION " + DOT
               + " COUNTS READ FROM THE GITHUB API", 9.5, DIM, 2))

    return doc(w, h, "".join(b))


# -- 3. abilities ----------------------------------------------------------
def abilities():
    w, h = 1200, 520
    b = [page(w, h, SKY, halftone=None)]
    b.append(level_meta(w, h, "\u80fd\u529b", "HUNTER ABILITIES", SKY))
    b.append(T(1160, 74, "NO PERCENTAGES", 10, DIM, 2.4, anchor="end"))

    cw = (1200 - 48 - 2 * 16) / 3
    for i, (jp, label, sub, items, col) in enumerate(ABILITIES):
        x = 24 + i * (cw + 16)
        b.append(mpanel(x, 112, cw, 372, 32, col, "bottom"))
        b.append(deco(T(x + cw - 26, 452, jp, 128, col, 0, "700", anchor="end",
                        family=JP, opacity=0.06)))
        b.append(T(x + 26, 158, jp, 15, col, 6, "600", family=JP))
        b.append(T(x + 26, 182, label, 11, MUTED, 5, "600"))
        b.append(T(x + 26, 202, sub, 10, DIM, 2.6))
        b.append(f'<rect x="{x + 26}" y="216" width="{cw - 52}" height="1" '
                 f'fill="{LINE2}"/>')
        for j, it in enumerate(items):
            y = 254 + j * 34
            b.append(f'<path d="M{x + 26} {y - 5} l7 5 l-7 5 l-7 -5 Z" fill="{col}" '
                     f'opacity="0.55"/>')
            b.append(T(x + 46, y, it, 16, INK, 0.6, "500"))

    b.append(T(24, 508, "\u6697\u304f\u3066\u3082\u3001\u9032\u3080", 11, DIM, 4,
               family=JP))
    return doc(w, h, "".join(b))


# -- 4. quest panels -------------------------------------------------------
def quest_card(q, idx):
    w, h = 1200, 268
    accent = GOLD if q["rank"] == "S" else SKY
    status_col = GREEN if q["status"] == "CLEARED" else accent
    b = [page(w, h, accent, halftone=None)]

    b.append(T(24, 34, f"\u4f9d\u983c {idx:02d}", 12.5, accent, 5, "600", family=JP))
    b.append(T(150, 34, q["jp"], 13, DIM, 5, family=JP))

    b.append(mpanel(24, 48, 1152, 190, 40, accent, "corner"))

    b.append(stamp(104, 143, 39, q["rank"], accent, rot=-8, size=34))
    b.append(T(104, 198, "RANK", 9, DIM, 2.6, anchor="middle"))

    b.append(T(166, 126, q["name"], 31, INK, 1.2, "900", family=HEAVY))
    b.append(T(166, 154, q["kind"], 11.5, MUTED, 3.6, "600"))
    b.append(T(166, 182, q["jp"], 12.5, accent, 4, "500", family=JP, opacity=0.9))

    # description, two lines max, in its own column clear of long names
    for i, line in enumerate(wrap(q["desc"], 82)[:2]):
        b.append(T(548, 130 + i * 24, line, 14, "#CFDCEA", 0.3))

    b.append(T(1144, 200, q["tech"], 11, VIOLET, 0.8, anchor="end", opacity=0.95))

    sw = 158
    b.append(f'<g transform="rotate(-2 1085 79)">'
             f'<rect x="{1144 - sw}" y="66" width="{sw}" height="26" fill="#05080F" '
             f'stroke="{status_col}" stroke-width="1" opacity="0.9"/>'
             + T(1144 - sw / 2, 84, q["status"], 10.5, status_col, 2.4, "700",
                 anchor="middle") + "</g>")

    return doc(w, h, "".join(b))


# -- 5. mission ------------------------------------------------------------
def mission():
    w, h = 1200, 440
    b = [page(w, h, VIOLET, halftone=None)]
    b.append(level_meta(w, h, "\u6b21\u306e\u4efb\u52d9", "CURRENT OBJECTIVE", VIOLET))
    b.append(T(1160, 74, "WHAT I AM DOING NOW", 10, DIM, 2.4, anchor="end"))

    b.append(f'<ellipse cx="600" cy="180" rx="430" ry="120" fill="url(#gAura)" '
             f'opacity="0.5"/>')
    b.append(f'<g transform="translate(60 182) skewX(-5)">'
             + T(0, 0, "\u201cTransform ideas into working software.\u201d", 36, INK,
                 0.6, "700", family=SANS) + "</g>")
    b.append(T(62, 216, "\u601d\u8003\u3092\u3001\u52d5\u304f\u5f62\u3078\u3002", 15,
               VIOLET, 5, "600", family=JP))

    for i, (num, title, note) in enumerate(GOALS):
        x = 60 + i * 364
        b.append(mpanel(x, 250, 340, 140, 26, VIOLET, "corner"))
        b.append(T(x + 24, 288, num, 12, VIOLET, 3, "800", family=HEAVY))
        b.append(T(x + 24, 316, title, 14.5, INK, 2, "700"))
        for j, line in enumerate(wrap(note, 34)[:2]):
            b.append(T(x + 24, 340 + j * 18, line, 11.5, MUTED, 0.3))

    b.append(T(24, 422, "OBJECTIVES ARE SELF-SET " + DOT + " NO DEADLINES PROMISED",
               9.5, DIM, 2))
    return doc(w, h, "".join(b))


# -- 6. log + rewards ------------------------------------------------------
def log_panel():
    w, h = 1200, 604
    b = [page(w, h, CYAN, halftone=None)]
    b.append(level_meta(w, h, "\u8a18\u9332", "SYSTEM LOG", CYAN))
    b.append(T(1160, 74, "FROM THE GITHUB API", 10, DIM, 2.4, anchor="end"))

    b.append(mpanel(24, 116, 700, 428, 32, CYAN, "bottom"))
    b.append(T(56, 156, "\u6700\u8fd1\u306e\u63a8\u9032", 12, DIM, 4, family=JP))
    b.append(T(692, 156, "RECENT PUSHES", 10, DIM, 3, anchor="end"))
    for i, (date, repo, lang) in enumerate(LOG):
        y = 200 + i * 62
        b.append(T(56, y, date, 12, DIM, 1.4))
        b.append(T(184, y, repo, 17, INK, 0.6, "600"))
        b.append(T(692, y, lang, 11.5, CYAN, 1.8, anchor="end"))
        b.append(f'<rect x="56" y="{y + 14}" width="636" height="1" fill="{LINE}" '
                 f'opacity="0.8"/>')

    b.append(mpanel(748, 116, 428, 428, 32, GOLD, "bottom"))
    b.append(T(780, 156, "\u8912\u8cde", 12, DIM, 4, family=JP))
    b.append(T(1144, 156, "REWARDS", 10, DIM, 3, anchor="end"))
    for i, (title, note) in enumerate(REWARDS):
        y = 196 + i * 112
        b.append(f'<g transform="rotate(-1.4 960 {y + 30})">'
                 f'<rect x="780" y="{y}" width="364" height="92" fill="#070C17" '
                 f'stroke="{GOLD}" stroke-width="1" opacity="0.55" '
                 f'stroke-dasharray="5 4"/></g>')
        b.append(T(800, y + 32, title, 16, GOLD, 2.4, "800", family=HEAVY))
        for j, line in enumerate(wrap(note, 42)[:2]):
            b.append(T(800, y + 56 + j * 18, line, 11.5, MUTED, 0.4))

    b.append(T(24, 590, "REWARDS ARE SHIPPED WORK " + DOT
               + " RANKS SHOW DIFFICULTY, NOT A CERTIFICATE", 9.5, DIM, 2))
    return doc(w, h, "".join(b))


# -- 7. finale -------------------------------------------------------------
def footer():
    w, h = 1200, 452
    b = [page(w, h, VIOLET, halftone="bottom")]

    b.append(deco(speedlines(600, 250, 120, 820, 54, VIOLET, 77, (0.04, 0.14))))
    b.append(f'<ellipse cx="600" cy="210" rx="430" ry="150" fill="url(#gAura)" '
             f'opacity="0.6"/>')

    b.append(f'<g transform="translate(560 218) skewX(-6)">'
             + T(0, 0, "TO BE CONTINUED", 62, "url(#gName)", 2, "900",
                 anchor="middle", family=HEAVY) + "</g>")

    b.append(f'<g transform="rotate(-2 1000 200)">'
             f'<path d="M 950,186 L 1010,186 L 1010,178 L 1042,196 L 1010,214 '
             f'L 1010,206 L 950,206 Z" fill="{SKY}" opacity="0.9"/></g>')

    b.append(T(600, 272, "\u3064\u3065\u304f", 30, MUTED, 10, "600",
               anchor="middle", family=JP))
    b.append(f'<rect x="420" y="296" width="360" height="1" fill="{LINE2}"/>')

    b.append(T(600, 344, "Keep building. Keep learning. Keep leveling up.", 20,
               INK, 0.6, "500", anchor="middle"))
    b.append(T(600, 384, "PLAYER: MAHESH " + DOT + " SYSTEM STATUS: ALWAYS EVOLVING",
               11, SKY, 3.4, "600", anchor="middle"))
    b.append(T(600, 428, "HAND-DRAWN SVG " + DOT + " NO TRACKING " + DOT
               + " REAL NUMBERS", 9, DIM, 2.6, anchor="middle"))
    return doc(w, h, "".join(b))


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

    keep = set(files)
    for old in OUT.glob("*.svg"):
        if old.name not in keep:
            old.unlink()
            print(f"removed stale {old.name}")
