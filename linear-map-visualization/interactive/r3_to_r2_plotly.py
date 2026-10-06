import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from interactive.common import export_page
from utils.examples import R3_TO_R2

if __name__=='__main__':
    export_page('r3_to_r2.html','R³ → R²：核方向如何消失',
                {'A':(R3_TO_R2,'collapse','R³ → R² · rank 1')})
