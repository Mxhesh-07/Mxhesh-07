"""
Bleach themed GitHub profile art - v4.

Black page, paper white ink, Ichigo orange and blood red. Zanpakuto across the
title, hollow hole, reiatsu shockwaves, a hell butterfly, 卍解, and 任務 cards.

Motion is SMIL (animate / animateTransform / animateMotion): GitHub strips
<script> and CSS out of READMEs, but declarative SVG animation still plays
inside <img>. Hover and cursor effects cannot work there - the interactive
layer lives in the README as <details> blocks and linked cards.

Numbers stay real (GitHub API, 2026-10-26, plus the repos' own READMEs).

Run: python build.py
"""

import base64
import math
from pathlib import Path

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

# -- palette ------------------------------------------------------------------
BG = "#060607"
BG2 = "#0C0C0E"
INK = "#F5F3EE"
ORANGE = "#FF6A00"
RED = "#E11D2E"
PALE = "#CFE9FF"
GOLD = "#E8C170"
DIM = "#6B6B72"
LINE = "#232326"
LINE2 = "#313136"

TITLE = ("'Impact','Haettenschweiler','Arial Narrow','Arial Black',"
         "'Helvetica Neue',sans-serif")
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
HEAVY = ("'Segoe UI Black','Segoe UI','Arial Black','Helvetica Neue',"
         "Helvetica,Arial,sans-serif")
JP = ("'Yu Gothic','Yu Gothic UI',Meiryo,'Hiragino Kaku Gothic ProN',"
      "'Hiragino Sans','Noto Sans JP','Noto Sans CJK JP',sans-serif")

DOT = "\u00b7"
ARROW = "\u2192"
BANKAI = "\u5345\u89e3"
SHINIGAMI = "\u6b7b\u795e\u4ee3\u884c"

# -- verified data ------------------------------------------------------------
PLAYER = dict(
    handle="Mxhesh-07",
    name="MAHESH",
    given="Mahesh S",
    role="Student developer",
    zanpakuto="Python",
    spec="AI " + DOT + " COMPUTER VISION " + DOT + " WEB",
    quest="Build useful software",
    seat=16,
    repos=6,
    commits=123,
    languages=11,
    tests=422,
)

QUESTS = [
    dict(rank="S", name="Mark-42", kind="DESKTOP AI ASSISTANT",
         jp="\u5f71\u306e\u4ed5\u4e8b", threat="MENOS CLASS",
         desc="Always-on voice agent that drives a Windows desktop: Gemini Live "
              "audio, planner and executor tool loop, screen OCR, browser control.",
         tech="Python / Gemini Live / Playwright / OpenGL",
         status="ACTIVE", url="https://github.com/Mxhesh-07/Mark-42"),
    dict(rank="S", name="KAVACH", kind="BORDER VIDEO ANALYTICS",
         jp="\u56fd\u5883\u306e\u773c", threat="MENOS CLASS",
         desc="Smart India Hackathon 2026, problem statement 26187. Sub-3ms "
              "inference over CCTV, thermal and drone feeds, sealed event logs.",
         tech="C++20 / CUDA / TensorRT / FastAPI",
         status="ACTIVE", url="https://github.com/Mxhesh-07/kavach"),
    dict(rank="A", name="iTantraMessage", kind="OFFLINE MESSENGER",
         jp="\u7e4b\u304c\u308b\u58f0", threat="ARRANCAR CLASS",
         desc="Peer-to-peer messaging over raw Bluetooth. No server, no account, "
              "no INTERNET permission in the release build. 422 tests passing.",
         tech="Kotlin / Android / RFCOMM / Whisper",
         status="ONE BOSS LEFT", url="https://github.com/Mxhesh-07/iTantraMessage"),
    dict(rank="A", name="nemotron-data-forge", kind="DATASET PIPELINE",
         jp="\u30c7\u30fc\u30bf\u306e\u7089", threat="ARRANCAR CLASS",
         desc="Turns a topic into a graded, de-duplicated, fine-tuning-ready "
              "dataset. Nebius x NVIDIA hackathon build.",
         tech="Python / Streamlit / Tavily",
         status="SEALED", url="https://github.com/Mxhesh-07/nemotron-data-forge"),
]

