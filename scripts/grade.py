#!/usr/bin/env python3
"""Grade hero + feature photos for every skin in LightCraft."""
import sys, os, json, glob
sys.path.insert(0, '/home/claude/craft')
from mcpc import Client
from skin_palettes import SKINS
GRADE = {
 'base': ('lc.bright-airy', 40), 'fall-2026': ('lc.autumn-gold', 50), 'halloween-2026': ('lc.warm-film', 40),
 'national-cat-day-2026': ('lc.warm-glow', 30), 'thanksgiving-2026': ('lc.warm-table', 40), 'bfcm-2026': ('lc.warm-glow', 30),
 'holidays-2026': ('lc.warm-glow', 40), 'winter-2026': ('lc.winter-blue', 35), 'new-year-2027': ('lc.cinematic', 30),
 'valentines-2027': ('lc.soft-pastel', 40), 'st-patricks-2027': ('lc.fresh-bright', 40), 'tailvani-anniversary-2027': ('lc.vivid-pop', 30),
 'spring-2027': ('lc.spring-fresh', 50), 'easter-2027': ('lc.soft-pastel', 40), 'fourth-of-july-2027': ('lc.vivid-pop', 30),
 'summer-2027': ('lc.vivid-pop', 35), 'national-dog-day-2027': ('lc.golden-glow', 40),
}
def src(stem):
    return glob.glob(f'/home/claude/craft/photos2/{stem}-*.jpg')[0]
os.makedirs('/home/claude/craft/artwork/graded', exist_ok=True)
c = Client('lightcraft')
only = sys.argv[1:] or list(SKINS)
for skin in only:
    pal = SKINS[skin]; preset, amt = GRADE[skin]
    for role in ('photo', 'feature'):
        path = src(pal[role])
        r = c.call('import', {'paths': [path]})['structuredContent']
        pid = r['imported'][0] if r['imported'] else r['duplicates'][0]['existing']
        c.call('apply_preset', {'preset': preset, 'ids': [pid], 'amount': amt})
        c.call('set_develop', {'id': pid, 'values': {'color.vibrance': 12, 'effects.clarity': 6, 'light.shadows': 10}})
        c.call('select_photos', {'ids': [pid], 'active': pid})
        out = f'/home/claude/craft/artwork/graded/{skin}-{role}.jpg'
        r = c.call('export', {'path': out})
        if r.get('isError'): print('ERR', skin, role, str(r)[:300])
    print('graded', skin, flush=True)
