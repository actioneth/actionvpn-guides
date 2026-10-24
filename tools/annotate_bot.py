"""Bot screenshots for the guides: hide the Telegram ID, the key and the QR codes, frame the buttons."""

import sys
from pathlib import Path

from PIL import Image

import annotate

OUT = Path(sys.argv[1])

# stem -> (name, preview scale, [targets], [blurs], crop the phone status bar and input field)
# Coordinates are taken from the previews; the chat crops were shown at their real size.
SHOTS = {
    "photo_2026-10-24_15-12-27": ("bot-cabinet", 1.0, [(30, 450, 590, 575, None, None)],
                                  [(130, 140, 445, 205)], False),
    "photo_2026-10-24_15-12-28": ("bot-subs", 1.0, [(30, 630, 1135, 750, None, None)], [], False),
    "photo_2026-10-24_15-12-28 (2)": ("bot-sub", 1.0, [(30, 268, 578, 392, None, None)], [], False),
    "photo_2026-10-24_15-12-30": ("bot-key", 1.28,
                                  [(20, 1545, 830, 1632, None, None), (20, 1640, 830, 1727, None, None)],
                                  [(0, 126, 923, 805)], True),
    "photo_2026-10-24_15-12-31": ("bot-qr-amnezia", 1.28, [(20, 670, 830, 760, None, None)],
                                  [(25, 968, 667, 1612)], True),
    "photo_2026-10-24_15-12-32": ("bot-qr-awg", 1.28, [(20, 790, 830, 878, None, None)],
                                  [(25, 990, 667, 1634)], True),
}

for stem, (name, k, targets, blurs, phone) in SHOTS.items():
    annotate.K = k
    img = Image.open(annotate.SRC / f"{stem}.jpg").convert("RGB")
    for box in blurs:
        annotate.blur(img, box)
    for target in targets:
        annotate.mark(img, target)
    if phone:  # status bar on top, the message field at the bottom
        img = img.crop((0, round(126 * k), img.width, round(1840 * k)))
    img.thumbnail((900, 1950))
    img.save(OUT / f"{name}.jpg", quality=85, optimize=True)
    print(name)
