import numpy as np
import matplotlib.pyplot as plt

# 定义复函数
def f(z):
    return z**2

# 生成复平面网格
x, y = np.linspace(-2, 2, 400), np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# 映射到新的平面
W = f(Z)

# 绘制形变前后的网格
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("原始复平面")
plt.contour(X, Y, np.real(Z), colors="blue", alpha=0.5)
plt.contour(X, Y, np.imag(Z), colors="red", alpha=0.5)
plt.axis("equal")

plt.subplot(1, 2, 2)
plt.title("变换后复平面")
plt.contour(np.real(W), np.imag(W), np.real(Z), colors="blue", alpha=0.5)
plt.contour(np.real(W), np.imag(W), np.imag(Z), colors="red", alpha=0.5)
plt.axis("equal")
plt.show()
