# Draws the exploded cake slice for the V2 "Lidija i Milan" section and writes it into the page.
# A wedge cut from a round cake, seen from above and in front: the tip points right, the cut face
# shows toward the viewer and the outer crust curves away on the left. Every layer is its own 3D piece,
# stacked straight on the one below, so each can drop in on its own:
# chocolate biscuit base, cooked vanilla custard, chocolate sponge, cream with cut raspberries,
# vanilla sponge, Belgian chocolate ganache with drips, and fresh decorations on top.
# Run: python3 tools/presek.py
import math, random, re, pathlib

PAGE = pathlib.Path(__file__).resolve().parent.parent / "index.html"
rnd = random.Random(11)
f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")

R = 370                    # cake radius: the wedge's cut faces are R long
TA, TB = 160, 202          # plan angles of the front cut face and the hidden back cut face
PITCH = math.radians(24)   # how far we look down at the slice
CP, SP = math.cos(PITCH), math.sin(PITCH)
OX, OY = R / 2, 470        # screen position of the tip at height 0

LAYERS = [                 # bottom to top: (name, height, key shared with its label)
    ("base", 44, "k-ruke"),
    ("fil", 36, "k-fil"),
    ("choc", 80, "k-kore"),
    ("voce", 66, "k-voce"),
    ("van", 80, "k-kore"),
    ("ganache", 24, "k-cok"),
]
LABELS = {                 # key: (text, side, plan fraction from the tip toward the crust)
    "k-ukras": ("ukrasi rađeni rukom", -1, None),
    "k-cok": ("belgijska čokolada", 1, .16),
    "k-kore": ("kore koje pečemo sami", -1, .9),
    "k-voce": ("domaće voće", 1, .16),
    "k-fil": ("filovi koje kuvamo sami", -1, .9),
    "k-ruke": ("i sve to rukom", 1, .16),
}


def plan(theta, r=R):
    a = math.radians(theta)
    return r * math.cos(a), r * math.sin(a)


def scr(x, z, y):
    return OX + x, OY - y * CP + z * SP


def pts(seq):
    return " ".join(f"{f(x)},{f(y)}" for x, y in seq)


ARC = [plan(t) for t in range(TA, TB + 1, 2)]
SIDE = [plan(t) for t in range(TA, 181, 2)]    # the part of the crust that faces us
A = ARC[0]


def on_front(t, y):
    """Screen point on the cut face, t from the tip (0) to the crust (1), at height y."""
    return scr(A[0] * t, A[1] * t, y)


def crumb(pid, base, light, dark, hole, n=26, size=48):
    dots = []
    for _ in range(n):
        x, y, r = rnd.uniform(0, size), rnd.uniform(0, size), rnd.uniform(.7, 2.1)
        dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{rnd.choice([light, dark, light])}"/>')
    for _ in range(4):
        x, y = rnd.uniform(4, size - 4), rnd.uniform(4, size - 4)
        rx, ry = rnd.uniform(1.6, 3.4), rnd.uniform(1, 2)
        dots.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{hole}"/>')
    return f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse"><rect width="{size}" height="{size}" fill="{base}"/>{"".join(dots)}</pattern>'


def specks(pid, base, dot, n=30, size=40):
    d = "".join(f'<ellipse cx="{f(rnd.uniform(0, size))}" cy="{f(rnd.uniform(0, size))}" rx="{f(rnd.uniform(.4, 1.1))}" ry=".5" fill="{dot}"/>' for _ in range(n))
    return f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse"><rect width="{size}" height="{size}" fill="{base}"/>{d}</pattern>'


def grad(gid, stops, x2=1, y2=0):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


# material per layer: (top, cut face, crust side)
MAT = {
    "base": ("url(#ps-base)", "url(#ps-base)", "url(#ps-base-side)"),
    "fil": ("url(#ps-custard)", "url(#ps-custard)", "url(#ps-custard-side)"),
    "choc": ("url(#ps-choc)", "url(#ps-choc)", "url(#ps-choc-side)"),
    "voce": ("#FFF6EE", "#FFF4EA", "url(#ps-cream-side)"),
    "van": ("url(#ps-van)", "url(#ps-van)", "url(#ps-van-side)"),
    "ganache": ("url(#ps-gloss)", "#4A2A22", "url(#ps-ganache-side)"),
}


