"""Reproduce the probability note figures and analytic numerical tables.

Run: python plot_distributions.py
Dependencies: numpy, scipy, matplotlib, pillow. Output is relative to this file.
All curves are exact model functions, not fitted or sampled observations.
PDF: vector; PNG: 600 dpi; nominal width: 178 mm. No random data are used.
"""

from __future__ import annotations

import csv
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import scipy
from scipy import stats

import sci_style as ss


OUT = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ["Microsoft YaHei", "Noto Sans CJK SC", "SimHei", "DejaVu Sans"]
ss.apply("double", font_size=9, tick_size=8, legend_size=7.5, mathtext=False)
FONT = ss.check_fonts()
if FONT == "DejaVu Sans":
    raise RuntimeError("Install Microsoft YaHei, Noto Sans CJK SC or SimHei for Chinese labels.")

BLUE, ORANGE, GREEN = [ss.OKABE_ITO[k] for k in ("blue", "vermillion", "green")]
COLORS = [BLUE, ORANGE, GREEN]
STYLES = ["-", "--", "-."]
MARKERS = ["o", "s", "^"]
FIGURES = []


def axes_pair(*, rows=1):
    return plt.subplots(rows, 2, figsize=ss.figsize("double", height_mm=76 if rows == 1 else 145),
                        layout="constrained")


def label(ax, *, cdf=False, discrete=False):
    ax.set_xlabel("取值 $x$（无量纲）" if not discrete else "计数取值 $k$（次 / 个）")
    ax.set_ylabel(("累计概率 $F(x)$" if cdf else ("单点概率 $P(X=k)$" if discrete else "密度 $f(x)$"))
                  + "（无量纲）")
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6, integer=discrete))
    if cdf:
        ax.set_ylim(0, 1.055)
        ax.set_yticks([0, .25, .5, .75, 1])
    else:
        ax.set_ylim(bottom=0)
    if discrete:
        ax.minorticks_off()


def save(fig, axs, name):
    ss.panels(fig, axs, "ABCD", x=0, y=1.025, size=10)
    pdf = OUT / f"{name}.pdf"
    ss.save(fig, pdf, dpi=600, also_png=True)
    size = ss.output_size_mm(pdf)
    assert size and abs(size[0] - 178) / 178 < .03, (name, size)
    FIGURES.append({"name": name, "width_mm": size[0], "height_mm": size[1], "png_dpi": 600})
    plt.close(fig)


