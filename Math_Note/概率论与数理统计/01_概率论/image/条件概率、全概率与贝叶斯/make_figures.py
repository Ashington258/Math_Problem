"""Deterministic probability diagrams; run from any working directory."""
from pathlib import Path
import json
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
from matplotlib.ticker import PercentFormatter
from PIL import Image, ImageOps
import numpy as np

import sci_style as ss

OUT = Path(__file__).resolve().parent
ss.apply("double")
plt.rcParams.update({"font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
                     "axes.unicode_minus": False, "savefig.pad_inches": 0})
BLUE, ORANGE = "#0072B2", "#E69F00"
manifest = []


def rectangle(ax, xy, w, h, color="white", hatch=None, alpha=1):
    ax.add_patch(Rectangle(xy, w, h, facecolor=color, edgecolor="0.2",
                           linewidth=0.8, hatch=hatch, alpha=alpha))


def panel_pair(ratio):
    fig, axs = plt.subplots(1, 2, figsize=ss.figsize("double", ratio=ratio),
                            layout="constrained")
    ss.panels(fig, axs, "AB", x=0, y=1.04)
    return fig, axs


def save(fig, stem):
    # Preserve the full journal-size canvas when equal-aspect axes leave margins.
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             facecolor="none", edgecolor="none", clip_on=False))
    fig.canvas.draw()
    fig.set_layout_engine("none")  # identical positions across PDF, SVG and PNG
    ss.save(fig, OUT / f"{stem}.pdf", also_png=True, dpi=600)
    ss.save(fig, OUT / f"{stem}.svg", dpi=600)
    width, height = ss.output_size_mm(OUT / f"{stem}.pdf")
    assert abs(width - 178) / 178 < 0.03, (stem, width)
    manifest.append({"file": stem, "width_mm": round(width, 2),
                     "height_mm": round(height, 2), "png_dpi": 600})
    with Image.open(OUT / f"{stem}.png") as img:
        preview = img.convert("RGB")
        preview.thumbnail((1500, 1000))
        preview.save(OUT / f"preview-{stem}.png")
        ImageOps.grayscale(preview).save(OUT / f"preview-{stem}-gray.png")
    plt.close(fig)


