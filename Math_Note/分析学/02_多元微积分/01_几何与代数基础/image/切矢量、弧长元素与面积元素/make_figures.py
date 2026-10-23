"""Reproduce seven analytic geometry figures; run: python make_figures.py."""
from pathlib import Path
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon, Arc
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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
    labels = ('$v_x$', '$v_y$', '$v_z$') if vector else ('$x$', '$y$', '$z$')
    ax.set_xlabel(labels[0] + '（无量纲）', labelpad=-2, fontsize=7)
    ax.set_ylabel(labels[1] + '（无量纲）', labelpad=-2, fontsize=7)
    ax.set_zlabel(labels[2] + '（无量纲）', labelpad=-1, fontsize=7)


def r(u, v):
    return np.array([u, v, .5 * (u*u + v*v)])


P = r(.5, .5)
RU, RV = np.array([1., 0., .5]), np.array([0., 1., .5])
NORMAL = np.cross(RU, RV)
H = np.array([.7, .6])
V = H[0] * RU + H[1] * RV
assert np.allclose(np.dot(NORMAL, V), 0)
assert np.linalg.matrix_rank(np.column_stack([RU, RV])) == 2


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


def position_displacement():
    fig = figure('位置矢量：从原点指向点', '位移矢量：坐标变化的组合', 110)
    p0, p1 = np.array([1., .4]), np.array([2., 1.6])
    delta = p1-p0
    ax = fig.add_axes([.08, .27, .36, .57])
    arrow2(ax, [0,0], p0, BLUE, style='-.')
    arrow2(ax, [0,0], p1, BLUE)
    arrow2(ax, p0, delta, ORANGE, style='--')
    ax.scatter(*p0, s=18, color=BLACK, zorder=15)
    ax.scatter(*p1, s=18, color=BLACK, marker='s', zorder=15)
    ax.text(-.08,-.18,'$O$',fontsize=8)
    ax.text(.8,.18,'$P_0=(1,0.4)$',fontsize=7)
    ax.text(1.45,1.75,'$P_1=(2,1.6)$',fontsize=7)
    ax.text(.36,.03,'$\\mathbf{r}_0$',color=BLUE)
    ax.text(.65,.85,'$\\mathbf{r}_1$',color=BLUE)
    ax.annotate('$\\Delta\\mathbf{r}$',(1.55,1.06),xytext=(1.83,.65),
                color='#805800',arrowprops=dict(arrowstyle='-',lw=.7,color=ORANGE))
    axes2(ax,(-.2,2.4),(-.2,2.2),'$x$（无量纲）','$y$（无量纲）')
    ax.set_xticks([0,1,2]);ax.set_yticks([0,1,2])
    ax=fig.add_axes([.59,.27,.35,.57])
    ax.plot([0,1,1],[0,0,1.2],':',color=GREY,lw=1)
    arrow2(ax,[0,0],delta,ORANGE,style='--')
    ax.scatter(0,0,s=18,color=BLACK,zorder=15)
    ax.scatter(*delta,s=18,color=BLACK,marker='s',zorder=15)
    ax.text(.15,.85,'$\\Delta\\mathbf{r}=(1,1.2)$',color='#805800',fontsize=8)
    ax.text(.5,-.19,'$\\Delta x=1$',ha='center',fontsize=8)
    ax.text(1.08,.55,'$\\Delta y=1.2$',fontsize=8)
    axes2(ax,(-.2,1.8),(-.3,1.7),'$\\Delta x$（无量纲）','$\\Delta y$（无量纲）')
    ax.set_xticks([0,1]);ax.set_yticks([0,1])
    fig.text(.5,.13,'$\\Delta\\mathbf{r}=\\mathbf{r}_1-\\mathbf{r}_0=(x_1-x_0,\\ y_1-y_0)$',ha='center',fontsize=9)
    fig.text(.5,.045,'位置矢量回答“点在哪里”；位移矢量回答“从一个点移动了多少”。',ha='center',fontsize=8)
    assert np.allclose(p0+delta,p1)
    export(fig,'fig-01-position-displacement')


