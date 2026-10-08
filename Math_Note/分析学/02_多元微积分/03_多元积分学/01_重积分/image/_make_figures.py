# -*- coding: utf-8 -*-
"""
Unified figures for the note:
    "弧长、面积与体积元素在常用坐标系下的表示"

Convention (math style):
    polar       (r, theta),      theta from +x axis, CCW
    cylindrical (r, theta, z),  theta from +x axis, CCW
    spherical   (r, theta, phi), phi from +z axis, theta = azimuth from +x

The radial coordinate is always written r; the azimuth is always written
theta; phi appears only in spherical, where it is the polar angle from +z.

The 3-D panels use a fixed oblique parallel projection (pure 2-D drawing),
so layering is fully controlled and no mplot3d quirks apply.

Outputs (written next to this script):
    fig-1-rect.png    rectangular (x, y, z)
    fig-2-polar.png   polar (r, theta)
    fig-3-cyl.png     cylindrical (r, theta, z)
    fig-4-sph.png     spherical (r, theta, phi)
    fig-overview.png  the four panels stitched horizontally

    fig-5-line.png    geometry of ds   (Cartesian / polar / spherical)
    fig-6-area.png    geometry of dS   (polar sector, sphere patch, cylinder patch)
    fig-7-volume.png  geometry of dV   (box, cylinder wedge, spherical shell block)

The three element figures share the colour convention of the coordinate figures:
blue = first coordinate, red = second (azimuth), green = third.  Every coloured
edge carries its own label, so the panels survive greyscale printing.

`python _make_figures.py` also prints an exact-vs-leading-order check of the
three closed-form element volumes quoted in section 4.3 of the note.
"""
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "mathtext.fontset": "cm",
})

# ---------------------------------------------------------------- projection
# oblique parallel projection: screen = ORIG + x*EX + y*EY + z*EZ
EX = np.array([-0.40, -0.30])   # x axis points lower-left
EY = np.array([0.95, -0.22])    # y axis points lower-right
EZ = np.array([0.00, 1.00])     # z axis points straight up
ORIG = np.array([0.36, 0.30])


