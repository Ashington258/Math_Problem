"""Analytic illustrations for the mean-value-theorems note.

Run: python make_figures.py
Dependencies: numpy, matplotlib, Pillow. All coordinates are dimensionless.
Local sci_style.py retains the chapter's tight=False export extension.
"""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from PIL import Image, ImageOps
import sci_style as ss

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
OUT = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ['Microsoft YaHei', 'DejaVu Sans']
ss.apply('double', font_size=8, legend_size=7, minor_ticks=False)
plt.rcParams.update({'mathtext.fontset': 'dejavusans',
                     'axes.unicode_minus': False, 'savefig.bbox': None})
BLUE, ORANGE, GRAY = '#0072B2', '#D55E00', '0.38'
PALE = '#EAF2F8'
MANIFEST = []


def pair(left_footer, right_footer, height=92):
    fig, axs = plt.subplots(1, 2, figsize=ss.figsize('double', height_mm=height))
    fig.subplots_adjust(left=.10, right=.98, bottom=.23, top=.89, wspace=.43)
    for ax, letter in zip(axs, 'AB'):
        ax.text(0, 1.07, letter, transform=ax.transAxes, weight='bold', fontsize=10)
        ax.set(xlabel='$x$（无量纲）', ylabel='$y$（无量纲）')
        ax.locator_params(nbins=4)
    fig.text(.28, .025, left_footer, ha='center', va='bottom', fontsize=8)
    fig.text(.79, .025, right_footer, ha='center', va='bottom', fontsize=8)
    return fig, axs[0], axs[1]


def point(ax, x, y, label=None, offset=(6, 7), color=ORANGE, marker='o'):
    ax.plot(x, y, marker, color=color, ms=4, zorder=6)
    if label:
        ax.annotate(label, (x, y), xytext=offset, textcoords='offset points',
                    fontsize=8, color=color)


def horizontal(ax, y, label=None):
    ax.axhline(y, color=GRAY, ls='--', lw=1)
    if label:
        ax.text(.04, .91, label, transform=ax.transAxes, fontsize=8)


def save(fig, stem, description):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    artists = list(fig.texts)
    for ax in fig.axes:
        artists.extend(ax.texts)
        artists.extend(ax.get_legend().get_texts() if ax.get_legend() else [])
        for axis in (ax.xaxis, ax.yaxis):
            artists.append(axis.label)
            lo, hi = sorted(axis.get_view_interval())
            artists.extend(t for loc, t in zip(axis.get_ticklocs(), axis.get_ticklabels())
                           if lo <= loc <= hi)
    for artist in artists:
        if artist.get_visible() and artist.get_text():
            box = artist.get_window_extent(renderer)
            assert box.x0 >= -2 and box.y0 >= -2 and box.x1 <= fig.bbox.width+2 and box.y1 <= fig.bbox.height+2, (stem, artist.get_text(), box)
    ss.save(fig, OUT / f'{stem}.pdf', also_png=True, dpi=600, tight=False)
    ss.save(fig, OUT / f'{stem}.svg', dpi=600, tight=False, verbose=False)
    size = ss.output_size_mm(OUT / f'{stem}.pdf')
    assert size and abs(size[0]-178) < .1
    with Image.open(OUT / f'{stem}.png') as im:
        assert min(im.info['dpi']) >= 599
    MANIFEST.append({'stem': stem, 'size_mm': [round(v, 3) for v in size],
                     'dpi': 600, 'description': description})
    plt.close(fig)


