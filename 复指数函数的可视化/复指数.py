import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 定义复指数函数
def f(z):
    return np.exp(z)

# 创建复平面
x = np.linspace(-2, 2, 400)  # 实部范围
y = np.linspace(-2, 2, 400)  # 虚部范围
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y  # 复平面上的点

# 计算函数值
W = f(Z)

# 模和辐角
modulus = np.abs(W)  # |f(z)|，表示为高度
phase = np.angle(W)  # arg(f(z))，用于颜色编码

# 设置颜色映射（HSV颜色空间）
hue = (phase + np.pi) / (2 * np.pi)  # 将辐角映射到 [0, 1]
brightness = np.log1p(modulus) / np.max(np.log1p(modulus))  # 控制亮度，使用 log 提高对比度
colors = plt.cm.hsv(hue)  # 转为 RGB
colors[..., :3] *= brightness[..., np.newaxis]  # 应用亮度

# 创建三维图
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制表面
surf = ax.plot_surface(X, Y, modulus, facecolors=colors, rstride=1, cstride=1, antialiased=True, linewidth=0)
ax.set_xlabel("Re(z)")
ax.set_ylabel("Im(z)")
ax.set_zlabel("|f(z)|")
ax.set_title("复指数函数 $e^z$ 的3D可视化")

# 调整视角
ax.view_init(elev=30, azim=120)

# 显示
plt.show()