ABILITIES = [
    ("\u65ac", "CUT", "BASE", "LANGUAGES",
     ["Python", "JavaScript", "HTML", "CSS"], ORANGE),
    ("\u970a", "SPIRIT", "POWER", "AI & VISION",
     ["AI API integration", "Computer vision", "Voice assistants", "Automation"],
     PALE),
    ("\u88c5", "FORGE", "TOOLS", "TOOLING",
     ["Git", "GitHub", "VS Code", "FastAPI", "OpenCV", "Docker"], RED),
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
    """Deterministic LCG so the artwork is identical on every build."""

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


def deco(svg):
    return f'<g data-deco="1">{svg}</g>'


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


def defs():
    return f"""
<defs>
  <linearGradient id="gPage" x1="0" y1="0" x2="0.7" y2="1">
    <stop offset="0" stop-color="{BG}"/>
    <stop offset="0.5" stop-color="#08080A"/>
    <stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <linearGradient id="gPanel" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0" stop-color="#0E0E11"/>
    <stop offset="1" stop-color="#050506"/>
  </linearGradient>
  <radialGradient id="gSun" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#FF7A1A" stop-opacity="1"/>
    <stop offset="0.62" stop-color="{ORANGE}" stop-opacity="0.92"/>
    <stop offset="0.86" stop-color="{RED}" stop-opacity="0.42"/>
    <stop offset="1" stop-color="{RED}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gRei" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{PALE}" stop-opacity="0.75"/>
    <stop offset="0.45" stop-color="{ORANGE}" stop-opacity="0.20"/>
    <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gHollow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#000000" stop-opacity="1"/>
    <stop offset="0.72" stop-color="#000000" stop-opacity="1"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="gName" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/>
    <stop offset="0.62" stop-color="{INK}"/>
    <stop offset="1" stop-color="#C9C2B6"/>
  </linearGradient>
  <linearGradient id="gBlade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.9"/>
    <stop offset="0.62" stop-color="{ORANGE}" stop-opacity="0.9"/>
    <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gSteel" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="#8C8C93"/>
    <stop offset="0.35" stop-color="#E9E9EE"/>
    <stop offset="0.62" stop-color="#FFFFFF"/>
    <stop offset="1" stop-color="#B9B9C2"/>
  </linearGradient>
  <linearGradient id="gSheen" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ORANGE}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{ORANGE}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gMask" x1="0.15" y1="0" x2="0.85" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/>
    <stop offset="0.4" stop-color="#F4F0E7"/>
    <stop offset="0.75" stop-color="#DDD6C8"/>
    <stop offset="1" stop-color="#B4AC9E"/>
  </linearGradient>
  <radialGradient id="gBoneShade" cx="0.32" cy="0.2" r="0.95">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.5"/>
    <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="1" stop-color="#2A2620" stop-opacity="0.5"/>
  </radialGradient>
  <linearGradient id="gBrow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000000" stop-opacity="0"/>
    <stop offset="0.55" stop-color="#000000" stop-opacity="0.32"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gJaw" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000000" stop-opacity="0"/>
    <stop offset="0.7" stop-color="#000000" stop-opacity="0.3"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.1"/>
  </linearGradient>
  <filter id="fBone" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="3"
                  seed="11"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <linearGradient id="gBody" x1="0" y1="0" x2="0.25" y2="1">
    <stop offset="0" stop-color="#23232B"/>
    <stop offset="0.45" stop-color="#1A1A21"/>
    <stop offset="1" stop-color="#121216"/>
  </linearGradient>
  <linearGradient id="gFadeUp" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="{BG}" stop-opacity="1"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="gVig" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0.5" stop-color="#060607" stop-opacity="0"/>
    <stop offset="0.85" stop-color="#060607" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#060607" stop-opacity="0.85"/>
  </radialGradient>
  <filter id="fDuo" x="-5%" y="-5%" width="110%" height="110%">
    <feColorMatrix type="matrix"
                   values="0.33 0.33 0.33 0 0 0.33 0.33 0.33 0 0
                           0.33 0.33 0.33 0 0 0 0 0 1 0"/>
    <feComponentTransfer>
      <feFuncR type="table" tableValues="0.04 1"/>
      <feFuncG type="table" tableValues="0.035 0.94"/>
      <feFuncB type="table" tableValues="0.03 0.86"/>
    </feComponentTransfer>
  </filter>
  <pattern id="htA" width="8" height="8" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.5" fill="{INK}" opacity="0.14"/>
  </pattern>
  <pattern id="htB" width="5" height="5" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="1" fill="{ORANGE}" opacity="0.16"/>
  </pattern>
  <pattern id="hatch" width="9" height="9" patternUnits="userSpaceOnUse"
           patternTransform="rotate(52)">
    <line x1="0" y1="0" x2="0" y2="9" stroke="{INK}" stroke-width="1"
          opacity="0.10"/>
  </pattern>
  <filter id="fGlow" x="-70%" y="-70%" width="240%" height="240%">
    <feGaussianBlur stdDeviation="4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="fBig" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="16" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="fSoft" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="24"/>
  </filter>
</defs>
"""


def doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n{defs()}\n{body}\n</svg>\n')


def page(w, h, accent=ORANGE, halftone="bottom"):
    out = [f'<rect width="{w}" height="{h}" fill="url(#gPage)"/>']
    out.append(f'<rect id="mk" width="{w}" height="{h}" fill="url(#hatch)" '
               f'opacity="0.5"/>')
    if halftone == "bottom":
        out.append(f'<rect x="0" y="{h * 0.58}" width="{w}" height="{h * 0.42}" '
                   f'fill="url(#htA)" opacity="0.5"/>')
        out.append(f'<rect x="0" y="{h * 0.58}" width="{w}" height="{h * 0.42}" '
                   f'fill="url(#gFadeUp)" opacity="0.75"/>')
    out.append(f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" '
               f'fill="none" stroke="{LINE}" stroke-width="1"/>')
    out.append(f'<rect x="0" y="0" width="96" height="3" fill="{accent}"/>')
    out.append(f'<rect x="{w - 3}" y="0" width="3" height="{h * 0.16}" '
               f'fill="{accent}" opacity="0.7"/>')
    return "".join(out)


def mpanel(x, y, w, h, cut=30, accent=None, texture="corner"):
    cid = uid("clip")
    pts = (f"{x + cut},{y} {x + w - cut},{y} {x + w},{y + cut} "
           f"{x + w},{y + h - cut} {x + w - cut},{y + h} {x + cut},{y + h} "
           f"{x},{y + h - cut} {x},{y + cut}")
    out = [f'<clipPath id="{cid}"><polygon points="{pts}"/></clipPath>',
           f'<polygon points="{pts}" fill="url(#gPanel)" stroke="{LINE2}" '
           f'stroke-width="1"/>']
    if texture == "corner":
        out.append(f'<g clip-path="url(#{cid})"><rect x="{x + w * 0.55}" y="{y}" '
                   f'width="{w * 0.45}" height="{h}" fill="url(#htA)" '
                   f'opacity="0.22"/></g>')
    elif texture == "bottom":
        out.append(f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y + h * 0.62}" '
                   f'width="{w}" height="{h * 0.38}" fill="url(#htB)" '
                   f'opacity="0.30"/></g>')
    if accent:
        out.append(f'<line x1="{x + cut}" y1="{y + 1.5}" x2="{x + w * 0.38}" '
                   f'y2="{y + 1.5}" stroke="{accent}" stroke-width="2"/>')
    return "".join(out), cid


