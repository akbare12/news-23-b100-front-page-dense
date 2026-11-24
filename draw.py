#!/usr/bin/env python3
"""news-23 b100 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(draw, x, y, text, color):
    f = font(SANS_B, 10)
    tw = draw.textlength(text, font=f)
    draw.rounded_rectangle([x, y, x + tw + 10, y + 15], radius=2, fill=color)
    draw.text((x + 5, y + 2), text, font=f, fill="white")
    return tw + 10


def main():
    img = Image.new("RGB", (W, H), "#fdfcf7")
    d = ImageDraw.Draw(img)

    # ---- masthead 0-62 ----
    d.rectangle([0, 0, W, 62], fill="#111111")
    d.text((14, 6), "THE WORLD TODAY", font=font(SERIF_B, 44), fill="white")
    d.text((700, 20), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 17), fill="#e8b93c")

    # ---- kicker 62-84 ----
    d.rectangle([0, 62, W, 84], fill="#b01e24")
    d.text((14, 66), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
           font=font(SANS_B, 14), fill="white")

    # ---- number strip 84-148: two rows of five ----
    nums = [
        ("-3.3%", "KOSPI", "#b01e24"), ("5.3", "US-CHINA POWER GAP", "#1b3a6b"),
        ("11,762", "EBOLA CASES, DRC", "#111111"), ("10T won", "SEOUL STABILISATION FUND", "#a67c00"),
        ("2%", "BILLIONAIRE TAX IN PARIS", "#15803d"),
        ("$450M", "SKUBAL DEAL", "#1b3a6b"), ("165", "RUSSIAN MISSILES/WEEK", "#b01e24"),
        ("12,000", "CLEARED IN MANCHESTER", "#111111"), ("264 kg", "EXPLOSIVES SEIZED", "#a67c00"),
        ("$107.3B", "ANTHROPIC IPO", "#15803d"),
    ]
    col_w = 201
    for i, (val, lab, col) in enumerate(nums):
        row, c = divmod(i, 5)
        x = 10 + c * col_w
        y = 86 + row * 30
        d.text((x, y), val, font=font(SANS_B, 18), fill=col)
        d.text((x, y + 19), lab, font=font(SANS_B, 8), fill="#444444")

    # ---- region bar 148-170 ----
    regions = [("ASIA-PACIFIC 7", 7, "#1b3a6b"), ("AMERICAS 8", 8, "#b01e24"),
               ("MIDDLE EAST 6", 6, "#a67c00"), ("EUROPE 5", 5, "#0f766e"),
               ("AFRICA 3", 3, "#15803d"), ("WORLD 2", 2, "#6b7280")]
    x = 8
    total = 31
    for name, n, col in regions:
        w = int(1008 * n / total)
        d.rectangle([x, 148, x + w - 2, 170], fill=col)
        d.text((x + 6, 153), name, font=font(SANS_B, 11), fill="white")
        x += w

    # ---- UTC strip 170-188 ----
    d.rectangle([0, 170, W, 188], fill="#ece8dc")
    d.text((10, 173), "THE DAY IN UTC", font=font(SANS_B, 11), fill="#111111")
    d.text((130, 173), "~00:00 Kospi dives    ~06:30 Guterres opens    ~09:00 Power Index    ~12:00 Paris 2% tax    ~15:00 Kyiv missiles",
           font=font(SANS, 11), fill="#333333")
    d.text((940, 173), "~ APPROX", font=font(SANS_B, 10), fill="#666666")

    # ---- heroes 188-420 ----
    heroes = [
        dict(kind="kospi", strip="KOSPI 4,708.54  \u00b7  -161 PTS",
             head="AI ROUT HITS ASIA",
             body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
             src="KOREA EXCHANGE"),
        dict(kind="guterres", strip="UN  \u00b7  BRIDGETOWN",
             head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body="UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
             src="UNITED NATIONS"),
        dict(kind="power", strip="ASIA POWER INDEX 2026",
             head="US LEAD OVER CHINA AT RECORD LOW",
             body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
             src="LOWY INSTITUTE"),
    ]
    hx = [8, 348, 688]
    hw = 328
    for i, hro in enumerate(heroes):
        x0 = hx[i]
        # scene 188-306
        if hro["kind"] == "kospi":
            d.rectangle([x0, 188, x0 + hw, 306], fill="#12264d")
            # buildings with lit windows
            import random
            rnd = random.Random(100 + i)
            bx = x0 + 4
            while bx < x0 + hw - 20:
                bw = rnd.randint(22, 42)
                bh = rnd.randint(40, 95)
                by = 306 - bh
                d.rectangle([bx, by, bx + bw, 306], fill="#0a1830")
                for wy in range(by + 6, 300, 12):
                    for wx in range(bx + 4, bx + bw - 4, 10):
                        if rnd.random() < 0.55:
                            d.rectangle([wx, wy, wx + 4, wy + 5], fill="#f5c542")
                bx += bw + 3
            # chart line
            pts = [(x0 + 10, 250), (x0 + 60, 228), (x0 + 110, 240), (x0 + 160, 210),
                   (x0 + 210, 222), (x0 + 260, 200), (x0 + 315, 192)]
            d.line(pts, fill="#ff7a1a", width=3)
            for px, py in pts:
                d.ellipse([px - 4, py - 4, px + 4, py + 4], fill="white", outline="#ff7a1a")
            d.text((x0 + 10, 196), "-3.3%", font=font(SANS_B, 26), fill="#ff7a1a")
        elif hro["kind"] == "guterres":
            d.rectangle([x0, 188, x0 + hw, 306], fill="#1d5c2e")
            d.text((x0 + 12, 202), "150 DELEGATES", font=font(SANS_B, 24), fill="#e8b93c")
            d.text((x0 + 12, 230), "BACK A RISK", font=font(SANS_B, 24), fill="#e8b93c")
            d.text((x0 + 12, 258), "FRAMEWORK", font=font(SANS_B, 24), fill="#e8b93c")
            # globe
            cx, cy, r = x0 + hw - 52, 248, 40
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#cfe8c9", outline="#7fb069", width=2)
            d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline="#7fb069", width=1)
            d.line([cx - r, cy, cx + r, cy], fill="#7fb069", width=1)
            d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill="#7fb069", width=1)
            d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill="#7fb069", width=1)
        else:
            d.rectangle([x0, 188, x0 + hw, 306], fill="#f5efe0")
            d.text((x0 + 10, 194), "NARROWEST SINCE 2018", font=font(SANS_B, 12), fill="#111111")
            d.text((x0 + hw - 78, 194), "GAP 5.3", font=font(SANS_B, 12), fill="#b01e24")
            bars = [("78.9", "US", 78.9, "#1b3a6b"), ("73.6", "CHINA", 73.6, "#b01e24"),
                    ("40.5", "INDIA", 40.5, "#d9a521")]
            base = 306
            for j, (val, lab, v, col) in enumerate(bars):
                bx0 = x0 + 18 + j * 106
                bh = int(v * 0.95)
                d.rectangle([bx0, base - bh, bx0 + 78, base], fill=col)
                d.text((bx0 + 14, base - bh - 22), val, font=font(SANS_B, 16),
                       fill="#111111" if lab == "INDIA" else "#111111")
                d.text((bx0 + 20, base - 20), lab, font=font(SANS_B, 12), fill="white")
        # black caption strip 306-324
        d.rectangle([x0, 306, x0 + hw, 324], fill="#111111")
        d.text((x0 + 8, 310), hro["strip"], font=font(SANS_B, 11), fill="white")
        # headline 328+, dynamic shrink to fit 2 lines
        for size in (21, 19, 17):
            f = font(SERIF_B, size)
            lines = wrap(d, hro["head"], f, hw - 8)
            if len(lines) <= 2:
                break
        y = 328
        for ln in lines[:2]:
            d.text((x0 + 2, y), ln, font=f, fill="#111111")
            y += size + 3
        # body: two lines starting just below headline
        bf = font(SANS, 11)
        blines = wrap(d, hro["body"], bf, hw - 8)
        yb = y + 4
        for ln in blines[:2]:
            d.text((x0 + 2, yb), ln, font=bf, fill="#333333")
            yb += 13
        # source + chip below body
        ys = yb + 3
        d.text((x0 + 2, ys), hro["src"], font=font(SANS, 9), fill="#666666")
        chip(d, x0 + hw - 78, ys - 2, "REPORTED", "#1b3a6b")

    # ---- cards header 420-440 ----
    d.rectangle([0, 420, W, 440], fill="#111111")
    d.text((10, 424), "MORE OF THE DAY  \u2014  10 STORIES", font=font(SANS_B, 13), fill="white")

    # ---- cards 442-590: 2 rows x 5, height 72 ----
    cards = [
        ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", "#0f766e"),
        ("FBI", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", "#1b3a6b"),
        ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", "#a67c00"),
        ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED", "#0f766e"),
        ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", "#b01e24"),
        ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED", "#b01e24"),
        ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", "#6d28d9"),
        ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED", "#1b3a6b"),
        ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", "#0f766e"),
        ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", "#6d28d9"),
    ]
    cw, ch, gap = 199, 72, 4
    for i, (reg, head, body, src, tag, col) in enumerate(cards):
        row, c = divmod(i, 5)
        x0 = 8 + c * (cw + gap)
        y0 = 442 + row * (ch + 4)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], outline="#cccccc", width=1)
        d.rectangle([x0, y0, x0 + cw, y0 + 16], fill=col)
        d.text((x0 + 5, y0 + 2), reg, font=font(SANS_B, 10), fill="white")
        d.text((x0 + cw - 16, y0 + 2), str(i + 1), font=font(SANS_B, 10), fill="white")
        hf = font(SANS_B, 11)
        hlines = wrap(d, head, hf, cw - 10)
        y = y0 + 19
        for ln in hlines[:2]:
            d.text((x0 + 5, y), ln, font=hf, fill="#111111")
            y += 12
        # body on its own line, then source + chip on the bottom line
        d.text((x0 + 5, y0 + 47), body, font=font(SANS, 9), fill="#444444")
        d.text((x0 + 5, y0 + 58), src, font=font(SANS, 8), fill="#888888")
        chip(d, x0 + cw - 74, y0 + 56, tag, "#1b3a6b" if tag == "REPORTED" else "#b01e24")

    # ---- section header 590-608 ----
    d.rectangle([0, 590, W, 608], fill="#111111")
    d.text((10, 594), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill="white")
    d.text((348, 594), "ALSO ON MONDAY", font=font(SANS_B, 13), fill="white")

    # ---- map 608-856 ----
    d.rectangle([8, 608, 336, 856], outline="#999999", width=1, fill="#f2f0e4")
    # continent blobs (stylised)
    d.polygon([(28, 648), (95, 620), (165, 636), (185, 676), (150, 738), (120, 808),
               (88, 836), (55, 808), (30, 748), (18, 698)], fill="#bcd6a8")          # Americas
    d.polygon([(195, 640), (245, 626), (275, 648), (262, 680), (215, 690), (192, 668)], fill="#bcd6a8")  # Europe
    d.polygon([(205, 708), (252, 706), (262, 748), (240, 808), (212, 790), (198, 748)], fill="#bcd6a8")  # Africa
    d.polygon([(285, 630), (325, 626), (333, 663), (315, 698), (288, 686), (278, 653)], fill="#bcd6a8")  # Asia
    pins = [
        (1, 290, 680), (2, 118, 814), (3, 306, 660), (4, 128, 734), (5, 138, 708),
        (6, 246, 672), (7, 108, 720), (8, 52, 726), (9, 76, 756), (10, 96, 780),
        (11, 224, 656), (12, 200, 650), (13, 320, 642),
    ]
    pf = font(SANS_B, 9)
    for n, px, py in pins:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill="#b01e24", outline="white", width=1)
        tw = d.textlength(str(n), font=pf)
        d.text((px - tw / 2, py - 7), str(n), font=pf, fill="white")
    d.text((16, 820), "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", font=font(SANS, 9), fill="#333333")
    d.text((16, 832), "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", font=font(SANS, 9), fill="#333333")
    d.text((16, 844), "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow",
           font=font(SANS, 9), fill="#333333")

    # ---- ALSO list 608-856, two columns of nine ----
    also = [
        "Paris: 100+ back 2% billionaire tax",
        "Manchester: 12,000 cleared",
        "Zelenskyy: 165 missiles in a week",
        "COP31: the day after Antalya pact rejected",
        "Benghazi: UN demands probe [CLAIM]",
        "Israel unity talks resume",
        "Gaza: two killed in Israeli strike",
        "West Bank settler attacks",
        "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives",
        "Bahrain: strike hits plant, 2 hurt",
        "Sudan: defences down drones [CLAIM]",
        "DRC: fighting traps Ebola teams",
        "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits in exam row",
        "SK Telecom -7.3% as hype cools",
        "China eases margin rules",
        "Seoul readies 10T-won fund",
    ]
    af = font(SANS, 12)
    ab = font(SANS_B, 12)
    for i, item in enumerate(also):
        col, row = divmod(i, 9)
        x0 = 348 + col * 340
        y0 = 616 + row * 28
        num = str(14 + i) + "."
        d.text((x0, y0), num, font=ab, fill="#111111")
        if "[CLAIM]" in item:
            txt = item.replace(" [CLAIM]", "")
            d.text((x0 + 26, y0), txt, font=af, fill="#111111")
            tw = d.textlength(txt, font=af)
            d.text((x0 + 26 + tw + 4, y0), "[CLAIM]", font=ab, fill="#b01e24")
        else:
            d.text((x0 + 26, y0), item, font=af, fill="#111111")

    # ---- DATE CHECK 856-932 ----
    d.rectangle([8, 856, 1016, 932], outline="#b01e24", width=2)
    d.text((16, 864), "DATE CHECK", font=font(SANS_B, 15), fill="#b01e24")
    d.text((620, 864), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
           font=font(SANS_B, 10), fill="#b01e24")
    d.text((16, 886), "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
           font=font(SANS, 10), fill="#111111")
    d.text((16, 906), "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
           font=font(SANS, 11), fill="#111111")

    # ---- footer 940-1024 ----
    d.text((10, 950), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=font(SANS, 10), fill="#555555")
    d.text((10, 966), "CHIPS: REPORTED = confirmed by wires.  CLAIM = one side's claim, not independently confirmed.  ONGOING = still developing.",
           font=font(SANS, 10), fill="#555555")
    d.text((10, 982), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
           font=font(SANS, 10), fill="#555555")
    d.line([10, 992, 1014, 992], fill="#d9a521", width=2)
    d.text((300, 998), "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
           font=font(SANS_B, 11), fill="#a67c00")

    img.save(OUT, "PNG")
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
