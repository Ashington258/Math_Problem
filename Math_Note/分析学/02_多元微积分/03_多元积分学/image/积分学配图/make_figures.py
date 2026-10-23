"""Reproducible geometry figures for the multivariable integration notes.

Run: python make_figures.py
Outputs: eight 178-mm figures, PDF + 600-dpi PNG, and preview contact sheets.
All coordinates are dimensionless; geometric projections are orthographic.
No empirical data or uncertainty is represented. No random numbers are used.
The local sci_style.py is copied from the invoked sci-plot skill.
"""
from pathlib import Path
import json
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
from matplotlib.lines import Line2D
import numpy as np
from PIL import Image, ImageOps, ImageDraw

import sci_style as ss

HERE = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ["DejaVu Sans"]
ss.apply("double", font_size=8, line_width=1.4, mathtext=False)
plt.rcParams.update({"savefig.pad_inches": 0, "svg.fonttype": "path"})
BLUE = ss.OKABE_ITO["blue"]
ORANGE = ss.OKABE_ITO["vermillion"]
GRAY = "0.48"
PALE = "0.91"
DASH = (0, (4, 2.5))
EXPORTS = []


def figure(height=76, n=2):
    fig, axes = plt.subplots(1, n, figsize=ss.figsize("double", height_mm=height))
    fig.subplots_adjust(left=.10, right=.94, bottom=.24, top=.88, wspace=.42)
    # Invisible canvas bounds keep ss.save(bbox_inches='tight') at 178 mm.
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             facecolor="none", edgecolor="none", linewidth=0))
    axes = np.atleast_1d(axes)
    ss.panels(fig, axes, "ABCDEFGH", x=-.10, y=1.045)
    return fig, axes


def label(ax, xy, s, color="black", ha="center", va="center", fs=8, box=True):
    s = re.sub(r"\\(mathbf|mathbb)\s+([A-Za-z])", r"\\\1{\2}", s)
    return ax.text(*xy, s, color=color, ha=ha, va=va, fontsize=fs, zorder=20,
                   bbox=dict(facecolor="white", edgecolor="none", alpha=.93,
                             pad=1.3) if box else None)


def arrow(ax, p, q, color=ORANGE, lw=1.4, ls="-", size=9, z=10):
    return ax.annotate("", xy=q, xytext=p, zorder=z,
                       arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                       linestyle=ls, mutation_scale=size,
                                       shrinkA=0, shrinkB=0))


def plane(ax, xlim, ylim, ticks=True):
    ax.set(xlim=xlim, ylim=ylim, aspect="equal")
    if ticks:
        ax.set_xlabel('$x$ (dimensionless)')
        ax.set_ylabel('$y$ (dimensionless)')
        ax.minorticks_off()
    else:
        ax.set_axis_off()


def footer(ax, s, color="black", y=-.15):
    s = re.sub(r"\\(mathbf|mathbb)\s+([A-Za-z])", r"\\\1{\2}", s)
    ax.text(.5, y, s, transform=ax.transAxes, ha="center", va="top",
            color=color, fontsize=8)


def circle_path(ax, radius=1, center=(0, 0), color=BLUE, lw=1.5, ls="-"):
    t = np.linspace(0, 2*np.pi, 361)
    center = np.asarray(center)
    points = center + radius*np.column_stack((np.cos(t), np.sin(t)))
    ax.plot(points[:, 0], points[:, 1], color=color, lw=lw, ls=ls)


def arc_arrow(ax, a, b, radius=1, color=BLUE, lw=1.4):
    t = np.linspace(a, b, 35)
    points = radius*np.column_stack((np.cos(t), np.sin(t)))
    ax.plot(points[:, 0], points[:, 1], color=color, lw=lw, zorder=8)
    arrow(ax, points[-3], points[-1], color, lw=lw, size=8)


def project(points):
    """Fixed orthographic projection; basis vectors are orthonormal."""
    points = np.asarray(points, dtype=float)
    matrix = np.array([[np.sqrt(3)/2, -.5, 0], [.25, np.sqrt(3)/4, np.sqrt(3)/2]])
    return points @ matrix.T


def space_line(ax, points, **kwargs):
    p = project(points)
    ax.plot(p[:, 0], p[:, 1], **kwargs)


