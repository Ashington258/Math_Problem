"""Scalar and oriented elements; analytic, dimensionless examples.

Run: python make_figures.py. Ten 178-mm PDF/SVG/600-dpi PNG figure sets.
Filename numbers are stable asset IDs, independent of the order in which
shared figures appear in a note. Inherited scalar figures keep their filenames. No randomness or empirical data.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.ticker import MaxNLocator
from PIL import Image,ImageDraw,ImageOps
import sci_style as ss

HERE=Path(__file__).resolve().parent
ss.DEFAULT_FONTS=["DejaVu Sans"]
ss.apply("double",font_size=8,line_width=1.4,mathtext=False)
plt.rcParams.update({"savefig.pad_inches":0,"svg.fonttype":"path"})
BLUE,RED=ss.OKABE_ITO["blue"],ss.OKABE_ITO["vermillion"]
EXPORTS=[]


def figure(kinds=("2d","2d"),height=100):
    rows=2 if len(kinds)==4 else 1
    fig=plt.figure(figsize=ss.figsize("double",height_mm=height))
    fig.subplots_adjust(left=.10,right=.94,bottom=.22 if rows==1 else .12,
                        top=.90,wspace=.46,hspace=.65)
    fig.add_artist(Rectangle((0,0),1,1,transform=fig.transFigure,fc="none",ec="none",lw=0))
    axs=[]
    for i,kind in enumerate(kinds):
        ax=fig.add_subplot(rows,2,i+1,projection="3d" if kind=="3d" else None)
        if kind=="3d":
            ax.set_proj_type("ortho"); ax.view_init(elev=25,azim=-55); ax.grid(False)
            for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
                axis.pane.fill=False; axis.pane.set_edgecolor("white")
                axis.set_major_locator(MaxNLocator(3))
            ax.set_xlabel(r"$x$ (dim.)",labelpad=0)
            ax.set_ylabel(r"$y$ (dim.)",labelpad=0)
            ax.set_zlabel(r"$z$ (dim.)",labelpad=0)
            ax.tick_params(labelsize=7,pad=0)
        else:
            ax.minorticks_off()
            ax.set_xlabel(r"$x$ (dim.)"); ax.set_ylabel(r"$y$ (dim.)")
            ax.xaxis.set_major_locator(MaxNLocator(4)); ax.yaxis.set_major_locator(MaxNLocator(4))
        pos=ax.get_position(original=True)
        fig.text(pos.x0,pos.y1+.025,"ABCD"[i],fontsize=10,weight="bold")
        axs.append(ax)
    return fig,axs


def footer(ax,s,rows=1):
    pos=ax.get_position(original=True)
    ax.figure.text(pos.x0+pos.width/2,.095 if rows==1 else pos.y0-.075,
                   s,ha="center",va="top",fontsize=7.5)


def arrow(ax,start,end,color=BLUE,ls="-",lw=1.5):
    ax.annotate("",xy=end,xytext=start,arrowprops=dict(arrowstyle="-|>",color=color,
                linestyle=ls,lw=lw,mutation_scale=10,shrinkA=0,shrinkB=0),zorder=10)


def vector(ax,start,value,color=BLUE,label=None,ls="-"):
    start,value=np.asarray(start),np.asarray(value)
    ax.quiver(*start,*value,color=color,linewidth=1.5,arrow_length_ratio=.16,linestyle=ls)
    if label: ax.text(*(start+value),label,color=color,fontsize=8)


def save(fig,name):
    ss.save(fig,HERE/(name+".pdf"),also_png=True,dpi=600)
    ss.save(fig,HERE/(name+".svg"))
    EXPORTS.append({"name":name,"size_mm":list(ss.output_size_mm(HERE/(name+".pdf"))),"dpi":600})
    plt.close(fig)


def line_elements():
    # Keep Chinese annotations local to this figure; the other assets retain
    # their established typography. All examples below are dimensionless.
    with plt.rc_context({"font.family":["Microsoft YaHei","SimHei","DejaVu Sans"],
                         "axes.unicode_minus":False}):
        _line_elements()


def _line_elements():
    # Abstract geometry only: no chosen field, path equation, or integral.
    fig=plt.figure(figsize=ss.figsize("double",height_mm=90))
    fig.add_artist(Rectangle((0,0),1,1,transform=fig.transFigure,fc="none",ec="none",lw=0))
    axs=fig.subplots(1,2)
    fig.subplots_adjust(left=.05,right=.96,bottom=.22,top=.82,wspace=.27)
    titles=["弧长加上切向", "坐标投影与分量合成"]
    notes=[r"$d\mathbf{r}=\mathbf{T}\,ds,\quad\|\mathbf{T}\|=1$",
           r"$d\mathbf{r}=dx\,\mathbf{e}_x+dy\,\mathbf{e}_y$"]
    for i,(ax,title,note) in enumerate(zip(axs,titles,notes)):
        ax.set_aspect("equal"); ax.set_axis_off()
        pos=ax.get_position(original=True)
        fig.text(pos.x0,pos.y1+.055,"AB"[i]+"  "+title,fontsize=9,weight="bold")
        fig.text(pos.x0+pos.width/2,.11,note,ha="center",fontsize=9)
    a,b=axs
    T=np.array([.8,.6]); N=np.array([-.6,.8]); p=np.array([.35,.30])
    u=np.linspace(-.35,1.6,120)
    curve=p+u[:,None]*T+.24*u[:,None]**2*N
    a.plot(*curve.T,color="0.7",lw=1.4)
    a.plot(*p,"ko",ms=3)
    a.text(*(p+np.array([-.13,-.06])),r"$P$",fontsize=8)
    a.text(*curve[-1],r"$C$",fontsize=9,color="0.45")
    # Collinear arrows: the black arrow specifies direction; blue is the element.
    end=p+1.26*T
    arrow(a,p,end,BLUE,lw=2.5)
    arrow(a,p,p+.57*T,"black",ls="--",lw=1.2)
    a.text(*(p+.56*T+.17*N),r"$\mathbf{T}$",fontsize=10)
    a.text(*(p+1.02*T+.12*N),r"$d\mathbf{r}$",fontsize=11,color=BLUE)
    # A dimension bracket labels the magnitude of the oriented line element.
    shift=-.26*N
    for q in (p,end):
        a.plot(*np.array([q+shift*.65,q+shift*1.15]).T,color="0.65",lw=.7)
    a.annotate("",xy=end+shift,xytext=p+shift,
               arrowprops=dict(arrowstyle="|-|",color=BLUE,lw=.9,shrinkA=0,shrinkB=0))
    a.text(*(p+.59*T+shift-.13*N),r"$ds$",fontsize=10,color=BLUE)
    a.set(xlim=(-.05,1.95),ylim=(-.15,1.65))
    # The same displacement, projected onto orthogonal coordinate directions.
    origin=np.array([.10,.10]); q=origin+np.array([1.30,.94])
    foot=np.array([q[0],origin[1]])
    arrow(b,origin,origin+np.array([1.72,0]),"0.55",lw=.9)
    arrow(b,origin,origin+np.array([0,1.48]),"0.55",lw=.9)
    b.text(1.87,.04,r"$x$",fontsize=9,color="0.45")
    b.text(.03,1.65,r"$y$",fontsize=9,color="0.45")
    b.plot([origin[0],q[0]],[q[1],q[1]],color="0.55",ls=":",lw=1)
    b.plot([q[0],q[0]],[origin[1],q[1]],color="0.55",ls=":",lw=1)
    arrow(b,origin,foot,RED,lw=2)
    arrow(b,foot,q,RED,ls="--",lw=2)
    arrow(b,origin,q,BLUE,lw=2.5)
    b.plot(*origin,"ko",ms=3)
    b.text(-.03,-.05,r"$P$",fontsize=8)
    b.text(.67,-.09,r"$dx$",fontsize=10,color=RED)
    b.text(1.49,.52,r"$dy$",fontsize=10,color=RED)
    b.text(.60,.67,r"$d\mathbf{r}$",fontsize=11,color=BLUE)
    b.text(-.07,1.03,r"$dy$",fontsize=9,color="0.45",ha="right")
    h=.09
    b.plot([foot[0]-h,foot[0]-h,foot[0]],
           [foot[1],foot[1]+h,foot[1]+h],color="0.4",lw=.8)
    b.set(xlim=(-.28,2.02),ylim=(-.20,1.70))
    save(fig,"fig-03-line-elements")



def patch(ax):
    ax.view_init(elev=25,azim=-145)
    a=np.array([1.,0,1]); b=np.array([0.,1,2])
    points=np.array([np.zeros(3),a,a+b,b])
    ax.add_collection3d(Poly3DCollection([points],fc="0.94",ec="0.55",alpha=.5))
    ax.set(xlim=(-.4,1.4),ylim=(-.7,1.3),zlim=(-.1,3.5))
    ax.set_box_aspect((1.8,2,3.6))
    return a,b,points


def area_projections():
    fig,axs=figure(("3d","2d","2d","2d"),height=169)
    a,b,quad=patch(axs[0])
    vector(axs[0],[0,0,0],a,BLUE,label=r"$r_u$")
    vector(axs[0],[0,0,0],b,RED,label=r"$r_v$",ls="--")
    vector(axs[0],[.5,.5,1.5],.25*np.cross(a,b),"black",label=r"$d\mathbf{S}$")
    footer(axs[0],r"$r=(u,v,u+2v)$; $r_u\times r_v=(-1,-2,1)$",2)
    for ax,coords,names,value in zip(axs[1:],[(1,2),(2,0),(0,1)],[("y","z"),("z","x"),("x","y")],[-1,-2,1]):
        projected=quad[:,coords]
        ax.add_patch(Polygon(projected,closed=True,fc="0.94",ec="0.6",lw=1))
        arrow(ax,projected[0],projected[1],BLUE)
        arrow(ax,projected[1],projected[2],RED,"--")
        arrow(ax,projected[2],projected[3],"0.45",":")
        arrow(ax,projected[3],projected[0],"0.45",":")
        ax.set(xlim=(-.35,max(projected[:,0])+.5),ylim=(-.35,max(projected[:,1])+.5),aspect="equal",
               xlabel=f"${names[0]}$ (dim.)",ylabel=f"${names[1]}$ (dim.)")
        label={-1:r"$dS_x=-du\,dv$",-2:r"$dS_y=-2du\,dv$",1:r"$dS_z=+du\,dv$"}[value]
        footer(ax,label+f"; signed unit area = {value:+d}",2)
    save(fig,"fig-06-area-projections")


def field_actions():
    fig,(a,b)=figure(("3d","3d"),height=112)
    P=np.array([.4,.4,1.2]); F=np.ones(3); N=np.array([-1.,-2,1])
    for ax in (a,b):
        patch(ax)
        ax.scatter(*P,color="black",s=12,depthshade=False)
        vector(ax,P,.4*F,RED,label=r"$F$")
    u=np.linspace(0,1,60)
    a.plot(u,np.full_like(u,.4),u+.8,color="0.35",lw=1.2)
    vector(a,P,.4*np.array([1,0,1]),BLUE,label=r"$d\mathbf{r}$")
    vector(b,P,.25*N,BLUE,label=r"$d\mathbf{S}$")
    normal_component=(F@N)/(N@N)*N
    vector(b,P,.7*normal_component,"black",label=r"$F_n$",ls="--")
    footer(a,r"$ds=\sqrt{2}du$; $F\cdot d\mathbf{r}=2du$")
    footer(b,r"$dS=\sqrt{6}du\,dv$; $F\cdot d\mathbf{S}=-2du\,dv$")
    save(fig,"fig-08-field-actions")


def operator_elements():
    fig,(a,b)=figure(("3d","2d"),height=108)
    for x in [0,1]: a.plot([x]*5,[0,1,1,0,0],[0,0,1,1,0],color="0.65",lw=.8)
    for y in [0,1]:
        for z in [0,1]: a.plot([0,1],[y,y],[z,z],color="0.65",lw=.8)
    for i in range(3):
        point=np.full(3,.5); point[i]=1
        vector(a,point,.3*np.eye(3)[i],BLUE)
        vector(a,point,.18*point,RED)
    a.text(.2,.3,.25,r"$dV=h^3$",fontsize=8)
    a.set(xlim=(-.2,1.5),ylim=(-.2,1.5),zlim=(-.2,1.5)); a.set_box_aspect((1,1,1))
    footer(a,r"$F=(x,y,z)$: $\Phi=3h^3$, $\mathrm{div}\,F=3$")
    b.add_patch(Rectangle((0,0),1,1,fill=False,ec="0.6",lw=1))
    for start,end in [((.15,0),(.75,0)),((1,.15),(1,.75)),((.75,1),(.15,1)),((0,.75),(0,.15))]:
        arrow(b,start,end)
    for point in [np.array([.5,0]),np.array([1,.5]),np.array([.5,1]),np.array([0,.5])]:
        F=np.array([-point[1],point[0]])
        arrow(b,point,point+.25*F,RED)
    b.text(1.08,.42,r"$+h^2$",fontsize=8)
    b.text(.3,1.15,r"$+h^2$",fontsize=8)
    b.text(.3,-.2,"0",fontsize=8); b.text(-.2,.3,"0",fontsize=8)
    b.set(xlim=(-.35,1.5),ylim=(-.35,1.5),aspect="equal")
    footer(b,r"$F=(-y,x)$: $\Gamma=2h^2$, $\mathrm{curl}_zF=2$")
    save(fig,"fig-09-operator-elements")



def planar_normal():
    fig,(a,b)=figure(height=103)
    angle=np.pi/4
    p=np.array([np.cos(angle),np.sin(angle)])
    t=np.array([-np.sin(angle),np.cos(angle)])
    n=p.copy()
    q=np.linspace(0,2*np.pi,300)
    for ax in (a,b):
        ax.plot(np.cos(q),np.sin(q),color="0.65",lw=1)
        ax.set(xlim=(-1.25,1.65),ylim=(-1.2,1.65),aspect="equal")
        ax.plot(*p,"ko",ms=3)
        ax.text(-.65,-.45,r"$D$",color="0.4")
    arrow(a,p,p+.55*t,BLUE)
    arrow(a,p,p+.55*n,RED,"--")
    a.text(.04,1.19,r"$d\mathbf{r}=(dx,dy)$",color=BLUE,fontsize=8)
    a.text(1.06,1.13,r"$d\ell_n$",color=RED,fontsize=8)
    arrow(a,[-1,0],[-.94,-.34],"0.35")
    footer(a,r"Positive tangent; outward normal is on its right")
    F=np.array([1.,.25])
    arrow(b,p,p+.6*F,"black")
    arrow(b,p,p+.6*(F@t)*t,BLUE)
    arrow(b,p,p+.6*(F@n)*n,RED,"--")
    b.text(1.4,.82,r"$F$",fontsize=8)
    b.text(.98,.38,r"$F_\parallel$",color=BLUE,fontsize=8)
    b.text(1.07,1.2,r"$F_n$",color=RED,fontsize=8)
    footer(b,r"$d\ell_n=(dy,-dx)$; $F\cdot d\ell_n=Pdy-Qdx$")
    save(fig,"fig-10-planar-normal")


def coordinate_surfaces():
    fig,(a,b)=figure(("3d","3d"),height=116)
    theta,phi=.6,.9
    # Uniform physical scales; unit radius, independently scaled annotations.
    q=np.linspace(0,2*np.pi,70); z=np.linspace(-.7,.7,9)
    Q,Z=np.meshgrid(q,z)
    a.plot_wireframe(np.cos(Q),np.sin(Q),Z,color="0.78",lw=.45,rstride=2,cstride=6)
    p=np.array([np.cos(theta),np.sin(theta),.25])
    er=np.array([np.cos(theta),np.sin(theta),0])
    et=np.array([-np.sin(theta),np.cos(theta),0])
    vector(a,p,.55*et,BLUE,label=r"$r_\theta$")
    vector(a,p,[0,0,.55],RED,label=r"$r_z$",ls="--")
    vector(a,p,.55*er,"black",label=r"$n$")
    a.set(xlim=(-1.2,1.65),ylim=(-1.2,1.65),zlim=(-.85,1.1))
    a.set_box_aspect((2.85,2.85,1.95));a.view_init(elev=25,azim=-10)
    footer(a,r"$r_\theta\times r_z=R\,e_r$; outward")
    tt=np.linspace(0,2*np.pi,61); pp=np.linspace(.03,np.pi-.03,25)
    T,P=np.meshgrid(tt,pp)
    b.plot_wireframe(np.sin(P)*np.cos(T),np.sin(P)*np.sin(T),np.cos(P),
                     color="0.8",lw=.4,rstride=4,cstride=6)
    er=np.array([np.sin(phi)*np.cos(theta),np.sin(phi)*np.sin(theta),np.cos(phi)])
    ep=np.array([np.cos(phi)*np.cos(theta),np.cos(phi)*np.sin(theta),-np.sin(phi)])
    et=np.array([-np.sin(theta),np.cos(theta),0])
    vector(b,er,.55*ep,BLUE,label=r"$r_\varphi$")
    vector(b,er,.55*np.sin(phi)*et,RED,label=r"$r_\theta$",ls="--")
    vector(b,er,.8*er,"black",label=r"$n$")
    b.set(xlim=(-1.2,1.65),ylim=(-1.2,1.65),zlim=(-1.2,1.65))
    b.set_box_aspect((1,1,1));b.view_init(elev=24,azim=-10)
    footer(b,r"$r_\varphi\times r_\theta=R^2\sin\varphi\,e_r$; outward")
    save(fig,"fig-11-coordinate-surfaces")


def triple_product():
    fig,(a,b)=figure(("3d","2d"),height=107)
    u=np.array([1.3,0,0]); v=np.array([.4,1.,0]); w=np.array([.5,.3,1.2])
    base=np.array([np.zeros(3),u,u+v,v])
    for quad in [base,base+w]:
        a.add_collection3d(Poly3DCollection([quad],fc="0.95",ec="0.6",alpha=.35,lw=.7))
    for x in base: a.plot(*np.array([x,x+w]).T,color="0.6",lw=.8)
    vector(a,[0,0,0],u,BLUE,label=r"$a$")
    vector(a,[0,0,0],v,RED,label=r"$b$",ls="--")
    vector(a,[0,0,0],w,"black",label=r"$c$")
    vector(a,[.85,.5,0],[0,0,.6],"0.4",label=r"$n$",ls=":")
    a.set(xlim=(-.2,2.4),ylim=(-.2,1.7),zlim=(-.1,1.7))
    a.set_box_aspect((2.6,1.9,1.8));a.view_init(elev=25,azim=-55)
    footer(a,r"$A=\|a\times b\|$; $V=|(a\times b)\cdot c|$")
    q=float(np.hypot(.5,.3))
    b.plot([-.3,1.3],[0,0],color="0.6",lw=1.2)
    arrow(b,[0,0],[q,1.2],"black")
    arrow(b,[q,0],[q,1.2],BLUE,"--")
    b.plot([0,q],[0,0],color=RED,ls="--",lw=1.3)
    b.plot([q-.12,q-.12,q],[0,.12,.12],color="0.5",lw=.7)
    b.text(.13,.68,r"$c$",fontsize=9)
    b.text(q+.1,.6,r"$h=|c\cdot n|$",color=BLUE,fontsize=8)
    b.text(.15,-.2,r"$c_\parallel$",color=RED,fontsize=8)
    b.set(xlim=(-.35,1.4),ylim=(-.3,1.55),aspect="equal",
          xlabel="In-plane distance (dim.)",ylabel="Normal distance (dim.)")
    footer(b,r"Only normal height contributes: $V=A\,h$")
    save(fig,"fig-12-triple-product")



def flux_projection():
    fig,(a,b)=figure(("2d","3d"),height=109)
    fig.subplots_adjust(right=.90)
    # This is a section through the normal and the velocity: the omitted
    # tangential component is zero. All lengths and times are dimensionless.
    v=np.array([.7,.9])
    a.plot([-.35,1.25],[0,0],color="0.55",lw=1.2)
    a.plot([0,0],[-.2,1.45],color="0.65",lw=.8,ls=":")
    arrow(a,[0,0],v,RED)
    arrow(a,[0,0],[0,.9],BLUE,"--")
    a.plot([0,.7],[.9,.9],color="0.4",lw=1,ls=":")
    arrow(a,[0,0],[.7,0],"0.35")
    a.text(.72,.95,r"$v$",color=RED)
    a.text(-.30,.59,r"$v_n n$",color=BLUE,fontsize=8)
    a.text(.35,-.18,r"$v_\parallel$",color="0.35",fontsize=8)
    a.text(-.14,1.36,r"$+n$",fontsize=8)
    a.text(.70,1.28,r"$v_n=v\cdot n$",ha="center",fontsize=8)
    a.set(xlim=(-.4,1.35),ylim=(-.28,1.5),aspect="equal",
          xlabel="Tangential coordinate (dim.)",ylabel="Normal coordinate (dim.)")
    footer(a,r"Only normal projection contributes: $\Phi=v_n A$")
    base=np.array([[-.6,-.4,0],[.6,-.4,0],[.6,.4,0],[-.6,.4,0]])
    displacement=np.array([.7,0,.9])
    faces=[base,base+displacement]
    for i in range(4):faces.append(np.array([base[i],base[(i+1)%4],base[(i+1)%4]+displacement,base[i]+displacement]))
    b.add_collection3d(Poly3DCollection(faces,fc="0.94",ec="0.6",alpha=.22,lw=.7))
    vector(b,[0,0,0],displacement,RED,label=r"$v\,\Delta t$")
    vector(b,[.7,0,0],[0,0,.9],BLUE,label=None,ls="--")
    b.text(.78,.02,.39,r"$v_n\Delta t$",color=BLUE,fontsize=8)
    b.plot([0,.7],[0,0],[0,0],color="0.4",ls=":",lw=1)
    b.text(-.40,-.18,0,r"$A$",fontsize=9)
    b.set(xlim=(-.8,1.55),ylim=(-.65,.75),zlim=(-.1,1.35))
    b.set_box_aspect((2.35,1.4,1.45));b.view_init(elev=25,azim=-65)
    footer(b,r"Swept volume: $\Delta V=A\,v_n\Delta t$")
    save(fig,"fig-13-flux-projection")


def local_area():
    fig,(a,b)=figure(("2d","3d"),height=111)
    u0,v0,du,dv=.5,.4,.35,.3
    U,V=np.meshgrid(np.linspace(.12,1.03,12),np.linspace(.05,.95,12))
    for u in np.linspace(.15,1,8):a.plot([u,u],[.05,.95],color="0.88",lw=.5)
    for v in np.linspace(.05,.95,8):a.plot([.12,1.03],[v,v],color="0.88",lw=.5)
    a.add_patch(Rectangle((u0,v0),du,dv,fc="0.94",ec="0.45",lw=1))
    arrow(a,[u0,v0],[u0+du,v0],BLUE)
    arrow(a,[u0,v0],[u0,v0+dv],RED,"--")
    a.plot(u0,v0,"ko",ms=3)
    a.text(u0+.12,v0-.10,r"$du$",color=BLUE,fontsize=8)
    a.text(u0-.13,v0+.12,r"$dv$",color=RED,fontsize=8)
    a.text(.57,.54,r"$du\,dv$",fontsize=8)
    a.set(xlim=(.08,1.06),ylim=(.0,.98),aspect="equal",
          xlabel="$u$ (dim.)",ylabel="$v$ (dim.)")
    footer(a,r"Parameter rectangle at $(u,v)=(0.5,0.4)$")
    z=lambda u,v:.4*u*u+.3*v*v
    b.plot_wireframe(U,V,z(U,V),color="0.8",lw=.45,rstride=2,cstride=2)
    p=np.array([u0,v0,z(u0,v0)])
    ru=np.array([1,0,.8*u0]);rv=np.array([0,1,.6*v0])
    av,bv=ru*du,rv*dv
    tangent=np.array([p,p+av,p+av+bv,p+bv])
    b.add_collection3d(Poly3DCollection([tangent],fc="0.92",ec="0.35",alpha=.35,lw=.8,linestyle="--"))
    # Actual curved patch boundary, as distinct from its tangent approximation.
    h=np.linspace(0,1,50)
    for u,v in [(u0+du*h,np.full_like(h,v0)),(np.full_like(h,u0+du),v0+dv*h),
                (u0+du*(1-h),np.full_like(h,v0+dv)),(np.full_like(h,u0),v0+dv*(1-h))]:
        b.plot(u,v,z(u,v),color="0.4",lw=.8)
    vector(b,p,av,BLUE)
    b.text(*(p+av+np.array([0,-.08,.045])),r"$r_u\,du$",color=BLUE,fontsize=8)
    vector(b,p,bv,RED,ls="--")
    b.text(*(p+bv+np.array([.02,0,.07])),r"$r_v\,dv$",color=RED,fontsize=8)
    normal=np.cross(ru,rv);normal/=np.linalg.norm(normal)
    vector(b,p,.5*normal,"black",label=r"$n$")
    b.scatter(*p,color="black",s=9,depthshade=False)
    b.set(xlim=(.05,1.12),ylim=(-.03,1.04),zlim=(-.03,.87))
    b.set_box_aspect((1.07,1.07,.9));b.view_init(elev=29,azim=-65)
    footer(b,r"$dS=\|r_u\times r_v\|du\,dv$; $d\mathbf{S}=n\,dS$")
    save(fig,"fig-14-local-area")


def flux_example():
    fig,(a,b)=figure(("3d","2d"),height=112)
    patch(a);a.view_init(elev=25,azim=-65)
    P=np.array([.4,.4,1.2]);F=np.ones(3)
    N=np.array([-1.,-2,1]);n=N/np.linalg.norm(N)
    a.scatter(*P,color="black",s=10,depthshade=False)
    vector(a,P,.6*F,RED,label=r"$F$")
    vector(a,P,.9*n,BLUE,label=r"$n$",ls="--")
    footer(a,r"$n=(-1,-2,1)/\sqrt{6}$; $F=(1,1,1)$")
    normal=F@n;tangent=np.sqrt(F@F-normal*normal)
    b.axhline(0,color="0.7",lw=.8)
    b.axvline(0,color="0.7",lw=.8)
    arrow(b,[0,0],[0,.85],BLUE)
    arrow(b,[0,0],[tangent,normal],RED)
    arrow(b,[0,0],[0,normal],BLUE,"--")
    arrow(b,[0,0],[tangent,0],"0.3",":")
    b.plot([0,tangent],[normal,normal],color="0.55",lw=.8,ls=":")
    b.plot([tangent,tangent],[normal,0],color="0.55",lw=.8,ls=":")
    b.text(.10,.82,r"$+n$",color=BLUE,fontsize=8)
    b.text(-.32,-.55,r"$F_n$",color=BLUE,fontsize=8)
    b.text(1.58,-.87,r"$F$",color=RED,fontsize=8)
    b.text(1.07,.10,r"$F_\parallel$",color="0.3",fontsize=8)
    b.set(xlim=(-.38,1.92),ylim=(-1.10,1.10),aspect="equal",
          xlabel="Tangential component (dim.)",ylabel="Normal component (dim.)")
    footer(b,r"$F\cdot n=-2/\sqrt{6}$; $d\Phi=-2du\,dv$")
    save(fig,"fig-15-flux-example")


def previews():
    for part in range((len(EXPORTS)+1)//2):
        items=EXPORTS[part*2:(part+1)*2]
        canvas=Image.new("RGB",(1100,len(items)*740),"white"); draw=ImageDraw.Draw(canvas)
        for i,item in enumerate(items):
            draw.text((12,i*740+7),item["name"],fill="black")
            with Image.open(HERE/(item["name"]+".png")) as im:
                im.thumbnail((1090,700)); canvas.paste(im.convert("RGB"),((1100-im.width)//2,i*740+30))
        canvas.save(HERE/f"preview-{part+1}.png")
        ImageOps.grayscale(canvas).save(HERE/f"preview-{part+1}-gray.png")


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only",choices=["line-elements"],help="Regenerate one figure and refresh previews.")
    args=parser.parse_args()
    ss.grayscale_check([BLUE,RED])
    if args.only:
        manifest_path=HERE/"figure_manifest.json"
        previous=json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
        line_elements()
        refreshed={item["name"]:item for item in EXPORTS}
        EXPORTS[:]=[refreshed.pop(item["name"],item) for item in previous]
        EXPORTS.extend(refreshed.values())
    else:
        line_elements(); area_projections(); field_actions(); operator_elements()
        planar_normal(); coordinate_surfaces(); triple_product()
        flux_projection(); local_area(); flux_example()
    previews()
    (HERE/"figure_manifest.json").write_text(json.dumps(EXPORTS,indent=2),encoding="utf-8")
    for item in EXPORTS: assert abs(item["size_mm"][0]-178)<178*.03,item
    print(f"Verified {len(EXPORTS)} reproducible figure sets.")
