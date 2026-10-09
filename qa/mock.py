#!/usr/bin/env python3
"""Static mock of the rebuilt homepage for visual QA (mirrors the Liquid markup + CSS vars).
Usage: mock.py <skin|base>  -> writes mock-<skin>.html"""
import sys, json
sys.path.insert(0, '/home/claude/craft')
from skin_palettes import SKINS

SCHEMES = {
 'scheme-1': dict(bg='#FFFDF8', text='#2B3524', button='#2B3524', label='#FFFDF8', sec='#2B3524'),
 'scheme-2': dict(bg='#F7D9CF', text='#2B3524', button='#2B3524', label='#FFFDF8', sec='#2B3524'),
 'scheme-3': dict(bg='#DCE5CF', text='#2B3524', button='#2B3524', label='#FFFDF8', sec='#2B3524'),
 'scheme-4': dict(bg='#2B3524', text='#FFFDF8', button='#FFFDF8', label='#2B3524', sec='#FFFDF8'),
 'scheme-5': dict(bg='#F2AE3D', text='#2B3524', button='#2B3524', label='#FFFDF8', sec='#2B3524'),
 'scheme-6': dict(bg='#A94E2B', text='#FFFDF8', button='#FFFDF8', label='#A94E2B', sec='#FFFDF8'),
}
COPY = {  # skin hero copy from the store (subset) and icons
 'base': ('A style for every tail', 'Clothing and accessories for dogs and cats, picked for comfort and made to be shown off.', 'Shop new arrivals', 'sprig',
          'Made for the way they live', 'We pick pieces that are easy to put on, comfortable to wear and fun to show off, from weekday walks to holiday photos.', 'Free US shipping on orders over $35'),
 'fall-2026': ('Cozy season is here', 'Warm layers and easy everyday pieces for every tail.', 'Shop fall', 'leaf',
          'Layers for leaf-pile season', 'Soft knits and bandanas that keep up with crunchy walks and cool mornings.', 'Fall layers are here. Free US shipping over $35.'),
 'halloween-2026': ('Spooky, but make it stylish', 'Costume-ready looks for little monsters.', 'Shop Halloween', 'bat',
          "Costumes they'll actually wear", 'Easy-on looks for trick-or-treat photos, porch greetings and the neighborhood parade.', 'Halloween looks are here. Free US shipping over $35.'),
 'holidays-2026': ('Holiday style for every tail', 'Gift-ready picks for the pets you love.', 'Shop gifts', 'snowflake',
          'Gifts that fit every tail', 'Festive sweaters, bandanas and gifts for the pets on your list. Order early for holiday delivery.', 'Holiday gifting is here. Order early for holiday delivery.'),
 'spring-2027': ('Fresh for spring', 'Light layers for sunny walks.', 'Shop spring', 'petal',
          'Fresh for spring walks', 'Light layers, bright collars and harnesses for longer days outside.', 'Spring styles are in. Free US shipping over $35.'),
 'summer-2027': ('Summer, styled', 'Light, breezy pieces for sunny days.', 'Shop summer', 'sun',
          'Made for sunny days', 'Breathable pieces and outdoor gear for beach trips, park days and evening walks.', 'Summer styles are here. Free US shipping over $35.'),
 'valentines-2027': ('Made with love', 'Sweet looks for your favorite valentine.', "Shop Valentine's", 'heart',
          'For your favorite valentine', "Sweet bandanas, collars and gifts for the one who's always happy to see you.", "Valentine's looks are here. Free US shipping over $35."),
 'st-patricks-2027': ('Feeling lucky', 'A little green for every tail.', 'Shop lucky', 'clover',
          'A little green goes a long way', 'Bandanas and accessories in every shade of lucky.', "Lucky looks for St. Patrick's Day."),
}

def rgb(h):
    h = h.lstrip('#'); return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

def scheme_css():
    out = []
    for i, (k, s) in enumerate(SCHEMES.items()):
        sel = (':root, ' if i == 0 else '') + f'.color-{k}'
        out.append(f"""{sel} {{ --color-background:{rgb(s['bg'])}; --gradient-background:{s['bg']}; --color-foreground:{rgb(s['text'])};
 --color-background-contrast:{rgb(s['text'])}; --color-shadow:{rgb('#2B3524')}; --color-button:{rgb(s['button'])}; --color-button-text:{rgb(s['label'])};
 --color-secondary-button:{rgb(s['bg'])}; --color-secondary-button-text:{rgb(s['sec'])}; --color-link:{rgb(s['sec'])};
 --color-badge-foreground:{rgb(s['text'])}; --color-badge-background:{rgb(s['bg'])}; --color-badge-border:{rgb(s['text'])}; }}""")
    out.append("body, " + ", ".join(f".color-{k}" for k in SCHEMES) + " { color: rgba(var(--color-foreground), .75); background-color: rgb(var(--color-background)); }")
    return "\n".join(out)

