# Draws the tiered cake for the "Koliko torte" calculator and writes it into all four pages.
# Style follows the client's reference illustration: pink tiers, twisted rope piping,
# white swags with blue flowers, polka dots, strawberries and a bunting topper on a lilac stand.
# Run: python3 tools/torta.py  (then copy the printed TOPS/HEAD into main.js if tier sizes change)
import math, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "verzije/v1-slatka-radnja/index.html",
         "verzije/v2-slatki-trenuci/index.html", "verzije/v3-rukom-pravljeno/index.html"]
CX, YB, K, H = 200, 402, 0.16, 512           # centre x, cake base y, ellipse squash, viewBox height
TIERS = [(280, 92), (212, 80), (148, 70), (94, 58)]
WORD = "ŽIVELI"
FLAGS = ["#F2CF6B", "#F3B3C1", "#A9B4E0", "#C9C79A", "#C98A96", "#F2CF6B"]

f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")


def arc_pts(cx, cy, rx, ry, t0, t1, n):
    return [(cx + rx * math.cos(t0 + (t1 - t0) * i / n), cy + ry * math.sin(t0 + (t1 - t0) * i / n)) for i in range(n + 1)]


def rope(cx, cy, rx, ry, s, bead, dark, back=False):
    """Twisted piping along the front (or back) half of an ellipse, built from slanted beads."""
    ext = 0.03 if not back else 0.1
    t0, t1 = (math.pi + ext, 2 * math.pi - ext) if back else (-ext, math.pi + ext)
    p = arc_pts(cx, cy, rx, ry, t0, t1, 60)
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in p)
    out = [f'<path d="{d}" fill="none" stroke="{dark}" stroke-width="{f(s * .95)}" stroke-linecap="round"/>']
    length = sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1))
    n = max(6, round(length / (s * .62)))
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        ang = math.degrees(math.atan2(ry * math.cos(t), -rx * math.sin(t))) + 48
        out.append(f'<use href="#{bead}" transform="translate({f(x)} {f(y)}) rotate({f(ang % 360)}) scale({f(s)})"/>')
    return "".join(out)


def flower(x, y, r):
    return f'<use href="#tfl" transform="translate({f(x)} {f(y)}) scale({f(r)})"/>'


def strawberry(x, y, b):
    return f'<use href="#tsb" transform="translate({f(x)} {f(y)}) scale({f(b)})"/>'


SYMBOLS = (
    # bead of white cream piping and of rose piping, unit size
    '<g id="tbw"><ellipse rx=".74" ry=".4" fill="#FFFBF5" stroke="#E2D2C0" stroke-width=".07"/><ellipse cx="-.16" cy="-.13" rx=".36" ry=".1" fill="#fff"/></g>'
    '<g id="tbr"><ellipse rx=".74" ry=".4" fill="#CF7686" stroke="#A3505F" stroke-width=".07"/><ellipse cx="-.16" cy="-.13" rx=".36" ry=".1" fill="#EEA9B3"/></g>'
    # five petal flower
    '<g id="tfl"><g fill="#A7B3E3">' + "".join(f'<circle cx="{f(math.cos(a))}" cy="{f(math.sin(a))}" r=".95"/>' for a in [i * 2 * math.pi / 5 - math.pi / 2 for i in range(5)])
    + '</g><circle r=".55" fill="#F6D77A"/></g>'
    # strawberry sitting on a cream dollop, tip up
    '<g id="tsb"><ellipse cy=".05" rx=".85" ry=".44" fill="#FFFDF8"/>'
    '<path d="M0,-1.3 C.4,-1.25 .82,-.62 .72,-.26 C.6,.05 -.6,.05 -.72,-.26 C-.82,-.62 -.4,-1.25 0,-1.3Z" fill="#DB3440"/>'
    '<path d="M-.38,-.85 q.1,-.3 .36,-.36" stroke="#F58A8F" stroke-width=".1" fill="none" stroke-linecap="round"/>'
    '<g fill="#F9D47A">' + "".join(f'<ellipse cx="{dx}" cy="{dy}" rx=".05" ry=".08"/>' for dx, dy in [(-.3, -.5), (.25, -.62), (0, -.9), (-.45, -.25), (.42, -.3), (0, -.35)]) + '</g>'
    '<g fill="#3F7A3D"><ellipse cx="-.42" cy="-.02" rx=".38" ry=".16" transform="rotate(28 -.42 0)"/><ellipse cx=".42" cy="-.02" rx=".38" ry=".16" transform="rotate(-28 .42 0)"/><ellipse cy="-.02" rx=".38" ry=".16"/></g></g>'
)