def curve():
    fig=figure('两个位置矢量相减，得到位移', '缩放位移，逼近切矢量', 116)
    # A true orthographic projection. Rows form an orthonormal pair.
    projection=np.array([[-.5,np.sqrt(3)/2,0],[-.3,-np.sqrt(3)/10,np.sqrt(.88)]])
    assert np.allclose(projection@projection.T,np.eye(2))
    def path(t):
        t=np.asarray(t)
        return np.stack([.6*np.sin(2*t),t+.7,.55*t+.4*np.sin(t)+.9],axis=-1)
    def velocity(t):
        return np.array([1.2*np.cos(2*t),1.,.55+.4*np.cos(t)])
    def project(x):return np.asarray(x)@projection.T
    t0=.6;h=1.1;p=path(t0);q=path(t0+h);tau=velocity(t0)
    pp,qq=project(p),project(q)
    tt=np.linspace(-1.2,3.25,400);cc=project(path(tt))
    ax=fig.add_axes([.045,.25,.44,.61])
    ax.set_aspect('equal');ax.set_axis_off()
    for end,label,offset in [(np.array([1.1,0,0]),'$x$',(-.12,-.03)),
                              (np.array([0,3.5,0]),'$y$',(.08,-.02)),
                              (np.array([0,0,2.8]),'$z$',(-.12,.07))]:
        arrow2(ax,[0,0],project(end),GREY,lw=.75)
        ax.text(*(project(end)+offset),label,fontsize=8)
    ax.plot(*cc.T,color='#56B4E9',lw=1.5,zorder=2)
    arrow2(ax,[0,0],pp,BLUE,lw=1.4)
    arrow2(ax,[0,0],qq,BLUE,style='-.',lw=1.4)
    arrow2(ax,pp,qq-pp,ORANGE,style='--',lw=1.7)
    arrow2(ax,pp,project(tau),BLACK,lw=1.7)
    ax.scatter(*pp,s=18,color=BLACK,zorder=15)
    ax.scatter(*qq,s=18,color=BLACK,marker='s',zorder=15)
    ax.scatter(0,0,s=12,color=BLACK,zorder=15)
    ax.text(-.15,-.16,'$O$',fontsize=8)
    ax.text(*(pp+[-.45,.1]),r'$P=\mathbf{r}(t)$',fontsize=7)
    ax.text(*(qq+[.02,.12]),r'$Q=\mathbf{r}(t+h)$',fontsize=7)
    ax.text(*(pp*.45+[-.36,.08]),r'$\mathbf{r}(t)$',color=BLUE,fontsize=8)
    ax.text(*(qq*.55+[.1,-.25]),r'$\mathbf{r}(t+h)$',color=BLUE,fontsize=8)
    ax.annotate(r'$\Delta\mathbf{r}$',xy=(pp+qq)*.5,xytext=(1.72,2.35),fontsize=8,
                color='#805800',arrowprops=dict(arrowstyle='-',color=ORANGE,lw=.7,
                                                connectionstyle='arc3,rad=.2'))
    ax.text(*(pp+project(tau)+[-.22,.17]),r'$\mathbf{r}\prime(t)$',fontsize=8)
    ax.text(*(cc[-25]+[.06,.08]),'$C$',color=GREY,fontsize=8)
    ax.set(xlim=(-.85,3.65),ylim=(-.65,3.15))
    ax=fig.add_axes([.56,.25,.40,.61])
    ax.set_aspect('equal');ax.set_axis_off()
    near=project(path(np.linspace(.25,2.5,180)))
    ax.plot(*near.T,color='#ADB5BB',lw=1.1,zorder=1)
    for hh,c,ls in [(1.1,ORANGE,'--'),(.55,GREY,':'),(.15,BLUE,'-.')]:
        rate=(path(t0+hh)-p)/hh
        arrow2(ax,pp,project(rate),c,style=ls,lw=1.6)
    arrow2(ax,pp,project(tau),BLACK,lw=1.9)
    ax.scatter(*pp,s=18,color=BLACK,zorder=15)
    ax.text(*(pp+[-.27,-.14]),'$P$',fontsize=8)
    ax.text(1.5,2.15,r'$h\longrightarrow0$',ha='center',fontsize=9)
    ax.set(xlim=(.55,2.45),ylim=(.75,2.55))
    fig.text(.25,.16,r'$\Delta\mathbf{r}=\mathbf{r}(t+h)-\mathbf{r}(t)$',ha='center',fontsize=8)
    fig.text(.75,.16,r'$\mathbf{r}\prime(t)=\lim_{h\to0}\frac{\Delta\mathbf{r}}{h}$',ha='center',fontsize=8)
    handles=[Line2D([],[],color=c,ls=ls,label=label) for c,ls,label in
             [(ORANGE,'--','$h=1.1$'),(GREY,':','$h=0.55$'),
              (BLUE,'-.','$h=0.15$'),(BLACK,'-',r'$\mathbf{r}\prime(t)$')]]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.045),ncol=4,fontsize=7)
    # Difference quotients converge to the actual derivative, without normalizing arrows.
    for hh in [.1,.01,.001]:
        error=np.linalg.norm((path(t0+hh)-p)/hh-tau)
        assert error<2*hh
    export(fig,'fig-02-position-tangent')