def curve(ax, x, y, i=0, *, legend=None):
    ax.plot(x, y, STYLES[i], color=COLORS[i], marker=MARKERS[i] if legend else None,
            markevery=max(1, len(x)//8), markersize=3.5, label=legend)


def relation():
    fig, axs = axes_pair(rows=2)
    z = np.linspace(-4, 4, 1601)
    for r in range(2):
        curve(axs[r, 0], z, stats.norm.pdf(z))
        curve(axs[r, 1], z, stats.norm.cdf(z))
        for c in range(2):
            label(axs[r, c], cdf=c == 1)
            axs[r, c].set_xlim(-4, 4)
    t = .5
    area = stats.norm.cdf(t)
    u = np.linspace(-4, t, 600)
    axs[0, 0].fill_between(u, stats.norm.pdf(u), color=BLUE, alpha=.22, linewidth=0)
    axs[0, 0].axvline(t, color=".5", lw=.9, ls=":")
    axs[0, 0].text(.04, .89, rf"$F(0.5)={area:.4f}$", transform=axs[0, 0].transAxes)
    axs[0, 1].plot([t, t], [0, area], ":", color=".45", lw=.9)
    axs[0, 1].plot([-4, t], [area, area], ":", color=".45", lw=.9)
    axs[0, 1].plot(t, area, "o", color=BLUE)
    axs[0, 1].annotate(f"累计到 0.5：{area:.4f}", xy=(t, area), xytext=(-3.5, .89),
                       arrowprops={"arrowstyle": "->", "color": ".3", "lw": .8}, fontsize=8)
    a, b = -1, 1
    u = np.linspace(a, b, 400)
    delta = stats.norm.cdf(b)-stats.norm.cdf(a)
    axs[1, 0].fill_between(u, stats.norm.pdf(u), color=ORANGE, alpha=.25, linewidth=0)
    axs[1, 0].text(.04, .89, f"阴影面积 = {delta:.4f}", transform=axs[1, 0].transAxes, fontsize=8)
    fa, fb = stats.norm.cdf(a), stats.norm.cdf(b)
    axs[1, 1].plot([a, b], [fa, fb], "o", color=ORANGE, ls="none")
    axs[1, 1].plot([a, 2], [fa, fa], ":", color=".45", lw=.9)
    axs[1, 1].plot([b, 2], [fb, fb], ":", color=".45", lw=.9)
    axs[1, 1].annotate("", xy=(2, fb), xytext=(2, fa),
                       arrowprops={"arrowstyle": "<->", "color": ORANGE, "lw": 1.4})
    axs[1, 1].text(2.2, .5, f"增量\n{delta:.4f}", color=ORANGE, fontsize=8, va="center")
    save(fig, axs, "01_pdf_cdf_relation")


def triangle():
    fig, axs = axes_pair()
    axs[0].plot([-.4, 0], [0, 0], color=BLUE)
    axs[0].plot([0, 2], [0, 1], color=BLUE)
    axs[0].plot([2, 2.4], [0, 0], color=BLUE)
    axs[0].plot(2, 1, "o", mfc="white", mec=BLUE)
    axs[0].plot(2, 0, "o", color=BLUE)
    u = np.linspace(1, 2, 400)
    axs[0].fill_between(u, u/2, color=ORANGE, alpha=.25, linewidth=0)
    axs[0].text(.04, .89, "阴影面积 = 0.7500", transform=axs[0].transAxes, fontsize=8)
    x = np.linspace(-.4, 2.4, 1000)
    f = np.clip(x, 0, 2)**2/4
    curve(axs[1], x, f)
    axs[1].plot([1, 2], [.25, 1], "o", color=ORANGE, ls="none")
    axs[1].plot([1, 2.2], [.25, .25], ":", color=".45", lw=.9)
    axs[1].annotate("", xy=(2.2, 1), xytext=(2.2, .25),
                    arrowprops={"arrowstyle": "<->", "color": ORANGE})
    for c, ax in enumerate(axs):
        label(ax, cdf=c == 1)
        ax.set_xlim(-.4, 2.4)
    save(fig, axs, "02_linear_density")


def step_cdf(ax, k, pmf, xmax):
    """Horizontal segments with filled right-continuous and open left limits.

    No connecting diagonal/vertical curves that suggest intermediate values.
    Infinite-support distributions retain their remaining tail probability.
    """
    prev = np.r_[0, np.cumsum(pmf)[:-1]]
    cdf = np.cumsum(pmf)
    ax.plot([k[0]-1, k[0]], [0, 0], color=BLUE)
    for i, ki in enumerate(k):
        end = k[i+1] if i+1 < len(k) else xmax
        ax.plot([ki, end], [cdf[i], cdf[i]], color=BLUE)
    ax.plot(k, prev, "o", mfc="white", mec=BLUE, ms=4, zorder=3, ls="none")
    ax.plot(k, cdf, "o", color=BLUE, ms=4, zorder=4, ls="none")


def discrete(name, rv, k, legend):
    k = np.array(k)
    p = rv.pmf(k)
    fig, axs = axes_pair()
    axs[0].bar(k, p, width=.55, color=BLUE, edgecolor=".2", linewidth=.6)
    axs[0].text(.97, .94, legend, transform=axs[0].transAxes, ha="right", va="top", fontsize=8)
    if len(k) <= 6:
        for ki, pi in zip(k, p):
            text = f"{pi:.4f}" if 0 < pi < .01 else f"{pi:.3f}"
            axs[0].text(ki, pi+.015, text, ha="center", fontsize=7)
        axs[0].set_ylim(0, min(1.1, max(p)*1.25+.02))
    step_cdf(axs[1], k, p, k[-1]+.85)
    for c, ax in enumerate(axs):
        label(ax, cdf=c == 1, discrete=True)
        ax.set_xlim(k[0]-.85, k[-1]+.85)
    save(fig, axs, name)


def uniform():
    fig, axs = axes_pair()
    x = np.linspace(-.3, 3.4, 1200)
    for i, (a, b) in enumerate([(0, .5), (0, 2), (1, 3)]):
        text = rf"$U({a:g},{b:g})$"
        # Exact constant segments; gaps at jumps prevent fictitious slopes.
        axs[0].plot([-.3, a, np.nan, a, b, np.nan, b, 3.4],
                    [0, 0, np.nan, 1/(b-a), 1/(b-a), np.nan, 0, 0],
                    STYLES[i], color=COLORS[i], label=text)
        curve(axs[1], x, stats.uniform(loc=a, scale=b-a).cdf(x), i, legend=text)
    for c, ax in enumerate(axs):
        label(ax, cdf=c == 1)
        ax.set_xlim(-.3, 3.4)
        ax.legend(loc="upper right" if c == 0 else "lower right")
    save(fig, axs, "09_uniform")


def exponential():
    fig, axs = axes_pair()
    x = np.linspace(0, 5, 1001)
    for i, rate in enumerate([.5, 1, 2]):
        rv = stats.expon(scale=1/rate)
        text = rf"$\lambda={rate:g}$"
        curve(axs[0], x, rv.pdf(x), i, legend=text)
        curve(axs[1], x, rv.cdf(x), i, legend=text)
    for c, ax in enumerate(axs):
        label(ax, cdf=c == 1)
        ax.set_xlim(0, 5)
        ax.legend(loc="upper right" if c == 0 else "lower right")
    save(fig, axs, "10_exponential")


def normal_parameters():
    fig, axs = axes_pair(rows=2)
    x = np.linspace(-5, 5, 1601)
    for r, params in enumerate([[(-1, 1), (0, 1), (1, 1)], [(0, .5), (0, 1), (0, 2)]]):
        for i, (mu, sigma) in enumerate(params):
            rv = stats.norm(loc=mu, scale=sigma)
            text = rf"$\mu={mu:g},\ \sigma={sigma:g}$"
            curve(axs[r, 0], x, rv.pdf(x), i, legend=text)
            curve(axs[r, 1], x, rv.cdf(x), i, legend=text)
        for c in range(2):
            ax = axs[r, c]
            label(ax, cdf=c == 1)
            ax.set_xlim(-5, 5)
            ax.legend(loc="upper right" if c == 0 else "lower right")
    save(fig, axs, "11_normal_parameters")


def normal_example():
    fig, axs = axes_pair()
    x = np.linspace(40, 160, 1601)
    rv = stats.norm(loc=100, scale=15)
    curve(axs[0], x, rv.pdf(x))
    curve(axs[1], x, rv.cdf(x))
    u = np.linspace(85, 130, 600)
    p = rv.cdf(130)-rv.cdf(85)
    axs[0].fill_between(u, rv.pdf(u), color=ORANGE, alpha=.25, linewidth=0)
    axs[0].text(.04, .89, f"阴影面积 = {p:.5f}", transform=axs[0].transAxes, fontsize=8)
    fa, fb = rv.cdf([85, 130])
    axs[1].plot([85, 130], [fa, fb], "o", color=ORANGE, ls="none")
    axs[1].plot([85, 145], [fa, fa], ":", color=".45", lw=.9)
    axs[1].plot([130, 145], [fb, fb], ":", color=".45", lw=.9)
    axs[1].annotate("", xy=(145, fb), xytext=(145, fa),
                    arrowprops={"arrowstyle": "<->", "color": ORANGE})
    for c, ax in enumerate(axs):
        label(ax, cdf=c == 1)
        ax.set_xlim(40, 160)
        ax.set_xticks([40, 70, 100, 130, 160])
    save(fig, axs, "12_normal_example")


def tables():
    """Tables use the same parameters as the embedded figures and examples."""
    specs = [
        ("coins", stats.binom(2, .5), [0, 1, 2], True),
        ("bernoulli", stats.bernoulli(.3), [0, 1], True),
        ("binomial", stats.binom(5, .2), list(range(6)), True),
        ("poisson", stats.poisson(2), list(range(7)), True),
        ("geometric", stats.geom(.5), list(range(1, 7)), True),
        ("hypergeometric", stats.hypergeom(10, 4, 3), list(range(4)), True),
        ("linear_density", None, [0, .5, 1, 1.5, 2], False),
        ("uniform", stats.uniform(loc=0, scale=2), [0, .5, 1, 1.5, 2], False),
        ("exponential", stats.expon(scale=1), [0, .5, 1, 2, 3], False),
        ("standard_normal", stats.norm(), [-2, -1, 0, 1, 2, 3], False),
        ("normal_example", stats.norm(loc=100, scale=15), [85, 100, 115, 130], False),
    ]
    data = {}
    csv_rows = []
    for name, rv, values, is_discrete in specs:
        rows = []
        for x in values:
            if name == "linear_density":
                v, f = (x/2 if 0 < x < 2 else 0), min(max(x, 0), 2)**2/4
            else:
                v, f = float(rv.pmf(x) if is_discrete else rv.pdf(x)), float(rv.cdf(x))
            row = {"x": x, "pmf" if is_discrete else "pdf": v, "cdf": f}
            rows.append(row)
            csv_rows.append([name, "discrete" if is_discrete else "continuous", x, v, f])
        data[name] = rows
    (OUT / "numerical_tables.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    with (OUT / "numerical_tables.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["distribution", "type", "x", "pmf_or_pdf", "cdf"])
        writer.writerows(csv_rows)
    # Exact model checks (no Monte Carlo sampling error).
    assert abs(sum(row["pmf"] for row in data["binomial"])-1) < 1e-12
    assert abs(sum(row["pmf"] for row in data["hypergeometric"])-1) < 1e-12
    assert abs(stats.norm.cdf(2)-stats.norm.cdf(-1)-.8185946) < 1e-7
    for rows in data.values():
        cumulative = [row["cdf"] for row in rows]
        assert all(0 <= y <= 1 for y in cumulative)
        assert all(a <= b for a, b in zip(cumulative, cumulative[1:]))


def main():
    ss.grayscale_check(COLORS)  # Similar luminances are also encoded by dash/marker.
    relation()
    triangle()
    discrete("03_coins", stats.binom(2, .5), range(3), r"$B(2,0.5)$")
    discrete("04_bernoulli", stats.bernoulli(.3), range(2), r"$p=0.3$")
    discrete("05_binomial", stats.binom(5, .2), range(6), r"$B(5,0.2)$")
    discrete("06_poisson", stats.poisson(2), range(11), r"$\lambda=2$")
    discrete("07_geometric", stats.geom(.5), range(1, 9), r"$p=0.5$")
    discrete("08_hypergeometric", stats.hypergeom(10, 4, 3), range(4), r"$H(10,4,3)$")
    uniform()
    exponential()
    normal_parameters()
    normal_example()
    tables()
    manifest = {"versions": {"python": platform.python_version(), "numpy": np.__version__,
                             "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
                "font": FONT, "source": "analytic PMF/PDF/CDF; no observations or error bars", "figures": FIGURES}
    (OUT / "figure_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Complete: {len(FIGURES)} figure pairs; 11 numerical tables.")


if __name__ == "__main__":
    main()
