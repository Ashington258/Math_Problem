import numpy as np
import os
from manim import *
from utils.examples import COLORS

KERNEL, ROW, COLUMN, LEFT_NULL = [COLORS[k] for k in ('kernel', 'row', 'column', 'left_null')]
FONT = os.environ.get('LINEAR_MAP_FONT', 'Microsoft YaHei')


def caption(message, size=25, color=WHITE):
    return Text(message, font=FONT, font_size=size, color=color)


def formula(source, size=32, color=WHITE):
    return MathTex(source, font_size=size, color=color)


def basis_geometry(axes, basis, color, extent=2, offset=None):
    """Create 0D/1D/2D/3D geometry from a computed basis."""
    d, k = basis.shape
    offset = np.zeros(d) if offset is None else np.asarray(offset)
    def p(v):
        return axes.c2p(*v)
    if k == 0:
        return Dot(p(offset), color=color, radius=.065)
    if k == 1:
        v = basis[:, 0]
        return VGroup(Line(p(offset-extent*v), p(offset+extent*v), color=color, stroke_width=5),
                      Arrow(p(offset), p(offset+1.4*v), buff=0, color=color, stroke_width=4))
    if k == 2:
        b, c = basis[:, 0], basis[:, 1]
        corners = [p(offset+extent*(u*b+v*c)) for u, v in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        patch = Polygon(*corners, color=color, fill_color=color, fill_opacity=.16, stroke_width=2)
        grid = VGroup()
        for t in np.linspace(-extent, extent, 7):
            grid.add(Line(p(offset+t*b-extent*c), p(offset+t*b+extent*c), color=color, stroke_opacity=.3),
                     Line(p(offset+t*c-extent*b), p(offset+t*c+extent*b), color=color, stroke_opacity=.3))
        return VGroup(patch, grid)
    return VGroup(*(Line(p(offset-extent*basis[:, i]), p(offset+extent*basis[:, i]), color=color) for i in range(k)))


class PanelCamera(ThreeDCamera):
    """Translate only the projected 3D viewport; keep HUD coordinates intact."""
    panel_offset = np.zeros(3)

    def project_points(self, points):
        return super().project_points(points) + self.panel_offset


class Split3DScene(ThreeDScene):
    """True 3D geometry on one side, fixed screen geometry/text on the other."""
    def __init__(self, **kwargs):
        super().__init__(camera_class=PanelCamera, **kwargs)

    def prepare_camera(self, side="left"):
        self.set_camera_orientation(phi=66*DEGREES, theta=12*DEGREES,
                                    zoom=.90, focal_distance=100)
        self.camera.panel_offset = np.array([-3.35 if side == 'left' else 3.35, 0., 0.])

    def fixed(self, *objects):
        self.add_fixed_in_frame_mobjects(*objects)
        return objects

    def heading(self, title, left, right):
        heading = caption(title, 29).to_edge(UP, buff=.25)
        labels = VGroup(caption(left, 23).move_to([-3.35, 2.68, 0]),
                        caption(right, 23).move_to([3.35, 2.68, 0]))
        divider = Line([0, -2.45, 0], [0, 2.35, 0], color=GRAY, stroke_opacity=.25)
        self.fixed(heading, labels, divider)

    def note(self, message, equation=None, color=WHITE):
        if hasattr(self, '_note'):
            self.play(FadeOut(self._note), run_time=.35)
            self.remove_fixed_in_frame_mobjects(self._note)
        parts = [caption(message, 24, color)]
        if equation:
            parts.append(formula(equation, 30))
        self._note = VGroup(*parts).arrange(DOWN, buff=.15).to_edge(DOWN, buff=.22)
        if self._note.width > 13.2:
            self._note.scale_to_fit_width(13.2)
        self.fixed(self._note)
        self.play(FadeIn(self._note), run_time=.6)

    def axes3d(self, extent=2.7, length=4.3):
        return ThreeDAxes(x_range=[-extent,extent,1], y_range=[-extent,extent,1],
                           z_range=[-extent,extent,1], x_length=length,
                           y_length=length, z_length=length,
                           axis_config=dict(include_tip=True, stroke_width=2, color=GRAY_B))

    def marker3d(self, axes, coordinates, color=WHITE, radius=.05):
        # Billboard circles give clear 3D points without thousands of tiny sphere faces.
        dot = Dot(axes.c2p(*coordinates), radius=radius, color=color)
        self.camera.add_fixed_orientation_mobjects(dot)
        return dot

    def turn_camera(self, degrees=14, duration=3):
        self.move_camera(theta=self.camera.get_theta()+degrees*DEGREES, run_time=duration)