def seal(cx, cy, r, label, color, rot=-8, size=None):
    """Rotated double ring seal - Bleach title-page badge."""
    size = size or r * 0.9
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#060607" '
            f'stroke="{color}" stroke-width="1.4"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 6}" fill="none" stroke="{color}" '
            f'stroke-width="1" stroke-dasharray="2 5" opacity="0.7"/>'
            + T(cx, cy + size * 0.35, label, size, color, 0, "900",
                anchor="middle", family=TITLE) + "</g>")


def inklines(x0, y0, x1, y1, n=40, seed=9, color=INK, op=(0.05, 0.16)):
    rnd = Rand(seed)
    out = []
    for _ in range(n):
        x = rnd.rng(x0, x1)
        y = rnd.rng(y0, y1)
        ln = rnd.rng(40, 220)
        out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + ln * 0.72:.0f}" '
                   f'y2="{y - ln * 0.69:.0f}" stroke="{color}" '
                   f'stroke-width="{rnd.rng(0.6, 1.8):.1f}" '
                   f'opacity="{rnd.rng(*op):.2f}"/>')
    return "".join(out)


def reiatsu_rings(cx, cy, color=ORANGE, n=3, dur=4.2):
    out = []
    for i in range(n):
        delay = i * dur / n
        out.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="8" fill="none" '
            f'stroke="{color}" stroke-width="2" opacity="0">'
            f'<animate attributeName="rx" values="30;520" dur="{dur}s" '
            f'begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="ry" values="8;150" dur="{dur}s" '
            f'begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.5;0" dur="{dur}s" '
            f'begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'</ellipse>')
    return "".join(out)


def butterfly(x=0, y=0, scale=1.0, color=PALE):
    """Hell butterfly (地獄蝶): two wings, glowing."""
    return (f'<g transform="translate({x} {y}) scale({scale})" filter="url(#fGlow)">'
            f'<path d="M0,0 C-16,-14 -30,-5 -25,7 C-20,16 -7,11 0,2 Z" '
            f'fill="{color}" opacity="0.85"/>'
            f'<path d="M0,0 C16,-14 30,-5 25,7 C20,16 7,11 0,2 Z" '
            f'fill="{color}" opacity="0.85"/>'
            f'<path d="M0,-4 L0,8" stroke="{color}" stroke-width="1.6"/>'
            f'<path d="M0,-4 L-6,-12 M0,-4 L6,-12" stroke="{color}" '
            f'stroke-width="0.8" opacity="0.8"/>'
            f'</g>')


def level_meta(w, jp, label, color=ORANGE):
    return (T(24, 62, jp, 24, color, 8, "700", family=JP)
            + T(24, 88, label, 12, INK, 5.5, "600", opacity=0.85))


# -- 1. hero ---------------------------------------------------------------
def katana():
    """Zanpakuto in local coords: blade up (-y), tsuba at origin, grip down."""
    p = []
    # blade
    p.append('<path d="M -8,-34 L 8,-34 L 10,-566 L 4,-636 L 0,-656 L -4,-636 '
             'L -10,-566 Z" fill="url(#gSteel)" stroke="#0A0A0B" '
             'stroke-width="1"/>')
    # edge highlight + hamon
    p.append('<path d="M 7,-40 L 8.5,-560" stroke="#FFFFFF" stroke-width="1.6" '
             'opacity="0.95"/>')
    p.append('<path d="M -7,-40 C -4,-200 -5,-420 -8,-556" stroke="#7A7A82" '
             'stroke-width="1" opacity="0.6"/>')
    # a gleam travelling up the blade
    p.append('<g><rect x="-9" y="-120" width="19" height="70" fill="#FFFFFF" '
             'opacity="0.0">'
             '<animate attributeName="y" values="-120;-620;-620" '
             'keyTimes="0;0.55;1" dur="5.5s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values="0;0.55;0;0" '
             'keyTimes="0;0.3;0.55;1" dur="5.5s" repeatCount="indefinite"/>'
             '</rect></g>')
    # tsuba
    p.append(f'<rect x="-32" y="-36" width="64" height="11" rx="3" fill="#111113" '
             f'stroke="{ORANGE}" stroke-width="1.4"/>')
    p.append(f'<rect x="-10" y="-25" width="20" height="16" fill="#141416" '
             f'stroke="{LINE2}" stroke-width="1"/>')
    # grip with diamond wrap
    p.append('<rect x="-9" y="-9" width="18" height="150" rx="4" fill="#141416" '
             'stroke="#2A2A2F" stroke-width="1"/>')
    for i in range(7):
        yy = 2 + i * 20
        p.append(f'<path d="M -9,{yy} L 0,{yy + 11} L 9,{yy} L 0,{yy - 11} Z" '
                 f'fill="none" stroke="{ORANGE}" stroke-width="1.1" '
                 f'opacity="0.55"/>')
    p.append('<circle cx="0" cy="146" r="5" fill="none" stroke="#3A3A40" '
             'stroke-width="1.4"/>')
    return "".join(p)