def space_arrow(ax, p, q, **kwargs):
    p, q = project([p, q])
    arrow(ax, p, q, **kwargs)


def space_label(ax, p, text, offset=(0, 0), **kwargs):
    label(ax, project(p)+np.asarray(offset), text, **kwargs)


def space_axes(ax, length=1.25):
    for end, name, off in [([length, 0, 0], '$x$', (.09, 0)),
                           ([0, length, 0], '$y$', (-.07, .07)),
                           ([0, 0, length], '$z$', (.07, .06))]:
        space_arrow(ax, [0, 0, 0], end, color=GRAY, lw=.7, size=6, z=2)
        space_label(ax, end, name, off, color=GRAY, box=False)


def save(fig, stem, caption):
    # Fit annotations inside the declared canvas; font sizes never shrink.
    width, height = fig.get_size_inches()
    for _ in range(24):
        fig.canvas.draw()
        bounds = fig.get_tightbbox(fig.canvas.get_renderer())
        if bounds.x0 >= -.00001 and bounds.y0 >= -.00001 and bounds.x1 <= width+.00001 and bounds.y1 <= height+.00001:
            break
        for ax in fig.axes:
            p = ax.get_position(original=True)
            ax.set_position([.5+.94*(p.x0-.5), .5+.94*(p.y0-.5), .94*p.width, .94*p.height])
    else:
        raise RuntimeError(f"Annotations outside fixed canvas: {stem}")
    for ax in fig.axes:
        for text in ax.texts:
            assert text.get_fontsize() >= 6, f"Small text: {text.get_text()}"
    path = ss.save(fig, HERE / f"{stem}.pdf", also_png=True, dpi=600)
    size = ss.output_size_mm(path)
    assert size and abs(size[0]-178) < .05, size
    with Image.open(path.with_suffix(".png")) as im:
        assert im.width >= 4200
        assert abs(im.info["dpi"][0]-600) < .1
    EXPORTS.append(dict(stem=stem, width_mm=round(size[0], 3),
                        height_mm=round(size[1], 3), dpi=600, caption=caption))
    plt.close(fig)


def slicing():
    fig, axs = figure(78)
    for ax in axs:
        plane(ax, (-.04, 1.10), (-.04, 1.10))
        ax.set_xticks([0, .5, 1]); ax.set_yticks([0, .5, 1])
        ax.add_patch(Polygon([[0, 0], [0, 1], [1, 1]], facecolor=PALE,
                             edgecolor=BLUE, lw=1.4))
        label(ax, (.22, .83), '$D$', box=False)
        label(ax, (.67, .59), '$y=x$', color=BLUE, box=False)
    ax = axs[0]
    x, dx = .37, .07
    ax.add_patch(Polygon([[x, x], [x, 1], [x+dx, 1], [x+dx, x+dx]],
                         facecolor=ORANGE, alpha=.22, edgecolor="none"))
    arrow(ax, (x+dx/2, .49), (x+dx/2, .95), color=ORANGE)
    label(ax, (.70, .82), '$x\\leq y\\leq1$', color=ORANGE)
    ax.plot([x, x], [0, x], color=GRAY, lw=.8, ls=DASH)
    label(ax, (x+dx/2, .075), '$\\mathrm{d}x$', color=ORANGE)
    footer(ax, '$\\int_0^1\\!\\left[\\int_x^1 f(x,y)\\,\\mathrm{d}y\\right]\\mathrm{d}x$', y=-.34)
    ax = axs[1]
    y, dy = .64, .07
    ax.add_patch(Polygon([[0, y], [y, y], [y+dy, y+dy], [0, y+dy]],
                         facecolor=ORANGE, alpha=.22, edgecolor="none"))
    arrow(ax, (.07, y+dy/2), (.58, y+dy/2), color=ORANGE)
    label(ax, (.62, .89), '$0\\leq x\\leq y$', color=ORANGE)
    label(ax, (.075, y+dy/2+.08), '$\\mathrm{d}y$', color=ORANGE)
    footer(ax, '$\\int_0^1\\!\\left[\\int_0^y f(x,y)\\,\\mathrm{d}x\\right]\\mathrm{d}y$', y=-.34)
    save(fig, "fig-01-slicing", "同一三角形区域的竖直、水平切片，换序只改变描述。")


