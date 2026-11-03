"""Tailvani social post generator.

Makes magazine-ad style social posts (deliberately unlike the website):
  image  -> 1080x1350 JPEG (4:5, works on Instagram, Facebook, TikTok photo, Pinterest)
  video  -> 1080x1920 MP4 H.264 + AAC, ~9 s, with an original music bed

Usage:  python3 tvsocial.py spec.json out_basename
spec.json:
{
  "format": "image" | "video",
  "template": "cover" | "split" | "thisorthat" | "edit"      (image only; video ignores)
  "palette": "fall" | "winter" | "holiday" | "brand" | "valentine" | "spring" | "summer",
  "kicker": "THE CAT EDIT",              short caps line (optional)
  "headline": "Sweater weather",         2-4 words work best
  "sub": "Fleece-lined for chilly mornings",   optional, one short line
  "offer": "10% off with WELCOME",       optional sticker text ("" to hide)
  "products": [ {"title": "...", "price": "30", "photo": "https://cdn.shopify.com/..."} , ...]
}
Rules baked in: product name + price always shown in small print; logo small;
JPEG only for images (TikTok/Instagram reject PNG/WebP in places).
"""
import io, json, math, os, random, subprocess, sys, tempfile, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
W, H = 1080, 1350
VW, VH, FPS = 1080, 1920, 30

PALETTES = {
    # bg = big colour block, ink = text on cream, cream = light, pop = accent/sticker, deep = dark text block
    "fall":      dict(bg="#5B1A22", deep="#2A1712", cream="#F6EBDD", pop="#E8743B", soft="#E9B9AE", alt="#D9A441"),
    "winter":    dict(bg="#1F3A4A", deep="#14222B", cream="#F3F1EC", pop="#E0A458", soft="#B9CED6", alt="#8FB3C2"),
    "holiday":   dict(bg="#1F3B2D", deep="#132219", cream="#F7F0E6", pop="#C8323A", soft="#E8C9A0", alt="#D9A441"),
    "brand":     dict(bg="#3B2418", deep="#22150E", cream="#F6EBDD", pop="#D97B5A", soft="#E9B9AE", alt="#8E9E7A"),
    "valentine": dict(bg="#7A1F35", deep="#3A0E18", cream="#FBEFEF", pop="#F08AA0", soft="#F5C6CF", alt="#E8743B"),
    "spring":    dict(bg="#4E6B4A", deep="#22301F", cream="#F7F3E8", pop="#F2A65A", soft="#F4C7C3", alt="#D9C36A"),
    "summer":    dict(bg="#1E5A6B", deep="#0F2E37", cream="#FBF4E6", pop="#F2994A", soft="#F7D08A", alt="#E86A5C"),
}


# ---------------------------------------------------------------- fonts
def font(kind, size, wght=None):
    files = {"serif": "BodoniModa.ttf", "italic": "BodoniModa-Italic.ttf",
             "sans": "Archivo.ttf", "hand": "Caveat.ttf"}
    f = ImageFont.truetype(os.path.join(FONTS, files[kind]), size)
    try:
        axes = f.get_variation_axes()
        vals = []
        for a in axes:
            n = a["name"]
            n = n.decode() if isinstance(n, bytes) else n
            if n == "Weight":
                vals.append(wght or {"serif": 700, "italic": 600, "sans": 600, "hand": 700}[kind])
            elif n == "Optical size":
                vals.append(min(max(size / 3, a["minimum"]), a["maximum"]))
            elif n == "Width":
                vals.append(a["minimum"] if kind == "sans" else a["default"])
            else:
                vals.append(a["default"])
        f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f


def hexrgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def tw(draw, text, f, tracking=0):
    if not text:
        return 0
    return draw.textlength(text, font=f) + tracking * (len(text) - 1)


def draw_tracked(draw, xy, text, f, fill, tracking=0, anchor="ls"):
    x, y = xy
    total = tw(draw, text, f, tracking)
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill, anchor="l" + anchor[1])
        x += draw.textlength(ch, font=f) + tracking


def fit_lines(draw, text, kind, max_w, max_size, min_size=40, max_lines=3, wght=None):
    """Largest font size at which text wraps into <= max_lines within max_w."""
    words = text.split()
    for size in range(max_size, min_size - 1, -4):
        f = font(kind, size, wght)
        lines, cur = [], ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if draw.textlength(t, font=f) <= max_w:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w_
        lines.append(cur)
        if len(lines) <= max_lines and all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, lines, size
    f = font(kind, min_size, wght)
    return f, [text], min_size


