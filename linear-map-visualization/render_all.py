"""Render the five scenes in teaching order using the active Python environment."""
import argparse
from pathlib import Path
import subprocess
import sys

SCENES = [
    ('scene_02_r3_to_r2.py','R3ToR2'),
    ('scene_01_domain_codomain.py','DomainCodomain'),
    ('scene_03_r2_to_r3.py','R2ToR3'),
    ('scene_04_four_subspaces.py','FourSubspaces'),
    ('scene_05_square_matrix_trap.py','SquareMatrixTrap'),
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quality',choices=['l','m','h'],default='m')
    parser.add_argument('--fps',type=int,default=30)
    args = parser.parse_args()
    for file,scene in SCENES:
        subprocess.run([sys.executable,'-m','manim',f'-q{args.quality}',
                        '--fps',str(args.fps),'--progress_bar','none',
                        f'manim_scenes/{file}',scene],
                       cwd=Path(__file__).resolve().parent,check=True)