def polar_element():
    fig, axs = figure(82)
    ax = axs[0]
    ax.set(xlim=(.55, 1.65), ylim=(.3, .94), aspect="auto",
           xlabel='$r$ (dimensionless)', ylabel='$\\theta$ (rad)')
    ax.set_xticks([.8, 1.3], ['$r$', '$r+\\Delta r$'])
    ax.set_yticks([.46, .72], ['$\\theta$', '$\\theta+\\Delta\\theta$'])
    ax.minorticks_off()
    ax.add_patch(Rectangle((.8, .46), .5, .26, facecolor=PALE, edgecolor=BLUE, lw=1.5))
    label(ax, (1.05, .59), '$\\Delta r\\,\\Delta\\theta$', color=BLUE)
    label(ax, (1.05, .84), '$U$', box=False)
    footer(ax, '$T(r,\\theta)=(r\\cos\\theta,r\\sin\\theta)$', y=-.35)
    ax = axs[1]
    plane(ax, (-.04, 1.45), (-.04, 1.2))
    ax.set_xticks([0, .5, 1]); ax.set_yticks([0, .5, 1])
    a, b, r1, r2 = .46, .72, .8, 1.3
    t = np.linspace(a, b, 80)
    outer = r2*np.column_stack([np.cos(t), np.sin(t)])
    inner = r1*np.column_stack([np.cos(t[::-1]), np.sin(t[::-1])])
    ax.add_patch(Polygon(np.vstack([outer, inner]), facecolor=PALE, edgecolor=BLUE, lw=1.4))
    for angle in [a, b]:
        ax.plot([0, r2*np.cos(angle)], [0, r2*np.sin(angle)], color=GRAY, lw=.7, ls=DASH)
    arc_arrow(ax, .02, a, radius=.30, color=GRAY, lw=.8)
    label(ax, (.40, .07), '$\\theta$', color=GRAY, box=False)
    arc_arrow(ax, a, b, radius=.50, color=ORANGE, lw=1.2)
    label(ax, (.37, .48), '$\\Delta\\theta$', color=ORANGE)
    label(ax, (1.19, .45), '$\\Delta r$', color=BLUE)
    label(ax, (.77, 1.00), '$r\\,\\Delta\\theta$', color=BLUE)
    # Leader targets the inner arc: its exact length is r*Delta theta.
    midpoint = r1*np.array([np.cos((a+b)/2), np.sin((a+b)/2)])
    ax.plot([.77, midpoint[0]], [.94, midpoint[1]], color=BLUE, lw=.65)
    footer(ax, '$\\mathrm{d}A=r\\,\\mathrm{d}r\\,\\mathrm{d}\\theta$', y=-.35)
    save(fig, "fig-02-polar-element", "参数矩形映成环形扇区，面积按局部 Jacobian r 缩放。")


def curve_direction():
    fig, axs = figure(79)
    a = np.pi/4
    p = np.array([np.cos(a), np.sin(a)])
    tangent = np.array([-np.sin(a), np.cos(a)])
    for ax, orientation in zip(axs, [1, -1]):
        plane(ax, (-1.35, 1.35), (-1.35, 1.42), ticks=False)
        ax.axhline(0, lw=.65, color="0.75"); ax.axvline(0, lw=.65, color="0.75")
        circle_path(ax)
        label(ax, (1.22, -.09), '$x$', color=GRAY, box=False)
        label(ax, (.10, 1.25), '$y$', color=GRAY, box=False)
        label(ax, (0, -.09), '$O$', color=GRAY, box=False)
        ax.plot(*p, "o", color="black", ms=4)
        arc_arrow(ax, 3.5 if orientation == 1 else 4.2,
                  4.2 if orientation == 1 else 3.5, color=BLUE)
        arrow(ax, p, p+.56*tangent, color=ORANGE)
        arrow(ax, p, p+orientation*.38*tangent, color=BLUE, ls=DASH)
        label(ax, (-.30, 1.24), '$\\mathbf{F}$', color=ORANGE)
        label(ax, p+orientation*.40*tangent+[.20, -.16],
              '$\\mathbf{T}$', color=BLUE)
        label(ax, (0, -.48), '$\\mathbf{F}=(-y,x)$', box=False)
        footer(ax, '$\\int_C \\mathrm{d}s=2\\pi\\qquad\\oint_C\\mathbf F\\cdot \\mathrm{d}\\mathbf r='
               + ('2\\pi$' if orientation == 1 else '-2\\pi$'), y=-.10)
    save(fig, "fig-03-curve-direction", "单位圆反向后，弧长不变，旋转场的功积分变号。")


