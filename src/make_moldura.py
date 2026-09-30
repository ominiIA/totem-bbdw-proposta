#!/usr/bin/env python3
"""Monta o conceito de moldura 10×15 do BBDW sobre uma foto gerada pelo totem."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1200, 1800
YELLOW, BLUE, INDIGO, CYAN, INK = "#FCFC30", "#465EFF", "#3333BD", "#54DCFC", "#07080F"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

photo_path = sys.argv[1] if len(sys.argv) > 1 else "img/gen/futuro-jovem.png"
out_path = sys.argv[2] if len(sys.argv) > 2 else "img/out/moldura-bbdw.jpg"

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# faixas diagonais no rodapé
for i, color in enumerate([YELLOW, BLUE, INDIGO]):
    x0 = -260 + i * 170
    d.polygon([(x0, H), (x0 + 120, H), (x0 + 520, H - 400), (x0 + 400, H - 400)], fill=color)

# foto
M, TOP, BOTTOM = 56, 196, 1480
pw, ph = W - 2 * M, BOTTOM - TOP
photo = ImageOps.fit(Image.open(photo_path).convert("RGB"), (pw, ph), centering=(0.5, 0.35))
img.paste(photo, (M, TOP))
d.rectangle([M, TOP, M + pw - 1, TOP + 10], fill=YELLOW)

# cabeçalho
big = ImageFont.truetype(FONT_BLACK, 70)
small = ImageFont.truetype(FONT_BOLD, 30)
d.text((M, 60), "BB DIGITAL WEEK", font=big, fill="white")
tw = d.textlength("BB DIGITAL WEEK ", font=big)
d.text((M + tw, 60), "2026", font=big, fill=YELLOW)

# rodapé
d.text((W - M, BOTTOM + 60), "27 A 29 DE OUTUBRO · BRASÍLIA", font=small, fill="white", anchor="ra")
d.text((W - M, BOTTOM + 104), "Ulysses Centro de Convenções", font=ImageFont.truetype(FONT_BOLD, 26),
       fill="#9A9EB2", anchor="ra")
logo = Image.open("img/out/logo-cria-white.png")
logo = logo.resize((360, int(360 * logo.height / logo.width)), Image.LANCZOS)
img.paste(logo, (W - M - logo.width, H - 70 - logo.height), logo)

img.save(out_path, quality=90)
print("ok", out_path)
