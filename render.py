#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news infographic (1024x1024 PNG).

Programmatic flat-design poster: a masthead with the date, then six story
cards, each with a small hand-drawn icon, a region/field kicker, a bold
headline and one faithful sub-line. No external assets, no network.
Run:  python3 render.py   (writes entry.png next to this script)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (26, 35, 50)
NAVY = (20, 33, 61)
GRAY = (90, 96, 110)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
RED = (192, 57, 43)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_TITLE = font("DejaVuSans-Bold.ttf", 76)
F_SUB = font("DejaVuSans-Bold.ttf", 27)
F_KICK = font("DejaVuSans-Bold.ttf", 21)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 18)

# (kicker, accent, headline, sub-line, icon key)
STORIES = [
    ("UKRAINE  ·  WAR", (192, 57, 43),
     "Kerch Bridge hit again — span collapses",
     "Ukraine hits the Crimea link again; a span falls.",
     "bridge"),
    ("MIDDLE EAST  ·  WAR", (211, 84, 0),
     "Iran drones target US radar base in Bahrain",
     "Third attack in days; intercepted, no casualties.",
     "radar"),
    ("ASIA-PACIFIC  ·  DIPLOMACY", (14, 124, 123),
     "Trump lands in Manila for ASEAN summit",
     "Xi–Trump–Putin three-way set for Thursday.",
     "globe"),
    ("EUROPE  ·  SECURITY", (108, 52, 131),
     "Estonia to shut its border with Russia",
     "Crossings close 1 Dec after a foiled sabotage plot.",
     "barrier"),
    ("TECHNOLOGY", (36, 113, 163),
     "OpenAI launches GPT-6.2 as Ignite opens",
     "New Astra and Sol models; Microsoft's Ignite opens.",
     "chip"),
    ("MARKETS", (30, 132, 73),
     "Nvidia reports first earnings since Huang exit",
     "Results after Tuesday's close; AI demand in focus.",
     "chart"),
]


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_bridge(d, x, y, s, c):
    # Two towers, a deck with a broken gap, suspension cables.
    d.line([(x, y + 62), (x + s, y + 62)], fill=c, width=7)
    d.line([(x + 8, y + 10), (x + 8, y + 62)], fill=c, width=7)
    d.line([(x + s - 8, y + 10), (x + s - 8, y + 62)], fill=c, width=7)
    d.line([(x + 8, y + 10), (x + s // 2 - 14, y + 62)], fill=c, width=3)
    d.line([(x + s - 8, y + 10), (x + s // 2 + 14, y + 62)], fill=c, width=3)
    # broken gap in the deck
    d.line([(x + s // 2 - 14, y + 62), (x + s // 2 - 4, y + 78)], fill=c, width=5)
    d.line([(x + s // 2 + 14, y + 62), (x + s // 2 + 4, y + 78)], fill=c, width=5)
    d.line([(x + s // 2 - 14, y + 62), (x + s // 2 - 4, y + 78)], fill=RED, width=5)


def draw_radar(d, x, y, s, c):
    cx, cy, r = x + s // 2, y + s // 2 + 6, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=6)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], start=300, end=360,
               fill=c)
    d.line([(cx, cy), (cx + r - 4, cy - r + 8)], fill=c, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=c)
    for rr in (48, 58):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=300, end=60,
              fill=c, width=4)


def draw_globe(d, x, y, s, c):
    cx, cy, r = x + s // 2, y + s // 2, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=6)
    d.ellipse([cx - 14, cy - r, cx + 14, cy + r], outline=c, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=c, width=3)
    d.arc([cx - r, cy - 20, cx + r, cy + 20], start=0, end=360,
          fill=c, width=3)
    d.ellipse([cx + 12, cy - 26, cx + 20, cy - 18], fill=RED)


def draw_barrier(d, x, y, s, c):
    # Striped road barrier on two posts.
    for i in range(5):
        x0 = x + 6 + i * 16
        d.polygon([(x0, y + 18), (x0 + 10, y + 18), (x0 + 2, y + 46),
                   (x0 - 8, y + 46)], fill=RED if i % 2 == 0 else c)
    d.rectangle([x + 2, y + 14, x + s - 2, y + 50], outline=c, width=5)
    d.line([(x + 14, y + 50), (x + 14, y + 78)], fill=c, width=7)
    d.line([(x + s - 14, y + 50), (x + s - 14, y + 78)], fill=c, width=7)


def draw_chip(d, x, y, s, c):
    d.rounded_rectangle([x + 16, y + 16, x + s - 16, y + s - 16],
                        radius=8, outline=c, width=6)
    d.rounded_rectangle([x + 32, y + 32, x + s - 32, y + s - 32],
                        radius=4, fill=c)
    for i in range(3):
        px = x + 30 + i * 18
        d.line([(px, y + 4), (px, y + 16)], fill=c, width=5)
        d.line([(px, y + s - 16), (px, y + s - 4)], fill=c, width=5)
        d.line([(x + 4, y + 30 + i * 18), (x + 16, y + 30 + i * 18)],
               fill=c, width=5)
        d.line([(x + s - 16, y + 30 + i * 18), (x + s - 4, y + 30 + i * 18)],
               fill=c, width=5)


def draw_chart(d, x, y, s, c):
    d.line([(x + 8, y + 8), (x + 8, y + s - 8)], fill=c, width=5)
    d.line([(x + 8, y + s - 8), (x + s - 4, y + s - 8)], fill=c, width=5)
    bars = [(20, 26), (42, 42), (64, 58)]
    for bx, bh in bars:
        d.rectangle([x + bx, y + s - 14 - bh, x + bx + 14, y + s - 14],
                    fill=c)
    d.line([(x + 14, y + 52), (x + 34, y + 34), (x + 56, y + 22),
            (x + s - 8, y + 10)], fill=RED, width=5)
    d.polygon([(x + s - 8, y + 10), (x + s - 20, y + 8),
               (x + s - 14, y + 20)], fill=RED)


ICONS = {"bridge": draw_bridge, "radar": draw_radar, "globe": draw_globe,
         "barrier": draw_barrier, "chip": draw_chip, "chart": draw_chart}


def draw_card(d, x, y, w, h, story):
    kicker, accent, headline, sub, icon = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.rounded_rectangle([x, y, x + 10, y + h], radius=5, fill=accent)
    d.text((x + 26, y + 16), kicker, font=F_KICK, fill=accent)
    ICONS[icon](d, x + 26, y + 62, 92, accent)
    tx = x + 140
    tw = w - 140 - 22
    lines = wrap(headline, F_HEAD, tw)[:3]
    ly = y + 52
    for ln in lines:
        d.text((tx, ly), ln, font=F_HEAD, fill=INK)
        ly += 34
    slines = wrap(sub, F_BODY, tw)[:2]
    ly = y + 162
    for ln in slines:
        d.text((tx, ly), ln, font=F_BODY, fill=GRAY)
        ly += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 176], fill=NAVY)
    d.rectangle([0, 176, W, 182], fill=RED)
    title = "17 NOVEMBER 2026"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 28), title, font=F_TITLE, fill=(255, 255, 255))
    sub = "TUESDAY  ·  THE WORLD'S NEWS IN ONE IMAGE"
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 122), sub, font=F_SUB, fill=(196, 205, 224))
    # Story grid: 2 cols x 3 rows
    cw, ch, gx, gy = 488, 240, 16, 16
    for i, story in enumerate(STORIES):
        cx = 16 + (i % 2) * (cw + gx)
        cy = 200 + (i // 2) * (ch + gy)
        draw_card(d, cx, cy, cw, ch, story)
    # Footer
    foot = ("As reported on 17 November 2026  ·  Sources: BBC, Al Jazeera, "
            "AP, Reuters, NPR")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 968), foot, font=F_FOOT, fill=GRAY)
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
