"""Reproduce bivariate probability figures, analytic tables and metadata.

Run: python plot_bivariate.py
Dependencies: numpy, matplotlib, pillow. No random samples or fitted curves.
Nominal width: 178 mm. PDF: vector. PNG: 600 dpi. Chinese font required.
"""
from __future__ import annotations

import csv
import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patches, ticker
from matplotlib.colors import Normalize
import numpy as np

import sci_style as ss

OUT = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ['Microsoft YaHei', 'Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']
ss.apply('double', font_size=9, tick_size=8, legend_size=7.5, mathtext=False)
FONT = ss.check_fonts()
if FONT == 'DejaVu Sans':
    raise RuntimeError('A Chinese sans-serif font is required.')
BLUE, ORANGE, GREEN = [ss.OKABE_ITO[k] for k in ('blue', 'vermillion', 'green')]
COLORS = [BLUE, ORANGE, GREEN]
STYLES = ['-', '--', '-.']
MARKERS = ['o', 's', '^']
FIGURES = []
JOINT = np.array([[.4, .1], [.2, .3]])  # Rows: X; columns: Y.


def pair():
    return plt.subplots(1, 2, figsize=ss.figsize('double', height_mm=82), layout='constrained')


def save(fig, axs, name):
    ss.panels(fig, axs, 'ABC', x=0, y=1.04)
    path = OUT / (name+'.pdf')
    ss.save(fig, path, dpi=600, also_png=True)
    w, h = ss.output_size_mm(path)
    assert abs(w-178)/178 < .03, (name, w)
    FIGURES.append(dict(name=name, width_mm=w, height_mm=h, png_dpi=600))
    plt.close(fig)


def xy_labels(ax, x='取值 $x$（无量纲）', y='取值 $y$（无量纲）'):
    ax.set(xlabel=x, ylabel=y)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))


def density_labels(ax, x='取值（无量纲）'):
    ax.set(xlabel=x, ylabel='密度（无量纲）', ylim=(0, None))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(5))


def triangle_cdf(x, y):
    u, v = np.clip(x, 0, 1), np.clip(y, 0, 1)
    return np.where(u >= v, v*v, 2*u*v-u*u)


def discrete_joint():
    fig, axs = pair()
    cumulative = JOINT.cumsum(0).cumsum(1)
    for ax, arr, title in zip(axs, [JOINT, cumulative], ['联合概率 $p_{ij}$', '累计概率 $F(i,j)$']):
        im = ax.imshow(arr, origin='upper', cmap='cividis', vmin=0, vmax=1, extent=(-.5,1.5,1.5,-.5))
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f'{arr[i,j]:.2f}', ha='center', va='center', color='white' if arr[i,j]<.5 else 'black')
        ax.set(xlabel='列：$Y$ 的取值', ylabel='行：$X$ 的取值', xticks=[0,1], yticks=[0,1])
        ax.minorticks_off()
        ss.colorbar(fig, im, ax, title+'（无量纲）', fraction=.045)
    save(fig, axs, '01_discrete_joint')


def continuous_joint():
    fig, axs = pair()
    edges = np.linspace(0,1,301)
    centers = (edges[:-1]+edges[1:])/2
    x, y = np.meshgrid(centers, centers)
    density = np.where(x<y,2.,0.)
    im = axs[0].pcolormesh(edges, edges, density, cmap='cividis', vmin=0, vmax=2, rasterized=True)
    ss.colorbar(fig, im, axs[0], '联合密度 $f(x,y)$（无量纲）')
    axs[0].plot([0,1],[0,1], '--', color='white', lw=1)
    region = patches.Polygon([(0,0),(.5,.5),(.5,.75),(0,.75)], fill=False,
                             edgecolor=ORANGE, lw=1.8, hatch='///')
    axs[0].add_patch(region)
    axs[0].text(.02,.96, '框内概率 = 0.5000', transform=axs[0].transAxes, va='top', fontsize=8)
    im = axs[1].pcolormesh(edges, edges, triangle_cdf(x,y), cmap='cividis', vmin=0, vmax=1, rasterized=True)
    ss.colorbar(fig, im, axs[1], '累计概率 $F(x,y)$（无量纲）')
    levels = [.25,.5,.75]
    cs = axs[1].contour(x,y,triangle_cdf(x,y), levels=levels, colors='white', linewidths=.8)
    axs[1].clabel(cs, fmt='%.2f', fontsize=7)
    axs[1].plot(.5,.75,'o', color=ORANGE)
    for ax in axs:
        xy_labels(ax)
        ax.set(xlim=(0,1), ylim=(0,1), aspect='equal')
    save(fig, axs, '02_triangle_pdf_cdf')


