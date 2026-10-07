# Draws the detailed cake slice for the V2 "Lidija i Milan" section and writes it into the page.
# A wedge seen from the front: the cut face shows every layer, the outer side is frosted with a
# chocolate drip, the top carries piped rosettes, raspberries, blueberries, a chocolate shard,
# mint and gold leaf, and the slice sits on a gold-rimmed plate with a fork.
# Run: python3 tools/presek.py
import math, random, re, pathlib

PAGE = pathlib.Path(__file__).resolve().parent.parent / "verzije/v2-slatki-trenuci/index.html"
rnd = random.Random(7)
f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")

X0, X1 = 230, 520          # cut face: crust side and tip
BX, BY = 140, -62          # back crust corner offset (x, y shift)
TOP, BOT = 170, 440
LAYERS = [                 # (name, y0, y1, fill)
    ("ganache", 170, 184, "#4A2A22"),
    ("sponge", 184, 240, "url(#ps-van)"),
    ("cream", 240, 258, "#FFF3E6"),
    ("jam", 258, 272, "#B8274B"),
    ("choc", 272, 330, "url(#ps-choc)"),
    ("mousse", 330, 348, "#8A5544"),
    ("sponge2", 348, 410, "url(#ps-van)"),
    ("base", 410, 440, "url(#ps-base)"),
]
LABELS = [                 # (text, leader start x, y, label y, key shared with its layers)
    ("ukrasi rađeni rukom", 250, 82, 64, "k-ukras"),
    ("belgijska čokolada", 505, 177, 142, "k-cok"),
    ("kore koje pečemo sami", 505, 212, 206, "k-kore"),
    ("filovi koje kuvamo sami", 505, 249, 262, "k-fil"),
    ("domaće voće", 505, 265, 318, "k-voce"),
    ("i sve to rukom", 505, 425, 404, "k-ruke"),
]
KEYS = {"ganache": "k-cok", "sponge": "k-kore", "choc": "k-kore", "sponge2": "k-kore",
        "cream": "k-fil", "mousse": "k-fil", "jam": "k-voce", "base": "k-ruke"}


def crumb(pid, base, light, dark, hole, n=26):
    dots = []
    for _ in range(n):
        x, y, r = rnd.uniform(0, 48), rnd.uniform(0, 48), rnd.uniform(.7, 2.1)
        dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{rnd.choice([light, dark, light])}"/>')
    for _ in range(4):
        x, y = rnd.uniform(4, 44), rnd.uniform(4, 44)
        rx, ry = rnd.uniform(1.6, 3.4), rnd.uniform(1, 2)
        dots.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{hole}"/><path d="M{f(x - rx)},{f(y + .4)} q{f(rx)},{f(ry * 1.4)} {f(2 * rx)},0" stroke="{light}" stroke-width=".7" fill="none"/>')
    return f'<pattern id="{pid}" width="48" height="48" patternUnits="userSpaceOnUse"><rect width="48" height="48" fill="{base}"/>{"".join(dots)}</pattern>'


def wavy(y, amp, x0=X0, x1=X1, step=14):
    pts = [(x, y + amp * math.sin(x / 9 + y)) for x in range(x0, x1 + 1, step)]
    return " L".join(f"{f(x)},{f(yy)}" for x, yy in pts)


def raspberry(x, y, s=1):
    out = [f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(11 * s)}" ry="{f(12 * s)}" fill="#9E1838"/>']
    for i in range(14):
        a, r = i * 2.4, 7.5 * s * math.sqrt((i + .5) / 14)
        cx, cy = x + r * math.cos(a), y + r * math.sin(a) * 1.08
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(3.6 * s)}" fill="#D2324F"/><circle cx="{f(cx - 1 * s)}" cy="{f(cy - 1.2 * s)}" r="{f(1 * s)}" fill="#F48A9C"/>')
    return "".join(out)