HAIR = "#FF7A18"
HAIR_D = "#A83404"
BODY = "#0A0A0C"
SKIN = "#E9C3A4"
SKIN_SH = "#C08D6C"
SKIN_D = "#8A563C"
MASK = "#F5F3EE"


def cleaver():
    """Giant slab of a zanpakuto, local coords: edge up (-y), grip down."""
    p = [f'<path d="M -34,40 L 30,40 L 46,-296 L 14,-382 L -30,-350 Z" '
         f'fill="{BODY}" stroke="{INK}" stroke-width="2.2" '
         f'stroke-opacity="0.85"/>',
         '<path d="M 30,40 L 46,-296 L 14,-382" fill="none" stroke="#FFFFFF" '
         'stroke-width="3.4" opacity="0.92"/>',
         f'<path d="M -14,16 L -4,-322" stroke="{ORANGE}" stroke-width="1.6" '
         f'opacity="0.32"/>',
         '<rect x="-19" y="28" width="38" height="104" rx="4" fill="#131316" '
         'stroke="#2C2C32" stroke-width="1.2"/>']
    for i in range(4):
        y = 40 + i * 24
        p.append(f'<path d="M -19,{y} L 0,{y + 12} L 19,{y} L 0,{y - 12} Z" '
                 f'fill="none" stroke="{ORANGE}" stroke-width="1.1" '
                 f'opacity="0.5"/>')
    p.append(f'<circle cx="0" cy="136" r="5" fill="none" stroke="#3A3A40" '
             f'stroke-width="1.4"/>')
    return "".join(p)


def portrait_panel():
    """The portrait, set into the hollow hole like a record photograph: warm
    duotone, vignette, a slow arc turning around it."""
    b64 = base64.b64encode((OUT / "portrait.jpg").read_bytes()).decode("ascii")
    cid = uid("portrait")
    p = ['<g transform="translate(980 300)">']

    p.append(f'<circle r="184" fill="{ORANGE}" opacity="0.13" '
             f'filter="url(#fSoft)">'
             f'<animate attributeName="opacity" values="0.13;0.21;0.13" '
             f'dur="7s" repeatCount="indefinite"/></circle>')

    p.append(f'<clipPath id="{cid}"><circle r="150"/></clipPath>')
    p.append(f'<g clip-path="url(#{cid})">')
    p.append(f'<image x="-150" y="-150" width="300" height="300" '
             f'preserveAspectRatio="xMidYMid slice" '
             f'href="data:image/jpeg;base64,{b64}" filter="url(#fDuo)"/>')
    p.append('<circle r="150" fill="url(#gVig)"/>')
    p.append(f'<path d="M -170,-38 L 170,-98 L 170,-62 L -170,-4 Z" '
             f'fill="{ORANGE}" opacity="0.09"/>')
    p.append("</g>")

    p.append('<circle r="151.5" fill="none" stroke="#0B0B0D" stroke-width="7"/>')
    p.append(f'<circle r="148" fill="none" stroke="{ORANGE}" stroke-width="1.8" '
             f'opacity="0.9"/>')
    p.append(f'<circle r="166" fill="none" stroke="{ORANGE}" stroke-width="1.4" '
             f'stroke-dasharray="70 260" opacity="0.75">'
             f'<animateTransform attributeName="transform" type="rotate" '
             f'from="0" to="360" dur="24s" repeatCount="indefinite"/></circle>')
    p.append(f'<circle r="177" fill="none" stroke="{INK}" stroke-width="0.9" '
             f'stroke-dasharray="2 10" opacity="0.32"/>')

    p.append("</g>")
    return "".join(p)


def hollow_mask(cx, cy, r, opacity=0.1):
    """Hollow mask watermark: oval, slanted eye slits, crest, teeth."""
    rx = r * 0.66
    eye = (f'M {cx - rx * 0.62:.0f} {cy - r * 0.26:.0f} '
           f'l {rx * 0.44:.0f} {r * 0.14:.0f} l -{rx * 0.1:.0f} {r * 0.19:.0f} '
           f'l -{rx * 0.4:.0f} -{r * 0.13:.0f} Z')
    eye2 = (f'M {cx + rx * 0.62:.0f} {cy - r * 0.26:.0f} '
            f'l -{rx * 0.44:.0f} {r * 0.14:.0f} l {rx * 0.1:.0f} {r * 0.19:.0f} '
            f'l {rx * 0.4:.0f} -{r * 0.13:.0f} Z')
    teeth = "".join(
        f'<path d="M {cx + (i - 1.5) * r * 0.24:.0f} {cy + r * 0.52:.0f} '
        f'l {r * 0.1:.0f} {r * 0.16:.0f} l {r * 0.1:.0f} -{r * 0.16:.0f}" '
        f'fill="none" stroke="{INK}" stroke-width="2"/>' for i in range(4))
    return (f'<g opacity="{opacity}" fill="none" stroke="{INK}" '
            f'stroke-width="2">'
            f'<path d="M {cx} {cy - r} C {cx + rx} {cy - r * 0.92:.0f} '
            f'{cx + rx} {cy + r * 0.3:.0f} {cx + rx * 0.6:.0f} '
            f'{cy + r * 0.78:.0f} L {cx} {cy + r} '
            f'L {cx - rx * 0.6:.0f} {cy + r * 0.78:.0f} '
            f'C {cx - rx} {cy + r * 0.3:.0f} {cx - rx} {cy - r * 0.92:.0f} '
            f'{cx} {cy - r} Z"/>'
            f'<path d="{eye}" fill="{INK}" stroke="none"/>'
            f'<path d="{eye2}" fill="{INK}" stroke="none"/>'
            f'<path d="M {cx} {cy - r * 0.62:.0f} L {cx} {cy + r * 0.44:.0f}"/>'
            f'{teeth}</g>')


