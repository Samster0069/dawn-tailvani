#!/usr/bin/env python3
"""Render props in VectorCraft. Usage: render_props.py <skin|ALL_PROPS_TEST> [prop ...]"""
import sys, os, json
sys.path.insert(0, '/home/claude/craft')
from mcpc import Client
from props_lib import P
from skin_palettes import SKINS

def resolve(tok, pal):
    if tok in ('none',): return 'none'
    if tok.startswith('#'): return tok
    return pal['dark'] if tok == 'D' else pal[tok]

def render(c, prop, pal, out):
    c.call('run_command', {'command': 'file.new', 'params': {'width': 200, 'height': 200}})
    for d, fill, stroke, sw in P[prop]:
        args = {'d': d, 'fill': resolve(fill, pal), 'stroke': resolve(stroke, pal)}
        if stroke != 'none':
            args['strokeWidth'] = sw
        r = c.call('draw_path', args)
        if r.get('isError') or 'error' in r:
            print('ERR', prop, str(r)[:200])
    r = c.call('export', {'path': out, 'scale': 2.5})
    c.call('run_command', {'command': 'file.close', 'params': {}})

if __name__ == '__main__':
    target = sys.argv[1]
    c = Client('vectorcraft')
    if target == 'ALL_PROPS_TEST':
        os.makedirs('/home/claude/craft/artwork/props/_test', exist_ok=True)
        for p in P:
            render(c, p, SKINS['base'], f'/home/claude/craft/artwork/props/_test/{p}.png')
    else:
        skins = list(SKINS) if target == 'ALL' else [target]
        for s in skins:
            pal = SKINS[s]; d = f'/home/claude/craft/artwork/props/{s}'; os.makedirs(d, exist_ok=True)
            for p in sorted(set(pal['props'])):
                render(c, p, pal, f'{d}/{p}.png')
            print('done', s)