def skin_css(p):
    if not p: return ''
    return f"""
:root, .color-scheme-1, .color-scheme-2, .color-scheme-3 {{ --color-foreground:{rgb(p['text'])}; --color-badge-foreground:{rgb(p['text'])};
 --color-secondary-button-text:{rgb(p['text'])}; --color-link:{rgb(p['text'])}; --color-button:{rgb(p['btn'])}; --color-button-text:{rgb(p['btn_label'])}; }}
.color-scheme-2 {{ --color-background:{rgb(p['hero'])}; --gradient-background:{p['hero']}; --color-secondary-button:{rgb(p['hero'])}; }}
.color-scheme-3 {{ --color-background:{rgb(p['band'])}; --gradient-background:{p['band']}; --color-secondary-button:{rgb(p['band'])}; }}
.color-scheme-4 {{ --color-background:{rgb(p['dark'])}; --gradient-background:{p['dark']}; --color-foreground:{rgb(p['btn_label'])}; --color-button:{rgb(p['btn_label'])};
 --color-button-text:{rgb(p['dark'])}; --color-secondary-button:{rgb(p['dark'])}; --color-secondary-button-text:{rgb(p['btn_label'])}; --color-link:{rgb(p['btn_label'])}; }}
:root {{ --tv-accent:{p['A']}; --tv-ink:{p['dark']}; --tv-hero:{p['hero']}; --tv-band:{p['band']}; }}"""

def page(skin):
    p = SKINS[skin] if skin != 'base' else None
    h, sub, btn, icon, fh, ft, ann = COPY[skin]
    hero_img = f'tv-hero-{skin}.webp'; feat = f'tv-feature-{skin}.jpg'
    garl = ''.join('<span></span>' for _ in range(9))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@font-face {{ font-family:'Young Serif'; src:url('tv-young-serif.woff2') format('woff2'); }}
@font-face {{ font-family:'Figtree'; font-weight:400 700; src:url('tv-figtree.woff2') format('woff2'); }}
{scheme_css()}
:root {{ --font-body-scale:1; --font-heading-scale:1; --page-width:130rem; --page-width-margin:0rem; --buttons-radius:40px; --buttons-radius-outset:41px;
 --buttons-border-width:1px; --buttons-border-opacity:1; --buttons-shadow-opacity:0; --buttons-shadow-visible:0; --buttons-shadow-horizontal-offset:0px;
 --buttons-shadow-vertical-offset:4px; --buttons-shadow-blur-radius:5px; --buttons-border-offset:0.3px; --inputs-radius:12px; --grid-desktop-horizontal-spacing:20px;
 --grid-mobile-horizontal-spacing:10px; --grid-desktop-vertical-spacing:28px; --grid-mobile-vertical-spacing:14px; --duration-short:100ms; --duration-default:200ms; }}
