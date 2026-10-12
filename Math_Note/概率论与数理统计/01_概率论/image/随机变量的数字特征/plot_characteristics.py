"""Analytic figures for the numerical characteristics of random variables.

Run: python plot_characteristics.py
All models and moments are analytic; no random observations are simulated.
Output: vector PDF + 600-dpi PNG, exactly 178 mm wide, and QA previews.
"""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image, ImageOps, ImageDraw
import sci_style as ss

OUT = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ["Microsoft YaHei", "Noto Sans CJK SC", "DejaVu Sans"]
ss.apply("double", font_size=9, tick_size=8, legend_size=7.5, mathtext=False)
plt.rcParams["savefig.pad_inches"] = 0
BLUE, ORANGE = [ss.OKABE_ITO[k] for k in ("blue", "vermillion")]
GRAY = "0.45"
RECORDS = []


def pair(height=86):
    fig, axs = plt.subplots(1, 2, figsize=ss.figsize("double", height_mm=height))
    fig.subplots_adjust(left=.10, right=.96, bottom=.24, top=.87, wspace=.49)
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                            edgecolor="none", facecolor="none", linewidth=0))
    ss.panels(fig, axs, "AB", x=0, y=1.035)
    for ax in axs:
        ax.minorticks_off()
    return fig, axs


def foot(ax, text):
    ax.text(.5, -.34, text, transform=ax.transAxes, ha="center", va="top", fontsize=8)


def note(ax, x, y, text, **kw):
    ax.text(x, y, text, fontsize=8, bbox=dict(facecolor="white", edgecolor="none", alpha=.9, pad=1.1), **kw)


def normpdf(x, mu=0., sigma=1.):
    return np.exp(-.5*((x-mu)/sigma)**2)/(sigma*np.sqrt(2*np.pi))


def save(fig, name):
    width, height = fig.get_size_inches()
    for _ in range(28):
        fig.canvas.draw()
        bb = fig.get_tightbbox(fig.canvas.get_renderer())
        if bb.x0 >= -1e-5 and bb.y0 >= -1e-5 and bb.x1 <= width+1e-5 and bb.y1 <= height+1e-5:
            break
        for ax in fig.axes:
            p = ax.get_position(original=True)
            ax.set_position([.5+.94*(p.x0-.5), .5+.94*(p.y0-.5), .94*p.width, .94*p.height])
    else:
        raise RuntimeError(f"Text exceeds fixed canvas: {name}")
    path = ss.save(fig, OUT/f"{name}.pdf", also_png=True, dpi=600)
    size = ss.output_size_mm(path)
    assert size and abs(size[0]-178) < .05, size
    with Image.open(path.with_suffix(".png")) as im:
        assert abs(im.info["dpi"][0]-600) < .1
    RECORDS.append(dict(name=name, width_mm=round(size[0],3), height_mm=round(size[1],3), png_dpi=600))
    plt.close(fig)


def weighted_mean():
    fig,axs=pair()
    x=np.array([0,1,3]); p=np.array([.25,.5,.25]); mu=float(x@p)
    axs[0].bar(x,p,width=.30,color=BLUE,edgecolor="black",lw=.6)
    axs[1].bar(x,x*p,width=.30,color=ORANGE,edgecolor="black",lw=.6,hatch="///")
    for ax in axs:
        ax.set(xlim=(-.35,3.35),xlabel="取值 $x$（无量纲）",xticks=[0,1,3])
        ax.axvline(mu,color=GRAY,lw=1,ls="--")
    axs[0].set(ylim=(0,.65),ylabel="单点概率 $p_k$（无量纲）")
    axs[1].set(ylim=(0,.97),ylabel="期望贡献 $x_kp_k$（无量纲）")
    note(axs[0],1.36,.56,r"$\mu=5/4$")
    note(axs[1],1.50,.87,r"$\sum_kx_kp_k=5/4$")
    for xx,pp in zip(x,p):
        axs[0].text(xx,pp+.03,f"{pp:g}",ha="center",fontsize=8)
    for xx,val in zip(x,x*p):
        axs[1].text(xx,val+.035,f"{val:g}",ha="center",fontsize=8)
    foot(axs[0],r"$\sum_k p_k=1$")
    foot(axs[1],r"$E(X)=5/4,\quad D(X)=19/16$")
    save(fig,"01_weighted_mean")


def location_spread():
    fig,axs=pair(88)
    x=np.linspace(-5,5,1601)
    for mu,col,ls in [(-1,BLUE,"-"),(1,ORANGE,"--")]:
        axs[0].plot(x,normpdf(x,mu,.7),color=col,ls=ls,label=rf"$\mu={mu},\ \sigma=0.7$")
        axs[0].axvline(mu,color=col,lw=.75,ls=":")
    for sigma,col,ls in [(.5,BLUE,"-"),(1.5,ORANGE,"--")]:
        axs[1].plot(x,normpdf(x,0,sigma),color=col,ls=ls,label=rf"$\mu=0,\ \sigma={sigma}$")
    for ax in axs:
        ax.set(xlim=(-4.5,4.5),ylim=(0,.88),xlabel="取值 $x$（无量纲）",ylabel="密度 $f(x)$（无量纲）")
        ax.set_xticks([-4,-2,0,2,4]);ax.set_yticks([0,.4,.8])
        ax.legend(loc="upper right")
    foot(axs[0],r"$D(X)=0.49$：中心位置改变")
    foot(axs[1],r"$E(X)=0$：分散尺度改变")
    save(fig,"02_location_spread")


