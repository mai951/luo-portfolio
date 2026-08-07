"""Create collage comparison images for Handan Moutai project page."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = r"D:\ai\01输出\luo-portfolio-master\images\邯郸茅台文化体验馆"
SRC = os.path.join(BASE, "source")

# Try to find a CJK font
FONT_PATH = None
candidates = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
    r"C:\Windows\Fonts\NotoSansCJKsc-Regular.otf",
]
for c in candidates:
    if os.path.exists(c):
        FONT_PATH = c
        break

def load_img(path, target_w):
    img = Image.open(path).convert("RGB")
    ratio = target_w / img.width
    h = int(img.height * ratio)
    return img.resize((target_w, h), Image.LANCZOS)

def add_label(draw, text, x, y, font_lg, w, color="#FFFFFF"):
    """Add a text label with semi-transparent background."""
    bbox = draw.textbbox((0, 0), text, font=font_lg)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 12
    # Center the label
    lx = x + (w - tw - pad*2) // 2
    ly = y + 8
    draw.rectangle([lx, ly, lx + tw + pad*2, ly + th + pad], fill=(0, 0, 0, 140))
    draw.text((lx + pad, ly + pad//2), text, fill=color, font=font_lg)

def make_collage_3panel(img1_path, img2_path, img3_path, labels, out_path, panel_w=900):
    """3-panel horizontal collage: 原始现场 → 效果图 → 落地实景"""
    imgs = [load_img(p, panel_w) for p in [img1_path, img2_path, img3_path]]
    max_h = max(i.height for i in imgs)
    # Pad to same height
    padded = []
    for i in imgs:
        if i.height < max_h:
            new_i = Image.new("RGB", (panel_w, max_h), (20, 15, 20))
            new_i.paste(i, (0, (max_h - i.height)//2))
            padded.append(new_i)
        else:
            padded.append(i)

    gap = 4
    total_w = panel_w * 3 + gap * 2
    total_h = max_h + 60  # space for labels
    canvas = Image.new("RGB", (total_w, total_h), (20, 15, 20))

    for idx, img in enumerate(padded):
        x = idx * (panel_w + gap)
        canvas.paste(img, (x, 60))

    draw = ImageDraw.Draw(canvas)
    try:
        font_lg = ImageFont.truetype(FONT_PATH, 28) if FONT_PATH else ImageFont.load_default()
        font_title = ImageFont.truetype(FONT_PATH, 36) if FONT_PATH else ImageFont.load_default()
    except:
        font_lg = ImageFont.load_default()
        font_title = ImageFont.load_default()

    for idx, label in enumerate(labels):
        x = idx * (panel_w + gap)
        add_label(draw, label, x, 0, font_lg, panel_w)

    canvas.save(out_path, quality=92)
    print(f"Created: {out_path} ({total_w}x{total_h})")
    return canvas

def make_collage_2panel(img1_path, img2_path, labels, out_path, panel_w=1000):
    """2-panel side-by-side comparison."""
    imgs = [load_img(p, panel_w) for p in [img1_path, img2_path]]
    max_h = max(i.height for i in imgs)
    padded = []
    for i in imgs:
        if i.height < max_h:
            new_i = Image.new("RGB", (panel_w, max_h), (20, 15, 20))
            new_i.paste(i, (0, (max_h - i.height)//2))
            padded.append(new_i)
        else:
            padded.append(i)

    gap = 4
    total_w = panel_w * 2 + gap
    total_h = max_h + 60
    canvas = Image.new("RGB", (total_w, total_h), (20, 15, 20))
    for idx, img in enumerate(padded):
        x = idx * (panel_w + gap)
        canvas.paste(img, (x, 60))

    draw = ImageDraw.Draw(canvas)
    try:
        font_lg = ImageFont.truetype(FONT_PATH, 28) if FONT_PATH else ImageFont.load_default()
    except:
        font_lg = ImageFont.load_default()

    for idx, label in enumerate(labels):
        x = idx * (panel_w + gap)
        add_label(draw, label, x, 0, font_lg, panel_w)

    canvas.save(out_path, quality=92)
    print(f"Created: {out_path} ({total_w}x{total_h})")
    return canvas

def make_grid_2x2(img_paths, labels, out_path, cell_w=700):
    """2x2 grid collage."""
    imgs = [load_img(p, cell_w) for p in img_paths]
    max_h = max(i.height for i in imgs)
    padded = []
    for i in imgs:
        if i.height < max_h:
            new_i = Image.new("RGB", (cell_w, max_h), (20, 15, 20))
            new_i.paste(i, (0, (max_h - i.height)//2))
            padded.append(new_i)
        else:
            padded.append(i)

    gap = 4
    label_h = 50
    total_w = cell_w * 2 + gap
    total_h = (max_h + label_h) * 2 + gap
    canvas = Image.new("RGB", (total_w, total_h), (20, 15, 20))

    draw = ImageDraw.Draw(canvas)
    try:
        font_sm = ImageFont.truetype(FONT_PATH, 22) if FONT_PATH else ImageFont.load_default()
    except:
        font_sm = ImageFont.load_default()

    positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for pos, img, label in zip(positions, padded, labels):
        col, row = pos
        x = col * (cell_w + gap)
        y = row * (max_h + label_h) + label_h
        canvas.paste(img, (x, y))
        add_label(draw, label, x, row * (max_h + label_h), font_sm, cell_w)

    canvas.save(out_path, quality=92)
    print(f"Created: {out_path} ({total_w}x{total_h})")
    return canvas


if __name__ == "__main__":
    # === Collage 1: 前厅空间演变 ===
    make_collage_3panel(
        os.path.join(SRC, "orig_01.jpg"),
        os.path.join(SRC, "render_01.png"),
        os.path.join(SRC, "final_01.jpg"),
        ["原始现场 · 2024.01", "效果图 · 2025.03", "落成实景 · 2026"],
        os.path.join(BASE, "collage_01_evolution.jpg"),
        panel_w=900,
    )

    # === Collage 2: 效果图 vs 落地 ===
    make_collage_2panel(
        os.path.join(SRC, "render_02.png"),
        os.path.join(SRC, "final_02.jpg"),
        ["效果图方案 · 2025", "落地实景 · 2026"],
        os.path.join(BASE, "collage_02_compare.jpg"),
        panel_w=1000,
    )

    # === Collage 3: 施工过程 ===
    make_grid_2x2(
        [
            os.path.join(SRC, "orig_02.jpg"),
            os.path.join(SRC, "orig_03.jpg"),
            os.path.join(SRC, "render_03.png"),
            os.path.join(SRC, "final_03.jpg"),
        ],
        ["原始场地测量", "结构改造阶段", "效果图方案", "完工实景"],
        os.path.join(BASE, "collage_03_process.jpg"),
        cell_w=800,
    )

    print("\n✅ All collages created!")