def hero():
    w, h = 1200, 800
    b = [page(w, h, ORANGE)]

    # sun / hollow hole
    b.append(f'<circle cx="980" cy="296" r="300" fill="url(#gSun)" opacity="0.72">'
             f'<animate attributeName="opacity" values="0.64;0.8;0.64" dur="7s" '
             f'repeatCount="indefinite"/></circle>')
    b.append(f'<circle cx="980" cy="296" r="294" fill="none" stroke="{ORANGE}" '
             f'stroke-width="1" opacity="0.35"/>')
    b.append(f'<circle cx="980" cy="296" r="148" fill="url(#gHollow)"/>')
    b.append(f'<circle cx="980" cy="296" r="148" fill="none" stroke="{ORANGE}" '
             f'stroke-width="1.8" opacity="0.75"/>')

    b.append(deco(inklines(700, 40, 1180, 740, 46, 5)))

    # reiatsu shockwaves
    b.append(deco(reiatsu_rings(980, 700, ORANGE, 3, 5.0)))

    # light slashes passing behind the figure
    for i, yy in enumerate((296, 336)):
        b.append(f'<rect x="-360" y="{yy}" width="340" height="4" '
                 f'fill="url(#gBlade)" opacity="0.9">'
                 f'<animate attributeName="x" values="-360;1320;1320" '
                 f'keyTimes="0;0.22;1" dur="{7 + i * 1.5}s" begin="{i * 0.6}s" '
                 f'repeatCount="indefinite"/></rect>')

    # zanpakuto planted behind the mask
    b.append(f'<g transform="translate(1105 760) rotate(12)">{cleaver()}</g>')

    # reiatsu aura behind the body, so the silhouette reads below the sun
    b.append(f'<ellipse cx="980" cy="610" rx="330" ry="270" fill="url(#gRei)" '
             f'opacity="0.22">'
             f'<animate attributeName="opacity" values="0.15;0.28;0.15" dur="6s" '
             f'repeatCount="indefinite"/></ellipse>')

    # the substitute shinigami
    b.append(portrait_panel())

    # hell butterfly crossing the page
    b.append(deco(
        f'<g>{butterfly(0, 0, 1.5)}'
        f'<animateMotion dur="19s" repeatCount="indefinite" rotate="auto" '
        f'path="M 1160 96 C 980 40 900 210 760 168 C 620 126 520 268 360 232 '
        f'C 220 200 140 274 30 240"/></g>'))

    # copy block
    b.append(T(88, 132, "BLEACH // CHAPTER 01", 12.5, ORANGE, 6, "700"))
    b.append(f'<rect x="88" y="146" width="248" height="2" fill="{ORANGE}"/>')
    b.append(T(88, 238, SHINIGAMI, 32, INK, 9, "600", family=JP, opacity=0.92))

    b.append(f'<g transform="translate(86 372) skewX(-4)">'
             + T(0, 0, PLAYER["name"], 118, "url(#gName)", 2, "900", family=TITLE)
             + "</g>")
    b.append(f'<g transform="translate(90 430) skewX(-4)">'
             + T(0, 0, "SUBSTITUTE SHINIGAMI", 25, ORANGE, 12, "800")
             + "</g>")
    b.append(f'<rect x="88" y="452" width="300" height="1" fill="{LINE2}"/>')

    b.append(T(88, 494, "Every developer starts at level 1.", 21, INK, 0.4, "500"))
    b.append(T(88, 526, "Python " + DOT + " AI " + DOT + " computer vision " + DOT
               + " offline-first Android", 14.5, INK, 0.3, opacity=0.62))

    # reiatsu chip
    b.append(f'<rect x="88" y="560" width="322" height="42" fill="#0B0B0D" '
             f'stroke="{ORANGE}" stroke-width="1.2"/>')
    b.append(f'<circle cx="112" cy="581" r="4.5" fill="{ORANGE}" filter="url(#fGlow)">'
             f'<animate attributeName="opacity" values="1;0.1;1" dur="2s" '
             f'repeatCount="indefinite"/></circle>')
    b.append(T(132, 587, "REIATSU DETECTED", 12.5, ORANGE, 4, "700"))

    # spiritual pressure figure
    b.append(T(88, 620, "REIATSU", 11, DIM, 4, "600"))
    b.append(T(88, 700, f"{PLAYER['commits']}", 56, INK, 1, "900", family=TITLE))
    b.append(T(196, 700, "COMMITS", 12, DIM, 4, "600"))
    b.append(T(320, 700, "SEAT 16", 12, DIM, 4, "600"))

    b.append(T(88, 766, "PLAYER " + PLAYER["handle"].upper(), 11, DIM, 3))
    b.append(T(690, 766, "STATUS: ONLINE", 11, ORANGE, 3, anchor="end"))

    return doc(w, h, "".join(b))


