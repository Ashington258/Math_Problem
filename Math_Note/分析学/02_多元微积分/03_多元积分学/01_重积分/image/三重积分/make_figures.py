"""Reproduce the triple-integral diagrams from analytic geometry.

Dependencies: numpy, matplotlib, Pillow. Run: python make_figures.py
All plotted quantities are dimensionless; no measured data or uncertainty.
Local sci_style.py includes the chapter's tight=False canvas-size extension.
"""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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
BLUE, ORANGE = '#0072B2', '#D55E00'
PALE, GRAY = '#EAF2F8', '0.40'
MANIFEST = []


def new_figure(space=False):
    fig = plt.figure(figsize=ss.figsize('double', height_mm=95))
    if space:
        ax = fig.add_axes([.005, .14, .49, .75], projection='3d')
        bx = fig.add_axes([.63, .23, .34, .62])
    else:
        ax = fig.add_axes([.09, .23, .35, .62])
        bx = fig.add_axes([.63, .23, .35, .62])
    fig.text(.025, .94, 'A', weight='bold', fontsize=10)
    fig.text(.56, .94, 'B', weight='bold', fontsize=10)
    for a in (ax, bx):
        if a.name != '3d':
            a.locator_params(nbins=4)
    return fig, ax, bx


def footer(fig, left, right):
    fig.text(.265, .035, left, ha='center', va='bottom', fontsize=8)
    fig.text(.79, .035, right, ha='center', va='bottom', fontsize=8)


def save(fig, stem, description):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    # Check 2-D text against the canvas; 3-D tick extents are not projected
    # by get_window_extent, so their layout is checked in the previews.
    artists = list(fig.texts)
    for ax in fig.axes:
        artists.extend(ax.texts)
        for axis in ([] if ax.name == '3d' else [ax.xaxis, ax.yaxis]):
            artists.append(axis.label)
            lo, hi = sorted(axis.get_view_interval())
            artists.extend(text for loc, text in zip(axis.get_ticklocs(), axis.get_ticklabels())
                           if lo <= loc <= hi)
    for artist in artists:
        if artist.get_visible() and artist.get_text():
            b = artist.get_window_extent(renderer)
            assert b.x0 >= -2 and b.y0 >= -2 and b.x1 <= fig.bbox.width+2 and b.y1 <= fig.bbox.height+2, (stem, artist.get_text(), b)
    ss.save(fig, OUT / f'{stem}.pdf', also_png=True, dpi=600, tight=False)
    ss.save(fig, OUT / f'{stem}.svg', dpi=600, tight=False, verbose=False)
    size = ss.output_size_mm(OUT / f'{stem}.pdf')
    assert size and abs(size[0]-178)/178 < .03
    with Image.open(OUT / f'{stem}.png') as im:
        assert min(im.info.get('dpi', (0, 0))) >= 599
    MANIFEST.append({'stem': stem, 'size_mm': [round(v, 3) for v in size],
                     'dpi': 600, 'description': description})
    plt.close(fig)


def slices():
    fig, ax, bx = new_figure(space=True)
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    ax.add_collection3d(Poly3DCollection(
        [vertices[[0, 1, 2]], vertices[[0, 1, 3]],
         vertices[[0, 2, 3]], vertices[[1, 2, 3]]],
        facecolors='0.85', alpha=.14, edgecolors='none'))
    for i, j in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        ax.plot(*vertices[[i, j]].T, color=GRAY, lw=1)
    t = .35
    section = np.array([[0, 0, t], [1-t, 0, t], [0, 1-t, t]])
    ax.add_collection3d(Poly3DCollection([section], facecolors=BLUE, alpha=.22,
                                       edgecolors=BLUE, linewidths=1.2))
    x, y = .2, .25
    ax.plot([x, x], [y, y], [0, 1-x-y], color=ORANGE, lw=2.8)
    ax.scatter([x, x], [y, y], [0, 1-x-y], color=ORANGE, s=17, depthshade=False)
    ax.text2D(.03, .91, '$z=0.35$', transform=ax.transAxes, color=BLUE, fontsize=7)
    ax.set(xlim=(0, 1.02), ylim=(0, 1.02), zlim=(0, 1.02),
           xlabel='$x$ (dim.)', ylabel='$y$ (dim.)', zlabel='$z$ (dim.)')
    ax.set_box_aspect((1, 1, 1))
    ax.set_proj_type('ortho')
    ax.view_init(elev=24, azim=-55)
    ax.grid(False)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_ticks([0, .5, 1])
        axis.set_tick_params(labelsize=7, pad=0)
        axis.pane.set_visible(False)
        axis.labelpad = 1
    ts = np.linspace(0, 1, 401)
    area = (1-ts)**2/2
    bx.fill_between(ts, 0, area, color=PALE)
    bx.plot(ts, area, color=BLUE)
    bx.plot(t, (1-t)**2/2, 'o', color=BLUE, ms=4)
    bx.plot([t, t], [0, (1-t)**2/2], '--', color=GRAY, lw=1)
    bx.text(.24, .43, '$A(t)=(1-t)^2/2$', fontsize=8)
    bx.text(.32, .31, '$V=\\int_0^1 A(t)\\,\\mathrm{d}t=1/6$', fontsize=8)
    bx.set(xlim=(0, 1), ylim=(0, .53), xlabel='$t=z$（无量纲）',
           ylabel='$A(t)$（无量纲）')
    footer(fig, '竖直线段与水平三角形截面', '截面积沿高度累积为体积')
    save(fig, 'fig-01-slices', '单位四面体的投影切片、水平截面与截面积函数。')