def surface_flux():
    fig, axs = figure(88)
    ax = axs[0]
    plane(ax, (-.95, 1.45), (-.22, 2.52), ticks=False)
    vertices = np.array([[0, 0, 0], [1, 0, 1], [1, 1, 2], [0, 1, 1]])
    shadow = vertices.copy(); shadow[:, 2] = 0
    ax.add_patch(Polygon(project(shadow), facecolor=PALE, edgecolor=GRAY, lw=.9, ls=DASH))
    ax.add_patch(Polygon(project(vertices), facecolor="#E5F0F6", edgecolor=BLUE, lw=1.6))
    for p, q in zip(vertices[1:], shadow[1:]):
        space_line(ax, [p, q], color=GRAY, lw=.65, ls=DASH)
    space_axes(ax)
    center = np.array([.50, .50, 1.])
    normal = np.array([-1, -1, 1])/np.sqrt(3)
    space_arrow(ax, center, center+.70*normal, color=BLUE, ls=DASH)
    space_label(ax, center+.82*normal, '$\\mathbf{n}$', offset=(-.1, .02), color=BLUE)
    space_arrow(ax, center, center+[0, 0, .83], color=ORANGE)
    label(ax, (-.28, 2.28), '$\\mathbf{F}=(0,0,1)$', color=ORANGE)
    label(ax, (1.0, 1.52), '$S:z=x+y$', color=BLUE)
    space_label(ax, [.55, .55, 0], '$D$', offset=(.04, -.04), color=GRAY)
    footer(ax, '$\\mathrm{Area}(S)=\\sqrt{3},\\quad\\mathrm{Area}(D)=1$', y=-.12)
    ax = axs[1]
    plane(ax, (-.9, 1.3), (-.45, 2.0), ticks=False)
    # True section through the vertical field and surface normal:
    # horizontal coordinate s=(x+y)/sqrt(2), plane z=sqrt(2)*s.
    slope = np.sqrt(2)
    s = np.linspace(-.32, .78, 2)
    ax.plot(s, slope*s, color=BLUE, lw=1.6)
    p = np.array([.3, slope*.3])
    n = np.array([-np.sqrt(2), 1])/np.sqrt(3)
    F = np.array([0, 1.])
    Fn = np.dot(F, n)*n
    Ft = F-Fn
    arrow(ax, p, p+F, color=ORANGE)
    arrow(ax, p, p+Fn, color=BLUE, ls=DASH)
    arrow(ax, p+Fn, p+F, color=GRAY, ls=DASH)
    label(ax, p+F+[.05, .12], '$\\mathbf{F}$', color=ORANGE)
    label(ax, p+Fn+[-.14, -.06], '$(\\mathbf{F}\\cdot\\mathbf{n})\\mathbf{n}$', color=BLUE)
    label(ax, p+Fn+.60*Ft+[.30, -.1], '$\\mathbf{F}_{\\parallel}$', color=GRAY)
    label(ax, (.82, .87), '$S$', color=BLUE)
    label(ax, (.23, -.28), '$\\mathbf{F}\\cdot\\mathbf{n}=1/\\sqrt{3}$')
    footer(ax, '$\\iint_S\\mathbf{F}\\cdot\\mathbf{n}\\,\\mathrm{d}S=(1/\\sqrt{3})\\sqrt{3}=1$', y=-.12)
    save(fig, "fig-04-surface-flux", "单位正方形上的斜面面积为 sqrt(3)，竖直场通量为 1。")


