"""Tailvani seasonal prop library: flat illustrated props drawn in VectorCraft.
Every prop is a list of (d, fill, stroke, strokeWidth) on a 200x200 artboard.
Colours are role tokens resolved per skin: A accent, A2 second accent, D dark/ink, G leaf green, L light, plus literal #hex.
"""
import math

def ell(cx, cy, rx, ry, rot=0):
    k = 0.5523
    pts = [  # start, c1, c2, end for 4 quarter arcs
        ((cx+rx, cy), (cx+rx, cy+k*ry), (cx+k*rx, cy+ry), (cx, cy+ry)),
        ((cx, cy+ry), (cx-k*rx, cy+ry), (cx-rx, cy+k*ry), (cx-rx, cy)),
        ((cx-rx, cy), (cx-rx, cy-k*ry), (cx-k*rx, cy-ry), (cx, cy-ry)),
        ((cx, cy-ry), (cx+k*rx, cy-ry), (cx+rx, cy-k*ry), (cx+rx, cy)),
    ]
    def R(p):
        if not rot: return p
        a = math.radians(rot); x, y = p[0]-cx, p[1]-cy
        return (cx + x*math.cos(a) - y*math.sin(a), cy + x*math.sin(a) + y*math.cos(a))
    s = R(pts[0][0]); d = f"M{s[0]:.1f} {s[1]:.1f}"
    for _, c1, c2, e in pts:
        c1, c2, e = R(c1), R(c2), R(e)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {e[0]:.1f} {e[1]:.1f}"
    return d + " Z"

def circ(cx, cy, r):
    return ell(cx, cy, r, r)

def poly(pts, close=True):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")

def xform(d, rot=0, cx=100, cy=100, s=1.0, dx=0, dy=0):
    """Rotate/scale/translate an absolute M/L/C/Z path."""
    a = math.radians(rot); out = []; toks = d.replace(',', ' ').split()
    i = 0; nums = []
    def tp(x, y):
        x, y = (x-cx)*s, (y-cy)*s
        return cx + x*math.cos(a) - y*math.sin(a) + dx, cy + x*math.sin(a) + y*math.cos(a) + dy
    res = []
    cmd = None; buf = []
    def flush():
        if cmd is None: return
        if cmd == 'Z': res.append('Z'); return
        pts = [tp(float(buf[j]), float(buf[j+1])) for j in range(0, len(buf), 2)]
        res.append(cmd + ' '.join(f"{x:.1f} {y:.1f}" for x, y in pts))
    for t in toks:
        if t[0] in 'MLCZ':
            flush(); cmd = t[0]; buf = []
            if len(t) > 1: buf.append(t[1:])
        else:
            buf.append(t)
    flush()
    return ' '.join(res)

def star(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n*2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i*180/n)
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    return poly(pts)

HEART = 'M100 175 C40 130 10 95 30 55 C48 20 90 25 100 55 C110 25 152 20 170 55 C190 95 160 130 100 175 Z'
LEAF = 'M100 12 C150 45 182 95 146 148 C128 172 100 188 100 188 C100 188 72 172 54 148 C18 95 50 45 100 12 Z'
PETAL = 'M100 100 C80 80 78 40 100 18 C122 40 120 80 100 100 Z'

P = {}

P['heart'] = [(HEART, 'A2', 'none', 0), ('M58 62 C66 50 80 48 90 58', 'none', 'L', 7)]
P['heart_small'] = [(HEART, 'A', 'none', 0)]

P['maple'] = [(poly([(100,8),(116,52),(150,36),(141,80),(188,74),(162,108),(184,124),(132,138),(138,172),(106,150),(100,150),(94,150),(62,172),(68,138),(16,124),(38,108),(12,74),(59,80),(50,36),(84,52)]), 'A', 'none', 0),
              ('M100 196 L100 70', 'none', 'D', 5), ('M100 118 L70 88', 'none', 'D', 4), ('M100 118 L130 88', 'none', 'D', 4)]
P['leaf'] = [(LEAF, 'A2', 'none', 0), ('M100 30 L100 196', 'none', 'D', 5), ('M100 80 L76 62', 'none', 'D', 3), ('M100 110 L126 90', 'none', 'D', 3), ('M100 140 L78 122', 'none', 'D', 3)]
P['acorn'] = [(ell(100, 128, 46, 56), 'A', 'none', 0),
              ('M48 92 C48 62 72 46 100 46 C128 46 152 62 152 92 C152 100 48 100 48 92 Z', 'D', 'none', 0),
              ('M100 46 C100 34 106 24 116 18', 'none', 'D', 7), ('M78 118 C80 140 88 156 96 164', 'none', 'L', 5)]
P['pumpkin'] = [(ell(64, 118, 46, 60), 'A2', 'none', 0), (ell(136, 118, 46, 60), 'A2', 'none', 0), (ell(100, 118, 40, 64), 'A', 'none', 0),
                ('M100 56 C100 40 104 28 114 20', 'none', 'D', 9), (ell(128, 46, 20, 10, -25), 'G', 'none', 0)]
