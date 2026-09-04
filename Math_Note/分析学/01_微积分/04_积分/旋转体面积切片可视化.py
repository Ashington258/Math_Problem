from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, Polygon, Rectangle
import numpy as np


OUTPUT_PATH = Path(__file__).with_name("image") / "旋转体_圆盘法与柱壳法.png"
EDGE = "#a61e3c"
FILL = "#ef476f"
INK = "#243238"


def setup(axis: plt.Axes, title: str) -> None:
    axis.set(xlim=(-3.5, 3.5), ylim=(-1.25, 5.35), aspect="equal")
    axis.axis("off")
    axis.set_title(title, loc="left", fontsize=16, fontweight="bold")


def dimension(
    axis: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    label: str,
    offset: tuple[float, float],
) -> None:
    axis.add_patch(FancyArrowPatch(start, end, arrowstyle="<->", mutation_scale=13,
                                  linewidth=1.5, color=INK))
    midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
    axis.text(midpoint[0] + offset[0], midpoint[1] + offset[1], label,
              fontsize=13, ha="center", va="center")


def draw_disk(axis: plt.Axes) -> None:
    setup(axis, "Disk method: slice along the x direction")
    radius, center_y, thickness, flattening = 2.15, 2.25, 0.38, 0.72
    left, right = -thickness / 2, thickness / 2

    axis.annotate(
        "", xy=(3.15, center_y), xytext=(-3.15, center_y),
        arrowprops={"arrowstyle": "->", "lw": 1.8, "color": INK},
    )
    axis.text(2.92, center_y + 0.18, r"rotation axis $x$", fontsize=12, ha="right")
    axis.add_patch(Rectangle((left, center_y - radius), thickness, 2 * radius,
                             facecolor=FILL, edgecolor="none", alpha=0.4))
    axis.add_patch(Ellipse((left, center_y), flattening, 2 * radius,
                           facecolor=FILL, edgecolor=EDGE, linewidth=1.8,
                           linestyle="--", alpha=0.28))
    axis.plot([left, right, right, left],
              [center_y + radius, center_y + radius, center_y - radius, center_y - radius],
              color=EDGE, linewidth=2)
    axis.add_patch(Ellipse((right, center_y), flattening, 2 * radius,
                           facecolor=FILL, edgecolor=EDGE, linewidth=2.5, alpha=0.78))

    axis.plot([right, right], [center_y, center_y + radius], color=INK, linewidth=1.4)
    axis.text(right + 0.16, center_y + radius / 2, r"$R(x)$", fontsize=13, va="center")
    dimension(axis, (left, center_y + radius + 0.35),
              (right, center_y + radius + 0.35), r"$dx$", (0, 0.25))
    axis.text(0, 4.88, r"cross-sectional area  $A(x)=\pi R(x)^2$",
              color=EDGE, fontsize=15, fontweight="bold", ha="center")
    formula(axis, r"$dV=A(x)\,dx=\pi R(x)^2\,dx$")


def draw_shell(axis: plt.Axes) -> None:
    setup(axis, "Shell method: parallel slice")
    axis.annotate(
        "", xy=(0, 5.05), xytext=(0, -0.25),
        arrowprops={"arrowstyle": "->", "lw": 1.8, "color": INK},
    )
    axis.text(0.15, 4.92, r"rotation axis $y$", fontsize=12)
    outer, inner = 2.55, 2.17
    bottom, top, flattening = 0.55, 3.55, 0.5
    angle = np.linspace(0, 2 * np.pi, 320)
    outer_x, outer_y = outer * np.cos(angle), flattening * np.sin(angle)
    inner_x, inner_y = inner * np.cos(angle), 0.84 * flattening * np.sin(angle)

    ring = np.column_stack((np.r_[outer_x, inner_x[::-1]],
                            np.r_[top + outer_y, top + inner_y[::-1]]))
    axis.add_patch(Polygon(ring, closed=True, facecolor=FILL, edgecolor="none", alpha=0.72))
    for left in (-outer, inner):
        width = outer - inner
        axis.add_patch(Rectangle((left, bottom), width, top - bottom,
                                 facecolor=FILL, edgecolor="none", alpha=0.3))
    for radius, linewidth in ((outer, 2.4), (inner, 1.7)):
        axis.plot([radius, radius], [bottom, top], color=EDGE, linewidth=linewidth)
        axis.plot([-radius, -radius], [bottom, top], color=EDGE, linewidth=linewidth)
    axis.plot(outer_x, top + outer_y, color=EDGE, linewidth=2.5)
    axis.plot(inner_x, top + inner_y, color=EDGE, linewidth=2)
    axis.plot(outer_x, bottom + outer_y, color=EDGE, linewidth=1.7, linestyle="--")
    axis.plot(inner_x, bottom + inner_y, color=EDGE, linewidth=1.3, linestyle="--")

    axis.plot([0, outer], [bottom, bottom], color=INK, linewidth=1.4)
    axis.text(outer / 2, bottom + 0.15, r"radius $x$", fontsize=12, ha="center")
    dimension(axis, (outer + 0.35, bottom), (outer + 0.35, top), r"$h(x)$", (0.43, 0))
    dimension(axis, (inner, top + 0.72), (outer, top + 0.72), r"$dx$", (0, 0.23))
    axis.text(0, 4.65, r"lateral area  $A(x)=2\pi xh(x)$",
              color=EDGE, fontsize=15, fontweight="bold", ha="center")
    formula(axis, r"$dV=A(x)\,dx=2\pi xh(x)\,dx$")


def formula(axis: plt.Axes, text: str) -> None:
    axis.text(0, -0.72, text, fontsize=16, ha="center",
              bbox={"boxstyle": "round,pad=0.35", "facecolor": "#fff4f5", "edgecolor": EDGE})


def main() -> None:
    figure, axes = plt.subplots(1, 2, figsize=(14, 7), constrained_layout=True)
    draw_disk(axes[0])
    draw_shell(axes[1])
    figure.suptitle("Volume is the integral of slice areas", fontsize=19, fontweight="bold")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Saved visualization to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()