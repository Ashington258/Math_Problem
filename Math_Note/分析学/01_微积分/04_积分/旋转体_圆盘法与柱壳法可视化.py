from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


OUTPUT_PATH = Path(__file__).with_name("image") / "旋转体_圆盘法与柱壳法.png"
DISK_Y = 0.42
DISK_DY = 0.045
SHELL_X = 0.58
SHELL_DX = 0.045


def boundary(x: np.ndarray | float) -> np.ndarray | float:
    return 1 - np.asarray(x) ** 2


def style_plane_axis(axis: plt.Axes, title: str) -> None:
    axis.set_xlim(-0.08, 1.08)
    axis.set_ylim(-0.08, 1.08)
    axis.set_aspect("equal")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_title(title, loc="left", fontweight="bold")
    axis.spines[["top", "right"]].set_visible(False)


def draw_planar_slices(axes: np.ndarray) -> None:
    x = np.linspace(0, 1, 500)
    y = boundary(x)

    for axis in axes:
        axis.fill_between(x, 0, y, color="#8ecae6", alpha=0.55)
        axis.plot(x, y, color="#174a5b", linewidth=2.2)
        axis.axvline(0, color="#283618", linewidth=2.4)
        style_plane_axis(axis, axis.get_title())

    disk_radius = np.sqrt(1 - DISK_Y)
    axes[0].add_patch(
        Rectangle(
            (0, DISK_Y - DISK_DY / 2),
            disk_radius,
            DISK_DY,
            facecolor="#e63946",
            edgecolor="#9d0208",
            linewidth=1.5,
        )
    )
    axes[0].annotate(
        r"horizontal slice: $R(y)=\sqrt{1-y}$",
        xy=(disk_radius * 0.58, DISK_Y),
        xytext=(0.18, 0.67),
        arrowprops={"arrowstyle": "->", "color": "#9d0208"},
        color="#9d0208",
    )

    shell_height = float(boundary(SHELL_X))
    axes[1].add_patch(
        Rectangle(
            (SHELL_X - SHELL_DX / 2, 0),
            SHELL_DX,
            shell_height,
            facecolor="#f4a261",
            edgecolor="#bc4b10",
            linewidth=1.5,
        )
    )
    axes[1].annotate(
        r"vertical slice: $h(x)=1-x^2$",
        xy=(SHELL_X, shell_height * 0.55),
        xytext=(0.12, 0.88),
        arrowprops={"arrowstyle": "->", "color": "#9c3d00"},
        color="#9c3d00",
    )


def style_3d_axis(axis: plt.Axes, title: str) -> None:
    axis.set_xlim(-1.05, 1.05)
    axis.set_ylim(-1.05, 1.05)
    axis.set_zlim(0, 1.05)
    axis.set_box_aspect((1, 1, 0.8))
    axis.set_xlabel("x")
    axis.set_ylabel("z")
    axis.set_zlabel("y")
    axis.set_title(title, loc="left", fontweight="bold")
    axis.view_init(elev=24, azim=-55)


def draw_solid(axis: plt.Axes, method: str) -> None:
    theta = np.linspace(0, 2 * np.pi, 140)
    radius = np.linspace(0, 1, 90)
    theta_grid, radius_grid = np.meshgrid(theta, radius)
    x_surface = radius_grid * np.cos(theta_grid)
    z_surface = radius_grid * np.sin(theta_grid)
    y_surface = 1 - radius_grid**2

    axis.plot_surface(
        x_surface,
        z_surface,
        y_surface,
        color="#8ecae6",
        alpha=0.38,
        linewidth=0,
        antialiased=True,
    )
    axis.plot_surface(
        x_surface,
        z_surface,
        np.zeros_like(y_surface),
        color="#d8e2dc",
        alpha=0.25,
        linewidth=0,
    )
    axis.plot([0, 0], [0, 0], [0, 1.08], color="#283618", linewidth=2.4)

    if method == "disk":
        disk_radius = np.sqrt(1 - DISK_Y)
        disk_r = np.linspace(0, disk_radius, 60)
        disk_theta, disk_radius_grid = np.meshgrid(theta, disk_r)
        disk_x = disk_radius_grid * np.cos(disk_theta)
        disk_z = disk_radius_grid * np.sin(disk_theta)
        disk_y = np.full_like(disk_x, DISK_Y)
        axis.plot_surface(
            disk_x,
            disk_z,
            disk_y,
            color="#e63946",
            alpha=0.9,
            linewidth=0,
        )
        title = r"3D element: $dV=\pi R(y)^2\,dy$"
    else:
        shell_theta, shell_y = np.meshgrid(
            theta, np.linspace(0, float(boundary(SHELL_X)), 70)
        )
        shell_x = SHELL_X * np.cos(shell_theta)
        shell_z = SHELL_X * np.sin(shell_theta)
        axis.plot_surface(
            shell_x,
            shell_z,
            shell_y,
            color="#f4a261",
            alpha=0.88,
            linewidth=0,
        )
        title = r"3D element: $dV=2\pi xh(x)\,dx$"

    style_3d_axis(axis, title)


def main() -> None:
    figure = plt.figure(figsize=(13, 10), constrained_layout=True)
    grid = figure.add_gridspec(2, 2, height_ratios=(0.82, 1.18))

    disk_plane = figure.add_subplot(grid[0, 0])
    shell_plane = figure.add_subplot(grid[0, 1])
    disk_plane.set_title("Disk method: slice perpendicular to axis")
    shell_plane.set_title("Shell method: slice parallel to axis")
    draw_planar_slices(np.array([disk_plane, shell_plane]))

    disk_solid = figure.add_subplot(grid[1, 0], projection="3d")
    shell_solid = figure.add_subplot(grid[1, 1], projection="3d")
    draw_solid(disk_solid, "disk")
    draw_solid(shell_solid, "shell")

    figure.suptitle(
        r"Region $0\leq x\leq1$, $0\leq y\leq1-x^2$ rotated about the $y$-axis",
        fontsize=16,
        fontweight="bold",
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Saved visualization to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()