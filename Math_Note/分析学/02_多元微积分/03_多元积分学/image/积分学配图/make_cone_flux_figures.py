"""Exact geometry for the lower-oriented cone-flux example.

Run: python make_cone_flux_figures.py
Coordinates are dimensionless. No data, randomness, or uncertainty is used.
The shared sci-plot style exports 178-mm PDFs and 600-dpi PNGs.
"""
import json

import numpy as np
from matplotlib.patches import Polygon, Wedge
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import make_figures as b
from make_surface_projection_figures import project, space_arrow, space_label


def panel_letters(fig, axes, xs):
    for ax in axes:
        for artist in list(ax.texts):
            if artist.get_text() in "ABC" and len(artist.get_text()) == 1:
                artist.remove()
    for x, name in zip(xs, "ABC"):
        fig.text(x, .91, name, fontsize=10, fontweight="bold", va="top")


def coordinate_projections():
    fig, axes = b.figure(82, n=3)
    fig.subplots_adjust(left=.07, right=.98, bottom=.24, top=.83, wspace=.47)
    for ax, horizontal, domain, positive, negative in zip(
        axes[:2], ["y", "x"], ["D_x", "D_y"],
        ['$x_+:\\quad +P$', '$y_+:\\quad +Q$'],
        ['$x_-:\\quad -P$', '$y_-:\\quad -Q$'],
    ):
        ax.set(xlim=(-2.2, 2.2), ylim=(.25, 2.45), aspect="equal",
               xlabel=f"${horizontal}$", ylabel='$z$')
        ax.set_xticks([-2, 0, 2])
        ax.set_yticks([1, 2])
        ax.minorticks_off()
        ax.add_patch(Polygon([[-1, 1], [1, 1], [2, 2], [-2, 2]],
                             facecolor="#F0F4F6", edgecolor=b.GRAY,
                             lw=1.1, hatch="///"))
        b.label(ax, (0, 2.27), f"${domain}$", fs=9, box=False)
        b.label(ax, (0, 1.78), positive, color=b.BLUE, fs=7)
        b.label(ax, (0, 1.27), negative, color=b.ORANGE, fs=7)

    ax = axes[2]
    ax.set(xlim=(-2.2, 2.2), ylim=(-2.2, 2.2), aspect="equal",
           xlabel='$x$', ylabel='$y$')
    ax.set_xticks([-2, 0, 2])
    ax.set_yticks([-2, 0, 2])
    ax.minorticks_off()
    ax.add_patch(Wedge((0, 0), 2, 0, 360, width=1,
                       facecolor="#F0F4F6", edgecolor=b.GRAY, lw=1.1, hatch="///"))
    b.label(ax, (0, 1.53), '$D$', fs=9)
    b.label(ax, (0, 0), '$-\\mathrm{d}A_{xy}$', color=b.ORANGE, fs=8, box=False)

    panel_letters(fig, axes, [.04, .37, .71])
    for x, formula in zip([.20, .53, .85],
                          ['$\\mathrm{d}y\\,\\mathrm{d}z=\\frac{x}{r}\\,\\mathrm{d}A_{xy}$',
                           '$\\mathrm{d}z\\,\\mathrm{d}x=\\frac{y}{r}\\,\\mathrm{d}A_{xy}$',
                           '$\\mathrm{d}x\\,\\mathrm{d}y=-\\mathrm{d}A_{xy}$']):
        fig.text(x, .07, formula, ha="center", fontsize=8)
    b.save(fig, "fig-25-cone-coordinate-projections",
           "A、B 为 yz、zx 投影，分别按 x、y 的正负分片；B 横轴 x、纵轴 z。C 为向下定向的圆环投影。")


def space_curve(ax, xyz, **kwargs):
    ax.plot(*project(xyz).T, **kwargs)


