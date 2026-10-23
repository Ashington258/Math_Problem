"""Reproducible analytic illustrations, not empirical data.

Run: python make_figures.py
Thirteen 178-mm figures: PDF, SVG and 600-dpi PNG; colour/gray preview sheets.
All quantities are dimensionless. No randomness or uncertainty is involved.
sci_style.py is vendored from the sci-plot skill, without modification.
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.ticker import MaxNLocator
import numpy as np
from PIL import Image, ImageOps, ImageDraw

import sci_style as ss

HERE = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ["DejaVu Sans"]
ss.apply("double", font_size=8, line_width=1.4, mathtext=False)
plt.rcParams.update({"savefig.pad_inches": 0, "svg.fonttype": "path"})
BLUE, RED = ss.OKABE_ITO["blue"], ss.OKABE_ITO["vermillion"]
GRAY = "0.45"
EXPORTS = []


def figure(n=2, height=86):
    fig, axs = plt.subplots(1, n, figsize=ss.figsize("double", height_mm=height))
    fig.subplots_adjust(left=.10, right=.96, bottom=.27, top=.88, wspace=.42)
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             facecolor="none", edgecolor="none", lw=0))
    axs = np.atleast_1d(axs)
    ss.panels(fig, axs, "ABC", x=-.12, y=1.07)
    for ax in axs:
        ax.minorticks_off()
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))
    return fig, axs


def plane(ax, lim=1.5):
    ax.set(xlim=(-lim, lim), ylim=(-lim, lim), aspect="equal",
           xlabel='$x$ (dimensionless)', ylabel='$y$ (dimensionless)')


def footer(ax, label):
    ax.text(.5, -.29, label, transform=ax.transAxes, ha="center", va="top", fontsize=8)


def arrow(ax, p, q, color=BLUE, ls="-", lw=1.6):
    ax.annotate("", xy=q, xytext=p, zorder=9,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, mutation_scale=10, shrinkA=0, shrinkB=0))


def save(fig, name):
    # Exact canvas bounds retain the intended 178-mm column width with tight export.
    for ext in ("pdf", "svg"):
        ss.save(fig, HERE / f"{name}.{ext}", also_png=(ext == "pdf"), dpi=600)
    with Image.open(HERE / f"{name}.png") as im:
        EXPORTS.append({"name": name, "pixel_size": list(im.size),
                        "size_mm": list(ss.output_size_mm(HERE / f"{name}.pdf")),
                        "dpi": 600})
    plt.close(fig)


def contours(ax):
    xx, yy = np.meshgrid(np.linspace(-.3, 2, 160), np.linspace(-.6, 1.65, 160))
    cs = ax.contour(xx, yy, xx**2+2*yy**2, levels=[.5, 1.5, 3, 5],
                    colors="0.6", linewidths=.8)
    ax.clabel(cs, fontsize=7, fmt="%g")
    ax.set(xlim=(-.2, 1.95), ylim=(-.5, 1.5), aspect="equal",
           xlabel='$x$ (dimensionless)', ylabel='$y$ (dimensionless)')
    ax.plot(1, .5, "ko", ms=4)
    ax.annotate('$\\mathbf{a}=(1,1/2)^T$', (1, .5), xytext=(9, -18), textcoords="offset points")


def counterexample():
    fig, (a, b) = figure()
    t = np.linspace(.001, .4, 400)
    a.plot(t, np.zeros_like(t), color="black", ls=":", label='$q(t,0)=0$')
    a.plot(t, t/(1+t*t), color=BLUE, ls="--", label='$q(t,t)$')
    a.plot(t, np.full_like(t, .5), color=RED, label='$q(t,t^2)=1/2$')
    a.plot(0, .5, "o", mfc="white", mec=RED, ms=5)
    a.plot(0, 0, "ko", ms=4)
    a.set(xlim=(-.015, .4), ylim=(-.03, .86), xlabel='$t$ (dimensionless)',
          ylabel='$q$ along path (dimensionless)')
    a.legend(loc="upper left", fontsize=7)
    footer(a, "Curved approach: discontinuity")
    t = np.linspace(-.25, .25, 401)
    for angle, color, ls in [(30, BLUE, "-"), (60, RED, "--"), (90, "black", ":")]:
        u, v = np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))
        b.plot(t, t*u*u*v/(t*t*u**4+v*v), color=color, ls=ls,
               label=rf"$\theta={angle}^\circ$")
    b.plot(0, 0, "ko", ms=4)
    b.set(xlabel='$t$ (dimensionless)', ylabel=r"Difference quotient (dimensionless)")
    b.legend(fontsize=7)
    footer(b, 'Each fixed direction: $D_{\\mathbf{u}}q(\\mathbf{0})=0$')
    save(fig, "fig-06-direction-counterexample")


def field(ax, mode, lim=1.4, color="black"):
    v = np.linspace(-1.2, 1.2, 9)
    x, y = np.meshgrid(v, v)
    if mode == "source": u, w = x, y
    elif mode == "sink": u, w = -x, -y
    elif mode == "uniform": u, w = np.ones_like(x), np.zeros_like(y)
    elif mode == "rotation": u, w = -y, x
    elif mode == "shear": u, w = y, np.zeros_like(y)
    else: raise ValueError(mode)
    ax.quiver(x, y, u, w, angles="xy", scale_units="xy", scale=5,
              color=color, width=.007, headwidth=3.5)
    plane(ax, lim)


def divergence():
    import sys
    import make_field_figures
    make_field_figures.divergence(sys.modules[__name__])


def loop(ax, radius=.65, clockwise=False, color=BLUE):
    ax.add_patch(Circle((0, 0), radius, fill=False, ec=color, lw=1.4))
    sign = -1 if clockwise else 1
    th = sign*np.linspace(.2, .52, 20)
    p = radius*np.column_stack((np.cos(th), np.sin(th)))
    arrow(ax, p[0], p[-1], color)


def curl():
    import sys
    import make_field_figures
    make_field_figures.curl(sys.modules[__name__])


def vortex():
    fig, (a, b) = figure()
    for r in [.38, .7, 1.05, 1.35]:
        loop(a, r)
    theta, radius = np.meshgrid(np.linspace(0, 2*np.pi, 16, endpoint=False), [.45, .9, 1.3])
    x, y = radius*np.cos(theta), radius*np.sin(theta)
    a.quiver(x, y, -y/radius**2, x/radius**2, angles="xy", scale_units="xy",
             scale=6, width=.006, color="black")
    a.plot(0, 0, "kx", ms=7, mew=1.5)
    a.text(.06, -.16, "excluded", fontsize=7,
           bbox=dict(facecolor="white", edgecolor="none", pad=1))
    plane(a)
    footer(a, '$\\mathbf{F}=\\mathbf{e}_\\theta/r:\\quad \\nabla\\times\\mathbf{F}=\\mathbf{0}\\ (r>0)$')
    r = np.linspace(.05, 1.5, 200)
    b.plot(r, np.full_like(r, 2*np.pi), color=BLUE, label='$\\mathbf{F}=\\mathbf{e}_\\theta/r$')
    b.plot(r, 2*np.pi*r*r, color=RED, ls="--", label='$\\mathbf{v}=r\\,\\mathbf{e}_\\theta$')
    b.set(xlim=(0, 1.5), ylim=(0, 15.5), xlabel='Radius $R$ (dimensionless)',
          ylabel=r"Circulation (dimensionless)")
    b.legend(fontsize=7)
    footer(b, "Global circulation around the origin")
    save(fig, "fig-11-vortex-domain")


def decomposition():
    fig, axs = figure(3, height=82)
    fig.subplots_adjust(left=.07, wspace=.50)
    th = np.linspace(0, 2*np.pi, 200)
    initial = np.vstack((np.cos(th), np.sin(th)))
    t = .35
    maps = [np.eye(2)*np.exp(t),
            np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]]),
            np.diag([np.exp(t), np.exp(-t)])]
    captions = ['$A=I$: dilation', '$A^T=-A$: rotation', '$A=\\operatorname{diag}(1,-1)$: strain']
    for ax, matrix, caption in zip(axs, maps, captions):
        plane(ax, 1.65)
        ax.plot(*initial, color=GRAY, ls="--", lw=1.1)
        ax.plot(*(matrix@initial), color=BLUE)
        ax.plot(1, 0, "s", color=GRAY, mfc="white", ms=4)
        end = matrix@np.array([1., 0.])
        ax.plot(*end, "o", color=BLUE, ms=4)
        arrow(ax, (0, 0), end, BLUE, lw=1.1)
        ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
        footer(ax, caption)
    save(fig, "fig-12-jacobian-decomposition")


def physical():
    fig, (a, b) = figure()
    q = np.linspace(-1.5, 1.5, 130)
    x, y = np.meshgrid(q, q)
    T = np.exp(-x*x-y*y)
    cs = a.contour(x, y, T, levels=[.1, .3, .5, .8], colors="0.65", linewidths=.8)
    a.clabel(cs, fontsize=7, fmt="%.1f")
    q = np.linspace(-1.3, 1.3, 9)
    x, y = np.meshgrid(q, q)
    T = np.exp(-x*x-y*y)
    a.quiver(x, y, 2*x*T, 2*y*T, angles="xy", scale_units="xy", scale=3,
             color="black", width=.005)
    plane(a)
    p = np.array([.5, 0])
    a.plot(*p, "ko", ms=4)
    arrow(a, p, (.12, 0), BLUE)
    arrow(a, p, (.88, 0), RED, "--")
    a.text(-.36, .13, '$\\nabla T$', color=BLUE)
    a.text(.76, .14, '$\\mathbf{q}$', color=RED)
    footer(a, '$T=e^{-(x^2+y^2)},\\quad \\mathbf{q}=-\\nabla T$')
    t = np.linspace(0, .7, 160)
    b.plot(t, np.exp(2*t), color=BLUE, label='Area $A/A_0$')
    b.plot(t, np.exp(-2*t), color=RED, ls="--", label='Density $\\rho/\\rho_0$')
    b.plot(t, np.ones_like(t), color="black", ls=":", label="Mass ratio")
    b.set(xlim=(0, .7), ylim=(0, 4.5), xlabel='$t$ (dimensionless)',
          ylabel="Normalized ratio (dimensionless)")
    b.legend(fontsize=7)
    footer(b, '$\\mathbf{v}=(x,y)^T,\\quad \\nabla\\cdot\\mathbf{v}=2$')
    save(fig, "fig-13-physical-meaning")


def previews():
    for part in range((len(EXPORTS)+3)//4):
        names = EXPORTS[part*4:(part+1)*4]
        canvas = Image.new("RGB", (1100, len(names)*580), "white")
        draw = ImageDraw.Draw(canvas)
        for i, item in enumerate(names):
            draw.text((12, i*580+8), item["name"], fill="black")
            with Image.open(HERE / (item["name"]+".png")) as im:
                im.thumbnail((1090, 545))
                canvas.paste(im.convert("RGB"), ((1100-im.width)//2, i*580+30))
        canvas.save(HERE / f"preview-{part+1}.png")
        ImageOps.grayscale(canvas).save(HERE / f"preview-{part+1}-gray.png")


if __name__ == "__main__":
    ss.grayscale_check([BLUE, RED])  # Curves also differ by solid/dashed styles.
    import sys
    import make_geometry_figures as geometry
    context = sys.modules[__name__]
    geometry.partial(context)
    geometry.direction(context)
    geometry.gradient(context)
    geometry.level3d(context)
    geometry.differential(context)
    counterexample()
    geometry.flux(context)
    divergence()
    geometry.circulation(context)
    curl()
    vortex()
    decomposition()
    physical()
    previews()
    (HERE / "figure_manifest.json").write_text(json.dumps(EXPORTS, indent=2), encoding="utf-8")
    for item in EXPORTS:
        assert abs(item["size_mm"][0]-178) < 178*.03, item
    print("Verified: thirteen analytic figures, 178-mm width, PDF/SVG/600-dpi PNG.")