</style>
<link rel="stylesheet" href="base.css"><link rel="stylesheet" href="tv-rebuild.css">
<style>{skin_css(p)}
html {{ box-sizing:border-box; font-size:calc(var(--font-body-scale)*62.5%); height:100%; }} body {{ display:grid; grid-template-rows:auto auto 1fr auto; grid-template-columns:100%; min-height:100%; margin:0; font-size:1.5rem; letter-spacing:.06rem; line-height:calc(1 + .8/var(--font-body-scale)); font-family:var(--font-body-family); font-style:var(--font-body-style); font-weight:var(--font-body-weight); }} @media (min-width:750px) {{ body {{ font-size:1.6rem; }} }}
.mock-header {{ display:flex; align-items:center; justify-content:space-between; padding:1.6rem 0; }}
.mock-header img {{ width:200px; height:auto; }} .mock-nav {{ display:flex; gap:2.4rem; font-weight:500; font-size:1.55rem; }}
.mock-ann {{ text-align:center; padding:1rem; }} @media (max-width:749px) {{ .mock-nav, .mock-header > span {{ display:none; }} .mock-header img {{ width:160px; }} .mock-footer .page-width {{ grid-template-columns:1fr !important; }} }} .mock-footer {{ padding:6.4rem 0 4.8rem; }}
</style></head>
<body class="gradient">
<div class="color-scheme-4 gradient mock-ann"><p class="announcement-bar__message" style="margin:0">{ann}</p></div>
<div class="color-scheme-1 header-wrapper"><div class="page-width mock-header"><img src="tailvani-logo.png" alt="Tailvani">
<nav class="mock-nav"><span>New arrivals</span><span>Dogs</span><span>Cats</span><span>Clothing</span><span>Accessories</span><span>Help</span></nav><span>Search · Cart</span></div></div>
<section class="tv-hero color-scheme-2 gradient"><div class="page-width tv-hero__grid">
 <div class="tv-hero__copy"><h1 class="tv-hero__heading">{h}</h1><p class="tv-hero__sub">{sub}</p>
 <div class="tv-hero__actions"><a class="button button--primary" href="#">{btn}</a><a class="tv-link" href="#">Browse everything</a></div></div>
 <div class="tv-hero__art"><img src="{hero_img}" alt=""></div></div></section>
<div class="tv-garland color-scheme-1 gradient" style="--tv-garland-icon:url('tv-overlay-{icon}.svg'); --tv-garland-size:24px"><div class="page-width"><div class="tv-garland__row">{garl}</div></div></div>
<section class="tv-tiles color-scheme-1 gradient"><div class="page-width"><div class="tv-section-head"><h2 class="tv-h2">Find their next favorite</h2></div>
<ul class="tv-tiles__grid tv-tiles__grid--3" role="list">
<li class="tv-tile"><a class="tv-tile__link" href="#"><span class="tv-tile__media"><img src="tv-tile-dogs.jpg" alt=""></span><span class="tv-tile__title">For dogs</span><span class="tv-tile__caption">Sweaters, coats and walk gear</span></a></li>
<li class="tv-tile"><a class="tv-tile__link" href="#"><span class="tv-tile__media"><img src="tv-tile-cats.jpg" alt=""></span><span class="tv-tile__title">For cats</span><span class="tv-tile__caption">Collars, bandanas and cozy picks</span></a></li>
<li class="tv-tile"><a class="tv-tile__link" href="#"><span class="tv-tile__media"><img src="tv-tile-accessories.jpg" alt=""></span><span class="tv-tile__title">Walk and play</span><span class="tv-tile__caption">Harnesses, leashes and toys</span></a></li>
</ul></div></section>
<section class="tv-feature color-scheme-3 gradient"><div class="page-width tv-feature__grid"><div class="tv-feature__media"><img src="{feat}" alt=""></div>
<div class="tv-feature__copy"><h2 class="tv-h2">{fh}</h2><p class="tv-feature__text">{ft}</p><a class="button button--secondary" href="#">{btn}</a></div></div></section>
<section class="tv-trust color-scheme-1 gradient"><div class="page-width"><ul class="tv-trust__list" role="list">
{''.join(f'<li class="tv-trust__item"><span class="tv-trust__icon"><span class="svg-wrapper">{open(ic).read()}</span></span><span class="tv-trust__copy"><span class="tv-trust__title">{t}</span><span class="tv-trust__text">{x}</span></span></li>' for ic,t,x in [('icon-truck.svg','Free US shipping over $35','Shipping details'),('icon-return.svg','14-day returns','On unused items with tags'),('icon-box.svg','Packed in 1–3 business days','Delivery in 7–12 business days'),('icon-chat-bubble.svg','Real people, quick replies','We answer within 1–2 business days')])}
</ul></div></section>
<footer class="footer color-scheme-4 gradient mock-footer"><div class="page-width" style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:4rem">
<div><h2 class="footer-block__heading">Tailvani</h2><p>Clothing and accessories for dogs, cats and every tail in between.</p></div>
<div><h2 class="footer-block__heading">Shop</h2><p>New arrivals<br>Dogs<br>Cats<br>Clothing</p></div><div><h2 class="footer-block__heading">Help and policies</h2><p>Help and FAQ<br>Contact<br>Shipping policy</p></div></div></footer>
</body></html>"""

if __name__ == '__main__':
    for s in (sys.argv[1:] or ['base']):
        open(f'/home/claude/qa/mock-{s}.html', 'w').write(page(s))
