"""Builds assets/icon-512.png, assets/apple-touch-icon.png and assets/og.png
from the game's pack01 art (the coloured subject PNGs).

    python3 tools/make_assets.py ~/IdeaProjects/MixReveal

The icon is a stand-in until the game has its final app icon: a cream tile with
a half-painted cupcake (sketch on the left, colour on the right), which is what
the game does: pour paint, reveal the picture.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

GAME = Path(sys.argv[1] if len(sys.argv) > 1 else "~/IdeaProjects/MixReveal").expanduser()
OUT = Path(__file__).resolve().parent.parent / "assets"
ART = GAME / "assets/art/pack01"
CREAM = (251, 233, 208)
PAPER = (246, 241, 231)
INK = (46, 42, 38)
TOMATO = (229, 72, 77)
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
PAINTS = [(229, 72, 77), (255, 197, 61), (62, 123, 250), (70, 182, 90), (142, 78, 198), (255, 138, 61)]


def subject(name, size):
    im = Image.open(ART / name / "subject.png").convert("RGBA")
    return im.resize((size, size), Image.LANCZOS)


def sketch(im):
    """The unpainted look: a pale grey line drawing of the subject."""
    gray = ImageOps.grayscale(im.convert("RGB"))
    a = im.getchannel("A")
    lines = gray.point(lambda v: 255 if v < 70 else 0)          # the dark outlines
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    fill = Image.new("RGBA", im.size, (232, 222, 206, 255))
    out.paste(fill, (0, 0), a)
    ink = Image.new("RGBA", im.size, (150, 140, 128, 255))
    out.paste(ink, (0, 0), Image.composite(lines, Image.new("L", im.size, 0), a))
    return out


def rounded(size, radius, color):
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle([0, 0, size - 1, size - 1], radius, fill=color)
    return tile


def half_revealed(name, size):
    art = subject(name, size)
    pale = sketch(art)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).polygon([(size * 0.42, 0), (size, 0), (size, size), (size * 0.58, size)], fill=255)
    return Image.composite(art, pale, mask)


def icon(size=1024):
    tile = rounded(size, int(size * 0.22), CREAM + (255,))
    d = ImageDraw.Draw(tile)
    for i, c in enumerate(PAINTS[:4]):          # paint drops along the top
        x = int(size * (0.2 + i * 0.2))
        d.ellipse([x - size * 0.05, size * 0.07, x + size * 0.05, size * 0.17], fill=c)
    art = half_revealed("cupcake", int(size * 0.74))
    tile.alpha_composite(art, (int(size * 0.13), int(size * 0.2)))
    return tile


def og():
    w, h = 1200, 630
    img = Image.new("RGBA", (w, h), PAPER + (255,))
    d = ImageDraw.Draw(img)
    for i, c in enumerate(PAINTS):
        d.rectangle([i * w // len(PAINTS), 0, (i + 1) * w // len(PAINTS), 14], fill=c)
    names = ["sleepy_cat", "cupcake", "sunflower", "goldfish_bowl"]
    size = 250
    for i, n in enumerate(names):
        x = 60 + i * 275
        card = rounded(size + 20, 34, (255, 255, 255, 255))
        shadow = rounded(size + 20, 34, (61, 43, 31, 60)).filter(ImageFilter.GaussianBlur(10))
        img.alpha_composite(shadow, (x + 4, 300 + 10))
        img.alpha_composite(card, (x, 300))
        art = half_revealed(n, size) if i % 2 == 0 else subject(n, size)
        img.alpha_composite(art, (x + 10, 310))
    ic = icon(170)
    img.alpha_composite(ic, (60, 70))
    title = ImageFont.truetype(FONT, 84)
    sub = ImageFont.truetype(FONT, 38)
    d.text((260, 82), "Mix & Reveal", font=title, fill=INK)
    d.text((262, 186), "Mix colors, pour paint, reveal the picture.", font=sub, fill=TOMATO)
    return img.convert("RGB")


OUT.mkdir(parents=True, exist_ok=True)
big = icon(1024)
big.resize((512, 512), Image.LANCZOS).save(OUT / "icon-512.png", optimize=True)
flat = Image.new("RGB", (1024, 1024), CREAM)               # iOS draws its own corners
flat.paste(big, (0, 0), big)
flat.resize((180, 180), Image.LANCZOS).save(OUT / "apple-touch-icon.png", optimize=True)
og().save(OUT / "og.png", optimize=True)
for n in ["sleepy_cat", "cupcake", "sunflower", "goldfish_bowl"]:     # the landing page art row
    subject(n, 256).save(OUT / f"art-{n.replace('_', '-')}.png", optimize=True)
print("wrote", ", ".join(p.name for p in sorted(OUT.glob("*.png"))))