def conditioning():
    fig = plt.figure(figsize=ss.figsize("double", ratio=.60))
    axs = [fig.add_axes([.035, .25, .44, .66]),
           fig.add_axes([.525, .25, .44, .66])]
    for index, ax in enumerate(axs):
        rectangle(ax, (0, 0), 10, 6.4, "#F7F8FA")
        ax.text(0, 6.8, r"样本空间 $\Omega$", ha="left", fontsize=9)
        a_center, b_center, radius = (3.6, 3.2), (6.4, 3.2), 2.35
        a = Circle(a_center, radius, facecolor="#E1EFF7", edgecolor=BLUE, lw=1.4)
        b = Circle(b_center, radius, facecolor="#F8EBCF", edgecolor="#A16C12", lw=1.4)
        if index:
            a.set(facecolor="none", edgecolor="0.8", linestyle="--", linewidth=.9)
            b.set(linewidth=2.0)
        ax.add_patch(a)
        ax.add_patch(b)
        # A complete circle clipped by B creates the true lens A intersection B.
        lens = Circle(a_center, radius, facecolor="#8BBBD6", edgecolor=BLUE,
                      lw=.6, hatch="///")
        lens.set_clip_path(b)
        ax.add_patch(lens)
        if not index:
            ax.add_patch(Circle(a_center, radius, facecolor="none", edgecolor=BLUE, lw=1.4))
        ax.add_patch(Circle(b_center, radius, facecolor="none", edgecolor="#A16C12", lw=2 if index else 1.4))
        ax.text(2.4, 3.2, "$A$", color=BLUE if not index else "0.7", fontsize=12, ha="center")
        ax.text(7.6, 3.2, "$B$", color="#805509", fontsize=12, ha="center")
        ax.text(5, 3.2, "$A\\cap B$", fontsize=9, ha="center", va="center",
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": .85, "pad": 2})
        ax.text(5, -.85, "完整保留 A、B 及其交集" if not index else "已知 B：只在 B 内比较交集的概率",
                ha="center", fontsize=8)
        ax.set(xlim=(-.2, 10.2), ylim=(-1.1, 7.3), aspect="equal")
        ax.set_axis_off()
    fig.text(.04, .94, "(a) 原始样本空间", fontsize=9, weight="bold")
    fig.text(.53, .94, "(b) 条件事件 B 成为参考范围", fontsize=9, weight="bold")
    fig.text(.5, .17, r"$P(A\mid B)=\frac{P(A\cap B)}{P(B)}$", ha="center", fontsize=13)
    fig.text(.5, .065, "斜线交集的概率 ÷ 整个 B 的概率；将 B 的总概率归一化为 1",
             ha="center", fontsize=8)
    save(fig, "fig-01-conditioning")


def total_probability():
    fig = plt.figure(figsize=ss.figsize("double", ratio=.73))
    ax = fig.add_axes([.04, .03, .92, .94])
    backgrounds = ["#EBF3F8", "#F0F4F1", "#FBF3E3"]
    fills = ["#A8CBDF", "#C4D7CD", "#E7CD9D"]
    hatches = [None, "//", ".."]
    for i, (background, fill, hatch) in enumerate(zip(backgrounds, fills, hatches)):
        strip = Rectangle((4*i, 0), 4, 6, facecolor=background, edgecolor="none")
        ax.add_patch(strip)
        piece = Ellipse((6, 3), 10.8, 3.5, facecolor=fill,
                        edgecolor="0.55", linewidth=.4, hatch=hatch)
        ax.add_patch(piece)
        piece.set_clip_path(strip)  # set after add_patch, which initializes clipping
        ax.text(4*i+2, 5.35, f"$A_{i+1}$", ha="center", fontsize=12)
        ax.text([2.5, 6, 9.5][i], 3, f"$B\\cap A_{i+1}$", ha="center", fontsize=10,
                bbox={"facecolor": fill, "edgecolor": "none", "pad": 3})
        ax.annotate("", (4*i+2, -.55), (4*i+2, 1.9),
                    arrowprops={"arrowstyle": "->", "lw": .85, "color": "0.3"})
        ax.text(4*i+2, -.95, f"$P(B\\cap A_{i+1})$", ha="center", fontsize=9)
        ax.text(4*i+2, -1.6, f"$=P(B\\mid A_{i+1})P(A_{i+1})$", ha="center", fontsize=8)
    ax.add_patch(Rectangle((0, 0), 12, 6, facecolor="none", edgecolor="0.2", lw=1.2))
    for x in (4, 8):
        ax.plot([x, x], [0, 6], ls="--", color="0.4", lw=1)
    ax.add_patch(Ellipse((6, 3), 10.8, 3.5, facecolor="none", edgecolor="#554366", lw=1.8))
    ax.text(0, 6.5, r"样本空间 $\Omega=A_1\cup A_2\cup A_3$", fontsize=10)
    ax.annotate("事件 $B$", (10.8, 3.8), (11.4, 4.85), ha="center", fontsize=10,
                color="#554366", arrowprops={"arrowstyle": "->", "color": "#554366", "lw": .9})
    ax.text(6, -2.65, r"$P(B)=\sum_{i=1}^{3}P(B\cap A_i)=\sum_{i=1}^{3}P(B\mid A_i)P(A_i)$",
            ha="center", fontsize=11)
    ax.set(xlim=(-.45, 12.45), ylim=(-3.1, 7), aspect="equal")
    ax.set_axis_off()
    save(fig, "fig-02-partition")


def factory():
    fig, axs = panel_pair(0.55)
    ax = axs[0]
    for start, width, rate, color, label in [(0, .6, .1, BLUE, "$A_1$"),
                                             (.6, .4, .3, ORANGE, "$A_2$")]:
        rectangle(ax, (start, 0), width, 1, color, alpha=.16)
        rectangle(ax, (start, 0), width, rate, color, "//")
        ax.text(start + width/2, .72, label + f"\n产量 {width:.0%}\n不合格率 {rate:.0%}",
                ha="center", va="center")
    ax.annotate("贡献 6%", (.3, .05), (.3, .25), ha="center", fontsize=7,
                arrowprops={"arrowstyle": "->", "lw": .8})
    ax.text(.8, .15, "贡献 12%", ha="center", va="center", fontsize=7)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="来源概率（无量纲）",
           ylabel="组内比例（无量纲）", aspect="equal")
    ax.set_xticks([0, .6, 1]); ax.set_yticks([0, .1, .3, 1]); ax.minorticks_off()
    ax.text(.5, 1.04, r"$P(B)=0.06+0.12=0.18$", transform=ax.transAxes, ha="center")
    ax = axs[1]
    for y, parts, texts in [(1, [.6, .4], ["60%", "40%"]),
                             (0, [1/3, 2/3], ["1/3", "2/3"])]:
        ax.barh(y, parts[0], .4, color=BLUE, edgecolor="0.2", label="$A_1$" if y else None)
        ax.barh(y, parts[1], .4, left=parts[0], color=ORANGE, hatch="//",
                edgecolor="0.2", label="$A_2$" if y else None)
        ax.text(parts[0]/2, y, texts[0], ha="center", va="center", color="white")
        ax.text(parts[0]+parts[1]/2, y, texts[1], ha="center", va="center")
    ax.set(xlim=(0, 1), ylim=(-.5, 1.7), xlabel="来源概率（%）")
    ax.set_yticks([0, 1], ["后验\n已知 B", "先验\n全部产品"])
    ax.set_xticks([0, .25, .5, .75, 1]); ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.minorticks_off(); ax.legend(loc="upper center", ncol=2)
    save(fig, "fig-03-total-and-bayes")