def parameter_surface():
    fig = figure('参数空间：选择变化方向', '曲面上：对位置向量求偏导', 105)
    ax = fig.add_axes([.085, .25, .32, .59])
    u0 = np.array([.5, .5])
    ax.axhline(.5, color=BLUE, lw=1.25)
    ax.axvline(.5, color=ORANGE, lw=1.25, linestyle='--')
    arrow2(ax, u0, [1, 0], BLUE)
    arrow2(ax, u0, [0, 1], ORANGE, style='--')
    ax.plot(*u0, 'o', color=BLACK, ms=4)
    ax.annotate('$\\mathbf{u}_0$', u0, xytext=(-25, -16), textcoords='offset points')
    ax.text(1.2, .64, '$\\mathbf{e}_1$', color=BLUE)
    ax.text(.63, 1.32, '$\\mathbf{e}_2$', color='#805800')
    axes2(ax, (-.2, 1.7), (-.2, 1.7), '$u$（无量纲）', '$v$（无量纲）')
    ax.set_xticks([0, .5, 1, 1.5]); ax.set_yticks([0, .5, 1, 1.5])
    fig.text(.445, .57, '$\\mathbf{r}$', ha='center', fontsize=11)
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
    ax.text(*[.43, .34, .1], '$p$', fontsize=9, zorder=20)
    ax.text2D(.80, .41, '$\\mathbf{r}_u$', transform=ax.transAxes,
              color=BLUE, fontsize=9, zorder=20)
    ax.text(*[.48, 1.48, .8], '$\\mathbf{r}_v$', color='#805800', fontsize=9, zorder=20)
    axes3(ax, (-.4, 1.6), (-.4, 1.6), (-.2, 2.1))
    fig.text(.255, .12, '实线：只改变 $u$；虚线：只改变 $v$。', ha='center', fontsize=8)
    fig.text(.75, .12, '$\\mathbf{r}(u,v)=(u,v,(u^2+v^2)/2)$', ha='center', fontsize=8)
    fig.text(.5, .045, '$\\mathrm{d}\\mathbf{r}=\\mathbf{r}_u\\,\\mathrm{d}u+\\mathbf{r}_v\\,\\mathrm{d}v,\\qquad'
             '\\mathbf{r}_u=(1,0,1/2),\\quad\\mathbf{r}_v=(0,1,1/2)$', ha='center', fontsize=9)
    export(fig, 'fig-05-parameter-surface')


