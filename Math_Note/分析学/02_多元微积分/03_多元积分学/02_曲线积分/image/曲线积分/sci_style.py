"""sci_style - publication-quality matplotlib defaults for SCI figures.

Design rules encoded here:
  - figure width is fixed by the journal column layout (mm), never guessed
  - fonts are sans-serif, sized for the FINAL printed size
  - categorical colours are colourblind-safe and grayscale-distinguishable
  - vector formats are the default, raster needs >= 300 dpi (600 for line art)
  - console output is pure ASCII (Windows cp936/cp1252 safety)

Usage:
    import sci_style as ss
    ss.apply("single")                 # or "1.5" / "double"
    fig, ax = plt.subplots(figsize=ss.figsize("single", ratio=0.75))
    ...
    ss.save(fig, "fig1.pdf", also_png=True)   # prints a size/dpi self-check

Run `python sci_style.py --demo` to render a smoke-test figure.
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

MM_PER_INCH = 25.4

# --------------------------------------------------------------------------
# Column widths (mm). Sources: see references/journal-specs.md
# --------------------------------------------------------------------------
COLUMN_WIDTHS: dict[str, float] = {
    "single": 85.0,  # 1 column  (Nature 88, IEEE 88.9, Elsevier 90)
    "1.5": 114.0,  # 1.5 column
    "double": 178.0,  # 2 columns (Nature 183, IEEE 181.6, Elsevier 190)
}

# --------------------------------------------------------------------------
# Palettes (hex). Okabe-Ito is the default categorical cycle.
# --------------------------------------------------------------------------
OKABE_ITO: dict[str, str] = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
}

CB_DARK2 = ["#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02", "#A6761D"]
CB_SET2 = ["#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494"]
TABLEAU_CB10 = [
    "#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC78BC",
    "#CA9161", "#FBAFE4", "#949494", "#ECE133", "#56B4E9",
]

# Okabe-Ito in an order that keeps adjacent series far apart in luminance.
CATEGORICAL: list[str] = [
    OKABE_ITO["blue"],
    OKABE_ITO["vermillion"],
    OKABE_ITO["green"],
    OKABE_ITO["orange"],
    OKABE_ITO["purple"],
    OKABE_ITO["sky"],
    OKABE_ITO["yellow"],
    OKABE_ITO["black"],
]

SEQUENTIAL = ["viridis", "cividis", "plasma", "magma"]
DIVERGING = ["RdBu_r", "PuOr_r", "coolwarm"]

# Dash patterns: pair with markers whenever there are more than 3 series.
LINESTYLES = ["-", "--", "-.", ":"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]

DEFAULT_FONTS = ["Arial", "Helvetica", "DejaVu Sans"]


# --------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------
def mm(value: float) -> float:
    """Millimetres -> inches."""
    return value / MM_PER_INCH


def figsize(
    width: str | float = "single",
    /,
    *,
    ratio: float | None = None,
    height_mm: float | None = None,
) -> tuple[float, float]:
    """Figure size in inches from a journal width.

    width: "single" | "1.5" | "double" or an explicit width in mm.
    Give exactly one of `height_mm` (absolute) or `ratio` (h/w, default 0.75).
    """
    width_mm = COLUMN_WIDTHS[width] if isinstance(width, str) else float(width)
    if height_mm is not None and ratio is not None:
        raise ValueError("pass either height_mm or ratio, not both")
    if height_mm is not None:
        return mm(width_mm), mm(height_mm)
    return mm(width_mm), mm(width_mm) * (0.75 if ratio is None else ratio)


# --------------------------------------------------------------------------
# Style application
# --------------------------------------------------------------------------
def apply(
    width: str | float = "single",
    /,
    *,
    font_size: float = 8.0,
    line_width: float = 1.6,
    marker_size: float = 4.0,
    label_size: float | None = None,
    legend_size: float | None = None,
    tick_size: float | None = None,
    grid: bool = False,
    spines: str = "open",  # "open" = drop top/right, "box", "all"
    ticks: str = "out",  # "out" | "in" | "inout"
    minor_ticks: bool = True,
    legend_frame: bool = False,
    mathtext: bool = True,
) -> tuple[float, float]:
    """Configure rcParams for publication figures. Returns a default figsize.

    Call once per script, before creating any figure.
    """
    tick_size = font_size if tick_size is None else tick_size
    label_size = font_size if label_size is None else label_size
    legend_size = font_size - 1 if legend_size is None else legend_size

    mpl.rcParams.update(
        {
            # --- fonts -----------------------------------------------------
            "font.family": "sans-serif",
            "font.sans-serif": DEFAULT_FONTS,
            "font.size": font_size,
            "axes.labelsize": label_size,
            "axes.titlesize": label_size + 1,
            "xtick.labelsize": tick_size,
            "ytick.labelsize": tick_size,
            "legend.fontsize": legend_size,
            "figure.titlesize": label_size + 1,
            # embedded vector text stays selectable/editable in Illustrator
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            # --- lines & markers -------------------------------------------
            "lines.linewidth": line_width,
            "lines.markersize": marker_size,
            "lines.markeredgewidth": 0.6,
            "lines.solid_capstyle": "round",
            "errorbar.capsize": 2.0,
            "errorbar.elinewidth": line_width * 0.75,
            "patch.linewidth": 0.6,
            # --- axes ------------------------------------------------------
            "axes.linewidth": 0.8,
            "axes.grid": grid,
            "axes.axisbelow": True,
            "axes.spines.top": spines == "all",
            "axes.spines.right": spines != "open" and spines != "all",
            "axes.prop_cycle": mpl.cycler(color=CATEGORICAL),
            "xtick.direction": ticks,
            "ytick.direction": ticks,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "xtick.minor.size": 1.8,
            "ytick.minor.size": 1.8,
            "xtick.minor.visible": minor_ticks,
            "ytick.minor.visible": minor_ticks,
            "xtick.top": spines != "open",
            "ytick.right": spines != "open" and spines != "box",
            # --- grid ------------------------------------------------------
            "grid.color": "0.85",
            "grid.linewidth": 0.6,
            "grid.linestyle": (0, (2, 2)),
            # --- legend ----------------------------------------------------
            "legend.frameon": legend_frame,
            "legend.handlelength": 2.0,
            "legend.handletextpad": 0.6,
            "legend.columnspacing": 1.2,
            "legend.labelspacing": 0.4,
            "legend.borderaxespad": 0.4,
            # --- layout & export -------------------------------------------
            "figure.figsize": figsize(width),
            "figure.dpi": 150,  # on-screen only
            "savefig.dpi": 600,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
            "savefig.transparent": False,
        }
    )

    resolved = check_fonts()
    if not mathtext:
        mpl.rcParams["mathtext.fontset"] = "dejavusans"
    else:
        # Keep math glyphs in the same family as the body text. Use the font
        # actually resolved on THIS machine: hardcoding "Arial" spams a
        # findfont warning for every math expression on machines without it.
        mpl.rcParams["mathtext.fontset"] = "custom"
        mpl.rcParams.update(
            {
                "mathtext.rm": resolved,
                "mathtext.it": f"{resolved}:italic",
                "mathtext.bf": f"{resolved}:bold",
                "mathtext.default": "it",
            }
        )
    return figsize(width)


def open_axes(fig=None, *, sharex=False, sharey=False, **kw):
    """Convenience: (fig, ax) with constrained layout and no wasted space."""
    if fig is None:
        fig, ax = plt.subplots(layout="constrained", sharex=sharex, sharey=sharey, **kw)
    else:
        ax = fig.add_subplot(layout="constrained", **kw)
    return fig, ax


def style_axes(ax, *, xlabel: str | None = None, ylabel: str | None = None,
               title: str | None = None, legend: bool | str = False,
               grid: bool | None = None, minor: bool | None = None,
               spines: str | None = None, log: str | None = None, **lim) -> None:
    """Apply the publication cosmetics to a single existing axes.

    `legend=True` uses loc="best"; pass a string for an explicit location.
    `log` accepts "x", "y" or "xy".
    """
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title, loc="left")
    if lim:
        ax.set(**lim)
    if log:
        if "x" in log:
            ax.set_xscale("log")
        if "y" in log:
            ax.set_yscale("log")
    if minor is not None:
        if minor:
            ax.minorticks_on()
        else:
            ax.minorticks_off()
    if log:
        if "x" in log:
            ax.set_xscale("log")
        if "y" in log:
            ax.set_yscale("log")
    if spines is not None:
        for side in ("top", "right", "bottom", "left"):
            ax.spines[side].set_visible(side not in spines.replace("only:", ""))
    if grid is not None:
        ax.grid(grid, which="major")
    if legend:
        ax.legend(loc="best" if legend is True else str(legend))


def panels(fig, axes, labels: str = "ABCDEFGH", *, x: float = -0.15, y: float = 1.06,
           size: float = 10.0, weight: str = "bold") -> None:
    """Stamp bold A/B/C panel labels in the upper-left corner of each axes."""
    flat = list(getattr(axes, "flat", axes))
    for ax, lab in zip(flat, labels):
        ax.text(x, y, lab, transform=ax.transAxes, fontsize=size, fontweight=weight,
                ha="left", va="bottom")


def scalebar(ax, length: float, label: str, *, unit: str = "um", color: str = "white",
             loc: str = "lower right", pad: float = 0.06, height: float = 0.012,
             fontsize: float = 7.0) -> None:
    """Add a scale bar to an image axes. `length` is in data units."""
    x0, x1 = sorted(ax.get_xlim())
    y0, y1 = sorted(ax.get_ylim())
    span = (x1 - x0) * height
    fx = 1 - pad if "right" in loc else pad
    fy = pad if "lower" in loc else 1 - pad - height * 3
    xa = x0 + (x1 - x0) * fx - (length if "right" in loc else 0)
    ya = y0 + (y1 - y0) * fy
    ax.plot([xa, xa + length], [ya, ya], color=color, lw=2.0,
            solid_capstyle="butt", clip_on=False)
    ax.text(xa + length / 2, ya + span, f"{label} {unit}", color=color, fontsize=fontsize,
            ha="center", va="bottom")


def colorbar(fig, mappable, ax, label: str = "", *, pad: float = 0.02,
             fraction: float = 0.046, extend: str | None = None):
    """Attach a labelled colorbar sized to sit inside a journal column."""
    cb = fig.colorbar(mappable, ax=ax, fraction=fraction, pad=pad, aspect=20, extend=extend)
    cb.set_label(label, fontsize=mpl.rcParams["axes.labelsize"])
    cb.outline.set_linewidth(0.6)
    return cb


# --------------------------------------------------------------------------
# Export with self-check  (see references/journal-specs.md)
# --------------------------------------------------------------------------
FORMAT_RULES = {
    ".pdf": ("vector", None),
    ".eps": ("vector", None),
    ".svg": ("vector", None),
    ".png": ("raster", 300),
    ".tif": ("raster", 600),
    ".tiff": ("raster", 600),
    ".jpg": ("raster", 300),
    ".jpeg": ("raster", 300),
}


def save(fig, path, *, dpi: int | None = None, also_png: bool = False,
         transparent: bool = False, verbose: bool = True, tight: bool = True) -> Path:
    """Save a figure at journal resolution and verify the result.

    Picks dpi from the extension, writes the file, then re-opens it to report
    the REAL exported size in mm (vector: MediaBox/pt; raster: pixels/dpi),
    the byte count, and whether that width still matches a column class.
    TIFF is written with LZW compression; without it a double-column figure at
    600 dpi lands around 28 MB per panel.
    """
    out = Path(path)
    kind, min_dpi = FORMAT_RULES.get(out.suffix.lower(), ("raster", 300))
    dpi = dpi if dpi is not None else mpl.rcParams["savefig.dpi"]
    if not isinstance(dpi, (int, float)):
        # matplotlib's rcParams default is the STRING 'figure' (or 'auto').
        # That happens whenever apply() was not called first, and it used to
        # blow up on the dpi comparison below with a cryptic TypeError.
        dpi = min_dpi or 600
    if kind == "raster" and dpi < (min_dpi or 300):
        print(f"[warn] {out.suffix} at {dpi} dpi is below the {min_dpi} dpi minimum")
    if mpl.rcParams.get("pdf.fonttype") != 42:
        print("[warn] pdf.fonttype != 42: text will be outlined, not selectable. "
              "Did you forget ss.apply()?")

    # Local extension: tight=False preserves the nominal column-size canvas.
    kwargs = {"dpi": dpi, "transparent": transparent, "bbox_inches": "tight" if tight else None}
    if out.suffix.lower() in {".tif", ".tiff"}:
        kwargs["pil_kwargs"] = {"compression": "tiff_lzw"}

    fig.savefig(out, **kwargs)
    notes = [_size_note(fig, out, dpi)]

    if also_png and out.suffix.lower() != ".png":
        png = out.with_suffix(".png")
        fig.savefig(png, dpi=max(dpi, 300), transparent=transparent,
                    bbox_inches="tight" if tight else None)
        notes.append(f"{png.name} [{_inspect(png)}]")

    if verbose:
        print(f"[ok] {out.name} | {kind} | {' | '.join(notes)}")
    return out


def _size_note(fig, out: Path, dpi: int) -> str:
    """Report the real exported size and how it compares to a column class."""
    w_nom, h_nom = (v * MM_PER_INCH for v in fig.get_size_inches())
    actual = output_size_mm(out, dpi)
    parts = [f"nominal {w_nom:.1f} x {h_nom:.1f} mm"]
    if actual:
        w_act, h_act = actual
        parts[0] = f"nominal {w_nom:.1f} mm -> actual {w_act:.1f} x {h_act:.1f} mm"
        near = min(COLUMN_WIDTHS.values(), key=lambda c: abs(c - w_act))
        off = abs(w_act - near) / near
        if off > 0.03:
            parts.append(f"[note] {w_act:.1f} mm is {off * 100:.0f}% off the nearest "
                         f"column class ({near:.0f} mm)")
    parts.append(_inspect(out))
    return " | ".join(parts)


def output_size_mm(path, dpi: int | None = None) -> tuple[float, float] | None:
    """TRUE printed size of an exported figure, in mm. None if undetectable.

    Why this exists: `bbox_inches='tight'` crops the figure to its content, so
    the real width is usually slightly SMALLER than the nominal figsize. A
    178 mm figure typically exports at ~177 mm. That cropped number is what the
    typesetter sees, so it is the one worth checking against the column spec.

    Understands: PNG/JPG/TIFF (pixels / dpi), PDF (MediaBox), SVG (pt width),
    EPS (BoundingBox). EPS is unsupported by nothing, but note that matplotlib
    writes the HiResBoundingBox in points as well.
    """
    p = Path(path)
    if not p.exists():
        return None
    suffix = p.suffix.lower()
    pt_to_mm = MM_PER_INCH / 72.0
    try:
        if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            from PIL import Image

            if not dpi:
                return None
            with Image.open(p) as im:
                return im.width / dpi * MM_PER_INCH, im.height / dpi * MM_PER_INCH

        head = p.open("rb").read(4000)
        if suffix == ".pdf":
            m = re.search(rb"/MediaBox\s*\[\s*([\d.\s-]+)\]", head)
            if m:
                v = [float(t) for t in m.group(1).split()]
                if len(v) == 4:
                    return (v[2] - v[0]) * pt_to_mm, (v[3] - v[1]) * pt_to_mm
        elif suffix == ".svg":
            wm = re.search(rb'width="([\d.]+)pt"', head)
            hm = re.search(rb'height="([\d.]+)pt"', head)
            if wm and hm:
                return float(wm.group(1)) * pt_to_mm, float(hm.group(1)) * pt_to_mm
        elif suffix == ".eps":
            m = re.search(rb"%%(?:HiRes)?BoundingBox:\s*([\d.\s-]+)", head)
            if m:
                v = [float(t) for t in m.group(1).split()]
                if len(v) == 4:
                    return (v[2] - v[0]) * pt_to_mm, (v[3] - v[1]) * pt_to_mm
    except Exception:
        return None
    return None


def _inspect(path: Path) -> str:
    """ASCII status string: size + (for raster) real pixel dimensions."""
    if not path.exists():
        return "MISSING"
    nbytes = path.stat().st_size
    if nbytes == 0:
        return "EMPTY FILE"
    try:
        from PIL import Image  # optional dependency

        with Image.open(path) as im:
            px = f"{im.width}x{im.height} px"
            mode = im.mode
        return f"{px} {mode} {nbytes / 1024:.0f} KiB"
    except Exception:
        head = path.open("rb").read(5)
        magic = "PDF" if head.startswith(b"%PDF") else head[:4].decode("ascii", "replace")
        return f"{magic} {nbytes / 1024:.0f} KiB"


def _linearize(c: float) -> float:
    """Inverse sRGB transfer function (IEC 61966-2-1)."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(color) -> float:
    """WCAG relative luminance of a colour (0 = black, 1 = white).

    Computed on LINEARISED RGB - applying the 0.2126/0.7152/0.0722 weights to
    gamma-encoded values gives a different, wrong number.
    """
    from matplotlib.colors import to_rgb

    r, g, b = (_linearize(c) for c in to_rgb(color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def grayscale_check(colors, *, hard: float = 0.05, soft: float = 0.12,
                    verbose: bool = True):
    """Check whether a set of series colours survives a greyscale print.

    Important caveat: Okabe-Ito and the ColorBrewer sets are optimised for HUE
    separation under colour-vision deficiency, NOT for LUMINANCE separation.
    Several of their pairs sit within a few percent of each other in greyscale,
    so a `[note]` here does not mean "bad palette" - it means "also vary the
    marker and the linestyle", which is required practice above three series
    regardless of palette.

    `[warn]` (gap < `hard`)  : visually identical in greyscale
    `[note]` (gap < `soft`)  : same greyscale family, reinforce with markers
    Returns the list of luminances, in the order given.
    """
    lums = [relative_luminance(c) for c in colors]
    if verbose:
        for c, v in zip(colors, lums):
            print(f"[lum] {c}  {v:.3f}")
        hard_bad, soft_bad = [], []
        for i in range(len(lums)):
            for j in range(i + 1, len(lums)):
                gap = abs(lums[i] - lums[j])
                if gap < hard:
                    hard_bad.append((colors[i], colors[j], gap))
                elif gap < soft:
                    soft_bad.append((colors[i], colors[j], gap))
        if len(set(colors)) == 1:
            print("[note] single-colour set: nothing to separate")
        for a, b, gap in hard_bad:
            print(f"[warn] {a} vs {b}: luminance gap {gap:.3f} < {hard} "
                  f"- indistinguishable in greyscale, change the marker")
        for a, b, gap in soft_bad:
            print(f"[note] {a} vs {b}: luminance gap {gap:.3f} "
                  f"- reinforce with marker/linestyle")
        if not hard_bad and not soft_bad:
            print("[ok] all colour pairs separable in greyscale")
    return lums


def luminance_ramp(n: int, cmap: str = "cividis", lo: float = 0.15,
                   hi: float = 0.88) -> list[str]:
    """n colours sampled along a perceptually uniform map: monotone luminance.

    Use this when the figure must survive a pure greyscale reproduction with no
    colour cue at all (photocopied thesis appendix, faxed manuscript). By
    construction the colours differ in luminance, which is exactly what
    Okabe-Ito does NOT guarantee - see `grayscale_check`.
    """
    import numpy as np
    from matplotlib.colors import to_hex

    return [to_hex(plt.get_cmap(cmap)(v)) for v in np.linspace(lo, hi, n)]


def check_fonts(fonts=None) -> str:
    """Return the first available font of preference (quiet, no warning spam)."""
    from matplotlib import font_manager

    for name in fonts or DEFAULT_FONTS:
        try:
            if Path(font_manager.findfont(name, fallback_to_default=False)).exists():
                return name
        except Exception:
            continue
    return "DejaVu Sans"


# --------------------------------------------------------------------------
def _demo(path: Path = Path("sci_style_demo.png")) -> None:
    import numpy as np

    apply("double")
    fig, axs = plt.subplots(1, 2, figsize=figsize("double", ratio=0.36),
                            layout="constrained")
    x = np.linspace(0, 10, 200)
    for i, ls in enumerate(LINESTYLES):
        axs[0].plot(x, np.sin(x - i) * np.exp(-x / 12), ls, marker=MARKERS[i],
                    markevery=25, label=f"series {i + 1}")
    axs[0].set(xlabel="Time (s)", ylabel="Amplitude (a.u.)", xlim=(0, 10))
    axs[0].legend(loc="upper right", ncol=2)

    rng = np.random.default_rng(0)
    vals = [rng.normal(m, 1.0, 60) for m in (0, 1.2, 2.1)]
    axs[1].boxplot(vals, widths=0.5, showfliers=False, patch_artist=True,
                   boxprops={"facecolor": "0.9"})
    for i, v in enumerate(vals, start=1):
        axs[1].plot(np.full(v.size, i) + rng.normal(0, 0.05, v.size), v, ".",
                    markersize=2, color="0.35", alpha=0.7)
    axs[1].set(xlabel="Condition", ylabel="Response (mV)")

    panels(fig, axs, "AB")
    save(fig, path, verbose=True)
    print("-- categorical (Okabe-Ito): hue-safe, NOT greyscale-safe --")
    grayscale_check(CATEGORICAL[:4])
    print("-- monotone luminance ramp: greyscale-safe --")
    grayscale_check(luminance_ramp(4))


if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv:
        _demo(Path(sys.argv[sys.argv.index("--demo") + 1])
              if len(sys.argv) > sys.argv.index("--demo") + 1 else Path("sci_style_demo.png"))
    else:
        print("sci_style: publication-quality matplotlib defaults")
        print(f"  column widths (mm): {COLUMN_WIDTHS}")
        print(f"  categorical cycle : {CATEGORICAL}")
        print(f"  font resolved     : {check_fonts()}")
        print("  run `python sci_style.py --demo` for a smoke-test figure")
