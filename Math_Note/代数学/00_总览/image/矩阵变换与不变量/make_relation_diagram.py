"""Render relation inclusions for general and symmetric real matrices.

Requires matplotlib, numpy, Pillow, and the sci-plot skill's sci_style.py.
Run from any directory; exports are placed beside this script.
Use --style-dir to select a different sci-plot scripts directory.
The sets contain ordered matrix pairs; their areas are not quantitative.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import Ellipse


def style_module(directory: Path | None):
    candidates = [directory] if directory else [
        Path.home() / ".agents/skills/sci-plot/scripts",
        Path.home() / ".codex/skills/sci-plot/scripts",
    ]
    for candidate in candidates:
        if (candidate / "sci_style.py").is_file():
            sys.path.insert(0, str(candidate))
            import sci_style

            return sci_style
    raise FileNotFoundError("Locate sci_style.py with --style-dir.")


def region(ax, center, width, height, color, linestyle, *, fill=True):
    patch = Ellipse(
        center, width, height,
        edgecolor=color,
        facecolor=to_rgba(color, 0.045) if fill else "none",
        linewidth=1.6,
        linestyle=linestyle,
    )
    ax.add_patch(patch)
    return patch


def label(ax, x, y, text, *, size=8):
    return ax.text(x, y, text, ha="center", va="center", fontsize=size)


def check_counterexample():
    j = np.array([[0.0, 1.0], [0.0, 0.0]])
    d = np.diag([1.0, 2.0])
    assert np.array_equal(np.linalg.solve(d, j @ d), 2 * j)
    assert np.array_equal(d.T @ j @ d, 2 * j)
    assert np.linalg.norm(j, "fro") != np.linalg.norm(2 * j, "fro")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--style-dir", type=Path)
    args = parser.parse_args()
    ss = style_module(args.style_dir)
    check_counterexample()

    ss.apply("double")
    # CJK sans-serif fallback; SVG paths make labels portable across machines.
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "Noto Sans CJK SC", "Arial", "DejaVu Sans"]
    plt.rcParams["svg.fonttype"] = "path"
    plt.rcParams["svg.hashsalt"] = "matrix-relation-inclusions"
    colors = [ss.OKABE_ITO[key] for key in ("black", "blue", "vermillion", "green")]
    ss.grayscale_check(colors)
    print("[accessibility] Explicit set labels and distinct boundary styles supplement colour.")
    black, blue, red, green = colors

    fig, axes = plt.subplots(
        1, 2, figsize=ss.figsize("double", height_mm=94), layout="constrained",
    )
    fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02, wspace=0.045)
    for ax, title in zip(axes, ("一般实方阵", "实对称矩阵")):
        ax.set(xlim=(0, 10), ylim=(-0.6, 8.3))
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.text(0.5, 1.04, title, transform=ax.transAxes, ha="center", va="bottom", fontsize=9)
    ss.panels(fig, axes, "AB", x=0.01, y=1.04)

    ax = axes[0]
    region(ax, (5, 4.15), 9.6, 7.5, black, "-", fill=False)
    region(ax, (4.05, 4.0), 5.7, 5.6, blue, "--")
    region(ax, (5.95, 4.0), 5.7, 5.6, red, "-.")
    region(ax, (5, 3.3), 2.3, 1.7, green, ":")
    label(ax, 5, 7.25, r"等价 $\mathcal{E}$")
    label(ax, 2.4, 4.3, r"相似 $\mathcal{S}$")
    label(ax, 7.6, 4.3, r"合同 $\mathcal{C}$")
    label(ax, 5, 3.3, "正交相似\n" + r"$\mathcal{O}$")
    ax.plot(5, 5.7, "o", markersize=4, color=black)
    label(ax, 5, 6.12, r"$(J,2J)$", size=7)
    label(ax, 5, -0.25, r"$\mathcal{O}\subsetneq\mathcal{S}\cap\mathcal{C}\subsetneq\mathcal{E}$")

    ax = axes[1]
    region(ax, (5, 4.15), 9.6, 7.5, black, "-", fill=False)
    region(ax, (5, 3.7), 7.4, 5.6, red, "-.")
    region(ax, (5, 3.1), 5.0, 3.4, blue, "--")
    label(ax, 5, 7.25, r"等价 $\mathcal{E}$")
    label(ax, 5, 5.75, r"合同 $\mathcal{C}$")
    label(ax, 5, 3.1, "相似 = 正交相似\n" + r"$\mathcal{S}=\mathcal{O}$")
    label(ax, 5, -0.25, r"$\mathcal{O}=\mathcal{S}\subsetneq\mathcal{C}\subsetneq\mathcal{E}$")

    # These are schematic sets, so axes, units, and numerical scales do not apply.
    output = Path(__file__).resolve().parent / "relation-inclusions"
    ss.save(fig, output.with_suffix(".pdf"), also_png=True)
    ss.save(fig, output.with_suffix(".svg"))
    width, height = ss.output_size_mm(output.with_suffix(".png"), dpi=600)
    assert abs(width - 178) / 178 < 0.03, (width, height)
    plt.close(fig)


if __name__ == "__main__":
    main()
