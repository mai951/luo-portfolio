"""Generate poster collages for 朗樾园 / 茅台专卖店 / 茅友宴 (邯郸-style, indigo).
Same engine as make_posters.py — center-crop, card+shadow, no distortion.
Layout adapts to image count: 1→single, 2→2-wide, 3-6→2 rows, 7+→3 rows.
"""
import os, glob
from PIL import Image, ImageFilter

SRC_BASE = r"D:\ai\02 输出\测试\images"
OUT_BASE = r"D:\ai\01输出\luo-portfolio-master\images"

BG_WARM = (250, 249, 246)
WHITE   = (255, 255, 255)

def center_crop(img, tw, th):
    iw, ih = img.size
    tr, ir = tw/th, iw/ih
    if ir > tr:
        nw = int(ih*tr); l = (iw-nw)//2; img = img.crop((l,0,l+nw,ih))
    else:
        nh = int(iw/tr); t = (ih-nh)//2; img = img.crop((0,t,iw,t+nh))
    return img.resize((tw,th), Image.LANCZOS)

def paste_card(bg, img, x, y, w, h):
    b = 6
    sd = Image.new("RGB", (w+8,h+8), (230,228,224)); sd = sd.filter(ImageFilter.GaussianBlur(3))
    bg.paste(sd, (x-2,y-2))
    card = Image.new("RGB", (w+b*2,h+b*2), WHITE)
    img = img.resize((w,h), Image.LANCZOS)
    card.paste(img, (b,b)); bg.paste(card, (x,y))

def rows_for(n):
    """Auto layout rows for n images."""
    if n <= 1: return [(1, 840)]
    if n == 2: return [(2, 420)]
    if n <= 4: return [(2, 420), (2, 420)]
    if n <= 6: return [(3, 300), (3, 290)]
    return [(3, 300), (3, 290), (3, 270)]

def make_collage(folder, out):
    files = sorted(glob.glob(os.path.join(folder,"*")))
    files = [f for f in files if f.lower().endswith((".jpg",".jpeg",".png"))]
    if not files: print(f"  (skip, no files in {folder})"); return
    imgs = [Image.open(f).convert("RGB") for f in files[:9]]
    rows = rows_for(len(imgs))
    W, H = 1600, 920
    bg = Image.new("RGB",(W,H),BG_WARM)
    margin, gap = 28, 12
    usable = W - margin*2
    y = margin
    idx = 0
    for n, rh in rows:
        rw = (usable - gap*(n-1))//n
        for i in range(n):
            if idx >= len(imgs): break
            x = margin + i*(rw+gap)
            paste_card(bg, center_crop(imgs[idx],rw,rh), x, y, rw, rh)
            idx += 1
        y += rh + gap
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bg.save(out, quality=94)
    print(f"  OK: {os.path.basename(out)} ({len(imgs)} imgs, {len(rows)} rows)")

PROJECTS = ["朗樾园", "茅台专卖店", "茅友宴"]
for name in PROJECTS:
    src = os.path.join(SRC_BASE, name)
    out = os.path.join(OUT_BASE, name)
    print(f"═══ {name} ═══")
    make_collage(os.path.join(src,"过程及原始"), os.path.join(out,"poster_01_original.jpg"))
    make_collage(os.path.join(src,"效果图"),    os.path.join(out,"poster_02_render.jpg"))
    make_collage(os.path.join(src,"现场图"),    os.path.join(out,"poster_03_final.jpg"))
print("\nDone.")