def arc_elements():
    fig = figure('平面曲线：一阶位移的长度', '空间曲线：方向 × 长度', 107)
    ax = fig.add_axes([.08, .28, .36, .56])
    x = np.linspace(.45, 1.85, 250)
    p = np.array([1., .5]); a = np.array([.5, .5]); q = np.array([1.5, 1.125])
    ax.plot(x, x*x/2, color=GREY, lw=1.4)
    ax.plot([1., 1.5, 1.5], [.5, .5, 1.], ':', color=BLACK, lw=1)
    arrow2(ax, p, q-p, ORANGE, style='--', lw=1.4)
    arrow2(ax, p, a, BLUE, lw=2)
    ax.scatter(*p, s=18, color=BLACK, zorder=15)
    ax.text(.78, .48, '$p$')
    ax.annotate('$\\mathbf{r}\\prime h$', p+a*.5, xytext=(.55, .94),
                color=BLUE, arrowprops=dict(arrowstyle='-', color=BLUE, lw=.7))
    ax.annotate('$\\Delta\\mathbf{r}$', (1.43, 1.07), xytext=(1.1, 1.38),
                color='#805800', arrowprops=dict(arrowstyle='-', color=ORANGE, lw=.7))
    ax.text(1.24, .39, '$h=0.5$', ha='center', fontsize=7)
    ax.text(1.55, .71, '$f\\prime h$', fontsize=7)
    axes2(ax, (.4, 1.9), (.2, 1.7), '$x$（无量纲）', '$y$（无量纲）')
    ax.set_xticks([.5, 1, 1.5]); ax.set_yticks([.5, 1, 1.5])
    ax = fig.add_axes([.51, .19, .46, .69], projection='3d', computed_zorder=False)
    t = np.linspace(-.6, 5.3, 320)
    ax.plot(np.cos(t), np.sin(t), t/2, color=GREY, lw=1.5)
    t0 = .6; h = .7
    p = np.array([np.cos(t0), np.sin(t0), t0/2])
    tau = np.array([-np.sin(t0), np.cos(t0), .5])
    a = h*tau
    arrow3(ax, p, a, BLUE, lw=2)
    ax.scatter(*p, s=18, color=BLACK, depthshade=False, zorder=20)
    ax.text(*(p+[-.1,-.2,-.12]), '$p$', zorder=20)
    ax.text2D(.12, .87, '$\\mathbf{r}(t)=(\\cos t,\\sin t,t/2)$', transform=ax.transAxes, fontsize=7)
    ax.text(*(p+a+[-.15,.1,.1]), '$\\mathbf{r}\\prime(t_0)h$', color=BLUE, fontsize=8, zorder=25)
    axes3(ax, (-1.3, 1.3), (-1.3, 1.8), (-.4, 2.8))
    fig.text(.25, .13, '$\\|\\mathbf{r}\\prime h\\|=\\sqrt{h^2+(f\\prime h)^2}$', ha='center')
    fig.text(.75, .13, '$\\mathbf{r}\\prime h=\\mathbf{T}\\,\\|\\mathbf{r}\\prime\\|h$', ha='center')
    fig.text(.5, .04, '有限参数增量用于展示：实际位移与一阶位移仅在微分极限中一致。', ha='center')
    assert np.isclose(np.linalg.norm(tau), np.sqrt(1.25))
    export(fig, 'fig-03-arc-elements')


def implicit_tangents():
    fig = figure('一个平面约束：梯度与切向量', '两个空间约束：交线的切方向', 110)
    ax = fig.add_axes([.08, .30, .36, .53])
    t = np.linspace(0, 2*np.pi, 300)
    ax.plot(np.cos(t), np.sin(t), color=GREY, lw=1.4)
    p = np.ones(2)/np.sqrt(2); grad = 2*p; tau = np.array([grad[1], -grad[0]])
    arrow2(ax, p, .55*grad, BLUE)
    arrow2(ax, p, .55*tau, ORANGE, style='--')
    ax.scatter(*p, s=18, color=BLACK, zorder=15)
    ax.text(.47, .8, '$p$', fontsize=8)
    ax.text(.65, 1.62, '$0.55\\nabla F$', color=BLUE, fontsize=8)
    ax.text(1.12, -.25, '$\\mathbf{T}$', color='#805800', fontsize=8)
    # Orthogonality marker, constructed along the two unit directions.
    e, f = grad/2, tau/2; corner = p+.12*e+.12*f
    ax.plot(*np.array([p+.12*e, corner, p+.12*f]).T, color=BLACK, lw=.8)
    axes2(ax, (-1.3, 1.9), (-1.3, 1.9), '$x$（无量纲）', '$y$（无量纲）')
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    ax = fig.add_axes([.50, .24, .44, .64], projection='3d', computed_zorder=False)
    theta, z = np.meshgrid(np.linspace(0, 2*np.pi, 70), np.linspace(-.5, 1.2, 10))
    ax.plot_surface(np.cos(theta), np.sin(theta), z, color=LIGHT, alpha=.12, shade=False, lw=0)
    xx, yy = np.meshgrid([-1.3, 1.3], [-1.4, 1.3])
    ax.plot_surface(xx, yy, xx*0, color=LIGHT, alpha=.2, shade=False, edgecolor=GREY, lw=.4)
    ax.plot(np.cos(t), np.sin(t), 0*t, color=BLACK, lw=1.5, zorder=4)
    p3 = np.array([1.,0.,0.]); g1=np.array([2.,0.,0.]); g2=np.array([0.,0.,1.])
    tangent = np.cross(g1,g2)
    arrow3(ax, p3, .6*g1, BLUE)
    arrow3(ax, p3, .6*g2, GREY, style='-.')
    arrow3(ax, p3, .6*tangent, ORANGE, style='--')
    ax.scatter(*p3, s=18, color=BLACK, depthshade=False, zorder=20)
    axes3(ax, (-1.4, 2.4), (-1.5, 1.4), (-.65, 1.5))
    fig.text(.25, .15, '$F=x^2+y^2-1=0$', ha='center')
    fig.text(.75, .15, '$F=x^2+y^2-1=0,\\quad G=z=0$', ha='center', fontsize=7)
    handles = [Line2D([],[],color=BLUE,label='$\\nabla F$'),
               Line2D([],[],color=GREY,ls='-.',label='$\\nabla G$'),
               Line2D([],[],color=ORANGE,ls='--',label='$\\nabla F\\times\\nabla G$')]
    fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(.5,.035), ncol=3, fontsize=8)
    assert np.isclose(grad@tau, 0) and np.isclose(g1@tangent, 0) and np.isclose(g2@tangent, 0)
    export(fig, 'fig-04-implicit-tangents')


