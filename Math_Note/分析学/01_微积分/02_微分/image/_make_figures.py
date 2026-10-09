# -*- coding: utf-8 -*-
"""
Figures for the note
    "微分与局部线性映射：从切线、切平面到 Jacobian"

The style deliberately matches the sibling note "弧长、面积与体积元素"
(02_多元微积分/03_多元积分学/01_重积分/image/_make_figures.py), so that the
figures of the two notes read as one set:

    * the same oblique parallel projection for 3-D panels,
    * the same fonts (DejaVu Sans + Computer Modern mathtext),
    * the same colour convention: blue = first coordinate direction,
      red = second (the two directions spanning the linear object),
    * the same white label boxes and 300 dpi tight-bbox export.

Outputs (written next to this script):
    fig-1-tangent-line.png    one variable : curve, tangent, dy vs Delta y
    fig-2-tangent-plane.png   two variables: graph surface and tangent plane
    fig-3-jacobian-area.png   general map  : the linearisation scales area
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


def xy(p):
    return proj(*p)[0]


def dot3(ax, p, color="#D62728", ms=5.5, zorder=7):
    q = xy(p)
    ax.plot([q[0]], [q[1]], marker="o", ms=ms, mfc=color, mec=color,
            zorder=zorder)


def poly3(ax, pts, **kw):
    p = proj([q[0] for q in pts], [q[1] for q in pts], [q[2] for q in pts])
    ax.add_patch(Polygon(p, closed=True, **kw))


def head_at(ax, a, b, color, head, zorder):
    d = b - a
    L = np.hypot(d[0], d[1])
    if L == 0:
        return
    d = d / L
    n = np.array([-d[1], d[0]])
    base = b - head * d
    ax.add_patch(Polygon([b, base + 0.55 * head * n, base - 0.55 * head * n],
                         closed=True, facecolor=color, edgecolor="none",
                         zorder=zorder))


def arrow3(ax, a, b, color="black", lw=1.6, head=0.030, zorder=6):
    """3-D vector a->b: a projected segment plus a filled triangular head."""
    pa, pb = xy(a), xy(b)
    ax.plot([pa[0], pb[0]], [pa[1], pb[1]], color=color, lw=lw,
            solid_capstyle="round", zorder=zorder)
    head_at(ax, pa, pb, color, head, zorder)


def arrow2(ax, a, b, color="black", lw=1.6, head=0.030, zorder=6):
    """Plain 2-D vector, same look as arrow3."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw,
            solid_capstyle="round", zorder=zorder)
    head_at(ax, a, b, color, head, zorder)


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


# ----------------------------------------------------------- shared styles
C1C, C2C, C3C = "#1F3FBF", "#B22222", "#009E73"
AXIS = dict(color="black", lw=1.5, zorder=3, solid_capstyle="round")
DASH = dict(color="black", lw=1.0, ls=(0, (4.5, 3)), zorder=4)
SOFT = dict(color="0.80", lw=0.6, zorder=1)
CURVE = dict(color="0.20", lw=1.7, zorder=5, solid_capstyle="round")
LABELBOX = dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.4)
DOT = "#D62728"


# --------------------------------------------- 1 one variable: tangent line
def fig_tangent_line(path):
    fig, ax = new_fig(4.2, 4.2)
    f = lambda t: 0.55 * t ** 2 + 0.15
    fp = lambda t: 1.10 * t
    x0, dx = 0.42, 0.42
    x1 = x0 + dx

    A = 1.46
    arrow2(ax, (-0.06, 0.0), (A, 0.0), lw=1.5, head=0.032)
    arrow2(ax, (0.0, -0.06), (0.0, A), lw=1.5, head=0.032)
    ax.text(A, -0.045, r"$x$", fontsize=15, ha="left", va="top")
    ax.text(-0.035, A, r"$y$", fontsize=15, ha="right", va="top")

    t = np.linspace(0.0, 1.20, 220)
    ax.plot(t, f(t), **CURVE)
    ax.text(1.045, f(1.045) + 0.055, r"$y=f(x)$", fontsize=14, ha="left",
            va="bottom", zorder=9, bbox=LABELBOX)

    # the tangent, i.e. the best linear approximation at x0
    L = lambda s: f(x0) + fp(x0) * (s - x0)
    s = np.linspace(0.02, 1.24, 2)
    ax.plot(s, L(s), color=C1C, lw=1.8, zorder=5, solid_capstyle="round")
    ax.text(1.10, L(1.10) + 0.050, r"$L_{x_0}$", fontsize=15, color=C1C,
            ha="left", va="bottom", zorder=9, bbox=LABELBOX)

    # guides: base level through (x0, f(x0)) and the vertical at x0 + dx
    ax.plot([x0, x1 + 0.13], [f(x0), f(x0)], **DASH)
    ax.plot([x0, x0], [0.0, f(x0)], **DASH)
    ax.plot([x1, x1], [0.0, f(x1) + 0.04], **DASH)

    # dy (from f(x0) up to the tangent) and the remainder o(|dx|) stacked on top
    arrow2(ax, (x1, f(x0)), (x1, L(x1)), color=C3C, lw=1.9, head=0.028)
    arrow2(ax, (x1, L(x1)), (x1, f(x1)), color=C2C, lw=1.9, head=0.028)

    dot2 = (x0, f(x0))
    ax.plot([dot2[0]], [dot2[1]], marker="o", ms=5.5, color=DOT, zorder=9)
    ax.text(x0, -0.055, r"$x_0$", fontsize=14, ha="center", va="top")
    ax.text(x1, -0.055, r"$x_0+\Delta x$", fontsize=14, ha="center", va="top")

    ax.text(x1 + 0.045, 0.5 * (f(x0) + L(x1)), r"$\mathrm{d}y$", color=C3C,
            fontsize=14, ha="left", va="center", zorder=9, bbox=LABELBOX)
    ax.text(x1 + 0.045, 0.5 * (L(x1) + f(x1)), r"$o(|\Delta x|)$",
            color=C2C, fontsize=13, ha="left", va="center", zorder=9,
            bbox=LABELBOX)
    ax.text(0.10, 1.33, r"$\Delta y=\mathrm{d}y+o(|\Delta x|)$",
            fontsize=12.5, ha="left", va="center", zorder=9, bbox=LABELBOX)

    fit(ax, pad=0.03)
    save(fig, path)