def raspberry(x, y, s=1):
    out = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(11 * s)}" ry="{f(12 * s)}" fill="#9E1838"/>']
    for i in range(14):
        a, r = i * 2.4, 7.5 * s * math.sqrt((i + .5) / 14)
        cx, cy = x + r * math.cos(a), y + r * math.sin(a) * 1.08
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(3.6 * s)}" fill="#D2324F"/><circle cx="{f(cx - 1 * s)}" cy="{f(cy - 1.2 * s)}" r="{f(1 * s)}" fill="#F48A9C"/>')
    return "".join(out)


def half_berry(x, y, s=1, sx=1):
    """A raspberry cut in half: drupelet rim, pink flesh and the hollow core."""
    rim = "".join(f'<circle cx="{f(x + 10 * s * sx * math.cos(a))}" cy="{f(y + 12 * s * math.sin(a))}" r="{f(3.4 * s)}" fill="#C42449"/>'
                  for a in [i * math.pi / 7 for i in range(14)])
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(11 * s * sx)}" ry="{f(13 * s)}" fill="#A3173A"/>{rim}'
            f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(7 * s * sx)}" ry="{f(9 * s)}" fill="#E85C7A"/>'
            f'<ellipse cx="{f(x)}" cy="{f(y + 1 * s)}" rx="{f(2.6 * s * sx)}" ry="{f(5.5 * s)}" fill="#FCE4E8"/>')


def rosette(x, y, s=1, c="#FFF7EE", d="#E9D3BF"):
    pet = "".join(f'<ellipse cx="{f(x + 10 * s * math.cos(a))}" cy="{f(y + 6 * s * math.sin(a))}" rx="{f(8.5 * s)}" ry="{f(6.5 * s)}" fill="{c}" stroke="{d}" stroke-width="1"/>'
                  for a in [i * math.pi / 3.5 for i in range(7)])
    return (f'{pet}<ellipse cx="{f(x)}" cy="{f(y - 4 * s)}" rx="{f(10 * s)}" ry="{f(8 * s)}" fill="{c}" stroke="{d}" stroke-width="1"/>'
            f'<path d="M{f(x - 7 * s)},{f(y - 3 * s)} q{f(7 * s)},{f(-12 * s)} {f(13 * s)},{f(-2 * s)} q{f(-3 * s)},{f(7 * s)} {f(-11 * s)},{f(5 * s)}" stroke="{d}" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
            f'<path d="M{f(x - 1 * s)},{f(y - 15 * s)} q{f(3 * s)},{f(5 * s)} {f(-1 * s)},{f(8 * s)}" stroke="{d}" stroke-width="1.2" fill="none" stroke-linecap="round"/>')


def leaf(x, y, rot, s=1):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({rot}) scale({s})"><path d="M0,0 q16,-18 40,-6 q-16,18 -40,6Z" fill="#5E9A55"/>'
            f'<path d="M2,0 q18,-6 34,-6" stroke="#376B37" stroke-width="1.3" fill="none"/><path d="M14,-3 l5,-6 M22,-5 l5,-5 M14,-3 l6,4 M22,-5 l6,3" stroke="#376B37" stroke-width=".9"/></g>')