# -- 2. shinigami file -----------------------------------------------------
def player():
    w, h = 1200, 640
    b = [page(w, h, ORANGE, halftone=None)]
    b.append(level_meta(w, "\u6b7b\u795e\u30d5\u30a1\u30a4\u30eb", "SHINIGAMI FILE"))
    b.append(T(1160, 74, "REAL NUMBERS ONLY", 10, DIM, 2.4, anchor="end"))

    b.append(mpanel(24, 116, 700, 296, 30, ORANGE, "corner")[0])
    b.append(T(56, 152, "\u767b\u9332", 12, DIM, 4, family=JP))
    b.append(T(712, 152, "REGISTRY", 9.5, DIM, 3, anchor="end"))
    rows = [("NAME", PLAYER["given"]), ("ROLE", PLAYER["role"]),
            ("ZANPAKUTO", PLAYER["zanpakuto"]), ("SPECIALTY", PLAYER["spec"]),
            ("CURRENT MISSION", PLAYER["quest"])]
    for i, (k, v) in enumerate(rows):
        y = 190 + i * 40
        b.append(T(56, y, k, 10, DIM, 3.4))
        b.append(T(240, y, v, 16.5, INK, 1.1, "600"))
        b.append(f'<rect x="56" y="{y + 13}" width="636" height="1" fill="{LINE}"/>')

    b.append(mpanel(740, 116, 436, 296, 30, ORANGE, "corner")[0])
    b.append(T(772, 152, "\u970a\u5727", 12, DIM, 4, family=JP))
    b.append(T(1144, 152, "REIATSU", 9.5, DIM, 3, anchor="end"))
    b.append(f'<ellipse cx="960" cy="286" rx="150" ry="86" fill="url(#gRei)" '
             f'opacity="0.35">'
             f'<animate attributeName="opacity" values="0.22;0.5;0.22" dur="4.5s" '
             f'repeatCount="indefinite"/></ellipse>')
    b.append(T(772, 300, f"{PLAYER['commits']}", 92, INK, 1, "900", family=TITLE))
    b.append(T(772, 336, "COMMITS", 10.5, DIM, 4, "600"))
    b.append(T(1144, 300, "SEAT", 9.5, DIM, 3.4, anchor="end"))
    b.append(T(1144, 336, f"{PLAYER['seat']:02d}", 30, ORANGE, 1, "900",
               anchor="end", family=TITLE))
    b.append(T(1144, 358, "THEMATIC", 8.5, DIM, 2, anchor="end"))

    tiles = [(f"{PLAYER['commits']}", "COMMITS", "\u63a8\u9032", ORANGE),
             (f"{PLAYER['repos']:02d}", "PUBLIC REPOS", "\u4f5c\u54c1", PALE),
             (f"{PLAYER['languages']:02d}", "LANGUAGES", "\u8a00\u8a9e", RED),
             (f"{PLAYER['tests']}", "PASSING TESTS", "\u8a66\u9a13", GOLD)]
    tw = (1200 - 48 - 3 * 14) / 4
    for i, (val, label, jp, col) in enumerate(tiles):
        x = 24 + i * (tw + 14)
        b.append(mpanel(x, 432, tw, 180, 26, col, "bottom")[0])
        b.append(T(x + 22, 468, jp, 12.5, col, 5, "600", family=JP))
        b.append(T(x + 22, 490, label, 9.5, DIM, 3.2, "600"))
        b.append(T(x + 22, 566, val, 54, INK, 0, "900", family=TITLE))
        b.append(f'<rect x="{x + 22}" y="578" width="{tw - 44}" height="2" '
                 f'fill="{col}" opacity="0.55"/>')

    b.append(T(24, 628, "SEAT IS PROGRESSION, NOT A RANK " + DOT
               + " COUNTS READ FROM THE GITHUB API", 9.5, DIM, 2))
    return doc(w, h, "".join(b))


# -- 3. zanpakuto releases -------------------------------------------------
def abilities():
    w, h = 1200, 540
    b = [page(w, h, PALE, halftone=None)]
    b.append(level_meta(w, "\u65ac\u9b44\u5200", "ZANPAKUTO " + DOT + " THREE RELEASES",
                        PALE))
    b.append(T(1160, 74, "NO PERCENTAGES", 10, DIM, 2.4, anchor="end"))

    cw = (1200 - 48 - 2 * 16) / 3
    for i, (jp, name, tier, sub, items, col) in enumerate(ABILITIES):
        x = 24 + i * (cw + 16)
        panel, cid = mpanel(x, 116, cw, 348, 28, col, "bottom")
        b.append(panel)
        b.append(deco(T(x + cw - 24, 430, jp, 118, col, 0, "700", anchor="end",
                        family=JP, opacity=0.07)))
        b.append(T(x + 24, 160, jp, 20, col, 4, "700", family=JP))
        b.append(T(x + 24, 186, name, 15, INK, 5, "700"))
        b.append(T(x + 24, 206, tier + " " + DOT + " " + sub, 9.5, DIM, 2.4))
        b.append(f'<rect x="{x + 24}" y="220" width="{cw - 48}" height="1" '
                 f'fill="{LINE2}"/>')
        for j, it in enumerate(items):
            y = 256 + j * 32
            b.append(f'<path d="M{x + 24} {y - 4} l5 4 l-5 4 l-5 -4 Z" fill="{col}" '
                     f'opacity="0.7"/>')
            b.append(T(x + 42, y, it, 15.5, INK, 0.5))
        # charging reiatsu underline
        b.append(f'<g clip-path="url(#{cid})">'
                 f'<rect x="{x + 24}" y="446" height="2" fill="{col}" opacity="0.8" '
                 f'width="0">'
                 f'<animate attributeName="width" '
                 f'values="0;{cw - 48:.0f};{cw - 48:.0f};0" '
                 f'keyTimes="0;0.35;0.8;1" dur="6s" begin="{i * 0.5}s" '
                 f'repeatCount="indefinite"/></rect></g>')

    b.append(T(24, 512, "\u5207\u308a\u958b\u3051\u308d", 11, INK, 5, family=JP,
               opacity=0.5))
    return doc(w, h, "".join(b))