def intermediate_values():
    fig, ax, bx = pair('水平线截取中间函数值', '端点异号保证内部至少一个零点')
    x = np.linspace(0, 2, 501)
    f = lambda t: t+.35*np.sin(np.pi*t)
    ax.plot(x, f(x), color=BLUE)
    horizontal(ax, 1, r'$\mu=1$')
    for a in (0, 2):
        point(ax, a, f(a), color=GRAY, marker='s')
    point(ax, 1, 1, r'$f(\xi)=\mu$', offset=(9, -20))
    ax.plot([1, 1], [0, 1], ':', color=ORANGE, lw=1)
    ax.text(.08, 1.64, r'$f(x)=x+0.35\sin(\pi x)$', fontsize=8)
    ax.set(xlim=(-.08, 2.08), ylim=(-.12, 2.15))
    z = np.linspace(-1, 1, 501)
    bx.plot(z, z**3+z, color=BLUE)
    horizontal(bx, 0)
    point(bx, -1, -2, color=GRAY, marker='s')
    point(bx, 1, 2, color=GRAY, marker='s')
    point(bx, 0, 0, r'$\xi=0$', offset=(10, -20))
    bx.text(-.85, 1.65, r'$f(x)=x^3+x$', fontsize=8)
    bx.set(xlim=(-1.08, 1.08), ylim=(-2.3, 2.3))
    save(fig, 'fig-01-intermediate-values', '介值定理与零点定理的水平线相交图像。')


def fermat():
    fig, ax, bx = pair('内点可导的局部极小值处切线水平', '水平切线不能反推出局部极值')
    x = np.linspace(-1, 1, 501)
    ax.plot(x, 1+x*x, color=BLUE, label=r'$f(x)=1+x^2$')
    ax.plot([-.65, .65], [1, 1], '--', color=ORANGE, label='水平切线')
    point(ax, 0, 1, r'$f\,\prime(0)=0$', offset=(10, 15))
    ax.set(xlim=(-1.1, 1.1), ylim=(.72, 2.25))
    ax.legend(loc='upper center', frameon=False)
    bx.plot(x, x**3, color=BLUE, label=r'$f(x)=x^3$')
    bx.plot([-.7, .7], [0, 0], '--', color=ORANGE, label='水平切线')
    point(bx, 0, 0, r'$f\,\prime(0)=0$', offset=(7, -23))
    bx.set(xlim=(-1.1, 1.1), ylim=(-1.2, 1.2))
    bx.legend(loc='upper left', frameon=False)
    save(fig, 'fig-02-fermat', '费马引理的必要条件，以及 x³ 的逆命题反例。')


def differential_mvt():
    fig, ax, bx = pair('Rolle：端点等高，中间存在水平切线', 'Lagrange：某处切线与端点割线平行')
    x = np.linspace(0, 2, 501)
    ax.plot(x, 1-(x-1)**2, color=BLUE, label=r'$f(x)=1-(x-1)^2$')
    ax.plot([0, 2], [0, 0], ':', color=GRAY, label='等高端点连线')
    ax.plot([.45, 1.55], [1, 1], '--', color=ORANGE, label='水平切线')
    for a in (0, 2):
        point(ax, a, 0, color=GRAY, marker='s')
    point(ax, 1, 1, r'$\xi=1$', offset=(5, -23))
    ax.set(xlim=(-.1, 2.1), ylim=(-.15, 1.6))
    ax.legend(loc='upper center', frameon=False)
    bx.plot(x, x*x, color=BLUE, label=r'$f(x)=x^2$')
    bx.plot(x, 2*x, ':', color=GRAY, label='割线：斜率 2')
    tx = np.array([.35, 1.8])
    bx.plot(tx, 2*tx-1, '--', color=ORANGE, label='切线：斜率 2')
    for a in (0, 2):
        point(bx, a, a*a, color=GRAY, marker='s')
    point(bx, 1, 1, r'$\xi=1$', offset=(8, -22))
    bx.set(xlim=(-.1, 2.1), ylim=(-.55, 4.6))
    bx.legend(loc='upper left', frameon=False)
    save(fig, 'fig-03-differential-mvt', 'Rolle 的水平切线与 Lagrange 的平行切线。')


