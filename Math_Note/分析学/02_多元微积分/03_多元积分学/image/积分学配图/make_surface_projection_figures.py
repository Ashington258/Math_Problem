"""Surface-area projections and field-normal projection, from exact geometry.

Run: python make_surface_projection_figures.py
Exports 178-mm vector PDFs and 600-dpi PNGs using the shared note style.
All geometry is dimensionless; micro-elements are enlarged for visibility.
"""
import json

import numpy as np
from matplotlib.patches import Polygon, Arc

import make_figures as b


def project(points):
    """Orthographic camera viewing the positive octant from above."""
    camera = np.array([[np.sqrt(3)/2, -.5, 0],
                       [-.25, -np.sqrt(3)/4, np.sqrt(3)/2]])
    assert np.allclose(camera @ camera.T, np.eye(2))
    return np.asarray(points, dtype=float) @ camera.T


def space_arrow(ax, p, q, **kwargs):
    b.arrow(ax, *project([p, q]), **kwargs)


def space_label(ax, p, text, offset=(0, 0), **kwargs):
    b.label(ax, project(p) + np.asarray(offset), text, **kwargs)


def space_axes(ax):
    for end, name, offset in [([1.25, 0, 0], '$x$', (.08, 0)),
                              ([0, 1.25, 0], '$y$', (-.08, 0)),
                              ([0, 0, 1.25], '$z$', (.07, .03))]:
        space_arrow(ax, [0, 0, 0], end, color=b.GRAY, lw=.7, size=6, z=1)
        space_label(ax, end, name, offset, color=b.GRAY, box=False)


P = np.array([0.28, 0.25, 0.85])
U = np.array([0.70, 0.0, -0.28])
V = np.array([0.0, 0.62, -0.31])
PATCH = np.array([P, P + U, P + U + V, P + V])
AREA_VECTOR = np.cross(U, V)
AREA = np.linalg.norm(AREA_VECTOR)
NORMAL = AREA_VECTOR / AREA
CENTER = PATCH.mean(axis=0)


def surface(ax):
    ax.add_patch(Polygon(project(PATCH), facecolor="#E5F0F6",
                         edgecolor=b.BLUE, lw=1.4, zorder=4))


def coordinate_projections():
    fig, axes = b.figure(82, n=3)
    fig.subplots_adjust(left=.045, right=.97, bottom=.27, top=.90, wspace=.14)
    names = ("x", "y", "z")
    elements = (r"dy\,dz", r"dz\,dx", r"dx\,dy")
    offsets = ((-.16, -.08), (.15, -.08), (.05, -.17))
    for i, ax in enumerate(axes):
        b.plane(ax, (-.78, 1.25), (-.80, 1.20), ticks=False)
        projected = PATCH.copy()
        projected[:, i] = 0
        # This projected cross product measures the actual shadow area.
        shadow_vector = np.cross(projected[1] - projected[0],
                                 projected[3] - projected[0])
        assert np.isclose(np.linalg.norm(shadow_vector), abs(AREA_VECTOR[i]))
        assert np.isclose(AREA_VECTOR[i], NORMAL[i] * AREA)
        ax.add_patch(Polygon(project(projected), facecolor="#FBE8DA",
                             edgecolor=b.ORANGE, lw=1.2, hatch="///", zorder=2))
        for p, q in zip(PATCH, projected):
            ax.plot(*project([p, q]).T, color=b.GRAY, lw=.8, ls=b.DASH, zorder=3)
        surface(ax)
        # A single stronger arrow explicitly gives the projection direction.
        space_arrow(ax, CENTER, projected.mean(axis=0), color=b.ORANGE,
                      lw=1.3, size=7, ls=b.DASH, z=6)
        space_axes(ax)
        space_label(ax, PATCH[0], '$\\mathrm{d}S$', offset=(.02, .15),
                      color=b.BLUE, box=False)
        space_label(ax, projected.mean(axis=0), f"$D_{names[i]}$",
                    offset=offsets[i], color=b.ORANGE, box=True)
        b.footer(ax, '$' + elements[i] + "=n_" + names[i] + '\\,\\mathrm{d}S$', y=-.12)
    fig.text(.5, .065, '$\\mathrm{d}\\mathbf{S}=(\\mathrm{d}y\\,\\mathrm{d}z,\\,\\mathrm{d}z\\,\\mathrm{d}x,\\,\\mathrm{d}x\\,\\mathrm{d}y)'
             '=(n_x,n_y,n_z)\\,\\mathrm{d}S\\qquad(n_x,n_y,n_z>0)$',
             ha="center", fontsize=8)
    b.save(fig, "fig-21-surface-coordinate-projections",
           "同一面元沿 x、y、z 轴投影到 yz、zx、xy 平面；所选法向三分量均为正。")


