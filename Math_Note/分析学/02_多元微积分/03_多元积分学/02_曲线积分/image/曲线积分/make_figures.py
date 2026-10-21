"""Deterministic geometry for the line-integral note; PDF + 600 dpi PNG.

Run with Python 3.12+: python make_figures.py
All variables are dimensionless. No measured data or statistical uncertainty.
"""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.patches import Circle, Rectangle
import numpy as np
from PIL import Image, ImageOps, ImageDraw
import sci_style as ss

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
OUT = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ['Microsoft YaHei', 'DejaVu Sans']
ss.apply('double', font_size=8, legend_size=7, minor_ticks=False)
plt.rcParams.update({'mathtext.fontset': 'dejavusans', 'axes.unicode_minus': False,
                     'savefig.bbox': None})
BLUE, ORANGE = '#0072B2', '#D55E00'
GRAY, PALE = '0.48', '#EAF2F8'
MANIFEST = []


def figure(rows=1, cols=2, height=86):
    fig, axes = plt.subplots(rows, cols, figsize=ss.figsize('double', height_mm=height),
                             layout='constrained', squeeze=False)
    fig.set_constrained_layout_pads(w_pad=.055, h_pad=.06, wspace=.10, hspace=.08)
    for i, ax in enumerate(axes.flat):
        ax.text(0, 1.055, chr(65+i), transform=ax.transAxes, weight='bold', fontsize=10)
        ax.locator_params(nbins=5)
    return fig, axes.ravel()


def plane(ax, xlim, ylim, equal=True):
    ax.set(xlim=xlim, ylim=ylim, xlabel='$x$（无量纲）', ylabel='$y$（无量纲）')
    if equal:
        ax.set_aspect('equal', adjustable='box')
    ax.locator_params(nbins=4)


def arrow(ax, start, end, color=BLUE, lw=1.4, ls='-', scale=9, zorder=6):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, ls=ls,
                                mutation_scale=scale, shrinkA=0, shrinkB=0), zorder=zorder)


def label(ax, x, y, text, **kwargs):
    return ax.text(x, y, text, ha=kwargs.pop('ha', 'center'),
                   va=kwargs.pop('va', 'center'), **kwargs)


def footer(ax, text, y=-.30):
    ax.text(.5, y, text, transform=ax.transAxes, ha='center', va='top', fontsize=8)


def path_arrow(ax, x, y, i, color=BLUE, reverse=False):
    j = min(i+12, len(x)-1)
    p, q = (x[i], y[i]), (x[j], y[j])
    arrow(ax, q if reverse else p, p if reverse else q, color=color)


def save(fig, stem, description):
    fig.canvas.draw()
    fig.set_layout_engine('none')
    ss.save(fig, OUT / (stem+'.pdf'), also_png=True, dpi=600, tight=False)
    size = ss.output_size_mm(OUT / (stem+'.pdf'))
    assert size and abs(size[0]-178)/178 < .03, (stem, size)
    fig.canvas.draw()
    # Text may sit outside an axes for labels, but must stay inside the figure.
    renderer = fig.canvas.get_renderer()
    box = fig.bbox
    for ax in fig.axes:
        for artist in [*ax.texts, ax.xaxis.label, ax.yaxis.label]:
            if not artist.get_visible() or not artist.get_text():
                continue
            b = artist.get_window_extent(renderer)
            assert b.x0 > -2 and b.y0 > -2 and b.x1 < box.width+2 and b.y1 < box.height+2, (stem, artist.get_text())
    MANIFEST.append(dict(file=stem, size_mm=[round(v, 2) for v in size],
                         dpi=600, description=description))
    plt.close(fig)