def cancellation():
    fig, axs = figure(70)
    for ax in axs:
        plane(ax, (-.24, 2.24), (-.22, 1.38), ticks=False)
        ax.add_patch(Rectangle((0, 0), 2, 1, facecolor=PALE, edgecolor=BLUE, lw=1.5))
        ax.plot([1, 1], [0, 1], color=GRAY, ls=DASH, lw=1)
        label(ax, (.5, .63), '$D_1$', color=GRAY)
        label(ax, (1.5, .63), '$D_2$', color=GRAY)
    ax = axs[0]
    for left in [0, 1]:
        arrow(ax, (left+.18, .025), (left+.70, .025), color=BLUE)
        arrow(ax, (left+.80, .975), (left+.28, .975), color=BLUE)
    arrow(ax, (.025, .74), (.025, .26), color=BLUE)
    arrow(ax, (1.975, .26), (1.975, .74), color=BLUE)
    arrow(ax, (.96, .18), (.96, .48), color=ORANGE, lw=1.7)
    arrow(ax, (1.04, .48), (1.04, .18), color=ORANGE, lw=1.7, ls=DASH)
    label(ax, (1, 1.19), '$\\mathrm{d}\\mathbf{r}_2=-\\mathrm{d}\\mathbf{r}_1$', color=ORANGE)
    footer(ax, '$\\int_{e}\\mathbf{F}\\cdot \\mathrm{d}\\mathbf{r}+\\int_{-e}\\mathbf{F}\\cdot \\mathrm{d}\\mathbf{r}=0$', y=-.18)
    ax = axs[1]
    arrow(ax, (.78, .32), (1.25, .32), color=ORANGE, lw=1.7)
    arrow(ax, (1.22, .18), (.75, .18), color=ORANGE, lw=1.7, ls=DASH)
    label(ax, (1, 1.19), '$\\mathbf{n}_2=-\\mathbf{n}_1$', color=ORANGE)
    for p, q in [((0, .45), (-.17, .45)), ((2, .45), (2.17, .45)),
                 ((.5, 1), (.5, 1.15)), ((1.5, 1), (1.5, 1.15)),
                 ((.5, 0), (.5, -.15)), ((1.5, 0), (1.5, -.15))]:
        arrow(ax, p, q, color=BLUE, lw=1.1, size=7)
    footer(ax, '$\\mathbf{F}\\cdot\\mathbf{n}_1+\\mathbf{F}\\cdot\\mathbf{n}_2=0$', y=-.18)
    save(fig, "fig-05-internal-cancellation", "共享边的走向相反，共享面的外法向相反，内部贡献相消。")


def stokes_surfaces():
    fig, axs = figure(86)
    t = np.linspace(0, 2*np.pi, 361)
    boundary = np.column_stack([np.cos(t), np.sin(t), np.zeros_like(t)])
    for ax in axs:
        plane(ax, (-1.35, 1.35), (-.88, 1.43), ticks=False)
    ax = axs[0]
    ax.add_patch(Polygon(project(boundary), facecolor=PALE, edgecolor="none"))
    space_line(ax, boundary, color=BLUE, lw=1.7)
    for x, y in [(-.5, 0), (0, 0), (.5, 0)]:
        space_arrow(ax, [x, y, 0], [x, y, .50], color=ORANGE, lw=1.3)
    space_label(ax, [0, 0, .82], '$\\nabla\\times\\mathbf{F}=(0,0,2)$', color=ORANGE)
    space_arrow(ax, [0, -.48, 0], [0, -.48, .34], color=BLUE, ls=DASH)
    space_label(ax, [0, -.48, .43], '$\\mathbf{n}$', offset=(.08, .02), color=BLUE)
    label(ax, (-.65, -.78), '$S_1$', color=GRAY)
    ax = axs[1]
    phis = np.linspace(0, np.pi/2, 80)
    for az in np.linspace(0, 2*np.pi, 13)[:-1]:
        points = np.column_stack([np.sin(phis)*np.cos(az), np.sin(phis)*np.sin(az), np.cos(phis)])
        space_line(ax, points, color="0.68", lw=.65)
    for phi in [.35, .7, 1.05, 1.35]:
        points = np.column_stack([np.sin(phi)*np.cos(t), np.sin(phi)*np.sin(t), np.full_like(t, np.cos(phi))])
        space_line(ax, points, color="0.68", lw=.65)
    space_line(ax, boundary, color=BLUE, lw=1.7)
    p = np.array([.48, -.36, .8])
    space_arrow(ax, p, 1.4*p, color=BLUE, ls=DASH)
    space_label(ax, 1.49*p, '$\\mathbf{n}$', offset=(.05, 0), color=BLUE)
    space_arrow(ax, [-.3, 0, .954], [-.3, 0, 1.28], color=ORANGE)
    label(ax, (-.70, -.78), '$S_2$', color=GRAY)
    for ax in axs:
        tt = np.linspace(4.0, 4.55, 25)
        p = project(np.column_stack([np.cos(tt), np.sin(tt), np.zeros_like(tt)]))
        ax.plot(p[:, 0], p[:, 1], color=BLUE, lw=1.7)
        arrow(ax, p[-3], p[-1], color=BLUE)
        label(ax, (.95, -.69), '$C=\\partial S$', color=BLUE)
        footer(ax, '$\\iint_S(\\nabla\\times\\mathbf{F})\\cdot\\mathbf{n}\\,\\mathrm{d}S=\\oint_C\\mathbf{F}\\cdot \\mathrm{d}\\mathbf{r}=2\\pi$', y=-.14)
    save(fig, "fig-06-stokes-surfaces", "同一边界可由圆盘或上半球跨接，旋度通量均为 2pi。")