def blueberry(x, y, r=8):
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="#36406E"/><circle cx="{f(x - r * .35)}" cy="{f(y - r * .35)}" r="{f(r * .45)}" fill="#5D6BA3" opacity=".7"/>'
            f'<path d="M{f(x - 2.4)},{f(y - r + 2)} l2.4,2 l2.4,-2" stroke="#232845" stroke-width="1.4" fill="none" stroke-linecap="round"/>')


def rosette(x, y, s=1, c="#F3B6C2", d="#DF8FA0"):
    pet = "".join(f'<ellipse cx="{f(x + 9 * s * math.cos(a))}" cy="{f(y + 6 * s * math.sin(a))}" rx="{f(8 * s)}" ry="{f(6 * s)}" fill="{c}" stroke="{d}" stroke-width="1"/>'
                  for a in [i * math.pi / 3.5 for i in range(7)])
    return (f'<ellipse cx="{f(x)}" cy="{f(y + 6 * s)}" rx="{f(18 * s)}" ry="{f(7 * s)}" fill="#2E1A15" opacity=".35"/>{pet}'
            f'<ellipse cx="{f(x)}" cy="{f(y - 2 * s)}" rx="{f(9 * s)}" ry="{f(7 * s)}" fill="{c}"/>'
            f'<path d="M{f(x - 6 * s)},{f(y - 1 * s)} q{f(6 * s)},{f(-9 * s)} {f(11 * s)},{f(-1 * s)} q{f(-3 * s)},{f(6 * s)} {f(-9 * s)},{f(4 * s)}" stroke="{d}" stroke-width="1.4" fill="none" stroke-linecap="round"/>')


