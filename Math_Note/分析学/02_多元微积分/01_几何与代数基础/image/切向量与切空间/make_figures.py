"""Reproduce the tangent-vector illustrations; run: python make_figures.py."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from PIL import Image, ImageOps
import sci_style as ss

OUT = Path(__file__).resolve().parent
ss.apply('double', font_size=8, minor_ticks=False)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial', 'DejaVu Sans']
BLUE, ORANGE, GREY = '#0072B2', '#E69F00', '#666666'
BLACK, LIGHT = '#202020', '#CBD3DA'
ss.grayscale_check([BLUE, ORANGE, BLACK])
RECORDS = []


class Arrow3D(FancyArrowPatch):
    def __init__(self, start, end, **kwargs):
        super().__init__((0, 0), (0, 0), **kwargs)
        self.xyz = np.asarray([start, end])

    def do_3d_projection(self, renderer=None):
        x, y, z = proj3d.proj_transform(*self.xyz.T, self.axes.get_proj())
        self.set_positions((x[0], y[0]), (x[1], y[1]))
        return float(np.min(z))

    def draw(self, renderer):
        self.do_3d_projection()
        super().draw(renderer)


def arrow2(ax, start, vector, color=BLUE, style='-', lw=1.8):
    end = np.asarray(start) + vector
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=11,
                                color=color, lw=lw, linestyle=style,
                                shrinkA=0, shrinkB=0, zorder=8))


def arrow3(ax, start, vector, color=BLUE, style='-', lw=1.8):
    ax.add_artist(Arrow3D(start, np.asarray(start) + vector,
                         arrowstyle='-|>', mutation_scale=10, lw=lw,
                         color=color, linestyle=style, zorder=12))


def figure(head_a, head_b, height=98):
    fig = plt.figure(figsize=ss.figsize('double', height_mm=height))
    # Keep the nominal canvas inside tight-bbox exports (178 mm + 1 mm padding).
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                             fill=False, linewidth=0, edgecolor='none'))
    fig.text(.035, .95, 'A', weight='bold', fontsize=10)
    fig.text(.075, .95, head_a, fontsize=9)
    fig.text(.535, .95, 'B', weight='bold', fontsize=10)
    fig.text(.575, .95, head_b, fontsize=9)
    return fig


def axes2(ax, xlim, ylim, xlabel, ylabel):
    ax.set(xlim=xlim, ylim=ylim, xlabel=xlabel, ylabel=ylabel)
    ax.set_aspect('equal', adjustable='box')
    ax.tick_params(labelsize=7)
    ax.axhline(0, color='.86', lw=.6, zorder=0)
    ax.axvline(0, color='.86', lw=.6, zorder=0)


def axes3(ax, xlim, ylim, zlim, vector=False):
    ax.set(xlim=xlim, ylim=ylim, zlim=zlim)
    ax.set_proj_type('ortho')
    ax.set_box_aspect([np.ptp(xlim), np.ptp(ylim), np.ptp(zlim)])
    ax.view_init(elev=25, azim=-58)
    ax.grid(False)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
        axis.pane.set_edgecolor('white')
        axis.set_major_locator(plt.MaxNLocator(3))
    ax.tick_params(pad=-1, labelsize=6.5)
    labels = (r'$v_x$', r'$v_y$', r'$v_z$') if vector else (r'$x$', r'$y$', r'$z$')
    ax.set_xlabel(labels[0], labelpad=-4)
    ax.set_ylabel(labels[1], labelpad=-4)
    ax.set_zlabel(labels[2], labelpad=-3)


def r(u, v):
    return np.array([u, v, .5 * (u*u + v*v)])


P = r(.5, .5)
RU, RV = np.array([1., 0., .5]), np.array([0., 1., .5])
NORMAL = np.cross(RU, RV)
H = np.array([.7, .6])
V = H[0] * RU + H[1] * RV
assert np.allclose(np.dot(NORMAL, V), 0)
assert np.linalg.matrix_rank(np.column_stack([RU, RV])) == 2


def tangent_patch(ax, base, lo=-.65, hi=1.1):
    a, b = np.meshgrid(np.linspace(lo, hi, 2), np.linspace(lo, hi, 2))
    xyz = base[:, None, None] + RU[:, None, None]*a + RV[:, None, None]*b
    ax.plot_surface(*xyz, color=LIGHT, alpha=.28, shade=False,
                    edgecolor='#9AA5AE', linewidth=.6, zorder=1)


def export(fig, stem):
    sizes = []
    for ext in ['pdf', 'svg', 'png']:
        path = OUT / f'{stem}.{ext}'
        ss.save(fig, path, dpi=600)
        size = ss.output_size_mm(path, 600)
        if size is not None:
            assert abs(size[0] - 178) / 178 < .03, size
        sizes.append({'format': ext, 'size_mm': size})
    with Image.open(OUT / f'{stem}.png') as im:
        im.thumbnail((1500, 1000))
        im.convert('RGB').save(OUT / f'preview-{stem}.png')
        ImageOps.grayscale(im).save(OUT / f'preview-{stem}-gray.png')
    RECORDS.append({'figure': stem, 'exports': sizes})
    plt.close(fig)


def curve():
    fig = figure('曲线上：位移与切向量', '向量空间中：全部切向量')
    ax = fig.add_axes([.085, .22, .37, .64])
    t = np.linspace(-.25, 2.1, 300)
    p = np.array([1., .5])
    q = np.array([1.6, 1.28])
    ax.plot(t, .5*t*t, color=GREY, lw=1.5, label=r'$M:\ y=x^2/2$')
    s = np.linspace(-1.2, 1.05, 100)
    ax.plot(p[0]+s, p[1]+s, '--', color=BLUE, lw=1.15,
            label=r'$p+T_pM$')
    arrow2(ax, p, q-p, ORANGE)
    arrow2(ax, p, np.array([1., 1.]), BLUE)
    ax.plot(*p, 'o', color=BLACK, ms=4)
    ax.plot(*q, 's', color=ORANGE, ms=4)
    ax.annotate(r'$p=(1,1/2)$', p, xytext=(-65, -12), textcoords='offset points')
    ax.annotate(r'$q$', q, xytext=(-17, 8), textcoords='offset points')
    ax.text(.9, 1.72, r'$\mathbf{v}=(1,1)$', ha='center', color=BLUE)
    ax.annotate(r'$\Delta\mathbf{r}$', (1.3, .89), xytext=(.55, 1.2),
                color='#805800', arrowprops={'arrowstyle': '-', 'lw': .65, 'color': '#805800'})
    axes2(ax, (-.3, 2.2), (-.65, 2.1), r'$x$（无量纲）', r'$y$（无量纲）')
    ax.legend(loc='upper left', fontsize=7)

    ax = fig.add_axes([.59, .22, .35, .64])
    s = np.linspace(-1.25, 1.25, 100)
    ax.plot(s, s, '--', color=BLUE, lw=1.2)
    arrow2(ax, np.zeros(2), np.ones(2), BLUE)
    arrow2(ax, np.zeros(2), -.85*np.ones(2), BLACK, style='-.')
    ax.plot(0, 0, 'o', color=BLACK, ms=4)
    ax.text(.1, -.18, r'$\mathbf{0}$')
    ax.text(.8, 1.15, r'$\mathbf{v}$', color=BLUE)
    ax.text(-1.18, -.73, r'$-0.85\mathbf{v}$')
    ax.text(-1.2, 1.1, r'$T_pM=\{a(1,1):a\in\mathbb{R}\}$', fontsize=8)
    axes2(ax, (-1.4, 1.4), (-1.4, 1.4), r'$v_x$（无量纲）', r'$v_y$（无量纲）')
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    fig.text(.5, .07, '切向量是一个向量；切空间包含它的所有实数倍，并经过向量原点。', ha='center')
    export(fig, 'fig-01-curve-tangent')


def parameter_surface():
    fig = figure('参数空间：选择变化方向', '曲面上：对位置向量求偏导', 105)
    ax = fig.add_axes([.085, .25, .32, .59])
    u0 = np.array([.5, .5])
    ax.axhline(.5, color=BLUE, lw=1.25)
    ax.axvline(.5, color=ORANGE, lw=1.25, linestyle='--')
    arrow2(ax, u0, [1, 0], BLUE)
    arrow2(ax, u0, [0, 1], ORANGE, style='--')
    ax.plot(*u0, 'o', color=BLACK, ms=4)
    ax.annotate(r'$\mathbf{u}_0$', u0, xytext=(-25, -16), textcoords='offset points')
    ax.text(1.2, .64, r'$\mathbf{e}_1$', color=BLUE)
    ax.text(.63, 1.32, r'$\mathbf{e}_2$', color='#805800')
    axes2(ax, (-.2, 1.7), (-.2, 1.7), r'$u$（无量纲）', r'$v$（无量纲）')
    ax.set_xticks([0, .5, 1, 1.5]); ax.set_yticks([0, .5, 1, 1.5])
    fig.text(.445, .57, r'$\mathbf{r}$', ha='center', fontsize=11)
    fig.add_artist(FancyArrowPatch((.418, .52), (.49, .52),
                   transform=fig.transFigure, arrowstyle='-|>', lw=1.1,
                   mutation_scale=10, color=BLACK))
    ax = fig.add_axes([.5, .17, .48, .72], projection='3d', computed_zorder=False)
    uv = np.linspace(-.3, 1.4, 28)
    u, v = np.meshgrid(uv, uv)
    ax.plot_surface(u, v, .5*(u*u+v*v), color=LIGHT, alpha=.16,
                    shade=False, linewidth=0, zorder=0)
    ax.plot_wireframe(u, v, .5*(u*u+v*v), rstride=5, cstride=5,
                      color='#ACB4BA', lw=.4, alpha=.6, zorder=1)
    t = np.linspace(-.3, 1.4, 180)
    ax.plot(t, .5+0*t, .5*(t*t+.25), color=BLUE, lw=1.6, zorder=4)
    ax.plot(.5+0*t, t, .5*(t*t+.25), color=ORANGE, lw=1.6, linestyle='--', zorder=4)
    arrow3(ax, P, RU, BLUE)
    arrow3(ax, P, RV, ORANGE, style='--')
    ax.scatter(*P, color=BLACK, s=18, depthshade=False, zorder=15)
    ax.text(*[.43, .34, .1], r'$p$', fontsize=9, zorder=20)
    ax.text2D(.80, .41, r'$\mathbf{r}_u$', transform=ax.transAxes,
              color=BLUE, fontsize=9, zorder=20)
    ax.text(*[.48, 1.48, .8], r'$\mathbf{r}_v$', color='#805800', fontsize=9, zorder=20)
    axes3(ax, (-.4, 1.6), (-.4, 1.6), (-.2, 2.1))
    fig.text(.255, .12, '实线：只改变 $u$；虚线：只改变 $v$。', ha='center', fontsize=8)
    fig.text(.75, .12, r'$\mathbf{r}(u,v)=(u,v,(u^2+v^2)/2)$', ha='center', fontsize=8)
    fig.text(.5, .045, r'$J_{\mathbf{r}}\mathbf{e}_1=\mathbf{r}_u=(1,0,1/2),\qquad'
             r'J_{\mathbf{r}}\mathbf{e}_2=\mathbf{r}_v=(0,1,1/2)$', ha='center', fontsize=9)
    export(fig, 'fig-02-parameter-surface')


def plane_space():
    fig = figure('切平面：经过几何点 $p$', '切空间：经过向量原点', 115)
    for i, base in enumerate([P, np.zeros(3)]):
        ax = fig.add_axes([.015+i*.5, .25, .475, .65], projection='3d', computed_zorder=False)
        tangent_patch(ax, base)
        arrow3(ax, base, RU, BLUE, lw=1.55)
        arrow3(ax, base, RV, ORANGE, style='--', lw=1.55)
        arrow3(ax, base, V, BLACK, lw=2.0)
        # Translated components show the parallelogram without changing the vector.
        end = base + V
        ax.plot(*np.array([base+H[0]*RU, end]).T, color=GREY, lw=.9, linestyle=':')
        ax.plot(*np.array([base+H[1]*RV, end]).T, color=GREY, lw=.9, linestyle=':')
        if i == 1:
            for a, b in [(-.5, .2), (.2, -.6), (-.4, -.4)]:
                arrow3(ax, base, a*RU+b*RV, GREY, lw=.8)
            arrow3(ax, base, .85*NORMAL, GREY, style='-.', lw=1.4)
            ax.text(-.62, -.5, .92, r'$\mathbf{n}$', color=GREY, fontsize=9, zorder=20)
        ax.scatter(*base, color=BLACK, s=18, depthshade=False, zorder=15)
        ax.text(*(base+[-.08,-.12,-.12]), r'$p$' if i == 0 else r'$\mathbf{0}$', fontsize=9, zorder=20)
        ax.text(*(base+RU+[.08,-.06,.01]), r'$\mathbf{r}_u$', color=BLUE, fontsize=8, zorder=20)
        ax.text(*(base+RV+[.05,.04,.05]), r'$\mathbf{r}_v$', color='#805800', fontsize=8, zorder=20)
        ax.text(*(base+V+[-.14,.04,.17]), r'$\mathbf{v}$', color=BLACK, fontsize=9, zorder=20)
        axes3(ax, (base[0]-.8, base[0]+1.4),
              (base[1]-.8, base[1]+1.4), (base[2]-.9, base[2]+1.35), vector=i==1)
    fig.text(.25, .18, r'$p+T_pM:\ z=\frac{1}{2}x+\frac{1}{2}y-\frac{1}{4}$', ha='center', fontsize=8)
    fig.text(.75, .18, r'$T_pM:\ v_z=\frac{1}{2}v_x+\frac{1}{2}v_y$', ha='center', fontsize=8)
    legend = [Line2D([0],[0],color=BLUE,lw=1.5,label=r'$\mathbf{r}_u$'),
              Line2D([0],[0],color=ORANGE,lw=1.5,ls='--',label=r'$\mathbf{r}_v$'),
              Line2D([0],[0],color=BLACK,lw=2,label=r'$\mathbf{v}=0.7\mathbf{r}_u+0.6\mathbf{r}_v$'),
              Line2D([0],[0],color=GREY,lw=1.4,ls='-.',label=r'$\mathbf{n}\perp T_pM$')]
    fig.legend(handles=legend, loc='lower center', bbox_to_anchor=(.5,.08), ncol=4, fontsize=7)
    fig.text(.5, .035, '阴影仅截取平面的一块；完整的切平面和切空间都向各方向无限延伸。', ha='center', fontsize=8)
    export(fig, 'fig-03-affine-tangent-space')


if __name__ == '__main__':
    curve()
    parameter_surface()
    plane_space()
    (OUT / 'export_sizes.json').write_text(json.dumps(RECORDS, indent=2), encoding='utf-8')