def layer(name, y0, y1):
    top_f, cut_f, side_f = MAT[name]
    top = [scr(0, 0, y1)] + [scr(x, z, y1) for x, z in ARC]
    front = [scr(0, 0, y1), scr(*A, y1), scr(*A, y0), scr(0, 0, y0)]
    side = [scr(x, z, y1) for x, z in SIDE] + [scr(x, z, y0) for x, z in reversed(SIDE)]
    out = [f'<polygon points="{pts(side)}" fill="{side_f}"/>',
           f'<polygon points="{pts(side)}" fill="url(#ps-round)"/>',
           f'<polygon points="{pts(top)}" fill="{top_f}"/>',
           f'<polygon points="{pts(top)}" fill="url(#ps-light)"/>',
           f'<polygon points="{pts(front)}" fill="{cut_f}"/>']
    h = y1 - y0
    if name == "voce":
        # cream with halved raspberries pressed into the cut face and the crust
        for t in (.12, .33, .55, .77):
            x, y = on_front(t, y0 + h / 2)
            out.append(half_berry(x, y + 1, .95))
        for x, z in [plan(170, R * .97), plan(176, R * .97)]:
            sx, sy = scr(x, z, y0 + h / 2)
            out.append(half_berry(sx, sy + 1, .9, .45))
    elif name == "fil":
        # cooked custard: wavy edges and a ribbon of raspberry jam folded through
        wave = " ".join(f"L{f(x)},{f(y + 2.2 * math.sin(i * 1.3))}" for i, (x, y) in enumerate(on_front(i / 24, y0 + h * .55) for i in range(25)))
        x0, y0s = on_front(0, y0 + h * .55)
        out.append(f'<path d="M{f(x0)},{f(y0s)} {wave}" stroke="#D44A6A" stroke-width="3.2" fill="none" stroke-linecap="round" opacity=".75"/>')
    elif name == "ganache":
        # white chocolate drizzle and a glossy streak on top, drips down the cut face and the crust
        for k, (r0, r1) in enumerate([(.18, .9), (.3, .95), (.45, .97)]):
            a0, a1 = plan(TA + 8 + k * 12, R * r0), plan(TA + 14 + k * 12, R * r1)
            p0, p1 = scr(*a0, y1), scr(*a1, y1)
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 10
            out.append(f'<path d="M{f(p0[0])},{f(p0[1])} Q{f(mx)},{f(my)} {f(p1[0])},{f(p1[1])}" stroke="#FFF4E8" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".9"/>')
        g0, g1 = scr(*plan(186, R * .25), y1), scr(*plan(178, R * .75), y1)
        out.append(f'<path d="M{f(g0[0])},{f(g0[1])} L{f(g1[0])},{f(g1[1])}" stroke="#A7776A" stroke-width="4" stroke-linecap="round" opacity=".5"/>')
        drips = []
        for t, L in [(.06, 18), (.17, 34), (.27, 14), (.38, 46), (.5, 22), (.6, 38), (.71, 16), (.82, 30), (.93, 20)]:
            x, y = on_front(t, y0)
            drips.append(f'<path d="M{f(x - 5)},{f(y - 2)} V{f(y + L)} a5 5 0 0 0 10 0 V{f(y - 2)}Z"/><ellipse cx="{f(x - 1.5)}" cy="{f(y + L - 2)}" rx="1.4" ry="3" fill="#8A5E50"/>')
        for th, L in [(162, 26), (168, 12), (174, 34), (179, 18)]:
            x, y = scr(*plan(th), y0)
            drips.append(f'<path d="M{f(x - 4)},{f(y - 2)} V{f(y + L)} a4 4 0 0 0 8 0 V{f(y - 2)}Z"/>')
        out.append(f'<g fill="#4A2A22">{"".join(drips)}</g>')
    # edges: a soft highlight on the front top edge and a fine line down the crust corner
    p, q = scr(0, 0, y1), scr(*A, y1)
    out.append(f'<path d="M{f(p[0])},{f(p[1])} L{f(q[0])},{f(q[1])}" stroke="#fff" stroke-width="1.4" opacity=".5"/>')
    c0, c1 = scr(*A, y1), scr(*A, y0)
    out.append(f'<path d="M{f(c0[0])},{f(c0[1])} V{f(c1[1])}" stroke="#2E1A15" stroke-width="1.2" opacity=".18"/>')
    return "".join(out)


