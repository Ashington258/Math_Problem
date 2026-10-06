"""First acceptance scene: collapse, affine fibers, and the true rectangular map."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from manim_scenes.common import *
from utils.examples import R3_TO_R2
from utils.linear_algebra import fundamental_subspaces, collapse


class R3ToR2(Split3DScene):
    def construct(self):
        A = R3_TO_R2
        s = fundamental_subspaces(A)
        self.prepare_camera()
        self.heading("01 · 核空间：映射忽略了什么？", "输入空间 / Domain · R³", "输出空间 / Codomain · R²")
        axes = self.axes3d()
        labels = axes.get_axis_labels(Text('x', font_size=22), Text('y', font_size=22), Text('z', font_size=22))
        out = Axes(x_range=[-4,4,1], y_range=[-2,2,1], x_length=5.0, y_length=3.5,
                   axis_config=dict(color=GRAY_B, stroke_width=2)).move_to([3.35,0,0])
        out_labels = out.get_axis_labels(formula('u',24),formula('v',24))
        self.fixed(out, out_labels)
        self.play(Create(axes), FadeIn(labels), run_time=2)
        mapping = formula(r"A=\begin{pmatrix}1&1&0\\0&0&0\end{pmatrix},\quad A(x,y,z)^T=(x+y,0)^T",27).move_to([0,2.15,0])
        self.fixed(mapping)
        self.note("列数决定输入维数；行数决定输出空间维数。")
        self.wait(2)

        kernel = basis_geometry(axes, s.kernel, KERNEL, 2)
        row = basis_geometry(axes, s.row, ROW, 2.5)
        col = basis_geometry(out, s.column, COLUMN, 4)
        ln = basis_geometry(out, s.left_null, LEFT_NULL, 1.7)
        self.fixed(col, ln)
        legend = VGroup(caption("粉：Kernel 平面 x+y=0",19,KERNEL), caption("蓝：Row(A) 有效输入方向",19,ROW),
                        caption("绿：Col(A) 可达输出",19,COLUMN), caption("黄：N(Aᵀ) 正交方向",19,LEFT_NULL)).arrange(DOWN,aligned_edge=LEFT,buff=.09).move_to([3.5,-2.10,0])
        self.fixed(legend)
        self.play(FadeIn(kernel),Create(row),run_time=2)
        self.note("行空间与核空间正交，且都属于三维输入端。", r"\operatorname{Row}(A)\perp N(A)")
        self.turn_camera(12,3)

        points = np.array([[x,y,z] for x in np.linspace(-2,2,5) for y in np.linspace(-2,2,5) for z in np.linspace(-2,2,5)])
        cloud = VGroup(*(self.marker3d(axes,p,radius=.037) for p in points))
        self.play(FadeIn(cloud),run_time=1.2)
        self.note("先在输入端收缩核方向：有效分量保留，核分量逐渐消失。", r"C_t x=P_{\rm Row}x+(1-t)P_Nx\quad (C_t:\mathbb R^3\to\mathbb R^3)")
        t = ValueTracker(0)
        cloud.add_updater(lambda group: [dot.move_to(axes.c2p(*p)) for dot,p in zip(group,collapse(points,s,t.get_value()))])
        self.play(t.animate.set_value(1),run_time=5,rate_func=smooth)
        cloud.clear_updaters()
        self.wait(1)
        self.note("这一步是输入端投影；再用 A 把保留的方向送到二维输出端。", r"AC_t x=Ax,\qquad A(\operatorname{Row}(A))=\operatorname{Col}(A)")
        # Screen transport is illustrative; endpoints are computed in their own spaces.
        outputs = points @ A.T
        output_cloud = VGroup(*(Dot(out.c2p(*p),radius=.047,color=COLUMN) for p in outputs))
        self.fixed(output_cloud)
        self.play(FadeOut(cloud),run_time=.8)
        self.wait(2)

        # Contrast ignored kernel motion with effective row-space motion.
        direction=s.row[:,0].copy()
        if (A@direction)[0]<0:
            direction=-direction
        image_direction=A@direction
        coefficient=ValueTracker(1)
        input_marker=self.marker3d(axes,direction,ROW,.08)
        output_marker=Dot(out.c2p(*image_direction),radius=.09,color=COLUMN)
        input_arrow=Arrow(axes.c2p(0,0,0),axes.c2p(*direction),buff=0,color=ROW)
        output_arrow=Arrow(out.c2p(0,0),out.c2p(*image_direction),buff=0,color=COLUMN)
        self.fixed(output_marker,output_arrow)
        self.play(FadeOut(output_cloud),FadeIn(input_marker),Create(input_arrow),run_time=.8)
        self.note('沿行空间的有效方向移动，输出沿列空间同步变化。',
                  r'v\in\operatorname{Row}(A):\quad A(sv)=sAv')
        input_marker.add_updater(lambda dot:dot.move_to(axes.c2p(*(coefficient.get_value()*direction))))
        output_marker.add_updater(lambda dot:dot.move_to(out.c2p(*(coefficient.get_value()*image_direction))))
        self.play(coefficient.animate.set_value(-1),run_time=2)
        self.play(coefficient.animate.set_value(1),run_time=2)
        input_marker.clear_updaters();output_marker.clear_updaters()
        self.play(FadeOut(input_marker),FadeOut(output_marker),FadeOut(input_arrow),FadeOut(output_arrow),run_time=.6)

        x0 = np.array([1.,0.,0.])
        shifts = np.array([[0.,0.],[1.3,0.],[-1.2,.9],[.4,-1.3]]) @ s.kernel.T
        fiber_points = x0 + shifts
        assert np.allclose(fiber_points @ A.T, A @ x0)
        fiber = basis_geometry(axes,s.kernel,KERNEL,1.7,offset=x0)
        dots = VGroup(*(self.marker3d(axes,p,radius=.08,color=KERNEL) for p in fiber_points))
        self.play(FadeOut(kernel),FadeIn(fiber),FadeIn(dots),run_time=1.5)
        self.note("同一个输出的全部原像，是核空间的一张平移平面。", r"A^{-1}(Ax_0)=x_0+N(A),\quad x_0=(1,0,0)^T")
        target = Dot(out.c2p(*(A@x0)),radius=.10,color=COLUMN)
        self.fixed(target)
        self.wait(2)
        for dot in dots:
            self.play(Indicate(dot,color=KERNEL),Indicate(target,color=COLUMN),run_time=.8)
        self.note("沿 Kernel 移动，输出完全不变。", r"A(x+z)=Ax\quad(z\in N(A))",KERNEL)
        # Show actual motion inside the affine fiber, with a fixed output.
        moving = self.marker3d(axes,fiber_points[0],radius=.10)
        self.add(moving)
        for p in fiber_points[1:]:
            self.play(moving.animate.move_to(axes.c2p(*p)),run_time=1.3)
        self.wait(1)
        self.note("核是一个二维子空间；消失的方向并非简单的两条坐标轴。",
                  rf"n=\dim N(A)+r(A):\qquad 3={s.kernel.shape[1]}+{s.rank}")
        self.turn_camera(-18,3)
        self.wait(3)