# -- 4. mission cards ------------------------------------------------------
def quest_card(q, idx):
    w, h = 1200, 276
    accent = GOLD if q["rank"] == "S" else PALE
    status_col = ORANGE if q["status"] != "SEALED" else PALE
    b = [page(w, h, accent, halftone=None)]

    b.append(T(24, 34, f"\u4efb\u52d9 {idx:02d}", 12.5, accent, 5, "700", family=JP))
    b.append(T(168, 34, q["threat"], 10, DIM, 3.6, "600"))

    panel, cid = mpanel(24, 48, 1152, 196, 38, accent, "corner")
    b.append(panel)

    # sheen sweep, clipped to the panel
    b.append(f'<g clip-path="url(#{cid})">'
             f'<rect y="48" width="180" height="196" fill="url(#gSheen)" opacity="0.5">'
             f'<animate attributeName="x" values="24;1180;1180" '
             f'keyTimes="0;0.3;1" dur="7s" begin="{idx * 0.9}s" '
             f'repeatCount="indefinite"/></rect></g>')

    b.append(seal(104, 146, 38, q["rank"], accent, rot=-8, size=32))
    b.append(T(104, 200, "THREAT", 8.5, DIM, 2.4, anchor="middle"))

    b.append(T(168, 128, q["name"], 30, INK, 1, "900", family=TITLE))
    b.append(T(168, 156, q["kind"], 11, INK, 3.4, "600", opacity=0.72))
    b.append(T(168, 184, q["jp"], 12.5, accent, 4, "600", family=JP))

    for i, line in enumerate(wrap(q["desc"], 80)[:2]):
        b.append(T(548, 134 + i * 24, line, 13.5, INK, 0.3, opacity=0.8))

    b.append(T(1152, 206, q["tech"], 10.5, RED, 0.8, anchor="end", opacity=0.95))

    sw = 168
    b.append(f'<g transform="rotate(-2 1085 79)">'
             f'<rect x="{1152 - sw}" y="66" width="{sw}" height="26" fill="#060607" '
             f'stroke="{status_col}" stroke-width="1"/>'
             + T(1152 - sw / 2, 84, q["status"], 10, status_col, 2.2, "700",
                 anchor="middle") + "</g>")

    return doc(w, h, "".join(b))


# -- 5. mission ------------------------------------------------------------
def mission():
    w, h = 1200, 460
    b = [page(w, h, RED, halftone=None)]
    b.append(level_meta(w, "\u5345\u89e3", "BANKAI " + DOT + " CURRENT OBJECTIVE", RED))
    b.append(T(1160, 74, "WHAT I AM DOING NOW", 10, DIM, 2.4, anchor="end"))

    b.append(deco(hollow_mask(1040, 194, 96, 0.12)))

    b.append(f'<ellipse cx="600" cy="196" rx="430" ry="126" fill="url(#gRei)" '
             f'opacity="0.28">'
             f'<animate attributeName="opacity" values="0.16;0.4;0.16" dur="6s" '
             f'repeatCount="indefinite"/></ellipse>')
    b.append(T(60, 186, "\u201cTransform ideas into working software.\u201d", 36, INK,
               0.5, "700"))
    b.append(T(62, 220, "\u601d\u8003\u3092\u3001\u52d5\u304f\u5f62\u3078\u3002", 15,
               RED, 5, "600", family=JP))
    b.append(f'<rect x="60" y="240" height="1.5" fill="{RED}" opacity="0.8" width="0">'
             f'<animate attributeName="width" values="0;1080;1080" '
             f'keyTimes="0;0.4;1" dur="5s" repeatCount="indefinite"/></rect>')

    for i, (num, title, note) in enumerate(GOALS):
        x = 60 + i * 364
        b.append(mpanel(x, 268, 340, 128, 24, RED, "corner")[0])
        b.append(T(x + 22, 302, num, 11.5, RED, 3, "800", family=TITLE))
        b.append(T(x + 22, 328, title, 14, INK, 2, "700"))
        for j, line in enumerate(wrap(note, 34)[:2]):
            b.append(T(x + 22, 350 + j * 19, line, 11, INK, 0.3, opacity=0.65))

    b.append(T(24, 442, "OBJECTIVES ARE SELF-SET " + DOT + " NO DEADLINES PROMISED",
               9.5, DIM, 2))
    return doc(w, h, "".join(b))