def cauchy():
    fig, ax, bx = pair('参数曲线：切线与端点弦平行', '辅助函数 H 端点相等，应用 Rolle')
    t = np.linspace(1, 2, 501)
    xi, k = 14/9, 7/3
    ax.plot(t*t, t**3, color=BLUE, label=r'$(g(t),f(t))=(t^2,t^3)$')
    X = np.array([1, 4])
    ax.plot(X, 1+k*(X-1), ':', color=GRAY, label=r'弦斜率 $7/3$')
    xx = np.linspace(1.35, 3.6, 101)
    ax.plot(xx, xi**3+k*(xx-xi**2), '--', color=ORANGE, label=r'切线斜率 $7/3$')
    point(ax, xi**2, xi**3, r'$t=\xi=14/9$', offset=(6, -23))
    point(ax, 1, 1, color=GRAY, marker='s')
    point(ax, 4, 8, color=GRAY, marker='s')
    ax.set(xlim=(.85, 4.15), ylim=(.1, 8.9),
           xlabel='$g(t)$（无量纲）', ylabel='$f(t)$（无量纲）')
    ax.legend(loc='upper left', frameon=False, fontsize=7)
    h = t**3-k*t*t
    bx.plot(t, h, color=BLUE, label=r'$H(t)=t^3-\frac{7}{3}t^2$')
    bx.plot([1, 2], [-4/3, -4/3], ':', color=GRAY)
    hx = xi**3-k*xi**2
    bx.plot([1.25, 1.85], [hx, hx], '--', color=ORANGE)
    point(bx, xi, hx, r'$H\,\prime(\xi)=0$', offset=(-30, -23))
    point(bx, 1, -4/3, color=GRAY, marker='s')
    point(bx, 2, -4/3, color=GRAY, marker='s')
    bx.text(1.10, -1.25, r'$H(1)=H(2)=-4/3$', fontsize=8)
    bx.set(xlim=(.96, 2.04), ylim=(-2.05, -.95),
           xlabel='$t$（无量纲）', ylabel='$H(t)$（无量纲）')
    bx.legend(loc='upper center', frameon=False)
    save(fig, 'fig-04-cauchy', '柯西中值定理的参数曲线解释与 Rolle 辅助函数。')


def taylor():
    fig, ax, bx = pair('二阶 Taylor 多项式与函数值的差', '余项落在三阶导数给出的界之间')
    x = np.linspace(0, 1, 501)
    f, p = np.exp(x), 1+x+x*x/2
    ax.plot(x, f, color=BLUE, label=r'$e^x$')
    ax.plot(x, p, '--', color=ORANGE, label=r'$P_2=1+x+x^2/2$')
    ax.plot([1, 1], [p[-1], f[-1]], color='black', lw=2)
    point(ax, 1, f[-1], color=BLUE)
    point(ax, 1, p[-1], color=ORANGE, marker='s')
    ax.annotate(r'$R_2(1)=e-5/2$', xy=(1, (np.e+2.5)/2), xytext=(.16, 2.46),
                arrowprops={'arrowstyle': '->', 'color': GRAY, 'lw': .8}, fontsize=8)
    ax.set(xlim=(-.02, 1.08), ylim=(.9, 3.05))
    ax.legend(loc='upper left', frameon=False)
    rem = f-p
    bx.fill_between(x, x**3/6, np.e*x**3/6, color=PALE)
    bx.plot(x, rem, color=BLUE, label=r'$R_2(x)=e^x-P_2(x)$')
    bx.plot(x, x**3/6, ':', color=GRAY, label=r'下界 $x^3/6$')
    bx.plot(x, np.e*x**3/6, '--', color=ORANGE, label=r'上界 $ex^3/6$')
    bx.set(xlim=(0, 1.03), ylim=(0, .49), ylabel='$R_2$（无量纲）')
    bx.legend(loc='upper left', frameon=False)
    save(fig, 'fig-05-taylor', '指数函数的二阶 Taylor 多项式、拉格朗日余项与一致上界。')


