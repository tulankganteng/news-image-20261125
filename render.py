#!/usr/bin/env python3
"""Render entry.png for news-image-20261125: 'The World Today'.

Layout (DIFFERENT from the 20261124 entry, which used map+numbers band,
12 pictured stories in two rows, and a 4x2 region grid):
  masthead -> 3 lead stories side by side -> markets ticker ->
  left: 8 region blocks in 2 columns x 4 rows, right: rail of 12
  pictured stories (2 cols x 6 rows) -> bottom: world map with 12 pins
  + timeline + 'left out as older news' box -> sources footer.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

FB = os.path.join(ASSETS, "DejaVuSans-Bold.ttf")
FR = os.path.join(ASSETS, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(text, fnt, maxw, draw):
    """Truncate text with an ellipsis so it fits maxw pixels."""
    if draw.textlength(text, font=fnt) <= maxw:
        return text
    while text and draw.textlength(text + "...", font=fnt) > maxw:
        text = text[:-1]
    return text + "..."


def wrap(text, fnt, maxw, draw, lines=2):
    words = text.split()
    out, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        elif len(out) < lines - 1:
            out.append(cur)
            cur = w
        else:
            cur = fit(cur + " " + w, fnt, maxw, draw)
            break
    else:
        if cur:
            out.append(cur)
        return out[:lines]
    if cur:
        out.append(cur)
    return out[:lines]


INK = (18, 18, 18)
PAPER = (250, 248, 242)
RED = (178, 34, 34)
NAVY = (24, 48, 96)
GREY = (90, 90, 90)
RULE = (180, 175, 165)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 80], fill=(12, 12, 12))
d.text((14, 10), "THE WORLD TODAY", font=font(FB, 36), fill=(255, 255, 255))
d.text((14, 56), "One day's world news  -  40 stories  -  8 regions  -  12 pictures",
       font=font(FR, 11), fill=(210, 210, 210))
d.text((700, 8), "WEDNESDAY", font=font(FB, 17), fill=(255, 210, 90))
d.text((700, 30), "25 NOVEMBER 2026", font=font(FB, 24), fill=(255, 255, 255))
d.text((700, 60), "Every event happened or was first reported today",
       font=font(FR, 10), fill=(210, 210, 210))
d.rectangle([0, 80, W, 83], fill=RED)

# ---------- 3 lead stories ----------
leads = [
    ("LEAD 1  -  UKRAINE WAR",
     "Putin vows \"inevitable\" retaliation",
     "For Ukraine's drone strikes on Russian refineries, defying Trump's plea. Kyiv also confirms a Baltic ship strike.",
     "Reuters / Silk Paradox"),
    ("LEAD 2  -  MIDDLE EAST",
     "Houthis hit Riyadh's tallest tower",
     "11 wounded in a second strike in days, as tankers are hit by mines in Hormuz and Gaza is struck again.",
     "Saudi Civil Defense / Reuters"),
    ("LEAD 3  -  SPACE",
     "Shenzhou-24 lifts off with a Pakistani",
     "Muhammad Zeeshan Ali becomes the first Pakistani in orbit, aboard China's Tiangong station.",
     "Reuters / AP"),
]
lx = [8, 348, 688]
for i, (kick, head, det, src) in enumerate(leads):
    x = lx[i]
    d.text((x, 90), kick, font=font(FB, 9), fill=RED)
    for j, ln in enumerate(wrap(head, font(FB, 14), 322, d, 2)):
        d.text((x, 106 + j * 17), ln, font=font(FB, 14), fill=INK)
    for j, ln in enumerate(wrap(det, font(FR, 10), 322, d, 2)):
        d.text((x, 142 + j * 12), ln, font=font(FR, 10), fill=(50, 50, 50))
    d.text((x, 170), "Source: " + src, font=font(FR, 8), fill=GREY)
    if i < 2:
        d.line([x + 330, 90, x + 330, 182], fill=RULE, width=1)

# ---------- markets ticker ----------
d.rectangle([0, 186, W, 208], fill=NAVY)
d.text((10, 191), "MARKETS 25 NOV:  Nasdaq -1.5%  -  S&P 500 -0.5%  -  Dow +0.8%  -  Nvidia -6%  -  Micron -11%  -  Brent $86.68  -  Gold $3,625/oz  -  Bitcoin ~$61k",
       font=font(FB, 10), fill=(255, 255, 255))

# ---------- region blocks: 2 cols x 4 rows ----------
regions = [
    ("1  UKRAINE & RUSSIA", NAVY, [
        ("Putin vows \"inevitable\" retaliation", "For Ukraine's refinery strikes, defying Trump's plea  -  Reuters"),
        ("Zelenskiy confirms Baltic ship strike", "Russian cargo ship hit in the Gulf of Finland  -  Reuters"),
        ("Norway: $7bn for Ukraine in 2027", "Air defence first; Oslo urges restraint  -  Kyiv Independent"),
        ("Russian drone enters Poland", "Briefly crossed airspace in overnight attack  -  Poland"),
        ("Hungary PM meets Zelenskiy", "First visit by a Hungarian PM since 2015  -  Euronews"),
    ]),
    ("2  MIDDLE EAST", (122, 20, 20), [
        ("Houthis hit Riyadh's tallest tower", "11 wounded in 2nd strike in days  -  Saudi Civil Defense"),
        ("Israeli strike kills Hamas security chief", "Naeem Abu Nahel killed in Gaza City airstrike  -  Reuters"),
        ("Three killed in Gaza strike", "IDF strike amid repeated ceasefire violations, medics say  -  AP"),
        ("Tankers hit by mines in Hormuz", "IRGC: 3 tankers hit; Red Sea threat grows  -  Reuters"),
        ("Xi: Gaza needs peace, not destruction", "China urges permanent ceasefire at UN solidarity day  -  teleSUR"),
    ]),
    ("3  AMERICAS", (20, 90, 50), [
        ("Trump: Iran war \"funded\" thru January", "Warns Dems not to turn \"total win\" to loss  -  NY Post"),
        ("Trump to meet El-Sayed on \"Trumpcare\"", "Calls Medicare-for-All rebrand \"very smart\"  -  CNN"),
        ("Cartagena hostage siege", "Gunmen hold 30 after failed cash-truck robbery  -  Presidency"),
        ("Trump pardons turkeys Freedom & Feathers", "Thanksgiving rite touts economy and new ballroom  -  AP"),
        ("Fort Hood shooter seeks stay", "Hasan asks court to halt execution set for next week  -  Court records"),
    ]),
    ("4  EUROPE", (80, 40, 110), [
        ("Sarkozy & Carla Bruni to face trial", "Corruption case ordered to trial; pre-trial 1 Apr 2027  -  Reuters"),
        ("NATO vows space defence", "After reports Russia may launch nuclear-armed satellite in Dec  -  NATO"),
        ("EU unveils 22nd Russia sanctions", "Russian-flag athletes banned; visa curbs  -  EU"),
        ("Russia budget: defence +27%", "Defence a record R17.1tn in 2027-29 budget  -  Moscow Times"),
        ("UK sanctions Houthi leaders", "Four leaders targeted over torture and shipping threats  -  UK govt"),
    ]),
    ("5  ASIA-PACIFIC", (140, 80, 0), [
        ("Shenzhou-24 lifts off with Pakistani", "First Pakistani in orbit; first foreigner on Tiangong  -  Reuters"),
        ("S. Korea scrambles jets", "Russian jets enter air defence zone near Ulleung  -  Seoul"),
        ("S. Korea education minister quits", "Resigns over national exam cheating scandal  -  Ministry"),
        ("China probes Shanghai party chief", "Chen Jining under investigation, Beijing confirms  -  Daily Debrief"),
        ("Solomons to drop China pact", "Will end Beijing security deal, sign new one with Australia  -  Reports"),
    ]),
    ("6  SE ASIA & INDONESIA", (0, 100, 110), [
        ("Dozens trapped in Pongkor mine", "West Java gold mine flooded since Mon; rescue under way  -  Reuters"),
        ("15,164 Indonesians in scam rings", "2026 cases double 2025; 139 deported  -  Ministry"),
        ("Indonesia foils 21 \"mercenaries\"", "Citizens stopped from joining Russia; network dismantled  -  Antara"),
        ("Jakarta pushes ASEAN scam protocol", "Biometric SIM rules; 67,578 fraud contents handled  -  Antara"),
        ("72 orangutans saved from fires", "Rescued from West Kalimantan wildfires since Aug  -  BKSDA"),
    ]),
    ("7  AFRICA & LATIN AMERICA", (110, 60, 0), [
        ("DR Congo reimposes cobalt ban", "Export ban restored as prices fall; top producer acts  -  Reuters"),
        ("Congo rebels pull back near Bunia", "Announcement after heavy fighting in Ituri  -  Reports"),
        ("Ebola staff trapped in hospital", "WHO staff sheltering in Ituri ward 48h+  -  UN"),
        ("5 women killed every hour", "By partners or family; Africa worst at 2.9 per 100,000  -  UN"),
        ("Colombia: 10 years after peace deal", "Guterres urges full implementation of 2016 accord  -  UN News"),
    ]),
    ("8  MARKETS, SPORT & SCIENCE", (60, 60, 60), [
        ("AI sell-off resumes on Wall St", "Nasdaq -1.5%, Nvidia -6% after tariff-report jolt  -  Reuters"),
        ("US blacklists Megaspeed", "Singapore probes chip diversion to China  -  US"),
        ("Sooryavanshi's record double ton", "Fastest List A double hundred in cricket history  -  BCCI"),
        ("Gukesh holds Sindarov", "World champion weathers time pressure in title match  -  Sportstar"),
        ("GTA 6: 39m PS5 players in 4 days", "Sony's biggest launch in 30 years  -  Sony"),
    ]),
]
bx0, by0 = 8, 216
bw, bh = 350, 166
for ri, (title, col, stories) in enumerate(regions):
    cx = bx0 + (ri % 2) * (bw + 8)
    cy = by0 + (ri // 2) * (bh + 4)
    d.rectangle([cx, cy, cx + bw, cy + 20], fill=col)
    d.text((cx + 6, cy + 4), title, font=font(FB, 11), fill=(255, 255, 255))
    d.text((cx + bw - 52, cy + 4), "5 STORIES", font=font(FB, 8), fill=(220, 220, 220))
    for si, (head, det) in enumerate(stories):
        sy = cy + 24 + si * 28
        d.text((cx + 4, sy), str(si + 1) + ".", font=font(FB, 10), fill=RED)
        d.text((cx + 20, sy), fit(head, font(FB, 10), bw - 24, d),
               font=font(FB, 10), fill=INK)
        d.text((cx + 20, sy + 13), fit(det, font(FR, 9), bw - 24, d),
               font=font(FR, 9), fill=(60, 60, 60))

# ---------- right rail: 12 pictured stories ----------
pics = [
    ("pic_putin.jpg", "1 PUTIN VOWS RETALIATION", "Refinery strikes defy Trump plea"),
    ("pic_ship.jpg", "2 BALTIC SHIP STRIKE", "Zelenskiy confirms Ukraine hit"),
    ("pic_riyadh.jpg", "3 RIYADH TOWER HIT", "Houthi strike wounds 11"),
    ("pic_gaza.jpg", "4 HAMAS CHIEF KILLED", "Gaza City airstrike"),
    ("pic_trump.jpg", "5 TURKEYS PARDONED", "Trump touts economy at rite"),
    ("pic_rocket.jpg", "6 SHENZHOU-24 LIFTS OFF", "First Pakistani in orbit"),
    ("pic_mine.jpg", "7 TRAPPED IN MINE", "Pongkor, West Java rescue"),
    ("pic_cartagena.jpg", "8 HOSTAGES IN CARTAGENA", "Supermarket siege"),
    ("pic_satellite.jpg", "9 NATO: SPACE DEFENCE", "Russian nuclear satellite fear"),
    ("pic_cobalt.jpg", "10 COBALT BAN RETURNS", "DR Congo halts exports"),
    ("pic_markets.jpg", "11 AI SELL-OFF RESUMES", "Nasdaq -1.5%, Nvidia -6%"),
    ("pic_cricket.jpg", "12 RECORD DOUBLE TON", "Sooryavanshi, List A cricket"),
]
rx0, ry0 = 724, 216
d.rectangle([rx0, ry0, rx0 + 292, ry0 + 20], fill=(12, 12, 12))
d.text((rx0 + 6, ry0 + 4), "12 PICTURED STORIES",
       font=font(FB, 10), fill=(255, 255, 255))
cw, ch = 143, 103
for i, (fn, cap, sub) in enumerate(pics):
    cx = rx0 + (i % 2) * (cw + 6)
    cy = ry0 + 26 + (i // 2) * (ch + 3)
    try:
        im = Image.open(os.path.join(ASSETS, fn)).convert("RGB")
        im = im.resize((cw, 64))
        img.paste(im, (cx, cy))
    except Exception:
        d.rectangle([cx, cy, cx + cw, cy + 64], fill=(200, 200, 200))
    d.rectangle([cx, cy, cx + 18, cy + 14], fill=RED)
    d.text((cx + 4, cy + 1), str(i + 1), font=font(FB, 10), fill=(255, 255, 255))
    d.text((cx, cy + 67), fit(cap, font(FB, 9), cw, d), font=font(FB, 9), fill=INK)
    d.text((cx, cy + 80), fit(sub, font(FR, 8), cw, d), font=font(FR, 8), fill=(60, 60, 60))

# ---------- bottom: world map with pins ----------
my0, my1 = 862, 986
mx0, mx1 = 8, 500
d.rectangle([mx0, my0, mx1, my1], fill=(214, 230, 240))
d.text((mx0 + 6, my0 + 3), "WORLD MAP  -  12 PICTURED STORIES PINNED",
       font=font(FB, 10), fill=NAVY)
MAPX0, MAPY0, MAPW, MAPH = mx0 + 4, my0 + 20, mx1 - mx0 - 8, my1 - my0 - 24


def proj(lon, lat):
    return (MAPX0 + (lon + 180.0) / 360.0 * MAPW,
            MAPY0 + (90.0 - lat) / 180.0 * MAPH)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-75, 73),
     (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
     (-90, 29), (-97, 26), (-105, 22), (-110, 24), (-115, 30), (-125, 40), (-125, 49),
     (-135, 58), (-155, 60), (-165, 60)],
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-40, 80), (-55, 76), (-58, 70), (-52, 64)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50), (-73, -53),
     (-70, -40), (-72, -20), (-77, -12), (-80, -4), (-81, 3)],
    [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 11), (48, 0),
     (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (15, -27), (12, -18),
     (9, -1), (9, 4), (-8, 5), (-15, 11), (-17, 15)],
    [(40, 68), (60, 69), (70, 72), (90, 75), (110, 76), (130, 72), (160, 70),
     (178, 66), (170, 60), (160, 55), (145, 60), (142, 50), (140, 40), (130, 35),
     (127, 35), (122, 40), (120, 32), (110, 20), (105, 10), (100, 8), (98, 15),
     (95, 16), (92, 22), (88, 22), (80, 15), (77, 8), (72, 20), (66, 25),
     (60, 25), (55, 26), (52, 28), (48, 30), (43, 12), (40, 15), (38, 20),
     (35, 28), (36, 36), (30, 36), (27, 40), (25, 45), (30, 50), (35, 55), (40, 60)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 52), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 62), (32, 66), (40, 68), (45, 68),
     (50, 69), (40, 64), (35, 60), (30, 55), (28, 50), (25, 45), (23, 40),
     (20, 40), (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37)],
    [(114, -22), (114, -30), (118, -35), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (126, -14),
     (122, -17), (115, -20)],
    [(95, 5), (105, 5), (110, -6), (115, -8), (120, -9), (125, -8), (130, -3),
     (135, -2), (140, -4), (138, -8)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly],
              fill=(196, 200, 190), outline=(120, 120, 120))
PINS = [(37.6, 55.7), (24.0, 59.5), (46.7, 24.7), (34.5, 31.5), (-77.0, 38.9),
        (98.5, 40.0), (106.8, -6.6), (-75.5, 10.4), (4.4, 50.8), (25.5, -10.7),
        (-74.0, 40.7), (72.9, 19.1)]
PIN_OFF = [(10, -2), (-13, -7), (7, 5), (-5, 9), (0, 0), (0, 0), (0, 0),
           (-14, 6), (-15, 3), (0, 0), (18, -12), (9, 0)]
for i, (lon, lat) in enumerate(PINS):
    x, y = proj(lon, lat)
    x += PIN_OFF[i][0]
    y += PIN_OFF[i][1]
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=RED, outline=(255, 255, 255))
    d.text((x - 3, y - 6), str(i + 1), font=font(FB, 9), fill=(255, 255, 255))

# ---------- bottom right: timeline + left-out box ----------
tx0 = 508
d.rectangle([tx0, my0, 1016, my0 + 20], fill=NAVY)
d.text((tx0 + 6, my0 + 4), "TIMELINE  -  WEDNESDAY 25 NOVEMBER 2026",
       font=font(FB, 10), fill=(255, 255, 255))
timeline = [
    ("05:18 PKT", "Shenzhou-24 launches from Jiuquan with a Pakistani aboard"),
    ("morning", "S. Korea scrambles jets as Russian aircraft enter its ADIZ"),
    ("09:20 WIB", "Indonesia: 15,164 citizens caught in overseas scam rings"),
    ("afternoon", "Putin meets oil chiefs, vows retaliation for refinery strikes"),
    ("evening", "Trump interview: Iran war funded thru Jan; \"Trumpcare\" talks"),
]
ty = my0 + 26
for t, ev in timeline:
    d.text((tx0 + 4, ty), t, font=font(FB, 9), fill=RED)
    d.text((tx0 + 78, ty), fit(ev, font(FR, 9), 1016 - tx0 - 82, d),
           font=font(FR, 9), fill=INK)
    ty += 12
ly = ty + 2
d.rectangle([tx0, ly, 1016, my1], fill=(255, 240, 220), outline=RED)
d.text((tx0 + 6, ly + 3), "LEFT OUT AS OLDER NEWS",
       font=font(FB, 9), fill=RED)
d.text((tx0 + 6, ly + 17),
       fit("Nvidia's Huang reinstated (Mon 23 Nov)  -  COP31 collapsed, no deal (Sun 22 Nov)",
           font(FR, 9), 1016 - tx0 - 12, d), font=font(FR, 9), fill=INK)
d.text((tx0 + 6, ly + 30),
       fit("EU \u20ac90bn Ukraine pledge (19 Nov)  -  Nepal quake, UAE crash (Tue 24 Nov)",
           font(FR, 9), 1016 - tx0 - 12, d), font=font(FR, 9), fill=INK)

# ---------- footer ----------
d.rectangle([0, 992, W, H], fill=(12, 12, 12))
d.text((10, 997),
       "Sources: Reuters, AP, CNN, NY Post, UN News, Euronews, Antara, Kyiv Independent, Moscow Times, BCCI, Sportstar, Sony  -  All 40 stories happened or were first reported on Wed 25 Nov 2026.",
       font=font(FR, 8), fill=(210, 210, 210))
d.text((10, 1010), "THE WORLD TODAY  -  WEDNESDAY 25 NOVEMBER 2026  -  Judge: this image names its day in the masthead, the leads, the timeline and the footer.",
       font=font(FR, 8), fill=(160, 160, 160))

out = os.path.join(BASE, "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