def same_moments():
    fig,axs=pair()
    axs[0].bar([-1,1],[.5,.5],width=.22,color=BLUE,edgecolor="black",lw=.7)
    axs[0].set(xlim=(-3,3),ylim=(0,.65),xlabel="取值 $x$（无量纲）",ylabel="单点概率（无量纲）")
    note(axs[0],-.35,.53,"两点分布")
    x=np.linspace(-4,4,1201)
    axs[1].plot(x,normpdf(x),color=ORANGE,ls="--")
    axs[1].set(xlim=(-4,4),ylim=(0,.5),xlabel="取值 $x$（无量纲）",ylabel="概率密度（无量纲）")
    note(axs[1],.75,.40,r"$N(0,1)$")
    for ax in axs: foot(ax,r"$E(X)=0,\quad D(X)=1$")
    save(fig,"03_same_moments")


def covariance_direction():
    fig,axs=pair(86)
    t=np.linspace(0,2*np.pi,361); unit=np.vstack([np.cos(t),np.sin(t)])
    for ax,rho,col in zip(axs,[.8,-.8],[BLUE,ORANGE]):
        Sigma=np.array([[1,rho],[rho,1]])
        eig,Q=np.linalg.eigh(Sigma)
        for radius,ls in [(1,"-"),(2,"--")]:
            pts=Q @ np.diag(np.sqrt(eig))*radius @ unit
            ax.plot(pts[0],pts[1],color=col,ls=ls,lw=1.3)
        ax.axhline(0,color=".75",lw=.7);ax.axvline(0,color=".75",lw=.7)
        x=np.linspace(-2.4,2.4,100)
        ax.plot(x,rho*x,color=GRAY,ls=":",lw=1)
        ax.set(xlim=(-2.5,2.5),ylim=(-2.5,2.5),aspect="equal",
               xlabel="中心化取值 $x$（无量纲）",ylabel="中心化取值 $y$（无量纲）")
        ax.set_xticks([-2,0,2]);ax.set_yticks([-2,0,2])
        note(ax,-2.3,2.05,rf"$\rho={rho}$",color=col)
        foot(ax,rf"$\operatorname{{Cov}}(X,Y)={rho}$")
    save(fig,"04_covariance_direction")


def uncorrelated_dependence():
    fig,axs=pair(90)
    x=np.linspace(-1,1,1001); y=x*x; g=x*(x*x-1/3)
    axs[0].plot(x,y,color=BLUE)
    axs[0].axhline(1/3,color=GRAY,ls="--",lw=.9)
    note(axs[0],-.92,.40,r"$E(Y)=1/3$")
    note(axs[0],-.36,.86,r"$Y=X^2$")
    axs[0].set(xlim=(-1.08,1.08),ylim=(-.03,1.1),xlabel="取值 $x$（无量纲）",ylabel="取值 $y$（无量纲）")
    axs[1].plot(x,g,color=GRAY,lw=1.2)
    axs[1].fill_between(x,0,g,where=g>=0,color=BLUE,alpha=.25)
    axs[1].fill_between(x,0,g,where=g<0,color=ORANGE,alpha=.25,hatch="///")
    axs[1].axhline(0,color=".7",lw=.7)
    axs[1].set(xlim=(-1.08,1.08),ylim=(-.76,.76),xlabel="取值 $x$（无量纲）",ylabel="中心化乘积 $x(x^2-1/3)$")
    note(axs[1],-.93,.52,r"$g(-x)=-g(x)$")
    for ax in axs: ax.set_xticks([-1,0,1])
    foot(axs[0],r"$X\sim U(-1,1)$：确定性非线性联系")
    foot(axs[1],r"$\operatorname{Cov}(X,Y)=\frac{1}{2}\int_{-1}^1g(x)\,dx=0$")
    save(fig,"05_uncorrelated_dependence")


