# Procedural, photo-real decoration rasters for the Lidija site (paper grain, torn edges, washi tape, glossy drips).
import re, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'deco') + '/'

def hexrgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255

def noise2(h, w, beta, rng, aniso=(1, 1)):
    """Periodic 1/f^beta noise, zero mean, unit std."""
    fy = np.fft.fftfreq(h)[:, None] * aniso[0]; fx = np.fft.fftfreq(w)[None, :] * aniso[1]
    f = np.sqrt(fx ** 2 + fy ** 2); f[0, 0] = 1
    spec = (rng.normal(size=(h, w)) + 1j * rng.normal(size=(h, w))) / f ** (beta / 2)
    spec[0, 0] = 0
    n = np.real(np.fft.ifft2(spec)); return (n - n.mean()) / n.std()

def noise1(n, beta, rng):
    f = np.fft.rfftfreq(n); f[0] = 1
    spec = (rng.normal(size=f.size) + 1j * rng.normal(size=f.size)) / f ** (beta / 2); spec[0] = 0
    v = np.fft.irfft(spec, n); return (v - v.mean()) / v.std()

def save(arr, name, q=90):
    """arr: float RGBA 0..1"""
    im = Image.fromarray((np.clip(arr, 0, 1) * 255 + .5).astype(np.uint8), 'RGBA')
    im.save(OUT + name, 'WEBP', quality=q, alpha_quality=100, method=6)
    return im

def down(a, k):
    k = int(k); return np.vstack([np.zeros((k,) + a.shape[1:], a.dtype), a[:-k]]) if k else a

def smooth(x): return np.clip(x, 0, 1) ** 2 * (3 - 2 * np.clip(x, 0, 1))

# ---------- paper grain overlay (tileable) ----------
def grain_field(h, w, rng):
    g = .55 * noise2(h, w, .6, rng) + .45 * noise2(h, w, 2.4, rng)
    fib = np.zeros((h, w), np.float32)
    for _ in range(int(h * w / 2600)):
        y, x = rng.uniform(0, h), rng.uniform(0, w); a = rng.uniform(0, np.pi); s = rng.choice([-1, 1]) * rng.uniform(.5, 1)
        for _ in range(int(rng.uniform(8, 34))):
            fib[int(y) % h, int(x) % w] += s; a += rng.normal(0, .25); y += np.sin(a); x += np.cos(a)
    return g, nd.gaussian_filter(fib, .6, mode='wrap')

def grain(name='grain.webp', size=512, strength=.075, seed=1):
    rng = np.random.default_rng(seed); g, fib = grain_field(size, size, rng)
    v = g * .55 + fib * 1.6
    light = v > 0
    rgb = np.where(light[..., None], np.array([1, 1, 1.0]), np.array([.36, .28, .2]))
    a = np.clip(np.abs(v) * strength, 0, .22)
    save(np.dstack([rgb, a]), name)

