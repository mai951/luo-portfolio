"""Clean magazine-style collage. NO distortion — crop, don't stretch.
Reference principles:
- Center-crop to fill frames, never deform aspect ratio
- Generous whitespace, thin borders, subtle shadows
- Consistent row heights within each band
"""
import os, glob
from PIL import Image, ImageFilter, ImageOps

SRC = r"D:\ai\02 输出\测试\images\邯郸茅台文化体验馆"
OUT = r"D:\ai\01输出\luo-portfolio-master\images\邯郸茅台文化体验馆"

# ── Main page color scheme (NOT crimson) ──
PRIMARY   = (15, 10, 42)     # #0f0a2a — deep indigo
BG_DARK   = (18, 13, 48)     # slightly lighter for gradient base
ACCENT    = (99, 102, 241)    # #6366f1
ACCENT_LT = (129, 140, 248)   # #818cf8
WHITE     = (255, 255, 255)
BG_WARM   = (250, 249, 246)   # #faf9f6 — warm off-white
BORDER_C  = (220, 218, 214)   # subtle border
SHADOW_C  = (0, 0, 0)


def center_crop(img, target_w, target_h):
    """Center-crop to target aspect ratio WITHOUT distortion, then resize."""
    tw, th = target_w, target_h
    iw, ih = img.size
    target_ratio = tw / th
    image_ratio = iw / ih

    if image_ratio > target_ratio:
        # Image wider — crop width
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        # Image taller — crop height
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))

    return img.resize((tw, th), Image.LANCZOS)


def shadow_bg(w, h, margin=20):
    """Return a white background with a soft shadow-ready canvas."""
    bg = Image.new("RGB", (w, h), BG_WARM)
    return bg


def paste_card(bg, img, x, y, card_w, card_h):
    """Paste an image as a 'card' — white border + soft shadow."""
    border = 6
    shadow_off = 3
    # Shadow
    sd = Image.new("RGB", (card_w + 8, card_h + 8), (230, 228, 224))
    sd = sd.filter(ImageFilter.GaussianBlur(3))
    bg.paste(sd, (x - 2, y - 2))
    # White card
    card = Image.new("RGB", (card_w + border*2, card_h + border*2), WHITE)
    card.paste(img, (border, border))
    bg.paste(card, (x - border, y - border))
    return bg


# ═══════════════════════════════
# COLLAGE 1 — 原始现场 & 施工过程 (7 images → 1+3+3)
# ═══════════════════════════════
def make_original():
    folder = os.path.join(SRC, "过程及原始")
    files = sorted(glob.glob(os.path.join(folder, "*")))
    if not files: return print("No files")
    imgs = [Image.open(f).convert("RGB") for f in files[:7]]

    # Canvas: landscape magazine spread
    W, H = 1600, 900
    bg = Image.new("RGB", (W, H), BG_WARM)

    margin = 28
    gap = 12
    usable_w = W - margin * 2

    # Row 1: 3 images, landscape
    r1_y = margin
    r1_h = 340
    r1_w = (usable_w - gap * 2) // 3
    for i in range(3):
        c = center_crop(imgs[i], r1_w, r1_h)
        x = margin + i * (r1_w + gap)
        paste_card(bg, c, x, r1_y, r1_w, r1_h)

    # Row 2: 4 images, smaller
    r2_y = r1_y + r1_h + 24 + gap
    r2_h = 420
    r2_w = (usable_w - gap * 3) // 4
    for i in range(4):
        idx = 3 + i
        if idx >= len(imgs): break
        c = center_crop(imgs[idx], r2_w, r2_h)
        x = margin + i * (r2_w + gap)
        paste_card(bg, c, x, r2_y, r2_w, r2_h)

    out = os.path.join(OUT, "poster_01_original.jpg")
    bg.save(out, quality=94)
    print(f"OK: poster_01 ({W}x{H})")


# ═══════════════════════════════
# COLLAGE 2 — 效果图 (7 images → 1 large + 6 smaller)
# ═══════════════════════════════
def make_render():
    folder = os.path.join(SRC, "效果图")
    files = sorted(glob.glob(os.path.join(folder, "*")))
    if not files: return print("No files")
    imgs = [Image.open(f).convert("RGB") for f in files[:7]]

    W, H = 1600, 880
    bg = Image.new("RGB", (W, H), BG_WARM)
    margin = 28
    gap = 12
    usable_w = W - margin * 2

    # Left: 1 large hero image
    hero_w = 620
    hero_h = H - margin * 2
    c = center_crop(imgs[0], hero_w, hero_h)
    paste_card(bg, c, margin, margin, hero_w, hero_h)

    # Right: 3 rows × 2 cols grid
    right_x = margin + hero_w + gap * 2
    right_w = usable_w - hero_w - gap * 2
    cell_w = (right_w - gap) // 2
    cell_h = (hero_h - gap * 2) // 3
    right_y = margin

    for row in range(3):
        for col in range(2):
            idx = 1 + row * 2 + col
            if idx >= len(imgs): break
            c = center_crop(imgs[idx], cell_w, cell_h)
            x = right_x + col * (cell_w + gap)
            y = right_y + row * (cell_h + gap)
            paste_card(bg, c, x, y, cell_w, cell_h)

    out = os.path.join(OUT, "poster_02_render.jpg")
    bg.save(out, quality=94)
    print(f"OK: poster_02 ({W}x{H})")


# ═══════════════════════════════
# COLLAGE 3 — 实际落地 (8 images → masonry style: 2+3+3)
# ═══════════════════════════════
def make_final():
    folder = os.path.join(SRC, "现场图")
    files = sorted(glob.glob(os.path.join(folder, "*")))
    if not files: return print("No files")
    imgs = [Image.open(f).convert("RGB") for f in files[:8]]

    W, H = 1600, 920
    bg = Image.new("RGB", (W, H), BG_WARM)
    margin = 28
    gap = 12
    usable_w = W - margin * 2

    # Row 1: 2 wide images
    r1_h = 320
    r1_w = (usable_w - gap) // 2
    r1_y = margin
    for i in range(2):
        c = center_crop(imgs[i], r1_w, r1_h)
        x = margin + i * (r1_w + gap)
        paste_card(bg, c, x, r1_y, r1_w, r1_h)

    # Row 2: 3 images
    r2_y = r1_y + r1_h + gap
    r2_h = 280
    r2_w = (usable_w - gap * 2) // 3
    for i in range(3):
        idx = 2 + i
        if idx >= len(imgs): break
        c = center_crop(imgs[idx], r2_w, r2_h)
        x = margin + i * (r2_w + gap)
        paste_card(bg, c, x, r2_y, r2_w, r2_h)

    # Row 3: 3 images
    r3_y = r2_y + r2_h + gap
    r3_h = H - r3_y - margin
    r3_w = (usable_w - gap * 2) // 3
    for i in range(3):
        idx = 5 + i
        if idx >= len(imgs): break
        c = center_crop(imgs[idx], r3_w, r3_h)
        x = margin + i * (r3_w + gap)
        paste_card(bg, c, x, r3_y, r3_w, r3_h)

    out = os.path.join(OUT, "poster_03_final.jpg")
    bg.save(out, quality=94)
    print(f"OK: poster_03 ({W}x{H})")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    make_original()
    make_render()
    make_final()
    print("\nDone — no distortion, clean magazine layout.")