def build():
    defs = ("<defs>" + crumb("ps-van", "#F1C77E", "#F8DCA4", "#DDAA5E", "#C9914A")
            + crumb("ps-choc", "#6B3E2E", "#875240", "#55301F", "#3D2016")
            + crumb("ps-base", "#4E2C20", "#C98E4E", "#6E4232", "#2E1A15", 40)
            + specks("ps-custard", "#F8E2B4", "#3A2418")
            + grad("ps-van-side", [(0, "#B97A3B"), (1, "#E0A962")])
            + grad("ps-choc-side", [(0, "#3A2016"), (1, "#5E3526")])
            + grad("ps-base-side", [(0, "#2E1A15"), (1, "#4E2C20")])
            + grad("ps-custard-side", [(0, "#E6C98E"), (1, "#F8E2B4")])
            + grad("ps-cream-side", [(0, "#EBDACB"), (1, "#FFF4EA")])
            + grad("ps-ganache-side", [(0, "#2C1712"), (1, "#4A2A22")])
            + grad("ps-gloss", [(0, "#3E231C"), (.55, "#6E4235"), (1, "#4A2A22")])
            + '<linearGradient id="ps-round" x1="0" x2="1"><stop offset="0" stop-color="#2E1A15" stop-opacity=".35"/><stop offset="1" stop-color="#2E1A15" stop-opacity="0"/></linearGradient>'
            + '<linearGradient id="ps-light" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".26"/></linearGradient>'
            + '<radialGradient id="ps-shadow"><stop offset="0" stop-color="#7A2E45" stop-opacity=".28"/><stop offset="1" stop-color="#7A2E45" stop-opacity="0"/></radialGradient>'
            + "</defs>")
    g = [defs]
    # soft shadow on the table under the stack
    sx, sy = scr(-R * .5, 0, 0)
    g.append(f'<ellipse class="ps-shadow" cx="{f(sx)}" cy="{f(sy + 34)}" rx="{f(R * .72)}" ry="{f(R * .18)}" fill="url(#ps-shadow)"/>')

    y, spans = 0, {}
    for d, (name, h, key) in enumerate(LAYERS, 1):
        g.append(f'<g class="ps-layer {key}" style="--d:{d}">{layer(name, y, y + h)}</g>')
        spans.setdefault(key, (y, y + h))
        if name == "van":
            spans[key] = (y, y + h)       # the label points at the upper sponge
        y += h
    top = y

    # decorations sitting on the ganache
    fy = top
    deco = []
    for th, rr, s in [(194, .66, 1.7), (180, .34, 1.3)]:
        x, yy = scr(*plan(th, R * rr), fy)
        deco.append(rosette(x, yy, s))
    mint = scr(*plan(200, R * .58), fy)
    deco.append(leaf(mint[0] + 10, mint[1] - 16, -24, 1.5))
    curl = scr(*plan(174, R * .82), fy)
    deco.append(f'<g transform="translate({f(curl[0])} {f(curl[1])}) rotate(-12) scale(1.4)"><rect x="-26" y="-7" width="52" height="14" rx="7" fill="#F6E7D3"/>'
                f'<path d="M-22,-3 H22 M-20,3 H18" stroke="#DCC3A6" stroke-width="1.4"/><ellipse cx="26" cy="0" rx="4" ry="7" fill="#E7D1B5"/></g>')
    gold = "".join(f'<path d="M{f(x)},{f(yy)} l5,-3 l3,5 l-6,2Z" fill="#E0B44C"/>' for x, yy in [scr(*plan(th, R * rr), fy) for th, rr in [(188, .9), (170, .55), (204, .4), (192, .2)]])
    deco.append(gold)
    big = scr(*plan(194, R * .66), fy)
    deco.append(raspberry(big[0], big[1] - 34, 2.1))
    small = scr(*plan(180, R * .34), fy)
    deco.append(raspberry(small[0], small[1] - 26, 1.6))
    third = scr(*plan(170, R * .62), fy)
    deco.append(raspberry(third[0], third[1] - 14, 1.3))
    g.append(f'<g class="ps-layer k-ukras" style="--d:{len(LAYERS) + 1}">{"".join(deco)}</g>')

    # labels left and right of the stack, joined to their layer by a straight hairline
    left_x, right_x = scr(-R, 0, 0)[0] - 46, OX + 46
    lab = []
    for key, (text, side, t) in LABELS.items():
        if t is None:
            tx, ty = big[0] - 22, big[1] - 36
        else:
            y0, y1 = spans[key]
            tx, ty = on_front(t, (y0 + y1) / 2)
        lx = left_x if side < 0 else right_x
        w = len(text) * 11.6 + 24
        hx = lx - w + 12 if side < 0 else lx - 12
        anchor = "end" if side < 0 else "start"
        lab.append(f'<g class="ps-lab {key}"><rect class="ps-hit" x="{f(hx)}" y="{f(ty - 21)}" width="{f(w)}" height="42" rx="21"/>'
                   f'<circle cx="{f(tx)}" cy="{f(ty)}" r="3.2"/><path d="M{f(tx)},{f(ty)} H{f(lx - 8 * side)}"/>'
                   f'<text x="{f(lx)}" y="{f(ty + 7)}" text-anchor="{anchor}">{text}</text></g>')
    g.append(f'<g class="ps-labels">{"".join(lab)}</g>')
    y_top, y_bot = big[1] - 90, sy + 34 + R * .16
    return f'<svg viewBox="-520 {f(y_top)} 1040 {f(y_bot - y_top)}" aria-hidden="true" class="ps-svg">{"".join(g)}</svg>'


if __name__ == "__main__":
    svg = build()
    html = PAGE.read_text()
    html, n = re.subn(r'<svg viewBox="[^"]*" aria-hidden="true" class="ps-svg">.*?</svg>', lambda m: svg, html, flags=re.S)
    assert n == 1, "slice placeholder not found"
    PAGE.write_text(html)
    print(f"{len(svg) / 1024:.1f} KB")