P['bat'] = [('M100 70 C108 58 112 52 112 44 C118 54 120 62 116 72 C134 60 160 56 192 70 C178 78 170 94 172 112 C160 102 146 104 136 116 C128 104 114 104 104 116 L100 120 L96 116 C86 104 72 104 64 116 C54 104 40 102 28 112 C30 94 22 78 8 70 C40 56 66 60 84 72 C80 62 82 54 88 44 C88 52 92 58 100 70 Z', 'D', 'none', 0)]
P['moon'] = [('M118 18 C70 22 36 62 38 108 C40 154 80 188 126 186 C150 185 170 174 184 158 C140 166 102 136 98 92 C96 62 104 36 118 18 Z', 'A', 'none', 0)]
P['paw'] = [(ell(100, 128, 44, 38), 'D', 'none', 0), (ell(48, 84, 17, 23, -20), 'D', 'none', 0), (ell(80, 50, 18, 25, -8), 'D', 'none', 0),
            (ell(120, 50, 18, 25, 8), 'D', 'none', 0), (ell(152, 84, 17, 23, 20), 'D', 'none', 0)]
P['yarn'] = [(circ(100, 100, 70), 'A', 'none', 0), ('M44 78 C80 64 130 70 164 96', 'none', 'L', 5), ('M38 108 C80 92 136 100 166 128', 'none', 'L', 5),
             ('M56 150 C90 128 128 128 150 152', 'none', 'L', 5), ('M96 32 C78 70 76 128 96 168', 'none', 'L', 5),
             ('M150 160 C166 178 186 176 196 190', 'none', 'A', 5)]
P['gift'] = [('M34 86 L166 86 L166 186 L34 186 Z', 'A', 'none', 0), ('M24 62 L176 62 L176 92 L24 92 Z', 'A2', 'none', 0),
             ('M90 62 L110 62 L110 186 L90 186 Z', 'L', 'none', 0), (ell(78, 48, 26, 15, 25), 'none', 'D', 8), (ell(122, 48, 26, 15, -25), 'none', 'D', 8)]
P['star'] = [(star(100, 104, 92, 40), 'A', 'none', 0)]
P['star_small'] = [(star(100, 104, 92, 40), 'A2', 'none', 0)]
P['sparkle'] = [(star(100, 100, 92, 20, 4), 'A', 'none', 0)]
P['bauble'] = [(circ(100, 120, 68), 'A2', 'none', 0), ('M38 104 L162 104 L164 132 L36 132 Z', 'A', 'none', 0),
               ('M82 38 L118 38 L118 56 L82 56 Z', 'D', 'none', 0), (ell(100, 26, 14, 12), 'none', 'D', 5), ('M72 88 C78 78 88 72 98 70', 'none', 'L', 7)]
P['fir'] = [('M100 196 L100 10', 'none', 'G', 7)] + [(f'M100 {y} L{100+side*w} {y+28}', 'none', 'G', 7) for y, w in [(30, 34), (60, 48), (92, 60), (126, 70)] for side in (-1, 1)]
P['snowflake'] = [(f'M100 100 L{100+88*math.cos(math.radians(a)):.1f} {100+88*math.sin(math.radians(a)):.1f}', 'none', 'D', 9) for a in range(0, 360, 60)] + \
                 [(f'M{100+52*math.cos(math.radians(a))+20*math.cos(math.radians(a+50)):.1f} {100+52*math.sin(math.radians(a))+20*math.sin(math.radians(a+50)):.1f} L{100+52*math.cos(math.radians(a)):.1f} {100+52*math.sin(math.radians(a)):.1f} L{100+52*math.cos(math.radians(a))+20*math.cos(math.radians(a-50)):.1f} {100+52*math.sin(math.radians(a))+20*math.sin(math.radians(a-50)):.1f}', 'none', 'D', 7) for a in range(0, 360, 60)]
P['burst'] = [(f'M{100+30*math.cos(math.radians(a)):.1f} {100+30*math.sin(math.radians(a)):.1f} L{100+88*math.cos(math.radians(a)):.1f} {100+88*math.sin(math.radians(a)):.1f}', 'none', 'A' if i % 2 else 'A2', 8) for i, a in enumerate(range(0, 360, 30))] + \
             [(circ(100+96*math.cos(math.radians(a+15)), 100+96*math.sin(math.radians(a+15)), 5), 'A', 'none', 0) for a in range(0, 360, 60)]
P['confetti'] = [(xform('M90 70 L110 70 L110 110 L90 110 Z', rot=25, dx=-50, dy=-40), 'A', 'none', 0),
                 (xform('M90 70 L110 70 L110 110 L90 110 Z', rot=-35, dx=40, dy=-30), 'A2', 'none', 0),
                 (xform('M90 70 L110 70 L110 110 L90 110 Z', rot=70, dx=10, dy=50), 'D', 'none', 0),
                 (circ(150, 140, 12), 'A', 'none', 0), (circ(50, 150, 10), 'A2', 'none', 0), (circ(110, 30, 9), 'D', 'none', 0),
                 ('M30 90 C40 76 50 104 60 90 C70 76 80 104 90 90', 'none', 'A2', 6)]