# ---------- torn paper strip ----------
def torn(name, color, rim='#FBF9F2', W=2400, H=56, seed=3, amp=7.0, grain_k=.05):
    rng = np.random.default_rng(seed)
    x = np.arange(W)
    ye = H * .40 + amp * .6 * noise1(W, 2.3, rng) + .9 * noise1(W, 1.4, rng) + .35 * noise1(W, .6, rng)
    ye = np.clip(ye, 5, H * .78)
    rw = 3 + 4.5 * np.abs(noise1(W, 2.4, rng)) + .6 * np.abs(noise1(W, 1.2, rng))                   # visible white core width
    Y = np.arange(H)[:, None].astype(np.float32)
    fuzz = .9 * noise2(H, W, .2, rng)
    surf = smooth(Y - (ye + rw)[None, :] + .5)                       # coloured face
    core = smooth((Y - ye[None, :] + .8 + .35 * fuzz) / 1.6)          # white torn core
    # fibres sticking out of the tear
    fib = np.zeros((H, W), np.float32)
    for _ in range(int(W / 4)):
        px = rng.uniform(0, W); py = np.interp(px, x, ye) + rng.uniform(0, 3)
        a = -np.pi / 2 + rng.normal(0, .75); L = rng.uniform(2, 13); k = rng.uniform(.35, .9)
        for t in np.linspace(0, L, int(L * 2)):
            yy, xx = int(py + np.sin(a) * t), int(px + np.cos(a) * t) % W
            if 0 <= yy < H: fib[yy, xx] = max(fib[yy, xx], k * (1 - t / L * .5))
            a += rng.normal(0, .06)
    fib = nd.gaussian_filter(fib, .45) * 1.6
    alpha = np.clip(np.maximum(core, fib), 0, 1)
    g, f2 = grain_field(H, W, rng); gr = (g * .5 + f2 * 1.4) * grain_k
    base = hexrgb(color); rimc = hexrgb(rim)
    # face: colour + grain, slight lift just under the tear
    lift = np.exp(-np.clip(Y - (ye + rw)[None, :], 0, 99) / 2.5) * .05
    face = base[None, None, :] * (1 + gr[..., None]) + lift[..., None]
    # core: off-white, a touch of the paper colour bleeding in, slight shadow where the face overhangs it
    over = np.exp(-np.clip((ye + rw)[None, :] - Y, 0, 99) / 1.3) * .09
    corec = rimc[None, None, :] * (1 + gr[..., None] * .6 - over[..., None]) * .92 + base * .08
    rgb = face * surf[..., None] + corec * (1 - surf[..., None])
    # soft contact shadow under the whole sheet
    sh = nd.gaussian_filter(down(alpha, 2), 2.6) * .26
    out_a = alpha + sh * (1 - alpha)
    out_rgb = (rgb * alpha[..., None] + np.array([.18, .14, .1]) * (sh * (1 - alpha))[..., None]) / np.maximum(out_a, 1e-4)[..., None]
    return save(np.dstack([out_rgb, out_a]), name)

# ---------- washi tape ----------
def washi(name, color, W=200, H=56, seed=5, opacity=.74):
    rng = np.random.default_rng(seed); pad = 10; Wt, Ht = W + 2 * pad, H + 2 * pad
    Y, X = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
    def end(sd):
        r = np.random.default_rng(sd); y = np.arange(Ht)
        tri = np.abs(((y / r.uniform(5, 7.5)) % 2) - 1) * r.uniform(2.5, 4.5)
        return tri + 1.4 * noise1(Ht, 1.2, r) + r.uniform(-1, 1)
    xl = pad + end(seed * 7 + 1)[:, None]; xr = Wt - pad - end(seed * 7 + 2)[:, None]
    yt = pad + .5 * noise1(Wt, 1.5, rng)[None, :]; yb = Ht - pad + .5 * noise1(Wt, 1.5, rng)[None, :]
    fz = .8 * noise2(Ht, Wt, .3, rng)
    m = smooth(X - xl + .5 + fz) * smooth(xr - X + .5 + fz) * smooth(Y - yt + .5) * smooth(yb - Y + .5)
    # washi fibres: long streaky noise in random directions + fine grain
    fib = .5 * noise2(Ht, Wt, 1.2, rng, aniso=(1, .25)) + .35 * noise2(Ht, Wt, 1.2, rng, aniso=(.3, 1)) + .4 * noise2(Ht, Wt, .4, rng)
    edge = np.exp(-np.minimum(Y - yt, yb - Y).clip(0) / 1.2) * .25        # denser long edges
    wr = np.zeros((Ht, Wt), np.float32)                                      # wrinkles near torn ends
    for cx in (xl.mean() + rng.uniform(4, 14), xr.mean() - rng.uniform(4, 14)):
        wr += np.exp(-((X - cx - (Y - Ht / 2) * rng.uniform(-.25, .25)) ** 2) / 3) * rng.uniform(-.12, .12)
    base = hexrgb(color)
    rgb = base[None, None, :] * (1 + .06 * fib[..., None] + wr[..., None]) + .05
    a = m * np.clip(opacity + .07 * fib + edge + np.abs(wr), 0, .95)
    sh = nd.gaussian_filter(down(m, 1), 1.3) * .14
    out_a = a + sh * (1 - a)
    out_rgb = (rgb * a[..., None] + .15 * (sh * (1 - a))[..., None]) / np.maximum(out_a, 1e-4)[..., None]
    return save(np.dstack([out_rgb, out_a]), name)

