"""Additional principle and worked-example figures; pure geometric data.

Run: python make_principle_figures.py
Shares the style, projection and export checks in make_figures.py.
Outputs fig-09 through fig-20, PDF + 600-dpi PNG, 178 mm wide.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Arc
from matplotlib.lines import Line2D
import make_figures as b

BLUE, ORANGE, GRAY, PALE, DASH = b.BLUE, b.ORANGE, b.GRAY, b.PALE, b.DASH
figures, label, arrow, footer, plane = b.figure, b.label, b.arrow, b.footer, b.plane


def riemann_sum():
    fig, axs = figures(86)
    ax = axs[0]
    plane(ax, (-.05, 1.10), (-.05, 1.10))
    ax.set_xticks([0, .5, 1]); ax.set_yticks([0, .5, 1])
    n = 3
    for i in range(n):
        for j in range(n):
            ax.add_patch(Rectangle((i/n, j/n), 1/n, 1/n,
                                  facecolor=PALE, edgecolor="0.65", lw=.7))
    ax.add_patch(Rectangle((1/n, 0), 1/n, 1/n, facecolor="#FBE8DA", edgecolor=ORANGE, lw=1.5))
    ax.plot(.5, 1/6, "o", ms=4, color=ORANGE)
    label(ax, (.5, .42), r"$(\xi_i,\eta_i)$", color=ORANGE)
    label(ax, (.88, .88), "$D$", color=BLUE)
    label(ax, (.5, .065), r"$\Delta A_i$", color=ORANGE)
    footer(ax, r"$D=\bigcup_iD_i$", y=-.34)
    ax = axs[1]
    plane(ax, (-.8, 1.3), (-.18, 2.15), ticks=False)
    # Nine Riemann columns for f(x,y)=.6+x+.5*y; top values at cell centers.
    for i, j in [(i, j) for j in range(n-1, -1, -1) for i in range(n)]:
        x, y, d = i/n, j/n, 1/n
        h = .6+(i+.5)/n+.5*(j+.5)/n
        selected = i == 1 and j == 0
        faces = [np.array([[x,y,0],[x+d,y,0],[x+d,y,h],[x,y,h]]),
                 np.array([[x,y,0],[x,y+d,0],[x,y+d,h],[x,y,h]]),
                 np.array([[x,y,h],[x+d,y,h],[x+d,y+d,h],[x,y+d,h]])]
        for k, face in enumerate(faces):
            ax.add_patch(Polygon(b.project(face), facecolor=("#FBE8DA" if selected else ["0.9","0.82","0.96"][k]),
                                 edgecolor=ORANGE if selected else "0.55", lw=1 if selected else .55))
    b.space_axes(ax, 1.25)
    p = np.array([.5, 0, 0]); h = .6+.5+.5/6
    b.space_arrow(ax, p, p+[0,0,h], color=ORANGE, ls=DASH, lw=1.2)
    b.space_label(ax, p+[0,0,h/2], "$f_i$", offset=(.20,0), color=ORANGE)
    label(ax, (.33, 1.95), r"$f_i=f(\xi_i,\eta_i)$")
    footer(ax, r"$\sum_i f_i\Delta A_i\ \longrightarrow\ \iint_D f\,dA$", y=-.16)
    b.save(fig, "fig-09-riemann-sum", "区域分割与高度乘底面积的黎曼和；非负函数的体积解释。")


def radial_example():
    fig, axs = figures(82)
    ax = axs[0]
    plane(ax, (-1.28, 1.28), (-1.28, 1.28), ticks=False)
    ax.add_patch(Circle((0,0), 1, facecolor=PALE, edgecolor=BLUE, lw=1.4))
    ax.add_patch(Circle((0,0), .69, facecolor="#FBE8DA", edgecolor=ORANGE, lw=1))
    ax.add_patch(Circle((0,0), .6, facecolor=PALE, edgecolor=ORANGE, lw=1))
    arrow(ax, (0,0), (.6,0), color=GRAY, lw=1)
    label(ax, (.3,-.13), "$r$", color=GRAY)
    arrow(ax, (.60,0), (.69,0), color=ORANGE, size=6)
    label(ax, (.83,-.10), "$dr$", color=ORANGE)
    label(ax, (0,1.18), "$x^2+y^2\\leq1$")
    label(ax, (0,-.86), "$f=r^2$")
    footer(ax, r"$dA_{\mathrm{ring}}=2\pi r\,dr$", y=-.12)
    ax = axs[1]
    r = np.linspace(0,1,300); weight = 2*np.pi*r**3
    ax.fill_between(r, 0, weight, facecolor=PALE)
    ax.plot(r, weight, color=BLUE)
    ax.set(xlim=(0,1.05), ylim=(0,7), xlabel=r"$r$ (dimensionless)",
           ylabel=r"$2\pi r^3$ (dimensionless)")
    ax.set_xticks([0,.5,1]); ax.set_yticks([0,np.pi,2*np.pi], ["$0$","$\\pi$","$2\\pi$"])
    ax.minorticks_off()
    label(ax, (.68,1.3), r"$\int_0^1 2\pi r^3\,dr=\pi/2$")
    footer(ax, r"$f(r)\,dA_{\mathrm{ring}}=2\pi r^3\,dr$", y=-.34)
    b.save(fig, "fig-10-radial-example", "圆盘径向积分：同心环面积权重 2pi*r 与函数 r^2 的乘积。")


def volume_slices():
    fig, axs = figures(86)
    ax = axs[0]
    plane(ax, (-.78,1.12), (-.17,1.43), ticks=False)
    O, X, Y, Z = np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1]])
    ax.add_patch(Polygon(b.project([X,Y,Z]), facecolor="#E5F0F6", edgecolor=BLUE, lw=1.4))
    for p in [X,Y,Z]: b.space_line(ax,[O,p],color=GRAY,lw=.8,ls=DASH)
    b.space_axes(ax, 1.12)
    p=np.array([.25,.25,0]); q=p+[0,0,.5]
    b.space_arrow(ax,p,q,color=ORANGE,lw=2)
    b.space_label(ax, q, "$1-x-y$", offset=(.23,.1), color=ORANGE)
    label(ax, (.22,1.23), "$x+y+z=1$", color=BLUE)
    footer(ax, r"$0\leq z\leq1-x-y$", y=-.15)
    ax=axs[1]
    plane(ax,(-.06,1.08),(-.06,1.08))
    ax.set_xticks([0,.5,1]); ax.set_yticks([0,.5,1])
    ax.add_patch(Polygon([[0,0],[1,0],[0,1]],facecolor=PALE,edgecolor=BLUE,lw=1.4))
    ax.plot(.25,.25,"o",ms=4,color=ORANGE)
    label(ax,(.28,.41),"$(x,y)$",color=ORANGE)
    label(ax,(.18,.73),"$D$",color=BLUE)
    label(ax,(.70,.42),"$x+y=1$",color=BLUE)
    footer(ax,r"$V=\int_0^1\!\int_0^{1-x}\!\int_0^{1-x-y}dz\,dy\,dx=1/6$",y=-.34)
    b.save(fig,"fig-11-volume-slices","四面体的竖直线段与平面投影；高度积分再累积投影面积。")


def tangent_component():
    fig,axs=figures(82)
    ax=axs[0]
    plane(ax,(-.08,1.45),(-.15,1.10),ticks=False)
    x=np.linspace(0,1.25,250); y=.4*x*x
    ax.plot(x,y,color=BLUE)
    p=np.array([.55,.4*.55**2]); tangent=np.array([1,.8*.55]); tangent/=np.linalg.norm(tangent)
    ax.plot(*p,"o",ms=4,color="black")
    arrow(ax,p,p+.52*tangent,color=BLUE,ls=DASH)
    label(ax,p+.55*tangent+[.1,.06],r"$\boldsymbol{\tau}$",color=BLUE)
    xx=np.linspace(.55,.75,30)
    ax.plot(xx,.4*xx**2,color=ORANGE,lw=3)
    label(ax,(.68,.01),"$ds$",color=ORANGE)
    arrow(ax,(.55,.4*.55**2),(.75,.4*.75**2),color=ORANGE,lw=.8,size=6)
    label(ax,(.28,.38),"$C$",color=BLUE)
    footer(ax,r"$d\mathbf r=\boldsymbol{\tau}\,ds$",y=-.15)
    ax=axs[1]
    plane(ax,(-.20,1.25),(-.20,1.20),ticks=False)
    O=np.array([0.,0.]); F=np.array([.75,.85]); Ft=np.array([.75,0.])
    ax.plot([-.12,1.16],[0,0],color=BLUE,lw=1.3)
    arrow(ax,O,F,color=ORANGE,lw=1.8)
    arrow(ax,O,Ft,color=BLUE,lw=2)
    arrow(ax,Ft,F,color=GRAY,ls=DASH)
    ax.add_patch(Arc(O,.50,.50,theta1=0,theta2=np.degrees(np.arctan2(F[1],F[0])),color=GRAY,lw=.8))
    label(ax,(.27,.14),"$\\alpha$",color=GRAY)
    label(ax,(.77,1.0),"$\\mathbf F$",color=ORANGE)
    label(ax,(.36,-.12),r"$(\mathbf F\cdot\boldsymbol{\tau})\boldsymbol{\tau}$",color=BLUE)
    label(ax,(1.07,.49),r"$\mathbf F_{\perp}$",color=GRAY)
    footer(ax,r"$\mathbf F\cdot d\mathbf r=\|\mathbf F\|\cos\alpha\,ds$",y=-.15)
    b.save(fig,"fig-12-tangent-component","有向位移与切向量的关系；法向分量不贡献功。")


def surface_element():
    fig,axs=figures(84)
    ax=axs[0]
    plane(ax,(-.18,1.2),(-.16,1.18),ticks=False)
    ax.add_patch(Rectangle((.18,.18),.66,.55,facecolor=PALE,edgecolor=BLUE,lw=1.4))
    arrow(ax,(.18,.18),(.84,.18),color=BLUE)
    arrow(ax,(.18,.18),(.18,.73),color=ORANGE)
    label(ax,(.5,.08),"$du$",color=BLUE)
    label(ax,(.055,.47),"$dv$",color=ORANGE)
    label(ax,(.5,.48),"$du\\,dv$")
    arrow(ax,(0,0),(1.07,0),color=GRAY,lw=.7)
    arrow(ax,(0,0),(0,1.02),color=GRAY,lw=.7)
    label(ax,(1.13,0),"$u$",color=GRAY)
    label(ax,(0,1.1),"$v$",color=GRAY)
    footer(ax,r"$(u,v)\mapsto\mathbf r(u,v)$",y=-.16)
    ax=axs[1]
    plane(ax,(-.78,1.20),(-.22,1.80),ticks=False)
    ru=np.array([1,0,1.]); rv=np.array([0,1,.5]); O=np.zeros(3)
    a=.66*ru; c=.55*rv; normal=np.cross(ru,rv); normal/=np.linalg.norm(normal)
    ax.add_patch(Polygon(b.project([O,a,a+c,c]),facecolor=PALE,edgecolor=GRAY,lw=1))
    b.space_arrow(ax,O,a,color=BLUE,lw=1.7)
    b.space_arrow(ax,O,c,color=ORANGE,lw=1.7)
    b.space_label(ax,a*.65,r"$\mathbf r_u\,du$",offset=(.25,-.1),color=BLUE)
    b.space_label(ax,c*.65,r"$\mathbf r_v\,dv$",offset=(-.20,.1),color=ORANGE)
    center=(a+c)/2
    b.space_arrow(ax,center,center+.80*normal,color=GRAY,ls=DASH,lw=1.4)
    b.space_label(ax,center+.9*normal,r"$\mathbf r_u\times\mathbf r_v$",offset=(.03,.16))
    footer(ax,r"$dS=\|\mathbf r_u\times\mathbf r_v\|\,du\,dv$",y=-.16)
    b.save(fig,"fig-13-surface-element","参数矩形对应切平行四边形；叉积的模表示面积，方向表示法向。")


def green_orientation():
    fig,axs=figures(82)
    ax=axs[0]
    plane(ax,(-1.35,1.35),(-1.35,1.35),ticks=False)
    ax.add_patch(Circle((0,0),1,facecolor=PALE,edgecolor=BLUE,lw=1.5))
    ax.add_patch(Circle((0,0),.40,facecolor="white",edgecolor=ORANGE,lw=1.5,ls=DASH))
    for a in [.2,2.2,4.2]:
        b.arc_arrow(ax,a,a+.42,color=BLUE)
        b.arc_arrow(ax,a+.42,a,radius=.40,color=ORANGE)
    arrow(ax,(1,0),(1.23,0),color=BLUE)
    arrow(ax,(-.40,0),(-.18,0),color=ORANGE,ls=DASH)
    label(ax,(0,.70),"$D$",color=GRAY)
    label(ax,(0,1.23),"$C_{\\mathrm{out}}$",color=BLUE)
    label(ax,(0,-.18),"$C_{\\mathrm{in}}$",color=ORANGE)
    footer(ax,r"$\partial D=C_{\mathrm{out}}+C_{\mathrm{in}}$",y=-.12)
    ax=axs[1]
    plane(ax,(-2.45,2.45),(-1.45,1.55))
    ax.set_xticks([-2,0,2]);ax.set_yticks([-1,0,1])
    t=np.linspace(0,2*np.pi,361); x=2*np.cos(t);y=np.sin(t)
    ax.fill(x,y,color=PALE);ax.plot(x,y,color=BLUE)
    for a in [.5,2.5,4.5]:
        p=np.array([2*np.cos(a),np.sin(a)]); q=np.array([2*np.cos(a+.15),np.sin(a+.15)])
        arrow(ax,p,q,color=BLUE,size=8)
    label(ax,(0,.32),"$x^2/4+y^2\\leq1$")
    label(ax,(0,-.30),"$A=2\\pi$",color=BLUE)
    footer(ax,r"$A=\frac{1}{2}\oint_C(x\,dy-y\,dx)$",y=-.34)
    b.save(fig,"fig-14-green-orientation","Green 正向边界：外逆内顺；例题中的椭圆边界与区域面积。")


def gauss_sphere():
    fig,axs=figures(84)
    ax=axs[0]
    plane(ax,(-1.42,1.42),(-1.35,1.45),ticks=False)
    ax.add_patch(Circle((0,0),1,facecolor=PALE,edgecolor=BLUE,lw=1.4))
    for t in np.linspace(0,2*np.pi,9)[:-1]:
        u=np.array([np.cos(t),np.sin(t)])
        arrow(ax,.55*u,1.13*u,color=ORANGE,lw=1.3,size=8)
    arrow(ax,(0,0),(.70,-.714),color=GRAY,lw=.8,ls=DASH)
    label(ax,(.22,-.38),"$R=1$",color=GRAY)
    label(ax,(0,1.31),"$\\mathbf F=(x,y,z)$",color=ORANGE)
    label(ax,(0,.19),"$\\nabla\\cdot\\mathbf F=3$")
    label(ax,(0,-.95),"$\\mathbf F\\cdot\\mathbf n=1$")
    footer(ax,r"$\Phi=1\times4\pi=4\pi$",y=-.12)
    ax=axs[1]
    z=np.linspace(-1,1,300);density=3*np.pi*(1-z*z)
    ax.fill_between(z,0,density,color=PALE);ax.plot(z,density,color=BLUE)
    ax.set(xlim=(-1.08,1.08),ylim=(0,10.5),xlabel=r"$z$ (dimensionless)",
           ylabel=r"$3\,\mathrm{Area}(D_z)$ (dimensionless)")
    ax.set_xticks([-1,0,1]);ax.set_yticks([0,3*np.pi],["$0$","$3\\pi$"])
    ax.minorticks_off()
    label(ax,(0,3),r"$\int_{-1}^1 3\pi(1-z^2)\,dz=4\pi$")
    footer(ax,r"$\iiint_\Omega3\,dV=3\,\mathrm{Vol}(\Omega)$",y=-.34)
    b.save(fig,"fig-15-gauss-sphere","单位球上 F·n=1；内部常散度的积分等于向外通量 4pi。")


def cap(ax,close=False):
    t=np.linspace(0,2*np.pi,241);phis=np.linspace(0,np.pi/2,60)
    circle=np.column_stack([np.cos(t),np.sin(t),np.zeros_like(t)])
    for az in np.linspace(0,2*np.pi,9)[:-1]:
        pts=np.column_stack([np.sin(phis)*np.cos(az),np.sin(phis)*np.sin(az),np.cos(phis)])
        b.space_line(ax,pts,color="0.67",lw=.7)
    if close:
        ax.add_patch(Polygon(b.project(circle),facecolor=PALE,edgecolor="none",alpha=.65))
    b.space_line(ax,circle,color=BLUE,lw=1.5)
    p=np.array([.45,-.30,np.sqrt(1-.45**2-.3**2)])
    b.space_arrow(ax,p,p*1.40,color=BLUE,ls=DASH,lw=1.3)
    b.space_label(ax,p*1.53,"$\\mathbf n$",color=BLUE)
    b.space_arrow(ax,[-.45,0,.82],[-.45,0,1.30],color=ORANGE,lw=1.4)
    label(ax,(-.63,1.32),"$\\mathbf F=(0,0,1)$",color=ORANGE)
    if close:
        b.space_arrow(ax,[0,0,0],[0,0,-.52],color=BLUE,ls=DASH,lw=1.4)
        b.space_label(ax,[0,0,-.65],"$\\mathbf n_0=-\\mathbf k$",color=BLUE)
        label(ax,(.80,-.31),"$S_0$",color=GRAY)
    else:
        label(ax,(.64,.73),"$S$",color=BLUE)


def cap_closure():
    fig,axs=figures(86)
    for ax in axs: plane(ax,(-1.38,1.38),(-.89,1.62),ticks=False)
    cap(axs[0]);cap(axs[1],close=True)
    footer(axs[0],r"$\Phi_S=\pi$",y=-.14)
    footer(axs[1],r"$\Phi_{S_0}=-\pi,\quad\Phi_S+\Phi_{S_0}=0$",y=-.14)
    b.save(fig,"fig-16-cap-closure","上半球通量计算：补入向下定向的底面，闭面总通量为零。")


def continuity():
    fig,axs=figures(64)
    ax=axs[0]
    plane(ax,(-1.1,2.2),(-.2,1.45),ticks=False)
    ax.add_patch(Rectangle((0,0),1.1,1.0,facecolor=PALE,edgecolor=BLUE,lw=1.4))
    arrow(ax,(-.82,.55),(.13,.55),color=BLUE,lw=2.5,size=11)
    arrow(ax,(.99,.55),(1.80,.55),color=ORANGE,lw=1.4,size=8)
    label(ax,(-.40,.83),"$8\\ \\mathrm{kg/s}$",color=BLUE)
    label(ax,(1.63,.83),"$3\\ \\mathrm{kg/s}$",color=ORANGE)
    label(ax,(.55,.30),"$\\Omega$",color=GRAY)
    footer(ax,r"$\Phi_{\mathrm{out}}=3-8=-5\ \mathrm{kg/s}$",y=-.18)
    ax=axs[1]
    plane(ax,(-.15,1.6),(-.1,1.3),ticks=False)
    ax.add_patch(Rectangle((0,.05),1.05,.83,facecolor=PALE,edgecolor=BLUE,lw=1.4))
    label(ax,(.53,.46),"$M(t)$")
    arrow(ax,(1.31,.2),(1.31,.88),color=BLUE,lw=1.8)
    label(ax,(.55,1.09),r"$\frac{dM}{dt}=5\ \mathrm{kg/s}$",color=BLUE)
    footer(ax,r"$dM/dt=-\Phi_{\mathrm{out}}$",y=-.18)
    b.save(fig,"fig-17-continuity","无内部源的固定控制体：流入 8 kg/s、流出 3 kg/s，存量增加 5 kg/s。")


def gradient_example():
    fig,axs=figures(86)
    ax=axs[0]
    plane(ax,(-.20,1.50),(-.2,2.38))
    ax.set_xticks([0,1]);ax.set_yticks([0,1,2])
    xx,yy=np.meshgrid(np.linspace(-.2,1.5,150),np.linspace(-.2,2.3,180))
    cs=ax.contour(xx,yy,xx*xx+yy*yy,levels=[1,2,4,5],colors="0.73",linewidths=.7)
    ax.clabel(cs,fmt="%g",fontsize=7)
    ax.plot([0,1],[0,2],color=BLUE,lw=1.6)
    ax.plot([0,1,1],[0,0,2],color=ORANGE,lw=1.6,ls=DASH)
    arrow(ax,(.37,.74),(.47,.94),color=BLUE,size=7)
    arrow(ax,(1,.8),(1,1.08),color=ORANGE,size=7)
    ax.plot([0,1],[0,2],"o",ms=4,color="black")
    label(ax,(.02,.22),"$A$",ha="left")
    label(ax,(1.15,2.17),"$B$",ha="left")
    label(ax,(.65,-.10),"$C_2$",color=ORANGE)
    label(ax,(.16,1.05),"$C_1$",color=BLUE)
    footer(ax,r"$f=x^2+y^2,\quad f(B)-f(A)=5$",y=-.34)
    ax=axs[1]
    t=np.linspace(0,1,200)
    ax.plot(t,5*t*t,color=BLUE,lw=1.6)
    ax.plot([0,1],[0,5],"o",color="black",ms=4)
    arrow(ax,(.83,.15),(.83,4.85),color=ORANGE,lw=1.3)
    label(ax,(.69,2.4),"$\\Delta f=5$",color=ORANGE)
    ax.set(xlim=(-.03,1.07),ylim=(-.1,5.6),xlabel=r"$t$ (dimensionless)",ylabel=r"$f(\mathbf{r}(t))$ (dimensionless)")
    ax.set_xticks([0,.5,1]);ax.set_yticks([0,2.5,5]);ax.minorticks_off()
    footer(ax,r"$\int_0^1\frac{d}{dt}(5t^2)\,dt=5$",y=-.34)
    b.save(fig,"fig-18-gradient-example","势 f=x^2+y^2 下的直线与折线路径，积分均为端点势差 5。")


def field_comparison():
    fig,axs=figures(84)
    xx,yy=np.meshgrid(np.linspace(-1,1,7),np.linspace(-1,1,7))
    for ax in axs:
        plane(ax,(-1.34,1.34),(-1.34,1.34))
        ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1])
        b.circle_path(ax,.85,color=GRAY,lw=.8,ls=DASH)
    axs[0].quiver(xx,yy,xx,yy,color=BLUE,angles="xy",scale_units="xy",scale=4.5,width=.006,headwidth=3.5)
    axs[1].quiver(xx,yy,-yy,xx,color=ORANGE,angles="xy",scale_units="xy",scale=4.5,width=.006,headwidth=3.5)
    label(axs[0],(0,1.25),"$\\mathbf F=(x,y,0)$",color=BLUE)
    label(axs[1],(0,1.25),"$\\mathbf F=(-y,x,0)$",color=ORANGE)
    footer(axs[0],r"$\nabla\cdot\mathbf F=2,\quad\nabla\times\mathbf F=0$",y=-.34)
    footer(axs[1],r"$\nabla\cdot\mathbf F=0,\quad\nabla\times\mathbf F=2\mathbf k$",y=-.34)
    b.save(fig,"fig-19-field-comparison","二维径向场与旋转场，区分散度与旋度；箭长按统一比例缩放。")


def ellipse_arc_chord():
    A=np.array([-.5,-.5]); B=np.array([.5,.5])
    def ellipse(t):
        return np.column_stack([np.cos(t),np.sin(t)/np.sqrt(3)])
    fig,axs=figures(82)
    ax=axs[0]
    plane(ax,(-1.34,1.34),(-.84,.84))
    ax.set_xticks([-1,-.5,0,.5,1]);ax.set_yticks([-.5,0,.5])
    t=np.linspace(4*np.pi/3,7*np.pi/3,400); arc=ellipse(t)
    s=np.linspace(0,1,40); chord=B+(A-B)*s[:,None]
    ax.add_patch(Polygon(np.vstack([arc,chord]),facecolor=PALE,edgecolor="none",zorder=1))
    ax.plot([-.84,.84],[-.84,.84],color="0.75",lw=.7,ls=(0,(1,2.4)),zorder=2)
    ax.plot(*ellipse(np.linspace(np.pi/3,4*np.pi/3,300)).T,color=GRAY,lw=.9,ls=DASH,zorder=3)
    ax.plot(*arc.T,color=BLUE,lw=1.7,zorder=4)
    ax.plot([B[0],A[0]],[B[1],A[1]],color=ORANGE,lw=1.4,ls=DASH,zorder=5)
    for t0 in [1.5*np.pi,2.15*np.pi]:
        p=ellipse(np.array([t0-.13,t0+.13]))
        arrow(ax,p[0],p[1],color=BLUE,lw=1.4,size=8,z=9)
    arrow(ax,B+.42*(A-B),B+.58*(A-B),color=ORANGE,lw=1.3,size=8,z=9)
    ax.plot(*np.column_stack([A,B]).T,"o",ms=4,color="black",zorder=6)
    label(ax,(A[0]-.09,A[1]-.13),"$A$",ha="right")
    label(ax,(B[0]+.09,B[1]+.13),"$B$",ha="left")
    label(ax,(.42,-.36),"$D$",color=GRAY)
    label(ax,(.30,-.66),"$L$",color=BLUE)
    label(ax,(.16,.40),"$C$",color=ORANGE)
    label(ax,(-.84,-.72),"$y=x$",color=GRAY,ha="right")
    footer(ax,r"$\partial D=L+C,\quad \oint_{L+C}=\iint_D 6\,dA=\pi\sqrt{3}$",y=-.34)
    ax=axs[1]
    x=np.linspace(-.5,.5,401)
    g=np.exp(x**2)*np.sin(x)+6*x-3*x**2-x*np.cos(x)**4
    even=-3*x**2
    ax.fill_between(x,even,0,color=PALE,zorder=1)
    ax.axhline(0,color="0.75",lw=.65,zorder=2)
    ax.plot(x,g-even,color=GRAY,lw=1.1,ls=DASH,zorder=3)
    ax.plot(x,even,color=ORANGE,lw=1.4,ls=DASH,zorder=3)
    ax.plot(x,g,color=BLUE,lw=1.5,zorder=4)
    ax.plot([-.5,.5],[g[0],g[-1]],"o",ms=4,color="black",zorder=5)
    ax.set(xlim=(-.56,.56),ylim=(-4.9,3.6),xlabel=r"$x$ (dimensionless)",
           ylabel=r"$g$ (dimensionless)")
    ax.set_xticks([-.5,0,.5]);ax.set_yticks([-4,-2,0,2]);ax.minorticks_off()
    label(ax,(-.44,-4.45),"$A$",ha="left")
    label(ax,(.46,2.82),"$B$",ha="right")
    label(ax,(.36,1.10),"$g$",color=BLUE)
    label(ax,(-.44,-2.35),"$g_{\\mathrm{odd}}$",color=GRAY)
    label(ax,(.28,-1.55),"$-3x^2$",color=ORANGE)
    ax.plot([.32,.44],[-1.47,-.68],color=ORANGE,lw=.65)
    footer(ax,r"$\int_{-1/2}^{1/2}g\,dx=\int_{-1/2}^{1/2}(-3x^2)\,dx=-\frac{1}{4}$",y=-.34)
    b.save(fig,"fig-20-ellipse-arc-chord","椭圆长弧与补弦：奇部抵消，偶部给出弦上积分 -1/4。")


def verify():
    x=np.linspace(0,1,10001)
    assert np.isclose(np.trapezoid((1-x)**2/2,x),1/6,atol=1e-8)
    assert np.isclose(np.trapezoid(2*np.pi*x**3,x),np.pi/2,atol=1e-7)
    t=np.linspace(0,2*np.pi,10001)
    assert np.isclose(np.trapezoid(np.cos(t)**2+np.sin(t)**2,t),2*np.pi)
    phi=np.linspace(0,np.pi/2,10001)
    assert np.isclose(2*np.pi*np.trapezoid(np.cos(phi)*np.sin(phi),phi),np.pi,atol=1e-7)
    ru=np.array([1,0,1.]);rv=np.array([0,1,.5])
    assert np.allclose(np.cross(ru,rv),[-1,-.5,1])
    assert np.isclose(np.linalg.norm(np.cross(ru,rv)),1.5)
    assert np.isclose(np.trapezoid(10*x,x),5)
    assert 8-3 == 5
    # Worked example: ellipse arc closed by the chord y=x.
    t=np.linspace(4*np.pi/3,7*np.pi/3,200001)
    px=np.cos(t); py=np.sin(t)/np.sqrt(3)
    P=np.exp(px**2)*np.sin(px)-2*px*py
    Q=6*px-px**2-py*np.cos(py)**4
    arc=np.trapezoid(P*(-np.sin(t))+Q*np.cos(t)/np.sqrt(3),t)
    s=np.linspace(.5,-.5,200001)
    chord=np.trapezoid(np.exp(s**2)*np.sin(s)-3*s*s+6*s-s*np.cos(s)**4,s)
    poly=np.vstack([np.column_stack([px,py]),[-.5,-.5]])
    area=.5*abs(np.sum(poly[:-1,0]*poly[1:,1]-poly[1:,0]*poly[:-1,1]))
    assert np.isclose(area,np.pi/(2*np.sqrt(3)),atol=1e-6)
    assert np.isclose(chord,.25,atol=1e-8)
    assert np.isclose(6*area,np.pi*np.sqrt(3),atol=1e-6)
    assert np.isclose(arc,6*area-chord,atol=1e-7)
    print("[ok] tetrahedron, radial integral, ellipse, cap flux, surface area, gradient, arc-chord checks")


if __name__=="__main__":
    verify()
    for maker in [riemann_sum,radial_example,volume_slices,tangent_component,
                  surface_element,green_orientation,gauss_sphere,cap_closure,
                  continuity,gradient_example,field_comparison,ellipse_arc_chord]:
        maker()
    b.previews("preview-extra")
    (b.HERE/"figure_manifest_extra.json").write_text(json.dumps(b.EXPORTS,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"[ok] {len(b.EXPORTS)} additional figures, PDF + PNG, 178 mm wide at 600 dpi")