def marginals_conditionals():
    fig, axs = pair()
    x = np.linspace(0,1,401)
    axs[0].plot(x,2*(1-x), '-', color=BLUE, label='$f_X(x)=2(1-x)$')
    axs[0].plot(x,2*x, '--', color=ORANGE, label='$f_Y(y)=2y$')
    for i, y in enumerate([.25,.5,.75]):
        axs[1].plot([0,y,np.nan,y,1],[1/y,1/y,np.nan,0,0], STYLES[i], color=COLORS[i],
                    label=rf'$Y={y:g}$')
        axs[1].plot(y,1/y,MARKERS[i],mfc='white',mec=COLORS[i],ms=4)
    for ax in axs:
        density_labels(ax)
        ax.set_xlim(0,1)
        ax.legend(loc='upper right')
    axs[1].set_ylabel(r'条件密度 $f_{X\mid Y}(x\mid y)$（无量纲）')
    save(fig, axs, '03_marginal_conditional')


def marginal_axes():
    fig, axs = plt.subplots(1, 3, figsize=ss.figsize('double', height_mm=77), layout='constrained')
    for ax in axs:
        ax.set_xlim(0, 1)
        ax.set_xticks([0, .25, .5, .75, 1])
        ax.tick_params(labelsize=7)
        ax.minorticks_off()
    return fig, axs


def triangle_domain(ax):
    ax.add_patch(patches.Polygon([(0, 0), (0, 1), (1, 1)],
                 facecolor=BLUE, alpha=.13, edgecolor='none'))
    ax.plot([0, 1], [0, 1], '--', color='.4', lw=.9)
    ax.set(xlabel='$x$（无量纲）', ylabel='$y$（无量纲）', ylim=(0, 1.06))
    ax.text(.43, .88, '$f(x,y)=2$', transform=ax.transAxes, fontsize=8)


def marginal_line():
    """Fixed x: a vertical integral gives a marginal density, not probability."""
    fig, axs = marginal_axes()
    t = .25
    triangle_domain(axs[0])
    axs[0].plot([t, t], [t, 1], color=ORANGE, lw=2.4)
    axs[0].plot([t, t], [0, t], ':', color='.45', lw=.9)
    axs[0].text(.43, .23, '$x=t=0.25$', transform=axs[0].transAxes, fontsize=8)
    axs[1].plot([0, t], [0, 0], color=BLUE)
    axs[1].plot([t, 1], [2, 2], color=ORANGE)
    axs[1].fill_between([t, 1], [2, 2], color=ORANGE, alpha=.24, linewidth=0)
    axs[1].set(xlabel='沿线坐标 $y$（无量纲）', ylabel='$f(t,y)$（无量纲）', ylim=(0, 2.6))
    axs[1].text(.04, .88, '积分面积 = 1.5', transform=axs[1].transAxes, fontsize=8)
    x = np.linspace(0, 1, 401)
    axs[2].plot(x, 2*(1-x), color=BLUE)
    axs[2].plot(t, 1.5, 'o', color=ORANGE)
    axs[2].plot([t, t], [0, 1.5], ':', color='.45', lw=.9)
    axs[2].set(xlabel='$x$（无量纲）', ylabel='$f_X(x)$（无量纲）', ylim=(0, 2.6))
    axs[2].text(.04, .88, '$f_X(0.25)=1.5$', transform=axs[2].transAxes, fontsize=8)
    save(fig, axs, '09_marginal_line')


