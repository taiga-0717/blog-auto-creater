"""関数 y=ax² プリント用の共通部品（グラフ SVG・分数・空欄など）"""
from fractions import Fraction as Fr

_clip = [0]


def fr(a, b=None):
    """分数の表示。fr(1,2) / fr(Fraction) / fr('x²','2') など"""
    if b is None:
        f = Fr(a)
        if f.denominator == 1:
            return str(f.numerator)
        sign = "−" if f < 0 else ""
        return f'{sign}<span class="frac"><span>{abs(f.numerator)}</span><span>{f.denominator}</span></span>'
    return f'<span class="frac"><span>{a}</span><span>{b}</span></span>'


def num(v):
    """数値を見やすく（負号は全角マイナス）"""
    f = Fr(v).limit_denominator(100)
    if f.denominator == 1:
        return str(f.numerator).replace("-", "−")
    return fr(f)


def bl(ch="", cls=""):
    return f'<span class="bl {cls}"><i>{ch}</i></span>'


def R(t):
    return f'<span class="red">{t}</span>'


def graph(xmin, xmax, ymin, ymax, u=6.0, curves=(), pts=(), segs=(), polys=(), hl=(),
          nums=True, xstep=1, ystep=1, grid=True, extra=""):
    """方眼つき座標平面。単位は mm（u = 1目盛りの mm）
    curves: dict(f, x0, x1, w=0.6, dash=False, lab=None, lx=None, ly=None)
    pts:    (x, y, label, dx, dy)  ラベル位置は mm で微調整
    segs:   (x1, y1, x2, y2, dash)
    polys:  ([(x,y),...], fill)
    hl:     太線で強調する区間 dict(f, x0, x1)
    """
    _clip[0] += 1
    cid = f"cp{_clip[0]}"
    pad = 5
    W, H = (xmax - xmin) * u, (ymax - ymin) * u
    X = lambda x: (x - xmin) * u
    Y = lambda y: (ymax - y) * u
    o = []
    if grid:
        for i in range(int(xmin), int(xmax) + 1):
            o.append(f'<line x1="{X(i):.2f}" y1="0" x2="{X(i):.2f}" y2="{H:.2f}" stroke="#c8c8c8" stroke-width="0.18"/>')
        for j in range(int(ymin), int(ymax) + 1):
            o.append(f'<line x1="0" y1="{Y(j):.2f}" x2="{W:.2f}" y2="{Y(j):.2f}" stroke="#c8c8c8" stroke-width="0.18"/>')
    # 軸
    if ymin <= 0 <= ymax:
        o.append(f'<line x1="-2" y1="{Y(0):.2f}" x2="{W + 2.5:.2f}" y2="{Y(0):.2f}" stroke="#111" stroke-width="0.35"/>')
        o.append(f'<path d="M{W + 3.5:.2f} {Y(0):.2f} l-2.2 -1 v2 z" fill="#111"/>')
        o.append(f'<text x="{W + 3.4:.2f}" y="{Y(0) + 3.6:.2f}" font-size="3.4" font-style="italic">x</text>')
    if xmin <= 0 <= xmax:
        o.append(f'<line x1="{X(0):.2f}" y1="{H + 2:.2f}" x2="{X(0):.2f}" y2="-2.5" stroke="#111" stroke-width="0.35"/>')
        o.append(f'<path d="M{X(0):.2f} -3.5 l-1 2.2 h2 z" fill="#111"/>')
        o.append(f'<text x="{X(0) + 1.4:.2f}" y="-1.6" font-size="3.4" font-style="italic">y</text>')
        if ymin <= 0 <= ymax:
            o.append(f'<text x="{X(0) - 2.9:.2f}" y="{Y(0) + 3.2:.2f}" font-size="2.9">O</text>')
    if nums:
        fs = 2.6 if u >= 5 else 2.2
        if ymin <= 0 <= ymax:
            for i in range(int(xmin), int(xmax) + 1):
                if i != 0 and i % xstep == 0:
                    o.append(f'<text x="{X(i):.2f}" y="{Y(0) + 3.2:.2f}" font-size="{fs}" text-anchor="middle" stroke="#fff" stroke-width="0.7" paint-order="stroke">{str(i).replace("-", "−")}</text>')
        if xmin <= 0 <= xmax:
            for j in range(int(ymin), int(ymax) + 1):
                if j != 0 and j % ystep == 0:
                    o.append(f'<text x="{X(0) - 0.9:.2f}" y="{Y(j) + 0.95:.2f}" font-size="{fs}" text-anchor="end" stroke="#fff" stroke-width="0.7" paint-order="stroke">{str(j).replace("-", "−")}</text>')
    o.append(f'<clipPath id="{cid}"><rect x="0" y="0" width="{W:.2f}" height="{H:.2f}"/></clipPath>')
    g = []
    for pl, fill in polys:
        ps = " ".join(f"{X(x):.2f},{Y(y):.2f}" for x, y in pl)
        g.append(f'<polygon points="{ps}" fill="{fill}" stroke="#111" stroke-width="0.3"/>')
    for c in curves:
        n = 160
        x0, x1 = c.get("x0", xmin), c.get("x1", xmax)
        ps = " ".join(f"{X(x0 + (x1 - x0) * k / n):.2f},{Y(c['f'](x0 + (x1 - x0) * k / n)):.2f}" for k in range(n + 1))
        da = ' stroke-dasharray="1.6 1.2"' if c.get("dash") else ""
        g.append(f'<polyline points="{ps}" fill="none" stroke="#111" stroke-width="{c.get("w", 0.55)}"{da}/>')
    for c in hl:
        n = 80
        x0, x1 = c["x0"], c["x1"]
        ps = " ".join(f"{X(x0 + (x1 - x0) * k / n):.2f},{Y(c['f'](x0 + (x1 - x0) * k / n)):.2f}" for k in range(n + 1))
        g.append(f'<polyline points="{ps}" fill="none" stroke="#111" stroke-width="1.6" stroke-linecap="round" opacity="0.85"/>')
    for x1, y1, x2, y2, dash in segs:
        da = ' stroke-dasharray="1.2 1"' if dash else ""
        g.append(f'<line x1="{X(x1):.2f}" y1="{Y(y1):.2f}" x2="{X(x2):.2f}" y2="{Y(y2):.2f}" stroke="#111" stroke-width="{0.3 if dash else 0.5}"{da}/>')
    o.append(f'<g clip-path="url(#{cid})">' + "".join(g) + "</g>")
    for c in curves:
        if c.get("lab"):
            o.append(f'<text x="{X(c["lx"]):.2f}" y="{Y(c["ly"]):.2f}" font-size="{c.get("fs", 3)}" text-anchor="middle" stroke="#fff" stroke-width="0.9" paint-order="stroke">{c["lab"]}</text>')
    for p in pts:
        x, y, lab = p[0], p[1], p[2]
        dx, dy = (p[3], p[4]) if len(p) > 3 else (1.5, -1.5)
        o.append(f'<circle cx="{X(x):.2f}" cy="{Y(y):.2f}" r="0.85" fill="#111"/>')
        if lab:
            o.append(f'<text x="{X(x) + dx:.2f}" y="{Y(y) + dy:.2f}" font-size="3" text-anchor="middle" stroke="#fff" stroke-width="0.9" paint-order="stroke">{lab}</text>')
    o.append(extra.format(X=X, Y=Y) if extra else "")
    vb = f"{-pad - 3} {-pad - 1} {W + 2 * pad + 5} {H + 2 * pad + 1}"
    return (f'<svg width="{W + 2 * pad + 5:.1f}mm" viewBox="{vb}" font-family="BIZ UDPGothic, sans-serif">'
            + "".join(o) + "</svg>")


def sq(a):
    return lambda x: a * x * x
