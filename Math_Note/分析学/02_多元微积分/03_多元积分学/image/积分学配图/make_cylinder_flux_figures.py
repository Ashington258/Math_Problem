"""Cylinder-flux example: coordinate shadows and field-normal projection.

Run: python make_cylinder_flux_figures.py
Geometry uses coordinates divided by R; the field decomposition uses R=1.
Exports two 178-mm vector PDFs and 600-dpi PNGs with the shared sci-plot style.
No measured data, randomness, or uncertainty is represented.
"""
import json

import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle

import make_figures as b
from make_surface_projection_figures import project, space_arrow, space_label


def domain_axes(ax, horizontal, vertical, disk=False):
    ax.set(xlim=(-1.12, 1.12), ylim=(-1.12, 1.12), aspect="equal",
           xlabel=horizontal, ylabel=vertical)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.minorticks_off()
    patch = (Circle((0, 0), 1) if disk else Rectangle((-1, -1), 2, 2))
    patch.set(facecolor="#F0F4F6", edgecolor=b.GRAY, linewidth=1.1,
              hatch="///")
    ax.add_patch(patch)


def coordinate_projections():
    fig, axes = b.figure(82, n=3)
    fig.subplots_adjust(left=.075, right=.98, bottom=.28, top=.85, wspace=.49)

    ax = axes[0]
    domain_axes(ax, '$y/R$', '$z/R$')
    b.label(ax, (0, .70), '$D_x$', fs=9)
    b.label(ax, (0, .24), '$x_+:\\quad +P(x_+)>0$', color=b.BLUE, fs=7)
    b.label(ax, (0, -.25), '$x_-:\\quad -P(x_-)>0$', color=b.ORANGE, fs=7)
    # Both sheets cover the whole rectangle; these labels do not partition it.
    b.footer(ax, '$I_x=\\pi^2R/2$', y=-.48)

    ax = axes[1]
    domain_axes(ax, '$z/R$', '$x/R$')
    b.label(ax, (0, .70), '$D_y$', fs=9)
    b.label(ax, (0, .15), '$y_+,\\ y_-$', fs=8)
    b.label(ax, (0, -.35), '$Q\\equiv0$', fs=10)
    b.footer(ax, '$I_y=0$', y=-.48)

    ax = axes[2]
    domain_axes(ax, '$x/R$', '$y/R$', disk=True)
    b.label(ax, (0, .66), '$D_z$', fs=9)
    b.label(ax, (0, .18), '$S_+:\\quad +W$', color=b.BLUE)
    b.label(ax, (0, -.29), '$S_-:\\quad -W$', color=b.ORANGE)
    b.footer(ax, '$I_z=I_++I_-=0$', y=-.48)

    b.save(fig, "fig-23-cylinder-coordinate-projections",
           "坐标以 R 归一化；左右半柱面重叠投到 D_x，y 向场分量为零，两底重叠投到 D_z 并相消。")


def cylinder(ax):
    b.plane(ax, (-1.62, 1.62), (-1.65, 1.95), ticks=False)
    t = np.linspace(0, 2*np.pi, 241)
    top = np.column_stack((np.cos(t), np.sin(t), np.ones_like(t)))
    bottom = top.copy()
    bottom[:, 2] = -1
    # Orthographic outline of a circular cylinder; the vertical silhouettes
    # occur at extrema of the camera's horizontal coordinate.
    a = np.arctan2(-.5, np.sqrt(3)/2)
    e = np.array([np.cos(a), np.sin(a), 0.])
    front_t = np.linspace(a, a+np.pi, 121)
    front_bottom = np.column_stack((np.cos(front_t), np.sin(front_t),
                                    -np.ones_like(front_t)))
    front_top = front_bottom.copy()
    front_top[:, 2] = 1
    side = np.vstack([front_top, front_bottom[::-1]])
    ax.add_patch(Polygon(project(side), facecolor="#F4F7F9", edgecolor="none"))
    ax.plot(*project(bottom).T, color=b.GRAY, lw=1, ls=b.DASH)
    ax.plot(*project(front_bottom).T, color=b.BLUE, lw=1.2)
    for sign in [-1, 1]:
        pts = np.array([sign*e+[0, 0, -1], sign*e+[0, 0, 1]])
        ax.plot(*project(pts).T, color=b.BLUE, lw=1.2)
    ax.add_patch(Polygon(project(top), facecolor="#E5F0F6",
                         edgecolor=b.BLUE, lw=1.2))
    for p, q, name, offset in [
        ([0, 0, 1], [0, 0, 1.72], '$(0,0,1)$', (.43, .08)),
        ([0, 0, -1], [0, 0, -1.72], '$(0,0,-1)$', (.47, -.04)),
        (e, 1.55*e, '$\\mathbf{n}_c$', (.13, -.04)),
    ]:
        space_arrow(ax, p, q, color=b.BLUE, ls=b.DASH, lw=1.3, size=8)
        space_label(ax, q, name, offset=offset, color=b.BLUE, box=False)
    space_label(ax, [0, -.5, 1], '$S_+$', offset=(.0, .10))
    space_label(ax, [0, -.5, -1], '$S_-$', offset=(.0, -.18))
    space_label(ax, [.4, -.8, 0], '$S_c$', offset=(.0, .03))
    b.footer(ax, '$\\mathbf{n}_c=(\\cos\\theta,\\sin\\theta,0)$', y=-.14)


