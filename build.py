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

# ======== EDIT ME: content ========
# About paragraph, one entry per rendered line (keep each ~80 chars to fit width)
ABOUT_LINES = [
    "SPEC-DRIVEN PRODUCT DESIGNER BRIDGING DESIGN AND DEVELOPMENT. I TURN CONCEPTS INTO",
    "INTERACTIVE, ANIMATED, DEV-READY DESIGNS — FIGMA, FRAMER, REACT / TS, GSAP, WEBGL.",
]
# ==================================

# ---------- hero typing SMIL ----------
def hero_typing(p):
    adv = 18.3  # 0.618em advance @28px + 1px letter-spacing
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
    s.append(f'<text x="34" y="54" class="lead" fill="{p["dim"]}">'
             f'// INITIALISING PROFILE</text>')
    s.append(title)
    s.append(cursor)
    s.append(f'<text x="34" y="128" class="sub" fill="{p["muted"]}">'
             f'BRIDGING THE GAP BETWEEN DESIGN AND DEVELOPMENT.</text>')
    # 00 / ABOUT
    s.append(f'<text x="8" y="186" class="sh" fill="{p["faint"]}">00 / ABOUT</text>')
    s.append(f'<line x1="120" y1="182" x2="832" y2="182" stroke="{p["rule"]}" stroke-width="1"/>')
    ay = 216
    for line in ABOUT_LINES:
        s.append(f'<text x="8" y="{ay}" class="ab" fill="{p["about"]}">{esc(line)}</text>')
        ay += 22
    # 01 / SOCIALS header (chips render below as markdown)
    sy = ay + 28
    s.append(f'<text x="8" y="{sy}" class="sh" fill="{p["faint"]}">01 / SOCIALS</text>')
    s.append(f'<line x1="140" y1="{sy-4}" x2="832" y2="{sy-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    H = sy + 22
    body = "\n".join(s) + '\n</svg>'
    return body.replace(f'height="310" viewBox="0 0 840 310"',
                        f'height="{H}" viewBox="0 0 840 {H}"')

# ---------- banner B: languages + recognitions + footer ----------
# EDIT ME: fallback core stack, used only when langs.json is absent (no live data yet)
LANGS_DEFAULT = [("TYPESCRIPT", 36), ("JAVASCRIPT", 22), ("SWIFT", 18), ("CSS", 14), ("HTML", 10)]

_lj = os.path.join(HERE, "langs.json")
if os.path.exists(_lj):
    import json as _json
    with open(_lj) as _f:
        LANGS = [(str(n).upper(), int(p)) for n, p in _json.load(_f)]
else:
    LANGS = LANGS_DEFAULT

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
    maxp = max(pt for _, pt in LANGS)
    rows = (len(LANGS) + 1) // 2
    lang_top = 60
    lang_bottom = lang_top + (rows - 1) * 32 + 12
    rec_h = lang_bottom + 40           # recognitions header baseline
    W, H = 840, rec_h + 128
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
    for i, (name, pct) in enumerate(LANGS):
        col = 8 if i % 2 == 0 else 430
        y = lang_top + (i // 2) * 32
        s.append(lang_cells(col, y, name, pct, maxp, p))
    # 03 / RECOGNITIONS
    ry = rec_h
    s.append(f'<text x="8" y="{ry}" class="sh" fill="{p["faint"]}">03 / RECOGNITIONS</text>')
    s.append(f'<line x1="172" y1="{ry-4}" x2="832" y2="{ry-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    cy = ry + 18
    s.append(f'<rect x="8" y="{cy}" width="384" height="34" rx="6" fill="none" '
             f'stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="24" y="{cy+21}" class="chip"><tspan fill="{p["dim"]}">3X </tspan>'
             f'<tspan fill="{p["text"]}">HONORABLE MENTION {esc("—")} WIX STUDIO x NEWFORM</tspan></text>')
    s.append(f'<rect x="400" y="{cy}" width="248" height="34" rx="6" fill="none" '
             f'stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="416" y="{cy+21}" class="chip"><tspan fill="{p["dim"]}">{esc("—")} </tspan>'
             f'<tspan fill="{p["text"]}">FRAMER TOP 1% CREATOR</tspan></text>')
    # footer
    fy = cy + 70
    s.append(f'<line x1="8" y1="{fy}" x2="832" y2="{fy}" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append(f'<text x="8" y="{fy+24}" class="ft" fill="{p["dim"]}">DESIGN + DEV BY ME</text>')
    s.append(f'<text x="832" y="{fy+24}" text-anchor="end" class="ft" fill="{p["dim"]}">'
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

# ---------- mobile variants (narrow viewBox, single column, larger relative text) ----------
def wrap(text, maxc):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + (1 if cur else 0) <= maxc:
            cur = (cur + " " + w) if cur else w
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def hero_typing_m(p, fs=22, x0=20, baseline=72):
    adv = fs * 0.618 + 1
    n = 16
    widths = [round(i * adv) for i in range(n + 1)]
    kt = [round(i / n * 0.40, 4) for i in range(n + 1)]
    wvals = ";".join(str(w) for w in widths) + f";{widths[-1]};0"
    ktvals = ";".join(str(k) for k in kt) + ";0.60;1"
    xvals = ";".join(str(x0 + w) for w in widths) + f";{x0 + widths[-1]};{x0}"
    top, h = round(baseline - fs * 0.80), round(fs * 1.05)
    clip = (f'<clipPath id="tcm"><rect x="{x0-2}" y="{top}" width="0" height="{h}">'
            f'<animate attributeName="width" values="{wvals}" keyTimes="{ktvals}" '
            f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>')
    title = (f'<text x="{x0}" y="{baseline}" clip-path="url(#tcm)" '
             f'style="font-size:{fs}px;letter-spacing:1px" fill="{p["text"]}">PRODUCT DESIGNER</text>')
    cursor = (f'<rect y="{top}" width="2.5" height="{round(fs)}" fill="{p["text"]}">'
              f'<animate attributeName="x" values="{xvals}" keyTimes="{ktvals}" '
              f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
              f'dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    return clip, title, cursor

def banner_a_mobile(p):
    W = 440
    clip, title, cursor = hero_typing_m(p)
    s = [f'<svg width="{W}" height="500" viewBox="0 0 {W} 500" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Sworup Kumar Behuria, Product Designer">']
    s.append(f'<defs><style>{FONT_FACE}text{{font-family:FM,monospace}}'
             f'.lead{{font-size:10px;letter-spacing:2px}}.sub{{font-size:9.5px;letter-spacing:.4px}}'
             f'.sh{{font-size:10px;letter-spacing:2px}}.ab{{font-size:11px;letter-spacing:.3px}}'
             f'</style>{clip}</defs>')
    s.append(f'<rect x="6" y="8" width="428" height="108" rx="8" fill="none" stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="20" y="36" class="lead" fill="{p["dim"]}">// INITIALISING PROFILE</text>')
    s.append(title); s.append(cursor)
    s.append(f'<text x="20" y="100" class="sub" fill="{p["muted"]}">BRIDGING THE GAP BETWEEN DESIGN AND DEVELOPMENT.</text>')
    s.append(f'<text x="6" y="152" class="sh" fill="{p["faint"]}">00 / ABOUT</text>')
    s.append(f'<line x1="84" y1="148" x2="434" y2="148" stroke="{p["rule"]}" stroke-width="1"/>')
    ay = 178
    for line in wrap(" ".join(ABOUT_LINES), 48):
        s.append(f'<text x="6" y="{ay}" class="ab" fill="{p["about"]}">{esc(line)}</text>')
        ay += 20
    sy = ay + 24
    s.append(f'<text x="6" y="{sy}" class="sh" fill="{p["faint"]}">01 / SOCIALS</text>')
    s.append(f'<line x1="120" y1="{sy-4}" x2="434" y2="{sy-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    H = sy + 18
    return ("\n".join(s) + "\n</svg>").replace('height="500" viewBox="0 0 440 500"',
                                               f'height="{H}" viewBox="0 0 440 {H}"')

def banner_b_mobile(p):
    W = 440
    maxp = max(pt for _, pt in LANGS)
    s = [f'<svg width="{W}" height="600" viewBox="0 0 {W} 600" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Most used languages and recognitions">']
    s.append(f'<defs><style>{FONT_FACE}text{{font-family:FM,monospace}}'
             f'.sh{{font-size:10px;letter-spacing:2px}}.ln{{font-size:11px;letter-spacing:1px}}'
             f'.pc{{font-size:11px;letter-spacing:1px}}.chip{{font-size:10px;letter-spacing:1px}}'
             f'.ft{{font-size:9px;letter-spacing:1.5px}}</style></defs>')
    s.append(f'<text x="6" y="30" class="sh" fill="{p["faint"]}">02 / MOST USED</text>')
    s.append(f'<line x1="140" y1="26" x2="434" y2="26" stroke="{p["rule"]}" stroke-width="1"/>')
    ly = 56
    for name, pct in LANGS:
        s.append(f'<text x="6" y="{ly+11}" class="ln" fill="{p["about"]}">{name}</text>')
        cx = 116
        filled = round(pct / maxp * 12)
        for i in range(12):
            col = p["cellon"] if i < filled else p["celloff"]
            s.append(f'<rect x="{cx + i*16}" y="{ly+1}" width="12" height="12" fill="{col}"/>')
        s.append(f'<text x="{cx + 12*16 + 8}" y="{ly+11}" class="pc" fill="{p["faint"]}">{pct}%</text>')
        ly += 28
    ry = ly + 20
    s.append(f'<text x="6" y="{ry}" class="sh" fill="{p["faint"]}">03 / RECOGNITIONS</text>')
    s.append(f'<line x1="172" y1="{ry-4}" x2="434" y2="{ry-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    c1 = ry + 14
    s.append(f'<rect x="6" y="{c1}" width="428" height="32" rx="6" fill="none" stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="18" y="{c1+20}" class="chip"><tspan fill="{p["dim"]}">3X </tspan>'
             f'<tspan fill="{p["text"]}">HONORABLE MENTION {esc("—")} WIX STUDIO x NEWFORM</tspan></text>')
    c2 = c1 + 42
    s.append(f'<rect x="6" y="{c2}" width="428" height="32" rx="6" fill="none" stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="18" y="{c2+20}" class="chip"><tspan fill="{p["dim"]}">{esc("—")} </tspan>'
             f'<tspan fill="{p["text"]}">FRAMER TOP 1% CREATOR</tspan></text>')
    fy = c2 + 58
    s.append(f'<line x1="6" y1="{fy}" x2="434" y2="{fy}" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append(f'<text x="6" y="{fy+22}" class="ft" fill="{p["dim"]}">DESIGN + DEV BY ME</text>')
    s.append(f'<text x="6" y="{fy+38}" class="ft" fill="{p["dim"]}">{esc("©")} 2026 SWORUP KUMAR BEHURIA</text>')
    H = fy + 50
    return ("\n".join(s) + "\n</svg>").replace('height="600" viewBox="0 0 440 600"',
                                               f'height="{H}" viewBox="0 0 440 {H}"')

# ---------- README ----------
def readme():
    chips = []
    for key, label, url in SOCIALS:
        chips.append(f'[<img src="./assets/soc-{key}.svg" height="36" alt="{esc(label)}">]({url})')
    chip_row = "\n".join(chips)
    return f"""<picture>
  <source media="(max-width: 768px) and (prefers-color-scheme: dark)" srcset="./assets/banner-a-mobile-dark.svg">
  <source media="(max-width: 768px)" srcset="./assets/banner-a-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-a-dark.svg">
  <img alt="Sworup Kumar Behuria — Product Designer" src="./assets/banner-a-light.svg" width="100%">
</picture>

{chip_row}

<picture>
  <source media="(max-width: 768px) and (prefers-color-scheme: dark)" srcset="./assets/banner-b-mobile-dark.svg">
  <source media="(max-width: 768px)" srcset="./assets/banner-b-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-b-dark.svg">
  <img alt="Most used languages and recognitions" src="./assets/banner-b-light.svg" width="100%">
</picture>

<!--
  Repo: sworup-kumar/sworup-kumar  (must match your username exactly)
  Banners are responsive: mobile variants serve under 768px, desktop above.
  The GitHub-native activity graph renders automatically below this README.
  Language %s come from fetch_langs.py (live); recognitions/about live in build.py.
-->
"""

def main():
    open(os.path.join(ASSETS, "banner-a-dark.svg"), "w").write(banner_a(DARK))
    open(os.path.join(ASSETS, "banner-a-light.svg"), "w").write(banner_a(LIGHT))
    open(os.path.join(ASSETS, "banner-b-dark.svg"), "w").write(banner_b(DARK))
    open(os.path.join(ASSETS, "banner-b-light.svg"), "w").write(banner_b(LIGHT))
    open(os.path.join(ASSETS, "banner-a-mobile-dark.svg"), "w").write(banner_a_mobile(DARK))
    open(os.path.join(ASSETS, "banner-a-mobile-light.svg"), "w").write(banner_a_mobile(LIGHT))
    open(os.path.join(ASSETS, "banner-b-mobile-dark.svg"), "w").write(banner_b_mobile(DARK))
    open(os.path.join(ASSETS, "banner-b-mobile-light.svg"), "w").write(banner_b_mobile(LIGHT))
    for key, label, _ in SOCIALS:
        open(os.path.join(ASSETS, f"soc-{key}.svg"), "w").write(chip_svg(label))
    open(os.path.join(HERE, "README.md"), "w").write(readme())
    print("built:", sorted(os.listdir(ASSETS)))

if __name__ == "__main__":
    main()
