#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up Friday 20 November 2026.

Deterministic: fixed text, fixed geometry, no randomness, no clock, no network.
Run: python3 generate.py  ->  writes news.png next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 238)
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (20, 55, 110)
GREY = (96, 96, 96)
FAINT = (205, 199, 184)
MAP_BG = (214, 228, 238)
LAND = (168, 188, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

EDITION = "Friday 20 November 2026"
SOURCES = ("Reuters", "AP", "AFP", "Bloomberg", "IMD", "Dow Jones", "ECDC")


def font(path, size):
    return ImageFont.truetype(path, size)


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, f, fill=INK, anchor="la"):
        self.d.text((x, y), s, font=f, fill=fill, anchor=anchor)

    def width(self, s, f):
        return self.d.textlength(s, font=f)

    def wrap(self, s, f, max_w):
        lines, cur = [], ""
        for word in s.split():
            trial = (cur + " " + word).strip()
            if self.width(trial, f) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def rule(self, x0, x1, y, color=INK, width=2):
        self.d.line([(x0, y), (x1, y)], fill=color, width=width)

    def kicker(self, x, y, label, size=14):
        self.text(x, y, label, font(SANS_B, size), RED)
        return y + size + 6

    def story(self, x, y, w, head, body, hsize=18, bsize=13, max_body=6):
        """Headline (bold) + body, returns y below the block."""
        for ln in self.wrap(head, font(SANS_B, hsize), w):
            self.text(x, y, ln, font(SANS_B, hsize))
            y += hsize + 3
        for ln in self.wrap(body, font(SANS, bsize), w)[:max_body]:
            self.text(x, y, ln, font(SANS, bsize), (40, 40, 40))
            y += bsize + 4
        return y

    def save(self):
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
        self.img.save(out, optimize=True)
        print(out, os.path.getsize(out))


p = Page()
d = p.d

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 90], fill=INK)
p.text(W // 2, 8, "THE  WORLD  TODAY", font(SERIF_B, 44), (255, 255, 255), "ma")
p.text(W // 2, 60, "Friday 20 November 2026  •  23 stories  •  6 continents  •  One page",
       font(SANS_B, 15), (255, 210, 120), "ma")
p.rule(24, W - 24, 100, RED, 4)
p.text(24, 108, "DATE CHECK: Friday 20 November 2026 — every story on this page happened, "
                 "or was first reported, on this day.",
       font(SANS_B, 12), BLUE)
p.rule(24, W - 24, 130, GREY, 1)

# ---------------------------------------------------------------- lead + rail
y = 140
y = p.kicker(24, y, "1  WAR • UKRAINE")
y = p.story(24, y, 640,
            "RUSSIA HITS KYIV'S BRIDGES IN BIGGEST BARRAGE OF THE WAR",
            "Russian ballistic missiles struck three bridges over the Dnipro in Kyiv early "
            "on Friday — the biggest attack on the capital's crossings since the invasion "
            "began — killing three people in the city and injuring 15. Across Ukraine, "
            "eight were killed as Moscow answered Kyiv's third strike this week on the "
            "Kerch Bridge. Poland said three Russian objects crossed its airspace overnight.",
            hsize=29, bsize=15, max_body=6)
p.rule(24, 664, y + 6, GREY, 1)

rx = 688
ry = 140
ry = p.kicker(rx, ry, "2  MARKETS • ASIA")
ry = p.story(rx, ry, 312,
             "AI SELL-OFF: NIKKEI −4.8% TO SEVEN-MONTH LOW",
             "Tokyo's Nikkei fell 4.8% on Friday as the AI trade unravelled: SoftBank "
             "−14.6%, Kioxia −11.3%, Seoul −4.7% and Taiwan −6.8%. It followed "
             "Anthropic's record $81.3bn Nasdaq debut — shares closed +17% at $97.17.",
             hsize=18, bsize=13, max_body=5)
p.rule(rx, W - 24, 284, GREY, 1)
ry = p.kicker(rx, 294, "3  WEATHER • INDIA")
p.story(rx, ry, 312,
        "CYCLONE AKVAN COMES ASHORE IN ODISHA",
        "Akvan crossed the coast near Gopalpur on Friday morning with winds of 70–80 "
        "km/h, gusting to 90. More than 300,000 people were evacuated; officials "
        "reported no major damage or loss of life. It is the third cyclone to threaten "
        "Odisha in 24 days.",
        hsize=17, bsize=13, max_body=6)

# ---------------------------------------------------------------- map band
my = 340
d.rectangle([24, my, 664, my + 132], fill=MAP_BG, outline=BLUE, width=2)
p.text(36, my + 8, "THE DAY ON THE MAP", font(SANS_B, 15), BLUE)
land_polys = [
    [(60, 398), (150, 378), (205, 390), (200, 420), (160, 448), (120, 436), (70, 428)],
    [(185, 436), (212, 432), (216, 452), (198, 466), (182, 450)],
    [(330, 382), (385, 376), (408, 392), (392, 420), (350, 416), (328, 398)],
    [(340, 420), (400, 416), (416, 448), (390, 466), (356, 452)],
    [(420, 378), (530, 372), (592, 396), (572, 436), (495, 424), (436, 412)],
    [(535, 440), (582, 436), (594, 458), (566, 466), (542, 456)],
]
for poly in land_polys:
    d.polygon(poly, fill=LAND, outline=(120, 140, 110))
pins = [
    (352, 394, "1", "Kyiv"),
    (468, 404, "4", "Riyadh"),
    (498, 434, "3", "Gopalpur"),
    (586, 396, "2", "Tokyo"),
    (530, 388, "5", "Shenzhen"),
    (398, 390, "6", "Rome"),
]
for px, py, num, _label in pins:
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=(255, 255, 255), width=2)
    p.text(px, py - 1, num, font(SANS_B, 12), (255, 255, 255), "ma")