def area_elements():
    fig = figure('参数域：一个小矩形', '切平面：对应的平行四边形', 112)
    h, k = .6, .5
    ax = fig.add_axes([.09, .26, .32, .55])
    q = np.array([.5,.5])
    ax.add_patch(Rectangle(q, h, k, facecolor='#D7E9F3', edgecolor=GREY, lw=.9))
    arrow2(ax, q, [h,0], BLUE)
    arrow2(ax, q, [0,k], ORANGE, style='--')
    ax.text(.8,.39,'$h$',ha='center',color=BLUE)
    ax.text(.38,.74,'$k$',color='#805800')
    ax.text(.78,.76,'$hk$',ha='center',fontsize=10)
    ax.text(.35,.49,'$\\mathbf{u}_0$',fontsize=8)
    axes2(ax, (.15,1.45),(.15,1.4),'$u$（无量纲）','$v$（无量纲）')
    ax.set_xticks([.5,1]);ax.set_yticks([.5,1])
    fig.add_artist(FancyArrowPatch((.43,.55),(.5,.55),transform=fig.transFigure,
                   arrowstyle='-|>',lw=1.1,mutation_scale=10,color=BLACK))
    ax = fig.add_axes([.51,.22,.47,.65],projection='3d',computed_zorder=False)
    a,b = h*RU,k*RV
    verts = np.array([P,P+a,P+a+b,P+b])
    ax.add_collection3d(Poly3DCollection([verts],facecolor='#D7E9F3',edgecolor=GREY,alpha=.7,lw=.8,zorder=2))
    uv=np.linspace(.25,1.3,24);u,v=np.meshgrid(uv,uv)
    ax.plot_surface(u,v,.5*(u*u+v*v),color=LIGHT,alpha=.12,shade=False,lw=0,zorder=0)
    for uline,vline in [(np.linspace(.5,1.1,50),np.full(50,.5)),
                        (np.full(50,1.1),np.linspace(.5,1.,50)),
                        (np.linspace(1.1,.5,50),np.ones(50)),
                        (np.full(50,.5),np.linspace(1.,.5,50))]:
        ax.plot(uline,vline,.5*(uline**2+vline**2),':',color='#A76B00',lw=1.2,zorder=4)
    arrow3(ax,P,a,BLUE)
    arrow3(ax,P,b,ORANGE,style='--')
    arrow3(ax,P,np.cross(a,b),BLACK,style='-.')
    ax.scatter(*P,s=18,color=BLACK,depthshade=False,zorder=20)
    ax.text2D(.11,.84,'$\\mathbf{a}=\\mathbf{r}_u h$',transform=ax.transAxes,color=BLUE,fontsize=8)
    ax.text2D(.63,.84,'$\\mathbf{b}=\\mathbf{r}_v k$',transform=ax.transAxes,color='#805800',fontsize=8)
    ax.text2D(.13,.1,'$\\mathbf{a}\\times\\mathbf{b}$',transform=ax.transAxes,fontsize=8)
    axes3(ax,(.15,1.5),(.15,1.5),(.05,1.65))
    fig.text(.5,.14,'$\\|\\mathbf{a}\\times\\mathbf{b}\\|=\\|\\mathbf{r}_u\\times\\mathbf{r}_v\\|\\,hk=\\sqrt{3/2}\\,hk$',ha='center')
    fig.text(.5,.045,'蓝色面片在切平面中；橙色点线为实际曲面片边界，两者仅在微分极限中一致。',ha='center',fontsize=8)
    assert np.allclose(np.cross(a,b),h*k*NORMAL)
    export(fig,'fig-06-area-elements')


