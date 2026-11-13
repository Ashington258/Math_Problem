"""Reproduce seven three-plane configurations; coordinates are dimensionless."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np
from PIL import Image, ImageOps

import sci_style as ss

OUT = Path(__file__).resolve().parent
COLORS = ["#0072B2", "#D55E00", "#009E73"]
STYLES = ["-", "--", "-."]
MARKERS = ["o", "s", "^"]
az, el = np.deg2rad([32, 22])
P = np.array([[np.cos(az), -np.sin(az), 0],
              [np.sin(az)*np.sin(el), np.cos(az)*np.sin(el), np.cos(el)]])


def project(p):
    return np.asarray(p) @ P.T


def label(ax, p, text, offset=(0, 10), color="#222222", size=11):
    ax.annotate(text, project(p), xytext=offset, textcoords="offset points",
                fontsize=size, color=color, ha="center", va="center", zorder=30)


def segment(ax, a, b, **kwargs):
    xy = project([a, b])
    ax.plot(xy[:, 0], xy[:, 1], **kwargs)


def arrow(ax, a, b, color="#222222", width=2.1):
    ax.annotate("", xy=project(b), xytext=project(a), zorder=22,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=13,
                                color=color, lw=width, shrinkA=0, shrinkB=0))


def patch(ax, i, corners, name_pos=None, width=1.3):
    color = COLORS[i]
    ax.add_patch(Polygon(project(corners), facecolor=color, alpha=.065,
                         edgecolor="none", zorder=1))
    ax.add_patch(Polygon(project(corners), facecolor="none", edgecolor=color,
                         lw=width, ls=STYLES[i], zorder=3+i))
    if name_pos is not None:
        label(ax, name_pos, rf"$\Pi_{i+1}$", (0, 0), color, 12)


def point_normal(ax, i, p, n, point_offset, normal_offset):
    p, n = np.asarray(p, dtype=float), np.asarray(n, dtype=float)
    color = COLORS[i]
    arrow(ax, p, p+n, color)
    ax.plot(*project(p), marker=MARKERS[i], ms=6, mfc="white", mec=color,
            mew=1.4, zorder=25)
    label(ax, p, rf"$\mathbf{{p}}_{i+1}$", point_offset, color)
    label(ax, p+.66*n, rf"$\mathbf{{n}}_{i+1}$", normal_offset, color)


def xy(z, a=1.8, b=1.45):
    return np.array([[-a, -b, z], [a, -b, z], [a, b, z], [-a, b, z]])


def yz(x):
    return np.array([[x, -1.7, -1.4], [x, 1.7, -1.4],
                     [x, 1.7, 1.4], [x, -1.7, 1.4]])


def xz(y):
    return np.array([[-1.8, y, -1.4], [1.8, y, -1.4],
                     [1.8, y, 1.4], [-1.8, y, 1.4]])


def diagonal(k):
    return np.array([[k/2-1.3, k/2+1.3, -1.4],
                     [k/2+1.3, k/2-1.3, -1.4],
                     [k/2+1.3, k/2-1.3, 1.4],
                     [k/2-1.3, k/2+1.3, 1.4]])


def canvas(rank, augmented, equations, conclusion, foot):
    fig = plt.figure(figsize=ss.figsize("double", height_mm=100))
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             facecolor="white", edgecolor="none", zorder=-100))
    ax = fig.add_axes([.015, .13, .72, .82])
    ax.set(xlim=(-3.2, 3.2), ylim=(-2.55, 2.7), aspect="equal")
    ax.axis("off")
    fig.text(.75, .80, rf"$r={rank},\quad r'={augmented}$", fontsize=15)
    for y, eq in zip([.65, .53, .41], equations):
        fig.text(.76, y, eq, fontsize=11)
    fig.text(.75, .25, conclusion, fontsize=10)
    fig.text(.035, .055, foot, fontsize=8, color="#555555")
    return fig, ax


def intersection_line(ax, x, y, text, offset=(10, -6), common=False):
    segment(ax, [x, y, -1.7], [x, y, 1.75], color="#222222",
            lw=2.0 if common else 1.2, ls="-" if common else (0, (3, 2)), zorder=12)
    label(ax, [x, y, -1.7], text, offset, size=10)


def verify(normals, points, corners, rank, augmented, common=None, direction=None):
    a, points = np.array(normals, dtype=float), np.array(points, dtype=float)
    b = np.einsum("ij,ij->i", a, points)
    assert np.all(np.linalg.norm(a, axis=1) > 0)
    assert np.linalg.matrix_rank(a) == rank
    assert np.linalg.matrix_rank(np.column_stack((a, b))) == augmented
    for n, c, rhs in zip(a, corners, b):
        assert np.allclose(np.array(c) @ n, rhs), (n, c, rhs)
    if common is not None:
        assert np.allclose(a @ np.asarray(common), b)
    if direction is not None:
        assert np.allclose(a @ np.asarray(direction), 0)


def export(fig, stem):
    ss.save(fig, OUT / f"{stem}.pdf", also_png=True)
    ss.save(fig, OUT / f"{stem}.svg")
    assert abs(ss.output_size_mm(OUT / f"{stem}.pdf")[0]-178) < .2
    plt.close(fig)
    with Image.open(OUT / f"{stem}.png") as im:
        thumb = ImageOps.grayscale(im).convert("RGB")
        thumb.thumbnail((1000, 565))
        return thumb.copy()


def three_planes(kind):
    if kind == "point":
        corners = [yz(0), xz(0), xy(0)]
        normals = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        points = [[0, -1.25, 1], [-1.3, 0, .75], [.8, .95, 0]]
        names = [[0, 1.5, -1.25], [1.55, 0, -1.25], [1.5, -1.2, 0]]
        offsets = [((14, -9), (10, 12)), ((5, -14), (-14, 4)), ((14, -4), (12, 1))]
        rank, aug, common, direction = 3, 3, [0, 0, 0], None
        eqs = [r"$\Pi_1:\ x=0$", r"$\Pi_2:\ y=0$", r"$\Pi_3:\ z=0$"]
        conclusion = "唯一公共点 C"
        foot = "三平面以透明色块示意；圆点、方点、三角点为各平面的基点，菱形为公共点。"
        stem = "fig-05-planes-common-point"
    elif kind == "line":
        corners = [yz(0), xz(0), diagonal(0)]
        normals = [[1, 0, 0], [0, 1, 0], [.7, .7, 0]]
        points = [[0, 1.4, .35], [1.4, 0, -.65], [-1.1, 1.1, -.6]]
        names = [[0, 1.55, 1.3], [1.65, 0, 1.3], [-1.25, 1.25, -1.2]]
        offsets = [((-9, -14), (1, 13)), ((13, -8), (10, 12)), ((-12, -10), (-15, 1))]
        rank, aug, common, direction = 2, 2, [0, 0, 0], [0, 0, 1]
        eqs = [r"$\Pi_1:\ x=0$", r"$\Pi_2:\ y=0$", r"$\Pi_3:\ x+y=0$"]
        conclusion = "公共交线 L：z 轴"
        foot = r"黑色实线为三平面的公共交线；$\mathbf{d}$ 为交线方向，$\mathbf{q}_0$ 为交线上一点。"
        stem = "fig-06-planes-common-line"
    elif kind == "parallel_pair":
        corners = [yz(-1), yz(1), xz(0)]
        normals = [[-1, 0, 0], [1, 0, 0], [0, -1, 0]]
        points = [[-1, -.9, .7], [1, .9, .7], [.4, 0, -.8]]
        names = [[-1, 1.5, 1.2], [1, -1.5, 1.2], [1.6, 0, -1.25]]
        offsets = [((5, -14), (-12, 9)), ((-9, 12), (12, 7)), ((-12, -10), (12, -5))]
        rank, aug, common, direction = 2, 3, None, None
        eqs = [r"$\Pi_1:\ x=-1$", r"$\Pi_2:\ x=1$", r"$\Pi_3:\ y=0$"]
        conclusion = "两平行平面被第三平面截切"
        foot = r"$\Pi_1\parallel\Pi_2$ 且互异；$L_{13}$、$L_{23}$ 是两条不同的平行交线，无三平面公共点。"
        stem = "fig-07-planes-parallel-pair"
    elif kind == "pairwise":
        corners = [yz(0), xz(0), diagonal(1)]
        normals = [[-1, 0, 0], [0, 1, 0], [.7, .7, 0]]
        points = [[0, -1.2, .8], [-1.3, 0, -.5], [1.5, -.5, -.35]]
        names = [[0, -1.55, -1.25], [-1.55, 0, 1.15], [1.65, -.65, 1.25]]
        offsets = [((9, -14), (-10, 10)), ((10, -9), (-13, 2)), ((12, -8), (13, 4))]
        rank, aug, common, direction = 2, 3, None, None
        eqs = [r"$\Pi_1:\ x=0$", r"$\Pi_2:\ y=0$", r"$\Pi_3:\ x+y=1$"]
        conclusion = "两两相交，无公共交点"
        foot = r"三条交线 $L_{12}$、$L_{13}$、$L_{23}$ 互相平行且互异；两两相交不保证三者有公共点。"
        stem = "fig-08-planes-pairwise-intersections"
    else:
        raise ValueError(kind)
    verify(normals, points, corners, rank, aug, common, direction)
    fig, ax = canvas(rank, aug, eqs, conclusion, foot)
    for i in range(3):
        patch(ax, i, corners[i], names[i])
        point_normal(ax, i, points[i], normals[i], *offsets[i])
    if kind == "point":
        ax.plot(*project(common), "D", ms=6, color="#222222", zorder=26)
        label(ax, common, "$C$", (11, -14))
    elif kind == "line":
        intersection_line(ax, 0, 0, "$L$", (11, -4), common=True)
        q = np.array([0, 0, -.8])
        ax.plot(*project(q), "D", ms=5, color="#222222", zorder=26)
        label(ax, q, r"$\mathbf{q}_0$", (-17, -3))
        arrow(ax, q, q+np.array(direction)*1.1, width=2.8)
        label(ax, q+np.array(direction)*.65, r"$\mathbf{d}$", (13, 0))
    elif kind == "parallel_pair":
        for indices, q in [([0, 2], [-1, 0, 0]), ([1, 2], [1, 0, 0])]:
            check_pair_line(normals, points, indices, q)
        intersection_line(ax, -1, 0, "$L_{13}$", (-11, -7))
        intersection_line(ax, 1, 0, "$L_{23}$", (11, -7))
    else:
        for indices, q in [([0, 1], [0, 0, 0]), ([0, 2], [0, 1, 0]),
                           ([1, 2], [1, 0, 0])]:
            check_pair_line(normals, points, indices, q)
        intersection_line(ax, 0, 0, "$L_{12}$", (0, -10))
        intersection_line(ax, 0, 1, "$L_{13}$", (-12, -9))
        intersection_line(ax, 1, 0, "$L_{23}$", (12, -9))
    return export(fig, stem)


def check_pair_line(normals, points, indices, q):
    a, p = np.asarray(normals)[indices], np.asarray(points)[indices]
    assert np.allclose(a @ q, np.einsum("ij,ij->i", a, p))
    assert np.allclose(a @ [0, 0, 1], 0)


def parallel_planes(levels, kind):
    corners = [xy(z) for z in levels]
    if kind == "coincident":
        points = [[-1.4, -.6, 0], [.3, -.7, 0], [1, 1.1, 0]]
        normals = [[0, 0, 1], [0, 0, -.9], [0, 0, 1.1]]
        rank, aug = 1, 1
        conclusion = "公共交集为整个平面"
        stem = "fig-09-planes-coincident"
    elif kind == "two_coincident":
        points = [[-1.1, -.5, 0], [.8, -.7, 0], [.4, .9, 1.4]]
        normals = [[0, 0, 1], [0, 0, -.9], [0, 0, .85]]
        rank, aug = 1, 2
        conclusion = "两个重合，第三个平行"
        stem = "fig-10-planes-two-coincident"
    else:
        points = [[-1, -.5, -1], [1, -.5, 0], [-.3, 1, 1]]
        normals = [[0, 0, -.8], [0, 0, .9], [0, 0, 1]]
        rank, aug = 1, 2
        conclusion = "三个平行且互不重合"
        stem = "fig-11-planes-distinct-parallel"
    verify(normals, points, corners, rank, aug,
           common=[0, 0, 0] if aug == 1 else None)
    eqs = [rf"$\Pi_{i+1}:\ z={z:g}$" for i, z in enumerate(levels)]
    fig, ax = canvas(rank, aug, eqs, conclusion,
                     "法向量共线，可同向或反向；平面以有限边界示意，实际无限延伸。")
    for i in range(3):
        name_pos = [1.5, -1.3, levels[i]] if len(set(levels)) == 3 else None
        patch(ax, i, corners[i], name_pos,
              width=[2.6, 1.7, 1.1][i] if aug == 1 else [2.4, 1.4, 1.3][i])
        point_normal(ax, i, points[i], normals[i],
                     [(-12, -8), (13, 6), (13, -7)][i],
                     [(-13, 0), (13, 0), (-13, 0)][i])
    if kind == "coincident":
        label(ax, [-.4, -1.6, 0], r"$\Pi_1=\Pi_2=\Pi_3$", (0, -40), size=12)
    elif kind == "two_coincident":
        label(ax, [-.4, -1.6, 0], r"$\Pi_1=\Pi_2$", (0, -40), size=12)
        label(ax, [1.5, -1.3, 1.4], r"$\Pi_3$", (0, 0), COLORS[2], 12)
    return export(fig, stem)


def main():
    ss.apply("double", font_size=10, line_width=1.6)
    plt.rcParams.update({
        "font.sans-serif": ["Microsoft YaHei", "Noto Sans CJK SC", "DejaVu Sans"],
        "mathtext.fontset": "dejavusans", "svg.fonttype": "path",
        "savefig.pad_inches": 0, "svg.hashsalt": "plane-position-v1",
    })
    ss.grayscale_check(COLORS)
    print("[note] Planes also use solid/dashed/dash-dot boundaries and o/s/^ points.")
    previews = [three_planes(k) for k in ["point", "line", "parallel_pair", "pairwise"]]
    previews += [parallel_planes([0, 0, 0], "coincident"),
                 parallel_planes([0, 0, 1.4], "two_coincident"),
                 parallel_planes([-1, 0, 1], "distinct")]
    sheet = Image.new("RGB", (2000, 2260), "white")
    for i, im in enumerate(previews):
        sheet.paste(im, ((i % 2)*1000, (i // 2)*565))
    sheet.save(OUT / "preview-planes-grayscale.png")
    print("[ok] Plane equations, normal ranks, augmented ranks and intersections verified.")


if __name__ == "__main__":
    main()