def line_elements():
    fig, (ax, bx) = figure(height=87)
    t = np.linspace(0, 1.15, 400)
    plane(ax, (-.08, 1.32), (-.16, 1.55))
    ax.plot(t, t*t, color=GRAY, lw=1)
    u, v = .52, .82
    mask = (t >= u) & (t <= v)
    ax.plot(t[mask], t[mask]**2, color=BLUE, lw=3)
    p, q = np.array([u,u*u]), np.array([v,v*v])
    ax.plot(*p, 'o', color='black'); ax.plot(*q, 's', color='black')
    arrow(ax, p, q, color=ORANGE)
    tangent = np.array([1,2*u]); tangent /= np.linalg.norm(tangent)
    arrow(ax, p, p+.64*tangent, color=BLUE, ls='--')
    label(ax, .35, .32, r'$\mathbf{r}(t)$', ha='right')
    label(ax, .88, .60, r'$\Delta\mathbf{r}$', color=ORANGE, ha='left')
    label(ax, .57, .65, r'$\Delta s$', color=BLUE)
    label(ax, 1.03, .96, r'$\mathbf{T}$（切向）', color=BLUE)
    label(ax, .45, 1.34, r'$C:\ \mathbf{r}(t)=(t,t^2)$')
    footer(ax, '有限弧段：弧长与弦长一般不同')
    s = t/2*np.sqrt(1+4*t*t)+np.arcsinh(2*t)/4
    bx.plot(t, s, color=BLUE)
    su = u/2*np.sqrt(1+4*u*u)+np.arcsinh(2*u)/4
    slope = np.sqrt(1+4*u*u)
    tt = np.array([.25,.91])
    bx.plot(tt, su+slope*(tt-u), '--', color=ORANGE)
    bx.plot(u,su,'o',color='black')
    bx.set(xlabel='$t$（无量纲）', ylabel='$s(t)$（无量纲）', xlim=(0,1.2), ylim=(0,2))
    label(bx, .23, 1.53, r'$ds/dt=\|\mathbf{r}\,\prime(t)\|$', ha='left')
    label(bx, .65, .25, '切线斜率为速率', color=ORANGE)
    footer(bx, r'$d\mathbf{r}=\mathbf{T}\,ds=\mathbf{r}\,\prime(t)\,dt$')
    save(fig,'fig-01-line-elements','弧长、弦位移、切向方向，以及参数到弧长的速率变换。')


def scalar_accumulation():
    fig, (ax,bx) = figure(height=88)
    t = np.linspace(0,np.pi,401)
    pts = np.c_[np.cos(t),np.sin(t)]
    seg = np.stack([pts[:-1],pts[1:]], axis=1)
    lc = LineCollection(seg, cmap='cividis', norm=Normalize(.5,1.5), linewidth=3)
    lc.set_array(1+.5*np.cos((t[:-1]+t[1:])/2)); ax.add_collection(lc)
    plane(ax,(-1.35,1.35),(-.16,1.45))
    ax.plot([-1,1],[0,0],'o',color='black')
    for ti in np.linspace(0,np.pi,9):
        ax.plot([.95*np.cos(ti),1.05*np.cos(ti)],[.95*np.sin(ti),1.05*np.sin(ti)],color='black',lw=.6)
    tc = .45*np.pi
    label(ax, .48, 1.22, r'$\rho_i\Delta s_i$')
    arrow(ax,(.44,1.10),(np.cos(tc),np.sin(tc)),color=ORANGE,lw=1)
    label(ax, 0,.28, r'$C:\ x^2+y^2=1,\quad y\geq0$')
    cb = fig.colorbar(lc, ax=ax, orientation='horizontal', fraction=.07, pad=.23, ticks=[.5,1,1.5])
    cb.set_label(r'$\rho=1+x/2$（无量纲）')
    rho = 1+.5*np.cos(t)
    bx.fill_between(t,0,rho,color=PALE)
    edges = np.linspace(0,np.pi,9)
    mid = (edges[:-1]+edges[1:])/2
    bx.bar(mid,1+.5*np.cos(mid),width=np.pi/8,align='center',facecolor='none',edgecolor=GRAY,lw=.65)
    bx.plot(t,rho,color=BLUE,lw=2)
    bx.set(xlim=(0,np.pi),ylim=(0,1.8),xlabel='$s=t$（无量纲）',ylabel=r'$\rho(s)$（无量纲）')
    bx.set_xticks([0,np.pi/2,np.pi],['$0$',r'$\pi/2$',r'$\pi$'])
    label(bx,np.pi*.56,.42,r'曲线下的面积为质量'+'\n'+r'$m=\int_0^\pi\rho(s)\,ds=\pi$')
    footer(bx,'每段贡献 = 线密度 × 弧长',y=-.28)
    save(fig,'fig-02-scalar-accumulation','半圆细线的密度加权与弧长参数下的黎曼和。')