def area_projection():
    fig=figure('空间中：曲面片与正交投影', '沿最陡方向的竖直截面',112)
    ax=fig.add_axes([.015,.24,.49,.64],projection='3d',computed_zorder=False)
    base=np.array([[0.,0.,0.],[1.,0.,0.],[1.,1.,0.],[0.,1.,0.]])
    top=base.copy();top[:,2]=.5*top[:,0]+.5*top[:,1]+.6
    ax.add_collection3d(Poly3DCollection([base],facecolor='#F6DBA3',edgecolor=ORANGE,lw=1.1,alpha=.6,zorder=1))
    ax.add_collection3d(Poly3DCollection([top],facecolor='#A9CFE4',edgecolor=BLUE,lw=1.1,alpha=.6,zorder=3))
    for s,e in zip(base,top):
        ax.plot(*np.array([s,e]).T,':',color=GREY,lw=.8,zorder=2)
    mid=np.mean(top,axis=0);n=NORMAL/np.linalg.norm(NORMAL)
    arrow3(ax,mid,.55*n,BLACK,style='-.')
    ax.text2D(.65,.72,'$\\mathbf{n}$',transform=ax.transAxes,fontsize=9)
    ax.text2D(.18,.69,'$\\mathrm{d}S$',transform=ax.transAxes,color=BLUE)
    ax.text2D(.31,.19,'$\\mathrm{d}A_{xy}$',transform=ax.transAxes,color='#805800')
    axes3(ax,(-.3,1.4),(-.3,1.4),(-.15,2.1))
    ax=fig.add_axes([.61,.28,.32,.52])
    slope=1/np.sqrt(2);s=np.linspace(-.25,1.3,100)
    ax.plot(s,.6+slope*s,color=BLUE,lw=1.6)
    ax.plot([0,1],[0,0],color=ORANGE,lw=2,ls='--')
    ax.plot([0,0],[0,.6],':',color=GREY,lw=.9)
    ax.plot([1,1],[0,.6+slope],':',color=GREY,lw=.9)
    m=np.array([.5,.6+.5*slope]);n2=np.array([-1/np.sqrt(3),np.sqrt(2/3)])
    arrow2(ax,m,.7*n2,BLACK,style='-.')
    arrow2(ax,m,[0,.7],GREY,lw=1.2)
    theta=np.degrees(np.arccos(np.sqrt(2/3)))
    ax.add_patch(Arc(m,.63,.63,theta1=90,theta2=90+theta,color=GREY,lw=.8))
    ax.text(m[0]-.18,m[1]+.4,'$\\theta$',fontsize=9)
    ax.text(.75,1.63,'$\\mathbf{k}$',color=GREY)
    ax.text(-.03,1.58,'$\\mathbf{n}$')
    axes2(ax,(-.35,1.4),(-.15,1.9),'$s=(x+y)/\\sqrt{2}$（无量纲）','$z$（无量纲）')
    ax.set_xticks([0,.5,1]);ax.set_yticks([0,.5,1,1.5])
    fig.text(.5,.14,'$\\mathrm{d}A_{xy}=|\\mathbf{n}\\cdot\\mathbf{k}|\\,\\mathrm{d}S=\\sqrt{2/3}\\,\\mathrm{d}S$',ha='center',fontsize=9)
    fig.text(.5,.045,'截面取沿最陡方向的竖直平面，包含真实单位法向量；面积投影因子由三维内积给出。',ha='center',fontsize=8)
    assert np.isclose(abs(n[2]),np.sqrt(2/3)) and np.isclose(np.linalg.norm(n2),1)
    export(fig,'fig-07-area-projection')


if __name__ == '__main__':
    position_displacement()
    curve()
    arc_elements()
    implicit_tangents()
    parameter_surface()
    area_elements()
    area_projection()
    (OUT / 'export_sizes.json').write_text(json.dumps(RECORDS, indent=2), encoding='utf-8')
