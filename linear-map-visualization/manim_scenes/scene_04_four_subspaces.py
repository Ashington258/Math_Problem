import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from manim_scenes.common import *
from utils.examples import R3_TO_R2
from utils.linear_algebra import fundamental_subspaces


class FourSubspaces(Scene):
    def construct(self):
        title=caption('四大子空间：正确的配对位于同一端',32).to_edge(UP,buff=.35)
        heads=VGroup(caption('输入空间 / Domain · Rⁿ',25).move_to([-3.7,2.6,0]),caption('输出空间 / Codomain · Rᵐ',25).move_to([3.7,2.6,0]))
        self.play(FadeIn(title),FadeIn(heads))
        cards=VGroup()
        items=[(-3.7,1.2,ROW,r'\operatorname{Row}(A)',r'\dim=r'),(-3.7,-.85,KERNEL,r'N(A)',r'\dim=n-r'),
               (3.7,1.2,COLUMN,r'\operatorname{Col}(A)',r'\dim=r'),(3.7,-.85,LEFT_NULL,r'N(A^T)',r'\dim=m-r')]
        for x,y,color,name,dim in items:
            card=VGroup(RoundedRectangle(width=4.2,height=1.75,corner_radius=.1,color=color,fill_color=color,fill_opacity=.06),
                        VGroup(formula(name,33,color),formula(dim,27)).arrange(DOWN,buff=.15)).move_to([x,y,0])
            cards.add(card)
            self.play(FadeIn(card),run_time=.8)
        arrow=Arrow([-1.5,1.2,0],[1.5,1.2,0],buff=.12,color=COLUMN)
        self.play(GrowArrow(arrow),Write(formula('A',30).next_to(arrow,UP,buff=.15)))
        self.wait(1)
        # Zero is in Col(A); the kernel does not map to nonzero left-null vectors.
        zero=formula('0',26).move_to([2.05,.64,0])
        null_arrow=Arrow([-1.5,-.8,0],[1.83,.58,0],buff=.12,color=KERNEL)
        self.play(Write(zero),GrowArrow(null_arrow),run_time=1.5)
        zero_note=caption('核方向全部映到零',19,KERNEL).move_to([0,-.75,0])
        self.play(FadeIn(zero_note))
        first=formula(r'\mathbb R^n=\operatorname{Row}(A)\oplus N(A)',30).move_to([-3.55,-2.25,0])
        second=formula(r'\mathbb R^m=\operatorname{Col}(A)\oplus N(A^T)',30).move_to([3.55,-2.25,0])
        first.scale_to_fit_width(5.8);second.scale_to_fit_width(5.8)
        self.play(Write(first),Write(second),run_time=2)
        orthogonal=formula(r'N(A)^\perp=\operatorname{Row}(A),\qquad N(A^T)^\perp=\operatorname{Col}(A)',31).move_to([0,-3,0])
        self.play(Write(orthogonal),run_time=2)
        self.wait(2)
        s=fundamental_subspaces(R3_TO_R2)
        example=caption(f'例：2×3 矩阵，秩 {s.rank} → 输入 3={s.kernel.shape[1]}+{s.rank}；输出 2={s.rank}+{s.left_null.shape[1]}',24).move_to([0,-3.0,0])
        self.play(ReplacementTransform(orthogonal,example),run_time=1)
        self.wait(3)