def switching():
    fig, axs = panel_pair(.56)
    x, y = .8, -.4
    grid = np.linspace(-3, 3, 201)
    u, v = np.meshgrid(grid, grid)
    density = np.exp(-(u*u+v*v)/2)/(2*np.pi)
    for ax in axs:
        rectangle(ax, (-3, -3), x+3, y+3, "0.92", "..")
        ax.axvline(x, color="0.4", ls="--", lw=.8)
        ax.axhline(y, color="0.4", ls=":", lw=.8)
        ax.set(xlim=(-3, 3), ylim=(-3, 3), aspect="equal",
               xlabel="$X_1$（无量纲）", ylabel="$Y$（无量纲）")
        ax.set_xticks([-3, 0, 3]); ax.set_yticks([-3, 0, 3]); ax.minorticks_off()
        ax.text(x+.1, 2.5, "$x$", fontsize=7)
        ax.text(2.5, y+.12, "$y$", fontsize=7)
    contours = axs[0].contour(u, v, density, levels=[.02, .06, .12], colors=BLUE, linewidths=.9)
    axs[0].clabel(contours, fmt="%.2f", fontsize=6,
                  manual=[(.6, .4), (1.2, .7), (1.65, 1.2)])
    axs[0].text(.5, 1.04, "$X_3=0:\\ Y=X_2$", transform=axs[0].transAxes, ha="center")
    axs[0].text(.5, -.27, r"$P(B\mid X_3=0)=\Phi(x)\Phi(y)$", transform=axs[0].transAxes, ha="center")
    axs[1].plot(grid, grid, "--", color="0.5", lw=1.2)
    selected = np.append(grid[grid < min(x, y)], min(x, y))
    axs[1].plot(selected, selected, color=BLUE, lw=2.5)
    axs[1].plot([min(x,y)], [min(x,y)], "o", color=BLUE, ms=4)
    axs[1].annotate(r"$X_1\leq\min\{x,y\}$", (-1.4, -1.4), (-2.8, .9),
                    fontsize=7, arrowprops={"arrowstyle": "->", "lw": .8})
    axs[1].text(.5, 1.04, "$X_3=1:\\ Y=X_1$", transform=axs[1].transAxes, ha="center")
    axs[1].text(.5, -.27, r"$P(B\mid X_3=1)=\Phi(\min\{x,y\})$", transform=axs[1].transAxes, ha="center")
    save(fig, "fig-04-switching-cdf")


if __name__ == "__main__":
    assert math.isclose(.24/.6, .4)
    assert math.isclose(.6*.1 + .4*.3, .18)
    assert math.isclose(.06/.18, 1/3)
    ss.grayscale_check([BLUE, ORANGE])
    conditioning()
    total_probability()
    factory()
    switching()
    (OUT / "figure_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
