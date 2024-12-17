from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# 定义复函数
def f(z):
    return np.exp(z)

# 生成复平面
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y
W = f(Z)

# 模和辐角
modulus = np.abs(W)
phase = np.angle(W)

# 绘制三维图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, modulus, facecolors=plt.cm.hsv((phase + np.pi) / (2 * np.pi)), cmap="hsv", edgecolor='none')
ax.set_title("复函数的三维表示")
plt.show()
