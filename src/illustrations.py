#!/usr/bin/env python3
"""Generates the site's demo illustrations (flat SVG, brand palette, no people).

Usage:  python src/illustrations.py   → writes assets/illustrations/*.svg

These are replaceable demo visuals. Swap any of them for real photography by
editing src/data/images.json; nothing else needs to change.
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "illustrations"
W, H = 800, 450

C = dict(cream="#F4ECE3", cream2="#FBF8F4", floor="#EADBCB", wine="#5B1A33", deep="#2E0F1D", wine2="#7A2A48",
         rose="#E7C9D1", blush="#F3E6E9", gold="#D4A853", gold2="#ECD5A2", gold3="#8A6420", wood="#6E4F1A",
         mari="#E8A33A", mari2="#F2C45A", leaf="#7C8454", white="#FFFFFF")


def svg(body, defs="", bg=C["cream"]):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<pattern id="jali" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="24" height="24" fill="{C['deep']}"/><rect x="3" y="3" width="18" height="18" fill="none" stroke="{C['gold']}" stroke-opacity=".45" stroke-width="1.5"/>
<circle cx="12" cy="12" r="2" fill="{C['gold']}" fill-opacity=".5"/></pattern>
<radialGradient id="glow" cx=".78" cy=".2" r=".55"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".7"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
{defs}
</defs>
<rect width="{W}" height="{H}" fill="{bg}"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{body}
</svg>
'''


def arch(cx, top, half, bottom, **attrs):
    """Mughal-style round arch: straight sides from `bottom` up to `top`, semicircle above."""
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="M{cx - half} {bottom} V{top} A{half} {half} 0 0 1 {cx + half} {top} V{bottom} Z" {a}/>'


def marigold(x, y, r=9):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{C["mari"]}"/>'
            f'<circle cx="{x - r * .25:.1f}" cy="{y - r * .25:.1f}" r="{r * .55:.1f}" fill="{C["mari2"]}"/>')


def garland(p0, c, p2, n=13, r=9, leaves=True):
    """Marigold string along a quadratic curve, with a leaf between flowers."""
    out = []
    pts = []
    for i in range(n):
        t = i / (n - 1)
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t ** 2 * p2[1]
        pts.append((x, y))
    out.append(f'<path d="M{p0[0]} {p0[1]} Q{c[0]} {c[1]} {p2[0]} {p2[1]}" fill="none" stroke="{C["leaf"]}" stroke-width="2"/>')
    for i, (x, y) in enumerate(pts):
        if leaves and i < len(pts) - 1:
            mx, my = (x + pts[i + 1][0]) / 2, (y + pts[i + 1][1]) / 2
            out.append(f'<ellipse cx="{mx:.1f}" cy="{my + 4:.1f}" rx="{r * .45:.1f}" ry="{r * .9:.1f}" fill="{C["leaf"]}" transform="rotate(20 {mx:.1f} {my + 4:.1f})"/>')
        out.append(marigold(x, y, r))
    return "".join(out)


def strand(x, y0, n=4, r=7):
    return "".join(marigold(x, y0 + i * r * 2.1, r) for i in range(n))


def lantern(x, y):
    return (f'<line x1="{x}" y1="0" x2="{x}" y2="{y - 22}" stroke="{C["gold3"]}" stroke-width="2"/>'
            f'<path d="M{x - 14} {y - 22} h28 l6 12 v26 l-6 12 h-28 l-6 -12 v-26 z" fill="{C["gold"]}"/>'
            f'<rect x="{x - 9}" y="{y - 12}" width="18" height="24" rx="3" fill="{C["gold2"]}"/>'
            f'<path d="M{x - 6} {y + 28} h12 l-6 10 z" fill="{C["gold3"]}"/>')


def floor(y=372, color=None):
    return f'<rect x="0" y="{y}" width="{W}" height="{H - y}" fill="{color or C["floor"]}"/>'


def sparkle(x, y, s=10, color=None):
    s2 = s * .28
    return (f'<path d="M{x} {y - s} L{x + s2} {y - s2} L{x + s} {y} L{x + s2} {y + s2} L{x} {y + s} '
            f'L{x - s2} {y + s2} L{x - s} {y} L{x - s2} {y - s2} Z" fill="{color or C["gold"]}"/>')


def diya(x, y):
    return (f'<path d="M{x - 26} {y} Q{x} {y + 26} {x + 26} {y} Z" fill="{C["gold3"]}"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="26" ry="5" fill="{C["gold"]}"/>'
            f'<path d="M{x} {y - 30} C{x + 10} {y - 16} {x + 7} {y - 4} {x} {y - 3} C{x - 7} {y - 4} {x - 10} {y - 16} {x} {y - 30} Z" fill="{C["mari2"]}"/>'
            f'<path d="M{x} {y - 20} C{x + 4} {y - 13} {x + 3} {y - 6} {x} {y - 5} C{x - 3} {y - 6} {x - 4} {y - 13} {x} {y - 20} Z" fill="{C["white"]}" fill-opacity=".8"/>')


def ghost_arches():
    return (arch(400, 170, 190, 450, fill="none", stroke=C["gold"], stroke_opacity=".35", stroke_width="1.5")
            + arch(400, 200, 230, 450, fill="none", stroke=C["gold"], stroke_opacity=".18", stroke_width="1"))


# ---------------------------------------------------------------------------- scenes
def family_meeting():
    sofa = lambda x, flip=1: (
        f'<rect x="{x}" y="250" width="150" height="80" rx="28" fill="{C["wine2"]}"/>'
        f'<rect x="{x - 12}" y="300" width="174" height="48" rx="16" fill="{C["wine"]}"/>'
        f'<rect x="{x + (18 if flip == 1 else 92)}" y="266" width="40" height="36" rx="10" fill="{C["gold2"]}"/>'
        f'<rect x="{x}" y="346" width="10" height="20" fill="{C["deep"]}"/><rect x="{x + 140}" y="346" width="10" height="20" fill="{C["deep"]}"/>')
    cup = lambda x: (f'<ellipse cx="{x}" cy="323" rx="17" ry="4" fill="{C["gold2"]}"/>'
                     f'<path d="M{x - 11} 304 h22 l-3 17 h-16 z" fill="{C["cream2"]}" stroke="{C["gold"]}" stroke-width="1.5"/>')
    body = (floor()
            + arch(400, 190, 150, 372, fill=C["wine"])
            + arch(400, 196, 128, 372, fill="url(#jali)")
            + garland((236, 150), (400, 262), (564, 150))
            + strand(236, 150) + strand(564, 150)
            + lantern(118, 110) + lantern(682, 110)
            + f'<ellipse cx="400" cy="404" rx="300" ry="34" fill="{C["rose"]}"/>'
            + f'<ellipse cx="400" cy="404" rx="282" ry="27" fill="none" stroke="{C["gold"]}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>'
            + sofa(70) + sofa(580, -1)
            + f'<rect x="300" y="332" width="200" height="30" rx="4" fill="{C["wood"]}"/>'
            + f'<rect x="316" y="360" width="10" height="26" fill="{C["wood"]}"/><rect x="474" y="360" width="10" height="26" fill="{C["wood"]}"/>'
            + f'<ellipse cx="400" cy="332" rx="112" ry="15" fill="{C["gold3"]}"/>'
            # teapot
            + f'<ellipse cx="400" cy="306" rx="30" ry="24" fill="{C["cream2"]}" stroke="{C["gold"]}" stroke-width="2"/>'
            + f'<path d="M428 300 q22 -6 26 -24" fill="none" stroke="{C["cream2"]}" stroke-width="7" stroke-linecap="round"/>'
            + f'<path d="M372 296 q-20 4 -12 22" fill="none" stroke="{C["gold"]}" stroke-width="4" stroke-linecap="round"/>'
            + f'<ellipse cx="400" cy="284" rx="15" ry="5" fill="{C["gold"]}"/><circle cx="400" cy="277" r="4" fill="{C["gold"]}"/>'
            + f'<path d="M378 312 h44" stroke="{C["wine"]}" stroke-width="2" stroke-dasharray="3 4"/>'
            + cup(338) + cup(466)
            # plate of sweets
            + f'<ellipse cx="400" cy="339" rx="30" ry="6" fill="{C["cream2"]}"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{C["mari2"]}"/>' for x, y in [(388, 334), (400, 332), (412, 334), (394, 328), (406, 328)])
            )
    return svg(body)


def verification():
    lines = lambda x, y, n, w: "".join(f'<rect x="{x}" y="{y + i * 20}" width="{w - (i % 2) * 40}" height="8" rx="4" fill="{C["rose"]}"/>' for i in range(n))
    body = (ghost_arches() + floor(390, C["rose"])
            # ID card behind
            + f'<g transform="rotate(-8 330 230)"><rect x="200" y="150" width="250" height="160" rx="16" fill="{C["wine"]}"/>'
            + f'<rect x="222" y="190" width="56" height="44" rx="8" fill="{C["gold"]}"/><rect x="232" y="202" width="36" height="20" rx="3" fill="{C["gold2"]}"/>'
            + f'<rect x="296" y="194" width="130" height="8" rx="4" fill="{C["gold2"]}"/><rect x="296" y="214" width="100" height="8" rx="4" fill="{C["gold2"]}" fill-opacity=".6"/>'
            + f'<rect x="222" y="262" width="204" height="8" rx="4" fill="{C["gold2"]}" fill-opacity=".45"/></g>'
            # document
            + f'<rect x="330" y="84" width="230" height="290" rx="14" fill="{C["white"]}" stroke="{C["rose"]}" stroke-width="2"/>'
            + f'<rect x="330" y="84" width="230" height="46" rx="14" fill="{C["wine"]}"/><rect x="330" y="112" width="230" height="18" fill="{C["wine"]}"/>'
            + f'<rect x="352" y="101" width="90" height="10" rx="5" fill="{C["gold2"]}"/>'
            + lines(352, 156, 8, 186)
            # shield
            + f'<path d="M560 212 c26 0 52 -10 64 -22 c12 12 38 22 64 22 v58 c0 50 -40 78 -64 90 c-24 -12 -64 -40 -64 -90 z" fill="{C["wine"]}" stroke="{C["gold"]}" stroke-width="5"/>'
            + f'<path d="M596 272 l20 20 l40 -44" fill="none" stroke="{C["gold2"]}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
            # stamp
            + f'<circle cx="382" cy="330" r="34" fill="none" stroke="{C["gold3"]}" stroke-width="3"/>'
            + f'<circle cx="382" cy="330" r="26" fill="none" stroke="{C["gold3"]}" stroke-width="1.5" stroke-dasharray="3 4"/>'
            + sparkle(382, 330, 12, C["gold3"])
            # pen
            + f'<g transform="rotate(35 520 380)"><rect x="440" y="372" width="150" height="16" rx="8" fill="{C["deep"]}"/>'
            + f'<path d="M440 372 l-24 8 l24 8 z" fill="{C["gold"]}"/><rect x="560" y="370" width="10" height="20" fill="{C["gold"]}"/></g>'
            + sparkle(150, 110, 12) + sparkle(680, 120, 8) + sparkle(700, 330, 10, C["gold3"]))
    return svg(body, bg=C["blush"])


def privacy_photo():
    defs = (f'<linearGradient id="veil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["rose"]}"/><stop offset="1" stop-color="{C["wine2"]}"/></linearGradient>'
            f'<filter id="blur" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>'
            f'<clipPath id="frameClip"><path d="M290 380 V190 A110 110 0 0 1 510 190 V380 Z"/></clipPath>')
    body = (arch(400, 170, 190, 450, fill="none", stroke=C["gold"], stroke_opacity=".35", stroke_width="1.5")
            + floor(392, "#2A0D19")
            + arch(400, 190, 124, 394, fill=C["gold"])
            + arch(400, 190, 110, 380, fill="url(#veil)")
            + f'<g clip-path="url(#frameClip)" filter="url(#blur)"><circle cx="360" cy="220" r="60" fill="{C["blush"]}" fill-opacity=".8"/>'
            + f'<circle cx="450" cy="300" r="70" fill="{C["wine"]}"/><circle cx="400" cy="160" r="40" fill="{C["gold2"]}" fill-opacity=".7"/></g>'
            # dupatta drape
            + f'<path d="M150 450 C220 330 330 360 400 300 C470 360 580 330 650 450 Z" fill="{C["rose"]}" fill-opacity=".92"/>'
            + f'<path d="M150 450 C220 330 330 360 400 300 C470 360 580 330 650 450" fill="none" stroke="{C["gold"]}" stroke-width="3" stroke-dasharray="1 9" stroke-linecap="round"/>'
            # padlock
            + f'<path d="M528 262 v-26 a32 32 0 0 1 64 0 v26" fill="none" stroke="{C["gold2"]}" stroke-width="12"/>'
            + f'<rect x="506" y="258" width="108" height="92" rx="16" fill="{C["gold"]}"/>'
            + f'<circle cx="560" cy="296" r="11" fill="{C["deep"]}"/><rect x="555" y="300" width="10" height="26" rx="4" fill="{C["deep"]}"/>'
            + sparkle(170, 120, 12, C["gold2"]) + sparkle(640, 110, 9, C["gold2"]) + sparkle(120, 260, 7, C["gold"]))
    return svg(body, defs=defs, bg=C["deep"])


def support():
    heart = ('M400 360 C330 312 262 262 262 198 C262 158 294 128 332 128 C360 128 384 144 400 168 '
             'C416 144 440 128 468 128 C506 128 538 158 538 198 C538 262 470 312 400 360 Z')
    body = (ghost_arches() + floor(378, "#EEDDB8")
            + garland((90, 60), (400, 170), (710, 60), n=17, r=10)
            + f'<path d="{heart}" fill="{C["wine"]}"/>'
            + f'<path d="{heart}" fill="none" stroke="{C["gold"]}" stroke-width="5" transform="translate(400 244) scale(.82) translate(-400 -244)"/>'
            + sparkle(400, 238, 30, C["gold2"])
            + diya(200, 380) + diya(600, 380)
            + "".join(marigold(x, 392, 7) for x in (280, 312, 488, 520))
            + sparkle(130, 250, 10) + sparkle(680, 240, 12))
    return svg(body, bg="#F6ECD6")


def rings():
    body = (ghost_arches() + floor(376, C["rose"])
            + f'<ellipse cx="400" cy="372" rx="150" ry="30" fill="{C["deep"]}" fill-opacity=".18"/>'
            + f'<path d="M262 330 q0 -46 138 -46 q138 0 138 46 q0 40 -138 40 q-138 0 -138 -40 z" fill="{C["wine"]}"/>'
            + f'<path d="M262 330 q0 40 138 40 q138 0 138 -40" fill="none" stroke="{C["gold"]}" stroke-width="4"/>'
            + f'<ellipse cx="400" cy="300" rx="120" ry="18" fill="{C["wine2"]}"/>'
            + f'<circle cx="368" cy="226" r="54" fill="none" stroke="{C["gold3"]}" stroke-width="16"/>'
            + f'<circle cx="368" cy="226" r="54" fill="none" stroke="{C["gold"]}" stroke-width="10"/>'
            + f'<circle cx="436" cy="226" r="54" fill="none" stroke="{C["gold3"]}" stroke-width="16"/>'
            + f'<circle cx="436" cy="226" r="54" fill="none" stroke="{C["gold"]}" stroke-width="10"/>'
            # re-draw the left ring's right arc on top so the rings interlock
            + f'<path d="M402 184 A54 54 0 0 1 402 268" fill="none" stroke="{C["gold3"]}" stroke-width="16"/>'
            + f'<path d="M402 184 A54 54 0 0 1 402 268" fill="none" stroke="{C["gold"]}" stroke-width="10"/>'
            + f'<path d="M334 196 a48 48 0 0 1 30 -22" fill="none" stroke="{C["gold2"]}" stroke-width="4" stroke-linecap="round"/>'
            + sparkle(470, 150, 14, C["gold3"]) + sparkle(300, 150, 9, C["gold3"]) + sparkle(560, 250, 8)
            + "".join(marigold(x, y, r) for x, y, r in [(170, 380, 8), (205, 395, 6), (610, 388, 8), (640, 402, 6), (590, 408, 5)]))
    return svg(body, bg=C["blush"])


def registration():
    row = lambda y, done: (f'<rect x="352" y="{y}" width="26" height="26" rx="6" fill="{C["wine"] if done else C["white"]}" stroke="{C["wine"]}" stroke-width="2"/>'
                           + (f'<path d="M358 {y + 13} l6 6 l10 -12" fill="none" stroke="{C["gold2"]}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>' if done else "")
                           + f'<rect x="392" y="{y + 5}" width="{120 if done else 96}" height="8" rx="4" fill="{C["rose"]}"/>'
                           + f'<rect x="392" y="{y + 17}" width="70" height="6" rx="3" fill="{C["rose"]}" fill-opacity=".6"/>')
    zig = " ".join(f"l-8 {'-' if i % 2 else ''}8" for i in range(14))  # back along the bottom edge
    body = (ghost_arches() + floor(390)
            + f'<rect x="318" y="70" width="230" height="310" rx="18" fill="{C["gold3"]}"/>'
            + f'<rect x="334" y="96" width="198" height="270" rx="10" fill="{C["white"]}"/>'
            + f'<rect x="392" y="56" width="82" height="36" rx="10" fill="{C["gold"]}"/><circle cx="433" cy="66" r="6" fill="{C["gold3"]}"/>'
            + row(126, True) + row(176, True) + row(226, True) + row(276, False)
            + f'<rect x="352" y="326" width="120" height="14" rx="7" fill="{C["wine"]}"/>'
            # receipt
            + f'<g transform="rotate(7 600 250)"><path d="M548 160 h112 v160 {zig} z" fill="{C["cream2"]}" stroke="{C["gold"]}" stroke-width="2"/>'
            + f'<rect x="566" y="184" width="76" height="10" rx="5" fill="{C["wine"]}"/>'
            + "".join(f'<rect x="566" y="{210 + i * 20}" width="{76 - (i % 2) * 24}" height="7" rx="3.5" fill="{C["rose"]}"/>' for i in range(4))
            + f'<circle cx="632" cy="296" r="14" fill="none" stroke="{C["gold3"]}" stroke-width="2.5"/></g>'
            # pen
            + f'<g transform="rotate(-28 250 300)"><rect x="170" y="292" width="150" height="16" rx="8" fill="{C["wine"]}"/>'
            + f'<path d="M170 292 l-24 8 l24 8 z" fill="{C["gold"]}"/><rect x="290" y="290" width="10" height="20" fill="{C["gold"]}"/></g>'
            + lantern(120, 120) + sparkle(690, 110, 12) + sparkle(220, 90, 8, C["gold3"]))
    return svg(body)


def journey():
    defs = (f'<radialGradient id="door" cx=".5" cy=".7" r=".7"><stop offset="0" stop-color="{C["cream2"]}"/>'
            f'<stop offset=".55" stop-color="{C["gold2"]}"/><stop offset="1" stop-color="{C["gold"]}"/></radialGradient>')
    stones = [(110, 410, 46), (220, 378, 40), (318, 352, 34), (400, 332, 29), (470, 316, 24)]
    body = (floor(300, C["floor"])
            + f'<path d="M0 300 Q400 270 800 300 V450 H0 Z" fill="{C["floor"]}"/>'
            + arch(560, 160, 110, 300, fill=C["wine"])
            + arch(560, 168, 90, 300, fill="url(#door)")
            + f'<path d="M470 300 L380 450 H740 L650 300 Z" fill="{C["gold2"]}" fill-opacity=".35"/>'
            + garland((436, 118), (560, 200), (684, 118), n=11, r=8)
            + strand(436, 118, 3, 6) + strand(684, 118, 3, 6)
            + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .32:.1f}" fill="{C["rose"]}" stroke="{C["gold"]}" stroke-width="2"/>' for x, y, r in stones)
            + diya(420, 292) + diya(700, 292)
            + lantern(160, 120) + sparkle(300, 130, 10) + sparkle(740, 80, 8, C["gold3"]))
    return svg(body, defs=defs, bg=C["cream"])


SCENES = {
    "family-meeting": family_meeting,
    "verification": verification,
    "privacy-photo": privacy_photo,
    "support": support,
    "rings": rings,
    "registration": registration,
    "journey": journey,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        data = fn()
        (OUT / f"{name}.svg").write_text(data, "utf-8", newline="\n")
        print(f"{name}.svg {len(data.encode()) / 1024:.1f} KB")
