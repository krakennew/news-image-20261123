#!/usr/bin/env python3
"""Draw the poster for Monday 23 November 2026: one day's world news.

Build-time script only. It renders entry.png (1024x1024, <=1 MiB) from the
verified story list below. main.py is the program that runs at grading time.

Revision notes (pass 2): every detail trimmed so it wraps to at most two
lines at the column width; the lead summary shortened to two lines so it
stays inside its card; the map shortened to give the story columns room;
the footer shortened so it no longer collides with the right-hand tag;
the Cikande and Selangor map markers nudged apart so they do not overlap.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 24, 24)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
AMBER = (244, 169, 0)
GREY = (90, 90, 90)
OCEAN = (214, 230, 240)
LAND = (196, 205, 158)
LAND_EDGE = (140, 150, 105)

DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
DJSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# (number, headline, detail, map lon, map lat) -- lon/lat None: no marker.
# Headlines fit two lines, details fit two lines, at the column width.
STORIES = [
    (2, "TANKERS ABLAZE IN HORMUZ",
     "Two supertankers hit mines and caught fire, Iran navy says.",
     57.0, 26.5),
    (3, "HOUTHIS CLAIM SAUDI REFINERY HIT",
     "Houthis claim Rabigh hit; Saudi defences stop missile.",
     None, None),
    (4, "BAHRAIN TAKES IRAN TO THE UN",
     "Manama wants UN action after Iran hit a civilian factory.",
     None, None),
    (5, "RUSSIAN WARSHIP HIT IN LIBYA",
     "Suspected Ukrainian drones hit corvette Merkury; 10 hurt.",
     20.0, 32.0),
    (6, "DRONE HITS FLATS NEAR KYIV",
     "Russian drone hits a five-storey block in Dymer; 9 killed.",
     30.5, 50.9),
    (7, "ODESA SCHOOLS GO REMOTE",
     "Schools online 23-27 Nov as strikes wreck power and water.",
     None, None),
    (8, "DRONES HIT RUSSIAN REFINERY",
     "Fire at Novoshakhtinsk refinery in Rostov after drone attack.",
     None, None),
    (9, "POLAND: ALL THREE WERE KH-101s",
     "Prosecutors confirm all three were Russian cruise missiles.",
     22.0, 50.5),
    (10, "RUTTE: 'EVERY INCH' OF POLAND",
     "NATO chief pledges to defend 'every inch' of Polish land.",
     None, None),
    (11, "HAMAS SEEKS URGENT GAZA TALKS",
     "Hamas seeks talks after a strike kills three aid workers.",
     34.5, 31.4),
    (12, "TWO KILLED IN GAZA SHELLING",
     "Two killed in south Gaza; one critical in northern strike.",
     None, None),
    (13, "SETTLERS TORCH 12 VEHICLES",
     "Cars torched near Ramallah; ex-minister condemns attacks.",
     None, None),
    (14, "DRONES HIT KHARTOUM, UN SITE",
     "RSF drones hit a UN site; three killed in Omdurman house.",
     32.5, 15.6),
    (15, "WHO WARNS OVER EBOLA IN DRC",
     "Fighting by Ebola-hit hospital puts patients at 'grave risk'.",
     25.0, -2.0),
    (16, "UN COUNCIL MEETS ON ENERGY",
     "Council examines energy sites and Black Sea shipping today.",
     None, None),
    (17, "DEMOCRATS CLINCH 258 SEATS",
     "Largest House majority since 1992; Hubbard wins in NC.",
     None, None),
    (18, "TRUMP COOL ON SCHUMER",
     "President says working with Schumer as leader is 'difficult'.",
     None, None),
    (19, "ICE DETAIN FATHER, DAUGHTER",
     "Masked agents seize pair on jetway to a baptism.",
     -122.3, 47.6),
    (20, "TRUMP: NO RUSH ON IRAN",
     "President plays down hawks' calls for fresh strikes on Iran.",
     None, None),
    (21, "'EL CHAPO ISIDRO' CAPTURED",
     "FBI most-wanted cartel boss seized; 11 dead in Sinaloa raid.",
     -108.0, 25.0),
    (22, "ISRAEL UNITY TALKS FAIL",
     "Likud and Yashar end coalition talks without a deal.",
     None, None),
    (23, "NO DEAL ON KILLER ROBOTS",
     "UN talks end with no binding rules on AI weapons.",
     None, None),
    (24, "MYANMAR SLAMS ASEAN RULING",
     "Army-backed govt calls ASEAN ruling 'unfair and imbalanced'.",
     None, None),
    (25, "INDIA: PROTESTS AT META",
     "Youth wing storms Meta offices over withheld accounts.",
     None, None),
    (26, "UK TO BUILD UKRAINE DRONES",
     "Britain to produce Ukrainian long-range drones at home.",
     None, None),
    (27, "KOSPI SINKS 3% ON AI FEARS",
     "Seoul extends Friday's 5.2% plunge as AI fears hit chips.",
     127.0, 37.5),
    (28, "TAIWAN BANS SHORT-SELLING",
     "Taipei bars short sales below prior close after worst week.",
     121.5, 25.0),
    (29, "CHINA EASES MARGIN RULES",
     "Beijing cuts stock-buying margin to 80% from 30 November.",
     None, None),
    (30, "KOREA READIES RESCUE FUND",
     "Seoul readies market fund after emergency Sunday meeting.",
     None, None),
    (31, "TOKYO SHUT FOR HOLIDAY",
     "Tokyo shut for holiday as Asia's sell-off spreads.",
     None, None),
    (32, "OIL NEAR $93 ON HORMUZ FEARS",
     "Brent near $93 as tanker attacks offset surplus worries.",
     None, None),
    (33, "FACTORY FIRE: 36 MISSING",
     "Candy factory blaze kills 3; dozens still unaccounted for.",
     107.0, -7.0),
    (34, "LAHORE CHOKES AGAIN",
     "AQI hits 538 on Sunday morning, IQAir data show.",
     74.3, 31.5),
    (35, "SELANGOR FLOODS EASE",
     "1,594 still in shelters as high tides are forecast this week.",
     99.0, 4.0),
    (36, "RUSSIAN SHIP STILL BURNING",
     "Ship attacked off Finland still smoulders; crews cool cargo.",
     None, None),
    (37, "KOREA MINISTER QUITS",
     "Choi Kyo-jin quits over AI exam cheating; 111 cases found.",
     None, None),
    (38, "TWO US SHOOTINGS",
     "Three killed at Ohio baby shower; nine shot at CA concert.",
     -81.7, 41.4),
    (39, "CAMEROON'S EX-REBELS IN LIMBO",
     "Ex-fighters face arrest fears and broken promises.",
     None, None),
    (40, "SHURI CASTLE REOPENS",
     "Main hall opens today, seven years after the 2019 fire.",
     None, None),
    (41, "LISBON MARCHES ON COSTS",
     "Thousands march in Lisbon for a sixth weekend running.",
     -9.1, 38.7),
    (42, "PAOLO BULGARI DIES AT 89",
     "Jeweller built family firm into global brand; funeral today.",
     None, None),
    (43, "TITANIC RING SELLS FOR \u00a3150K",
     "Lady Duff Gordon's ring beats its \u00a380,000 estimate.",
     None, None),
    (44, "LIVERPOOL ROUT UNITED 4-0",
     "Pochettino's debut ends in ruin; Yoro off after 8 minutes.",
     -3.0, 53.4),
    (45, "MARQUEZ SEALS 8TH TITLE",
     "Crown clinched in Portugal; Bezzecchi wins the race.",
     None, None),
    (46, "INDIA PUSH FOR TEST WIN",
     "NZ 157/4 at lunch on day five as India chase victory.",
     None, None),
    (47, "CHESS CROWN UNDER WAY",
     "FIDE World Championship opens; Sindarov takes white.",
     None, None),
]

COLUMNS = [
    ("WAR & CONFLICT", STORIES[0:10]),
    ("WAR  \u2022  POLITICS", STORIES[10:19]),
    ("POLITICS  \u2022  MARKETS", STORIES[19:28]),
    ("MARKETS  \u2022  DISASTER", STORIES[28:37]),
    ("SOCIETY  \u2022  SPORT", STORIES[37:46]),
]

# Coarse continent outlines as (lon, lat) points, equirectangular.
N_AMERICA = [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-130, 54),
             (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
             (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12),
             (-83, 9), (-79, 9), (-81, 13), (-84, 16), (-87, 21),
             (-90, 21), (-96, 19), (-97, 26), (-93, 30), (-89, 30),
             (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-74, 40),
             (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 47),
             (-60, 52), (-65, 58), (-68, 58), (-78, 62), (-85, 66),
             (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70),
             (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68),
             (-22, 70), (-20, 74), (-25, 76), (-40, 78), (-58, 76),
             (-62, 74), (-60, 70)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
             (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
             (-74, -50), (-70, -54), (-66, -55), (-65, -45), (-62, -41),
             (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17),
             (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0),
             (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
          (10, 37), (11, 34), (19, 33), (25, 32), (32, 31), (34, 28),
          (37, 22), (39, 18), (43, 12), (48, 11), (51, 12), (46, 5),
          (42, 0), (40, -5), (40, -10), (36, -18), (33, -26), (28, -33),
          (20, -35), (17, -32), (14, -22), (12, -18), (13, -12), (9, -1),
          (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
          (10, 59), (5, 60), (5, 62), (12, 65), (18, 69), (25, 71),
          (30, 70), (35, 68), (40, 68), (44, 66), (40, 64), (35, 62),
          (30, 60), (28, 58), (24, 58), (21, 55), (21, 54), (24, 52),
          (28, 50), (30, 48), (28, 46), (24, 44), (22, 40), (19, 42),
          (15, 44), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36)]
ASIA = [(30, 70), (40, 68), (50, 69), (60, 69), (68, 73), (75, 73),
        (85, 75), (95, 76), (105, 77), (113, 74), (120, 73), (130, 72),
        (140, 72), (150, 70), (158, 70), (162, 66), (170, 66), (178, 65),
        (170, 62), (162, 60), (158, 56), (156, 52), (150, 59), (142, 59),
        (140, 55), (138, 50), (135, 45), (132, 43), (130, 42), (127, 40),
        (122, 40), (120, 39), (122, 37), (120, 34), (122, 32), (120, 28),
        (118, 25), (110, 21), (108, 18), (105, 10), (103, 8), (100, 7),
        (98, 10), (97, 15), (94, 17), (92, 21), (89, 22), (86, 20),
        (82, 17), (80, 13), (77, 8), (75, 12), (72, 20), (68, 22),
        (66, 25), (62, 25), (58, 26), (56, 27), (54, 27), (52, 28),
        (50, 29), (48, 30), (44, 29), (42, 27), (40, 25), (38, 22),
        (36, 20), (35, 18), (34, 16), (33, 15), (35, 12), (39, 12),
        (43, 12), (45, 12), (48, 14), (51, 16), (55, 17), (58, 20),
        (59, 22), (57, 25), (55, 26), (52, 25), (50, 26), (48, 28),
        (44, 29), (40, 30), (36, 33), (33, 35), (30, 36), (27, 37),
        (27, 40), (30, 41), (32, 42), (33, 45), (30, 46), (28, 47),
        (30, 50), (32, 53), (35, 56), (38, 58), (40, 60), (38, 63),
        (35, 65), (32, 67), (30, 69)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -11), (140, -17), (136, -15), (135, -12),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)]
JAPAN = [(130, 31), (132, 33), (134, 34), (137, 35), (139, 36), (141, 38),
         (141, 41), (143, 43), (145, 44), (142, 44), (140, 42), (139, 38)]
INDONESIA = [(95, 5), (98, 3), (100, 0), (104, -3), (106, -6), (110, -7),
             (114, -8), (118, -9), (120, -10), (122, -9), (125, -9),
             (128, -8), (130, -7), (131, -3), (135, -3), (138, -4),
             (141, -5), (141, -2), (138, 0), (134, 0), (130, 1), (126, 1),
             (122, 0), (118, 0), (114, 0), (110, 0), (106, 0), (102, 2),
             (98, 4)]
NZ = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
      (178, -37), (175, -40), (172, -42), (168, -46)]
CONTINENTS = [N_AMERICA, GREENLAND, S_AMERICA, AFRICA, EUROPE, ASIA,
              AUSTRALIA, UK, JAPAN, INDONESIA, NZ]

MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 24, 214, 1000, 352


def project(lon, lat):
    x = MAP_X0 + (lon + 170.0) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (78.0 - lat) / 136.0 * (MAP_Y1 - MAP_Y0)
    return (x, y)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.rectangle([0, 100, W, 104], fill=RED)
    f_title = font(DJSB, 46)
    f_date = font(DJB, 25)
    f_tag = font(DJB, 15)
    d.text((24, 12), "THE WORLD TODAY", font=f_title, fill=(255, 255, 255))
    d.text((24, 64), "MONDAY  23  NOVEMBER  2026", font=f_date, fill=AMBER)
    chip = "47 STORIES  \u2022  ONE DAY"
    cw = d.textlength(chip, font=f_tag)
    d.rounded_rectangle([W - 24 - cw - 20, 30, W - 24, 62], radius=4,
                        outline=AMBER, width=2)
    d.text((W - 24 - cw - 10, 37), chip, font=f_tag, fill=AMBER)

    # ---- lead story ----
    d.rectangle([24, 112, 1000, 214], fill=(255, 255, 255),
                outline=(200, 190, 170), width=1)
    d.rectangle([24, 112, 32, 214], fill=RED)
    d.text((44, 118), "1  \u2022  LEAD STORY", font=font(DJB, 13), fill=RED)
    d.text((44, 136), "COP31 CLIMATE TALKS COLLAPSE",
           font=font(DJSB, 30), fill=INK)
    lead = ("UN climate summit in Antalya ends with no deal after record "
            "overtime \u2014 the first collapse since Copenhagen 2009. The EU "
            "and island states rejected a text with no mention of fossil fuels.")
    lead_lines = wrap(d, lead, font(DJS, 15), 940)
    assert len(lead_lines) <= 2, "lead overflows: %r" % (lead_lines,)
    y = 172
    for line in lead_lines:
        d.text((44, y), line, font=font(DJS, 15), fill=(50, 50, 50))
        y += 19

    # ---- world map ----
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=OCEAN,
                outline=(180, 190, 200), width=1)
    for lon in range(-150, 181, 30):
        x = MAP_X0 + (lon + 170.0) / 360.0 * (MAP_X1 - MAP_X0)
        d.line([(x, MAP_Y0), (x, MAP_Y1)], fill=(200, 214, 224), width=1)
    for lat in (-60, -30, 0, 30, 60):
        y = MAP_Y0 + (78.0 - lat) / 136.0 * (MAP_Y1 - MAP_Y0)
        d.line([(MAP_X0, y), (MAP_X1, y)], fill=(200, 214, 224), width=1)
    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_EDGE)
    f_num = font(DJB, 10)
    for num, _h, _t, lon, lat in STORIES:
        if lon is None:
            continue
        x, y = project(lon, lat)
        r = 9 if num >= 10 else 8
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=f_num)
        d.text((x - tw / 2, y - 6.5), str(num), font=f_num,
               fill=(255, 255, 255))
    d.text((MAP_X0 + 4, MAP_Y1 - 18),
           "WHERE IT HAPPENED \u2014 numbers match the stories below",
           font=font(DJB, 11), fill=(70, 90, 110))

    # ---- story columns ----
    col_w = 185
    gap = 12
    top = 364
    bottom = 978
    f_head = font(DJB, 12)
    f_body = font(DJ, 10)
    f_col = font(DJB, 12)
    for ci, (title, items) in enumerate(COLUMNS):
        x0 = 24 + ci * (col_w + gap)
        d.text((x0, top), title, font=f_col, fill=NAVY)
        d.line([(x0, top + 17), (x0 + col_w, top + 17)], fill=RED, width=2)
        y = top + 24
        cell = (bottom - y) / len(items)
        for num, head, detail, _lon, _lat in items:
            hlines = wrap(d, head, f_head, col_w - 20)
            blines = wrap(d, detail, f_body, col_w - 20)
            assert len(hlines) <= 2, "headline overflows: %r" % (head,)
            assert len(blines) <= 2, "detail overflows: %r" % (detail,)
            assert 15 * len(hlines) + 13 * len(blines) <= cell, \
                "item %d too tall for its cell" % num
            d.text((x0, y), str(num), font=f_head, fill=RED)
            nwid = d.textlength(str(num) + " ", font=f_head)
            d.text((x0 + nwid, y), hlines[0], font=f_head, fill=INK)
            yy = y + 15
            for extra in hlines[1:]:
                d.text((x0 + nwid, yy), extra, font=f_head, fill=INK)
                yy += 15
            for bline in blines:
                d.text((x0 + nwid, yy), bline, font=f_body, fill=(60, 60, 60))
                yy += 13
            y += cell

    # ---- footer ----
    d.line([(24, 988), (1000, 988)], fill=(180, 170, 150), width=1)
    foot = ("Sources: AP, Reuters, CNN, WSJ, Le Monde, Al Jazeera, BBC, "
            "The Guardian \u2014 23 Nov 2026.")
    d.text((24, 996), foot, font=font(DJ, 11), fill=GREY)
    tag = "make.fun  \u2022  news-image-20261123"
    tw = d.textlength(tag, font=font(DJB, 11))
    d.text((1000 - tw, 996), tag, font=font(DJB, 11), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    draw()