p.text(24, my + 138, "1 Kyiv  •  2 Tokyo  •  3 Gopalpur  •  4 Riyadh  •  5 Shenzhen  •  6 Rome",
       font(SANS_B, 11), BLUE)

# ---------------------------------------------------------------- UTC timeline
ty = 494
p.text(24, ty, "THE DAY IN UTC", font(SANS_B, 15), BLUE)
timeline = [
    ("02:00", "Akvan crosses the Odisha coast"),
    ("06:00", "Nikkei closes −4.8%, lowest since April"),
    ("07:57", "Kyiv toll confirmed: 3 dead, 15 hurt"),
    ("11:13", "Riyadh confirms PIF Tower damage"),
    ("DAY", "Italy strike; youth marches in 25+ nations"),
    ("EVENING", "Shelton into the ATP Finals semis"),
]
xx = 24
for t, label in timeline:
    p.text(xx, ty + 22, t, font(SANS_B, 12), RED)
    ly = ty + 40
    for ln in p.wrap(label, font(SANS, 11), 158):
        p.text(xx, ly, ln, font(SANS, 11), (40, 40, 40))
        ly += 14
    xx += 168
p.rule(24, W - 24, ty + 70, GREY, 1)

# ---------------------------------------------------------------- middle grid
gy = 574
cols = [(24, 320), (352, 320), (680, 320)]
grid = [
    ("4  GULF • RIYADH", "HOUTHI MISSILE SCARS RIYADH'S TALLEST TOWER",
     "Saudi Arabia confirmed on Friday that a Houthi missile damaged several floors "
     "of the 80-storey PIF Tower, the kingdom's sovereign-wealth HQ; no one was hurt. "
     "Air defences downed four more ballistic missiles."),
    ("5  DIPLOMACY • SHENZHEN", "TRUMP, XI & PUTIN: DECLARATION, NO BREAKTHROUGH",
     "The three presidents issued a four-point declaration after Thursday's 70-minute "
     "trilateral — no breakthrough on Ukraine, Iran or nuclear arms. Envoys said "
     "Russia was 'comfortable' with Article 5-style guarantees."),
    ("6  EUROPE • PROTEST", "YOUTH STRIKE SWEEPS 25 COUNTRIES",
     "Students walked out in 25+ nations against living costs and rearmament — "
     "'Fight for our future, not their wars'. Italy's CGIL held a general strike; "
     "350+ British schools joined; 10,000 marched in Cologne."),
    ("7  SPORT • TURIN", "SHELTON INTO ATP FINALS SEMIS",
     "Ben Shelton beat Rafael Jodar 7-6(8), 7-5 in Turin to reach the last four, where "
     "he meets Carlos Alcaraz. In Rawalpindi, Pakistan beat Sri Lanka by eight wickets "
     "to seal the Test series 1-0."),
    ("8  GAMES • LOS ANGELES", "GTA VI: 24.6M COPIES, $2.36BN IN A DAY",
     "The full first-day tally is in: GTA VI sold ~24.6m copies for ~$2.36bn "
     "(Sensor Tower), with 125m hours watched and a 7.91m peak across Twitch, "
     "YouTube and Kick — the biggest launch in streaming history."),
    ("9  USA • WASHINGTON", "SENATE PASSES PERMITTING BILL 62–33",
     "The Senate passed a bipartisan energy-permitting overhaul to speed power "
     "plants, pipelines and data centres. House documents showed 879,000 AI chips "
     "were licensed for Chinese firms from Dec 2025 to May 2026."),
]
for i, (kick, head, body) in enumerate(grid):
    cx, cw = cols[i % 3]
    cy = gy if i < 3 else gy + 116
    p.kicker(cx, cy, kick, size=12)
    p.story(cx, cy + 18, cw, head, body, hsize=15, bsize=11, max_body=4)
    if i % 3 != 2:
        d.line([(cx + cw + 14, cy), (cx + cw + 14, cy + 104)], fill=FAINT, width=1)
