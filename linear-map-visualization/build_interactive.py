"""Build all three standalone HTML files without requiring Manim/LaTeX."""
from interactive.common import export_page
from utils.examples import R3_TO_R2,R2_TO_R3,SQUARE_TRAP

if __name__=='__main__':
    a=(R3_TO_R2,'collapse','R³ → R² · 非方阵')
    b=(R2_TO_R3,'lift','R² → R³ · 嵌入')
    export_page('r3_to_r2.html','R³ → R²：核方向如何消失',{'A':a})
    export_page('r2_to_r3.html','R² → R³：二维网格嵌入三维',{'B':b})
    export_page('four_subspaces.html','四大子空间：先确定它属于哪一端',{
        'A':a,'B':b,'square':(SQUARE_TRAP,'collapse','R³ → R³ · 方阵反例')})
