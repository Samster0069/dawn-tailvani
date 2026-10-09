#!/usr/bin/env python3
"""Compose the 'boutique window' hero art for each skin: graded photo in an arch,
a thin offset arch line (echo of the logo), and VectorCraft props dressing the window.
Output: transparent PNG 1320x1560 (artwork/hero/<skin>.png) + a preview on the band colour."""
import sys, os
sys.path.insert(0, '/home/claude/craft')
from PIL import Image, ImageDraw, ImageOps, ImageFilter
from skin_palettes import SKINS

CW, CH = 1320, 1560
AX, AY, AW, AH = 200, 90, 960, 1380          # arch box
OFF = (-44, -40)                              # offset outline arch
SS = 2                                        # supersample for smooth edges
# prop slots: (cx, cy, size, rotation)
SLOTS = [(232, 1305, 380, -12), (1148, 318, 270, 16), (118, 600, 160, -18), (1192, 1050, 245, 8),
         (412, 1450, 170, 10), (1012, 160, 130, -10), (950, 1478, 170, -6)]
CENTER = {  # focal point (x, y) for the arch crop, 0..1
 'base': (0.5, 0.45), 'bfcm-2026': (0.6, 0.6), 'spring-2027': (0.42, 0.45), 'holidays-2026': (0.5, 0.3),
 'new-year-2027': (0.5, 0.55), 'thanksgiving-2026': (0.5, 0.55), 'fourth-of-july-2027': (0.45, 0.45),
}

def hexrgb(h, a=255):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

def arch_mask(w, h, ss=SS):
    m = Image.new('L', (w*ss, h*ss), 0); d = ImageDraw.Draw(m)
    r = w*ss//2
    d.rectangle([0, r, w*ss, h*ss], fill=255); d.ellipse([0, 0, w*ss, w*ss], fill=255)
    return m.resize((w, h), Image.LANCZOS)

def arch_outline(w, h, width, color, ss=SS):
    im = Image.new('RGBA', (w*ss, h*ss), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    r = w*ss//2; lw = width*ss
    d.arc([lw//2, lw//2, w*ss - lw//2, w*ss - lw//2], 180, 360, fill=color, width=lw)
    d.line([lw//2, r, lw//2, h*ss], fill=color, width=lw)
    d.line([w*ss - lw//2 - 1, r, w*ss - lw//2 - 1, h*ss], fill=color, width=lw)
    return im.resize((w, h), Image.LANCZOS)

def compose(skin):
    pal = SKINS[skin]
    canvas = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    # 1. thin offset arch (logo echo)
    ol = arch_outline(AW, AH - 60, 5, hexrgb(pal['dark'], 200))
    canvas.alpha_composite(ol, (AX + OFF[0], AY + OFF[1]))
    # 2. photo in the arch
    photo = Image.open(f'/home/claude/craft/artwork/graded/{skin}-photo.jpg').convert('RGB')
    photo = ImageOps.fit(photo, (AW, AH), Image.LANCZOS, centering=CENTER.get(skin, (0.5, 0.42)))
    m = arch_mask(AW, AH)
    canvas.paste(photo, (AX, AY), m)
    # 3. props with a soft shadow
    for i, (cx, cy, size, rot) in enumerate(SLOTS):
        name = pal['props'][i % len(pal['props'])]
        p = Image.open(f'/home/claude/craft/artwork/props/{skin}/{name}.png').convert('RGBA')
        p = p.resize((size, size), Image.LANCZOS).rotate(rot, resample=Image.BICUBIC, expand=True)
        sh = Image.new('RGBA', p.size, hexrgb(pal['dark'], 0))
        a = p.split()[3].point(lambda v: int(v * 0.22))
        sh.putalpha(a); sh = sh.filter(ImageFilter.GaussianBlur(10))
        x, y = cx - p.width//2, cy - p.height//2
        canvas.alpha_composite(sh, (x + 6, y + 12)); canvas.alpha_composite(p, (x, y))
    os.makedirs('/home/claude/craft/artwork/hero', exist_ok=True)
    canvas.save(f'/home/claude/craft/artwork/hero/{skin}.png', optimize=True)
    prev = Image.new('RGBA', (CW, CH), hexrgb(pal['hero'])); prev.alpha_composite(canvas)
    return prev.convert('RGB')

if __name__ == '__main__':
    skins = sys.argv[1:] or list(SKINS)
    previews = [(s, compose(s)) for s in skins]
    # contact sheet
    tw, th = 330, 390; cols = 6
    rows = (len(previews) + cols - 1)//cols
    sheet = Image.new('RGB', (cols*tw, rows*(th+18)), 'white'); d = ImageDraw.Draw(sheet)
    for i, (s, im) in enumerate(previews):
        x, y = (i % cols)*tw, (i//cols)*(th+18)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y)); d.text((x+4, y+th+3), s, fill='black')
    sheet.save('/home/claude/craft/sheets/heroes.jpg', quality=85)