def normal_projection():
    fig, axes = b.figure(88)
    fig.subplots_adjust(left=.07, right=.96, bottom=.26, top=.90, wspace=.32)
    ax = axes[0]
    b.plane(ax, (-.6, 1.35), (-.55, 1.20), ticks=False)
    surface(ax)
    space_label(ax, PATCH[3], '$\\mathrm{d}S$', offset=(-.09, .16), color=b.BLUE)
    end = CENTER + .82 * NORMAL
    space_arrow(ax, CENTER, end, color=b.BLUE, lw=2, size=10)
    space_label(ax, end, '$\\mathbf{n}$', offset=(.08, .10), color=b.BLUE)
    space_label(ax, P + U, '$S$', offset=(.12, -.06), color=b.BLUE)
    b.footer(ax, '$\\mathrm{d}\\mathbf{S}=\\mathbf{n}\\,\\mathrm{d}S$', y=-.15)

    ax = axes[1]
    b.plane(ax, (-1.0, 1.10), (-.72, 1.48), ticks=False)
    origin = np.zeros(2)
    normal = np.array([.6, .8])
    tangent = np.array([.8, -.6])
    field = np.array([.10, 1.20])
    fn = np.dot(field, normal)
    fn_vector = fn * normal
    tangent_vector = field - fn_vector
    assert np.isclose(np.dot(tangent_vector, normal), 0)
    assert np.allclose(fn_vector + tangent_vector, field)
    ax.plot(*np.array([-.95*tangent, 1.0*tangent]).T, color=b.BLUE, lw=1.5)
    # Dashed normal line, solid field projection, dashed tangential remainder.
    ax.plot(*np.array([-.30*normal, 1.50*normal]).T,
            color=b.GRAY, lw=.9, ls=b.DASH)
    b.arrow(ax, origin, fn_vector, color=b.BLUE, lw=2, size=10)
    b.arrow(ax, origin, field, color=b.ORANGE, lw=1.8, size=10)
    b.arrow(ax, fn_vector, field, color=b.GRAY, ls=b.DASH, lw=1.1, size=7)
    # The right-angle marker lies between the normal and tangential directions.
    r = .09
    square = np.array([fn_vector-r*normal,
                       fn_vector-r*normal-r*tangent,
                       fn_vector-r*tangent])
    ax.plot(*square.T, color=b.GRAY, lw=.8)
    theta_n = np.degrees(np.arctan2(normal[1], normal[0]))
    theta_f = np.degrees(np.arctan2(field[1], field[0]))
    ax.add_patch(Arc(origin, .65, .65, theta1=theta_n, theta2=theta_f,
                     color=b.GRAY, lw=.8))
    b.label(ax, (.13, .41), '$\\theta$', color=b.GRAY, box=False)
    b.label(ax, field + [-.10, .10], '$\\mathbf{F}$', color=b.ORANGE)
    b.label(ax, (.91, .77), '$F_n\\mathbf{n}$', color=b.BLUE)
    b.label(ax, (.43, 1.30), '$\\mathbf{F}_{\\mathrm{tan}}$', color=b.GRAY)
    b.label(ax, (.94, 1.24), '$\\mathbf{n}$', color=b.GRAY, box=False)
    b.label(ax, (.70, -.67), '$S$', color=b.BLUE)
    ax.plot(0, 0, "o", color="black", ms=3, zorder=20)
    b.footer(ax, '$F_n=\\mathbf{F}\\cdot\\mathbf{n}=\\|\\mathbf{F}\\|\\cos\\theta$',
             y=-.15)
    fig.text(.5, .065,
             '$\\mathbf{F}\\cdot \\mathrm{d}\\mathbf{S}=(\\mathbf{F}\\cdot\\mathbf{n})\\,\\mathrm{d}S'
             '=F_n\\,\\mathrm{d}S$', ha="center", fontsize=8)
    b.save(fig, "fig-22-surface-normal-projection",
           "A 为面元的法向定向，箭头仅示单位法向；B 为场与法向所在截面中的正交分解。")


if __name__ == "__main__":
    coordinate_projections()
    normal_projection()
    b.ss.grayscale_check([b.BLUE, b.ORANGE])
    (b.HERE / "figure_manifest_surface_projections.json").write_text(
        json.dumps(b.EXPORTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[ok] projected areas, direction cosines, and normal decomposition")