def projections():
    fig,(ax,bx) = figure(height=87)
    plane(ax,(-.15,2.15),(-.15,2.18))
    arrow(ax,(0,0),(1.8,1.2),color=BLUE,lw=2)
    arrow(ax,(0,0),(1.8,0),color=ORANGE)
    arrow(ax,(1.8,0),(1.8,1.2),color=ORANGE,ls='--')
    label(ax,1,1.1,r'$d\mathbf{r}=(dx,dy)$',rotation=34,color=BLUE)
    label(ax,.9,.12,'$dx$',va='bottom',color=ORANGE)
    label(ax,1.91,.58,'$dy$',ha='left',color=ORANGE)
    label(ax,.9,1.85,r'$\mathbf{F}=(P,Q)$')
    footer(ax,r'$dW=P\,dx+Q\,dy$')
    # T is exactly unit length; the displayed F has length sqrt(.6^2+2.5^2).
    plane(bx,(-.5,3.5),(-.6,3.3))
    T = np.array([.8,.6]); F = np.array([.6,2.5]); V = np.dot(F,T)*T
    line = np.array([-.35,3.3]); bx.plot(line*T[0],line*T[1],color=GRAY,lw=1)
    arrow(bx,(0,0),T,color='black',lw=1.2)
    arrow(bx,(0,0),F,color=BLUE,lw=2)
    arrow(bx,(0,0),V,color=ORANGE,lw=2)
    bx.plot([F[0],V[0]],[F[1],V[1]],':',color=GRAY)
    N = np.array([-T[1],T[0]])*.15
    bx.plot(*np.array([V-N,V-N-.15*T,V-.15*T]).T,color=GRAY,lw=.7)
    label(bx,.36,2.65,r'$\mathbf{F}$',color=BLUE)
    label(bx,.73,.16,r'$\mathbf{T}$',color='black')
    label(bx,1.97,.87,r'$(\mathbf{F}\cdot\mathbf{T})\mathbf{T}$',color=ORANGE)
    label(bx,2.1,2.6,'法向部分\n不贡献功',color=GRAY)
    footer(bx,r'$dW=(\mathbf{F}\cdot\mathbf{T})\,ds$')
    save(fig,'fig-03-two-projections','坐标分解与正交切向投影；投影向量长度由点积精确计算。')


def reversal():
    fig,axes = figure(height=86)
    t = np.linspace(0,np.pi/2,300)
    x,y = np.cos(t),np.sin(t)
    for i,ax in enumerate(axes):
        plane(ax,(-.18,1.24),(-.18,1.24))
        ax.plot(x,y,'-' if i == 0 else '--',color=BLUE,lw=2)
        path_arrow(ax,x,y,125,color=BLUE,reverse=bool(i))
        ax.plot([1,0],[0,1],'o',color='black')
        label(ax,1.12,-.02,'$A$'); label(ax,-.08,1.1,'$B$')
        arrow(ax,(.32,.30),(.83,.30),color=GRAY)
        label(ax,.58,.41,r'$\mathbf{F}=(1,0)$',color=GRAY)
        label(ax,.58,.11,r'$\rho=1$')
        footer(ax,(r'$C:A\to B$'+'\n'+r'$\int_C ds=\pi/2,\quad\int_C dx=-1$' if i == 0 else
                   r'$-C:B\to A$'+'\n'+r'$\int_{-C}ds=\pi/2,\quad\int_{-C}dx=1$'))
    save(fig,'fig-04-reversal','同一四分之一圆反向行进：弧长不变，恒力场的功反号。')


def potential():
    fig,(ax,bx) = figure(height=94)
    grid = np.linspace(-.08,1.15,150)
    X,Y = np.meshgrid(grid,grid); phi = X*X*Y+Y*Y/2
    cs = ax.contour(X,Y,phi,levels=[.1,.3,.6,1.,1.5],colors='0.65',linewidths=.6)
    ax.clabel(cs,inline=True,fontsize=6.5,fmt='%g')
    g = np.linspace(.1,1.,7); U,V = np.meshgrid(g,g)
    ax.quiver(U,V,2*U*V,U*U+V,color='0.70',angles='xy',scale_units='xy',scale=13,width=.004)
    t = np.linspace(0,1,300)
    ax.plot(t,t*t,color=BLUE,label=r'$C_1:\ y=x^2$')
    ax.plot(t,t,'--',color=ORANGE,label=r'$C_2:\ y=x$')
    path_arrow(ax,t,t*t,140); path_arrow(ax,t,t,100,color=ORANGE)
    ax.plot([0,1],[0,1],'o',color='black')
    label(ax,.05,-.09,'$A$'); label(ax,1.07,1.07,'$B$')
    plane(ax,(-.10,1.2),(-.12,1.22))
    ax.legend(loc='upper left',fontsize=7)
    footer(ax,r'等势线 $\phi=x^2y+y^2/2$'+'\n'+r'箭头为 $\nabla\phi$，两条路均从 $A$ 到 $B$')
    w1 = 1.5*t**4; w2 = t**3+.5*t**2
    bx.plot(t,w1,color=BLUE,label=r'$\phi(\mathbf{r}_1(t))-\phi(A)$')
    bx.plot(t,w2,'--',color=ORANGE,label=r'$\phi(\mathbf{r}_2(t))-\phi(A)$')
    bx.axhline(1.5,color=GRAY,lw=.7,ls=':')
    bx.plot([1],[1.5],'o',color='black')
    bx.set(xlim=(0,1.08),ylim=(0,1.8),xlabel='$t$（无量纲）',ylabel='累积功 $W(t)$（无量纲）')
    bx.legend(loc='upper left')
    label(bx,.73,1.65,'$W_1(1)=W_2(1)=3/2$')
    footer(bx,r'沿途累积可以不同'+'\n'+r'终值均为 $\phi(B)-\phi(A)$')
    save(fig,'fig-05-potential','势函数例题：等势线、梯度场、不同路径与相同的端点势差。')


