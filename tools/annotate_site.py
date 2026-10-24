"""Mark the system tab (1) and the download button (2) on amnezia.org download page shots."""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WEB = Path(__file__).parent / "web"
OUT = Path(sys.argv[1])
ORANGE, WHITE = (255, 106, 0), (255, 255, 255)
FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 34)

# os -> (tab box, download box) in page pixels, from getBoundingClientRect
SHOTS = {
    "Windows": ((358, 462, 90, 90), (403, 584, 190, 56)),
    "macOS": ((453, 462, 90, 90), (421, 584, 190, 56)),
    "Linux": ((738, 462, 90, 90), (545, 584, 190, 56)),
}


def frame(draw, box, number):
    x, y, w, h = box
    for color, width in ((WHITE, 9), (ORANGE, 5)):
        draw.rounded_rectangle((x - 8, y - 8, x + w + 8, y + h + 8), radius=16, outline=color, width=width)
    cx, cy, r = x - 8, y - 8, 24
    draw.ellipse((cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3), fill=WHITE)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE)
    draw.text((cx, cy), str(number), fill=WHITE, font=FONT, anchor="mm")


for os_name, (tab, button) in SHOTS.items():
    img = Image.open(WEB / f"site-{os_name}.png").convert("RGB")
    draw = ImageDraw.Draw(img)
    frame(draw, tab, 1)
    frame(draw, button, 2)
    img = img.crop((140, 410, 1140, 720))  # heading, system tabs and the download button
    img.save(OUT / f"site-{os_name.lower()}.jpg", quality=88, optimize=True)
    print(os_name)
