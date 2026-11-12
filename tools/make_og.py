#!/usr/bin/env python3
"""Gera assets/og-image.png (1200x630) no estilo do hero: fundo ameixa, brilho lilás."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
FONTS = HERE / "fonts"
MASCOT = HERE / "assets" / "nelis-hero.png"
OUT = HERE / "assets" / "og-image.png"

WHITE = (255, 255, 255)
LILAC_TXT = (201, 166, 245)
DIM = (214, 188, 232)

W, H = 1200, 630


def font(name, size, weight=400):
    p = FONTS / name
    if p.exists():
        f = ImageFont.truetype(str(p), size)
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
        return f
    return ImageFont.load_default()


def main():
    # fundo com brilho radial suave (sem anéis)
    from PIL import ImageFilter

    base = Image.new("RGB", (W, H), (37, 15, 46))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([560, -220, 1320, 780], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(150))
    glow = Image.new("RGB", (W, H), (146, 92, 180))
    img = Image.composite(glow, base, mask)
    d = ImageDraw.Draw(img)

    # mascote em círculo
    if MASCOT.exists():
        size = 330
        m = Image.open(MASCOT).convert("RGB").resize((size, size), Image.LANCZOS)
        circ = Image.new("L", (size, size), 0)
        ImageDraw.Draw(circ).ellipse([0, 0, size - 1, size - 1], fill=255)
        img.paste(m, (835, 150), circ)
        d.ellipse([835, 150, 835 + size, 150 + size], outline=(255, 255, 255), width=5)

    title = font("Montserrat-Regular.ttf", 82, 800)
    sub = font("Montserrat-Regular.ttf", 29, 500)
    eyebrow = font("Montserrat-Regular.ttf", 20, 600)

    d.text((86, 116), "SUA ASSISTENTE DE MARKETING COM IA", font=eyebrow, fill=(226, 208, 240))
    d.text((82, 158), "Seu marketing,", font=title, fill=WHITE)
    d.text((82, 248), "com mais", font=title, fill=WHITE)
    d.text((82, 338), "direção.", font=title, fill=LILAC_TXT)
    d.text((86, 462), "Você participa. Você revisa. Você aprova.", font=sub, fill=(236, 224, 244))
    d.text((86, 516), "@use_nelis.ia", font=sub, fill=LILAC_TXT)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"gerado: {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
