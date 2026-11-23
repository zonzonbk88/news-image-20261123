#!/usr/bin/env python3
"""Draw the front-page news image for Monday 23 November 2026.

Every story below was reported on 23 November 2026 by major news services
(COP31 collapse, the US House result, the Iran warning, the Kyiv strikes,
Kim Jong Un's statement, the WHO Ebola plea, BepiColombo at Mercury).
The picture is a one-page newspaper: a dated masthead, one lead story,
four grid stories, two short stories and a ticker of the rest of the day.

Run:  python3 draw.py   ->  writes entry.png beside this file.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 30, 43)
WHITE = (255, 255, 255)
RED = (178, 34, 44)
BLUE = (28, 84, 148)
AMBER = (176, 106, 12)
TEAL = (14, 110, 96)
GREY = (84, 96, 108)
PANEL_LINE = (196, 188, 172)

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.12):
    x, y = xy
    step = int(fnt.size * leading)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def fit_font(draw, text, path, size, max_w):
    """Shrink a bold font until the single line fits max_w."""
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


# ---------------------------------------------------------------- icons
# Grid icons are drawn inside a box of half-size 52 around (cx, cy);
# short-panel icons inside a box of half-size 36.
def icon_globe_doc(d, cx, cy):
    """Lead art: globe beside a deal document struck through."""
    r = 74
    d.ellipse([cx - 150, cy - r, cx - 150 + 2 * r, cy + r], fill=(88, 148, 196))
    d.ellipse([cx - 138, cy - 52, cx - 96, cy - 18], fill=(74, 148, 92))
    d.ellipse([cx - 118, cy + 6, cx - 74, cy + 44], fill=(74, 148, 92))
    d.ellipse([cx - 62, cy - 40, cx - 26, cy - 8], fill=(74, 148, 92))
    dx0, dy0, dx1, dy1 = cx + 18, cy - 66, cx + 118, cy + 66
    d.rectangle([dx0, dy0, dx1, dy1], fill=WHITE, outline=INK, width=3)
    for i in range(4):
        ly = dy0 + 22 + i * 24
        d.line([dx0 + 14, ly, dx1 - 14, ly], fill=GREY, width=5)
    d.line([dx0 - 8, dy1 + 8, dx1 + 8, dy0 - 8], fill=RED, width=11)
    d.line([dx0 - 8, dy0 - 8, dx1 + 8, dy1 + 8], fill=RED, width=11)


def icon_capitol(d, cx, cy):
    d.polygon([(cx - 5, cy - 52), (cx + 5, cy - 52), (cx + 3, cy - 40),
               (cx - 3, cy - 40)], fill=INK)
    d.pieslice([cx - 36, cy - 42, cx + 36, cy + 20], 180, 360, fill=BLUE)
    d.rectangle([cx - 46, cy - 10, cx + 46, cy - 3], fill=INK)
    for i in range(5):
        x = cx - 40 + i * 18
        d.rectangle([x, cy, x + 8, cy + 32], fill=INK)
    d.rectangle([cx - 50, cy + 32, cx + 50, cy + 41], fill=INK)


def icon_missile(d, cx, cy):
    d.polygon([(cx + 30, cy - 50), (cx + 46, cy - 20), (cx + 20, cy - 4),
               (cx - 4, cy - 30)], fill=RED)
    d.polygon([(cx - 4, cy - 30), (cx + 20, cy - 4), (cx + 2, cy + 16),
               (cx - 24, cy - 10)], fill=(120, 130, 140))
    d.polygon([(cx - 24, cy - 10), (cx - 42, cy + 18), (cx - 16, cy + 14)],
              fill=AMBER)
    d.polygon([(cx - 16, cy + 14), (cx - 28, cy + 42), (cx - 4, cy + 24)],
              fill=(226, 146, 32))


def icon_burst(d, cx, cy):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = 52 if i % 2 == 0 else 24
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=AMBER)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED)


def icon_quote(d, cx, cy):
    d.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], fill=TEAL)
    fnt = font(SERIF_B, 88)
    w = d.textlength("\u201C", font=fnt)
    d.text((cx - w / 2, cy - 62), "\u201C", font=fnt, fill=WHITE)


def icon_cross(d, cx, cy):
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=RED)
    d.rectangle([cx - 8, cy - 22, cx + 8, cy + 22], fill=WHITE)
    d.rectangle([cx - 22, cy - 8, cx + 22, cy + 8], fill=WHITE)


def icon_planet(d, cx, cy):
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(216, 128, 52))
    d.ellipse([cx - 19, cy - 11, cx - 4, cy + 3], fill=(188, 102, 38))
    d.ellipse([cx + 5, cy + 7, cx + 19, cy + 20], fill=(188, 102, 38))
    d.arc([cx - 48, cy - 16, cx + 48, cy + 18], 200, 330, fill=BLUE, width=4)
    d.rectangle([cx + 20, cy - 40, cx + 31, cy - 29], fill=INK)
    d.rectangle([cx + 34, cy - 43, cx + 51, cy - 27], fill=BLUE)
    d.rectangle([cx + 3, cy - 43, cx + 17, cy - 27], fill=BLUE)


ICON = {
    "capitol": icon_capitol,
    "missile": icon_missile,
    "burst": icon_burst,
    "quote": icon_quote,
    "cross": icon_cross,
    "planet": icon_planet,
}


# ---------------------------------------------------------------- panels
def panel(d, box, chip_color, chip_text, icon, headline, sub,
          head_size=26, sub_size=20):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE, outline=PANEL_LINE, width=2)
    d.rectangle([x0, y0, x1, y0 + 38], fill=chip_color)
    d.text((x0 + 14, y0 + 7), chip_text, font=font(SANS_B, 21), fill=WHITE)
    ICON[icon](d, x0 + 62, (y0 + 42 + y1) // 2)
    tx = x0 + 124
    y = text_block(d, (tx, y0 + 48), headline, font(SANS_B, head_size),
                   INK, x1 - tx - 12)
    text_block(d, (tx, y + 3), sub, font(SANS_R, sub_size), GREY,
               x1 - tx - 12)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0-140) ------------------------------------------------
    d.rectangle([0, 0, W, 140], fill=INK)
    centered(d, W // 2, 12, "T H E   W O R L D   I N   O N E   D A Y",
             font(SANS_B, 23), (170, 196, 220))
    centered(d, W // 2, 42, "MONDAY 23 NOVEMBER 2026", font(SANS_B, 57), WHITE)
    centered(d, W // 2, 108, "The day's biggest stories, on one page",
             font(SANS_R, 19), (170, 196, 220))
    d.rectangle([0, 140, W, 146], fill=RED)

    # ---- lead story: COP31 (158-446) --------------------------------------
    d.rectangle([28, 158, 996, 446], fill=WHITE, outline=PANEL_LINE, width=2)
    d.rectangle([28, 158, 996, 198], fill=RED)
    d.text((42, 166), "LEAD STORY \u00b7 CLIMATE SUMMIT \u00b7 T\u00dcRK\u0130YE",
           font=font(SANS_B, 23), fill=WHITE)
    icon_globe_doc(d, 196, 306)
    y = text_block(d, (392, 216), "COP31 climate talks collapse without a deal",
                   font(SANS_B, 43), INK, 576)
    text_block(d, (392, y + 8),
               "Nearly 200 nations end the UN summit in T\u00fcrkiye with no "
               "agreement, after the EU rejects a draft that drops the "
               "fossil-fuel phase-out.",
               font(SANS_R, 24), GREY, 576)

    # ---- grid stories (458-806) -------------------------------------------
    panel(d, (28, 458, 500, 626), BLUE, "US POLITICS", "capitol",
          "Democrats clinch a historic House majority",
          "At least 258 seats \u2014 the largest since 1992.")
    panel(d, (524, 458, 996, 626), RED, "MIDDLE EAST", "missile",
          "Trump warns Iran: deal, or new strikes",
          "He says he is 'inclined' to resume attacks if talks stall.")
    panel(d, (28, 638, 500, 806), AMBER, "WAR IN UKRAINE", "burst",
          "Russian strikes kill 11 in the Kyiv region",
          "Missiles inside Polish airspace; NATO holds emergency talks.")
    panel(d, (524, 638, 996, 806), TEAL, "ASIA \u00b7 NORTH KOREA", "quote",
          "Kim: North seeks 'security, not supremacy'",
          "Kim Jong Un says Pyongyang arms for security, not dominance.")

    # ---- short stories (818-946) ------------------------------------------
    panel(d, (28, 818, 500, 946), RED, "HEALTH \u00b7 AFRICA", "cross",
          "WHO chief pleads for peace in Ebola-hit DR Congo",
          "Fighting disrupts the Ebola response.",
          head_size=23, sub_size=19)
    panel(d, (524, 818, 996, 946), BLUE, "SCIENCE \u00b7 SPACE", "planet",
          "BepiColombo spacecraft reaches Mercury",
          "ESA and JAXA's joint mission arrives.",
          head_size=23, sub_size=19)

    # ---- ticker (958-1024) --------------------------------------------------
    d.rectangle([0, 958, W, 1024], fill=INK)
    line1 = ("ISRAEL: NETANYAHU\u2013EISENKOT TALKS END WITHOUT A DEAL  \u00b7  "
             "NIGERIA: 24 DEAD IN BOAT ACCIDENT")
    line2 = ("INDONESIA FACTORY FIRE: 3 DEAD, 36 MISSING  \u00b7  CHESS: GUKESH "
             "OPENS WORLD TITLE DEFENCE")
    centered(d, W // 2, 966, line1, fit_font(d, line1, SANS_B, 19, 1000), WHITE)
    centered(d, W // 2, 992, line2, fit_font(d, line2, SANS_B, 19, 1000),
             (170, 196, 220))

    out = HERE / "entry.png"
    img.save(out, optimize=True)
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