# ---------------------------------------------------------------- images
def fetch(url):
    if os.path.exists(url):
        return Image.open(url).convert("RGB")
    if "cdn.shopify.com" in url:
        url += ("&" if "?" in url else "?") + "format=pjpg"
    req = urllib.request.Request(url, headers={"Accept": "image/jpeg,*/*", "User-Agent": "tvsocial/1.0"})
    data = urllib.request.urlopen(req, timeout=60).read()
    return ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")


def is_studio(im):
    """True when the photo is a product shot on a plain white/near-white background."""
    a = np.asarray(im.resize((120, 120))).astype(int)
    edge = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    return (edge.min(axis=1) > 225).mean() > 0.7


def studio_on(im, size, bg):
    """Place a white-background product shot onto a coloured backdrop (multiply keeps it natural)."""
    tw_, th = size
    canvas = Image.new("RGB", size, bg[:3])
    s = min(tw_ * 0.92 / im.width, th * 0.92 / im.height)
    p = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    # soft-key the white background out so the product sits on the backdrop
    arr = np.asarray(p).astype(float)
    lum = arr.min(axis=2)
    alpha = np.clip((250 - lum) / 22.0, 0, 1)
    alpha = Image.fromarray((alpha * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
    canvas.paste(p, ((tw_ - p.width) // 2, th - p.height - int(th * 0.03)), alpha)
    return canvas


def cover_crop(im, size, focus=(0.5, 0.42)):
    out = ImageOps.fit(im, size, Image.LANCZOS, centering=focus)
    out = ImageEnhance.Sharpness(out).enhance(1.15)
    return out


def photo_panel(im, size, backdrop):
    if is_studio(im):
        return studio_on(im, size, backdrop)
    return cover_crop(im, size)


def grain(img, amount=7):
    n = np.random.default_rng(7).normal(0, amount, (img.height, img.width, 1))
    a = np.clip(np.asarray(img).astype(float) + n, 0, 255).astype("uint8")
    return Image.fromarray(a)


def logo(color, size):
    m = Image.open(os.path.join(HERE, "mark.png")).convert("RGB")
    lum = np.asarray(m.convert("L")).astype(float)
    alpha = np.clip((235 - lum) / 120.0, 0, 1)
    out = Image.new("RGBA", m.size, hexrgb(color))
    out.putalpha(Image.fromarray((alpha * 255).astype("uint8")))
    return out.resize((size, size), Image.LANCZOS)


def sticker(text, pal, d=230, rot=-12):
    """Round offer sticker, e.g. '10% off with WELCOME'."""
    s = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    dr = ImageDraw.Draw(s)
    dr.ellipse((0, 0, d - 1, d - 1), fill=hexrgb(pal["pop"]))
    dr.ellipse((10, 10, d - 11, d - 11), outline=hexrgb(pal["cream"]), width=2)
    parts = text.split(" with ")
    big = parts[0].upper()
    f1, l1, _ = fit_lines(dr, big, "sans", d * 0.66, int(d * 0.24), 18, 2, 800)
    y = d * 0.40 - (len(l1) - 1) * f1.size * 0.5
    for l in l1:
        dr.text((d / 2, y), l, font=f1, fill=hexrgb(pal["cream"]), anchor="mm")
        y += f1.size * 1.0
    if len(parts) > 1:
        f2 = font("sans", int(d * 0.085), 600)
        draw_tracked(dr, (d / 2, d * 0.72), "CODE " + parts[1].upper(), f2, hexrgb(pal["cream"]), 2, "mm")
    return s.rotate(rot, resample=Image.BICUBIC, expand=True)


def credit(dr, xy, prod, color, anchor="ls", size=26):
    """Small fashion-ad product credit: 'WEARING  Fleece-Lined Cat Hoodie · $30'."""
    f1 = font("sans", size, 700)
    f2 = font("sans", size, 400)
    label = "WEARING  " if prod.get("worn", True) else "SHOWN  "
    t2 = f"{prod['title']}  ·  ${float(prod['price']):.0f}"
    total = tw(dr, label, f1, 2) + tw(dr, t2, f2)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    draw_tracked(dr, (x, y), label, f1, color, 2, "l" + anchor[1])
    dr.text((x + tw(dr, label, f1, 2), y), t2, font=f2, fill=color, anchor="l" + anchor[1])


def footer_url(dr, xy, color, anchor="ls"):
    draw_tracked(dr, xy, "TAILVANI.COM", font("sans", 24, 700), color, 4, anchor)


def tilted_print(im, w, h, rot, pal, caption=None, border=18, bottom=70):
    card = Image.new("RGBA", (w, h), hexrgb("#FFFFFF"))
    ph = photo_panel(im, (w - 2 * border, h - border - bottom), hexrgb(pal["soft"]))
    card.paste(ph, (border, border))
    if caption:
        dr = ImageDraw.Draw(card)
        f, lines, _ = fit_lines(dr, caption, "hand", w - 2 * border, 46, 28, 1, 700)
        dr.text((w / 2, h - bottom / 2 + 2), lines[0], font=f, fill=hexrgb(pal["deep"]), anchor="mm")
    sh = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((30, 36, w + 30, h + 36), fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    sh.paste(card, (30, 30), card)
    return sh.rotate(rot, resample=Image.BICUBIC, expand=True)


# ---------------------------------------------------------------- templates (1080x1350)
def t_cover(spec, pal, photos):
    """Magazine cover: full-bleed photo, big masthead, cover line, credit."""
    p = spec["products"][0]
    im = photos[0]
    base = photo_panel(im, (W, H), hexrgb(pal["soft"])).convert("RGBA")
    # darken top + bottom for legibility
    g = Image.new("L", (1, H))
    for y in range(H):
        t = y / H
        g.putpixel((0, y), int(255 * (max(0, 0.30 - t) / 0.30 * 0.75 + max(0, t - 0.52) / 0.48 * 0.92)))
    shade = Image.new("RGBA", (W, H), hexrgb(pal["deep"]))
    shade.putalpha(g.resize((W, H)))
    base = Image.alpha_composite(base, shade)
    dr = ImageDraw.Draw(base)
    # masthead
    fm = font("serif", 128, 800)
    draw_tracked(dr, (W / 2, 175), "TAILVANI", fm, hexrgb(pal["cream"]), 10, "ms")
    if spec.get("kicker"):
        draw_tracked(dr, (W / 2, 225), spec["kicker"].upper(), font("sans", 26, 700), hexrgb(pal["cream"]), 6, "ms")
    # cover line bottom-left
    f, lines, size = fit_lines(dr, spec["headline"], "italic", W - 140, 150, 70, 2)
    y = H - 150 - (len(lines) - 1) * size * 0.95 - (60 if spec.get("sub") else 0)
    for l in lines:
        dr.text((70, y), l, font=f, fill=hexrgb(pal["cream"]), anchor="ls")
        y += size * 0.95
    if spec.get("sub"):
        dr.text((72, y - size * 0.95 + 62), spec["sub"], font=font("sans", 34, 500), fill=hexrgb(pal["cream"]), anchor="ls")
    dr.line((70, H - 92, W - 70, H - 92), fill=hexrgb(pal["cream"], 140), width=2)
    credit(dr, (70, H - 50), p, hexrgb(pal["cream"]))
    footer_url(dr, (W - 70, H - 50), hexrgb(pal["cream"]), "rs")
    if spec.get("offer"):
        s = sticker(spec["offer"], pal, 220, -10)
        base.alpha_composite(s, (W - s.width - 40, 270))
    return base


def t_split(spec, pal, photos):
    """Photo on top, deep colour block below with oversized headline (fashion ad)."""
    p = spec["products"][0]
    base = Image.new("RGBA", (W, H), hexrgb(pal["bg"]))
    ph_h = 820
    base.paste(photo_panel(photos[0], (W, ph_h), hexrgb(pal["soft"])), (0, 0))
    dr = ImageDraw.Draw(base)
    # logo + small kicker on the photo
    lg = logo(pal["cream"] if not is_studio(photos[0]) else pal["deep"], 96)
    base.alpha_composite(lg, (40, 34))
    if spec.get("kicker"):
        kf = font("sans", 24, 700)
        kt = spec["kicker"].upper()
        kw = tw(dr, kt, kf, 6)
        dr.rounded_rectangle((W - 50 - kw - 44, 52, W - 50, 104), radius=26, fill=hexrgb(pal["bg"]))
        draw_tracked(dr, (W - 72, 87), kt, kf, hexrgb(pal["cream"]), 6, "rs")
    # headline
    f, lines, size = fit_lines(dr, spec["headline"], "serif", W - 120, 170, 70, 2, 800)
    y = ph_h + 40 + size * 0.85
    for l in lines:
        dr.text((60, y), l, font=f, fill=hexrgb(pal["cream"]), anchor="ls")
        y += size * 0.92
    if spec.get("sub"):
        dr.text((62, y - size * 0.92 + 64), spec["sub"], font=font("italic", 40, 500), fill=hexrgb(pal["soft"]), anchor="ls")
    credit(dr, (60, H - 58), p, hexrgb(pal["cream"]))
    footer_url(dr, (W - 60, H - 58), hexrgb(pal["soft"]), "rs")
    # pop bar
    dr.rectangle((60, ph_h + 26, 200, ph_h + 34), fill=hexrgb(pal["pop"]))
    if spec.get("offer"):
        s = sticker(spec["offer"], pal, 210, 12)
        base.alpha_composite(s, (W - s.width - 30, ph_h - s.height // 2 - 10))
    return base


def t_thisorthat(spec, pal, photos):
    """Engagement post: two products as tilted prints, 'This or that?'"""
    a, b = spec["products"][:2]
    base = Image.new("RGBA", (W, H), hexrgb(pal["cream"]))
    dr = ImageDraw.Draw(base)
    # big colour band
    dr.rectangle((0, 0, W, 470), fill=hexrgb(pal["bg"]))
    f = font("italic", 140, 600)
    dr.text((W / 2, 215), spec.get("headline") or "This or that?", font=f, fill=hexrgb(pal["cream"]), anchor="ms")
    if spec.get("kicker"):
        draw_tracked(dr, (W / 2, 95), spec["kicker"].upper(), font("sans", 26, 700), hexrgb(pal["soft"]), 6, "ms")
    if spec.get("sub"):
        dr.text((W / 2, 300), spec["sub"], font=font("sans", 36, 500), fill=hexrgb(pal["cream"]), anchor="ms")
    for i, (prod, im, rot, x) in enumerate([(a, photos[0], 4, 40), (b, photos[1], -4, 548)]):
        pr = tilted_print(im, 480, 620, rot, pal, None, 16, 16)
        base.alpha_composite(pr, (x - 20, 360))
        num = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        nd = ImageDraw.Draw(num)
        nd.ellipse((0, 0, 119, 119), fill=hexrgb(pal["pop"]))
        nd.text((60, 64), str(i + 1), font=font("serif", 74, 800), fill=hexrgb(pal["cream"]), anchor="mm")
        base.alpha_composite(num, (x + 170, 330))
        cx = x + 240
        tf, tl, _ = fit_lines(dr, prod["title"], "sans", 440, 30, 20, 2, 700)
        yy = 1085
        for l in tl:
            dr.text((cx, yy), l, font=tf, fill=hexrgb(pal["deep"]), anchor="ms")
            yy += tf.size * 1.2
        dr.text((cx, yy + 8), f"${float(prod['price']):.0f}", font=font("serif", 44, 700), fill=hexrgb(pal["bg"]), anchor="ms")
    draw_tracked(dr, (W / 2, H - 50), "COMMENT 1 OR 2  ·  TAILVANI.COM", font("sans", 26, 700), hexrgb(pal["deep"]), 4, "ms")
    return base


def t_edit(spec, pal, photos):
    """'The edit' list: 3 products as prints with numbered captions on a colour field."""
    prods = spec["products"][:3]
    base = Image.new("RGBA", (W, H), hexrgb(pal["bg"]))
    dr = ImageDraw.Draw(base)
    if spec.get("kicker"):
        draw_tracked(dr, (70, 110), spec["kicker"].upper(), font("sans", 26, 700), hexrgb(pal["soft"]), 6, "ls")
    f, lines, size = fit_lines(dr, spec["headline"], "serif", W - 140, 140, 60, 2, 800)
    y = 110 + size * 1.0
    for l in lines:
        dr.text((66, y), l, font=f, fill=hexrgb(pal["cream"]), anchor="ls")
        y += size * 0.95
    top = int(y + 40)
    spots = [(60, top + 30, -5), (380, top + 90, 3), (700, top + 20, -2)]
    if len(prods) == 2:
        spots = [(110, top + 20, -4), (560, top + 50, 4)]
    pw = 340 if len(prods) == 3 else 430
    for i, (prod, im) in enumerate(zip(prods, photos)):
        x, yy, rot = spots[i]
        pr = tilted_print(im, pw, int(pw * 1.32), rot, pal, f"{i + 1}. {prod['title'].split(' with ')[0]}", 14, 74)
        base.alpha_composite(pr, (x - 30, yy))
    dr = ImageDraw.Draw(base)
    ytxt = H - 150
    for i, prod in enumerate(prods):
        pass
    prices = "   ".join(f"{i + 1}. ${float(p_['price']):.0f}" for i, p_ in enumerate(prods))
    dr.text((70, ytxt), prices, font=font("serif", 46, 700), fill=hexrgb(pal["cream"]), anchor="ls")
    if spec.get("sub"):
        dr.text((70, ytxt + 52), spec["sub"], font=font("sans", 30, 500), fill=hexrgb(pal["soft"]), anchor="ls")
    footer_url(dr, (W - 70, H - 50), hexrgb(pal["cream"]), "rs")
    base.alpha_composite(logo(pal["cream"], 84), (W - 84 - 50, 50))
    if spec.get("offer"):
        s = sticker(spec["offer"], pal, 190, -12)
        base.alpha_composite(s, (W - s.width - 20, ytxt - s.height + 10))
    return base


TEMPLATES = {"cover": t_cover, "split": t_split, "thisorthat": t_thisorthat, "edit": t_edit}


def make_image(spec, out):
    pal = PALETTES.get(spec.get("palette", "brand"), PALETTES["brand"])
    photos = [fetch(p["photo"]) for p in spec["products"]]
    img = TEMPLATES[spec.get("template", "split")](spec, pal, photos).convert("RGB")
    img = grain(img, 4)
    img.save(out, "JPEG", quality=92, optimize=True, progressive=False, subsampling=0)
    return out


# ---------------------------------------------------------------- music (original, generated)
def music(seconds, path, seed=3, key=0):
    sr = 44100
    n = int(seconds * sr)
    t = np.arange(n) / sr
    bpm = 92
    beat = 60 / bpm
    rng = np.random.default_rng(seed)
    out = np.zeros(n)
    # warm chord pads: Imaj7 - vi7 - IVmaj7 - V6 (C major, shiftable)
    prog = [[0, 4, 7, 11], [-3, 0, 4, 7], [-7, -3, 0, 4], [-5, -1, 2, 4]]
    bar = beat * 4
    for i in range(int(seconds / bar) + 1):
        ch = prog[i % 4]
        s0 = int(i * bar * sr)
        s1 = min(n, int((i + 1) * bar * sr) + int(0.3 * sr))
        if s0 >= n:
            break
        tt = np.arange(s1 - s0) / sr
        env = np.minimum(1, tt / 0.25) * np.exp(-tt / 3.5)
        for k, semi in enumerate(ch):
            f = 261.63 * 2 ** ((semi + key) / 12)
            voice = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 0.3) + 0.12 * np.sin(2 * np.pi * 3 * f * tt)
            out[s0:s1] += 0.06 * env * voice
        # bass on beat 1 and 3
        for b in (0, 2):
            bs = s0 + int(b * beat * sr)
            if bs >= n:
                continue
            be = min(n, bs + int(beat * 1.6 * sr))
            tb = np.arange(be - bs) / sr
            fb = 65.41 * 2 ** ((ch[0] + key) / 12)
            out[bs:be] += 0.22 * np.sin(2 * np.pi * fb * tb) * np.exp(-tb / 0.6) * np.minimum(1, tb / 0.01)
    # plucked melody (pentatonic, gentle)
    scale = [0, 2, 4, 7, 9, 12, 14, 16]
    step = beat / 2
    for i in range(int(seconds / step)):
        if rng.random() < 0.45:
            continue
        s0 = int(i * step * sr)
        tt = np.arange(int(0.6 * sr)) / sr
        s1 = min(n, s0 + len(tt))
        f = 523.25 * 2 ** ((rng.choice(scale) + key) / 12)
        pl = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.18)
        out[s0:s1] += 0.09 * pl[: s1 - s0]
    # soft kick + shaker
    for i in range(int(seconds / beat) + 1):
        s0 = int(i * beat * sr)
        if s0 >= n:
            break
        tt = np.arange(int(0.25 * sr)) / sr
        s1 = min(n, s0 + len(tt))
        if i % 2 == 0:
            k = np.sin(2 * np.pi * (55 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt / 0.09)
            out[s0:s1] += 0.35 * k[: s1 - s0]
        sh0 = s0 + int(beat / 2 * sr)
        if sh0 < n:
            ts = np.arange(int(0.06 * sr)) / sr
            sh1 = min(n, sh0 + len(ts))
            noise = rng.normal(0, 1, len(ts)) * np.exp(-ts / 0.015)
            noise = np.diff(np.concatenate([[0], noise]))
            out[sh0:sh1] += 0.03 * noise[: sh1 - sh0]
    # fades + normalise + light warmth (one-pole low-pass)
    fade = np.minimum(1, t / 0.4) * np.minimum(1, (seconds - t) / 1.2)
    out *= fade
    y = np.zeros_like(out)
    a = 0.18
    for i in range(1, n):
        y[i] = y[i - 1] + a * (out[i] - y[i - 1])
    y = 0.6 * y + 0.4 * out
    y = y / (np.abs(y).max() + 1e-9) * 0.7
    st = np.stack([y, np.roll(y, 220) * 0.96], axis=1)
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    return path


# ---------------------------------------------------------------- video (1080x1920)
def ease(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3


def make_video(spec, out, seconds=9.0):
    pal = PALETTES.get(spec.get("palette", "brand"), PALETTES["brand"])
    prods = spec["products"]
    photos = [fetch(p["photo"]) for p in prods]
    # pre-render big photo plates (larger than frame for Ken Burns)
    plates = []
    for im in photos[:2]:
        if is_studio(im):
            plates.append(studio_on(im, (int(VW * 1.12), int(VH * 1.12)), hexrgb(pal["soft"])).convert("RGB"))
        else:
            plates.append(cover_crop(im, (int(VW * 1.12), int(VH * 1.12))))
    if len(plates) == 1:
        alt = ImageOps.mirror(plates[0])
        plates.append(alt.crop((0, int(alt.height * 0.15), alt.width, alt.height)).resize(plates[0].size, Image.LANCZOS))
    words = spec["headline"].split()
    hf, hlines, hsize = fit_lines(ImageDraw.Draw(Image.new("RGB", (10, 10))), spec["headline"], "italic", VW - 160, 190, 90, 3)
    lg = logo(pal["cream"], 220)
    tmp = tempfile.mkdtemp()
    nframes = int(seconds * FPS)
    s1, s2 = 3.4, 6.4  # scene boundaries
    for fi in range(nframes):
        t = fi / FPS
        if t < s2:
            k = 0 if t < s1 else 1
            t0 = 0 if k == 0 else s1
            dur = s1 if k == 0 else s2 - s1
            u = (t - t0) / dur
            pl = plates[k]
            z = 1.0 + 0.10 * u if k == 0 else 1.10 - 0.08 * u
            cw, chh = int(VW * 1.12 / z), int(VH * 1.12 / z)
            ox = int((pl.width - cw) * (0.5 + (0.08 * (u - 0.5) if k == 0 else -0.08 * (u - 0.5))))
            oy = int((pl.height - chh) * 0.45)
            frame = pl.crop((ox, oy, ox + cw, oy + chh)).resize((VW, VH), Image.BILINEAR).convert("RGBA")
            # bottom shade
            sh = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
            sd = ImageDraw.Draw(sh)
            for yy in range(VH // 2, VH, 8):
                a = int(220 * ((yy - VH / 2) / (VH / 2)) ** 1.6)
                sd.rectangle((0, yy, VW, yy + 8), fill=hexrgb(pal["deep"], a))
            for yy in range(0, 420, 6):
                a = int(150 * (1 - yy / 420) ** 1.5)
                sd.rectangle((0, yy, VW, yy + 6), fill=hexrgb(pal["deep"], a))
            frame = Image.alpha_composite(frame, sh)
            dr = ImageDraw.Draw(frame)
            draw_tracked(dr, (VW / 2, 150), "TAILVANI", font("serif", 96, 800), hexrgb(pal["cream"]), 8, "ms")
            if k == 0:
                # kicker + kinetic headline, word by word
                if spec.get("kicker"):
                    al = int(255 * ease(t / 0.5))
                    ky = VH - 470 - (len(hlines) - 1) * hsize * 0.95 - hsize * 0.85 - 30
                    kf = font("sans", 32, 700)
                    kw = tw(dr, spec["kicker"].upper(), kf, 6)
                    dr.rounded_rectangle((70, ky - 44, 70 + kw + 44, ky + 14), radius=29, fill=hexrgb(pal["bg"], al))
                    draw_tracked(dr, (92, ky), spec["kicker"].upper(), kf, hexrgb(pal["cream"], al), 6, "ls")
                y = VH - 470 - (len(hlines) - 1) * hsize * 0.95
                wi = 0
                for line in hlines:
                    x = 80
                    for w_ in line.split():
                        appear = 0.35 + wi * 0.28
                        e = ease((t - appear) / 0.45)
                        if e > 0:
                            dr.text((x, y + 40 * (1 - e)), w_, font=hf, fill=hexrgb(pal["cream"], int(255 * e)), anchor="ls")
                        x += dr.textlength(w_ + " ", font=hf)
                        wi += 1
                    y += hsize * 0.95
                if spec.get("sub"):
                    e = ease((t - 1.6) / 0.5)
                    dr.text((82, y - hsize * 0.95 + 80), spec["sub"], font=font("sans", 44, 500), fill=hexrgb(pal["cream"], int(255 * e)), anchor="ls")
            else:
                # product credit card slides in
                prod = prods[1] if len(prods) > 1 else prods[0]
                e = ease((t - s1 - 0.2) / 0.5)
                cardw = VW - 160
                x0 = 80 - int((1 - e) * 900)
                ty = VH - 470
                dr.rectangle((x0, ty, x0 + cardw, ty + 260), fill=hexrgb(pal["cream"]))
                dr.rectangle((x0, ty, x0 + 16, ty + 260), fill=hexrgb(pal["pop"]))
                draw_tracked(dr, (x0 + 56, ty + 70), ("WEARING" if prod.get("worn", True) else "SHOWN"), font("sans", 30, 700), hexrgb(pal["bg"]), 5, "ls")
                tf, tl, _ = fit_lines(dr, prod["title"], "serif", cardw - 110, 64, 38, 2, 700)
                yy = ty + 140
                for l in tl:
                    dr.text((x0 + 56, yy), l, font=tf, fill=hexrgb(pal["deep"]), anchor="ls")
                    yy += tf.size * 1.05
                dr.text((x0 + cardw - 40, ty + 70), f"${float(prod['price']):.0f}", font=font("serif", 60, 800), fill=hexrgb(pal["bg"]), anchor="rs")
        else:
            # end card
            u = (t - s2) / (seconds - s2)
            frame = Image.new("RGBA", (VW, VH), hexrgb(pal["bg"]))
            dr = ImageDraw.Draw(frame)
            e = ease(u / 0.35)
            frame.alpha_composite(lg, ((VW - 220) // 2, 430 + int(30 * (1 - e))))
            draw_tracked(dr, (VW / 2, 820), "TAILVANI", font("serif", 150, 800), hexrgb(pal["cream"], int(255 * e)), 10, "ms")
            dr.text((VW / 2, 905), "A Style for Every Tail", font=font("italic", 56, 500), fill=hexrgb(pal["soft"], int(255 * e)), anchor="ms")
            if spec.get("offer"):
                e2 = ease((u - 0.2) / 0.35)
                s = sticker(spec["offer"], pal, 300, -10 + 10 * (1 - e2))
                if e2 > 0:
                    s2i = s.resize((max(1, int(s.width * e2)), max(1, int(s.height * e2))), Image.BICUBIC)
                    frame.alpha_composite(s2i, ((VW - s2i.width) // 2, 1180 - s2i.height // 2 + 60))
            draw_tracked(dr, (VW / 2, VH - 260), "SHOP TAILVANI.COM", font("sans", 44, 800), hexrgb(pal["cream"]), 6, "ms")
        frame.convert("RGB").save(os.path.join(tmp, f"f{fi:04d}.jpg"), quality=90)
    wav = music(seconds, os.path.join(tmp, "m.wav"), seed=random.randint(1, 9999), key=random.choice([0, 2, -3, 5]))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.jpg"), "-i", wav,
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    # cover image for the video (first scene, headline fully in)
    return out


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    base = sys.argv[2]
    if spec.get("format") == "video":
        print(make_video(spec, base + ".mp4"))
    else:
        print(make_image(spec, base + ".jpg"))
