"""Reproduce line and plane position diagrams: python make_figures.py.

Dependencies: Python >= 3.10, numpy, matplotlib, Pillow.
Geometry is exact in R^3; only the display uses an oblique projection.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np
from PIL import Image, ImageOps

import sci_style as ss

OUT = Path(__file__).resolve().parent
BLUE, ORANGE, INK = "#0072B2", "#D55E00", "#222222"
PROJECTION = np.array([[1., .4, 0.], [0., .65, 1.]])

ss.apply("double", font_size=10, line_width=1.6)
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "Noto Sans CJK SC", "DejaVu Sans"],
    "mathtext.fontset": "dejavusans",
    "svg.fonttype": "path",  # Portable Chinese glyphs, independent of viewer fonts.
    "savefig.pad_inches": 0,
    "svg.hashsalt": "line-position-v1",
})


def project(p):
    return np.asarray(p) @ PROJECTION.T


def canvas():
    fig = plt.figure(figsize=ss.figsize("double", height_mm=100))
    # Retain the exact journal width even with bbox_inches='tight'.
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             facecolor="white", edgecolor="none", zorder=-100))
    ax = fig.add_axes([.025, .12, .70, .82])
    ax.set(xlim=(-3.7, 3.7), ylim=(-1.65, 3.0), aspect="equal")
    ax.axis("off")
    return fig, ax


def label(ax, p, text, offset=(0, 9), color=INK, **kwargs):
    return ax.annotate(text, project(p), xytext=offset, textcoords="offset points",
                       ha="center", va="center", color=color, fontsize=11,
                       zorder=12, **kwargs)


def segment(ax, a, b, **kwargs):
    q = project([a, b])
    ax.plot(q[:, 0], q[:, 1], **kwargs)


def arrow(ax, a, b, color=INK, width=1.9, style="-", zorder=7):
    ax.annotate("", xy=project(b), xytext=project(a), zorder=zorder,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=13,
                                linewidth=width, color=color, linestyle=style,
                                shrinkA=0, shrinkB=0))


def plane(ax):
    corners = np.array([[-2.65, -1.8, 0], [2.65, -1.8, 0],
                        [2.65, 1.8, 0], [-2.65, 1.8, 0]])
    ax.add_patch(Polygon(project(corners), facecolor="#F1F4F6",
                         edgecolor="#A3AAB0", lw=.8, zorder=0))
    label(ax, [2.35, -1.5, 0], r"$\Pi$", offset=(0, 0), color="#626970")


def base_point(ax, p, index, offset):
    color = (BLUE, ORANGE)[index]
    q = project(p)
    ax.plot(*q, marker=("o", "s")[index], ms=6, mec=color, mfc="white",
            mew=1.5, zorder=10)
    label(ax, p, rf"$\mathbf{{p}}_{index}$", offset, color)


def direction(ax, p, d, index, offset):
    color = (BLUE, ORANGE)[index]
    arrow(ax, p, p + d, color, 2.6)
    label(ax, p + .58 * d, rf"$\mathbf{{d}}_{index}$", offset, color)


def displacement(ax, p0, p1, offset=(0, 0)):
    arrow(ax, p1, p0, width=1.6, style="-.", zorder=5)
    label(ax, .5 * (p0 + p1), r"$\mathbf{p}_0-\mathbf{p}_1$", offset)


def relation(fig, rank, lines):
    fig.text(.775, .73, f"$r={rank}$", fontsize=17, weight="bold")
    for y, text in zip([.59, .47, .35, .23], lines):
        fig.text(.75, y, text, fontsize=10, va="center")


def footer(fig, text):
    fig.text(.04, .055, text, fontsize=8, color="#555555")


def export(fig, stem):
    ss.save(fig, OUT / f"{stem}.pdf", also_png=True)
    ss.save(fig, OUT / f"{stem}.svg")
    size = ss.output_size_mm(OUT / f"{stem}.pdf")
    assert size and abs(size[0] - 178) < .2, size
    plt.close(fig)
    with Image.open(OUT / f"{stem}.png") as im:
        thumb = ImageOps.grayscale(im).convert("RGB")
        thumb.thumbnail((1000, 565))
        return thumb.copy()


def geometry(p0, p1, d0, d1, rank):
    """Verify each example against the classification shown in the note."""
    vectors = [np.array(v, dtype=float) for v in (p0, p1, d0, d1)]
    p0, p1, d0, d1 = vectors
    assert np.linalg.norm(d0) > 0 and np.linalg.norm(d1) > 0
    assert np.linalg.matrix_rank(np.column_stack((p0 - p1, d0, d1))) == rank
    return vectors


def skew():
    p0, p1, d0, d1 = geometry([-1.5, -.4, 0], [.1, -.6, 1.65],
                             [1.4, 0, 0], [-.9, 1.1, 0], 3)
    fig, ax = canvas()
    plane(ax)
    q1 = p1 * [1, 1, 0]
    segment(ax, q1, p1, color="#8C9399", lw=1, ls=(0, (2, 3)), zorder=1)
    segment(ax, q1 - 1.4*d1, q1 + 1.45*d1,
            color="#9AA2A9", lw=1, ls=(0, (2, 3)), zorder=1)
    segment(ax, [-2.8, -.4, 0], [2.65, -.4, 0], color=BLUE, lw=1.6)
    segment(ax, p1 - 1.3*d1, p1 + 1.55*d1, color=ORANGE, lw=1.6, ls="--")
    displacement(ax, p0, p1, (-37, 4))
    direction(ax, p0, d0, 0, (0, -15))
    direction(ax, p1, d1, 1, (-19, 4))
    base_point(ax, p0, 0, (-12, -15))
    base_point(ax, p1, 1, (19, -1))
    label(ax, [2.65, -.4, 0], "$L_0$", (7, 11), BLUE)
    label(ax, p1 + 1.55*d1, "$L_1$", (15, 0), ORANGE)
    label(ax, q1, "$q_1$", (15, -10), "#626970")
    relation(fig, 3, [r"$\mathbf{d}_0\times\mathbf{d}_1\ne\mathbf{0}$",
                     r"$(\mathbf{p}_0-\mathbf{p}_1)\cdot$",
                     r"$\quad(\mathbf{d}_0\times\mathbf{d}_1)\ne 0$",
                     "两直线不共面"])
    footer(fig, r"空间斜投影；灰色虚线为辅助投影，$L_0$ 位于 $\Pi$ 内，$L_1$ 位于 $\Pi$ 上方且平行于 $\Pi$。")
    return export(fig, "fig-01-skew-lines")


def parallel():
    p0, p1, d0, d1 = geometry([-1.5, -.7, 0], [-.7, 1.15, 0],
                             [1.3, 0, 0], [1.3, 0, 0], 2)
    fig, ax = canvas()
    plane(ax)
    for i, (p, d, color) in enumerate([(p0, d0, BLUE), (p1, d1, ORANGE)]):
        segment(ax, [-2.65, p[1], 0], [2.65, p[1], 0],
                color=color, lw=1.6, ls=("-", "--")[i])
        direction(ax, p, d, i, (0, (-16, 15)[i]))
        base_point(ax, p, i, (-14, (-13, 14)[i]))
        label(ax, [2.65, p[1], 0], f"$L_{i}$", (0, 12), color)
    displacement(ax, p0, p1, (-39, 3))
    relation(fig, 2, [r"$\mathbf{d}_0\times\mathbf{d}_1=\mathbf{0}$",
                     r"$(\mathbf{p}_0-\mathbf{p}_1)$",
                     r"$\quad\notin\operatorname{span}\{\mathbf{d}_0\}$",
                     "共面，无公共点"])
    footer(fig, "浅灰区域表示共同平面 Π；两条直线平行且不重合。")
    return export(fig, "fig-02-parallel-lines")


def intersecting():
    p0, p1, d0, d1 = geometry([-1.7, -.6, 0], [-1.35, 1.1, 0],
                             [1.4, .45, 0], [1.2, -1, 0], 2)
    t, s = np.linalg.lstsq(np.column_stack((d0, -d1)), p1 - p0, rcond=None)[0]
    c = p0 + t*d0
    assert np.allclose(c, p1 + s*d1)
    fig, ax = canvas()
    plane(ax)
    for i, (p, d, end, color) in enumerate([(p0, d0, 2.8, BLUE),
                                            (p1, d1, 2.7, ORANGE)]):
        segment(ax, p - .65*d, p + end*d, color=color, lw=1.6, ls=("-", "--")[i])
        direction(ax, p, d, i, ((3, -17), (13, 13))[i])
        base_point(ax, p, i, ((-10, -16), (-8, 16))[i])
        label(ax, p + end*d, f"$L_{i}$", (8, 8), color)
    displacement(ax, p0, p1, (-40, 0))
    ax.plot(*project(c), "D", color=INK, ms=5, zorder=11)
    label(ax, c, "$C$", (13, 12))
    relation(fig, 2, [r"$\mathbf{d}_0\times\mathbf{d}_1\ne\mathbf{0}$",
                     r"$C=\mathbf{p}_0+t_*\mathbf{d}_0$",
                     r"$\quad=\mathbf{p}_1+s_*\mathbf{d}_1$",
                     "共面，唯一交点 C"])
    footer(fig, "浅灰区域表示共同平面 Π；菱形标记为交点 C，两个参数 t*、s* 独立取值。")
    return export(fig, "fig-03-intersecting-lines")


def coincident():
    p0, p1, d0, d1 = geometry([-1.6, 0, 0], [1.1, 0, 0],
                             [1.2, 0, 0], [-.9, 0, 0], 1)
    fig, ax = canvas()
    ax.set_ylim(-2.0, 2.65)
    segment(ax, [-3, 0, 0], [3, 0, 0], color=BLUE, lw=2.5)
    segment(ax, [-3, 0, 0], [3, 0, 0], color=ORANGE, lw=1.4, ls="--")
    direction(ax, p0, d0, 0, (0, -19))
    direction(ax, p1, d1, 1, (0, -19))
    base_point(ax, p0, 0, (-9, -18))
    base_point(ax, p1, 1, (9, -18))
    shift = np.array([0, 0, 1.0])
    for p in (p0, p1):
        segment(ax, p, p+shift, color="#9AA2A9", lw=.8, ls=":")
    displacement(ax, p0+shift, p1+shift, (0, 14))
    label(ax, [2.55, 0, 0], "$L_0=L_1$", (0, 14))
    relation(fig, 1, [r"$\mathbf{d}_0\times\mathbf{d}_1=\mathbf{0}$",
                     r"$(\mathbf{p}_0-\mathbf{p}_1)$",
                     r"$\quad\in\operatorname{span}\{\mathbf{d}_0\}$",
                     "公共点为整条直线"])
    footer(fig, "位移向量向上平移展示，竖直虚线连接其原始端点；方向向量可以反向。")
    return export(fig, "fig-04-coincident-lines")


def main():
    ss.grayscale_check([BLUE, ORANGE, INK])
    print("[note] Lines use solid/dashed strokes; base points use circles/squares.")
    previews = [skew(), parallel(), intersecting(), coincident()]
    sheet = Image.new("RGB", (2000, 1130), "white")
    for i, im in enumerate(previews):
        sheet.paste(im, ((i % 2)*1000, (i // 2)*565))
    sheet.save(OUT / "preview-grayscale.png")
    print("[ok] Geometry ranks, intersection and exported widths verified.")
    from make_plane_figures import main as make_planes
    make_planes()


if __name__ == "__main__":
    main()