def build():
    defs = ("<defs>" + crumb("ps-van", "#F1C77E", "#F8DCA4", "#DDAA5E", "#C9914A")
            + crumb("ps-choc", "#6B3E2E", "#875240", "#55301F", "#3D2016")
            + crumb("ps-base", "#C98E4E", "#E2B074", "#A86E35", "#8C5626", 34)
            + '<linearGradient id="ps-side" x1="0" x2="1"><stop offset="0" stop-color="#E2AEB4"/><stop offset=".6" stop-color="#F2C9CD"/><stop offset="1" stop-color="#EDBEC3"/></linearGradient>'
            + '<linearGradient id="ps-gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E4235"/><stop offset="1" stop-color="#3E231C"/></linearGradient>'
            + '<linearGradient id="ps-steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F2F0"/><stop offset=".5" stop-color="#BDB7B3"/><stop offset="1" stop-color="#E7E3E0"/></linearGradient>'
            + "</defs>")
    g = [defs]
    # plate with gold rim and a soft shadow
    g.append('<g class="ps-plate"><ellipse cx="350" cy="462" rx="300" ry="56" fill="#2E1A15" opacity=".12"/>'
             '<ellipse cx="345" cy="448" rx="300" ry="58" fill="#FFFDF8" stroke="#D9B26A" stroke-width="3"/>'
             '<ellipse cx="345" cy="446" rx="232" ry="40" fill="none" stroke="#EFE3D3" stroke-width="2"/>'
             '<path d="M84 470 q 30 18 120 26" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9"/>'
             '<ellipse cx="350" cy="442" rx="190" ry="14" fill="#2E1A15" opacity=".14"/></g>')
    # fork on the plate, drawn flat and turned
    tines = "".join(f'<rect x="-86" y="{f(-11 + k * 6.4)}" width="46" height="3.6" rx="1.8"/>' for k in range(4))
    g.append('<g class="ps-fork" transform="translate(560 482) rotate(-13)" fill="url(#ps-steel)" stroke="#A39C97" stroke-width=".8">'
             f'{tines}<path d="M-44,-12 Q-14,-12 0,-3 L120,-4 q8,0 8,4 q0,4 -8,4 L0,3 Q-14,12 -44,12Z"/></g>')
    # crumbs on the plate
    g.append('<g class="ps-crumbs">' + "".join(f'<circle cx="{f(rnd.uniform(110, 600))}" cy="{f(rnd.uniform(456, 486))}" r="{f(rnd.uniform(1.2, 3))}" fill="{rnd.choice(["#DDAA5E", "#875240", "#F1C77E"])}"/>' for _ in range(16)) + "</g>")

    drips = [f"M{BX},{TOP + BY}"]
    for i in range(7):
        t0, t1 = i / 7, (i + 1) / 7
        xa = BX + (X0 - BX) * t0; ya = TOP + BY - BY * t0
        xm = BX + (X0 - BX) * (t0 + t1) / 2; ym = TOP + BY - BY * (t0 + t1) / 2
        xb = BX + (X0 - BX) * t1; yb = TOP + BY - BY * t1
        L = rnd.choice([18, 34, 52, 26, 64, 22])
        drips.append(f"L{f(xm - 4)},{f(ym)} V{f(ym + L)} a4 4 0 0 0 8 0 V{f(ym + 2)} L{f(xb)},{f(yb)}")
    drip = " ".join(drips) + f" V{TOP - 6} L{BX},{TOP + BY - 6}Z"
    pearls = "".join(f'<circle cx="{f(BX + (X0 - BX) * t / 9)}" cy="{f(BOT + BY - BY * t / 9 - 3)}" r="5" fill="#FFF8F0" stroke="#E7D6C5" stroke-width=".8"/>' for t in range(10))
    # Every layer is a solid wedge piece: frosted outer side, its own top face and the cut face.
    # Drawn bottom to top, so while the slice assembles each piece already reads as 3D,
    # and once stacked the upper pieces hide the lower tops.
    def side(y0, y1):
        return (f'<path d="M{BX},{f(y0 + BY)} Q{BX + 30},{f(y0 + BY / 2 + 6)} {X0},{y0} V{y1 + .6} '
                f'Q{BX + 30},{f(y1 + .6 + BY / 2 + 6)} {BX},{f(y1 + .6 + BY)}Z" fill="url(#ps-side)"/>')

    def top_face(y0, fill):
        t = f"M{BX},{f(y0 + BY)} Q{BX + 30},{f(y0 + BY / 2 + 6)} {X0},{y0} L{X1},{y0}Z"
        return f'<path d="{t}" fill="{fill}"/><path d="{t}" fill="#fff" opacity=".16"/><path d="M{X0},{y0} H{X1}" stroke="#fff" stroke-width="1.2" opacity=".45"/>'

    for k, (name, y0, y1, fill) in enumerate(reversed(LAYERS)):
        d = len(LAYERS) - k
        key = KEYS[name]
        piece = side(y0, y1) + (pearls if name == "base" else "")
        piece += top_face(y0, "url(#ps-gloss)" if name == "ganache" else fill)
        if name == "cream":
            shape = f'<path d="M{X0},{y0} L{wavy(y0, 1.6)} L{X1},{y1} L{X0},{y1}Z" fill="{fill}"/><path d="M{X0},{y1 - 1} H{X1}" stroke="#F3DCC6" stroke-width="2"/>'
        elif name == "jam":
            seeds = "".join(f'<ellipse cx="{f(rnd.uniform(X0 + 6, X1 - 6))}" cy="{f(rnd.uniform(y0 + 3, y1 - 3))}" rx="1.2" ry="1.8" fill="#F28AA2"/>' for _ in range(26))
            seep = "".join(f'<path d="M{f(x)},{y1} q3,{f(rnd.uniform(5, 10))} 6,0" fill="{fill}"/>' for x in range(X0 + 18, X1 - 10, 37))
            shape = f'<rect x="{X0}" y="{y0}" width="{X1 - X0}" height="{y1 - y0}" fill="{fill}"/>{seep}{seeds}<path d="M{X0},{y0 + 2} H{X1}" stroke="#E0546F" stroke-width="1.2" opacity=".7"/>'
        elif name == "mousse":
            shape = f'<path d="M{X0},{y0} L{wavy(y0, 1.2)} L{X1},{y1} L{X0},{y1}Z" fill="{fill}"/><path d="M{X0},{y0 + 4} H{X1}" stroke="#A56C5A" stroke-width="1.4" opacity=".7"/>'
        elif name == "ganache":
            shape = (f'<rect x="{X0}" y="{y0}" width="{X1 - X0}" height="{y1 - y0}" fill="url(#ps-gloss)"/><path d="M{X0 + 6},{y0 + 4} H{X1 - 40}" stroke="#9A6A5A" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>'
                     f'<path d="M{X0 + 30},{TOP - 6} L{X1 - 60},{TOP - 2}" stroke="#A7776A" stroke-width="2" stroke-linecap="round" opacity=".6"/><path d="{drip}" fill="#4A2A22"/>')
        else:
            shape = f'<rect x="{X0}" y="{y0}" width="{X1 - X0}" height="{y1 - y0}" fill="{fill}"/>'
        shape += f'<path d="M{X1},{y0} V{y1}" stroke="#2E1A15" stroke-width="2" opacity=".18"/>'
        g.append(f'<g class="ps-layer {key}" style="--d:{d}">{piece}{shape}</g>')

    # decorations on top
    deco = [rosette(166, 126, 1.45), rosette(210, 146, 1.3), rosette(286, 160, 1, "#FFF4EC", "#E8CDB8"),
            '<path d="M226 150 L244 72 L266 148Z" fill="#3B2420"/><path d="M236 138 L246 84" stroke="#7A5246" stroke-width="2.4" stroke-linecap="round"/><path d="M244 72 L266 148 L256 150Z" fill="#2A1712"/>',
            '<path d="M310 164 q20 -28 46 -15 q-18 23 -46 15Z" fill="#4F8A4B"/><path d="M312 163 q18 -13 38 -13" stroke="#2F5E31" stroke-width="1.3" fill="none"/>',
            raspberry(166, 104, 1.3), raspberry(210, 126, 1.15), raspberry(286, 148, .9), blueberry(190, 128, 9), blueberry(246, 156, 8), blueberry(372, 166, 6.5),
            "".join(f'<path d="M{f(x)},{f(y)} l4,-2 l2,4 l-5,1Z" fill="#E0B44C"/>' for x, y in [(330, 164), (390, 166), (420, 167), (256, 120), (190, 104)])]
    g.append(f'<g class="ps-layer ps-top k-ukras" style="--d:{len(LAYERS) + 1}">{"".join(deco)}</g>')

    # leader lines and labels; each label carries the key of the layers it describes
    lab = []
    for text, sx, sy, ly, key in LABELS:
        lab.append(f'<g class="ps-lab {key}"><rect class="ps-hit" x="556" y="{ly - 30}" width="{len(text) * 12 + 20}" height="42" rx="21"/>'
                   f'<circle cx="{sx}" cy="{sy}" r="3.2"/><path d="M{sx},{sy} C{sx + 40},{sy} {556 - 34},{ly - 6} 556,{ly - 6}"/><text x="566" y="{ly}">{text}</text></g>')
    g.append(f'<g class="ps-labels">{"".join(lab)}</g>')
    return f'<svg viewBox="-120 20 920 490" aria-hidden="true" class="ps-svg">{"".join(g)}</svg>'


if __name__ == "__main__":
    svg = build()
    html = PAGE.read_text()
    html, n = re.subn(r'<svg viewBox="[^"]*" aria-hidden="true" class="ps-svg">.*?</svg>', lambda m: svg, html, flags=re.S)
    assert n == 1, "slice placeholder not found"
    PAGE.write_text(html)
    print(f"{len(svg) / 1024:.1f} KB")
