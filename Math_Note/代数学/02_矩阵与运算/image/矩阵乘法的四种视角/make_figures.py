"""Reproduce the academic diagrams as SVG, PDF and 600-dpi PNG.

Dependencies: numpy, matplotlib, Pillow and sci-plot/scripts/sci_style.py.
Run from any directory. Use --style-dir to override skill discovery.
All examples use A (2 x 3), B (3 x 2), and the same computed C.
The diagrams have no quantitative axes; canvas coordinates are in mm.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Rectangle


A = np.array([[1, 2, 3], [4, 5, 6]])
B = np.array([[1, 2], [0, 1], [2, -1]])
C = A @ B
COLORS = ["#fbb4ae", "#b3cde3", "#ccebc5"]
INK = "#202020"
GRAY = "#626262"
OUT = Path(__file__).resolve().parent
TEXTS = []
FORMULAS = {}


def load_style(directory):
    candidates = [directory] if directory else [
        Path.home() / ".agents/skills/sci-plot/scripts",
        Path.home() / ".codex/skills/sci-plot/scripts",
    ]
    for candidate in candidates:
        if (candidate / "sci_style.py").is_file():
            sys.path.insert(0, str(candidate))
            import sci_style

            return sci_style
    raise FileNotFoundError("Pass --style-dir pointing to sci-plot/scripts.")


def label(ax, x, y, text, *, size=8, color=INK, ha="center"):
    # Mathtext requires braces for font commands that TeX permits unbraced.
    text = re.sub(r"\\(mathrm|mathsf)\s+([A-Za-z])", r"\\\1{\2}", text)
    # Keep numerical entries and indices upright even with an italic math default.
    text = re.sub(r"\$([^$]+)\$", lambda m: "$" + re.sub(
        r"(\d+)", r"\\mathrm{\1}", m.group(1)) + "$", text)
    highlight = color in COLORS
    obj = ax.text(x, y, text, ha=ha, va="center", fontsize=size,
                  color=INK if highlight else color,
                  bbox={"facecolor": color, "edgecolor": "none", "pad": 1.5}
                  if highlight else None)
    TEXTS.append(obj)
    return obj


def canvas(ss, height=100):
    TEXTS.clear()
    fig = plt.figure(figsize=ss.figsize("double", height_mm=height))
    # 1-mm margins plus savefig's 1-mm padding preserve a 178-mm output.
    ax = fig.add_axes([1 / 178, 1 / height, 176 / 178, (height - 2) / height])
    ax.set(xlim=(1, 177), ylim=(1, height - 1))
    ax.set_axis_off()
    return fig, ax


def matrix(ax, x, y, values, *, cell=10, mode=None, chosen=None,
           colored=False, tint=None, name=None):
    """Place a matrix by its centre; return the individual cell centres."""
    values = np.asarray(values)
    rows, cols = values.shape
    left, bottom = x - cols * cell / 2, y - rows * cell / 2
    points = {}
    for i in range(rows):
        for j in range(cols):
            cx = left + (j + 0.5) * cell
            cy = bottom + (rows - i - 0.5) * cell
            points[i, j] = (cx, cy)
            active = (
                mode in ("all", "columns", "rows")
                or mode == "row" and i == chosen
                or mode == "col" and j == chosen
                or mode == "entry" and (i, j) == chosen
            )
            color = tint
            if active and (colored or mode in ("columns", "rows")):
                color = COLORS[j if mode in ("row", "columns") else i]
            if active:
                color = color or COLORS[0]
                ax.add_patch(Rectangle(
                    (cx - cell * 0.46, cy - cell * 0.43),
                    cell * 0.92, cell * 0.86,
                    facecolor=color if color in COLORS else "#e6e6e6",
                    edgecolor="none",
                ))
            label(ax, cx, cy, f"${values[i, j]}$", size=10, color=INK)
    for bx, sign in [(left - 1.8, 1), (left + cols * cell + 1.8, -1)]:
        ax.plot([bx + sign * 1.7, bx, bx, bx + sign * 1.7],
                [bottom + rows * cell, bottom + rows * cell, bottom, bottom],
                color=INK, linewidth=0.8)
    if name:
        label(ax, x, bottom + rows * cell + 6, name, size=9)
    return points


def arrow(ax, start, end):
    ax.annotate("", xy=end, xytext=start,
                arrowprops={"arrowstyle": "->", "color": GRAY, "lw": 0.9})


def main_product(ax, *, left_mode, left_chosen, right_mode, right_chosen,
                 result_mode, result_chosen, colored=False):
    matrix(ax, 29, 70, A, mode=left_mode, chosen=left_chosen,
           colored=colored, name=r"$A\;(2\times3)$")
    label(ax, 57, 70, r"$\cdot$", size=11)
    matrix(ax, 85, 70, B, mode=right_mode, chosen=right_chosen,
           colored=colored, name=r"$B\;(3\times2)$")
    label(ax, 111, 70, "$=$", size=13)
    matrix(ax, 141, 70, C, mode=result_mode, chosen=result_chosen, tint=INK,
           name=r"$C\;(2\times2)$")


def save(ss, fig, name):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    # Check that labels stay on the canvas and distinct labels do not overlap.
    boxes = [(obj, obj.get_window_extent(renderer)) for obj in TEXTS]
    for obj, box in boxes:
        if not fig.bbox.contains(box.x0, box.y0) or not fig.bbox.contains(box.x1, box.y1):
            raise ValueError(f"Label outside figure: {obj.get_text()}")
    for i, (first, box1) in enumerate(boxes):
        for second, box2 in boxes[i + 1:]:
            if box1.overlaps(box2):
                raise ValueError(f"Overlapping labels: {first.get_text()} / {second.get_text()}")
    FORMULAS[name] = sorted({tex for obj in TEXTS
                            for tex in re.findall(r"\$([^$]+)\$", obj.get_text())})
    ss.save(fig, OUT / f"{name}.svg", dpi=600, also_png=True)
    ss.save(fig, OUT / f"{name}.pdf", dpi=600)
    plt.close(fig)


def inner(ss):
    fig, ax = canvas(ss, 110)
    label(ax, 89, 104, r"$c_{ij}=\alpha_{\mathrm r,i}^{\mathsf T}\beta_{\mathrm c,j}=\sum_{k=1}^{n}a_{ik}b_{kj}$", size=10)
    main_product(ax, left_mode="row", left_chosen=0,
                 right_mode="col", right_chosen=1,
                 result_mode="entry", result_chosen=(0, 1), colored=True)
    label(ax, 29, 49, r"取第 1 行 $\alpha_{\mathrm r,1}^{\mathsf T}$", color=GRAY)
    label(ax, 85, 49, r"取第 2 列 $\beta_{\mathrm c,2}$", color=GRAY)
    label(ax, 141, 49, r"填入 $c_{12}$", color=GRAY)
    label(ax, 89, 41, r"$\alpha_{\mathrm r,1}^{\mathsf T}\beta_{\mathrm c,2}=a_{11}b_{12}+a_{12}b_{22}+a_{13}b_{32}$", size=9)
    terms = [(25, r"$1\cdot2$"), (68, r"$2\cdot1$"), (111, r"$3\cdot(-1)$")]
    for k, (x, text) in enumerate(terms):
        label(ax, x, 30, text, size=10, color=COLORS[k])
        label(ax, x, 19, f"$k={k + 1}$", color=COLORS[k])
    for x in (46, 89):
        label(ax, x, 30, "$+$", size=10)
    label(ax, 132, 30, "$=$", size=10)
    label(ax, 151, 30, f"${C[0, 1]}$", size=10)
    label(ax, 89, 7, "对应位置相乘，再求和；一次得到一个数。")
    save(ss, fig, "01_inner")


def outer(ss):
    fig, ax = canvas(ss, 135)
    label(ax, 89, 128, r"$C=\sum_{k=1}^{n}M_k,\qquad M_k=\alpha_{\mathrm c,k}\beta_{\mathrm r,k}^{\mathsf T}$", size=10)
    for k, x in enumerate((29, 89, 149)):
        color = COLORS[k]
        label(ax, x, 114, f"$k={k + 1}$", color=color)
        matrix(ax, x - 17, 98, A[:, [k]], cell=8,
               mode="all", tint=color, name=rf"$\alpha_{{\mathrm c,{k + 1}}}$")
        label(ax, x - 5, 98, r"$\cdot$", size=10)
        matrix(ax, x + 10, 98, B[[k], :], cell=8,
               mode="all", tint=color, name=rf"$\beta_{{\mathrm r,{k + 1}}}^{{\mathsf T}}$")
        arrow(ax, (x, 85), (x, 77))
        matrix(ax, x, 64, np.outer(A[:, k], B[k, :]), cell=9,
               mode="all", tint=color)
        label(ax, x, 47, rf"$M_{k + 1}=\alpha_{{\mathrm c,{k + 1}}}\beta_{{\mathrm r,{k + 1}}}^{{\mathsf T}}$", size=8, color=color)
    for x in (59, 119):
        label(ax, x, 64, "$+$", size=11)
    arrow(ax, (89, 40), (89, 34))
    matrix(ax, 89, 22, C, cell=9)
    label(ax, 61, 22, "$C=$", size=11)
    label(ax, 89, 5, "每个 k 贡献一整张矩阵；相同位置逐项相加。")
    save(ss, fig, "02_outer")


def column(ss):
    fig, ax = canvas(ss, 110)
    label(ax, 89, 104, r"$\gamma_{\mathrm c,j}=A\beta_{\mathrm c,j}=\sum_{k=1}^{n}b_{kj}\alpha_{\mathrm c,k}$", size=10)
    matrix(ax, 29, 70, A, mode="columns", name=r"$A\;(2\times3)$")
    for k in range(3):
        label(ax, 19 + 10 * k, 55, rf"$\alpha_{{\mathrm c,{k + 1}}}$", size=7, color=COLORS[k])
    label(ax, 57, 70, r"$\cdot$", size=11)
    matrix(ax, 85, 70, B, mode="col", chosen=1, colored=True,
           name=r"$B\;(3\times2)$")
    label(ax, 111, 70, "$=$", size=13)
    matrix(ax, 141, 70, C, mode="col", chosen=1, tint=INK, name=r"$C\;(2\times2)$")
    label(ax, 85, 49, r"系数列 $\beta_{\mathrm c,2}$", color=GRAY)
    label(ax, 141, 49, r"结果列 $\gamma_{\mathrm c,2}$", color=GRAY)
    label(ax, 89, 41, r"$A\beta_{\mathrm c,2}=b_{12}\alpha_{\mathrm c,1}+b_{22}\alpha_{\mathrm c,2}+b_{32}\alpha_{\mathrm c,3}$", size=9)
    for k, x in enumerate((25, 65, 105)):
        coefficient = str(B[k, 1]) if B[k, 1] >= 0 else f"({B[k, 1]})"
        label(ax, x - 10, 31, f"${coefficient}$", size=11, color=COLORS[k])
        matrix(ax, x, 31, A[:, [k]], cell=8, mode="all", tint=COLORS[k])
    for x in (44, 84):
        label(ax, x, 31, "$+$", size=12)
    label(ax, 124, 31, "$=$", size=12)
    matrix(ax, 147, 31, C[:, [1]], cell=8, mode="all", tint=INK)
    label(ax, 89, 9, "A 的列是被组合的向量，B 的一列是组合系数。")
    save(ss, fig, "03_column")


def row(ss):
    fig, ax = canvas(ss, 110)
    label(ax, 89, 104, r"$\gamma_{\mathrm r,i}^{\mathsf T}=\alpha_{\mathrm r,i}^{\mathsf T}B=\sum_{k=1}^{n}a_{ik}\beta_{\mathrm r,k}^{\mathsf T}$", size=10)
    matrix(ax, 29, 70, A, mode="row", chosen=1, colored=True,
           name=r"$A\;(2\times3)$")
    label(ax, 57, 70, r"$\cdot$", size=11)
    matrix(ax, 85, 70, B, mode="rows", name=r"$B\;(3\times2)$")
    for k in range(3):
        label(ax, 104, 80 - 10 * k, rf"$\beta_{{\mathrm r,{k + 1}}}^{{\mathsf T}}$", size=7, color=COLORS[k])
    label(ax, 115, 70, "$=$", size=13)
    matrix(ax, 141, 70, C, mode="row", chosen=1, tint=INK, name=r"$C\;(2\times2)$")
    label(ax, 29, 49, r"系数行 $\alpha_{\mathrm r,2}^{\mathsf T}$", color=GRAY)
    label(ax, 141, 49, r"结果行 $\gamma_{\mathrm r,2}^{\mathsf T}$", color=GRAY)
    label(ax, 89, 41, r"$\alpha_{\mathrm r,2}^{\mathsf T}B=a_{21}\beta_{\mathrm r,1}^{\mathsf T}+a_{22}\beta_{\mathrm r,2}^{\mathsf T}+a_{23}\beta_{\mathrm r,3}^{\mathsf T}$", size=9)
    for k, x in enumerate((27, 68, 109)):
        label(ax, x - 16, 31, f"${A[1, k]}$", size=11, color=COLORS[k])
        matrix(ax, x, 31, B[[k], :], cell=8, mode="all", tint=COLORS[k])
    for x in (46, 87):
        label(ax, x, 31, "$+$", size=12)
    label(ax, 128, 31, "$=$", size=12)
    matrix(ax, 152, 31, C[[1], :], cell=8, mode="all", tint=INK)
    label(ax, 89, 9, "B 的行是被组合的向量，A 的一行是组合系数。")
    save(ss, fig, "04_row")


def verify_arithmetic():
    np.testing.assert_array_equal(C, [[7, 1], [16, 7]])
    contributions = [np.outer(A[:, k], B[k, :]) for k in range(A.shape[1])]
    np.testing.assert_array_equal(sum(contributions), C)
    for j in range(B.shape[1]):
        np.testing.assert_array_equal(sum(B[k, j] * A[:, k] for k in range(3)), C[:, j])
    for i in range(A.shape[0]):
        np.testing.assert_array_equal(sum(A[i, k] * B[k, :] for k in range(3)), C[i, :])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--style-dir", type=Path)
    args = parser.parse_args()
    ss = load_style(args.style_dir)
    ss.apply("double")
    for font_path in sorted((OUT / "fonts").glob("*.ttf")):
        font_manager.fontManager.addfont(font_path)
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ("Microsoft YaHei", "Noto Sans CJK SC", "SimHei") if f in installed]
    if not fonts:
        raise RuntimeError("Install a Chinese sans-serif font before rendering.")
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": fonts + ["DejaVu Sans"],
        "mathtext.fontset": "custom", "mathtext.default": "it",
        "mathtext.rm": "KaTeX_Main", "mathtext.it": "KaTeX_Math:italic",
        "mathtext.bf": "KaTeX_Main:bold", "mathtext.bfit": "KaTeX_Math:italic:bold",
        "mathtext.sf": "KaTeX_SansSerif", "mathtext.tt": "KaTeX_Typewriter",
        "mathtext.fallback": "cm", "svg.fonttype": "path",
        "svg.hashsalt": "matrix-multiplication-four-views",
        "savefig.pad_inches": 1 / 25.4,
    })
    ss.grayscale_check(COLORS)
    # Matching indices, spatial order and captions disambiguate close luminances.
    verify_arithmetic()
    for draw in (inner, outer, column, row):
        draw(ss)
    (OUT / "figure_formulas.json").write_text(
        json.dumps(FORMULAS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Verified: four decompositions, label bounds, and label overlaps.")


if __name__ == "__main__":
    main()