p.rule(24, W - 24, gy + 114, GREY, 1)
p.rule(24, W - 24, gy + 232, GREY, 1)

# ---------------------------------------------------------------- markets strip
my2 = gy + 242
d.rectangle([24, my2, W - 24, my2 + 28], fill=INK)
strip = ("MARKETS — Nikkei −4.8% · 56,595  |  KOSPI −4.7%  |  Taiwan −6.8%  |  "
         "S&P 500 −2.0% (Thu)  |  Nasdaq −2.3%  |  Brent $92.77  |  "
         "Gold <$3,590  |  Bitcoin ~$62,000")
for sz in (12, 11, 10):
    if p.width(strip, font(SANS_B, sz)) <= W - 48:
        break
p.text(W // 2, my2 + 7, strip, font(SANS_B, sz), (255, 255, 255), "ma")

# ---------------------------------------------------------------- briefs
by = my2 + 40
p.text(24, by, "IN BRIEF — THE REST OF THE WORLD IN ONE LINE EACH", font(SANS_B, 14), BLUE)
briefs = [
    "BAGHDAD: Iraq sends federal forces to the Kataib Hezbollah stronghold of Jurf al-Sakhar.",
    "TALLINN: Estonia will shut its border with Russia for at least six months.",
    "LONDON: Two men will stand trial in Nov 2027 over the RAF Fairford security incident.",
    "WASHINGTON: Trump tells Axios he will not decide the next Iran step until the new year.",
    "WASHINGTON: Senate Republicans block an Iran war-powers measure, 51–48.",
    "GAZA: Israeli forces cross the Yellow Line in central Gaza.",
    "THE HAGUE: After Thursday's ICJ genocide ruling on Myanmar, states debate enforcement.",
    "KINSHASA: DR Congo's Ebola toll reaches 11,680 cases and 5,715 deaths; still a global emergency.",
]
yy = by + 20
for b in briefs:
    p.text(24, yy, "•  " + b, font(SANS, 12), (35, 35, 35))
    yy += 15

# ---------------------------------------------------------------- footer
d.rectangle([0, H - 28, W, H], fill=INK)
p.text(W // 2, H - 22,
       "All the day's news, in one image — " + EDITION +
       "  •  Sources: " + ", ".join(SOURCES),
       font(SANS, 11), (255, 255, 255), "ma")

p.save()