def curl_and_topology():
    fig,(ax,bx) = figure(height=91)
    theta = np.linspace(0,2*np.pi,400)
    g = np.linspace(-1.2,1.2,9); X,Y = np.meshgrid(g,g)
    ax.quiver(X,Y,np.ones_like(X),np.zeros_like(Y),color='0.75',
              angles='xy',scale_units='xy',scale=5,width=.004)
    for r,ls in [(1.,'-'),(.62,'--'),(.26,':')]:
        xx,yy = r*np.cos(theta),r*np.sin(theta)
        ax.plot(xx,yy,ls,color=BLUE,lw=1.4)
        path_arrow(ax,xx,yy,40)
    ax.plot(0,0,'o',color='black',ms=4)
    label(ax,0,1.35,r'$\mathbf{F}=(1,0),\quad\kappa=0$')
    plane(ax,(-1.4,1.4),(-1.35,1.55))
    footer(ax,'闭路可在域内收缩\n'+r'任意闭路：$\oint_C\mathbf{F}\cdot d\mathbf{r}=0$')
    R2 = X*X+Y*Y
    U = np.divide(-Y,R2,out=np.zeros_like(Y),where=R2>.13)
    V = np.divide(X,R2,out=np.zeros_like(X),where=R2>.13)
    bx.quiver(X,Y,U,V,color='0.75',angles='xy',scale_units='xy',scale=6,width=.004)
    xx,yy = np.cos(theta),np.sin(theta)
    bx.plot(xx,yy,color=BLUE,lw=2); path_arrow(bx,xx,yy,40)
    xx2,yy2 = .75+.20*np.cos(theta),.20*np.sin(theta)
    bx.plot(xx2,yy2,'--',color=ORANGE,lw=1.3)
    bx.plot(0,0,'x',color='black',ms=6,mew=1.4)
    label(bx,-.34,-.17,'原点缺失',ha='right')
    label(bx,0,1.35,r'$\kappa=0\quad (x,y)\neq(0,0)$')
    label(bx,.75,.40,'小闭路：0',color=ORANGE)
    plane(bx,(-1.4,1.4),(-1.35,1.55))
    footer(bx,'绕孔闭路不能在域内收缩\n'+r'单位圆：$\oint_C\mathbf{F}\cdot d\mathbf{r}=2\pi$')
    save(fig,'fig-06-curl-topology','可收缩闭路与穿孔场：局部无旋不能排除绕孔的全局环量。')