def split_order():
    fig, ax, bx = new_figure()
    r = np.linspace(0, 1, 401)
    ax.fill_between(r, r*r, 2, color='0.92')
    ax.plot(r, r*r, color=BLUE, label='$z=r^2$')
    ax.plot([0, 1], [2, 2], color=GRAY)
    ax.plot([1, 1], [1, 2], color=GRAY)
    ax.plot([.65, .65], [.65**2, 2], color=ORANGE, lw=2)
    ax.plot([0, np.sqrt(.55)], [.55, .55], '--', color=BLUE, lw=1.8)
    ax.plot([0, 1], [1.5, 1.5], '--', color=BLUE, lw=1.8)
    ax.text(.03, 1.58, '$r\\leq1$', fontsize=8)
    ax.text(.04, .65, '$r\\leq\\sqrt{z}$', fontsize=8)
    ax.text(.70, .28, '$z=r^2$', color=BLUE, fontsize=8)
    ax.text(.10, 2.08, '$z=2$', fontsize=8)
    ax.set(xlim=(0, 1.13), ylim=(0, 2.26),
           xlabel='$r$（无量纲）', ylabel='$z$（无量纲）')
    z = np.linspace(0, 2, 401)
    a = np.pi*np.minimum(z, 1)
    bx.fill_between(z, 0, a, color=PALE)
    bx.plot(z, a, color=BLUE)
    bx.plot(1, np.pi, 'o', color=ORANGE, ms=4)
    bx.axvline(1, color=GRAY, ls='--', lw=1)
    bx.text(.24, 2.1, '$A=\\pi z$', rotation=40, fontsize=8)
    bx.text(1.27, 3.37, '$A=\\pi$', fontsize=8)
    bx.text(.40, .60, '$V=3\\pi/2$', fontsize=8)
    bx.set(xlim=(0, 2.08), ylim=(0, 3.8),
           xlabel='$z$（无量纲）', ylabel='$A(z)$（无量纲）')
    bx.set_xticks([0, 1, 2])
    bx.set_yticks([0, np.pi/2, np.pi], ['$0$', '$\\pi/2$', '$\\pi$'])
    footer(fig, '母线区域：竖直实线、水平虚线', '在 z = 1 处切换截面半径公式')
    save(fig, 'fig-02-order-split', '柱面内、抛物面上方的区域，截面积在 z=1 处分段。')


def cylindrical():
    fig, ax, bx = new_figure()
    r = np.linspace(0, 1, 401)
    lower, upper = r*r, 2-r*r
    ax.fill_between(r, lower, upper, color='0.92')
    ax.plot(r, lower, color=BLUE, label='$z=r^2$')
    ax.plot(r, upper, '--', color=GRAY, label='$z=2-r^2$')
    r0 = .55
    ax.plot([r0, r0], [r0*r0, 2-r0*r0], color=ORANGE, lw=2.3)
    ax.text(.12, .65, '$2-2r^2$', color=ORANGE, fontsize=8)
    ax.set(xlim=(0, 1.08), ylim=(0, 2.15),
           xlabel='$r$（无量纲）', ylabel='$z$（无量纲）')
    ax.legend(loc='upper right', frameon=False)
    weight = 2*np.pi*r*(upper-lower)
    bx.fill_between(r, 0, weight, color=PALE)
    bx.plot(r, weight, color=BLUE)
    bx.text(.10, 5.15, '$w(r)=4\\pi r(1-r^2)$', fontsize=8)
    bx.text(.30, 1.6, '$V=\\int_0^1w(r)\\,\\mathrm{d}r=\\pi$', fontsize=8)
    bx.set(xlim=(0, 1.02), ylim=(0, 5.7),
           xlabel='$r$（无量纲）', ylabel='$w(r)$（无量纲）')
    footer(fig, '两抛物面之间：厚度为 2 − 2r²', '厚度 × 整周薄环权重 2πr')
    save(fig, 'fig-03-cylindrical', '双抛物面立体的母线区域与径向体积权重。')