def side_decomposition(ax):
    # At z=0 and R=1 the ACTUAL field is (x, 0, 0).
    ax.set(xlim=(-1.18, 2.13), ylim=(-1.17, 1.85), aspect="equal",
           xlabel='$x/R$', ylabel='$y/R$')
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.minorticks_off()
    ax.add_patch(Circle((0, 0), 1, facecolor="#F5F7F9", edgecolor=b.GRAY, lw=1))
    theta = np.deg2rad(40)
    p = np.array([np.cos(theta), np.sin(theta)])
    normal = p.copy()
    field = np.array([p[0], 0])
    fn_vector = np.dot(field, normal) * normal
    tangent = field-fn_vector
    assert np.isclose(np.dot(tangent, normal), 0)
    assert np.allclose(fn_vector+tangent, field)
    ax.plot(*np.array([[0, 0], 1.82*normal]).T, color=b.BLUE, lw=.8, ls=b.DASH)
    ax.plot(*np.array([p-.50*np.array([-p[1], p[0]]),
                       p+.65*np.array([-p[1], p[0]])]).T,
            color=b.GRAY, lw=.7, ls=b.DASH)
    b.arrow(ax, p, p+field, color=b.ORANGE, lw=1.8, size=8)
    b.arrow(ax, p, p+fn_vector, color=b.BLUE, lw=1.8, size=8)
    b.arrow(ax, p+fn_vector, p+field, color=b.GRAY, ls=b.DASH, lw=1, size=7)
    t_unit = tangent/np.linalg.norm(tangent)
    corner = p+fn_vector
    square = np.array([corner-.09*normal,
                       corner-.09*normal+.09*t_unit,
                       corner+.09*t_unit])
    ax.plot(*square.T, color=b.GRAY, lw=.7)
    ax.plot(*p, "o", color="black", ms=3, zorder=21)
    b.label(ax, (-.52, .63), '$z=0$', fs=8)
    b.label(ax, p+field+[.12, -.14], '$\\mathbf{F}$', color=b.ORANGE)
    b.label(ax, (.76, 1.36), '$F_n\\mathbf{n}$', color=b.BLUE)
    b.label(ax, p+.72*field+[.36, .18], '$\\mathbf{F}_{\\rm tan}$', color=b.GRAY, fs=7)
    b.label(ax, (1.65, 1.34), '$\\mathbf{n}$', color=b.BLUE)
    b.footer(ax, '$F_n=\\dfrac{R\\cos^2\\theta}{R^2+z^2}\\geq0$', y=-.38)


def cap_components(ax):
    ax.set(xlim=(-1.18, 1.18), ylim=(-1.85, 1.85), aspect="equal",
           xlabel='$x/R$', ylabel='$z/R$')
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.minorticks_off()
    ax.plot([-1, -1], [-1, 1], color=b.GRAY, lw=.7, ls=b.DASH)
    ax.plot([1, 1], [-1, 1], color=b.GRAY, lw=.7, ls=b.DASH)
    for z in [1, -1]:
        ax.plot([-1, 1], [z, z], color=b.BLUE, lw=1.4)
        b.arrow(ax, (-.38, z), (-.38, z+.58*z), color=b.BLUE,
                ls=b.DASH, lw=1.2, size=8)
        # W is even in z, so the vertical field points up on BOTH caps.
        b.arrow(ax, (.40, z), (.40, z+.58), color=b.ORANGE, lw=1.8, size=8)
    b.label(ax, (-.38, 1.73), '$(0,0,1)$', color=b.BLUE, fs=7, box=False)
    b.label(ax, (-.38, -1.75), '$(0,0,-1)$', color=b.BLUE, fs=7, box=False)
    b.label(ax, (.47, .72), '$(0,0,W)$', color=b.ORANGE, fs=7, box=False)
    b.label(ax, (-.38, -.65), '$(0,0,W)$', color=b.ORANGE, fs=7, box=False)
    b.label(ax, (0, .42), '$F_{n,+}=+W$', fs=7)
    b.label(ax, (0, -.12), '$F_{n,-}=-W$', fs=7)
    b.footer(ax, '$I_\\pm=\\pm\\pi R^2\\ln2$', y=-.31)


def normal_projection():
    fig, axes = b.figure(92, n=3)
    fig.subplots_adjust(left=.055, right=.97, bottom=.28, top=.85, wspace=.43)
    cylinder(axes[0])
    side_decomposition(axes[1])
    cap_components(axes[2])
    # Equal-aspect panels have different heights. Anchor letters to the canvas.
    for ax in axes:
        for artist in list(ax.texts):
            if artist.get_text() in ["A", "B", "C"]:
                artist.remove()
    for x, name in zip([.04, .37, .72], "ABC"):
        fig.text(x, .91, name, fontsize=10, fontweight="bold", va="top")
    b.save(fig, "fig-24-cylinder-normal-projection",
           "A 为圆柱三片的外法向；B 为 R=1、z=0 侧面截面的实际场分解；C 仅画两底的竖直场分量。")


if __name__ == "__main__":
    coordinate_projections()
    normal_projection()
    b.ss.grayscale_check([b.BLUE, b.ORANGE])
    print("[note] normal/tangent distinguished by dashed lines and direct labels")
    (b.HERE / "figure_manifest_cylinder_flux.json").write_text(
        json.dumps(b.EXPORTS, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
