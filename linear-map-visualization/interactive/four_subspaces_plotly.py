import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from interactive.common import export_page
from utils.examples import R3_TO_R2,R2_TO_R3,SQUARE_TRAP

if __name__=='__main__':
    export_page('four_subspaces.html','四大子空间：先确定它属于哪一端',{
        'A':(R3_TO_R2,'collapse','R³ → R² · 非方阵'),
        'B':(R2_TO_R3,'lift','R² → R³ · 嵌入'),
        'square':(SQUARE_TRAP,'collapse','R³ → R³ · 方阵反例')})
