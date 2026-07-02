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

# Match the effective gap GitHub adds between the linked social row and the
# following banner. These values are measured in each SVG's viewBox units.
SECTION_GAP = 60
SECTION_GAP_MOBILE = 65

# ======== EDIT ME: content ========
# About paragraph, one entry per rendered line (keep each ~80 chars to fit width)
ABOUT_LINES = [
    "I'M A SPEC-DRIVEN PRODUCT DESIGNER. I TURN CONCEPTS INTO INTERACTIVE,",
    "ANIMATED, DEV-READY DESIGNS THAT AMPLIFIES YOUR PRESENCE.",
    "I ALSO BUILD APPS!",
]
# ==================================

# ---------- hero typing SMIL ----------
def hero_typing(p, baseline=90):
    adv = 18.3  # 0.618em advance @28px + 1px letter-spacing
    n = 16  # chars in "PRODUCT DESIGNER"
    widths = [round(i * adv) for i in range(n + 1)]
    kt = [round(i / n * 0.40, 4) for i in range(n + 1)]
    wvals = ";".join(str(w) for w in widths) + f";{widths[-1]};0"
    ktvals = ";".join(str(k) for k in kt) + ";0.60;1"
    xvals = ";".join(str(34 + w) for w in widths) + f";{34 + widths[-1]};34"
    clip_y, cur_y = baseline - 26, baseline - 24
    clip = (
        f'<clipPath id="tc"><rect x="32" y="{clip_y}" width="0" height="34">'
        f'<animate attributeName="width" values="{wvals}" keyTimes="{ktvals}" '
        f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>'
    )
    title = (
        f'<text x="34" y="{baseline}" clip-path="url(#tc)" class="h1" fill="{p["text"]}">'
        f'PRODUCT DESIGNER</text>'
    )
    cursor = (
        f'<rect y="{cur_y}" width="2.5" height="28" fill="{p["text"]}">'
        f'<animate attributeName="x" values="{xvals}" keyTimes="{ktvals}" '
        f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
        f'dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    )
    return clip, title, cursor

# ---------- banner A: hero + about + socials header ----------
def banner_a(p):
    # equal-padding hero: box derives from content + PAD on top and bottom
    PAD = 28
    box_top = 10
    lead_b = box_top + PAD + 8          # 11px lead ascent ~8
    title_b = lead_b + 46
    sub_b = title_b + 28
    box_bottom = sub_b + PAD
    box_h = box_bottom - box_top
    clip, title, cursor = hero_typing(p, baseline=title_b)
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
    s.append(f'<rect x="8" y="{box_top}" width="824" height="{box_h}" rx="8" fill="none" '
             f'stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="34" y="{lead_b}" class="lead" fill="{p["dim"]}">'
             f'// INITIALISING PROFILE</text>')
    s.append(title)
    s.append(cursor)
    s.append(f'<text x="34" y="{sub_b}" class="sub" fill="{p["muted"]}">'
             f'BRIDGING THE GAP BETWEEN DESIGN AND DEVELOPMENT.</text>')
    # 00 / ABOUT
    about_y = box_bottom + SECTION_GAP + 9
    s.append(f'<text x="8" y="{about_y}" class="sh" fill="{p["faint"]}">00 / ABOUT</text>')
    s.append(f'<line x1="120" y1="{about_y-4}" x2="832" y2="{about_y-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    ay = about_y + 30
    for line in ABOUT_LINES:
        s.append(f'<text x="8" y="{ay}" class="ab" fill="{p["about"]}">{esc(line)}</text>')
        ay += 22
    # 01 / SOCIALS header (chips render below as markdown)
    about_bottom = ay - 18
    sy = about_bottom + SECTION_GAP + 9
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
    most_y = 48
    lang_top = most_y + 26
    lang_bottom = lang_top + (rows - 1) * 32 + 12
    rec_h = lang_bottom + SECTION_GAP + 9
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
    s.append(f'<text x="8" y="{most_y}" class="sh" fill="{p["faint"]}">02 / MOST USED</text>')
    s.append(f'<line x1="150" y1="{most_y-4}" x2="832" y2="{most_y-4}" stroke="{p["rule"]}" stroke-width="1"/>')
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
    s.append(f'<text x="416" y="{cy+21}" class="chip" fill="{p["text"]}">FRAMER TOP 1% CREATOR</text>')
    # footer
    fy = cy + 70
    s.append(f'<line x1="8" y1="{fy}" x2="832" y2="{fy}" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append(f'<text x="8" y="{fy+24}" class="ft" fill="{p["dim"]}">DESIGN + DEV BY ME</text>')
    s.append(f'<text x="832" y="{fy+24}" text-anchor="end" class="ft" fill="{p["dim"]}">'
             f'{esc("©")} 2026 SWORUP KUMAR BEHURIA</text>')
    s.append('</svg>')
    return "\n".join(s)

# ---------- social chips (adaptive palette, individual links) ----------
SOCIALS = [
    ("linkedin", "/ LINKEDIN", "https://www.linkedin.com/in/sworup-behuria/"),
    ("instagram", "/ INSTAGRAM", "https://www.instagram.com/sworup_ku/"),
    ("x", "/ TWITTER (X)", "https://x.com/sworup_ku"),
    ("portfolio", "/ PORTFOLIO", "https://www.sworupkumar.com/"),
    ("email", "/ EMAIL", "mailto:hello@sworupkumar.com"),
]
def chip_svg(label, width=None, centered=False):
    adv = 7.9  # 13px mono
    w = width or round(len(label) * adv) + 46
    h = 44
    text_x = w / 2 if centered else 18
    anchor = ' text-anchor="middle"' if centered else ''
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}">'
        f'<defs><style>{FONT_FACE}'
        f':root{{--chip-text:#57606A;--chip-slash:#8C959F;--chip-border:rgba(0,0,0,.20)}}'
        f'@media (prefers-color-scheme:dark){{:root{{--chip-text:#C4C4C4;--chip-slash:#6E6E6E;--chip-border:rgba(255,255,255,.18)}}}}'
        f'text{{font-family:FM,monospace;font-size:13px;letter-spacing:1px}}'
        f'</style></defs>'
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="6" fill="none" '
        f'stroke="var(--chip-border)" stroke-width="1"/>'
        f'<text x="{text_x:g}" y="28"{anchor}><tspan fill="var(--chip-slash)">/ </tspan>'
        f'<tspan fill="var(--chip-text)">{esc(label[2:])}</tspan></text></svg>'
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
    PAD = 18
    box_top = 8
    lead_b = box_top + PAD + 7          # 10px lead ascent ~7
    title_b = lead_b + 36
    sub_b = title_b + 28
    box_bottom = sub_b + PAD
    box_h = box_bottom - box_top
    clip, title, cursor = hero_typing_m(p, baseline=title_b)
    s = [f'<svg width="{W}" height="500" viewBox="0 0 {W} 500" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Sworup Kumar Behuria, Product Designer">']
    s.append(f'<defs><style>{FONT_FACE}text{{font-family:FM,monospace}}'
             f'.lead{{font-size:10px;letter-spacing:2px}}.sub{{font-size:9.5px;letter-spacing:.4px}}'
             f'.sh{{font-size:10px;letter-spacing:2px}}.ab{{font-size:11px;letter-spacing:.3px}}'
             f'</style>{clip}</defs>')
    s.append(f'<rect x="6" y="{box_top}" width="428" height="{box_h}" rx="8" fill="none" stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="20" y="{lead_b}" class="lead" fill="{p["dim"]}">// INITIALISING PROFILE</text>')
    s.append(title); s.append(cursor)
    s.append(f'<text x="20" y="{sub_b}" class="sub" fill="{p["muted"]}">BRIDGING THE GAP BETWEEN DESIGN AND DEVELOPMENT.</text>')
    about_y = box_bottom + SECTION_GAP_MOBILE + 8
    s.append(f'<text x="6" y="{about_y}" class="sh" fill="{p["faint"]}">00 / ABOUT</text>')
    s.append(f'<line x1="84" y1="{about_y-4}" x2="434" y2="{about_y-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    ay = about_y + 26
    for line in wrap(" ".join(ABOUT_LINES), 48):
        s.append(f'<text x="6" y="{ay}" class="ab" fill="{p["about"]}">{esc(line)}</text>')
        ay += 20
    about_bottom = ay - 16
    sy = about_bottom + SECTION_GAP_MOBILE + 8
    s.append(f'<text x="6" y="{sy}" class="sh" fill="{p["faint"]}">01 / SOCIALS</text>')
    s.append(f'<line x1="120" y1="{sy-4}" x2="434" y2="{sy-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    H = sy + 18
    return ("\n".join(s) + "\n</svg>").replace('height="500" viewBox="0 0 440 500"',
                                               f'height="{H}" viewBox="0 0 440 {H}"')

def banner_b_mobile(p):
    W = 440
    maxp = max(pt for _, pt in LANGS)
    most_y = 42
    s = [f'<svg width="{W}" height="600" viewBox="0 0 {W} 600" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Most used languages and recognitions">']
    s.append(f'<defs><style>{FONT_FACE}text{{font-family:FM,monospace}}'
             f'.sh{{font-size:10px;letter-spacing:2px}}.ln{{font-size:11px;letter-spacing:1px}}'
             f'.pc{{font-size:11px;letter-spacing:1px}}.chip{{font-size:10px;letter-spacing:1px}}'
             f'.ft{{font-size:9px;letter-spacing:1.5px}}</style></defs>')
    s.append(f'<text x="6" y="{most_y}" class="sh" fill="{p["faint"]}">02 / MOST USED</text>')
    s.append(f'<line x1="140" y1="{most_y-4}" x2="434" y2="{most_y-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    ly = most_y + 26
    for name, pct in LANGS:
        s.append(f'<text x="6" y="{ly+11}" class="ln" fill="{p["about"]}">{name}</text>')
        cx = 116
        filled = round(pct / maxp * 12)
        for i in range(12):
            col = p["cellon"] if i < filled else p["celloff"]
            s.append(f'<rect x="{cx + i*16}" y="{ly+1}" width="12" height="12" fill="{col}"/>')
        s.append(f'<text x="{cx + 12*16 + 8}" y="{ly+11}" class="pc" fill="{p["faint"]}">{pct}%</text>')
        ly += 28
    lang_bottom = ly - 15
    ry = lang_bottom + SECTION_GAP_MOBILE + 8
    s.append(f'<text x="6" y="{ry}" class="sh" fill="{p["faint"]}">03 / RECOGNITIONS</text>')
    s.append(f'<line x1="172" y1="{ry-4}" x2="434" y2="{ry-4}" stroke="{p["rule"]}" stroke-width="1"/>')
    c1 = ry + 14
    s.append(f'<rect x="6" y="{c1}" width="428" height="32" rx="6" fill="none" stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="18" y="{c1+20}" class="chip"><tspan fill="{p["dim"]}">3X </tspan>'
             f'<tspan fill="{p["text"]}">HONORABLE MENTION {esc("—")} WIX STUDIO x NEWFORM</tspan></text>')
    c2 = c1 + 42
    s.append(f'<rect x="6" y="{c2}" width="428" height="32" rx="6" fill="none" stroke="{p["border"]}" stroke-width="1"/>')
    s.append(f'<text x="18" y="{c2+20}" class="chip" fill="{p["text"]}">FRAMER TOP 1% CREATOR</text>')
    fy = c2 + 58
    s.append(f'<line x1="6" y1="{fy}" x2="434" y2="{fy}" stroke="{p["rule"]}" stroke-width="1"/>')
    s.append(f'<text x="6" y="{fy+22}" class="ft" fill="{p["dim"]}">DESIGN + DEV BY ME</text>')
    s.append(f'<text x="6" y="{fy+38}" class="ft" fill="{p["dim"]}">{esc("©")} 2026 SWORUP KUMAR BEHURIA</text>')
    H = fy + 50
    return ("\n".join(s) + "\n</svg>").replace('height="600" viewBox="0 0 440 600"',
                                               f'height="{H}" viewBox="0 0 440 {H}"')

# ---------- sponsor banner (same adaptive palette as the profile hero) ----------
SPONSOR_THEME = (
    ':root{--sp-text:#1F2328;--sp-muted:#57606A;--sp-dim:#8C959F;--sp-border:rgba(0,0,0,.16)}'
    '@media (prefers-color-scheme:dark){:root{--sp-text:#EDEDED;--sp-muted:#8A8A8A;'
    '--sp-dim:#5A5A5A;--sp-border:rgba(255,255,255,.14)}}'
)

def _sp_typing(fs, x0, baseline, cid):
    adv = fs * 0.618 + 1
    n = 16  # "SUPPORT THE WORK"
    widths = [round(i * adv) for i in range(n + 1)]
    kt = [round(i / n * 0.40, 4) for i in range(n + 1)]
    wv = ";".join(str(w) for w in widths) + f";{widths[-1]};0"
    kv = ";".join(str(k) for k in kt) + ";0.60;1"
    xv = ";".join(str(x0 + w) for w in widths) + f";{x0 + widths[-1]};{x0}"
    top, h = round(baseline - fs * 0.80), round(fs * 1.05)
    clip = (f'<clipPath id="{cid}"><rect x="{x0-2}" y="{top}" width="0" height="{h}">'
            f'<animate attributeName="width" values="{wv}" keyTimes="{kv}" '
            f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>')
    title = (f'<text x="{x0}" y="{baseline}" clip-path="url(#{cid})" '
             f'style="font-size:{fs}px;letter-spacing:1px" fill="var(--sp-text)">SUPPORT THE WORK</text>')
    cursor = (f'<rect y="{top}" width="2.5" height="{round(fs)}" fill="var(--sp-text)">'
              f'<animate attributeName="x" values="{xv}" keyTimes="{kv}" '
              f'dur="4.5s" calcMode="discrete" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
              f'dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    return clip, title, cursor

def sponsor_banner():          # universal banner used by GitHub on desktop + mobile
    W, x0, PAD, box_top = 840, 34, 56, 8
    lead_b = box_top + PAD + 14        # 18px ascent ~14
    head_b = lead_b + 96
    sub_b = head_b + 78
    box_bottom = sub_b + PAD
    box_h, H = box_bottom - box_top, box_bottom + 8
    clip, title, cursor = _sp_typing(72, x0, head_b, "ts")
    return (
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Support the work">'
        f'<defs><style>{FONT_FACE}{SPONSOR_THEME}text{{font-family:FM,monospace}}</style>{clip}</defs>'
        f'<rect x="8" y="{box_top}" width="824" height="{box_h}" rx="8" fill="none" stroke="var(--sp-border)" stroke-width="1"/>'
        f'<text x="{x0}" y="{lead_b}" style="font-size:18px;letter-spacing:2px" fill="var(--sp-dim)">// INITIALISING SPONSORSHIP</text>'
        f'{title}{cursor}'
        f'<text x="{x0}" y="{sub_b}" style="font-size:20px;letter-spacing:.6px" fill="var(--sp-muted)">'
        f'INDEPENDENT DESIGN + DEV {esc("—")} FUNDED BY PEOPLE WHO USE IT.</text>'
        f'</svg>'
    )

def sponsor_banner_mobile():   # narrow, larger relative text, wrapped subtitle
    W, x0, PAD, box_top = 460, 22, 30, 8
    lead_b = box_top + PAD + 9         # 12px ascent ~9
    head_b = lead_b + 56
    sub_lines = ["INDEPENDENT DESIGN + DEV " + esc("—") + " FUNDED", "BY PEOPLE WHO USE IT."]
    sub_b1 = head_b + 48
    sub_b2 = sub_b1 + 22
    box_bottom = sub_b2 + PAD
    box_h, H = box_bottom - box_top, box_bottom + 8
    clip, title, cursor = _sp_typing(36, x0, head_b, "tsm")
    subs = "".join(
        f'<text x="{x0}" y="{y}" style="font-size:12px;letter-spacing:.4px" fill="var(--sp-muted)">{line}</text>'
        for line, y in [(sub_lines[0], sub_b1), (sub_lines[1], sub_b2)]
    )
    return (
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Support the work">'
        f'<defs><style>{FONT_FACE}{SPONSOR_THEME}text{{font-family:FM,monospace}}</style>{clip}</defs>'
        f'<rect x="6" y="{box_top}" width="448" height="{box_h}" rx="8" fill="none" stroke="var(--sp-border)" stroke-width="1"/>'
        f'<text x="{x0}" y="{lead_b}" style="font-size:12px;letter-spacing:2px" fill="var(--sp-dim)">// INITIALISING SPONSORSHIP</text>'
        f'{title}{cursor}{subs}'
        f'</svg>'
    )

# ---------- README ----------
def readme():
    chips = []
    for key, label, url in SOCIALS:
        chips.append(
            f'<a href="{url}"><picture>'
            f'<source media="(max-width: 768px)" srcset="./assets/soc-{key}-mobile.svg">'
            f'<img src="./assets/soc-{key}.svg" height="42" alt="{esc(label)}">'
            f'</picture></a>'
        )
    chip_row = " ".join(chips)
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
    open(os.path.join(ASSETS, "sponsor-banner.svg"), "w").write(sponsor_banner())
    open(os.path.join(ASSETS, "sponsor-banner-mobile.svg"), "w").write(sponsor_banner_mobile())
    for key, label, _ in SOCIALS:
        open(os.path.join(ASSETS, f"soc-{key}.svg"), "w").write(chip_svg(label))
        mobile_width = 320 if key == "email" else 156
        open(os.path.join(ASSETS, f"soc-{key}-mobile.svg"), "w").write(
            chip_svg(label, width=mobile_width, centered=True)
        )
    open(os.path.join(HERE, "README.md"), "w").write(readme())
    print("built:", sorted(os.listdir(ASSETS)))

if __name__ == "__main__":
    main()