def crown(w, rx, ry, yT):
    """Strawberries on the top plus a bunting on two sticks; shown only on the top tier."""
    out = []
    b = max(8, min(16, w * .066))
    n = max(4, round(w / 30))
    ring = [(CX + rx * .72 * math.cos(2 * math.pi * k / n + .3), yT + ry * .72 * math.sin(2 * math.pi * k / n + .3)) for k in range(n)]
    back = [p for p in ring if p[1] < yT]
    front = [p for p in ring if p[1] >= yT]
    hb = max(w * .5, 72)
    xb, xt = w * .36, max(w * .42, 66)
    top = yT - hb
    sticks = (f'<path d="M{f(CX - xb)},{f(yT + ry * .15)} L{f(CX - xt)},{f(top)} M{f(CX + xb)},{f(yT + ry * .15)} L{f(CX + xt)},{f(top)}" '
              f'stroke="#B98352" stroke-width="3" stroke-linecap="round"/>')
    # string sagging between the stick tips, flags hang from it
    sx0, sx1, sy = CX - xt, CX + xt, top + 5
    sag = (sx1 - sx0) * .14
    q = lambda t: ((1 - t) ** 2 * sx0 + 2 * (1 - t) * t * CX + t * t * sx1, (1 - t) ** 2 * sy + 2 * (1 - t) * t * (sy + 2 * sag) + t * t * sy)
    flags = [f'<path d="M{f(sx0)},{f(sy)} Q{f(CX)},{f(sy + 2 * sag)} {f(sx1)},{f(sy)}" fill="none" stroke="#FFFDF8" stroke-width="1.4"/>']
    m = len(WORD)
    fw = (sx1 - sx0) * .84 / m
    for i, ch in enumerate(WORD):
        t = (i + .5) / m * .92 + .04
        x, y = q(t)
        dx = 2 * (1 - t) * (CX - sx0) + 2 * t * (sx1 - CX)
        dy = 2 * (1 - t) * (2 * sag) + 2 * t * (-2 * sag)
        ang = math.degrees(math.atan2(dy, dx)) * .6
        hh = fw * 1.3
        flags.append(f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)})"><path d="M{f(-fw * .46)},0 H{f(fw * .46)} V{f(hh)} L0,{f(hh * .76)} L{f(-fw * .46)},{f(hh)}Z" fill="{FLAGS[i % len(FLAGS)]}"/>'
                     f'<text y="{f(hh * .52)}" font-size="{f(fw * .62)}" text-anchor="middle" fill="#FFFDF8" font-weight="700" font-family="system-ui, sans-serif">{ch}</text></g>')
    out.append(sticks + "".join(flags))
    out += [strawberry(x, y, b) for x, y in sorted(back, key=lambda p: p[1])]
    out += [strawberry(x, y, b) for x, y in sorted(front, key=lambda p: p[1])]
    return f'<g class="crown">{"".join(out)}</g>', hb + 6