# ------------------------------------------- 2 two variables: tangent plane
def fig_tangent_plane(path):
    fig, ax = new_fig(4.2, 4.0)

    par = lambda x, y: 1.00 - 1.30 * ((x - 0.55) ** 2 + (y - 0.50) ** 2)
    x0, y0 = 0.38, 0.32
    z0 = par(x0, y0)
    fx = -2.60 * (x0 - 0.55)
    fy = -2.60 * (y0 - 0.50)
    plane = lambda x, y: z0 + fx * (x - x0) + fy * (y - y0)

    A = 1.16
    for v, nm, ex, ey in (((A, 0, 0), "x", -0.030, -0.035),
                          ((0, A, 0), "y", 0.035, -0.020),
                          ((0, 0, A), "z", 0.020, 0.030)):
        seg(ax, (0, 0, 0), v, **AXIS)
        p = xy(v)
        ax.text(p[0] + ex, p[1] + ey, r"$%s$" % nm, fontsize=15,
                ha="center", va="center", zorder=9)

    xlo, xhi, ylo, yhi = 0.14, 0.96, 0.12, 0.90
    for xv in np.linspace(xlo, xhi, 9):
        curve(ax, [(xv, yv, par(xv, yv)) for yv in np.linspace(ylo, yhi, 60)],
              **SOFT)
    for yv in np.linspace(ylo, yhi, 9):
        curve(ax, [(xv, yv, par(xv, yv)) for xv in np.linspace(xlo, xhi, 60)],
              **SOFT)
    # the two coordinate traces through the point of tangency
    curve(ax, [(xv, y0, par(xv, y0)) for xv in np.linspace(xlo, xhi, 60)],
          color="0.58", lw=0.9, zorder=2)
    curve(ax, [(x0, yv, par(x0, yv)) for yv in np.linspace(ylo, yhi, 60)],
          color="0.58", lw=0.9, zorder=2)

    h = 0.17
    corners = [(x0 - h, y0 - h), (x0 + h, y0 - h),
               (x0 + h, y0 + h), (x0 - h, y0 + h)]
    poly3(ax, [(x, y, plane(x, y)) for x, y in corners],
          facecolor="0.90", edgecolor="black", lw=1.1, ls=(0, (5, 3)),
          zorder=3)

    seg(ax, (x0, y0, 0.0), (x0, y0, z0), **DASH)

    g = 0.80
    arrow3(ax, (x0, y0, 0.0), (x0 + g * fx, y0 + g * fy, 0.0), color=C1C,
           lw=1.9, head=0.026)
    dot3(ax, (x0, y0, z0))

    p = xy((x0, y0, z0))
    ax.text(p[0], p[1] + 0.055, r"$\mathbf{x}_0$", fontsize=14,
            ha="center", va="bottom", zorder=9, bbox=LABELBOX)
    pc = xy((x0 + h, y0 + h, plane(x0 + h, y0 + h)))
    ax.text(pc[0] + 0.070, pc[1] - 0.085, r"$L_{\mathbf{x}_0}$", fontsize=14,
            ha="left", va="top", zorder=9, bbox=LABELBOX)
    q = xy((x0 + g * fx, y0 + g * fy, 0.0))
    ax.text(q[0] + 0.020, q[1] - 0.075, r"$\nabla f(\mathbf{x}_0)$",
            color=C1C, fontsize=13, ha="left", va="top", zorder=9,
            bbox=LABELBOX)
    r = xy((xhi, yhi, par(xhi, yhi)))
    ax.text(r[0] + 0.030, r[1] + 0.030, r"$z=f(x,y)$", fontsize=14,
            ha="left", va="bottom", zorder=9, bbox=LABELBOX)

    fit(ax, pad=0.04)
    save(fig, path)


