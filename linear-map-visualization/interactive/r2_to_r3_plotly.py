import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from interactive.common import export_page
from utils.examples import R2_TO_R3

if __name__=='__main__':
    export_page('r2_to_r3.html','R² → R³：二维网格嵌入三维',
                {'B':(R2_TO_R3,'lift','R² → R³ · rank 2')})