def marginal_area():
    """The joint left-side integral equals marginal area and the CDF value."""
    fig, axs = marginal_axes()
    t, probability = .25, .4375
    triangle_domain(axs[0])
    axs[0].add_patch(patches.Polygon([(0, 0), (t, t), (t, 1), (0, 1)],
                     facecolor=ORANGE, alpha=.3, edgecolor=ORANGE, hatch='///', lw=.9))
    axs[0].plot([t, t], [0, 1], ':', color=ORANGE, lw=1.2)
    # Keep the probability annotation clear of the shaded strip and the diagonal.
    axs[0].text(.35, .23, '左侧区域概率\n0.4375', transform=axs[0].transAxes, fontsize=8)
    x = np.linspace(0, 1, 401)
    u = np.linspace(0, t, 201)
    axs[1].plot(x, 2*(1-x), color=BLUE)
    axs[1].fill_between(u, 2*(1-u), color=ORANGE, alpha=.25, linewidth=0)
    axs[1].plot([t, t], [0, 1.5], ':', color=ORANGE, lw=.9)
    axs[1].set(xlabel='累计坐标 $u$（无量纲）', ylabel='$f_X(u)$（无量纲）', ylim=(0, 2.6))
    axs[1].text(.04, .88, '阴影面积 = 0.4375', transform=axs[1].transAxes, fontsize=8)
    axs[2].plot(x, 2*x-x*x, color=BLUE)
    axs[2].plot(t, probability, 'o', color=ORANGE)
    axs[2].plot([0, t], [probability, probability], ':', color='.45', lw=.9)
    axs[2].plot([t, t], [0, probability], ':', color='.45', lw=.9)
    axs[2].set(xlabel='阈值 $t$（无量纲）', ylabel='$F_X(t)$（无量纲）', ylim=(0, 1.16))
    axs[2].text(.04, .9, '$F_X(0.25)=0.4375$', transform=axs[2].transAxes, fontsize=8)
    save(fig, axs, '10_marginal_area')


def normal_contours():
    fig, axs = plt.subplots(1,3, figsize=ss.figsize('double', height_mm=79), layout='constrained')
    x = np.linspace(-3.4,3.4,241)
    xx, yy = np.meshgrid(x,x)
    probability = [.5,.9,.99]
    angle = np.linspace(0,2*math.pi,401)
    circle = np.vstack([np.cos(angle),np.sin(angle)])
    norm = Normalize(0, .27)
    for ax, rho in zip(axs,[-.8,0,.8]):
        q = (xx**2-2*rho*xx*yy+yy**2)/(1-rho*rho)
        f = np.exp(-q/2)/(2*math.pi*math.sqrt(1-rho*rho))
        im = ax.pcolormesh(x,x,f,cmap='cividis',norm=norm,rasterized=True,shading='auto')
        eig, vectors = np.linalg.eigh([[1,rho],[rho,1]])
        root = vectors @ np.diag(np.sqrt(eig))
        for p, style in zip(probability,['-','--',':']):
            ellipse = math.sqrt(-2*math.log(1-p))*root@circle
            ax.plot(ellipse[0],ellipse[1],style,color='white',lw=1.05,label=f'{p:.0%}')
        ax.text(.2,1.04, rf'$\rho={rho:g}$',transform=ax.transAxes, color='black', fontsize=8)
        ax.set(xlim=(-3.4,3.4),ylim=(-3.4,3.4),aspect='equal',xticks=[-3,0,3],yticks=[-3,0,3])
        ax.set(xlabel='$x$（无量纲）',ylabel='$y$（无量纲）')
    cb = fig.colorbar(im, ax=list(axs), fraction=.026, pad=.02, shrink=.72)
    cb.set_label('联合密度（无量纲）', fontsize=9)
    cb.outline.set_linewidth(.6)
    save(fig, axs, '04_bivariate_normal')