# ------------------------------------------- 3 general map: area scaling
def fig_jacobian_area(path):
    fig, ax = new_fig(5.0, 2.4)

    # left: the elementary square in the (u, v) domain
    arrow2(ax, (-0.06, 0.0), (1.24, 0.0), lw=1.5, head=0.030)
    arrow2(ax, (0.0, -0.06), (0.0, 1.24), lw=1.5, head=0.030)
    ax.text(1.24, -0.05, r"$u$", fontsize=15, ha="left", va="top")
    ax.text(-0.035, 1.24, r"$v$", fontsize=15, ha="right", va="top")
    ax.add_patch(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], closed=True,
                         facecolor="0.93", edgecolor="0.25", lw=1.1, zorder=3))
    arrow2(ax, (0, 0), (1, 0), color=C1C, lw=1.9, head=0.028)
    arrow2(ax, (0, 0), (0, 1), color=C2C, lw=1.9, head=0.028)
    ax.text(0.5, -0.055, r"$\mathrm{d}u$", color=C1C, fontsize=14,
            ha="center", va="top")
    ax.text(-0.055, 0.5, r"$\mathrm{d}v$", color=C2C, fontsize=14,
            ha="right", va="center")
    ax.text(0.5, 0.5, r"$\mathrm{d}u\,\mathrm{d}v$", fontsize=13.5,
            ha="center", va="center", zorder=9, bbox=LABELBOX)

    # the linearisation acting on the two edges
    arrow2(ax, (1.46, 0.5), (2.02, 0.5), color="black", lw=1.6, head=0.034)
    ax.text(1.74, 0.60, r"$J_{\mathbf{g}}(\mathbf{u})$", fontsize=13,
            ha="center", va="bottom", zorder=9)

    # right: the image parallelogram, i.e. the tangent parallelogram
    ox, oy = 2.34, 0.0
    eu = np.array([1.25, 0.42])
    ev = np.array([0.48, 1.22])
    arrow2(ax, (ox - 0.06, oy), (ox + 1.98, oy), lw=1.5, head=0.030)
    arrow2(ax, (ox, oy - 0.06), (ox, oy + 1.46), lw=1.5, head=0.030)
    ax.text(ox + 1.98, oy - 0.05, r"$x$", fontsize=15, ha="left", va="top")
    ax.text(ox - 0.035, oy + 1.46, r"$y$", fontsize=15, ha="right", va="top")
    o = np.array([ox, oy])
    quad = [o, o + eu, o + eu + ev, o + ev]
    ax.add_patch(Polygon(quad, closed=True, facecolor="0.90",
                         edgecolor="0.25", lw=1.1, zorder=3))
    arrow2(ax, o, o + eu, color=C1C, lw=1.9, head=0.028)
    arrow2(ax, o, o + ev, color=C2C, lw=1.9, head=0.028)

    d = eu / np.hypot(*eu)
    n = np.array([d[1], -d[0]])          # downward normal of the blue edge
    m = o + 0.68 * eu + 0.16 * n
    ax.text(m[0], m[1], r"$J_{\mathbf{g}}\,\mathrm{d}u$", color=C1C,
            fontsize=13, ha="center", va="center", zorder=9, bbox=LABELBOX)
    m = o + 0.5 * ev
    ax.text(m[0] + 0.30, m[1], r"$J_{\mathbf{g}}\,\mathrm{d}v$", color=C2C,
            fontsize=13, ha="left", va="center", zorder=9, bbox=LABELBOX)
    c = o + ev + 0.5 * eu
    ax.text(c[0], c[1] + 0.12,
            r"$|\det J_{\mathbf{g}}|\,\mathrm{d}u\,\mathrm{d}v$",
            fontsize=13, ha="center", va="bottom", zorder=9, bbox=LABELBOX)

    fit(ax, pad=0.03)
    save(fig, path)


# ------------------------------------------------------------------- main
def main():
    def p(name):
        return os.path.join(HERE, name)

    fig_tangent_line(p("fig-1-tangent-line.png"))
    fig_tangent_plane(p("fig-2-tangent-plane.png"))
    fig_jacobian_area(p("fig-3-jacobian-area.png"))

    for nm in ("fig-1-tangent-line.png", "fig-2-tangent-plane.png",
               "fig-3-jacobian-area.png"):
        with Image.open(p(nm)) as im:
            print("%-28s %5d x %4d px   %6.1f x %5.1f mm at 300 dpi"
                  % (nm, im.width, im.height, im.width / 300.0 * 25.4,
                     im.height / 300.0 * 25.4))


if __name__ == "__main__":
    main()