def total_variance():
    fig,axs=pair(90)
    x=np.linspace(-3,9,1601);f0=.5*normpdf(x,1,1);f1=.5*normpdf(x,5,1)
    axs[0].plot(x,f0,color=BLUE,ls="--",label=r"$\frac{1}{2}f_{X\mid G=0}$")
    axs[0].plot(x,f1,color=ORANGE,ls="-.",label=r"$\frac{1}{2}f_{X\mid G=1}$")
    axs[0].plot(x,f0+f1,color="black",lw=1.8,label="总体密度")
    axs[0].axvline(3,color=GRAY,ls=":",lw=.8)
    axs[0].set(xlim=(-2.5,8.5),ylim=(0,.33),xlabel="取值 $x$（无量纲）",ylabel="密度（无量纲）")
    axs[0].legend(loc="upper center")
    note(axs[0],3.2,.07,r"$E(X)=3$")
    vals=[1,4,5]
    bars=axs[1].bar([0,1,2],vals,width=.58,color=[BLUE,ORANGE,"0.5"],edgecolor="black",lw=.7)
    for bar,hatch in zip(bars,["","///","xx"]):bar.set_hatch(hatch)
    for i,v in enumerate(vals):axs[1].text(i,v+.16,str(v),ha="center",fontsize=9)
    axs[1].set(ylim=(0,6),xticks=[0,1,2],xticklabels=["组内","组间","总体"],ylabel="方差（无量纲平方）")
    foot(axs[0],r"$X\mid G=0\sim N(1,1),\quad X\mid G=1\sim N(5,1)$")
    foot(axs[1],r"$D(X)=E[D(X\mid G)]+D[E(X\mid G)]$")
    save(fig,"06_total_variance")


def continuous_expectation():
    fig,axs=pair(86)
    x=np.linspace(0,2,501)
    for ax,y,col in zip(axs,[x/2,x*x/2],[BLUE,ORANGE]):
        ax.fill_between(x,0,y,color=col,alpha=.18)
        ax.plot(x,y,color=col)
        ax.set(xlim=(0,2.15),ylim=(0,2.35),xlabel="取值 $x$（无量纲）")
        ax.set_xticks([0,1,2]);ax.set_yticks([0,1,2])
    axs[0].set_ylabel("概率密度 $f_X(x)$（无量纲）")
    axs[1].set_ylabel("加权函数 $xf_X(x)$（无量纲）")
    note(axs[0],.4,.50,r"$\int_0^2 f_X(x)\,dx=1$")
    note(axs[1],.1,1.90,r"$\int_0^2 x f_X(x)\,dx=4/3$")
    foot(axs[0],r"$f_X(x)=x/2,\quad 0<x<2$")
    foot(axs[1],r"$E(X)=4/3,\quad D(X)=2/9$")
    save(fig,"07_continuous_expectation")


def verify():
    x=np.array([0,1,3]);p=np.array([.25,.5,.25]);mu=x@p
    assert np.isclose(mu,5/4) and np.isclose((x*x)@p-mu*mu,19/16)
    grid=np.linspace(0,2,20001)
    assert np.isclose(np.trapezoid(grid*grid/2,grid),4/3,atol=1e-8)
    assert np.isclose(np.trapezoid(grid**3/2,grid),2,atol=1e-8)
    x=np.linspace(-1,1,20001)
    assert np.isclose(np.trapezoid(x*(x*x-1/3),x)/2,0,atol=1e-12)
    grid=np.linspace(-12,18,30001);f=.5*normpdf(grid,1)+.5*normpdf(grid,5)
    assert np.isclose(np.trapezoid(f,grid),1,atol=1e-8)
    assert np.isclose(np.trapezoid(grid*f,grid),3,atol=1e-8)
    assert np.isclose(np.trapezoid((grid-3)**2*f,grid),5,atol=1e-8)
    # Normal ellipses satisfy v^T Sigma^{-1} v = r^2.
    for rho in [.8,-.8]:
        S=np.array([[1,rho],[rho,1]]);L=np.linalg.cholesky(S)
        v=L@np.array([.6,.8]); assert np.isclose(v@np.linalg.solve(S,v),1)
    print("[ok] analytic moments, mixture variance, and ellipse checks")


def previews():
    for start in range(0,len(RECORDS),4):
        sheet=Image.new("RGB",(2280,1180),"white")
        for i,record in enumerate(RECORDS[start:start+4]):
            with Image.open(OUT/(record["name"]+".png")) as im:
                im=im.convert("RGB");im.thumbnail((1100,540),Image.Resampling.LANCZOS)
                xx=(i%2)*1140+(1140-im.width)//2; yy=(i//2)*590+12
                sheet.paste(im,(xx,yy))
                ImageDraw.Draw(sheet).text(((i%2)*1140+20,(i//2)*590+567),record["name"],fill="black")
        sheet.save(OUT/f"preview-{start//4+1}.png")
        ImageOps.grayscale(sheet).save(OUT/f"preview-{start//4+1}-gray.png")


if __name__=="__main__":
    verify()
    ss.grayscale_check([BLUE,ORANGE])
    print("[style] direct labels, separate panels, dashes and hatches supplement color")
    for maker in [weighted_mean,location_spread,same_moments,covariance_direction,
                  uncorrelated_dependence,total_variance,continuous_expectation]:maker()
    previews()
    (OUT/"figure_manifest.json").write_text(json.dumps(RECORDS,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"[ok] {len(RECORDS)} figures, each 178 mm, PDF + 600 dpi PNG")