def gauss_hole():
    fig, axs = figure(80)
    for ax in axs:
        plane(ax, (-1.40, 1.40), (-1.50, 1.45), ticks=False)
        ax.add_patch(Circle((0, 0), 1, facecolor=PALE, edgecolor=BLUE, lw=1.5))
        for angle in np.linspace(0, 2*np.pi, 9)[:-1]:
            radial = np.array([np.cos(angle), np.sin(angle)])
            arrow(ax, .99*radial, 1.23*radial, color=BLUE, lw=1.2, size=7)
        label(ax, (0, 1.38), '$\\Phi_{\\mathrm{outer}}=4\\pi$', color=BLUE)
    ax = axs[0]
    ax.plot(0, 0, "x", color=ORANGE, mew=1.6, ms=6)
    label(ax, (0, -.38), '$\\mathbf{F}=\\mathbf{r}/\\|\\mathbf{r}\\|^3$', color=ORANGE)
    label(ax, (0, .36), '$\\nabla\\cdot\\mathbf{F}=0\\quad(r>0)$', color=GRAY)
    footer(ax, '$\\mathbf{F}(0)\\ \\mathrm{undefined}$', color=ORANGE, y=-.10)
    ax = axs[1]
    ax.add_patch(Circle((0, 0), .37, facecolor="white", edgecolor=ORANGE, lw=1.4, ls=DASH))
    for angle in np.linspace(0, 2*np.pi, 7)[:-1]:
        radial = np.array([np.cos(angle), np.sin(angle)])
        arrow(ax, .37*radial, .21*radial, color=ORANGE, lw=1.1, ls=DASH, size=7)
    label(ax, (0, .61), '$\\Phi_{\\mathrm{inner}}=-4\\pi$', color=ORANGE)
    label(ax, (0, -.63), '$\\nabla\\cdot\\mathbf{F}=0$', color=GRAY)
    footer(ax, '$\\Phi_{\\mathrm{total}}=4\\pi-4\\pi=0$', y=-.10)
    save(fig, "fig-07-gauss-hole", "球体包含奇点时不能直接套 Gauss；球壳内外边界通量抵消。")


