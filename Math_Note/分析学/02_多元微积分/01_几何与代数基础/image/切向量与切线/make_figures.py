"""Regenerate the note's analytic geometry figures; no external data needed."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np
from PIL import Image, ImageOps
import sci_style as ss

OUT = Path(__file__).resolve().parent
BLUE = ss.OKABE_ITO["blue"]
ORANGE = ss.OKABE_ITO["orange"]
BLACK = "#222222"


def axes2d(ax, xlim, ylim):
    ax.set(xlim=xlim, ylim=ylim, xlabel="$x$ (dimensionless)",
           ylabel="$y$ (dimensionless)")
    ax.set_aspect("equal", adjustable="box")
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))


def arrow2d(ax, p, q, color=BLUE):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6,
                                shrinkA=0, shrinkB=0, mutation_scale=10))


def finish(fig, name):
    # Anchor the tight bounding box to the original canvas, preserving column
    # width even when equal-aspect axes leave empty margins.
    for x, y in [(0, 0), (1, 1)]:
        fig.text(x, y, ".", fontsize=0.1, alpha=0)
    ss.save(fig, OUT / f"{name}.pdf", also_png=True, dpi=600)
    ss.save(fig, OUT / f"{name}.svg", dpi=600)
    size = ss.output_size_mm(OUT / f"{name}.pdf")
    assert size and abs(size[0] - 178) / 178 < 0.03, size
    # Previews are QA artifacts, not the embedded production figures.
    with Image.open(OUT / f"{name}.png") as im:
        small = im.convert("RGB")
        small.thumbnail((1400, 850))
        small.save(OUT / f"preview-{name}.png")
        ImageOps.grayscale(small).save(OUT / f"preview-{name}-gray.png")
    plt.close(fig)


def secants():
    fig, axs = plt.subplots(1, 2, figsize=ss.figsize("double", height_mm=91),
                            layout="constrained")
    x = np.linspace(0, 2, 500)
    for ax, h, label in zip(axs, [0.8, 0.2], ["A", "B"]):
        ax.plot(x, x*x, color=BLUE, label="$y=x^2$")
        ax.plot(x, 1 + 2*(x-1), "--", color=BLACK, label="Tangent")
        ax.plot(x, 1 + (2+h)*(x-1), "-.", color=ORANGE, label="Secant")
        p, q = (1, 1), (1+h, (1+h)**2)
        ax.plot(*p, "o", color=BLACK, zorder=5)
        ax.plot(*q, "s", color=ORANGE, mec=BLACK, zorder=5)
        ax.annotate("$P$", p, xytext=(-13, 5), textcoords="offset points")
        ax.annotate("$Q$", q, xytext=(6, 1), textcoords="offset points")
        ax.text(0.03, 0.97, label, transform=ax.transAxes,
                va="top", fontweight="bold", fontsize=10)
        ax.text(0.97, 0.05, f"$h={h}$", transform=ax.transAxes, ha="right")
        axes2d(ax, (-0.05, 2.05), (-0.2, 4.2))
        ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.88))
    finish(fig, "fig-01-secant-limit")


def helix():
    fig = plt.figure(figsize=ss.figsize("double", height_mm=98))
    ax = fig.add_subplot(121, projection="3d")
    xy = fig.add_subplot(122)
    fig.subplots_adjust(left=0.015, right=0.985, bottom=0.17, top=0.84, wspace=0.38)
    t = np.linspace(0, 2*np.pi, 700)
    r = np.array([np.cos(t), np.sin(t), t/2])
    p = np.array([0., 1., np.pi/4])
    v = np.array([-1., 0., 0.5])
    lam = np.linspace(-0.75, 1.25, 50)
    line = p[:, None] + v[:, None]*lam
    ax.plot(*r, color=BLUE)
    ax.plot(*line, "--", color=BLACK)
    ax.scatter(*p, color=BLACK, s=18)
    ax.quiver(*p, *v, color=ORANGE, arrow_length_ratio=0.18, linewidth=2)
    ax.text(*(p + [0.10, 0.08, 0.05]), "$P$")
    ax.text(*(p + 0.7*v + [0.06, 0.04, 0.16]), "$\\mathbf{v}$")
    ax.set(xlim=(-1.35, 1.35), ylim=(-1.35, 1.35), zlim=(-0.15, 3.3))
    ax.set_box_aspect((2.7, 2.7, 3.45))
    ax.view_init(elev=23, azim=-57)
    ax.grid(False)
    for axis, name in zip([ax.xaxis, ax.yaxis, ax.zaxis], ["x", "y", "z"]):
        axis.set_pane_color((1, 1, 1, 0))
        axis.set_major_locator(MaxNLocator(4))
        axis.set_rotate_label(False)
        axis.labelpad = 7
        axis.set_label_text(f"${name}$ (dimensionless)", fontsize=7)
    xy.plot(r[0], r[1], color=BLUE)
    xy.plot(line[0], line[1], "--", color=BLACK)
    xy.plot(*p[:2], "o", color=BLACK)
    arrow2d(xy, p[:2], (p+v)[:2], ORANGE)
    xy.annotate("$P_{xy}$", p[:2], xytext=(5, -15), textcoords="offset points")
    xy.text(-0.75, 0.77, "$(-1,0)$", fontsize=8)
    axes2d(xy, (-1.4, 1.4), (-1.4, 1.4))
    ax.text2D(0.04, 1.05, "A", transform=ax.transAxes, fontweight="bold", fontsize=10)
    xy.text(0.02, 1.05, "B", transform=xy.transAxes, fontweight="bold", fontsize=10)
    handles = [Line2D([], [], color=BLUE, label="Curve"),
               Line2D([], [], color=BLACK, ls="--", label="Tangent line"),
               Line2D([], [], color=ORANGE, marker=">", label="Derivative vector")]
    fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 0.99))
    finish(fig, "fig-02-helix-tangent")


def zero_derivative():
    fig, axs = plt.subplots(1, 2, figsize=ss.figsize("double", height_mm=84),
                            layout="constrained")
    t = np.linspace(-1, 1, 800)
    funcs = [lambda u: (u**3, u**6), lambda u: (u**2, u**3)]
    for ax, f, letter in zip(axs, funcs, "AB"):
        ax.plot(*f(t), color=BLUE)
        ax.axhline(0, color=BLACK, ls="--")
        ax.plot(0, 0, "o", color=BLACK)
        for start, end in [(-0.8, -0.65), (0.65, 0.8)]:
            arrow2d(ax, f(start), f(end))
        ax.text(0.04, 0.96, letter, transform=ax.transAxes, fontweight="bold",
                fontsize=10, va="top")
        ax.annotate("$O$", (0, 0), xytext=(-10, 7), textcoords="offset points")
    axes2d(axs[0], (-1.15, 1.15), (-0.2, 1.2))
    axes2d(axs[1], (-0.15, 1.15), (-1.15, 1.15))
    finish(fig, "fig-03-zero-derivative")


if __name__ == "__main__":
    ss.apply("double")
    ss.grayscale_check([BLUE, ORANGE, BLACK])
    secants()
    helix()
    zero_derivative()