def green_orientation():
    fig,(ax,bx) = figure(height=91)
    theta = np.linspace(0,2*np.pi,400)
    ax.add_patch(Circle((0,0),1.2,facecolor=PALE,edgecolor='none'))
    ax.add_patch(Circle((0,0),.5,facecolor='white',edgecolor='none'))
    for r,col,ls,rev in [(1.2,BLUE,'-',False),(.5,ORANGE,'--',True)]:
        xx,yy = r*np.cos(theta),r*np.sin(theta)
        ax.plot(xx,yy,color=col,ls=ls)
        for i in [30,130,230,330]:
            path_arrow(ax,xx,yy,i,color=col,reverse=rev)
    label(ax,.82,-.37,'$D$')
    label(ax,0,0,'孔')
    label(ax,-.6,1.42,'外边界：逆时针',color=BLUE)
    label(ax,.7,.65,'内边界：顺时针',color=ORANGE)
    plane(ax,(-1.5,1.5),(-1.42,1.6))
    footer(ax,'行进时，区域 $D$ 始终位于左侧')
    values = np.pi*np.array([1.2**2,-.5**2,1.2**2-.5**2])
    bars = bx.bar([0,1,2],values,width=.56,color=[BLUE,ORANGE,'0.3'],edgecolor='black',lw=.65)
    for b,hatch in zip(bars,['','///','xx']):
        b.set_hatch(hatch)
    bx.axhline(0,color='black',lw=.8)
    bx.set_xticks([0,1,2],['外边界','内边界','总环量'])
    bx.set(xlim=(-.65,2.65),ylim=(-1.4,5.8),xlabel='边界贡献',ylabel='环量（无量纲）')
    for x,v,txt in zip([0,1,2],values,[r'$1.44\pi$',r'$-0.25\pi$',r'$1.19\pi$']):
        label(bx,x,v+(.28 if v>0 else -.28),txt)
    label(bx,1,5.35,r'$\mathbf{F}=(-y/2,x/2),\quad\kappa=1$')
    footer(bx,r'$\oint_{\partial D}\mathbf{F}\cdot d\mathbf{r}$'+'\n'+r'$=\operatorname{Area}(D)=1.19\pi$')
    save(fig,'fig-07-green-orientation','环域的正向外、内边界及其有符号环量贡献。')