def normal_conditional():
    fig, axs = pair()
    rho, sigma = .8, .6
    x = np.linspace(-3.2,3.2,801)
    for i,y in enumerate([-1,0,1]):
        f = np.exp(-.5*((x-rho*y)/sigma)**2)/(sigma*math.sqrt(2*math.pi))
        axs[0].plot(x,f,STYLES[i],color=COLORS[i],marker=MARKERS[i],markevery=100,ms=3.5,
                    label=rf'$Y={y:g}$')
    density_labels(axs[0], '$x$（无量纲）')
    axs[0].legend(loc='upper right')
    y = np.linspace(-2,2,401)
    axs[1].fill_between(y,rho*y-sigma,rho*y+sigma,alpha=.2,color=BLUE,linewidth=0,
                        label='条件均值 ± 1 条件标准差')
    axs[1].plot(y,rho*y,color=BLUE,label=r'$E(X\mid Y=y)=0.8y$')
    axs[1].set(xlabel='给定的 $y$（无量纲）',ylabel='$X$ 的条件位置（无量纲）',xlim=(-2,2))
    axs[1].legend(loc='upper left',fontsize=7)
    save(fig, axs, '05_normal_conditional')


def sum_uniform():
    fig, axs = pair()
    z = np.linspace(-.2,2.2,1001)
    f = np.where((z>0)&(z<=1),z,np.where((z>1)&(z<2),2-z,0))
    u = np.clip(z,0,2)
    F = np.where(u<=1,u*u/2,1-(2-u)**2/2)
    axs[0].plot(z,f,color=BLUE)
    v = np.linspace(.5,1.5,501)
    axs[0].fill_between(v,np.minimum(v,2-v),alpha=.25,color=ORANGE,linewidth=0)
    axs[0].text(.04,.9,'阴影面积 = 0.7500',transform=axs[0].transAxes,fontsize=8)
    axs[1].plot(z,F,color=BLUE)
    axs[1].plot([.5,1.5],[.125,.875],'o',color=ORANGE,ls='none')
    density_labels(axs[0],'和 $z=x+y$（无量纲）')
    axs[1].set(xlabel='和 $z=x+y$（无量纲）',ylabel='累计概率 $F_Z(z)$（无量纲）',ylim=(0,1.055))
    for ax in axs:
        ax.set_xlim(-.2,2.2)
    save(fig, axs, '06_sum_uniform')


def linear_transform():
    fig, axs = pair()
    fig.set_size_inches(ss.figsize('double', height_mm=100))
    axs[0].add_patch(patches.Polygon([(0,0),(1,0),(1,1),(0,1)],facecolor=BLUE,alpha=.17,edgecolor=BLUE))
    axs[1].add_patch(patches.Polygon([(0,0),(1,1),(2,0),(1,-1)],facecolor=BLUE,alpha=.17,edgecolor=BLUE))
    points = np.array([[0,0],[1,0],[1,1],[0,1]])
    converted = np.column_stack([points.sum(1),points[:,0]-points[:,1]])
    for ax, coords in zip(axs,[points,converted]):
        for i,(a,b) in enumerate(coords):
            ax.plot(a,b,'o',color=BLUE,ms=4)
            ax.annotate(str(i+1),(a,b),xytext=(5,5),textcoords='offset points',fontsize=8)
        ax.set_aspect('equal')
    xy_labels(axs[0])
    axs[0].set(xlim=(-.3,1.35),ylim=(-.3,1.35))
    xy_labels(axs[1], '和 $u=x+y$（无量纲）','差 $v=x-y$（无量纲）')
    axs[1].set(xlim=(-.3,2.35),ylim=(-1.3,1.35))
    axs[0].text(.06,.92,'面积 = 1；密度 = 1',transform=axs[0].transAxes,fontsize=8)
    axs[1].text(.06,.92,'面积 = 2；密度 = 1/2',transform=axs[1].transAxes,fontsize=8)
    save(fig, axs, '07_linear_transform')


def multinomial_matrix(n=3, p1=.25, p2=.25):
    arr = np.zeros((n+1,n+1))
    for i in range(n+1):
        for j in range(n+1-i):
            arr[i,j] = math.factorial(n)/(math.factorial(i)*math.factorial(j)*math.factorial(n-i-j))*p1**i*p2**j*(1-p1-p2)**(n-i-j)
    return arr


