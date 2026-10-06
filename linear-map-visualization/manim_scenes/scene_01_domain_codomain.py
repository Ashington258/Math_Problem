import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from manim_scenes.common import *


class DomainCodomain(Scene):
    def construct(self):
        title=caption("线性映射：先分清输入与输出",32).to_edge(UP,buff=.4)
        matrix=formula(r'A\in\mathbb R^{m\times n}',56)
        self.play(FadeIn(title),Write(matrix),run_time=1.5)
        self.wait(1)
        mapping=formula(r'\mathbb R^n_{\rm input}\xrightarrow{\quad A\quad}\mathbb R^m_{\rm output}',46).move_to([0,2.2,0])
        self.play(ReplacementTransform(matrix,mapping),run_time=2)
        boxes=VGroup(*(RoundedRectangle(width=5.0,height=3.8,corner_radius=.12,color=GRAY_B,stroke_opacity=.45).move_to([x,-.15,0]) for x in [-3.55,3.55]))
        labels=VGroup(caption('输入空间 / Domain',27).move_to([-3.55,1.2,0]),caption('输出空间 / Codomain',27).move_to([3.55,1.2,0]))
        dims=VGroup(caption('n = 输入维数 = 矩阵列数',22,ROW).move_to([-3.55,.65,0]),caption('m = 输出维数 = 矩阵行数',22,COLUMN).move_to([3.55,.65,0]))
        self.play(Create(boxes),FadeIn(labels),FadeIn(dims),run_time=2)
        relations=[formula(r'N(A)\subseteq\mathbb R^n',32,KERNEL).move_to([-3.55,-.2,0]),
                   formula(r'\operatorname{Row}(A)\subseteq\mathbb R^n',32,ROW).move_to([-3.55,-1.1,0]),
                   formula(r'\operatorname{Col}(A)\subseteq\mathbb R^m',32,COLUMN).move_to([3.55,-.2,0]),
                   formula(r'N(A^T)\subseteq\mathbb R^m',32,LEFT_NULL).move_to([3.55,-1.1,0])]
        for relation in relations:
            self.play(Write(relation),run_time=1)
            self.wait(.5)
        identity=formula(r'\dim N(A)+r(A)=n',38).move_to([0,-2.55,0])
        intuition=caption('输入维数 = 被忽略的维数 + 保留的独立方向数',25).move_to([0,-3.25,0])
        self.play(Write(identity),FadeIn(intuition),run_time=2)
        self.wait(3)