def green_cancellation():
    fig,(ax,bx) = figure(height=91)
    x,y,w,h = .4,.5,.9,.7
    corners = [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
    ax.add_patch(Rectangle((x,y),w,h,facecolor=PALE,edgecolor='none'))
    for p,q in zip(corners[:-1],corners[1:]):
        arrow(ax,p,q,color=BLUE,lw=1.6)
    label(ax,x+w/2,y-.20,r'$-y\,\Delta x/2$')
    label(ax,x+w/2,y+h+.20,r'$(y+\Delta y)\Delta x/2$')
    label(ax,x+w+.20,y+h/2,r'$(x+\Delta x)\Delta y/2$',rotation=90)
    label(ax,x-.20,y+h/2,r'$-x\,\Delta y/2$',rotation=90)
    label(ax,x+w/2,y+h/2,r'$\kappa\,\Delta x\Delta y$')
    plane(ax,(-.13,1.83),(-.05,1.75))
    ax.set_xticks([x,x+w],['$x$',r'$x+\Delta x$'])
    ax.set_yticks([y,y+h],['$y$',r'$y+\Delta y$'])
    footer(ax,r'$\mathbf{F}=(-y/2,x/2)$：四边贡献相加'+'\n'+r'$=\Delta x\Delta y,\quad\kappa=1$')
    for i in range(3):
        for j in range(3):
            bx.add_patch(Rectangle((i,j),1,1,facecolor=PALE,edgecolor='0.65',lw=.7))
            pts = np.array([[i+.10,j+.10],[i+.90,j+.10],[i+.90,j+.90],[i+.10,j+.90],[i+.10,j+.10]])
            for p,q in zip(pts[:-1],pts[1:]):
                m = (p+q)/2; d = (q-p)*.2
                arrow(bx,m-d,m+d,color=GRAY,lw=.7,scale=6)
    outer = np.array([[0,0],[3,0],[3,3],[0,3],[0,0]])
    bx.plot(*outer.T,color=BLUE,lw=2)
    for p,q in zip(outer[:-1],outer[1:]):
        m = (p+q)/2; d = (q-p)*.1
        arrow(bx,m-d,m+d,color=BLUE,lw=2)
    plane(bx,(-.18,3.18),(-.18,3.18))
    bx.set_xticks([0,1,2,3]); bx.set_yticks([0,1,2,3])
    footer(bx,'共享边双向贡献抵消，只剩正向外边界\n'+r'$\sum_i\oint_{\partial D_i}=\oint_{\partial D}$')
    save(fig,'fig-08-green-cancellation','微小矩形的环量密度与区域分割后的内部边界相消。')


def worked_example():
    fig,axes = figure(rows=2,cols=2,height=173)
    ax,bx,cx,dx = axes
    t = np.linspace(0,1,400)
    ax.fill_between(t,t*t,t,facecolor=PALE)
    ax.plot(t,t*t,color=BLUE,label=r'$C_1:\ y=x^2$')
    ax.plot(t,t,'--',color=ORANGE,label=r'$C_2:\ y=x$')
    path_arrow(ax,t,t*t,190); path_arrow(ax,t,t,120,color=ORANGE)
    ax.plot([0,1],[0,1],'o',color='black')
    label(ax,.05,-.08,'$A$'); label(ax,1.06,1.07,'$B$')
    label(ax,.65,.5,'$D$')
    plane(ax,(-.08,1.17),(-.10,1.17)); ax.legend(loc='upper left')
    footer(ax,r'两条路径均从 $A$ 到 $B$'+'\n'+r''+r'$\mathbf{F}=(6xy,x^2+y)$',y=-.29)
    bx.plot(t,10*t**3,color=BLUE,label=r'$C_1:\ 10t^3$')
    bx.plot(t,7*t*t+t,'--',color=ORANGE,label=r'$C_2:\ 7t^2+t$')
    bx.set(xlim=(0,1.03),ylim=(0,11.8),xlabel='$t$（无量纲）',ylabel=r'功密度 $\mathbf{F}\cdot\mathbf{r}\,\prime$（无量纲）')
    bx.legend(loc='upper left')
    footer(bx,r'$\int_{C_1}=5/2,\qquad\int_{C_2}=17/6$',y=-.29)
    X,Y = np.meshgrid(np.linspace(0,1,140),np.linspace(0,1,140))
    K = np.ma.masked_where((Y<X*X)|(Y>X),-4*X)
    pc = cx.pcolormesh(X,Y,K,cmap='cividis',vmin=-4,vmax=0,shading='auto',rasterized=False)
    cx.plot(t,t*t,color=BLUE,lw=1.5); cx.plot(t,t,'--',color=ORANGE,lw=1.5)
    path_arrow(cx,t,t*t,180); path_arrow(cx,t,t,150,color=ORANGE,reverse=True)
    x0 = .60
    cx.plot([x0,x0],[x0*x0,x0],color='black',lw=1.3)
    label(cx,.65,.29,'$x^2$'); label(cx,.48,.66,'$x$')
    plane(cx,(-.08,1.13),(-.10,1.13))
    cb = fig.colorbar(pc,ax=cx,fraction=.055,pad=.03,ticks=[-4,-2,0])
    cb.set_label(r'$\kappa=-4x$（无量纲）')
    footer(cx,r'正向边界为 $C_1$ 接 $-C_2$'+'\n'+r'竖切片高度为 $x-x^2$',y=-.29)
    integrand = -4*t*(t-t*t)
    dx.fill_between(t,0,integrand,facecolor=PALE,hatch='///',edgecolor='0.65',lw=0)
    dx.plot(t,integrand,color=BLUE,lw=2)
    dx.axhline(0,color='black',lw=.7)
    dx.set(xlim=(0,1),ylim=(-.73,.10),xlabel='$x$（无量纲）',ylabel=r'$-4x(x-x^2)$（无量纲）')
    label(dx,.49,-.18,r'有符号面积 $=-1/3$')
    footer(dx,r'$\iint_D\kappa\,dA=-1/3$'+'\n'+r'$=5/2-17/6$',y=-.29)
    save(fig,'fig-09-worked-example','非保守场例题：路径、功密度、正向闭合边界、旋度及竖切片积分。')


def previews():
    thumbs = []
    for item in MANIFEST:
        with Image.open(OUT/(item['file']+'.png')) as im:
            thumb = im.convert('RGB'); thumb.thumbnail((940,900))
        tile = Image.new('RGB',(980,thumb.height+65),'white')
        tile.paste(thumb,((980-thumb.width)//2,35))
        ImageDraw.Draw(tile).text((18,12),item['file'],fill='black')
        thumbs.append(tile)
    for k,start in enumerate(range(0,len(thumbs),4),1):
        group = thumbs[start:start+4]
        heights = [max(t.height for t in group[j:j+2]) for j in range(0,len(group),2)]
        sheet = Image.new('RGB',(1960,sum(heights)),'#dddddd')
        for i,tile in enumerate(group):
            sheet.paste(tile,((i%2)*980,sum(heights[:i//2])))
        sheet.save(OUT/f'preview-{k}.png')
        ImageOps.grayscale(sheet).save(OUT/f'preview-{k}-gray.png')


if __name__ == '__main__':
    ss.grayscale_check([BLUE,ORANGE])
    print('Accessibility: all paths have direct labels; paired paths also use solid/dashed strokes.')
    for draw in [line_elements,scalar_accumulation,projections,reversal,potential,
                 curl_and_topology,green_orientation,green_cancellation,worked_example]:
        draw()
    (OUT/'figure_manifest.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2),encoding='utf-8')
    previews()
    print(f'Completed: {len(MANIFEST)} figures, PDF + 600 dpi PNG; color and grayscale contact sheets.')
