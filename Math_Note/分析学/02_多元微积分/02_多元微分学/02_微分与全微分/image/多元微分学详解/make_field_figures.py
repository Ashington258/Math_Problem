"""Matched 2-D/3-D vector fields for divergence and curl concepts."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def space(ax, lim=1.35):
    ax.set_proj_type("ortho")
    ax.view_init(elev=25, azim=-55)
    ax.set(xlim=(-lim,lim),ylim=(-lim,lim),zlim=(-lim,lim))
    ax.set_box_aspect((1,1,1))
    ax.grid(False)
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        axis.pane.fill=False
        axis.pane.set_edgecolor("white")
    ax.set_xticks([-1,0,1]); ax.set_yticks([-1,0,1]); ax.set_zticks([-1,0,1])
    ax.tick_params(labelsize=7,pad=0)
    ax.set_xlabel(r"$x$ (dim.)",labelpad=0)
    ax.set_ylabel(r"$y$ (dim.)",labelpad=0)
    ax.set_zlabel(r"$z$ (dim.)",labelpad=0)


def canvas(p,rows,cols,height):
    fig=plt.figure(figsize=p.ss.figsize("double",height_mm=height))
    fig.subplots_adjust(left=.085,right=.94,bottom=.13,top=.94,wspace=.52,hspace=.48)
    fig.add_artist(Rectangle((0,0),1,1,transform=fig.transFigure,fc="none",ec="none",lw=0))
    axes=[]
    for k in range(rows*cols):
        ax=fig.add_subplot(rows,cols,k+1,projection="3d" if k>=cols else None)
        if k>=cols: space(ax)
        else: ax.minorticks_off()
        pos=ax.get_position(original=True)
        fig.text(pos.x0,pos.y1+.01,"ABCDEF"[k],fontsize=10,weight="bold")
        axes.append(ax)
    return fig,axes


def caption(ax,text):
    pos=ax.get_position(original=True)
    ax.figure.text(pos.x0+pos.width/2,pos.y0-.057,text,ha="center",va="top",fontsize=7)


def vector(ax,origin,value,color,label=None):
    ax.quiver(*origin,*value,color=color,linewidth=1.5,arrow_length_ratio=.15)
    if label: ax.text(*(np.asarray(origin)+value),label,color=color,fontsize=7)


def divergence(p):
    fig,axes=canvas(p,2,3,166)
    modes=["source","sink","uniform"]
    captions=[r"$\mathbf{F}_2=(x,y)^T,\quad\nabla\cdot\mathbf{F}_2=2$",
              r"$\mathbf{F}_2=(-x,-y)^T,\quad\nabla\cdot\mathbf{F}_2=-2$",
              r"$\mathbf{F}_2=(1,0)^T,\quad\nabla\cdot\mathbf{F}_2=0$"]
    for ax,mode,text in zip(axes[:3],modes,captions):
        p.field(ax,mode)
        ax.set_xlabel(r"$x$ (dim.)"); ax.set_ylabel(r"$y$ (dim.)")
        ax.set_xticks([-1,0,1]); ax.set_yticks([-1,0,1])
        ax.add_patch(Rectangle((-.55,-.55),1.1,1.1,fill=False,ec=p.BLUE,ls="--",lw=1))
        caption(ax,text)
    directions=np.array([[i,j,k] for i in [-1,1] for j in [-1,1] for k in [-1,1]]+
                        [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],dtype=float)
    directions/=np.linalg.norm(directions,axis=1)[:,None]
    points=.75*directions
    th,ph=np.meshgrid(np.linspace(0,2*np.pi,17),np.linspace(.05,np.pi-.05,11))
    sphere=np.array([np.sin(ph)*np.cos(th),np.sin(ph)*np.sin(th),np.cos(ph)])
    texts=[r"$\mathbf{F}_3=(x,y,z)^T,\quad\nabla\cdot\mathbf{F}_3=3$",
           r"$\mathbf{F}_3=(-x,-y,-z)^T,\quad\nabla\cdot\mathbf{F}_3=-3$",
           r"$\mathbf{F}_3=(1,0,0)^T,\quad\nabla\cdot\mathbf{F}_3=0$"]
    for ax,mode,text in zip(axes[3:],modes,texts):
        ax.plot_wireframe(*sphere,rstride=2,cstride=2,color="0.82",lw=.45)
        values=points if mode=="source" else -points if mode=="sink" else np.tile([1,0,0],(len(points),1))
        ax.quiver(*points.T,*(.55*values).T,color=p.BLUE,linewidth=1.2,arrow_length_ratio=.25)
        caption(ax,text)
    p.save(fig,"fig-08-divergence")


def curl(p):
    fig,axes=canvas(p,2,2,175)
    a,b,c,d=axes
    p.field(a,"rotation"); p.loop(a)
    p.field(b,"shear"); p.loop(b,color=p.RED)
    for ax in (a,b):
        ax.set_xlabel(r"$x$ (dim.)"); ax.set_ylabel(r"$y$ (dim.)")
    caption(a,r"$\mathbf{v}_2=(-y,x)^T:\quad(\nabla\times\mathbf{v}_2)_z=2$")
    caption(b,r"$\mathbf{v}_2=(y,0)^T:\quad(\nabla\times\mathbf{v}_2)_z=-1$")
    n=np.ones(3)/np.sqrt(3); u=np.array([1,-1,0])/np.sqrt(2); v=np.cross(n,u)
    c.view_init(elev=25,azim=-15)
    theta=np.linspace(0,2*np.pi,160)
    for h in [-.5,0,.5]:
        line=h*n[:,None]+.65*(u[:,None]*np.cos(theta)+v[:,None]*np.sin(theta))
        c.plot(*line,color="0.7",lw=.7)
        t=np.linspace(0,2*np.pi,7,endpoint=False)
        pts=h*n[:,None]+.65*(u[:,None]*np.cos(t)+v[:,None]*np.sin(t))
        vel=np.cross(n,pts.T).T
        c.quiver(*pts,*(.35*vel),color=p.BLUE,linewidth=1.1,arrow_length_ratio=.25)
    vector(c,np.zeros(3),.95*n,p.RED,label=r"$\nabla\times\mathbf{v}_3=2\mathbf{n}$")
    caption(c,r"$\mathbf{v}_3=\mathbf{n}\times\mathbf{r},\quad \mathbf{n}=(1,1,1)^T/\sqrt{3}$")
    t=np.linspace(-1.8,1.8,180)
    for phase in [0,2*np.pi/3,4*np.pi/3]:
        xyz=np.array([.65*np.cos(t+phase),.65*np.sin(t+phase),.5*t])
        d.plot(*xyz,color="0.7",lw=.7)
        ts=np.array([-1.2,0,1.2])
        pts=np.array([.65*np.cos(ts+phase),.65*np.sin(ts+phase),.5*ts])
        vel=np.array([-pts[1],pts[0],np.full(3,.5)])
        d.quiver(*pts,*(.3*vel),color=p.BLUE,linewidth=1.1,arrow_length_ratio=.25)
    vector(d,np.zeros(3),np.array([0,0,.9]),p.RED,label=r"$\nabla\times\mathbf{v}_3=2\mathbf{e}_z$")
    caption(d,r"$\mathbf{v}_3=(-y,x,1/2)^T$: rotation + translation")
    p.save(fig,"fig-10-curl")