def multinomial():
    fig, axs = pair()
    arr = multinomial_matrix()
    im = axs[0].imshow(arr, origin='upper',cmap='cividis',vmin=0,vmax=.2)
    for i in range(4):
        for j in range(4):
            text = f'{arr[i,j]:.3f}' if i+j<=3 else '0'
            axs[0].text(j,i,text,ha='center',va='center',fontsize=7,color='white' if arr[i,j]<.1 else 'black')
    axs[0].set(xlabel='列：第 2 类次数 $Y$',ylabel='行：第 1 类次数 $X$',xticks=range(4),yticks=range(4))
    ss.colorbar(fig,im,axs[0],'联合概率（无量纲）')
    axs[1].bar(range(4),arr.sum(1),color=BLUE,width=.55,edgecolor='.2',linewidth=.6)
    axs[1].set(xlabel='第 1 类次数 $k$（次）',ylabel='边缘概率 $P(X=k)$（无量纲）',ylim=(0,.5),xticks=range(4))
    for ax in axs:
        ax.minorticks_off()
    save(fig, axs, '08_multinomial')


def tables():
    coords = [0,.25,.5,.75,1]
    cdf = [[float(triangle_cdf(x,y)) for y in coords] for x in coords]
    data = dict(discrete_joint=JOINT.tolist(), discrete_cdf=JOINT.cumsum(0).cumsum(1).tolist(),
                discrete_marginal_x=JOINT.sum(1).tolist(),discrete_marginal_y=JOINT.sum(0).tolist(),
                discrete_y_given_x=(JOINT/JOINT.sum(1)[:,None]).tolist(),
                triangle_coordinates=coords,triangle_cdf=cdf,
                triangle_marginals=[dict(t=t,pdf_x=2*(1-t),pdf_y=2*t,cdf_x=2*t-t*t,cdf_y=t*t) for t in [.25,.5,.75]],
                multinomial=multinomial_matrix().tolist(),
                normal_conditionals=[dict(y=y,mean=.8*y,variance=.36,std=.6) for y in [-1,0,1]],
                uniform_sum=[dict(z=z,pdf=min(z,2-z),cdf=z*z/2 if z<=1 else 1-(2-z)**2/2) for z in [0,.5,1,1.5,2]])
    (OUT/'numerical_tables.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'numerical_tables.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.writer(stream)
        writer.writerow(['model','x','y','value'])
        for key in ['discrete_joint','discrete_cdf','multinomial']:
            for i,row in enumerate(data[key]):
                for j,v in enumerate(row):
                    writer.writerow([key,i,j,v])
        for i,x in enumerate(coords):
            for j,y in enumerate(coords):
                writer.writerow(['triangle_cdf',x,y,cdf[i][j]])
    # Checks connect joint probabilities, marginalization and conditioning.
    assert np.isclose(JOINT.sum(),1)
    assert np.allclose((JOINT/JOINT.sum(1)[:,None]).sum(1),1)
    assert np.allclose(JOINT.cumsum(0).cumsum(1)[-1,:],JOINT.sum(0).cumsum())
    assert np.isclose(multinomial_matrix().sum(),1)
    assert np.isclose(triangle_cdf(.5,.75),.5)
    assert np.all(np.diff(np.array(cdf),axis=0)>=-1e-12)
    assert np.all(np.diff(np.array(cdf),axis=1)>=-1e-12)


def main():
    ss.grayscale_check(COLORS)  # Linestyles and markers also distinguish curves.
    discrete_joint()
    continuous_joint()
    marginals_conditionals()
    normal_contours()
    normal_conditional()
    sum_uniform()
    linear_transform()
    multinomial()
    marginal_line()
    marginal_area()
    tables()
    meta=dict(versions=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__),
              font=FONT,source='analytic distributions; no observations',figures=FIGURES)
    (OUT/'figure_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Complete: {len(FIGURES)} figures and analytic tables.')


if __name__=='__main__':
    main()
