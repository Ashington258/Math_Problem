"""Nine analytic figures for Green, Stokes and Gauss.

Run: python make_figures.py. Outputs PDF/SVG/600-dpi PNG at 178-mm width.
Coordinates/field values are dimensionless. No randomness or empirical data.
3-D views are orthographic; surfaces are unshaded mathematical geometry.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon
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


def figure(kinds=("2d","3d"),height=104):
    fig=plt.figure(figsize=ss.figsize("double",height_mm=height))
    fig.subplots_adjust(left=.10,right=.94,bottom=.22,top=.89,wspace=.46)
    fig.add_artist(Rectangle((0,0),1,1,transform=fig.transFigure,fc="none",ec="none",lw=0))
    axes=[]
    for i,kind in enumerate(kinds):
        ax=fig.add_subplot(1,2,i+1,projection="3d" if kind=="3d" else None)
        if kind=="3d":
            ax.set_proj_type("ortho"); ax.view_init(elev=25,azim=-55)
            ax.set_box_aspect((1,1,1)); ax.grid(False)
            for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
                axis.pane.fill=False; axis.pane.set_edgecolor("white")
                axis.set_major_locator(MaxNLocator(3))
            ax.set_xlabel('$x$ (dim.)',labelpad=0)
            ax.set_ylabel('$y$ (dim.)',labelpad=0)
            ax.set_zlabel('$z$ (dim.)',labelpad=0)
            ax.tick_params(labelsize=7,pad=0)
        else:
            ax.minorticks_off()
            ax.set_xlabel('$x$ (dim.)'); ax.set_ylabel('$y$ (dim.)')
            ax.xaxis.set_major_locator(MaxNLocator(4)); ax.yaxis.set_major_locator(MaxNLocator(4))
        pos=ax.get_position(original=True)
        fig.text(pos.x0,.93,"AB"[i],fontsize=10,weight="bold")
        axes.append(ax)
    return fig,axes


def footer(ax,s):
    pos=ax.get_position(original=True)
    ax.figure.text(pos.x0+pos.width/2,.10,s,ha="center",va="top",fontsize=8)


def arrow(ax,p,q,color=BLUE,ls="-",lw=1.5):
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="-|>",color=color,
                linestyle=ls,lw=lw,mutation_scale=10,shrinkA=0,shrinkB=0),zorder=10)


def vector(ax,point,value,color=BLUE,label=None,ls="-"):
    point,value=np.asarray(point),np.asarray(value)
    ax.quiver(*point,*value,color=color,linewidth=1.3,arrow_length_ratio=.18,linestyle=ls)
    if label: ax.text(*(point+value),label,color=color,fontsize=8)


def plane(ax,lim=1.45):
    ax.set(xlim=(-lim,lim),ylim=(-lim,lim),aspect="equal")


def space(ax,lim=1.4):
    ax.set(xlim=(-lim,lim),ylim=(-lim,lim),zlim=(-lim,lim))


def circle(ax,r=1,center=(0,0),ccw=True,color=BLUE,fill=False):
    ax.add_patch(Circle(center,r,fc="0.95" if fill else "none",ec=color,lw=1.5))
    for theta in [0,np.pi/2,np.pi,3*np.pi/2]:
        d=.22 if ccw else -.22
        p=np.asarray(center)+r*np.array([np.cos(theta),np.sin(theta)])
        q=np.asarray(center)+r*np.array([np.cos(theta+d),np.sin(theta+d)])
        arrow(ax,p,q,color)


def ball(ax,r=1,color="0.75"):
    th,ph=np.meshgrid(np.linspace(0,2*np.pi,25),np.linspace(.04,np.pi-.04,17))
    ax.plot_wireframe(r*np.sin(ph)*np.cos(th),r*np.sin(ph)*np.sin(th),r*np.cos(ph),
                      rstride=2,cstride=2,color=color,lw=.55)


def samples():
    v=np.array([[i,j,k] for i in [-1,1] for j in [-1,1] for k in [-1,1]]+
               [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],dtype=float)
    return v/np.linalg.norm(v,axis=1)[:,None]


def cap(ax,curved=True,color="0.7"):
    r,t=np.meshgrid(np.linspace(0,1,9),np.linspace(0,2*np.pi,41))
    x,y=r*np.cos(t),r*np.sin(t); z=1-r*r if curved else np.zeros_like(r)
    ax.plot_wireframe(x,y,z,rstride=5,cstride=2,color=color,lw=.65)
    theta=np.linspace(0,2*np.pi,240)
    ax.plot(np.cos(theta),np.sin(theta),np.zeros_like(theta),color=BLUE,lw=1.6)


def save(fig,name):
    ss.save(fig,HERE/(name+".pdf"),also_png=True,dpi=600)
    ss.save(fig,HERE/(name+".svg"))
    EXPORTS.append({"name":name,"size_mm":list(ss.output_size_mm(HERE/(name+".pdf"))),"dpi":600})
    plt.close(fig)


def domains():
    fig,(a,b)=figure()
    circle(a,fill=True)
    a.text(0,0,'$D\\subset\\mathbb{R}^2$',ha="center",fontsize=10)
    a.text(.7,.95,'$C=\\partial D$',fontsize=8)
    plane(a)
    footer(a,"Area domain: boundary is a curve")
    ball(b); space(b)
    b.text(0,0,0,'$\\Omega\\subset\\mathbb{R}^3$',fontsize=10)
    vector(b,[.8,0,.6],[.3,0,.2],RED,label='$\\partial\\Omega$')
    footer(b,"Volume domain: boundary is a surface")
    save(fig,"fig-01-domains-boundaries")


def cancellation():
    fig,(a,b)=figure()
    for x in [0,1]:
        for y in [0,1]: a.add_patch(Rectangle((x,y),1,1,fill=False,ec="0.72",lw=.9))
    # Two adjacent CCW cells traverse their common edge in opposite directions.
    arrow(a,(.96,.18),(.96,.8),RED)
    arrow(a,(1.04,.8),(1.04,.18),RED,ls="--")
    arrow(a,(.2,0),(.8,0)); arrow(a,(1.2,0),(1.8,0))
    arrow(a,(2,.2),(2,.8)); arrow(a,(2,1.2),(2,1.8))
    arrow(a,(1.8,2),(1.2,2)); arrow(a,(.8,2),(.2,2))
    arrow(a,(0,1.8),(0,1.2)); arrow(a,(0,.8),(0,.2))
    a.text(.25,1.1,"Cell loops cancel\non shared edges",fontsize=8)
    a.set(xlim=(-.3,2.3),ylim=(-.3,2.3),aspect="equal")
    footer(a,'$\\int_e \\mathbf{F}\\cdot \\mathrm{d}\\mathbf{r}+\\int_{-e}\\mathbf{F}\\cdot \\mathrm{d}\\mathbf{r}=0$')
    for x0 in [0,1]:
        for x in [x0,x0+1]:
            b.plot([x]*5,[0,1,1,0,0],[0,0,1,1,0],color="0.6",lw=.8)
        for y in [0,1]:
            for z in [0,1]: b.plot([x0,x0+1],[y,y],[z,z],color="0.65",lw=.8)
    face=np.array([[1,0,0],[1,1,0],[1,1,1],[1,0,1]])
    b.add_collection3d(Poly3DCollection([face],fc="0.9",ec=RED,alpha=.5))
    vector(b,[1,.45,.45],[.6,0,0],RED,label='$\\mathbf{n}_1$')
    vector(b,[1,.55,.55],[-.6,0,0],RED,label='$\\mathbf{n}_2=-\\mathbf{n}_1$',ls="--")
    b.set(xlim=(-.1,2.2),ylim=(-.1,1.2),zlim=(-.1,1.2))
    b.set_box_aspect((2.3,1.3,1.3))
    footer(b,'$\\mathbf{F}\\cdot \\mathbf{n}_1+\\mathbf{F}\\cdot \\mathbf{n}_2=0$')
    save(fig,"fig-02-internal-cancellation")


def green():
    fig,(a,b)=figure(("2d","2d"))
    grid=np.linspace(-.8,.8,7); x,y=np.meshgrid(grid,grid); mask=x*x+y*y<.85**2
    for ax,radial in [(a,True),(b,False)]:
        plane(ax)
        circle(ax,fill=True)
        u,w=(x/2,y/2) if radial else (-y/2,x/2)
        ax.quiver(x[mask],y[mask],u[mask],w[mask],angles="xy",scale_units="xy",scale=2.1,
                  color="0.45",width=.006)
    arrow(a,(1,0),(1.34,0),RED,ls="--")
    a.text(1.12,.13,'$\\mathbf{n}$',color=RED)
    a.text(-.95,1.18,'$\\mathbf{F}=(x/2,y/2)$',fontsize=8)
    b.text(-.95,1.18,'$\\mathbf{F}=(-y/2,x/2)$',fontsize=8)
    footer(a,'Normal flux = $\\pi$; circulation = 0')
    footer(b,'Circulation = $\\pi$; normal flux = 0')
    save(fig,"fig-03-green-flux-circulation")


def orientation():
    fig,(a,b)=figure(("2d","2d"))
    circle(a,fill=True); circle(a,r=.45,ccw=False,color=RED)
    a.add_patch(Circle((0,0),.44,fc="white",ec="none"))
    arrow(a,(.45,0),(.15,0),RED,ls="--")
    arrow(a,(1,0),(1.3,0),RED,ls="--")
    a.text(-.65,1.18,"Outer: CCW",fontsize=8)
    a.text(-.34,-.1,"hole",fontsize=8)
    plane(a)
    footer(a,"Positive boundary: domain on the left")
    p=np.array([1.,1.])/np.sqrt(2); tangent=np.array([-1.,1.])/np.sqrt(2); normal=p.copy()
    theta=np.linspace(0,2*np.pi,160); b.plot(np.cos(theta),np.sin(theta),color="0.7",lw=1)
    arrow(b,p,p+.5*tangent,BLUE); arrow(b,p,p+.5*normal,RED,ls="--")
    # The formula below uses a general positively oriented unit tangent (t_x,t_y).
    b.text(.25,-.35,'$\\mathbf{n}=(T_y,-T_x)$',fontsize=9)
    b.text(1.05,1.06,'$\\mathbf{n}$',color=RED)
    b.text(.18,1.06,'$\\mathbf{T}$',color=BLUE)
    plane(b,1.5)
    footer(b,'$\\mathbf{F}\\cdot \\mathbf{n}\\,\\mathrm{d}s=P\\,\\mathrm{d}y-Q\\,\\mathrm{d}x$')
    save(fig,"fig-04-green-orientation")


def stokes_surfaces():
    fig,axs=figure(("3d","3d"))
    for ax,curved in zip(axs,[False,True]):
        cap(ax,curved)
        for t in np.linspace(0,2*np.pi,7,endpoint=False):
            pos=np.array([np.cos(t),np.sin(t),0])
            vector(ax,pos,.2*np.array([-pos[1],pos[0],0]),BLUE)
        xy=np.array([[.5,0],[-.5,0],[0,.5]])
        for x,y in xy:
            pos=np.array([x,y,1-x*x-y*y if curved else 0])
            n=np.array([2*x,2*y,1]) if curved else np.array([0,0,1])
            vector(ax,pos,.3*n/np.linalg.norm(n),RED,ls="--")
        vector(ax,[0,0,1 if curved else 0],[0,0,.45],"black",label='$\\nabla\\times\\mathbf{F}$')
        ax.set(xlim=(-1.35,1.35),ylim=(-1.35,1.35),zlim=(-.25,1.65))
        ax.set_box_aspect((2.7,2.7,1.9))
    footer(axs[0],'Disk: $\\iint (\\nabla\\times\\mathbf{F})\\cdot \\mathbf{n}\\,\\mathrm{d}S=2\\pi$')
    footer(axs[1],'Cap $z=1-r^2$: same flux $2\\pi$')
    save(fig,"fig-05-stokes-surfaces")


def stokes_tilted():
    fig,(a,b)=figure(("3d","2d"))
    n=np.ones(3)/np.sqrt(3); u=np.array([1,-1,0])/np.sqrt(2); v=np.cross(n,u)
    t=np.linspace(0,2*np.pi,200)
    boundary=u[:,None]*np.cos(t)+v[:,None]*np.sin(t)
    a.add_collection3d(Poly3DCollection([boundary.T],fc="0.94",ec=BLUE,alpha=.75))
    for theta in np.linspace(0,2*np.pi,7,endpoint=False):
        point=u*np.cos(theta)+v*np.sin(theta)
        vector(a,point,.22*np.cross(n,point),BLUE)
    vector(a,[0,0,0],.9*n,RED,label='$\\mathbf{n}$',ls="--")
    space(a)
    a.view_init(elev=24,azim=-20)
    footer(a,'$\\mathbf{F}=\\mathbf{n}\\times \\mathbf{r},\\quad \\nabla\\times\\mathbf{F}=2\\mathbf{n}$')
    b.bar([0,1,2],[2/3]*3,width=.55,color="0.78",edgecolor="black",hatch="//")
    b.set_xticks([0,1,2],['$c_x n_x$','$c_y n_y$','$c_z n_z$'])
    b.set(xlabel="Component contribution",ylabel="Projection (dim.)",ylim=(0,1.1))
    b.axhline(2/3,color=RED,lw=.8,ls="--")
    footer(b,'$\\mathbf{c}=\\nabla\\times\\mathbf{F}:\\quad \\mathbf{c}\\cdot \\mathbf{n}=2$')
    save(fig,"fig-06-stokes-tilted-disk")


def gauss_ball():
    fig,(a,b)=figure(("3d","2d"))
    ball(a); points=samples()
    a.quiver(*points.T,*(.25*points).T,color=BLUE,linewidth=1.1,arrow_length_ratio=.25)
    a.scatter([0,.3,-.3],[0,.2,-.2],[0,-.2,.2],marker="+",color=RED,s=22)
    space(a,1.45)
    footer(a,'$\\mathbf{F}=\\mathbf{r}:\\quad\\nabla\\cdot\\mathbf{F}=3,\\quad\\Phi=4\\pi$')
    z=np.linspace(-1,1,250); integrand=3*np.pi*(1-z*z)
    b.fill_between(z,integrand,color="0.9"); b.plot(z,integrand,color=BLUE)
    b.set(xlim=(-1,1),ylim=(0,11),xlabel='Slice height $z$ (dim.)',
          ylabel='$3\\,\\mathrm{Area}(D_z)$ (dim.)')
    footer(b,'$\\int_{-1}^{1}3\\pi(1-z^2)\\,\\mathrm{d}z=4\\pi$')
    save(fig,"fig-07-gauss-ball")


def gauss_closure():
    fig,axs=figure(("3d","3d"))
    for ax in axs:
        cap(ax,True)
        vector(ax,[.5,0,.75],[.3,0,.3],RED,label='$n_S$',ls="--")
        ax.set(xlim=(-1.35,1.35),ylim=(-1.35,1.35),zlim=(-.6,1.45))
        ax.set_box_aspect((2.7,2.7,2.05))
    theta=np.linspace(0,2*np.pi,100)
    rim=np.column_stack((np.cos(theta),np.sin(theta),np.zeros_like(theta)))
    axs[1].add_collection3d(Poly3DCollection([rim],fc="0.91",ec=BLUE,alpha=.5))
    vector(axs[1],[0,0,0],[0,0,-.45],RED,label='$n_{S_0}=-e_z$',ls="--")
    axs[1].text(0,0,.4,'$\\Omega$',fontsize=10)
    footer(axs[0],'$S$ has an edge: $\\partial S=C$')
    footer(axs[1],'$S\\cup S_0=\\partial\\Omega$: closed surface')
    save(fig,"fig-08-gauss-surface-closure")


def singular_shell():
    fig,(a,b)=figure(("2d","2d"))
    for ax,hole in [(a,False),(b,True)]:
        ax.add_patch(Circle((0,0),1,fc="0.95",ec=BLUE,lw=1.4))
        if hole: ax.add_patch(Circle((0,0),.42,fc="white",ec=RED,lw=1.4))
        for theta in np.linspace(0,2*np.pi,8,endpoint=False):
            n=np.array([np.cos(theta),np.sin(theta)])
            arrow(ax,n,1.25*n,BLUE)
            if hole: arrow(ax,.42*n,.22*n,RED,ls="--")
        ax.plot(0,0,"kx",ms=6,mew=1.4)
        plane(ax)
        ax.set_xlabel('$x$ (dim.)'); ax.set_ylabel('$z$ (dim.)')
    a.text(-.85,.1,"Undefined at origin",fontsize=8)
    b.text(-.32,-.1,"excluded",fontsize=7)
    footer(a,r"Ball: singularity invalidates Gauss")
    footer(b,'Shell: $\\Phi_{out}=4\\pi,\\quad\\Phi_{in}=-4\\pi$')
    save(fig,"fig-09-singularity-shell")


def previews():
    for part in range((len(EXPORTS)+2)//3):
        items=EXPORTS[part*3:(part+1)*3]
        canvas=Image.new("RGB",(1100,len(items)*655),"white")
        draw=ImageDraw.Draw(canvas)
        for k,item in enumerate(items):
            draw.text((12,k*655+7),item["name"],fill="black")
            with Image.open(HERE/(item["name"]+".png")) as im:
                im.thumbnail((1090,620))
                canvas.paste(im.convert("RGB"),((1100-im.width)//2,k*655+28))
        canvas.save(HERE/f"preview-{part+1}.png")
        ImageOps.grayscale(canvas).save(HERE/f"preview-{part+1}-gray.png")


if __name__=="__main__":
    ss.grayscale_check([BLUE,RED])
    domains(); cancellation(); green(); orientation()
    stokes_surfaces(); stokes_tilted(); gauss_ball(); gauss_closure(); singular_shell()
    previews()
    (HERE/"figure_manifest.json").write_text(json.dumps(EXPORTS,indent=2),encoding="utf-8")
    assert len(EXPORTS)==9
    for item in EXPORTS: assert abs(item["size_mm"][0]-178)<178*.03,item
    print("Verified nine 178-mm analytic figure sets.")