def integral_first():
    fig, ax, bx = pair('曲线下面积 = 平均高度 × 区间长度', '加权后两曲线间的正负面积抵消')
    x = np.linspace(0, 1, 501)
    xi = 1/np.sqrt(3)
    ax.fill_between(x, 0, 1+x*x, color=PALE)
    ax.plot(x, 1+x*x, color=BLUE, label=r'$f(x)=1+x^2$')
    ax.add_patch(Rectangle((0, 0), 1, 4/3, fill=False, edgecolor=ORANGE, lw=1.6, ls='--'))
    ax.axhline(4/3, color=ORANGE, ls='--', lw=1.2, label=r'$f(\xi)=4/3$')
    point(ax, xi, 4/3, r'$\xi=1/\sqrt{3}$', offset=(-25, 18))
    ax.set(xlim=(-.03, 1.03), ylim=(0, 2.3))
    ax.legend(loc='upper left', frameon=False)
    fg, mg = 2*x+2*x**3, 3*x
    bx.fill_between(x, fg, mg, where=fg <= mg, color='0.92', interpolate=True)
    bx.fill_between(x, fg, mg, where=fg >= mg, facecolor=PALE, hatch='///',
                    edgecolor='0.6', linewidth=0, interpolate=True)
    bx.plot(x, fg, color=BLUE, label=r'$f(x)g(x)$')
    bx.plot(x, mg, '--', color=ORANGE, label=r'$f(\xi)g(x)=3x$')
    xi = 1/np.sqrt(2)
    point(bx, xi, 3*xi, r'$\xi=1/\sqrt{2}$', offset=(-60, 20))
    bx.text(.46, .44, r'$g(x)=2x$', fontsize=8)
    bx.set(xlim=(0, 1.03), ylim=(0, 4.6), ylabel='加权函数值（无量纲）')
    bx.legend(loc='upper left', frameon=False)
    save(fig, 'fig-06-integral-first', '积分第一中值定理的等面积矩形与非负权重推广。')


def integral_second():
    fig, ax, bx = pair('单调函数可用端点高度的阶梯替代', '乘以 g 后，积分仍可在某个分点相等')
    x = np.linspace(0, 1, 601)
    xi = np.sqrt(7/3)-1
    ax.plot(x, 2-x, color=BLUE, label=r'$f(x)=2-x$')
    ax.plot([0, xi], [2, 2], '--', color=ORANGE, label='端点值阶梯')
    ax.plot([xi, 1], [1, 1], '--', color=ORANGE)
    ax.plot([xi, xi], [1, 2], ':', color=GRAY, lw=.8)
    point(ax, xi, 2, color=ORANGE)
    ax.plot(xi, 1, 'o', ms=4, mfc='white', mec=ORANGE)
    ax.set(xlim=(-.03, 1.03), ylim=(.65, 2.55))
    ax.set_xticks([0, xi, 1], ['$0$', r'$\xi$', '$1$'])
    ax.legend(loc='upper right', frameon=False)
    # Separate branches preserve the step's jump; no interpolated fake segment.
    for lo, hi, height in [(0, xi, 2), (xi, 1, 1)]:
        xx = np.linspace(lo, hi, 301)
        yy = (2-xx)*(1+xx)
        step = height*(1+xx)
        bx.fill_between(xx, yy, step, color=PALE if height == 2 else '0.92',
                        hatch=None if height == 2 else '///', edgecolor='0.6', linewidth=0)
        bx.plot(xx, step, '--', color=ORANGE,
                label=r'$h_\xi(x)g(x)$' if height == 2 else None)
    bx.plot(x, (2-x)*(1+x), color=BLUE, label=r'$f(x)g(x)$')
    bx.plot([xi, xi], [1+xi, 2*(1+xi)], ':', color=GRAY, lw=.8)
    bx.text(.08, 1.12, r'$g(x)=1+x$', fontsize=8)
    bx.text(.08, .78, r'$\int fg=\int h_\xi g=13/6$', fontsize=8)
    bx.set(xlim=(0, 1.03), ylim=(.55, 3.9), ylabel='加权函数值（无量纲）')
    bx.set_xticks([0, xi, 1], ['$0$', r'$\xi$', '$1$'])
    bx.legend(loc='upper left', frameon=False)
    save(fig, 'fig-07-integral-second', '积分第二中值定理：端点加权阶梯与单调函数具有相同加权积分。')