def tier(i, w, h, yB):
    rx, ry = w / 2, w / 2 * K
    yT = yB - h
    x0, x1 = CX - rx, CX + rx
    body = f"M{f(x0)},{f(yT)} V{f(yB)} A{f(rx)} {f(ry)} 0 0 0 {f(x1)},{f(yB)} V{f(yT)}Z"
    s = max(8, min(15, w * .056))
    g = [f'<clipPath id="tc{i}"><path d="{body}"/></clipPath>', f'<path d="{body}" fill="url(#tier-shade)"/>']
    deco = []
    if i % 2 == 0:  # polka dots that wrap around the cylinder
        rows = int((h - s) // 15)
        for r in range(rows):
            yy = yT + ry + s * .6 + 15 * r + 8
            for k in range(-9, 10):
                phi = (k + (r % 2) * .5) * math.pi / 19
                if abs(phi) >= math.pi / 2 * .97:
                    continue
                deco.append(f'<ellipse cx="{f(CX + rx * math.sin(phi))}" cy="{f(yy + ry * math.cos(phi))}" rx="{f(2.1 * math.cos(phi))}" ry="2.1"/>')
        g.append(f'<g clip-path="url(#tc{i})" fill="#FCE4E5">{"".join(deco)}</g>')
    else:  # two rows of white swags with little blue flowers at the peaks
        segs = max(3, round(w / 55))
        for row, frac in enumerate((.36, .68)):
            y0 = yT + h * frac - 6
            pts = [(CX + rx * math.sin(-math.pi / 2 + math.pi * k / segs), y0 + ry * math.cos(-math.pi / 2 + math.pi * k / segs)) for k in range(segs + 1)]
            dip = h * .17
            d = "".join(f'M{f(a[0])},{f(a[1])} Q{f((a[0] + c[0]) / 2)},{f((a[1] + c[1]) / 2 + 2 * dip)} {f(c[0])},{f(c[1])}' for a, c in zip(pts, pts[1:]))
            g.append(f'<g clip-path="url(#tc{i})" fill="none" stroke-linecap="round"><path d="{d}" stroke="#FFF8F2" stroke-width="3.4"/>'
                     f'<path d="{d}" stroke="#C97C8C" stroke-width=".9" transform="translate(0 3.4)"/></g>')
            g += [flower(x, y, 2.6 if w > 120 else 2.1) for x, y in pts[1:-1]]
    g.append(f'<ellipse cx="{CX}" cy="{f(yT)}" rx="{f(rx)}" ry="{f(ry)}" fill="url(#tier-top)"/>')
    g.append(rope(CX, yT, rx, ry, s * .95, "tbr", "#A95569", back=True))
    g.append(rope(CX, yT, rx, ry, s * .95, "tbr", "#A95569"))
    g.append(rope(CX, yB, rx + s * .25, ry + s * .06, s * 1.35, "tbw", "#E9DCCB"))
    c, head = crown(w, rx, ry, yT)
    g.append(c)
    return f'<g class="tier" data-tier="{i + 1}">{"".join(g)}</g>', yT, head


def stand():
    cy, rx, ry = YB + 4, 188, 188 * K
    return (f'<ellipse cx="{CX}" cy="{YB + 100}" rx="96" ry="9" fill="#8E7A92" opacity=".18"/>'
            f'<path d="M{CX - 30},{f(cy + ry + 6)} C{CX - 24},{f(cy + 52)} {CX - 12},{f(cy + 58)} {CX - 12},{f(cy + 62)} '
            f'C{CX - 14},{f(cy + 74)} {CX - 60},{f(cy + 84)} {CX - 76},{f(cy + 92)} A76 12 0 0 0 {CX + 76},{f(cy + 92)} '
            f'C{CX + 60},{f(cy + 84)} {CX + 14},{f(cy + 74)} {CX + 12},{f(cy + 62)} C{CX + 12},{f(cy + 58)} {CX + 24},{f(cy + 52)} {CX + 30},{f(cy + ry + 6)}Z" fill="#A9B2DE"/>'
            f'<ellipse cx="{CX}" cy="{f(cy + 61)}" rx="17" ry="6" fill="#B9C1E8" stroke="#8C96C9" stroke-width="1.2"/>'
            f'<path d="M{CX - 6},{f(cy + 70)} C{CX - 10},{f(cy + 80)} {CX - 30},{f(cy + 88)} {CX - 46},{f(cy + 94)} M{CX + 6},{f(cy + 70)} C{CX + 10},{f(cy + 80)} {CX + 30},{f(cy + 88)} {CX + 46},{f(cy + 94)} '
            f'M{CX - 20},{f(cy + 44)} C{CX - 16},{f(cy + 50)} {CX - 12},{f(cy + 54)} {CX - 10},{f(cy + 56)}" fill="none" stroke="#8C96C9" stroke-width="1.2" stroke-linecap="round"/>'
            f'<path d="M{CX - rx},{f(cy)} v10 A{rx} {f(ry)} 0 0 0 {CX + rx},{f(cy + 10)} v-10Z" fill="#949FD2"/>'
            f'<ellipse cx="{CX}" cy="{f(cy)}" rx="{rx}" ry="{f(ry)}" fill="#B6BEE6"/>'
            f'<path d="M{CX - rx + 10},{f(cy + 6)} A{rx - 10} {f(ry - 2)} 0 0 0 {CX + rx - 10},{f(cy + 6)}" fill="none" stroke="#8C96C9" stroke-width="1.4" opacity=".6"/>')


def build():
    defs = ('<defs>' + SYMBOLS + '<linearGradient id="tier-shade" x1="0" x2="1">'
            '<stop offset="0" stop-color="#E5939E"/><stop offset=".2" stop-color="#F2AEB5"/><stop offset=".55" stop-color="#F7C1C4"/>'
            '<stop offset=".85" stop-color="#F0A8AF"/><stop offset="1" stop-color="#DE8995"/></linearGradient>'
            '<radialGradient id="tier-top" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#FAD2D4"/><stop offset="1" stop-color="#F2B2B8"/></radialGradient></defs>')
    parts, tops, heads = [defs, stand()], {}, {}
    y = YB
    for i, (w, h) in enumerate(TIERS):
        g, y, head = tier(i, w, h, y)
        parts.append(g)
        tops[i + 1], heads[i + 1] = round(y), round(head)
    svg = f'<svg viewBox="0 0 400 {H}" id="cake-svg">{"".join(parts)}</svg>'
    return svg, tops, heads


if __name__ == "__main__":
    svg, tops, heads = build()
    for p in PAGES:
        path = ROOT / p
        html = path.read_text()
        html, n = re.subn(r'<svg viewBox="0 0 400 \d+" id="cake-svg">.*?</svg>', lambda m: svg, html, flags=re.S)
        assert n == 1, p
        path.write_text(html)
    print("TOPS", tops, "HEAD", heads, "H", H, f"{len(svg) / 1024:.1f} KB")