def cone_geometry(ax):
    b.plane(ax, (-2.6, 3.0), (-1.55, 2.9), ticks=False)
    t = np.linspace(0, 2*np.pi, 241)
    outer = np.column_stack([2*np.cos(t), 2*np.sin(t), np.zeros_like(t)])
    inner = np.column_stack([np.cos(t[::-1]), np.sin(t[::-1]), np.zeros_like(t)])
    # Opposite winding makes the projected annulus retain its central hole.
    codes = [Path.MOVETO]+[Path.LINETO]*239+[Path.CLOSEPOLY]
    ring = Path.make_compound_path(Path(project(outer), codes),
                                   Path(project(inner), codes))
    ax.add_patch(PathPatch(ring, facecolor="#FBEFE7", edgecolor=b.GRAY,
                           lw=.6, hatch="///", zorder=1))
    a = -np.pi/6
    front_t = np.linspace(a, a+np.pi, 121)
    low = np.column_stack([np.cos(front_t), np.sin(front_t), np.ones_like(front_t)])
    high = 2*low
    ax.add_patch(Polygon(project(np.vstack([low, high[::-1]])),
                         facecolor="#E5F0F6", edgecolor="none", zorder=4))
    for r in [1, 2]:
        full = np.column_stack([r*np.cos(t), r*np.sin(t), r*np.ones_like(t)])
        front = np.column_stack([r*np.cos(front_t), r*np.sin(front_t),
                                  r*np.ones_like(front_t)])
        space_curve(ax, full, color=b.GRAY, lw=.9, ls=b.DASH, zorder=5)
        space_curve(ax, front, color=b.BLUE, lw=1.3, zorder=6)
        for theta in [a, a+np.pi]:
            point = np.array([r*np.cos(theta), r*np.sin(theta), r])
            shadow = point.copy()
            shadow[2] = 0
            space_curve(ax, [point, shadow], color=b.GRAY, lw=.7,
                        ls=b.DASH, zorder=2)
    for theta in [a, a+np.pi]:
        p = np.array([np.cos(theta), np.sin(theta), 1])
        space_curve(ax, [p, 2*p], color=b.BLUE, lw=1.3, zorder=7)
    p = 1.55*np.array([np.cos(a), np.sin(a), 1])
    normal = np.array([np.cos(a), np.sin(a), -1])/np.sqrt(2)
    assert np.isclose(np.linalg.norm(normal), 1)
    assert np.isclose(np.dot(p, normal), 0)
    space_arrow(ax, p, p+.95*normal, color=b.BLUE, lw=1.6, size=9)
    space_label(ax, p+.95*normal, '$\\mathbf{n}$', offset=(.18, -.06), color=b.BLUE)
    space_label(ax, [.8, .8*np.sqrt(3), 1.6], '$\\Sigma$',
                offset=(0, .04), color=b.BLUE)
    space_label(ax, [.8, .8*np.sqrt(3), 0], '$D$',
                offset=(0, -.05), color=b.ORANGE)
    space_label(ax, [-1, 0, 1], '$z=r=1$', offset=(-.36, .18), fs=7)
    space_label(ax, [-2, 0, 2], '$z=r=2$', offset=(-.23, .14), fs=7)


def meridian(ax):
    ax.set(xlim=(.25, 2.85), ylim=(.25, 2.85), aspect="equal",
           xlabel='$r$ (dimensionless)', ylabel='$z$ (dimensionless)')
    ax.set_xticks([1, 2])
    ax.set_yticks([1, 2])
    ax.minorticks_off()
    ax.plot([.55, 2.55], [.55, 2.55], color=b.GRAY, lw=.8, ls=b.DASH)
    ax.plot([1, 2], [1, 2], color=b.BLUE, lw=1.5)
    p = np.array([1.35, 1.35])
    normal = np.array([1., -1.])/np.sqrt(2)
    h = np.array([2*p[0], p[1]])
    h_normal = np.dot(h, normal)*normal
    h_tangent = h-h_normal
    assert np.isclose(np.dot(h_tangent, normal), 0)
    assert np.isclose(np.dot(h, normal), p[0]/np.sqrt(2))
    scale = .4
    corner = p+scale*h_normal
    end = p+scale*h
    ax.plot(*np.array([p, p+.95*normal]).T, color=b.BLUE, lw=.8, ls=b.DASH)
    b.arrow(ax, p, end, color=b.ORANGE, lw=1.8, size=9)
    b.arrow(ax, p, corner, color=b.BLUE, lw=1.8, size=9)
    b.arrow(ax, corner, end, color=b.GRAY, ls=b.DASH, lw=1, size=8)
    tangent_unit = h_tangent/np.linalg.norm(h_tangent)
    square = np.array([corner-.075*normal,
                       corner-.075*normal+.075*tangent_unit,
                       corner+.075*tangent_unit])
    ax.plot(*square.T, color=b.GRAY, lw=.7)
    ax.plot(*p, "o", color="black", ms=3, zorder=21)
    b.label(ax, (.92, 1.82), '$\\mathbf{G}\\parallel\\Sigma$', color=b.GRAY, fs=8)
    b.label(ax, (2.54, 2.01), '$\\mathbf{H}$', color=b.ORANGE)
    b.label(ax, (1.77, .98), '$F_n\\mathbf{n}$', color=b.BLUE)
    b.label(ax, (2.48, 1.42), '$\\mathbf{H}_{\\rm tan}$', color=b.GRAY, fs=7)
    b.label(ax, (2.15, .67), '$\\mathbf{n}$', color=b.BLUE)
    b.label(ax, (2.26, 2.61), '$z=r$', color=b.BLUE, fs=8)


def normal_projection():
    fig, axes = b.figure(94, n=2)
    fig.subplots_adjust(left=.055, right=.97, bottom=.24, top=.85, wspace=.35)
    cone_geometry(axes[0])
    meridian(axes[1])
    panel_letters(fig, axes, [.04, .54])
    fig.text(.26, .075, '$\\mathbf{n}=\\frac{1}{\\sqrt{2}}(x/r,\\,y/r,\\,-1)$',
             ha="center", fontsize=8)
    fig.text(.76, .075, '$F_n=r/\\sqrt{2},\\quad \\mathrm{d}S=\\sqrt{2}\\,\\mathrm{d}A_{xy}$',
             ha="center", fontsize=8)
    b.save(fig, "fig-26-cone-normal-projection",
           "A 为无底盖的圆锥截段及圆环投影；B 为 y=0、x>0 截面内 H 的实际法向、切向分解，向量同比缩放。")


if __name__ == "__main__":
    coordinate_projections()
    normal_projection()
    b.ss.grayscale_check([b.BLUE, b.ORANGE])
    print("[note] direct labels, arrow direction, hatching and dashed tangents distinguish roles")
    (b.HERE / "figure_manifest_cone_flux.json").write_text(
        json.dumps(b.EXPORTS, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
