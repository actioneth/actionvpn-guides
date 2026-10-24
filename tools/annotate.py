"""Mark where to tap on the guide screenshots: an orange frame, an arrow and a step number.

Coordinates are taken from the 923x2000 previews and scaled to the 1181x2560 originals.
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC = Path(r"C:\Users\WubWub\Downloads\Telegram Desktop")
OUT = Path(sys.argv[1])
K = 1.28
ORANGE = (255, 106, 0)
WHITE = (255, 255, 255)
FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 64)

# file stem -> (output name, [targets], [areas to blur])
# target: (x1, y1, x2, y2, arrow side, step number or None)
SHOTS = {
    "photo_2026-10-24_14-28-48": ("ios-appstore", [(330, 446, 500, 514, "bottom", None)], []),
    "photo_2026-10-24_14-28-52": ("defaultvpn-plus", [(756, 921, 887, 1044, "top", None)], []),
    "photo_2026-10-24_14-28-54": ("defaultvpn-paste", [(35, 1091, 887, 1218, "right", 1),
                                                       (35, 1245, 887, 1372, "right", 2)], []),
    "photo_2026-10-24_14-28-55": ("defaultvpn-connect", [(35, 1081, 887, 1848, "top", None)], []),
    "photo_2026-10-24_14-28-56": ("defaultvpn-allow", [(152, 1320, 770, 1422, "bottom", None)], []),
    "photo_2026-10-24_14-28-59": ("defaultvpn-connected", [], []),
    "photo_2026-10-24_14-30-13": ("amnezia-appstore", [(330, 446, 500, 514, "bottom", None)], []),
    "photo_2026-10-24_14-30-15": ("amnezia-paste", [(729, 511, 887, 668, "bottom", None)], []),
    "photo_2026-10-24_14-30-16": ("amnezia-allow-paste", [(152, 1040, 770, 1143, "bottom", None)], []),
    "photo_2026-10-24_14-30-17": ("amnezia-continue", [(35, 549, 887, 669, "bottom", None)],
                                  [(60, 420, 728, 480)]),
    "photo_2026-10-24_14-30-18": ("amnezia-connect", [(35, 695, 887, 815, "bottom", None)], []),
    "photo_2026-10-24_14-30-19": ("amnezia-qr", [(35, 1386, 887, 1566, "top", None)], []),
    "photo_2026-10-24_14-30-20": ("amnezia-qr-camera", [],
                                  [(137, 755, 750, 1375), (140, 1540, 760, 1732), (34, 428, 135, 1732)]),
    "photo_2026-10-24_14-31-54": ("awg-appstore", [(330, 446, 500, 514, "bottom", None)], []),
    "photo_2026-10-24_14-31-56": ("awg-add", [(296, 953, 626, 1048, "bottom", None)], []),
    "photo_2026-10-24_14-31-58": ("awg-from-qr", [(238, 668, 684, 770, "bottom", None)], []),
    # The camera shots show the real key's QR around the dialogs: blur everything but the dialog.
    "photo_2026-10-24_14-32-00": ("awg-name", [(470, 783, 770, 884, "bottom", None)],
                                  [(0, 300, 120, 1260), (800, 300, 923, 1260), (120, 915, 800, 1260),
                                   (0, 0, 923, 300)]),
    "photo_2026-10-24_14-32-02": ("awg-allow", [(152, 1320, 770, 1422, "bottom", None)],
                                  [(0, 0, 923, 598), (0, 598, 120, 1760), (805, 598, 923, 1760),
                                   (120, 1455, 805, 1760)]),
    "photo_2026-10-24_14-32-05": ("awg-toggle", [(712, 280, 848, 340, "bottom", None)], []),
    "photo_2026-10-24_14-32-06": ("awg-connected", [], []),
}


def scale(box):
    return tuple(round(v * K) for v in box)


def blur(img, box):
    x1, y1, x2, y2 = scale(box)
    region = img.crop((x1, y1, x2, y2))
    small = region.resize((max(1, (x2 - x1) // 40), max(1, (y2 - y1) // 40)), Image.Resampling.BILINEAR)
    img.paste(small.resize(region.size, Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(8)), (x1, y1))


def arrow(draw, start, end, width=22):
    for color, w in ((WHITE, width + 12), (ORANGE, width)):
        draw.line([start, end], fill=color, width=w)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        head = 70 + (w - width)
        left = (end[0] - head * math.cos(angle - 0.5), end[1] - head * math.sin(angle - 0.5))
        right = (end[0] - head * math.cos(angle + 0.5), end[1] - head * math.sin(angle + 0.5))
        draw.polygon([end, left, right], fill=color)


def badge(draw, center, number):
    x, y = center
    r = 52
    draw.ellipse((x - r - 6, y - r - 6, x + r + 6, y + r + 6), fill=WHITE)
    draw.ellipse((x - r, y - r, x + r, y + r), fill=ORANGE)
    draw.text((x, y), str(number), fill=WHITE, font=FONT, anchor="mm")


def mark(img, target):
    x1, y1, x2, y2 = scale(target[:4])
    side, number = target[4], target[5]
    draw = ImageDraw.Draw(img)
    for color, w, pad in ((WHITE, 18, 14), (ORANGE, 10, 14)):
        draw.rounded_rectangle((x1 - pad, y1 - pad, x2 + pad, y2 + pad), radius=36, outline=color, width=w)
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    gap, length = 30, 230
    if side == "bottom":
        end, start = (cx, y2 + gap), (cx, y2 + gap + length)
    elif side == "top":
        end, start = (cx, y1 - gap), (cx, y1 - gap - length)
    elif side == "right":
        end, start = (x2 - 40, cy), (x2 - 40 + length, cy)
        end = (min(end[0], img.width - 300), cy)
        start = (end[0] + length, cy)
    else:
        end, start = (x1 - gap, cy), (x1 - gap - length, cy)
    arrow(draw, start, end)
    if number is not None:
        badge(draw, start, number)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, (name, targets, blurs) in SHOTS.items():
        img = Image.open(SRC / f"{stem}.jpg").convert("RGB")
        for box in blurs:
            blur(img, box)
        for target in targets:
            mark(img, target)
        # Cut off the iPhone status bar (time, battery) and the home indicator strip.
        img = img.crop((0, round(126 * K), img.width, round(1925 * K)))
        img.thumbnail((900, 1950))  # lighter pages, still sharp on a phone
        img.save(OUT / f"{name}.jpg", quality=85, optimize=True)
        print(name)


main()