# -- 6. log + honours ------------------------------------------------------
def log_panel():
    w, h = 1200, 620
    b = [page(w, h, PALE, halftone=None)]
    b.append(level_meta(w, "\u8a18\u9332", "SYSTEM LOG", PALE))
    b.append(T(1160, 74, "FROM THE GITHUB API", 10, DIM, 2.4, anchor="end"))

    log_panel, log_clip = mpanel(24, 116, 700, 440, 30, PALE, "bottom")
    b.append(log_panel)
    b.append(f'<g clip-path="url(#{log_clip})">'
             f'<rect y="116" width="170" height="440" fill="url(#gSheen)" '
             f'opacity="0.30">'
             f'<animate attributeName="x" values="24;720;720" keyTimes="0;0.32;1" '
             f'dur="9s" repeatCount="indefinite"/></rect></g>')
    b.append(T(56, 156, "\u6700\u8fd1\u306e\u63a8\u9032", 12, DIM, 4, family=JP))
    b.append(f'<circle cx="614" cy="152" r="3.5" fill="{ORANGE}" filter="url(#fGlow)">'
             f'<animate attributeName="opacity" values="1;0.15;1" dur="2.6s" '
             f'repeatCount="indefinite"/></circle>')
    b.append(T(692, 156, "RECENT PUSHES", 9.5, DIM, 3, anchor="end"))
    for i, (date, repo, lang) in enumerate(LOG):
        y = 202 + i * 64
        b.append(T(56, y, date, 11.5, DIM, 1.4))
        b.append(T(184, y, repo, 17, INK, 0.5, "600"))
        b.append(T(692, y, lang, 11, PALE, 1.8, anchor="end"))
        b.append(f'<rect x="56" y="{y + 15}" width="636" height="1" fill="{LINE}"/>')

    b.append(mpanel(748, 116, 428, 440, 30, GOLD, "bottom")[0])
    b.append(T(780, 156, "\u52f2\u7ae0", 12, DIM, 4, family=JP))
    b.append(T(1144, 156, "HONOURS", 9.5, DIM, 3, anchor="end"))
    for i, (title, note) in enumerate(REWARDS):
        y = 192 + i * 118
        b.append(f'<g transform="rotate(-1.2 960 {y + 34})">'
                 f'<rect x="780" y="{y}" width="364" height="98" fill="#070708" '
                 f'stroke="{GOLD}" stroke-width="1" opacity="0.6" '
                 f'stroke-dasharray="6 4"/></g>')
        b.append(T(802, y + 34, title, 16, GOLD, 2.2, "800", family=HEAVY))
        for j, line in enumerate(wrap(note, 40)[:2]):
            b.append(T(802, y + 58 + j * 19, line, 11, INK, 0.3, opacity=0.7))

    b.append(T(24, 606, "HONOURS ARE SHIPPED WORK " + DOT
               + " THREAT CLASS IS THEMATIC, NOT A CERTIFICATE", 9.5, DIM, 2))
    return doc(w, h, "".join(b))


# -- 7. finale -------------------------------------------------------------
def footer():
    w, h = 1200, 470
    b = [page(w, h, ORANGE, halftone="bottom")]

    b.append(deco(reiatsu_rings(600, 250, ORANGE, 3, 6.0)))

    # zanpakuto planted at the edge
    b.append(deco(f'<g transform="translate(1064 392) scale(0.5) rotate(8)">'
                  f'{katana()}</g>'))

    # bankai flash
    b.append(f'<rect width="{w}" height="{h}" fill="#FFFFFF" opacity="0">'
             f'<animate attributeName="opacity" '
             f'values="0;0;0.12;0;0;0;0" keyTimes="0;0.62;0.66;0.72;0.8;0.94;1" '
             f'dur="7s" repeatCount="indefinite"/></rect>')

    # 卍解 drawn on with a stroke sweep
    b.append(deco(f'<g transform="translate(600 196)">'
                  + f'<text x="0" y="0" font-family="{JP}" font-size="112" '
                    f'font-weight="700" fill="none" stroke="{ORANGE}" '
                    f'stroke-width="1.5" text-anchor="middle" '
                    f'letter-spacing="10" opacity="0.55" '
                    f'stroke-dasharray="1600" stroke-dashoffset="1600">'
                    f'{BANKAI}'
                    f'<animate attributeName="stroke-dashoffset" '
                    f'values="1600;0;0" keyTimes="0;0.35;1" dur="7s" '
                    f'repeatCount="indefinite"/></text>'
                  + T(0, 0, BANKAI, 112, "url(#gName)", 10, "700",
                      anchor="middle", family=JP)
                  + "</g>"))

    b.append(T(600, 300, "THE STORY CONTINUES", 40, INK, 3, "900",
               anchor="middle", family=TITLE))
    b.append(T(600, 366, "\u7d9a\u304f", 24, ORANGE, 10, "600",
               anchor="middle", family=JP))
    b.append(f'<rect x="420" y="390" width="360" height="1" fill="{LINE2}"/>')
    b.append(T(600, 426, "Keep building. Keep learning. Keep leveling up.", 17,
               INK, 0.5, "500", anchor="middle", opacity=0.85))
    b.append(T(600, 452, "PLAYER: MAHESH " + DOT + " SYSTEM STATUS: ALWAYS EVOLVING",
               10, ORANGE, 3.2, "600", anchor="middle"))
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
