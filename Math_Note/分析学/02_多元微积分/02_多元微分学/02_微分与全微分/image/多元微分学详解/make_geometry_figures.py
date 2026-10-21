"""Coordinate geometry illustrations used by make_figures.py.

Three-dimensional axes represent actual graphs, tangent planes or volumes.
Orthographic projection, unshaded wireframes and explicit 2-D views avoid
decorative perspective effects. All quantities are dimensionless.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def pair(p, height=101, both3d=False):
    fig = plt.figure(figsize=p.ss.figsize("double", height_mm=height))
    a = fig.add_subplot(121, projection="3d")
    b = fig.add_subplot(122, projection="3d" if both3d else None)
    fig.subplots_adjust(left=.055, right=.94, bottom=.22, top=.90, wspace=.48)
    fig.add_artist(Rectangle((0, 0), 1, 1, transform=fig.transFigure,
                            facecolor="none", edgecolor="none", lw=0))
    for i, ax in enumerate((a, b)):
        if ax.name == "3d":
            ax.set_proj_type("ortho")
            ax.view_init(elev=25, azim=-58)
            ax.grid(False)
            for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
                axis.pane.fill = False
                axis.pane.set_edgecolor("white")
                axis.set_major_locator(p.MaxNLocator(3))
            ax.set_xlabel(r"$x$ (dim.)", labelpad=1)
            ax.set_ylabel(r"$y$ (dim.)", labelpad=1)
            ax.set_zlabel(r"$z$ (dim.)", labelpad=1)
            ax.tick_params(labelsize=7, pad=0)
        else:
            ax.minorticks_off()
        fig.text(ax.get_position(original=True).x0, .93, "AB"[i],
                 weight="bold", fontsize=10)
    return fig, a, b


def foot(ax, s):
    bounds = ax.get_position(original=True)
    ax.figure.text(bounds.x0+bounds.width/2, .105, s,
                   ha="center", va="top", fontsize=8)


def vector(ax, point, value, color, ls="-", label=None):
    point, value = np.asarray(point), np.asarray(value)
    ax.quiver(*point, *value, color=color, linewidth=1.6,
              arrow_length_ratio=.16, linestyle=ls, normalize=False)
    if label:
        ax.text(*(point+value), label, color=color, fontsize=8)


def graph(ax):
    x, y = np.meshgrid(np.linspace(.45, 1.55, 15), np.linspace(.05, .95, 15))
    ax.plot_wireframe(x, y, x*x+2*y*y, rstride=2, cstride=2,
                      color="0.78", linewidth=.55)
    ax.set(xlim=(.4, 1.65), ylim=(0, 1), zlim=(0, 4.4))
    ax.set_box_aspect((1.25, 1, 1.55))
    ax.plot([1, 1], [.5, .5], [0, 1.5], color="0.45", ls=":", lw=1)
    ax.scatter([1], [.5], [1.5], color="black", s=16, depthshade=False)


def partial(p):
    fig, a, b = pair(p)
    graph(a)
    s = np.linspace(-.4, .4, 150)
    a.plot(1+s, np.full_like(s, .5), (1+s)**2+.5, color=p.BLUE, lw=2)
    a.plot(np.ones_like(s), .5+s, 1+2*(.5+s)**2, color=p.RED, lw=2, ls="--")
    a.plot(1+s, np.full_like(s, .5), 1.5+2*s, color=p.BLUE, lw=1, ls=":")
    a.plot(np.ones_like(s), .5+s, 1.5+2*s, color=p.RED, lw=1, ls="-.")
    # Thin vertical-plane boundaries make the fixed coordinate explicit.
    for coords, color, ls in [(([.55,1.5,1.5,.55,.55],[.5]*5,[0,0,4,4,0]),p.BLUE,"-"),
                              (([1]*5,[.1,.9,.9,.1,.1],[0,0,4,4,0]),p.RED,"--")]:
        a.plot(*coords, color=color, ls=ls, lw=.7, alpha=.7)
    foot(a, r"Graph cuts: $y=1/2$ and $x=1$")
    b.plot(s, (1+s)**2+.5, color=p.BLUE, label=r"$x$-slice, $y=1/2$")
    b.plot(s, 1+2*(.5+s)**2, color=p.RED, ls="--", label=r"$y$-slice, $x=1$")
    b.plot(s, 1.5+2*s, color="black", ls=":", label="Common tangent")
    b.plot(0, 1.5, "ko", ms=4)
    b.set(xlabel=r"Input displacement $s$ (dim.)", ylabel=r"Height $z$ (dim.)")
    b.legend(fontsize=7, loc="upper left")
    foot(b, r"True-section slopes: $f_x=f_y=2$")
    p.save(fig, "fig-01-partial-derivatives")


def direction(p):
    fig, a, b = pair(p)
    graph(a)
    u = np.array([.6, .8])
    s = np.linspace(-.45, .45, 150)
    x, y = 1+s*u[0], .5+s*u[1]
    a.plot(x, y, x*x+2*y*y, color=p.BLUE, lw=2)
    a.plot(x, y, 1.5+2.8*s, color=p.RED, lw=1.5, ls="--")
    a.plot(x, y, np.zeros_like(s), color="0.4", ls=":", lw=1.2)
    vector(a, [1,.5,0], [.3,.4,0], "black", label=r"$\mathbf{u}$")
    vector(a, [1,.5,1.5], [.15,.2,.7], p.RED, label=r"$(\mathbf{u},D_{\mathbf{u}}f)$")
    foot(a, r"Vertical section above $\mathbf{a}+s\mathbf{u}$")
    b.plot(s, x*x+2*y*y, color=p.BLUE, label=r"Section $f(\mathbf{a}+s\mathbf{u})$")
    b.plot(s, 1.5+2.8*s, color=p.RED, ls="--", label="Tangent")
    b.plot(0,1.5,"ko",ms=4)
    b.set(xlabel=r"Input distance $s$ (dim.)", ylabel=r"Height $z$ (dim.)")
    b.legend(fontsize=7, loc="upper left")
    foot(b, r"$\mathbf{u}=(3/5,4/5)^T,\quad D_{\mathbf{u}}f=14/5$")
    p.save(fig, "fig-02-direction-derivative")


def gradient(p):
    fig, a, b = pair(p, both3d=True)
    # First panel is replaced by an input-plane view, not a 3-D embedding.
    position = a.get_position()
    a.remove()
    a = fig.add_axes(position)
    a.set_position([.10,.25,.34,.60])
    p.contours(a)
    a.set_xlabel(r"$x$ (dim.)")
    a.set_ylabel(r"$y$ (dim.)")
    p.arrow(a,(1,.5),(1.5,1),p.BLUE)
    p.arrow(a,(1,.5),(.65,.85),p.RED,"--")
    a.text(1.22,1.12,r"$\nabla f$ (scaled)",color=p.BLUE)
    a.text(.12,.99,r"$\mathbf{u}_0$",color=p.RED)
    foot(a,"Input plane: gradient and level tangent")
    x,y=np.meshgrid(np.linspace(.7,1.35,9),np.linspace(.2,.85,9))
    z=1.5+2*(x-1)+2*(y-.5)
    b.plot_wireframe(x,y,z,rstride=2,cstride=2,color="0.68",linewidth=.8)
    P=np.array([1,.5,1.5])
    b.scatter(*P,color="black",s=16,depthshade=False)
    vector(b,P,[.25,0,.5],p.BLUE,label=r"$\mathbf{r}_x$")
    vector(b,P,[0,.25,.5],p.RED,"--",label=r"$\mathbf{r}_y$")
    n=np.array([-2,-2,1])/3
    vector(b,P,.7*n,"black",label=r"$\mathbf{n}$")
    b.set(xlim=(.4,1.65),ylim=(-.05,1.1),zlim=(0,3.5))
    b.set_box_aspect((1.25,1.15,1.4))
    foot(b,r"Graph space: $\mathbf{n}=\mathbf{r}_x\times\mathbf{r}_y$")
    p.save(fig,"fig-03-gradient-tangent-plane")


def level3d(p):
    fig,a,b=pair(p,both3d=True)
    c=1.75
    th,ph=np.meshgrid(np.linspace(0,2*np.pi,25),np.linspace(.06,np.pi-.06,17))
    x=np.sqrt(c)*np.sin(ph)*np.cos(th)
    y=np.sqrt(c/2)*np.sin(ph)*np.sin(th)
    z=np.sqrt(c)*np.cos(ph)
    a.plot_wireframe(x,y,z,rstride=2,cstride=2,color="0.7",linewidth=.6)
    P=np.array([1,.5,.5]); g=np.array([2,2,1])
    a.scatter(*P,color="black",s=16,depthshade=False)
    vector(a,P,.25*g,p.BLUE,label=r"$\nabla g$")
    # Orthogonal tangent basis, constructed from the normal via dot/cross products.
    u=np.array([1,-1,0])/np.sqrt(2)
    v=np.cross(g/np.linalg.norm(g),u)
    grid=np.linspace(-.5,.5,5)
    s,t=np.meshgrid(grid,grid)
    plane=P[:,None,None]+u[:,None,None]*s+v[:,None,None]*t
    a.plot_wireframe(*plane,rstride=1,cstride=1,color=p.RED,linewidth=.6)
    for ax in (a,b):
        ax.set(xlim=(-1.5,1.8),ylim=(-1.2,1.3),zlim=(-1.5,1.5))
        ax.set_box_aspect((3.3,2.5,3))
        ax.view_init(elev=24, azim=-25)
    foot(a,r"Input space: $g=x^2+2y^2+z^2=7/4$")
    # A level-surface tangent direction versus a direction with nonzero derivative.
    b.scatter(*P,color="black",s=16,depthshade=False)
    b.plot_wireframe(*plane,rstride=1,cstride=1,color="0.7",linewidth=.7)
    vector(b,P,.6*u,p.RED,"--",label=r"$\mathbf{u}_0$")
    vector(b,P,.25*g,p.BLUE,label=r"$\nabla g$")
    foot(b,r"$\nabla g=(2,2,1)^T,\quad D_{\mathbf{u}_0}g=0$")
    p.save(fig,"fig-04-gradient-level-surface")


def differential(p):
    fig,a,b=pair(p)
    P=np.array([1,.5,1.5]); X=np.array([1.4,.5,2.3]); Q=np.array([1.4,.8,2.9])
    x,y=np.meshgrid(np.linspace(.95,1.45,6),np.linspace(.45,.85,6))
    a.plot_wireframe(x,y,1.5+2*(x-1)+2*(y-.5),color="0.75",linewidth=.65)
    a.plot(*np.vstack((P,X)).T,color=p.BLUE,lw=2)
    a.plot(*np.vstack((X,Q)).T,color=p.RED,lw=2,ls="--")
    a.plot(*np.vstack((P,Q)).T,color="black",ls=":",lw=1.4)
    actual=np.array([1.4,.8,3.24])
    a.plot(*np.vstack((Q,actual)).T,color="black",lw=1.4)
    for v,label in [(P,"P"),(X,"X"),(Q,"Q (linear)"),(actual,"Q (actual)")]:
        a.scatter(*v,color="black",s=12,depthshade=False)
        a.text(*v,label,fontsize=7)
    a.set(xlim=(.9,1.65),ylim=(.4,.95),zlim=(1.3,3.5))
    a.set_box_aspect((.75,.55,1.2))
    foot(a,r"Tangent-plane steps: $df=0.8+0.6$")
    s=np.linspace(0,.7,201)
    xp=1+np.minimum(s,.4); yp=.5+np.maximum(s-.4,0)
    b.plot(s,xp*xp+2*yp*yp-1.5,color="black",ls=":",label=r"Actual $\Delta f$")
    b.plot([0,.4],[0,.8],color=p.BLUE,lw=2,label=r"$x$ contribution")
    b.plot([.4,.7],[.8,1.4],color=p.RED,ls="--",lw=2,label=r"$y$ contribution")
    b.plot([.7,.7],[1.4,1.74],color="0.5",lw=1.3)
    b.set(xlim=(0,.78),ylim=(0,2.15),xlabel="Coordinate-path length (dim.)",
          ylabel="Height increment (dim.)")
    b.legend(loc="upper left",fontsize=7)
    foot(b,r"$\Delta f-df=(0.4)^2+2(0.3)^2=0.34$")
    p.save(fig,"fig-05-total-differential")


def flux(p):
    fig,a,b=pair(p)
    # Rectangular cell; highlighted faces are perpendicular to x.
    for x in [-.25,.25]:
        a.plot([x]*5,[-.5,.5,.5,-.5,-.5],[-.5,-.5,.5,.5,-.5],color="0.5",lw=1)
    for y in [-.5,.5]:
        for z in [-.5,.5]: a.plot([-.25,.25],[y,y],[z,z],color="0.7",lw=.8)
    for x,sign in [(-.25,-1),(.25,1)]:
        vector(a,[x,0,0],[.4*sign,0,0],p.RED,"--",label=rf"${'+' if sign>0 else '-'}\mathbf{{e}}_x$")
        vector(a,[x,0,.2],[.22*(1+2*x),0,0],p.BLUE)
    a.set(xlim=(-.95,1),ylim=(-.65,.65),zlim=(-.6,.75))
    a.set_box_aspect((1.95,1.3,1.35))
    foot(a,r"Flux: $\mathbf{F}\cdot\mathbf{n}\,dS$; opposite normals")
    b.add_patch(Rectangle((-.25,-.5),.5,1,fill=False,ec="0.5",lw=1))
    p.arrow(b,(-.25,0),(-.05,0),p.BLUE)
    p.arrow(b,(.25,0),(.85,0),p.BLUE)
    p.arrow(b,(-.25,-.3),(-.7,-.3),p.RED,"--")
    p.arrow(b,(.25,-.3),(.7,-.3),p.RED,"--")
    b.text(-.9,.3,r"$-P_-\Delta y\Delta z$",fontsize=8)
    b.text(.12,.3,r"$+P_+\Delta y\Delta z$",fontsize=8)
    b.set(xlim=(-1,1),ylim=(-.8,.8),aspect="equal",
          xlabel=r"$x$ (dim.)",ylabel=r"$y$ (dim.)")
    b.set_xticks([-.25,.25]); b.set_yticks([-.5,.5])
    foot(b,r"$P=1+2x:\quad P_+-P_-=2\Delta x$")
    p.save(fig,"fig-07-flux-geometry")


def circulation(p):
    fig,a,b=pair(p,both3d=True)
    position=a.get_position(); a.remove(); a=fig.add_axes(position)
    a.add_patch(Rectangle((0,0),1,1,fill=False,ec="0.65",lw=1))
    for start,end in [((.2,0),(.75,0)),((1,.2),(1,.75)),((.75,1),(.2,1)),((0,.75),(0,.2))]:
        p.arrow(a,start,end,p.BLUE)
    a.text(.5,-.17,r"$+P_{\rm bottom}\Delta x$",ha="center",fontsize=8)
    a.text(.5,1.1,r"$-P_{\rm top}\Delta x$",ha="center",fontsize=8)
    a.text(1.09,.5,r"$+Q_{\rm right}\Delta y$",rotation=90,va="center",fontsize=8)
    a.text(-.13,.5,r"$-Q_{\rm left}\Delta y$",rotation=90,va="center",ha="right",fontsize=8)
    a.set(xlim=(-.4,1.45),ylim=(-.4,1.5),aspect="equal",
          xlabel=r"$x$ (dim.)",ylabel=r"$y$ (dim.)")
    a.set_xticks([0,1]); a.set_yticks([0,1])
    foot(a,r"CCW circulation: $(Q_x-P_y)\Delta x\Delta y$")
    u=np.array([1,0,0]); v=np.array([0,1,1])/np.sqrt(2); n=np.cross(u,v)
    corners=np.array([-.6*u-.6*v,.6*u-.6*v,.6*u+.6*v,-.6*u+.6*v])
    b.add_collection3d(Poly3DCollection([corners],facecolor="0.93",edgecolor="0.7",alpha=.6))
    for i in range(4):
        start=corners[i]; edge=corners[(i+1)%4]-start
        vector(b,start+.2*edge,.5*edge,p.BLUE)
    vector(b,[0,0,0],.9*n,p.RED,label=r"$\mathbf{n}=\mathbf{e}_u\times\mathbf{e}_v$")
    vector(b,corners[0],.55*u,"black",label=r"$\mathbf{e}_u$")
    vector(b,corners[0],.55*v,"black","--",label=r"$\mathbf{e}_v$")
    b.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1))
    b.set_box_aspect((1,1,1))
    foot(b,r"Oriented area: $\mathbf{n}\,dS$ (right-hand rule)")
    p.save(fig,"fig-09-circulation-geometry")