def potential_paths():
    fig, axs = figure(82)
    ax = axs[0]
    plane(ax, (-.13, 1.23), (-.12, 1.30))
    ax.set_xticks([0, .5, 1]); ax.set_yticks([0, .5, 1])
    xx, yy = np.meshgrid(np.linspace(-.10, 1.18, 180), np.linspace(-.1, 1.18, 180))
    f = xx**2*yy+xx+yy**2
    cs = ax.contour(xx, yy, f, levels=[.5, 1, 2, 3], colors="0.72", linewidths=.65)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%g")
    t = np.linspace(0, 1, 200)
    ax.plot(t, t, color=BLUE, lw=1.6)
    ax.plot(t, t*t, color=ORANGE, lw=1.6, ls=DASH)
    arrow(ax, (.45, .45), (.57, .57), color=BLUE, size=8)
    arrow(ax, (.45, .45**2), (.57, .57**2), color=ORANGE, size=8)
    ax.plot([0, 1], [0, 1], "o", color="black", ms=4)
    label(ax, (.03, .15), '$A:f=0$', ha="left")
    label(ax, (.92, 1.18), '$B:f=3$')
    ax.legend(handles=[Line2D([], [], color=BLUE, label='$C_1$'),
                       Line2D([], [], color=ORANGE, ls=DASH, label='$C_2$')],
              loc="lower right", fontsize=7)
    footer(ax, '$\\int_{C_1}\\nabla f\\cdot \\mathrm{d}\\mathbf{r}=\\int_{C_2}\\nabla f\\cdot \\mathrm{d}\\mathbf{r}=3$', y=-.35)
    ax = axs[1]
    plane(ax, (-1.33, 1.33), (-1.33, 1.42), ticks=False)
    circle_path(ax)
    ax.plot(0, 0, "x", color=ORANGE, ms=6, mew=1.5)
    label(ax, (.28, -.18), '$0\\notin U$', color=ORANGE)
    for angle in np.linspace(0, 2*np.pi, 9)[:-1]:
        p = np.array([np.cos(angle), np.sin(angle)])
        tangent = np.array([-np.sin(angle), np.cos(angle)])
        arrow(ax, p, p+.27*tangent, color=BLUE, size=7)
    label(ax, (0, -.75), '$Q_x-P_y=0$', color=GRAY)
    label(ax, (0, 1.35), '$U=\\mathbb{R}^2\\setminus\\{0\\}$')
    footer(ax, '$\\oint_C\\frac{-y\\,\\mathrm{d}x+x\\,\\mathrm{d}y}{x^2+y^2}=2\\pi\\ne0$', y=-.10)
    save(fig, "fig-08-potential-paths", "有势时不同路径给出同一端点差；穿孔平面上的无旋场可能有非零环流。")


def verify_geometry():
    # Checks connect the actual figure geometry to the values in the notes.
    basis = np.array([[np.sqrt(3)/2, -.5, 0], [.25, np.sqrt(3)/4, np.sqrt(3)/2]])
    assert np.allclose(basis @ basis.T, np.eye(2))
    cross = np.cross([1, 0, 1], [0, 1, 1])
    assert np.allclose(cross, [-1, -1, 1])
    assert np.isclose(np.linalg.norm(cross), np.sqrt(3))
    assert np.isclose(np.dot(cross, [0, 0, 1]), 1)
    t = np.linspace(0, 1, 10001)
    for y, yp in [(t, np.ones_like(t)), (t*t, 2*t)]:
        integrand = (2*t*y+1)+(t*t+2*y)*yp
        assert np.isclose(np.trapezoid(integrand, t), 3, atol=1e-7)
    t = np.linspace(0, 2*np.pi, 10001)
    integrand = np.sin(t)**2+np.cos(t)**2
    assert np.isclose(np.trapezoid(integrand, t), 2*np.pi)
    a, b, r, dr = .46, .72, .8, .5
    sector_area = .5*((r+dr)**2-r**2)*(b-a)
    assert sector_area > r*dr*(b-a)
    print("[ok] geometry, orientation, and path-integral checks")


def previews(prefix="preview"):
    thumbs = []
    for record in EXPORTS:
        with Image.open(HERE / (record["stem"]+".png")) as im:
            im = im.convert("RGB")
            im.thumbnail((1100, 550), Image.Resampling.LANCZOS)
            card = Image.new("RGB", (1140, 590), "white")
            card.paste(im, ((1140-im.width)//2, 20))
            ImageDraw.Draw(card).text((20, 568), record["stem"], fill="black")
            thumbs.append(card)
    for start in range(0, len(EXPORTS), 4):
        sheet = Image.new("RGB", (2280, 1180), "white")
        for i, thumb in enumerate(thumbs[start:start+4]):
            sheet.paste(thumb, ((i%2)*1140, (i//2)*590))
        sheet.save(HERE / f"{prefix}-{start//4+1}.png")
        ImageOps.grayscale(sheet).save(HERE / f"{prefix}-{start//4+1}-gray.png")


if __name__ == "__main__":
    verify_geometry()
    ss.grayscale_check([BLUE, ORANGE])
    print("[style] direct labels, dashed vs solid, and arrow direction supplement color")
    for maker in [slicing, polar_element, curve_direction, surface_flux,
                  cancellation, stokes_surfaces, gauss_hole, potential_paths]:
        maker()
    previews()
    (HERE / "figure_manifest.json").write_text(json.dumps(EXPORTS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] {len(EXPORTS)} figures, PDF + PNG, 178 mm wide at 600 dpi")