# ---------- glossy drips from the SVG drip paths ----------
def path_points(d, steps=24):
    toks = re.findall(r'[MHVCSLZ]|-?\d*\.?\d+', d); i = 0; pts = []; cur = np.zeros(2); cmd = None; last_c2 = None
    def num():
        nonlocal i; v = float(toks[i]); i += 1; return v
    while i < len(toks):
        if re.match('[A-Z]', toks[i]): cmd = toks[i]; i += 1
        if cmd == 'M': cur = np.array([num(), num()]); pts.append(cur.copy()); last_c2 = None
        elif cmd == 'H': cur = np.array([num(), cur[1]]); pts.append(cur.copy()); last_c2 = None
        elif cmd == 'V': cur = np.array([cur[0], num()]); pts.append(cur.copy()); last_c2 = None
        elif cmd == 'L': cur = np.array([num(), num()]); pts.append(cur.copy()); last_c2 = None
        elif cmd in 'CS':
            if cmd == 'C': c1 = np.array([num(), num()])
            else: c1 = 2 * cur - last_c2 if last_c2 is not None else cur.copy()
            c2 = np.array([num(), num()]); p = np.array([num(), num()])
            for t in np.linspace(0, 1, steps)[1:]:
                pts.append((1 - t) ** 3 * cur + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * p)
            cur = p; last_c2 = c2
        elif cmd == 'Z': pass
    return pts

