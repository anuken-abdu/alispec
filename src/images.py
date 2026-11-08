# -*- coding: utf-8 -*-
"""Фото: orig/*.jpg → assets/img/{имя}-{ширина}.webp (без EXIF/GPS). Запуск: python3 src/images.py
Кадрирование под 4:3 (карточки) и 4:5 (первый экран); новые фото клиента добавлять в CROPS."""
from pathlib import Path
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parent.parent
O = ROOT / "orig"; A = ROOT / "assets" / "img"; A.mkdir(parents=True, exist_ok=True)
# имя: (файл, соотношение, центр кадра по x и y в долях)
CROPS = {"hero": ("hero-2.jpg", (4, 5), .5, .42), "m25": ("manip-25t.jpg", (4, 3), .5, .47), "m20": ("hero-3.jpg", (4, 3), .5, .45),
         "m12": ("manip-12t.jpg", (4, 3), .5, .42), "m7": ("manip-7t.jpg", (4, 3), .5, .5), "g1": ("hero-1.jpg", (4, 3), .5, .42),
         "g2": ("manip-5t.jpg", (4, 3), .5, .6), "g3": ("manip-15t.jpg", (4, 3), .5, .5), "g4": ("hero-2.jpg", (4, 3), .5, .46)}
WIDTHS = [480, 800, 1200]
def crop(im, ratio, cx, cy):
    W, H = im.size; rw, rh = ratio
    if W / H > rw / rh: w, h = int(H * rw / rh), H
    else: w, h = W, int(W * rh / rw)
    x0 = min(max(0, int(cx * W - w / 2)), W - w); y0 = min(max(0, int(cy * H - h / 2)), H - h)
    return im.crop((x0, y0, x0 + w, y0 + h))
SIZES = {}
for name, (f, ratio, cx, cy) in CROPS.items():
    im = ImageOps.exif_transpose(Image.open(O / f)).convert("RGB")
    if f == "hero-1.jpg":                                   # у кадра чёрные поля сверху и снизу
        g = im.convert("L"); rows = [y for y in range(im.height) if sum(g.crop((0, y, im.width, y + 1)).getdata()) / im.width > 18]
        im = im.crop((0, rows[0], im.width, rows[-1]))
    im = crop(im, ratio, cx, cy); ws = []
    for w in WIDTHS:
        if w > im.width and ws: break
        ww = min(w, im.width); r = im.resize((ww, round(im.height * ww / im.width)), Image.LANCZOS)
        r.save(A / f"{name}-{w}.webp", "WEBP", quality=70, method=6); ws.append(w)
    SIZES[name] = (ws, ratio)
    print(name, im.size, ws, [round((A / f"{name}-{w}.webp").stat().st_size / 1024) for w in ws], "KB")
