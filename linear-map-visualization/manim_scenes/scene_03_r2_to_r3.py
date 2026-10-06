import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from manim_scenes.common import *
from utils.examples import R2_TO_R3
from utils.linear_algebra import fundamental_subspaces


class R2ToR3(Split3DScene):
    def construct(self):
        B=R2_TO_R3
        s=fundamental_subspaces(B)
        self.prepare_camera('right')
        self.heading('02 · 输入完整保留，输出只占一个平面','输入空间 / Domain · R²','输出空间 / Codomain · R³')
        inp=Axes(x_range=[-2.5,2.5,1],y_range=[-2.5,2.5,1],x_length=4.2,y_length=4.2,
                 axis_config=dict(color=GRAY_B,stroke_width=2)).move_to([-3.35,0,0])
        self.fixed(inp,inp.get_axis_labels(formula('x',24),formula('y',24)))
        axes=self.axes3d(extent=4.5,length=4.5)
        self.play(Create(axes),run_time=1.5)
        labels=axes.get_axis_labels(Text('u',font_size=22),Text('v',font_size=22),Text('w',font_size=22))
        self.add(labels)
        equation=formula(r'B=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\quad B(x,y)^T=(x,y,x+y)^T',27).move_to([0,2.1,0])
        self.fixed(equation)
        row=basis_geometry(inp,s.row,ROW,1.9)
        self.fixed(row)
        points=np.array([[x,y] for x in np.linspace(-2,2,5) for y in np.linspace(-2,2,5)])
        input_points=VGroup(*(Dot(inp.c2p(*p),radius=.035,color=ROW) for p in points))
        self.fixed(input_points)
        self.note('核空间只有零向量：两个独立输入方向都能保留下来。',r'N(B)=\{0\},\qquad\operatorname{Row}(B)=\mathbb R^2')
        self.wait(2)
        def lifted(p,t):
            embedded=np.r_[p,0.]
            return (1-t)*embedded+t*(B@p)
        t=ValueTracker(0)
        output_points=VGroup(*(self.marker3d(axes,lifted(p,0),COLUMN,.04) for p in points))
        edges=[(np.array([a,-2.]),np.array([a,2.])) for a in np.linspace(-2,2,5)]
        edges += [(np.array([-2.,a]),np.array([2.,a])) for a in np.linspace(-2,2,5)]
        grid=VGroup(*(Line(axes.c2p(*lifted(a,0)),axes.c2p(*lifted(b,0)),color=COLUMN,stroke_opacity=.6) for a,b in edges))
        self.play(Create(grid),FadeIn(output_points),run_time=1.5)
        self.note('右端先画二维网格的嵌入，再逐渐抬升到真正的像平面。',r'H_t(x,y)=(x,y,t(x+y));\quad H_1=B')
        output_points.add_updater(lambda group:[dot.move_to(axes.c2p(*lifted(p,t.get_value()))) for dot,p in zip(group,points)])
        grid.add_updater(lambda group:[line.put_start_and_end_on(axes.c2p(*lifted(a,t.get_value())),axes.c2p(*lifted(b,t.get_value()))) for line,(a,b) in zip(group,edges)])
        self.play(t.animate.set_value(1),run_time=5,rate_func=smooth)
        output_points.clear_updaters();grid.clear_updaters()
        plane=basis_geometry(axes,s.column,COLUMN,2.4)
        self.play(FadeIn(plane),run_time=1)
        self.note('整个二维输入成为 z=x+y 的平面；没有新增第三个独立方向。',
                  rf'\dim N(B)={s.kernel.shape[1]},\quad r(B)={s.rank},\quad 2=0+2')
        self.turn_camera(20,3)
        left_null=basis_geometry(axes,s.left_null,LEFT_NULL,3)
        self.play(Create(left_null),run_time=1.5)
        self.note('三维是输出空间的维数；真正可达的列空间仍然只有二维。',r'\mathbb R^3=\operatorname{Col}(B)\oplus N(B^T)',COLUMN)
        self.wait(3)
