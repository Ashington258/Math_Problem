import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 定义任意函数 f(x, y)
def f(x, y):
    """
    定义笛卡尔坐标系中的函数 f(x, y)
    可根据需要修改为其他函数，例如 x*y, x + y 等
    """
    return x**2 + y**2  # 示例函数 f(x, y) = x^2 + y^2


# 极坐标系中的函数 f(r cos θ, r sin θ)
def f_polar(r, theta):
    """
    将 f(x, y) 转换为极坐标形式，通过 x = r cos θ, y = r sin θ
    """
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return f(x, y)


# 1. 笛卡尔坐标系可视化
def plot_cartesian():
    # 创建 x, y 网格
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)  # 计算函数值

    # 绘制 3D 表面图
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")
    ax.set_title("Function f(x, y) in Cartesian Coordinates")
    fig.colorbar(surf)
    plt.show()


# 2. 极坐标系可视化
def plot_polar():
    # 创建 r, θ 网格
    r = np.linspace(0, 2, 100)  # r 从 0 到 2
    theta = np.linspace(0, 2 * np.pi, 100)  # θ 从 0 到 2π
    R, Theta = np.meshgrid(r, theta)
    Z = f_polar(R, Theta)  # 计算极坐标下的函数值

    # 绘制 3D 表面图（以 r, θ 为坐标）
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(R, Theta, Z, cmap="plasma")
    ax.set_xlabel("r")
    ax.set_ylabel("θ")
    ax.set_zlabel("f(r cos θ, r sin θ)")
    ax.set_title("Function f(r cos θ, r sin θ) in Polar Coordinates")
    fig.colorbar(surf)
    plt.show()


# 3. 可选：极坐标函数在笛卡尔网格上的投影
def plot_polar_in_cartesian():
    # 创建 r, θ 网格
    r = np.linspace(0, 2, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    R, Theta = np.meshgrid(r, theta)
    Z = f_polar(R, Theta)

    # 转换回笛卡尔坐标进行显示
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)

    # 绘制 3D 表面图
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="inferno")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(r cos θ, r sin θ)")
    ax.set_title("Polar Function Projected onto Cartesian Coordinates")
    fig.colorbar(surf)
    plt.show()


# 执行可视化
if __name__ == "__main__":
    print("Visualizing function in Cartesian coordinates...")
    plot_cartesian()
    print("Visualizing function in Polar coordinates...")
    plot_polar()
    print("Visualizing polar function projected onto Cartesian coordinates...")
    plot_polar_in_cartesian()