def drip(name, d, color, vb=(1440, 90), scale=2, extra=12, R=16, ks=.9, kd=.5, amb=.6, floor=.9, shadow=.24):
    W, H0 = vb[0] * scale, vb[1] * scale; H = H0 + extra * scale; ss = 4
    im = Image.new('L', (W * ss, H * ss), 0)
    ImageDraw.Draw(im).polygon([(x * scale * ss, y * scale * ss) for x, y in path_points(d)], fill=255)
    m = np.asarray(im.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
    padm = np.vstack([np.ones((60, W), np.float32), m])                       # glaze continues above the image
    dist = nd.distance_transform_edt(padm > .5)[60:] + (m - .5)
    hgt = R * np.sqrt(1 - np.clip(1 - dist / R, 0, 1) ** 2)
    hgt = nd.gaussian_filter(hgt, 1.6)
    gy, gx = np.gradient(hgt)
    N = np.dstack([-gx, -gy, np.ones_like(hgt)]); N /= np.linalg.norm(N, axis=2, keepdims=True)
    V = np.array([0, 0, 1.])
    L = np.array([-.3, -.55, 1.]); L /= np.linalg.norm(L)
    dif = (N @ L).clip(0); flat = L[2]
    shade = np.maximum((amb + kd * dif) / (amb + kd * flat), floor)
    # studio environment reflection: soft window on the left, softbox above
    ndv = N[..., 2]; R = 2 * ndv[..., None] * N - V
    env = 1.0 * np.exp(-((R[..., 0] + .62) ** 2) / .018) * np.exp(-((R[..., 1] + .1) ** 2) / .5) \
        + .7 * np.exp(-((R[..., 1] + .7) ** 2) / .025) * np.exp(-(R[..., 0] ** 2) / .6) \
        + .25 * np.exp(-((R[..., 0] - .7) ** 2) / .03)
    fres = .04 + .96 * (1 - ndv.clip(0, 1)) ** 5
    spec = ks * (.35 + fres) * env
    base = hexrgb(color)
    rgb = base[None, None, :] * shade[..., None] + spec[..., None]
    # cast shadow onto whatever is below
    sh = nd.gaussian_filter(down(m, 4 * scale), 4 * scale) * shadow
    sh[: int(H0 * .2)] = 0
    a = m + sh * (1 - m)
    out = (rgb * m[..., None] + np.array([.16, .08, .12]) * (sh * (1 - m))[..., None]) / np.maximum(a, 1e-4)[..., None]
    return save(np.dstack([out, a]), name, q=92)

# ---------- gingham: woven thread by thread (plain weave) ----------
def gingham_weave(name, color='#F4A3B5', base='#FFFAFB', period=112, pitch=4, reps=4, strength=.38, seed=22):
    T = period * reps; rng = np.random.default_rng(seed)
    n = T // pitch                                             # threads per tile
    idx = np.arange(T) // pitch
    pos = (np.arange(T) % pitch + .5) / pitch                  # position across a thread 0..1
    per = period // pitch
    warp_pink = ((np.arange(n) % per) < per // 2)              # vertical threads (index by x)
    weft_pink = ((np.arange(n) % per) < per // 2)              # horizontal threads (index by y)
    W, P = hexrgb(base), hexrgb(base) * (1 - strength) + hexrgb(color) * strength
    tw = rng.normal(1, .025, n); tf = rng.normal(1, .025, n)  # per-thread tone
    slub_w = 1 + .03 * noise2(T, n, 1.4, rng, aniso=(1, 9)).T   # along-thread variation (n, T)
    slub_f = 1 + .03 * noise2(T, n, 1.4, rng, aniso=(1, 9)).T
    X, Y = np.meshgrid(np.arange(T), np.arange(T))
    ix, iy = idx[X], idx[Y]
    warp_top = ((ix + iy) % 2) == 0
    prof_x = .9 + .14 * np.sin(np.pi * pos[X]); prof_y = .9 + .14 * np.sin(np.pi * pos[Y])
    col_w = np.where(warp_pink[ix][..., None], P, W) * (tw[ix] * prof_x * slub_w[ix, Y])[..., None]
    col_f = np.where(weft_pink[iy][..., None], P, W) * (tf[iy] * prof_y * slub_f[iy, X])[..., None]
    rgb = np.where(warp_top[..., None], col_w, col_f)
    rgb = nd.gaussian_filter(rgb, (.55, .55, 0), mode='wrap')
    rgb *= (1 + .018 * noise2(T, T, 2.6, rng))[..., None]
    return save(np.dstack([rgb, np.ones((T, T))]), name, q=94)

# ---------- satin ribbon (vertical tile, repeat-y) ----------
def satin(name, color='#F29AB2', w=80, L=640, seed=31, rot=False, hi='#FFD9E3'):
    rng = np.random.default_rng(seed)
    y = np.arange(L, dtype=np.float32); x = (np.arange(w) + .5) / w
    s = noise1(L, 3.4, rng); s = (s - s.min()) / (s.max() - s.min())      # broad sheen bands along the length
    tilt = .35 * noise1(L, 3.0, rng)                                         # gentle twist moves the sheen across
    X, Y = np.meshgrid(np.arange(w), y)
    u = x[None, :] + tilt[:, None] * (x[None, :] - .5)
    band = np.exp(-((u - .5) ** 2) / .5)
    k = (s[:, None] ** 2.2) * band                                           # 0 = body colour, 1 = sheen colour
    shade = .9 + .08 * np.sin(np.pi * x)[None, :] - .1 * (1 - s[:, None]) ** 3
    twill = .018 * np.sin(2 * np.pi * (X + Y) / 3.0) + .01 * noise2(L, w, .3, rng)
    edge = np.minimum(X, w - 1 - X)
    selv = np.where(edge < 1, -.14, 0) + np.where((edge >= 2) & (edge < 3), -.06, 0) + np.where((edge >= 3) & (edge < 4), .04, 0)
    body, sh = hexrgb(color), hexrgb(hi)
    rgb = (body[None, None, :] * (1 - k[..., None] * .8) + sh[None, None, :] * (k[..., None] * .8)) * (shade + twill + selv)[..., None]
    alpha = np.where(edge < .5, .6, 1.0) * np.ones((L, w))
    arr = np.dstack([rgb, alpha])
    if rot: arr = np.rot90(arr)
    return save(arr, name, q=92)

# ---------- twisted twine (vertical tile) ----------
def twine(name, color='#D9B98E', w=10, L=96, seed=41):
    rng = np.random.default_rng(seed)
    X, Y = np.meshgrid((np.arange(w) + .5) / w, np.arange(L, dtype=np.float32))
    ply = (np.sin(2 * np.pi * (Y / 12 + X * .9)) + 1) / 2                   # 3-ply twist
    round_ = np.sin(np.pi * X) ** .7
    lum = (.62 + .5 * ply ** 1.5) * (.55 + .5 * round_) + .05 * noise2(L, w, .5, rng)
    a = np.clip(np.sin(np.pi * X) * 3, 0, 1)
    rgb = hexrgb(color)[None, None, :] * lum[..., None]
    return save(np.dstack([rgb, a]), name, q=92)

# ---------- paper doily (punched lace, embossed, with paper grain) ----------
def doily(name, size=900, seed=51, color='#FFFFFF'):
    rng = np.random.default_rng(seed); ss = 2; S = size * ss
    Y, X = np.mgrid[0:S, 0:S].astype(np.float32); c = S / 2
    r = np.hypot(X - c, Y - c) / c; th = np.arctan2(Y - c, X - c)
    nS = 28                                                                   # scallops
    scallop_r = .93 + .055 * np.abs(np.cos(th * nS / 2))
    mask = r < scallop_r
    holes = np.zeros_like(r, bool)
    # ring of small round punches along the scallops
    for k in range(nS):
        t = (k + .5) / nS * 2 * np.pi; px, py = c + .935 * c * np.cos(t), c + .935 * c * np.sin(t)
        holes |= np.hypot(X - px, Y - py) < .018 * c
    # band of petal-shaped cut-outs
    pet = (np.abs(r - .8) < .075) & (np.cos(th * 36) > .25 + 3.5 * np.abs(r - .8))
    # fine filigree ring of slots
    slot = (np.abs(r - .67) < .028) & (np.cos(th * 96) > .35)
    # lattice band
    lat = (np.abs(r - .55) < .065) & ((np.cos(th * 48 + r * 60) > .55) | (np.cos(th * 48 - r * 60) > .55))
    # inner dotted ring
    dots = np.zeros_like(r, bool)
    for k in range(60):
        t = k / 60 * 2 * np.pi; px, py = c + .45 * c * np.cos(t), c + .45 * c * np.sin(t)
        dots |= np.hypot(X - px, Y - py) < .009 * c
    holes |= pet | slot | lat | dots
    paper = mask & ~holes
    p = Image.fromarray((paper * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    a = np.asarray(p).astype(np.float32) / 255
    # emboss: raised rims around every cut
    hgt = nd.gaussian_filter(a, 1.4); gy, gx = np.gradient(hgt)
    light = 1 + (-gx * .6 - gy * .9) * 2.2
    g, f = grain_field(size, size, rng)
    lum = (light * (1 + .025 * g + .05 * f)).clip(.7, 1.1)
    rr = np.hypot(*np.mgrid[0:size, 0:size] - size / 2) / (size / 2)
    lum *= 1 - .03 * rr                                                        # faint vignette from the table light
    rgb = hexrgb(color)[None, None, :] * lum[..., None]
    sh = nd.gaussian_filter(down(a, 4), 5) * .28
    oa = a + sh * (1 - a)
    orgb = (rgb * a[..., None] + np.array([.35, .2, .26]) * (sh * (1 - a))[..., None]) / np.maximum(oa, 1e-4)[..., None]
    return save(np.dstack([orgb, oa]), name, q=90)

# ---------- texture mapped along an SVG path (ribbons, cords) ----------
from scipy.spatial import cKDTree
def along(name, paths, vb, scale, tex, width, tex_len, shadow=.25, knots=()):
    """paths: list of SVG path d; tex: RGBA float array (rows = across, cols = along); width/tex_len in viewBox units."""
    W, H = int(vb[0] * scale), int(vb[1] * scale)
    out = np.zeros((H, W, 4), np.float32); cov = np.zeros((H, W), np.float32)
    th, tw = tex.shape[:2]
    for d in paths:
        pts = np.array(path_points(d, steps=400)) * scale
        seg = np.diff(pts, axis=0); ln = np.hypot(*seg.T); keep = ln > 1e-6; pts = np.vstack([pts[:1], pts[1:][keep]])
        seg = np.diff(pts, axis=0); ln = np.hypot(*seg.T)
        s = np.concatenate([[0], np.cumsum(ln)])
        tang = np.vstack([seg, seg[-1:]]) / np.hypot(*np.vstack([seg, seg[-1:]]).T)[:, None]
        tang = nd.gaussian_filter1d(tang, 3, axis=0); tang /= np.hypot(*tang.T)[:, None]
        nrm = np.stack([-tang[:, 1], tang[:, 0]], 1)
        w = width * scale
        ys, xs = np.mgrid[0:H, 0:W]; P = np.stack([xs.ravel(), ys.ravel()], 1).astype(np.float32)
        dist, idx = cKDTree(pts).query(P, distance_upper_bound=w)
        ok = np.isfinite(dist); P, idx = P[ok], idx[ok]
        v = ((P - pts[idx]) * nrm[idx]).sum(1); u = s[idx]
        inb = np.abs(v) < w / 2 + 1; P, v, u = P[inb], v[inb], u[inb]
        tv = (v / w + .5) * (th - 1); tu = (u / (tex_len * scale) * tw) % tw
        smp = np.stack([nd.map_coordinates(tex[..., c], [tv, tu], order=1, mode='wrap') for c in range(4)], 1)
        edge = np.clip(w / 2 + .5 - np.abs(v), 0, 1)
        a = smp[:, 3] * edge
        yy, xx = P[:, 1].astype(int), P[:, 0].astype(int)
        prev = out[yy, xx]; pa = prev[:, 3]
        na = a + pa * (1 - a)
        out[yy, xx, :3] = (smp[:, :3] * a[:, None] + prev[:, :3] * (pa * (1 - a))[:, None]) / np.maximum(na, 1e-4)[:, None]
        out[yy, xx, 3] = na
    for (kx, ky, kr, col) in knots:
        Y, X = np.mgrid[0:H, 0:W]; r = np.hypot((X - kx * scale) / (kr * scale * 1.2), (Y - ky * scale) / (kr * scale))
        m = np.clip((1 - r) * kr * scale, 0, 1); shade = .75 + .35 * np.clip(1 - np.hypot((X - kx * scale + kr * scale * .3) / (kr * scale), (Y - ky * scale + kr * scale * .4) / (kr * scale)), 0, 1)
        c = hexrgb(col)[None, None, :] * shade[..., None]
        out[..., :3] = c * m[..., None] + out[..., :3] * (1 - m[..., None]); out[..., 3] = np.maximum(out[..., 3], m)
    a = out[..., 3]; sh = nd.gaussian_filter(down(a, int(3 * scale)), 3 * scale) * shadow
    oa = a + sh * (1 - a)
    orgb = (out[..., :3] * a[..., None] + np.array([.3, .12, .2]) * (sh * (1 - a))[..., None]) / np.maximum(oa, 1e-4)[..., None]
    return save(np.dstack([orgb, oa]), name, q=90)