P['balloon'] = [(ell(100, 82, 62, 74), 'A2', 'none', 0), (poly([(92, 154), (108, 154), (100, 166)]), 'A2', 'none', 0),
                ('M100 166 C88 178 112 186 100 198', 'none', 'D', 4), ('M66 60 C70 44 82 34 96 30', 'none', 'L', 8)]
P['party_hat'] = [(poly([(100, 22), (160, 178), (40, 178)]), 'A', 'none', 0), ('M78 80 L122 80 L130 102 L70 102 Z', 'A2', 'none', 0),
                  ('M58 130 L142 130 L150 152 L50 152 Z', 'A2', 'none', 0), (circ(100, 22, 16), 'D', 'none', 0)]
P['shamrock'] = [(xform(xform(HEART, s=0.52), rot=180 + r, dy=0, dx=0, cx=100, cy=100), 'G', 'none', 0) for r in (0, 120, 240)]
# shift each heart outward from centre so the points meet in the middle
P['shamrock'] = []
for r in (0, 120, 240):
    h = xform(HEART, s=0.5, dy=-46)  # heart above centre, point near centre
    P['shamrock'].append((xform(h, rot=r), 'G', 'none', 0))
P['shamrock'].append(('M100 104 C104 140 118 168 140 190', 'none', 'G', 9))
P['coin'] = [(circ(100, 100, 74), 'A', 'none', 0), (circ(100, 100, 56), 'none', 'D', 5), (star(100, 102, 30, 13), 'D', 'none', 0)]
P['blossom'] = [(xform(PETAL, rot=r, s=1.0), 'A2', 'none', 0) for r in range(0, 360, 72)] + [(circ(100, 100, 22), 'A', 'none', 0)]
P['petal'] = [(xform(PETAL, s=1.45, dy=45, rot=30), 'A2', 'none', 0)]
P['tulip'] = [('M100 196 L100 100', 'none', 'G', 8), (xform(LEAF, s=0.42, rot=-40, dx=-28, dy=46), 'G', 'none', 0),
              ('M58 46 L78 66 L100 30 L122 66 L142 46 L142 92 C142 118 124 130 100 130 C76 130 58 118 58 92 Z', 'A2', 'none', 0)]
P['egg'] = [('M100 16 C140 16 168 78 168 118 C168 160 138 188 100 188 C62 188 32 160 32 118 C32 78 60 16 100 16 Z', 'A', 'none', 0),
            (poly([(34, 104), (58, 88), (82, 104), (106, 88), (130, 104), (154, 88), (166, 98), (166, 122), (154, 112), (130, 128), (106, 112), (82, 128), (58, 112), (34, 128)]), 'A2', 'none', 0),
            (circ(80, 60, 8), 'L', 'none', 0), (circ(118, 54, 6), 'L', 'none', 0), (circ(70, 154, 7), 'L', 'none', 0), (circ(124, 160, 9), 'L', 'none', 0)]
P['sun'] = [(star(100, 100, 96, 70, 12, -90), 'A', 'none', 0), (circ(100, 100, 60), 'A2', 'none', 0)]
P['lemon'] = [(circ(100, 100, 80), 'A', 'none', 0), (circ(100, 100, 66), 'L', 'none', 0), (circ(100, 100, 58), 'A2', 'none', 0)] + \
             [(f'M100 100 L{100+58*math.cos(math.radians(a)):.1f} {100+58*math.sin(math.radians(a)):.1f}', 'none', 'L', 5) for a in range(0, 360, 45)]
P['bone'] = [(circ(40, 74, 24), 'L', 'none', 0), (circ(40, 126, 24), 'L', 'none', 0), (circ(160, 74, 24), 'L', 'none', 0), (circ(160, 126, 24), 'L', 'none', 0),
             ('M40 78 L160 78 L160 122 L40 122 Z', 'L', 'none', 0)]
P['sprig'] = [('M40 190 C70 150 96 100 150 20', 'none', 'G', 6)] + \
             [(ell(x, y, 26, 11, rot), 'G', 'none', 0) for x, y, rot in [(68, 140, -10), (110, 140, 35), (86, 104, -15), (124, 96, 30), (108, 64, -30), (146, 54, 20)]]
P['bunting'] = [('M6 40 C60 70 140 70 194 40', 'none', 'D', 5)] + \
               [(poly([(x - 20, y), (x + 20, y + 2), (x, y + 50)]), c, 'none', 0) for (x, y, c) in [(38, 54, 'A2'), (100, 64, 'L'), (162, 54, 'A')]]
P['dot'] = [(circ(100, 100, 60), 'A', 'none', 0)]
P['ring'] = [(circ(100, 100, 70), 'none', 'A', 14)]

PROP_NAMES = list(P.keys())