def proj(x, y, z):
    """(x, y, z) arrays/scalars -> Nx2 screen coordinates."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    y = np.atleast_1d(np.asarray(y, dtype=float))
    z = np.atleast_1d(np.asarray(z, dtype=float))
    return ORIG + x[:, None] * EX + y[:, None] * EY + z[:, None] * EZ


def seg(ax, a, b, **kw):
    p = proj([a[0], b[0]], [a[1], b[1]], [a[2], b[2]])
    ax.plot(p[:, 0], p[:, 1], **kw)


def curve(ax, pts, **kw):
    p = proj([q[0] for q in pts], [q[1] for q in pts], [q[2] for q in pts])
    ax.plot(p[:, 0], p[:, 1], **kw)


def dot(ax, p, color="#D62728", ms=5.5, zorder=7):
    q = proj(*p)[0]
    ax.plot([q[0]], [q[1]], marker="o", ms=ms, mfc=color, mec=color, zorder=zorder)
    return q


def tag(ax, p, text, dx=0.02, dy=0.02, ha="left", va="center", fs=13, **kw):
    q = proj(*p)[0]
    ax.text(q[0] + dx, q[1] + dy, text, fontsize=fs, ha=ha, va=va, zorder=8, **kw)


def outward(p, base=(0.0, 0.0, 0.0), k=0.09):
    """shift p radially away from base, used to park labels outside arcs."""
    p = np.asarray(p, dtype=float)
    d = p - np.asarray(base, dtype=float)
    n = np.linalg.norm(d)
    return p + (k * d / n if n > 0 else 0.0)


def xy(p):
    return proj(*p)[0]


def perp(a, b):
    """unit screen-space normal of the segment a->b."""
    d = xy(b) - xy(a)
    d = d / np.hypot(d[0], d[1])
    return np.array([d[1], -d[0]])


def label_s(ax, p, text, off=(0.0, 0.0), fs=15, color="black"):
    """label at the screen position of p, nudged by a screen-space offset."""
    q = xy(p)
    ax.text(q[0] + off[0], q[1] + off[1], text, fontsize=fs, ha="center",
            va="center", color=color, zorder=8)


# ------------------------------------------------------------------ 3-D frame
GRAY = dict(color="0.87", lw=0.55, zorder=1)
AXIS = dict(color="black", lw=1.5, zorder=3, solid_capstyle="round")
DASH = dict(color="black", lw=1.0, ls=(0, (4.5, 3)), zorder=4)
BLUE = dict(color="#1F3FBF", lw=1.7, zorder=5, solid_capstyle="round")
RED = dict(color="#B22222", lw=1.4, zorder=5)


def frame3(ax, L=1.0, n=8):
    """light grid on the three coordinate planes + black axes + axis labels."""
    t = np.linspace(0.0, L, n + 1)
    for s in t:
        seg(ax, (s, 0, 0), (s, L, 0), **GRAY)     # z = 0 plane
        seg(ax, (0, s, 0), (L, s, 0), **GRAY)
        seg(ax, (s, 0, 0), (s, 0, L), **GRAY)     # y = 0 plane
        seg(ax, (0, 0, s), (L, 0, s), **GRAY)
        seg(ax, (0, s, 0), (0, s, L), **GRAY)     # x = 0 plane
        seg(ax, (0, 0, s), (0, L, s), **GRAY)

    A = 1.04
    seg(ax, (0, 0, 0), (A, 0, 0), **AXIS)
    seg(ax, (0, 0, 0), (0, A, 0), **AXIS)
    seg(ax, (0, 0, 0), (0, 0, A), **AXIS)
    for v, nm, dx, dy in (((A, 0, 0), "x", -0.030, -0.035),
                          ((0, A, 0), "y", 0.035, -0.020),
                          ((0, 0, A), "z", 0.020, 0.030)):
        tag(ax, v, rf"${nm}$", dx=dx, dy=dy, ha="center", fs=15)


def new_fig(w=4.0, h=3.5):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.set_axis_off()
    return fig, ax


def fit(ax, pad=0.05):
    x0, x1 = ax.dataLim.x0, ax.dataLim.x1
    y0, y1 = ax.dataLim.y0, ax.dataLim.y1
    ax.set_xlim(x0 - pad, x1 + pad)
    ax.set_ylim(y0 - pad, y1 + pad)


def save(fig, path):
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white",
                pad_inches=0.06)
    plt.close(fig)


# -------------------------------------------------------------- 1 rectangular
def fig_rect(path):
    fig, ax = new_fig()
    frame3(ax)
    x, y, z = 0.70, 0.64, 0.68
    seg(ax, (x, y, z), (x, y, 0), **DASH)
    seg(ax, (x, y, 0), (x, 0, 0), **DASH)
    seg(ax, (x, y, 0), (0, y, 0), **DASH)
    seg(ax, (x, y, z), (0, 0, z), **DASH)
    dot(ax, (x, y, z))
    tag(ax, (x, y, z), r"$(x,\,y,\,z)$", dx=0.025, dy=0.020, va="bottom")
    fit(ax)
    save(fig, path)


# ------------------------------------------------------------------- 2 polar
def fig_polar(path):
    fig, ax = plt.subplots(figsize=(4.0, 3.5))
    ax.set_aspect("equal")
    ax.set_axis_off()

    x0, y0 = 0.70, 0.52
    xa, ya = 1.18, 1.02

    ax.annotate("", xy=(xa, 0), xytext=(-0.05, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5))
    ax.annotate("", xy=(0, ya), xytext=(0, -0.05),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5))
    ax.text(xa, -0.03, r"$x$", fontsize=15, ha="left", va="top")
    ax.text(-0.02, ya, r"$y$", fontsize=15, ha="right", va="top")

    # radius vector
    ax.plot([0, x0], [0, y0], color="#1F3FBF", lw=1.8,
            solid_capstyle="round", zorder=5)
    # legs
    ax.plot([x0, x0], [0, y0], **RED)
    ax.plot([0, x0], [0, 0], **RED)
    # right angle marker
    s = 0.055
    ax.plot([x0 - s, x0 - s, x0], [0, s, s], color="#B22222", lw=1.0, zorder=5)
    # angle arc
    t = np.linspace(0, np.arctan2(y0, x0), 60)
    R = 0.26
    ax.plot(R * np.cos(t), R * np.sin(t), color="#B22222", lw=1.4, zorder=5)

    ax.plot([x0], [y0], marker="o", ms=5.5, color="#D62728", zorder=7)
    ax.text(x0 * 0.55 - 0.05, y0 * 0.55 + 0.03, r"$r$", fontsize=15,
            color="#1F3FBF", ha="right", va="bottom")
    ax.text(R * np.cos(0.5 * np.arctan2(y0, x0)) + 0.02,
            R * np.sin(0.5 * np.arctan2(y0, x0)) - 0.02, r"$\theta$",
            fontsize=15, color="#B22222", ha="left", va="top")
    ax.text(x0 * 0.5, -0.045, r"$r\cos\theta$", fontsize=13,
            color="#B22222", ha="center", va="top")
    ax.text(x0 + 0.025, y0 * 0.5, r"$r\sin\theta$", fontsize=13,
            color="#B22222", ha="left", va="center", rotation=90)
    ax.text(x0 + 0.02, y0 + 0.03, r"$(x,\,y)$", fontsize=13, ha="left",
            va="bottom")

    ax.set_xlim(-0.10, xa + 0.06)
    ax.set_ylim(-0.10, ya + 0.06)
    save(fig, path)


# ------------------------------------------------------------- 3 cylindrical
def fig_cyl(path):
    fig, ax = new_fig()
    frame3(ax)
    r, z = 0.84, 0.72
    th = np.deg2rad(38)          # azimuth, from +x
    x, y = r * np.cos(th), r * np.sin(th)

    seg(ax, (x, y, z), (x, y, 0), **DASH)
    seg(ax, (x, y, 0), (x, 0, 0), **DASH)
    seg(ax, (x, y, 0), (0, y, 0), **DASH)
    seg(ax, (x, y, z), (0, 0, z), **DASH)
    # radius in the xy-plane
    seg(ax, (0, 0, 0), (x, y, 0), **BLUE)
    # azimuth arc
    R = 0.34
    t = np.linspace(0, th, 60)
    curve(ax, [(R * np.cos(s), R * np.sin(s), 0) for s in t], **RED)

    dot(ax, (x, y, z))
    tag(ax, (x, y, z), r"$(r,\,\theta,\,z)$", dx=0.025, dy=0.018, va="bottom")
    n = perp((0, 0, 0), (x, y, 0))
    label_s(ax, (0.5 * x, 0.5 * y, 0.0), r"$r$", off=0.085 * n,
            color="#1F3FBF")
    label_s(ax, (R * np.cos(th / 2), R * np.sin(th / 2), 0.0),
            r"$\theta$", off=(-0.010, 0.055), color="#B22222")
    fit(ax)
    save(fig, path)


# -------------------------------------------------------------- 4 spherical
def fig_sph(path):
    fig, ax = new_fig()
    frame3(ax)
    r = 1.00
    th = np.deg2rad(52)          # azimuth, from +x
    ph = np.deg2rad(40)          # polar,    from +z
    x = r * np.sin(ph) * np.cos(th)
    y = r * np.sin(ph) * np.sin(th)
    z = r * np.cos(ph)

    seg(ax, (x, y, z), (0, 0, z), **DASH)
    seg(ax, (x, y, z), (x, y, 0), **DASH)
    seg(ax, (0, 0, 0), (x, y, 0), **DASH)
    seg(ax, (0, 0, 0), (0, 0, z), **DASH)
    # radius vector
    seg(ax, (0, 0, 0), (x, y, z), **BLUE)
    # azimuth arc theta in the xy-plane
    R1 = 0.30
    t = np.linspace(0, th, 60)
    curve(ax, [(R1 * np.cos(s), R1 * np.sin(s), 0) for s in t], **RED)
    # polar arc phi between +z and OP (inside the plane spanned by z and OP)
    R2 = 0.42
    ux, uy = np.cos(th), np.sin(th)
    t = np.linspace(0, ph, 60)
    curve(ax, [(R2 * np.sin(s) * ux, R2 * np.sin(s) * uy, R2 * np.cos(s))
               for s in t], **RED)

    dot(ax, (x, y, z))
    tag(ax, (x, y, z), r"$(r,\,\theta,\,\varphi)$", dx=0.025, dy=0.018, va="bottom")
    n = perp((0, 0, 0), (x, y, z))
    label_s(ax, (0.5 * x, 0.5 * y, 0.5 * z), r"$r$", off=0.085 * n,
            color="#1F3FBF")
    label_s(ax, outward((R1 * np.cos(th / 2), R1 * np.sin(th / 2), 0), k=0.085),
            r"$\theta$", color="#B22222")
    mid = 0.5 * ph
    label_s(ax, (R2 * np.sin(mid) * ux, R2 * np.sin(mid) * uy,
                 R2 * np.cos(mid)), r"$\varphi$", off=(0.058, 0.032),
            color="#B22222")
    fit(ax)
    save(fig, path)


# ============================================================= element figures
# Geometry of the infinitesimal elements.  Colour encodes the COORDINATE
# DIRECTION and carries over to every panel of fig-5/6/7:
#     blue  = 1st coordinate (x, r, r)
#     red   = 2nd coordinate (y, theta, theta)   [the azimuth]
#     green = 3rd coordinate (z, z, phi)         [phi = polar angle from +z]
C1C, C2C, C3C = "#1F3FBF", "#B22222", "#009E73"
FACE = dict(facecolor="0.90", edgecolor="none", zorder=2)
WIRE = dict(color="0.35", lw=0.9, zorder=4)
SOFT = dict(color="0.80", lw=0.6, zorder=1)
LEG = dict(lw=1.9, zorder=6, solid_capstyle="round")


def cross3(ax, L=1.05):
    """The three coordinate axes only (no grid): a local frame for one element."""
    for v, nm, dx, dy in (((L, 0, 0), "x", -0.030, -0.035),
                          ((0, L, 0), "y", 0.035, -0.020),
                          ((0, 0, L), "z", 0.020, 0.030)):
        seg(ax, (0, 0, 0), v, **AXIS)
        tag(ax, v, rf"${nm}$", dx=dx, dy=dy, ha="center", fs=14)


def new_row(n=3, w=3.9, h=3.5):
    fig, axs = plt.subplots(1, n, figsize=(w * n, h))
    for ax in np.atleast_1d(axs):
        ax.set_aspect("equal")
        ax.set_axis_off()
    return fig, np.atleast_1d(axs)


def letter(ax, s):
    ax.text(0.02, 0.98, s, transform=ax.transAxes, fontsize=17,
            fontweight="bold", ha="left", va="top", zorder=12)


def poly3(ax, pts, **kw):
    p = proj([q[0] for q in pts], [q[1] for q in pts], [q[2] for q in pts])
    ax.add_patch(Polygon(p, closed=True, **kw))


# ---- the three maps, same convention as the panels of fig-overview ---------
def F_cart(x, y, z):
    return (x, y, z)


def F_cyl(r, th, z):
    return (r * np.cos(th), r * np.sin(th), z)


def F_sph(r, th, ph):
    return (r * np.sin(ph) * np.cos(th), r * np.sin(ph) * np.sin(th),
            r * np.cos(ph))


def _grid(u0, u1, v0, v1, n):
    return np.meshgrid(np.linspace(u0, u1, n), np.linspace(v0, v1, n),
                       indexing="ij")


def _quads(P):
    a, b, c, d = P[:-1, :-1], P[1:, :-1], P[1:, 1:], P[:-1, 1:]
    return [np.array([a[i, j], b[i, j], c[i, j], d[i, j]])
            for i in range(a.shape[0]) for j in range(a.shape[1])]


def block_faces(F, rng, n=12):
    """Six (generally curved) boundary faces of one coordinate block."""
    (a0, a1), (b0, b1), (c0, c1) = rng
    out = []
    for a in (a0, a1):
        B, C = _grid(b0, b1, c0, c1, n)
        out += _quads(np.stack(F(np.full_like(B, a), B, C), -1))
    for b in (b0, b1):
        A, C = _grid(a0, a1, c0, c1, n)
        out += _quads(np.stack(F(A, np.full_like(A, b), C), -1))
    for c in (c0, c1):
        A, B = _grid(a0, a1, b0, b1, n)
        out += _quads(np.stack(F(A, B, np.full_like(A, c)), -1))
    return out


def block_curves(F, rng, n=40):
    """The twelve boundary curves of one coordinate block."""
    (a0, a1), (b0, b1), (c0, c1) = rng
    out = []
    for c in (c0, c1):
        for b in (b0, b1):
            A = np.linspace(a0, a1, n)
            out.append(np.stack(F(A, np.full_like(A, b), np.full_like(A, c)), -1))
        for a in (a0, a1):
            B = np.linspace(b0, b1, n)
            out.append(np.stack(F(np.full_like(B, a), B, np.full_like(B, c)), -1))
    for a in (a0, a1):
        for b in (b0, b1):
            C = np.linspace(c0, c1, n)
            out.append(np.stack(F(np.full_like(C, a), np.full_like(C, b), C), -1))
    return out


def _pt(F, *coords):
    return np.asarray(F(*[np.array([c], float) for c in coords]), float).ravel()


def leg_of(F, base, var):
    """A callable t -> points, following coordinate `var` of F from `base`."""
    def cur(t):
        args = list(base)
        args[var] = t
        args = [np.full(np.shape(t), a, float) if np.ndim(a) == 0
                else np.asarray(a, float) for a in args]
        return np.stack(F(*args), -1)
    return cur


LABELBOX = dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.4)


def draw_leg(ax, cur, span, colour, text, centre, frac=0.5, off=0.095, fs=14):
    """One elementary displacement: coloured curve + a label pushed outward."""
    t = np.linspace(span[0], span[1], 40)
    pts = np.asarray(cur(t), float).reshape(len(t), 3)
    curve(ax, list(pts), color=colour, **LEG)
    a0, am = xy(pts[0]), xy(pts[int(round(frac * (len(t) - 1)))])
    d = am - a0
    L = np.hypot(d[0], d[1])
    d = d / L if L > 0 else np.array([1.0, 0.0])
    n = np.array([-d[1], d[0]])
    if np.dot(n, am - np.asarray(centre)) < 0:
        n = -n
    ax.text(am[0] + off * n[0], am[1] + off * n[1], text, fontsize=fs,
            color=colour, ha="center", va="center", zorder=9,
            bbox=LABELBOX)


def draw_block(ax, F, rng, base, legs, n=12):
    """Faces + wireframe of one coordinate block, then its coloured edges."""
    (a0, a1), (b0, b1), (c0, c1) = rng
    corners = np.array([_pt(F, a, b, c) for a in (a0, a1) for b in (b0, b1)
                        for c in (c0, c1)]).T
    centre = xy(corners.mean(axis=1))
    for q in block_faces(F, rng, n):
        poly3(ax, q, **FACE)
    for e in block_curves(F, rng):
        curve(ax, list(e), **WIRE)
    for var, span, colour, text, frac in legs:
        draw_leg(ax, leg_of(F, base, var), span, colour, text, centre, frac=frac)


def draw_patch(ax, G, rng, legs, n=16):
    """Faces + boundary of a coordinate patch on a surface, then two edges."""
    (a0, a1), (b0, b1) = rng
    A, B = _grid(a0, a1, b0, b1, n)
    corners = np.array([_pt(G, a, b) for a in (a0, a1) for b in (b0, b1)]).T
    centre = xy(corners.mean(axis=1))
    for q in _quads(np.stack(G(A, B), -1)):
        poly3(ax, q, facecolor="0.88", edgecolor="none", zorder=3)
    for fixed, var in ((b0, 0), (b1, 0), (a0, 1), (a1, 1)):
        t = np.linspace(rng[var][0], rng[var][1], 40)
        f = (lambda s: G(s, np.full_like(s, fixed))) if var == 0 else \
            (lambda s: G(np.full_like(s, fixed), s))
        # G returns (x, y, z) as three parallel arrays: stack, never reshape,
        # or the three components get interleaved into meaningless points.
        pts = np.stack(f(t), -1)
        curve(ax, list(pts), color="0.30", lw=0.9, zorder=4)
    for var, span, colour, text, frac in legs:
        draw_leg(ax, leg_of(G, (a0, b0), var), span, colour, text, centre,
                 frac=frac)


def soft_curve(ax, F, base, var, span, n=90, **kw):
    """A faint coordinate curve through (or near) the element, for context."""
    pts = np.asarray(leg_of(F, base, var)(np.linspace(span[0], span[1], n)),
                     float).reshape(n, 3)
    curve(ax, list(pts), **dict(SOFT, **kw))


def label_line(ax, p0, p1, text, frac=0.8, off=(0.07, 0.05), fs=15, colour="black"):
    """Label at a fraction along a 3-D segment, nudged in screen space."""
    p = np.asarray(p0, float) + frac * (np.asarray(p1, float) - np.asarray(p0, float))
    q = xy(p)
    ax.text(q[0] + off[0], q[1] + off[1], text, fontsize=fs, color=colour,
            ha="center", va="center", zorder=9, bbox=LABELBOX)


# --------------------------------------------------------- 5 arc-length ds
def fig_elem_line(path):
    fig, axs = new_row(3)

    # A: rectangular -- ds is the space diagonal of the dx dy dz box
    ax = axs[0]
    cross3(ax)
    base = (0.24, 0.20, 0.22)
    d = (0.50, 0.46, 0.50)
    rng = tuple((base[k], base[k] + d[k]) for k in range(3))
    draw_block(ax, F_cart, rng, base,
               [(0, rng[0], C1C, r"$\mathrm{d}x$", 0.50),
                (1, rng[1], C2C, r"$\mathrm{d}y$", 0.34),
                (2, rng[2], C3C, r"$\mathrm{d}z$", 0.50)])
    p0 = np.array(base, float)
    p1 = p0 + np.array(d, float)
    seg(ax, p0, p1, color="black", lw=1.9, zorder=7)
    label_line(ax, p0, p1, r"$\mathrm{d}s$", frac=0.84, off=(0.085, 0.055))
    letter(ax, "A")
    fit(ax)

    # B: polar -- the tangent right triangle with legs dr and r dtheta
    ax = axs[1]
    r0, th0 = 1.00, np.deg2rad(16)
    dr, dth = 0.50, np.deg2rad(26)
    er = np.array([np.cos(th0), np.sin(th0)])
    et = np.array([-np.sin(th0), np.cos(th0)])
    P, A = r0 * er, (r0 + dr) * er
    B = A + r0 * dth * et
    t = np.linspace(-0.13, th0 + dth + 0.15, 140)
    for rad in (r0, r0 + dr):
        ax.plot(rad * np.cos(t), rad * np.sin(t), **SOFT)
    for th in (th0, th0 + dth):
        ax.plot([0.60 * np.cos(th), 1.60 * np.cos(th)],
                [0.60 * np.sin(th), 1.60 * np.sin(th)], **SOFT)
    ax.add_patch(Polygon([P, A, B], closed=True, facecolor="0.93",
                         edgecolor="none", zorder=2))
    ax.annotate("", xy=A, xytext=P,
                arrowprops=dict(arrowstyle="-|>", color=C1C, lw=1.9))
    ax.annotate("", xy=B, xytext=A,
                arrowprops=dict(arrowstyle="-|>", color=C2C, lw=1.9))
    ax.plot([P[0], B[0]], [P[1], B[1]], color="black", lw=1.9, zorder=6)
    s = 0.062
    ax.plot([A[0] - s * er[0], A[0] - s * er[0] + s * et[0], A[0] + s * et[0]],
            [A[1] - s * er[1], A[1] - s * er[1] + s * et[1], A[1] + s * et[1]],
            color=C2C, lw=1.0, zorder=6)
    ax.plot([P[0]], [P[1]], marker="o", ms=5.0, color="#D62728", zorder=7)
    ax.text(*((P + A) / 2 - 0.115 * et), r"$\mathrm{d}r$", color=C1C,
            fontsize=14, ha="center", va="center")
    ax.text(*((A + B) / 2 + 0.140 * er), r"$r\,\mathrm{d}\theta$", color=C2C,
            fontsize=14, ha="center", va="center")
    ax.text(*((P + B) / 2 + 0.20 * (et - er) / np.sqrt(2)), r"$\mathrm{d}s$",
            color="black", fontsize=15, ha="center", va="center")
    ax.set_xlim(0.52, 1.72)
    ax.set_ylim(0.05, 1.30)
    letter(ax, "B")

    # C: spherical -- three mutually orthogonal elementary displacements
    ax = axs[2]
    r0, th0, ph0 = 1.00, np.deg2rad(52), np.deg2rad(38)
    dr, dth, dph = 0.30, np.deg2rad(22), np.deg2rad(22)
    base = (r0, th0, ph0)
    soft_curve(ax, F_sph, base, 1, (th0 - 0.7 * dth, th0 + 1.6 * dth))
    soft_curve(ax, F_sph, base, 2, (ph0 - 0.7 * dph, ph0 + 1.6 * dph))
    seg(ax, tuple(_pt(F_sph, r0 - 0.34, th0, ph0)),
        tuple(_pt(F_sph, r0 + dr + 0.22, th0, ph0)), **DASH)
    rng = ((r0, r0 + dr), (th0, th0 + dth), (ph0, ph0 + dph))
    draw_block(ax, F_sph, rng, base,
               [(0, rng[0], C1C, r"$\mathrm{d}r$", 0.85),
                (1, rng[1], C2C, r"$r\sin\varphi\,\mathrm{d}\theta$", 0.92),
                (2, rng[2], C3C, r"$r\,\mathrm{d}\varphi$", 0.70)])
    q0 = _pt(F_sph, r0, th0, ph0)
    q1 = _pt(F_sph, r0 + dr, th0 + dth, ph0 + dph)
    seg(ax, q0, q1, color="black", lw=1.8, zorder=7)
    label_line(ax, q0, q1, r"$\mathrm{d}s$", frac=0.86, off=(0.075, 0.055))
    letter(ax, "C")
    fit(ax)

    save(fig, path)


# ------------------------------------------------------------- 6 area dA/dS
def fig_elem_area(path):
    fig, axs = new_row(3)

    # A: polar -- exact annular sector vs the tangent rectangle
    ax = axs[0]
    r0, th0 = 0.95, np.deg2rad(14)
    dr, dth = 0.50, np.deg2rad(26)
    er = np.array([np.cos(th0), np.sin(th0)])
    et = np.array([-np.sin(th0), np.cos(th0)])
    t = np.linspace(th0, th0 + dth, 80)
    cell = np.vstack([np.stack([r0 * np.cos(t[::-1]), r0 * np.sin(t[::-1])], 1),
                      np.stack([(r0 + dr) * np.cos(t),
                                (r0 + dr) * np.sin(t)], 1)])
    ax.add_patch(Polygon(cell, closed=True, facecolor="0.88",
                         edgecolor="0.30", lw=1.1, zorder=3))
    P = r0 * er
    A = (r0 + dr) * er
    B = A + r0 * dth * et
    C = P + r0 * dth * et
    ax.add_patch(Polygon([P, A, B, C], closed=True, fill=False,
                         ls=(0, (5, 3)), edgecolor="black", lw=1.3, zorder=5))
    ax.annotate("", xy=A, xytext=P,
                arrowprops=dict(arrowstyle="-|>", color=C1C, lw=1.9))
    ax.annotate("", xy=C, xytext=P,
                arrowprops=dict(arrowstyle="-|>", color=C2C, lw=1.9))
    s = 0.065
    ax.plot([P[0] + s * er[0], P[0] + s * (er[0] + et[0]), P[0] + s * et[0]],
            [P[1] + s * er[1], P[1] + s * (er[1] + et[1]), P[1] + s * et[1]],
            color=C1C, lw=1.0, zorder=6)
    ax.plot([P[0]], [P[1]], marker="o", ms=5.0, color="#D62728", zorder=7)
    ax.text(*((P + A) / 2 - 0.115 * et), r"$\mathrm{d}r$", color=C1C,
            fontsize=14, ha="center", va="center")
    ax.text(*((P + C) / 2 + 0.135 * er), r"$r\,\mathrm{d}\theta$", color=C2C,
            fontsize=14, ha="center", va="center")
    mid = 0.25 * (P + A + B + C)
    ax.annotate(r"$\mathrm{d}r\cdot r\,\mathrm{d}\theta$", xy=mid,
                xytext=(mid[0] + 0.55, mid[1] + 0.16), fontsize=13,
                color="black", ha="center", va="center", zorder=9,
                bbox=LABELBOX,
                arrowprops=dict(arrowstyle="-", color="0.55", lw=0.8,
                                shrinkA=2, shrinkB=2))
    t = np.linspace(th0 - 0.13, th0 + dth + 0.15, 140)
    for rad in (r0, r0 + dr):
        ax.plot(rad * np.cos(t), rad * np.sin(t), **SOFT)
    ax.set_xlim(0.60, 1.92)
    ax.set_ylim(0.06, 1.16)
    letter(ax, "A")

    # B: sphere patch R dphi x R sin(phi) dtheta
    ax = axs[1]
    R = 1.0
    p0, dp = np.deg2rad(46), np.deg2rad(24)
    t0, dt_ = np.deg2rad(12), np.deg2rad(30)
    G = lambda a, b: F_sph(R, b, a)          # a = phi, b = theta
    soft_curve(ax, G, (p0, t0), 1, (t0 - 0.45 * dt_, t0 + 1.45 * dt_))
    soft_curve(ax, G, (p0 + dp, t0), 1, (t0 - 0.45 * dt_, t0 + 1.45 * dt_))
    soft_curve(ax, G, (p0, t0), 0, (p0 - 0.30 * dp, p0 + 1.30 * dp))
    soft_curve(ax, G, (p0, t0 + dt_), 0, (p0 - 0.30 * dp, p0 + 1.30 * dp))
    seg(ax, (0, 0, 0), tuple(R * np.array(_pt(F_sph, R, t0, p0))), **DASH)
    draw_patch(ax, G, ((p0, p0 + dp), (t0, t0 + dt_)),
               [(0, (p0, p0 + dp), C3C, r"$R\,\mathrm{d}\varphi$", 0.50),
                (1, (t0, t0 + dt_), C2C,
                 r"$R\sin\varphi\,\mathrm{d}\theta$", 0.50)])
    letter(ax, "B")
    fit(ax)

    # C: cylinder patch R dtheta x dz
    ax = axs[2]
    R2 = 0.62
    t0, dt_ = np.deg2rad(8), np.deg2rad(66)
    z0, dz = -0.30, 0.75
    G2 = lambda a, b: F_cyl(R2, a, b)        # a = theta, b = z
    soft_curve(ax, G2, (t0, z0), 0, (t0 - 0.28 * dt_, t0 + 1.28 * dt_))
    soft_curve(ax, G2, (t0, z0 + dz), 0, (t0 - 0.28 * dt_, t0 + 1.28 * dt_))
    soft_curve(ax, G2, (t0, z0), 1, (z0 - 0.22 * dz, z0 + 1.22 * dz))
    soft_curve(ax, G2, (t0 + dt_, z0), 1, (z0 - 0.22 * dz, z0 + 1.22 * dz))
    seg(ax, (0, 0, z0 - 0.35), (0, 0, z0 + dz + 0.35), **DASH)
    seg(ax, (0, 0, z0), (R2 * np.cos(t0), R2 * np.sin(t0), z0), **DASH)
    draw_patch(ax, G2, ((t0, t0 + dt_), (z0, z0 + dz)),
               [(0, (t0, t0 + dt_), C2C, r"$R\,\mathrm{d}\theta$", 0.50),
                (1, (z0, z0 + dz), C3C, r"$\mathrm{d}z$", 0.50)])
    letter(ax, "C")
    fit(ax)

    save(fig, path)


# ----------------------------------------------------------- 7 volume dV
def fig_elem_volume(path):
    fig, axs = new_row(3)

    # A: rectangular box
    ax = axs[0]
    cross3(ax)
    base = (0.24, 0.20, 0.22)
    d = (0.50, 0.46, 0.50)
    rng = tuple((base[k], base[k] + d[k]) for k in range(3))
    draw_block(ax, F_cart, rng, base,
               [(0, rng[0], C1C, r"$\mathrm{d}x$", 0.50),
                (1, rng[1], C2C, r"$\mathrm{d}y$", 0.34),
                (2, rng[2], C3C, r"$\mathrm{d}z$", 0.50)])
    letter(ax, "A")
    fit(ax)

    # B: cylindrical wedge (an annular sector swept along z)
    ax = axs[1]
    r0, th0 = 0.72, np.deg2rad(12)
    dr, dth = 0.20, np.deg2rad(34)
    z0, dz = 0.12, 0.55
    base = (r0, th0, z0)
    soft_curve(ax, F_cyl, base, 1, (th0 - dth, th0 + 2.0 * dth))
    soft_curve(ax, F_cyl, base, 2, (z0 - 0.35 * dz, z0 + 1.35 * dz))
    seg(ax, (0, 0, z0 - 0.45 * dz), (0, 0, z0 + 1.45 * dz), **DASH)
    seg(ax, (0, 0, z0), (r0 * np.cos(th0), r0 * np.sin(th0), z0), **DASH)
    rng = ((r0, r0 + dr), (th0, th0 + dth), (z0, z0 + dz))
    draw_block(ax, F_cyl, rng, base,
               [(0, rng[0], C1C, r"$\mathrm{d}r$", 0.50),
                (1, rng[1], C2C, r"$r\,\mathrm{d}\theta$", 0.50),
                (2, rng[2], C3C, r"$\mathrm{d}z$", 0.50)])
    letter(ax, "B")
    fit(ax)

    # C: spherical shell block
    ax = axs[2]
    r0, th0, ph0 = 0.95, np.deg2rad(50), np.deg2rad(36)
    dr, dth, dph = 0.28, np.deg2rad(22), np.deg2rad(22)
    base = (r0, th0, ph0)
    soft_curve(ax, F_sph, base, 1, (th0 - 0.7 * dth, th0 + 1.6 * dth))
    soft_curve(ax, F_sph, base, 2, (ph0 - 0.7 * dph, ph0 + 1.6 * dph))
    seg(ax, tuple(_pt(F_sph, r0 - 0.32, th0, ph0)),
        tuple(_pt(F_sph, r0 + dr + 0.20, th0, ph0)), **DASH)
    rng = ((r0, r0 + dr), (th0, th0 + dth), (ph0, ph0 + dph))
    draw_block(ax, F_sph, rng, base,
               [(0, rng[0], C1C, r"$\mathrm{d}r$", 0.85),
                (1, rng[1], C2C, r"$r\sin\varphi\,\mathrm{d}\theta$", 0.92),
                (2, rng[2], C3C, r"$r\,\mathrm{d}\varphi$", 0.70)])
    letter(ax, "C")
    fit(ax)

    save(fig, path)


# ------------------------------------------------------- exact-volume check
def check_exact():
    """Element volumes: closed form vs leading order, and the O(h) error decay.

    All increments are scaled so that each elementary arc length equals h, i.e.
    dr = h, r dtheta = h, r sin(phi) dtheta = h, r dphi = h.
    """
    r, ph = 1.00, 0.80

    def wedge(h):
        dr, dth, dz = h, h / r, h
        return 0.5 * dth * ((r + dr) ** 2 - r ** 2) * dz, r * dr * dth * dz

    def shell(h):
        dr, dth, dph = h, h / (r * np.sin(ph)), h / r
        v = (dth / 3.0) * (np.cos(ph) - np.cos(ph + dph)) * \
            ((r + dr) ** 3 - r ** 3)
        return v, r ** 2 * np.sin(ph) * dr * dph * dth

    print("exact vs leading order  (increments scaled by h)")
    for name, fn in (("cylindrical wedge", wedge), ("spherical shell", shell)):
        step, errs = (0.02, 0.01, 0.005), []
        for h in step:
            v, lead = fn(h)
            errs.append(abs(v - lead) / v)
        print("  %-18s rel.error  %.3e  %.3e  %.3e   ratio %.2f  [O(h) -> 2]"
              % (name, errs[0], errs[1], errs[2], errs[0] / errs[1]))


# ------------------------------------------------------------------ stitching
def stitch(paths, out, height=1000, gap=30, bg="white"):
    ims = [Image.open(p).convert("RGB") for p in paths]
    ims = [im.resize((max(1, int(round(im.width * height / im.height))), height),
                     Image.LANCZOS) for im in ims]
    W = sum(im.width for im in ims) + gap * (len(ims) - 1)
    canvas = Image.new("RGB", (W, height), bg)
    x = 0
    for im in ims:
        canvas.paste(im, (x, 0))
        x += im.width + gap
    canvas.save(out)
    return canvas.size


def main():
    io = os.path.join

    def p(name):
        return io(HERE, name)

    fig_rect(p("fig-1-rect.png"))
    fig_polar(p("fig-2-polar.png"))
    fig_cyl(p("fig-3-cyl.png"))
    fig_sph(p("fig-4-sph.png"))

    size = stitch([p("fig-1-rect.png"), p("fig-2-polar.png"),
                   p("fig-3-cyl.png"), p("fig-4-sph.png")],
                  p("fig-overview.png"))

    fig_elem_line(p("fig-5-line.png"))
    fig_elem_area(p("fig-6-area.png"))
    fig_elem_volume(p("fig-7-volume.png"))

    for nm in ("fig-1-rect.png", "fig-2-polar.png", "fig-3-cyl.png",
               "fig-4-sph.png", "fig-overview.png", "fig-5-line.png",
               "fig-6-area.png", "fig-7-volume.png"):
        with Image.open(p(nm)) as im:
            print("%-20s %5d x %4d px   %6.1f x %5.1f mm at 300 dpi"
                  % (nm, im.width, im.height, im.width / 300.0 * 25.4,
                     im.height / 300.0 * 25.4))
    print("overview canvas: %d x %d" % size)

    check_exact()


if __name__ == "__main__":
    main()