def spherical():
    fig, ax, bx = new_figure()
    phi = np.linspace(0, np.pi/4, 301)
    s, z = np.sin(phi), np.cos(phi)
    poly = np.vstack([[0, 0], np.c_[s, z], [0, 0]])
    ax.add_patch(Polygon(poly, facecolor='0.92', edgecolor='none'))
    ax.plot(s, z, color=BLUE, lw=1.8)
    ax.plot([0, 1/np.sqrt(2)], [0, 1/np.sqrt(2)], color=GRAY)
    p = np.pi/6
    ax.plot([0, np.sin(p)], [0, np.cos(p)], color=ORANGE, lw=2)
    sc = .38
    ax.plot([sc, sc], [sc, np.sqrt(1-sc*sc)], '--', color=BLUE, lw=1.5)
    arc = np.linspace(0, p, 80)
    ax.plot(.28*np.sin(arc), .28*np.cos(arc), color=ORANGE, lw=1)
    ax.text(.04, .33, '$\\varphi$', color=ORANGE, fontsize=9)
    ax.text(.11, .70, '$r$', color=ORANGE, fontsize=9)
    ax.text(.62, .45, '$z=s$', fontsize=8)
    ax.text(.33, 1.03, '$s^2+z^2=1$', color=BLUE, fontsize=8)
    ax.set(xlim=(0, 1.08), ylim=(0, 1.13), aspect='equal',
           xlabel='$s$（到轴距离，无量纲）', ylabel='$z$（无量纲）')
    ax.set_xticks([0, .5, 1])
    ax.set_yticks([0, .5, 1])
    bx.add_patch(Rectangle((0, 0), np.pi/4, 1, facecolor=PALE,
                           edgecolor=BLUE, lw=1.3))
    bx.plot([p, p], [0, 1], color=ORANGE, lw=2)
    bx.text(.075, .72, '$0\\leq r\\leq1$', fontsize=8)
    bx.text(.075, .53, '$0\\leq\\varphi\\leq\\pi/4$', fontsize=8)
    bx.text(.075, .29, '$0\\leq\\theta<2\\pi$', fontsize=8)
    bx.set(xlim=(0, .90), ylim=(0, 1.13), xlabel='$\\varphi$（rad）',
           ylabel='$r$（到原点距离，无量纲）')
    bx.set_xticks([0, np.pi/6, np.pi/4], ['$0$', '$\\pi/6$', '$\\pi/4$'])
    bx.set_yticks([0, .5, 1])
    footer(fig, '子午区域：球面截取圆锥内部', '参数区域：体积元须乘 r² sin φ')
    save(fig, 'fig-04-spherical', '球内圆锥上方区域的子午截面与球坐标参数范围。')


def previews():
    thumbs = []
    for record in MANIFEST:
        with Image.open(OUT / (record['stem']+'.png')) as im:
            tile = im.convert('RGB')
            tile.thumbnail((1000, 540), Image.Resampling.LANCZOS)
            thumbs.append(tile.copy())
    preview = Image.new('RGB', (2000, 1080), 'white')
    for i, tile in enumerate(thumbs):
        preview.paste(tile, ((i % 2)*1000, (i // 2)*540))
    preview.save(OUT / 'preview.png')
    ImageOps.grayscale(preview).save(OUT / 'preview-gray.png')


if __name__ == '__main__':
    # Luminance is supplementary: solid/dashed lines and labels carry meaning.
    ss.grayscale_check([BLUE, ORANGE])
    slices()
    split_order()
    cylindrical()
    spherical()
    (OUT / 'figure_manifest.json').write_text(
        json.dumps(MANIFEST, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    previews()