def derivative(t):
    return 2*t*np.sin(1/t)-np.cos(1/t)


def darboux():
    fig, ax, bx = pair('原函数在 0 处可导，且 f′(0) = 0', '导函数在 0 处不连续，但不跳过中间值')
    # Uniform reciprocal spacing resolves the increasingly rapid oscillations.
    positive = 1/np.linspace(1/.30, 1/.0003, 40000)
    positive.sort()
    x = np.r_[-positive[::-1], 0, positive]
    y = np.zeros_like(x)
    mask = x != 0
    y[mask] = x[mask]**2*np.sin(1/x[mask])
    ax.plot(x, y, color=BLUE, lw=1.1)
    ax.plot([-.16, .16], [0, 0], '--', color=ORANGE, lw=1)
    point(ax, 0, 0, r'$f\,\prime(0)=0$', offset=(-14, 19))
    ax.text(-.28, .065, r'$f(x)=x^2\sin(1/x),\ f(0)=0$', fontsize=8)
    ax.set(xlim=(-.31, .31), ylim=(-.06, .08))
    bx.plot(positive, derivative(positive), color=BLUE, lw=.8)
    bx.plot(0, 0, 'o', color='black', ms=4)
    n = np.arange(2, 9)
    minus, plus = 1/(2*np.pi*n), 1/((2*n+1)*np.pi)
    bx.plot(minus, -np.ones_like(minus), 'o', ms=4, mfc='white', mec='black')
    bx.plot(plus, np.ones_like(plus), 's', ms=4, mfc='white', mec='black')
    lam = .3
    bx.axhline(lam, color=ORANGE, ls='--', lw=1)
    lo, hi = 1/(5*np.pi), 1/(4*np.pi)
    for _ in range(60):
        mid = (lo+hi)/2
        if derivative(mid) > lam:
            lo = mid
        else:
            hi = mid
    xi = (lo+hi)/2
    assert abs(derivative(xi)-lam) < 1e-12
    point(bx, xi, lam, marker='D')
    bx.text(.18, .43, r'$\lambda=0.3$', color=ORANGE, fontsize=8)
    bx.set(xlim=(-.006, .305), ylim=(-1.35, 1.45), ylabel=r'$f\,\prime(x)$（无量纲）')
    save(fig, 'fig-08-darboux', '原函数可导而导函数振荡不连续；两列点趋于 0 时导数分别恒为 ±1。')


def previews():
    for page in range(2):
        canvas = Image.new('RGB', (2000, 1050), 'white')
        for j, record in enumerate(MANIFEST[page*4:page*4+4]):
            with Image.open(OUT / (record['stem']+'.png')) as im:
                tile = im.convert('RGB')
                tile.thumbnail((1000, 525), Image.Resampling.LANCZOS)
                canvas.paste(tile, ((j % 2)*1000, (j // 2)*525))
        canvas.save(OUT / f'preview-{page+1}.png')
        ImageOps.grayscale(canvas).save(OUT / f'preview-{page+1}-gray.png')


if __name__ == '__main__':
    ss.grayscale_check([BLUE, ORANGE])
    intermediate_values()
    fermat()
    differential_mvt()
    cauchy()
    taylor()
    integral_first()
    integral_second()
    darboux()
    (OUT / 'figure_manifest.json').write_text(
        json.dumps(MANIFEST, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    previews()
