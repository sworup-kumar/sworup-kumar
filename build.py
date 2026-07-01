#!/usr/bin/env python3
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
with open(os.path.join(ASSETS, "fm-latin.b64")) as f:
    FONT_B64 = f.read().strip()

FONT_FACE = (
    "@font-face{font-family:'FM';font-style:normal;font-weight:400;"
    "src:url(data:font/woff2;base64," + FONT_B64 + ") format('woff2');}"
)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------- palettes ----------
DARK = dict(text="#EDEDED", muted="#8A8A8A", dim="#5A5A5A", faint="#6E6E6E",
            about="#C4C4C4", border="rgba(255,255,255,.14)",
            rule="rgba(255,255,255,.10)", cellon="#EDEDED",
            celloff="rgba(255,255,255,.13)")
LIGHT = dict(text="#1F2328", muted="#57606A", dim="#8C959F", faint="#6E7781",
             about="#3D444D", border="rgba(0,0,0,.16)",
             rule="rgba(0,0,0,.10)", cellon="#1F2328",
             celloff="rgba(0,0,0,.10)")

# ---------- hero typing SMIL ----------
def hero_typing(p):
    adv = 16.8
    n = 16  # chars in "PRODUCT DESIGNER"
    widths = [round(i * adv) for i in range(n + 1)]
    kt = [round(i / n * 0.40, 4) for i in range(n + 1)]
    wvals = ";".join(str(w) for w in widths) + f";{widths[-1]};0"
    ktvals = ";".join(str(k) for k in kt) + ";0.60;1"
    xvals = ";".join(str(34 + w) for w in widths) + f";{34 + widths[-1]};34"
    clip = (
        f'<clipPath id="tc"><rect x="32" y="74" width="0" height="34">'
        f'<animate attributeName="width" values="{wvals}" keyTimes="{ktvals}" '
        f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>'
    )
    title = (
        f'<text x="34" y="100" clip-path="url(#tc)" class="h1" fill="{p["text"]}">'
        f'PRODUCT DESIGNER</text>'
    )
    cursor = (
        f'<rect y="76" width="2.5" height="28" fill="{p["text"]}">'
        f'<animate attributeName="x" values="{xvals}" keyTimes="{ktvals}" '
        f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
        f'dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    )
    return clip, title, cursor

# ---------- banner A: hero + about + socials header ----------
def banner_a(p):
    clip, title, cursor = hero_typing(p)
    W, H = 840, 310
    s = []
    s.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Sworup Kumar Behuria, Product Designer">')
    s.append(f'<defs><style>{FONT_FACE}'
             f'text{{font-family:FM,monospace}}'
             f'.h1{{font-size:28px;letter-spacing:1px}}'
             f'.lead{{font-size:11px;letter-spacing:2px}}'
             f'.sub{{font-size:12px;letter-spacing:.6px}}'
             f'.tag{{font-size:10px;letter-spacing:1.5px}}'
             f'.sh{{font-size:11px;letter-spacing:2px}}'
             f'.ab{{font-size:12.5px;letter-spacing:.4px}}'
             f'</style>{clip}</defs>')
    # hero box
    s.append(f'<rect x="8" y="10" width="824" height="132" rx="8" fill="none" '
             f'stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="812" y="32" text-anchor="end" class="tag" '
             f'fill="{p["dim"]}">SWORUP KUMAR BEHURIA</text>')
    s.append(f'<text x="34" y="54" class="lead" fill="{p["dim"]}">'
             f'// INITIALISING PROFILE</text>')
    s.append(title)
    s.append(cursor)
    s.append(f'<text x="34" y="128" class="sub" fill="{p["muted"]}">'
             f'BRIDGING THE GAP BETWEEN DESIGN AND DEVELOPMENT.</text>')
    # 00 / ABOUT
    s.append(f'<text x="8" y="186" class="sh" fill="{p["faint"]}">00 / ABOUT</text>')
    s.append(f'<line x1="120" y1="182" x2="832" y2="182" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append(f'<text x="8" y="216" class="ab" fill="{p["about"]}">'
             f'SPEC-DRIVEN PRODUCT DESIGNER BRIDGING DESIGN AND DEVELOPMENT. I TURN CONCEPTS INTO</text>')
    s.append(f'<text x="8" y="238" class="ab" fill="{p["about"]}">'
             f'INTERACTIVE, ANIMATED, DEV-READY DESIGNS {esc("—")} FIGMA, FRAMER, REACT / TS, GSAP, WEBGL.</text>')
    # 01 / SOCIALS header (chips render below as markdown)
    s.append(f'<text x="8" y="288" class="sh" fill="{p["faint"]}">01 / SOCIALS</text>')
    s.append(f'<line x1="140" y1="284" x2="832" y2="284" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append('</svg>')
    return "\n".join(s)

# ---------- banner B: languages + recognitions + footer ----------
LANGS = [("TYPESCRIPT", 41), ("JAVASCRIPT", 28), ("CSS", 19), ("HTML", 12)]

def lang_cells(x, y, name, pct, maxp, p):
    out = [f'<text x="{x}" y="{y+11}" class="ln" fill="{p["about"]}">{name}</text>']
    cx = x + 104
    filled = round(pct / maxp * 12)
    for i in range(12):
        col = p["cellon"] if i < filled else p["celloff"]
        out.append(f'<rect x="{cx + i*13}" y="{y+1}" width="10" height="11" fill="{col}"/>')
    out.append(f'<text x="{cx + 12*13 + 8}" y="{y+11}" class="pc" fill="{p["faint"]}">{pct}%</text>')
    return "".join(out)

def banner_b(p):
    W, H = 840, 282
    maxp = max(pt for _, pt in LANGS)
    s = []
    s.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Most used languages and recognitions">')
    s.append(f'<defs><style>{FONT_FACE}'
             f'text{{font-family:FM,monospace}}'
             f'.sh{{font-size:11px;letter-spacing:2px}}'
             f'.ln{{font-size:11px;letter-spacing:1px}}'
             f'.pc{{font-size:11px;letter-spacing:1px}}'
             f'.chip{{font-size:11px;letter-spacing:1px}}'
             f'.ft{{font-size:10px;letter-spacing:1.5px}}'
             f'</style></style></defs>'.replace("</style></style>", "</style>"))
    # 02 / MOST USED
    s.append(f'<text x="8" y="34" class="sh" fill="{p["faint"]}">02 / MOST USED</text>')
    s.append(f'<line x1="150" y1="30" x2="832" y2="30" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append(lang_cells(8, 60, LANGS[0][0], LANGS[0][1], maxp, p))
    s.append(lang_cells(430, 60, LANGS[1][0], LANGS[1][1], maxp, p))
    s.append(lang_cells(8, 92, LANGS[2][0], LANGS[2][1], maxp, p))
    s.append(lang_cells(430, 92, LANGS[3][0], LANGS[3][1], maxp, p))
    # 03 / RECOGNITIONS
    s.append(f'<text x="8" y="154" class="sh" fill="{p["faint"]}">03 / RECOGNITIONS</text>')
    s.append(f'<line x1="172" y1="150" x2="832" y2="150" stroke="{p["rule"]}" stroke-width="1"/>')
    # chip 1
    s.append(f'<rect x="8" y="172" width="384" height="34" rx="6" fill="none" '
             f'stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="24" y="193" class="chip"><tspan fill="{p["dim"]}">3X </tspan>'
             f'<tspan fill="{p["text"]}">HONORABLE MENTION {esc("—")} WIX STUDIO x NEWFORM</tspan></text>')
    # chip 2
    s.append(f'<rect x="400" y="172" width="248" height="34" rx="6" fill="none" '
             f'stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="416" y="193" class="chip"><tspan fill="{p["dim"]}">{esc("—")} </tspan>'
             f'<tspan fill="{p["text"]}">FRAMER TOP 1% CREATOR</tspan></text>')
    # footer
    s.append(f'<line x1="8" y1="242" x2="832" y2="242" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append(f'<text x="8" y="266" class="ft" fill="{p["dim"]}">DESIGN + DEV BY ME</text>')
    s.append(f'<text x="832" y="266" text-anchor="end" class="ft" fill="{p["dim"]}">'
             f'{esc("©")} 2026 SWORUP KUMAR BEHURIA</text>')
    s.append('</svg>')
    return "\n".join(s)

# ---------- social chips (neutral, theme-agnostic) ----------
SOCIALS = [
    ("linkedin", "/ LINKEDIN", "https://www.linkedin.com/in/sworup-behuria/"),
    ("instagram", "/ INSTAGRAM", "https://www.instagram.com/sworup_ku/"),
    ("x", "/ TWITTER (X)", "https://x.com/sworup_ku"),
    ("portfolio", "/ PORTFOLIO", "https://www.sworupkumar.com/"),
    ("email", "/ EMAIL", "mailto:hello@sworupkumar.com"),
]
CHIP_TXT = "#7C848D"
CHIP_SLASH = "#5C636B"
CHIP_BORDER = "rgba(124,132,141,.40)"

def chip_svg(label):
    adv = 7.3  # 12px mono
    w = round(len(label) * adv) + 44
    h = 38
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}">'
        f'<defs><style>{FONT_FACE}text{{font-family:FM,monospace;font-size:12px;letter-spacing:1px}}</style></defs>'
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="6" fill="none" '
        f'stroke="{CHIP_BORDER}" stroke-width="1"/>'
        f'<text x="18" y="24"><tspan fill="{CHIP_SLASH}">/ </tspan>'
        f'<tspan fill="{CHIP_TXT}">{esc(label[2:])}</tspan></text></svg>'
    )

# ---------- README ----------
def readme():
    chips = []
    for key, label, url in SOCIALS:
        chips.append(f'[<img src="./assets/soc-{key}.svg" height="36" alt="{esc(label)}">]({url})')
    chip_row = "\n".join(chips)
    return f"""<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-a-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner-a-light.svg">
  <img alt="Sworup Kumar Behuria — Product Designer" src="./assets/banner-a-dark.svg" width="100%">
</picture>

{chip_row}

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-b-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner-b-light.svg">
  <img alt="Most used languages and recognitions" src="./assets/banner-b-dark.svg" width="100%">
</picture>

<!--
  Repo: sworup-kumar/sworup-kumar  (must match your username exactly)
  The GitHub-native activity graph renders automatically below this README.
  Language %s and recognitions are hand-set in build.py — edit + re-run to update.
-->
"""

def main():
    open(os.path.join(ASSETS, "banner-a-dark.svg"), "w").write(banner_a(DARK))
    open(os.path.join(ASSETS, "banner-a-light.svg"), "w").write(banner_a(LIGHT))
    open(os.path.join(ASSETS, "banner-b-dark.svg"), "w").write(banner_b(DARK))
    open(os.path.join(ASSETS, "banner-b-light.svg"), "w").write(banner_b(LIGHT))
    for key, label, _ in SOCIALS:
        open(os.path.join(ASSETS, f"soc-{key}.svg"), "w").write(chip_svg(label))
    open(os.path.join(HERE, "README.md"), "w").write(readme())
    print("built:", sorted(os.listdir(ASSETS)))

if __name__ == "__main__":
    main()
