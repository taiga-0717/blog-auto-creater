"""円の単元プリント用の図形（SVG）を座標計算して生成する。"""
import math

FONT = 'font-family="BIZ UDPGothic, sans-serif"'


def P(deg, r=1.0, c=(0.0, 0.0)):
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def add(p, q, k=1.0):
    return (p[0] + k * q[0], p[1] + k * q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def norm(v):
    return math.hypot(v[0], v[1])


def unit(v):
    n = norm(v)
    return (v[0] / n, v[1] / n)


def dist(p, q):
    return norm(sub(p, q))


def inter(p1, p2, q1, q2):
    """直線 p1p2 と直線 q1q2 の交点"""
    d1, d2 = sub(p2, p1), sub(q2, q1)
    den = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((q1[0] - p1[0]) * d2[1] - (q1[1] - p1[1]) * d2[0]) / den
    return add(p1, d1, t)


def angle_at(v, a, b):
    da, db = unit(sub(a, v)), unit(sub(b, v))
    return math.degrees(math.acos(max(-1, min(1, da[0] * db[0] + da[1] * db[1]))))


def circumcenter(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return (ux, uy)


class Fig:
    def __init__(self, scale=58, fs=15, sw=1.7):
        self.s, self.fs, self.sw = scale, fs, sw
        self.items = []   # (z, svg string)
        self.pts = []     # bbox 用 (svg 座標)

    def X(self, p):
        return (p[0] * self.s, -p[1] * self.s)

    def _bb(self, *ps, pad=0):
        for p in ps:
            x, y = self.X(p)
            self.pts += [(x - pad, y - pad), (x + pad, y + pad)]

    def circle(self, c, r, dashed=False, w=None):
        x, y = self.X(c)
        R = r * self.s
        da = ' stroke-dasharray="5 4"' if dashed else ''
        self.items.append((1, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R:.1f}" fill="none" stroke="#111" stroke-width="{w or self.sw}"{da}/>'))
        self.pts += [(x - R, y - R), (x + R, y + R)]

    def seg(self, p, q, dashed=False, w=None):
        (x1, y1), (x2, y2) = self.X(p), self.X(q)
        da = ' stroke-dasharray="5 4"' if dashed else ''
        self.items.append((2, f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#111" stroke-width="{w or self.sw}"{da}/>'))
        self._bb(p, q)

    def poly(self, *ps, close=True):
        for i in range(len(ps) - (0 if close else 1)):
            self.seg(ps[i], ps[(i + 1) % len(ps)])

    def fill(self, *ps, color="#e4e4e4"):
        pts = " ".join(f"{self.X(p)[0]:.1f},{self.X(p)[1]:.1f}" for p in ps)
        self.items.append((0, f'<polygon points="{pts}" fill="{color}"/>'))

    def dot(self, p, r=2.6):
        x, y = self.X(p)
        self.items.append((3, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#111"/>'))

    def text(self, p, t, size=None, bold=False, at=None, off=0.0):
        """p に文字を置く。at（角度°）を与えたら、その方向に off（モデル単位）だけずらす"""
        if at is not None:
            p = add(p, P(at, off))
        x, y = self.X(p)
        fs = size or self.fs
        fw = ' font-weight="700"' if bold else ''
        self.items.append((4, f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" text-anchor="middle" dominant-baseline="central"{fw} stroke="#fff" stroke-width="4" paint-order="stroke">{t}</text>'))
        w = fs * 0.6 * max(1, len(t)) / 2
        self.pts += [(x - w, y - fs * 0.7), (x + w, y + fs * 0.7)]

    def lab(self, p, t, center=None, off=0.17, at=None):
        """点のラベル。center から外向き、または at 方向へ"""
        if at is None:
            d = unit(sub(p, center))
            at = math.degrees(math.atan2(d[1], d[0]))
        self.text(p, t, at=at, off=off)

    def ang(self, v, a, b, t=None, r=0.2, tr=None, right=False, size=None):
        """頂点 v の ∠avb に角の印（弧 or 直角）とラベル"""
        da, db = unit(sub(a, v)), unit(sub(b, v))
        A1 = math.degrees(math.atan2(da[1], da[0]))
        A2 = math.degrees(math.atan2(db[1], db[0]))
        diff = (A2 - A1) % 360
        if diff > 180:
            A1, A2 = A2, A1
            diff = 360 - diff
        mid = A1 + diff / 2
        if right:
            k = r * 0.75
            p1, p3 = add(v, da, k), add(v, db, k)
            p2 = add(p1, db, k)
            (x1, y1), (x2, y2), (x3, y3) = self.X(p1), self.X(p2), self.X(p3)
            self.items.append((2, f'<polyline points="{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}" fill="none" stroke="#111" stroke-width="1.1"/>'))
        else:
            p1, p2 = add(v, P(A1, r)), add(v, P(A2, r))
            (x1, y1), (x2, y2) = self.X(p1), self.X(p2)
            R = r * self.s
            # SVG は y 反転なので反時計回り(数学)→ sweep=0
            self.items.append((2, f'<path d="M{x1:.1f} {y1:.1f} A{R:.1f} {R:.1f} 0 0 0 {x2:.1f} {y2:.1f}" fill="none" stroke="#111" stroke-width="1.1"/>'))
        if t:
            self.text(add(v, P(mid, tr or r + 0.17)), t, size=size or self.fs - 2)

    def tick(self, p, q, n=1):
        """線分 pq の中点に等長の印"""
        m = add(p, sub(q, p), 0.5)
        d = unit(sub(q, p))
        nrm = (-d[1], d[0])
        for i in range(n):
            c = add(m, d, (i - (n - 1) / 2) * 0.05)
            self.seg(add(c, nrm, 0.06), add(c, nrm, -0.06), w=1.2)

    def svg(self, width_mm, pad=6):
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
        body = "\n".join(s for _, s in sorted(self.items, key=lambda z: z[0]))
        return (f'<svg width="{width_mm}mm" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" {FONT}>'
                f'\n{body}\n</svg>')


O = (0.0, 0.0)
PLAB = -20


def on(deg):
    return P(deg)


# ------------------------------------------------------------------ 導入 1
def f_intro1():
    f = Fig(scale=62)
    A, B, Pp = on(220), on(320), on(100)
    f.circle(O, 1)
    f.poly(A, Pp, B, close=False); f.seg(O, A); f.seg(O, B)
    f.dot(O)
    for p, t in ((A, "A"), (B, "B"), (Pp, "P")):
        f.lab(p, t, O)
    f.text(O, "O", at=90, off=0.15)
    f.ang(O, A, B, "100°", r=0.18, tr=0.36)
    f.ang(Pp, A, B, "ア", r=0.25, tr=0.42)
    return f


# ------------------------------------------------------------------ 導入 2 (6問)
def f_d1():   # 中心角110 -> 円周角
    f = Fig(); A, B, Pp = on(215), on(325), on(95)
    f.circle(O, 1); f.poly(A, Pp, B, close=False); f.seg(O, A); f.seg(O, B); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (Pp, "P"))]
    f.text(O, "O", at=90, off=0.14)
    f.ang(O, A, B, "110°", r=0.17, tr=0.36); f.ang(Pp, A, B, "x", r=0.25, tr=0.4)
    return f


def f_d2():   # 円周角35 -> 中心角
    f = Fig(); A, B, Pp = on(235), on(305), on(80)
    f.circle(O, 1); f.poly(A, Pp, B, close=False); f.seg(O, A); f.seg(O, B); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (Pp, "P"))]
    f.text(O, "O", at=100, off=0.14)
    f.ang(Pp, A, B, "35°", r=0.28, tr=0.45); f.ang(O, A, B, "x", r=0.16, tr=0.3)
    return f


def f_d3():   # 同じ弧
    f = Fig(); A, B, C, D = on(230), on(310), on(55), on(135)
    f.circle(O, 1); f.poly(A, C, B, close=False); f.poly(A, D, B, close=False)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.ang(C, A, B, "40°", r=0.25, tr=0.43); f.ang(D, A, B, "x", r=0.25, tr=0.4)
    return f


def f_d4():   # 直径
    f = Fig(); A, B, C = on(180), on(0), on(124)
    f.circle(O, 1); f.poly(A, B, C); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"))]
    f.text(O, "O", at=-90, off=0.14)
    f.ang(B, A, C, "28°", r=0.3, tr=0.5); f.ang(A, B, C, "x", r=0.25, tr=0.4)
    return f


def f_d5():   # P が劣弧上
    f = Fig(); A, B, Pp = on(200), on(330), on(265)
    f.circle(O, 1); f.poly(A, Pp, B, close=False); f.seg(O, A); f.seg(O, B); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (Pp, "P"))]
    f.text(O, "O", at=90, off=0.14)
    f.ang(O, A, B, "130°", r=0.17, tr=0.36); f.ang(Pp, A, B, "x", r=0.15, tr=0.28)
    return f


def f_d6():   # 二等辺三角形 OAB
    f = Fig(); A, B, Pp = on(220), on(320), on(90)
    f.circle(O, 1); f.poly(A, Pp, B, close=False); f.seg(O, A); f.seg(O, B); f.seg(A, B); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (Pp, "P"))]
    f.text(O, "O", at=90, off=0.14)
    f.ang(Pp, A, B, "50°", r=0.28, tr=0.46); f.ang(A, O, B, "x", r=0.28, tr=0.42)
    return f


# ------------------------------------------------------------------ 演習 (9問)
def f_e1():   # 交わる弦
    f = Fig(); A, B, C, D = on(135), on(235), on(305), on(45)
    E = inter(A, C, B, D)
    f.circle(O, 1); f.seg(A, C); f.seg(B, D); f.seg(A, B); f.seg(C, D)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.lab(E, "E", at=90, off=0.15)
    f.ang(A, B, C, "35°", r=0.3, tr=0.5); f.ang(C, A, D, "45°", r=0.3, tr=0.5)
    f.ang(E, A, B, "x", r=0.13, tr=0.26)
    return f


def f_e2():   # 直径 + 同じ弧
    f = Fig(); A, B, C, D = on(180), on(0), on(72), on(300)
    f.circle(O, 1); f.poly(A, B, C); f.seg(A, D); f.seg(D, C); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.text(O, "O", at=-100, off=0.14)
    f.ang(D, A, C, "54°", r=0.3, tr=0.48); f.ang(A, B, C, "x", r=0.3, tr=0.46)
    return f


def f_e3():   # ∠OBC
    f = Fig(); A, B, C = on(100), on(200), on(340)
    f.circle(O, 1); f.poly(A, B, C); f.seg(O, B); f.seg(O, C); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"))]
    f.text(O, "O", at=90, off=0.14)
    f.ang(B, O, C, "20°", r=0.36, tr=0.55); f.ang(A, B, C, "x", r=0.25, tr=0.42)
    return f


def f_e4():   # 外部の交点
    f = Fig(scale=52); A, B, D, C = on(155), on(60), on(205), on(300)
    Pp = inter(A, B, D, C)
    f.circle(O, 1); f.seg(Pp, B); f.seg(Pp, C); f.seg(B, D)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.lab(Pp, "P", at=180, off=0.13)
    f.ang(B, A, D, "25°", r=0.36, tr=0.58); f.ang(D, B, C, "60°", r=0.22, tr=0.42)
    f.ang(Pp, A, D, "x", r=0.45, tr=0.6)
    return f


def f_e5():   # 10等分
    f = Fig(); L = "ABCDEFGHIJ"
    pts = {L[k]: on(90 - 36 * k) for k in range(10)}
    f.circle(O, 1)
    for k, c in enumerate(L):
        f.dot(pts[c], r=2.2); f.lab(pts[c], c, O, off=0.15)
    f.seg(pts["A"], pts["D"]); f.seg(pts["C"], pts["H"])
    Pp = inter(pts["A"], pts["D"], pts["C"], pts["H"])
    f.lab(Pp, "P", at=160, off=0.17)
    f.ang(Pp, pts["C"], pts["D"], "x", r=0.14, tr=0.27)
    return f


def f_e6():   # 等しい弧
    f = Fig(); A, B, C, D = on(200), on(256), on(312), on(90)
    f.circle(O, 1); f.seg(D, A); f.seg(D, B); f.seg(D, C)
    f.seg(A, B, dashed=True, w=1.1); f.seg(B, C, dashed=True, w=1.1)
    f.tick(A, B); f.tick(B, C)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.ang(D, A, B, "28°", r=0.42, tr=0.62); f.ang(D, A, C, "x", r=0.24, tr=0.36)
    return f


def f_e7():   # ∠OAB, ∠OCB
    f = Fig(); A, B, C = on(140), on(270), on(30)
    f.circle(O, 1); f.seg(A, B); f.seg(C, B); f.seg(O, A); f.seg(O, B); f.seg(O, C); f.dot(O)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"))]
    f.text(O, "O", at=-140, off=0.15)
    f.ang(A, O, B, "25°", r=0.32, tr=0.52); f.ang(C, O, B, "30°", r=0.32, tr=0.52)
    f.ang(O, A, C, "x", r=0.15, tr=0.28)
    return f


def f_e8():   # 弧の比
    f = Fig(); A, B, C = on(90), on(0), on(240)
    f.circle(O, 1); f.poly(A, B, C)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"))]
    f.ang(B, A, C, "x", r=0.25, tr=0.4)
    return f


def f_e9():   # 円周角の定理の逆（円は描かない）
    f = Fig(); B, C, A, D = on(220), on(320), on(145), on(75)
    f.seg(A, B); f.seg(A, C); f.seg(D, B); f.seg(D, C); f.seg(B, C); f.seg(A, D)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.ang(A, B, C, "50°", r=0.42, tr=0.62); f.ang(D, B, C, "50°", r=0.3, tr=0.5)
    f.ang(B, A, D, "35°", r=0.28, tr=0.47); f.ang(C, A, D, "x", r=0.25, tr=0.4)
    return f


# ------------------------------------------------------------------ 応用
def f_a1():
    """弦 AC, BD が P で交わる。PA=4, PC=9, PB=PD=6, AB=5"""
    cphi = 27 / 48                     # cos∠APB
    sb = -cphi                         # u1・u2（PA=4u1, PB=-6u2 なので cos∠APB = -u1・u2）
    cb = math.sqrt(1 - sb * sb)
    v = 2.5 / cb                       # |OP|
    r = math.sqrt(36 + v * v)
    k = 1 / r                          # 半径 1 に正規化
    Pp = (v * k, 0)
    vh, u2 = (1, 0), (0, 1)
    u1 = (cb, sb)
    # 回転して見やすく
    rot = math.radians(115)

    def R(p):
        return (p[0] * math.cos(rot) - p[1] * math.sin(rot), p[0] * math.sin(rot) + p[1] * math.cos(rot))
    A = R(add(Pp, u1, 4 * k)); C = R(add(Pp, u1, -9 * k))
    B = R(add(Pp, u2, -6 * k)); D = R(add(Pp, u2, 6 * k)); Pp = R(Pp)
    assert abs(dist(A, B) / k - 5) < 1e-6 and abs(norm(A) - 1) < 1e-9 and abs(norm(B) - 1) < 1e-9
    f = Fig(scale=78)
    f.circle(O, 1); f.seg(A, C); f.seg(B, D); f.seg(A, B); f.seg(D, C)
    [f.lab(p, t, O) for p, t in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.lab(Pp, "P", at=PLAB, off=0.14)
    f.dot(Pp)
    return f


def f_a2():
    """外部の点 P。PA=4,PB=9 / PC=3,PD=12, |PO|=10, r=8"""
    d = 8.0; r = math.sqrt(d * d - 36)
    k = 1 / r
    Pp = (-d * k, 0)
    def pt(cos_t, sgn, t):
        s = math.sqrt(1 - cos_t**2)
        return add(Pp, (cos_t, sgn * s), t * k)
    A, B = pt(13 / (2 * d), 1, 4), pt(13 / (2 * d), 1, 9)
    C, D = pt(15 / (2 * d), -1, 3), pt(15 / (2 * d), -1, 12)
    for q in (A, B, C, D):
        assert abs(norm(q) - 1) < 1e-9
    f = Fig(scale=70)
    f.circle(O, 1); f.seg(Pp, B); f.seg(Pp, D); f.seg(A, D); f.seg(C, B)
    f.lab(Pp, "P", at=180, off=0.14); f.dot(Pp)
    for p, t, a in ((A, "A", 110), (B, "B", 60), (C, "C", -110), (D, "D", -40)):
        f.lab(p, t, at=a, off=0.15)
    return f


def f_a3():
    """直径 AD, AB=10, AC=9, AD=12。AH⊥BC"""
    Rr = 6.0
    A = on(90)
    dB = 2 * math.degrees(math.asin(10 / 12)); dC = 2 * math.degrees(math.asin(9 / 12))
    B, C, D = on(90 + dB), on(90 - dC), on(270)
    # H: A から BC への垂線の足
    bc = unit(sub(C, B)); t = (A[0] - B[0]) * bc[0] + (A[1] - B[1]) * bc[1]
    H = add(B, bc, t)
    assert abs(dist(A, H) * Rr - 7.5) < 1e-6
    f = Fig(scale=74)
    f.circle(O, 1); f.poly(A, B, C); f.seg(A, D); f.seg(A, H); f.seg(D, C); f.dot(O)
    [f.lab(p, t_, O) for p, t_ in ((A, "A"), (B, "B"), (C, "C"), (D, "D"))]
    f.text(O, "O", at=150, off=0.11)
    f.lab(H, "H", at=-60, off=0.12)
    f.ang(H, A, C, right=True, r=0.13)
    return f


def f_a4():
    """AB=6, AC=8, ∠A の二等分線が BC と D、円と E。AD=4, AE=12"""
    k2 = 8 / 3; kk = math.sqrt(k2)
    a = 7 * kk  # BC
    B = (0.0, 0.0); C = (a, 0.0)
    # A: AB=6, AC=8
    x = (36 - 64 + a * a) / (2 * a); y = math.sqrt(36 - x * x)
    A = (x, y)
    Oc = circumcenter(A, B, C); R = dist(Oc, A)
    D = add(B, unit(sub(C, B)), 3 * kk)
    assert abs(dist(A, D) - 4) < 1e-6
    u = unit(sub(D, A)); E = add(A, u, 12)
    assert abs(dist(E, Oc) - R) < 1e-6
    n = lambda p: ((p[0] - Oc[0]) / R, (p[1] - Oc[1]) / R)
    A_, B_, C_, D_, E_ = map(n, (A, B, C, D, E))
    f = Fig(scale=78)
    f.circle(O, 1); f.poly(A_, B_, C_); f.seg(A_, E_); f.seg(B_, E_)
    for p, t in ((A_, "A"), (B_, "B"), (C_, "C"), (E_, "E")):
        f.lab(p, t, O)
    f.lab(D_, "D", at=-20, off=0.11)
    f.ang(A_, B_, D_, r=0.2); f.ang(A_, D_, C_, r=0.2)
    return f, dist(B, E)


if __name__ == "__main__":
    print("BE =", f_a4()[1], "4√6 =", 4 * math.sqrt(6))
