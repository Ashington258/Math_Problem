import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from manim_scenes.common import *
from utils.examples import SQUARE_TRAP
from utils.linear_algebra import fundamental_subspaces


class SquareMatrixTrap(Split3DScene):
    def construct(self):
        A=SQUARE_TRAP
        s=fundamental_subspaces(A)
        self.prepare_camera()
        self.camera.panel_offset=np.zeros(3)
        title=caption('03 · 方阵错觉：相同维数不代表相同角色',30).to_edge(UP,buff=.3)
        warning=caption('暂时识别两端坐标：观察反例',22,LEFT_NULL).move_to([0,2.95,0])
        equation=formula(r'A=\begin{pmatrix}0&1&0\\0&0&0\\0&0&0\end{pmatrix},\quad A(x,y,z)^T=(y,0,0)^T',20).move_to([0,2.18,0])
        self.fixed(title,warning,equation)
        axes=self.axes3d(length=3.8)
        kernel=basis_geometry(axes,s.kernel,KERNEL,2.3)
        column=basis_geometry(axes,s.column,COLUMN,2.8)
        self.play(Create(axes),FadeIn(kernel),Create(column),run_time=2)
        self.note('列空间的直线就在核平面里：它们并不是互补方向。',r'\operatorname{Col}(A)\subset N(A)')
        self.turn_camera(18,3)
        self.note('此例交集非零；普通和仅为核平面，直和条件也不成立。',r'N(A)+\operatorname{Col}(A)=N(A)\ne\mathbb R^3')
        self.wait(2)
        self.play(FadeOut(warning),FadeOut(column),run_time=.8)
        self.remove_fixed_in_frame_mobjects(warning)
        # Split the screen. Input stays in true 3D. Output is projected with the
        # same actual 3D camera into a separately labeled, fixed viewport.
        shift=ValueTracker(0)
        shift.add_updater(lambda tracker:setattr(self.camera,'panel_offset',np.array([-tracker.get_value(),0.,0.])))
        self.add(shift)
        self.play(shift.animate.set_value(3.35),run_time=2)
        labels=VGroup(caption('输入空间 / Domain · R³',23).move_to([-3.35,2.95,0]),
                      caption('输出空间 / Codomain · R³',23).move_to([3.35,2.95,0]))
        self.fixed(labels)
        # Independent output 3D viewport, rendered from its own coordinates.
        out_axes=self.axes3d(length=4.8)
        out_column=basis_geometry(out_axes,s.column,COLUMN,2.8)
        out_left=basis_geometry(out_axes,s.left_null,LEFT_NULL,2.3)
        output=VGroup(out_axes,out_column,out_left)
        originals=[(mob,mob.get_points().copy()) for mob in output.family_members_with_points()]
        for mob,points in originals:
            mob.set_points(self.camera.project_points(points)+np.array([6.7,0,0]))
        self.fixed(output)
        row=basis_geometry(axes,s.row,ROW,2.8)
        self.play(Create(row),FadeIn(output),run_time=1.5)
        self.note('两端坐标都是 R³，但输入端与输出端承担不同角色。',r'\mathbb R^3_{\rm input}\xrightarrow{A}\mathbb R^3_{\rm output}')
        self.wait(2)
        self.note('输入端的正确补空间是行空间；输出端的正确补空间是左核。',
                  r'\mathbb R^3=N(A)\oplus\operatorname{Row}(A)\qquad\mathbb R^3=\operatorname{Col}(A)\oplus N(A^T)')
        self.wait(3)
